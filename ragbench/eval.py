from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from statistics import mean
from typing import Any

from ragbench.clients import LocalKeywordClient, MockRagClient, OpenAICompatibleClient, RagFlowClient
from ragbench.html_report import render_eval_html
from ragbench.metrics import citation_hit, classify_failure, keyword_recall


def load_questions(path: Path) -> list[dict]:
    return json.loads(path.read_text(encoding="utf-8"))


def evaluate(questions: list[dict], client: Any) -> list[dict]:
    rows = []
    for item in questions:
        result = client.ask(item["question"])
        answer = result.get("answer", "")
        citations = result.get("citations", [])
        keyword_score = keyword_recall(answer, item.get("expected_keywords", []))
        citation_ok = citation_hit(citations, item.get("gold_doc"))
        failure_type = classify_failure(keyword_score, citation_ok, answer)
        rows.append(
            {
                "id": item["id"],
                "question": item["question"],
                "answer": answer,
                "citations": citations,
                "keyword_recall": round(keyword_score, 2),
                "citation_hit": citation_ok,
                "latency_ms": result.get("latency_ms", 0),
                "failure_type": failure_type,
            }
        )
    return rows


def summarize(rows: list[dict]) -> dict:
    citation_rate = sum(1 for row in rows if row["citation_hit"]) / len(rows) if rows else 0
    keyword_avg = mean(row["keyword_recall"] for row in rows) if rows else 0
    latency_avg = mean(row["latency_ms"] for row in rows) if rows else 0
    failure_counts: dict[str, int] = {}
    for row in rows:
        failure_type = row["failure_type"]
        failure_counts[failure_type] = failure_counts.get(failure_type, 0) + 1
    return {
        "questions": len(rows),
        "citation_hit_rate": round(citation_rate, 4),
        "average_keyword_recall": round(keyword_avg, 4),
        "average_latency_ms": round(latency_avg, 2),
        "failure_counts": failure_counts,
    }


def worst_cases(rows: list[dict], limit: int = 5) -> list[dict]:
    ranked = sorted(
        rows,
        key=lambda row: (
            row["failure_type"] == "ok",
            row["keyword_recall"],
            row["citation_hit"],
            row["latency_ms"],
        ),
    )
    return ranked[:limit]


def compact_rows(rows: list[dict], include_answers: bool = False) -> list[dict]:
    compacted = []
    for row in rows:
        item = dict(row)
        if not include_answers:
            item.pop("answer", None)
        compacted.append(item)
    return compacted


def render_report(rows: list[dict], client_name: str) -> str:
    summary = summarize(rows)
    lines = [
        "# RAGBench-CN Sample Report",
        "",
        "## Summary",
        "",
        f"- Client: {client_name}",
        f"- Questions: {summary['questions']}",
        f"- Citation hit rate: {summary['citation_hit_rate']:.2f}",
        f"- Average keyword recall: {summary['average_keyword_recall']:.2f}",
        f"- Average latency: {summary['average_latency_ms']:.2f} ms",
        "",
        "## Failure Types",
        "",
        "| Type | Count |",
        "| --- | ---: |",
    ]

    for failure_type, count in sorted(summary["failure_counts"].items()):
        lines.append(f"| {failure_type} | {count} |")

    lines.extend(
        [
            "",
            "## Details",
            "",
            "| ID | Keyword Recall | Citation Hit | Latency ms | Failure Type | Question |",
            "| --- | ---: | --- | ---: | --- | --- |",
        ]
    )

    for row in rows:
        lines.append(
            "| {id} | {keyword_recall:.2f} | {citation_hit} | {latency_ms:.2f} | {failure_type} | {question} |".format(
                **row
            )
        )
    lines.extend(
        [
            "",
            "## Worst Cases",
            "",
            "| ID | Keyword Recall | Citation Hit | Failure Type | Question |",
            "| --- | ---: | --- | --- | --- |",
        ]
    )
    for row in worst_cases(rows):
        lines.append(
            "| {id} | {keyword_recall:.2f} | {citation_hit} | {failure_type} | {question} |".format(
                **row
            )
        )
    lines.extend(
        [
            "",
            "## Notes",
            "",
            "- `mock` only validates the evaluation pipeline.",
            "- `local-keyword` is a simple retrieval baseline over local Markdown files.",
            "- Real production RAG quality should be tested after connecting a RAGFlow/OpenAI-compatible client.",
        ]
    )
    return "\n".join(lines)


def build_json_payload(rows: list[dict], include_answers: bool = False) -> dict:
    return {
        "summary": summarize(rows),
        "worst_cases": compact_rows(worst_cases(rows), include_answers=include_answers),
        "results": compact_rows(rows, include_answers=include_answers),
    }


def write_json_result(rows: list[dict], out: Path, include_answers: bool = False) -> None:
    payload = {
        **build_json_payload(rows, include_answers=include_answers),
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def require_value(value: str | None, name: str) -> str:
    if not value:
        raise SystemExit(f"Missing required value: {name}")
    return value


def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluate a RAG QA system with a Chinese question set.")
    parser.add_argument("--questions", required=True, help="Path to question set JSON.")
    parser.add_argument("--out", required=True, help="Path to Markdown report.")
    parser.add_argument("--json-out", help="Optional path to machine-readable JSON result.")
    parser.add_argument("--html-out", help="Optional path to HTML report.")
    parser.add_argument(
        "--client",
        choices=["mock", "local-keyword", "openai-compatible", "ragflow"],
        default="mock",
        help="Evaluation target client.",
    )
    parser.add_argument("--docs-dir", default="examples/docs", help="Markdown docs dir for local-keyword client.")
    parser.add_argument("--top-k", type=int, default=3, help="Number of local chunks to retrieve.")
    parser.add_argument("--chunk-size", type=int, help="Optional character chunk size for local-keyword client.")
    parser.add_argument("--base-url", help="Base URL for openai-compatible client.")
    parser.add_argument("--api-key", help="API key for openai-compatible client.")
    parser.add_argument("--model", help="Model name for openai-compatible client.")
    parser.add_argument("--chat-id", help="RAGFlow chat assistant ID.")
    parser.add_argument("--include-answers", action="store_true", help="Include full answers in JSON output.")
    parser.add_argument("--mock", action="store_true", help="Deprecated alias for --client mock.")
    args = parser.parse_args()

    client_name = "mock" if args.mock else args.client
    if client_name == "mock":
        client = MockRagClient()
    elif client_name == "local-keyword":
        client = LocalKeywordClient(Path(args.docs_dir), top_k=args.top_k, chunk_size=args.chunk_size)
    elif client_name == "openai-compatible":
        base_url = args.base_url or os.getenv("OPENAI_COMPATIBLE_BASE_URL")
        api_key = args.api_key or os.getenv("OPENAI_COMPATIBLE_API_KEY")
        model = args.model or os.getenv("OPENAI_COMPATIBLE_MODEL")
        client = OpenAICompatibleClient(
            base_url=require_value(base_url, "--base-url or OPENAI_COMPATIBLE_BASE_URL"),
            api_key=require_value(api_key, "--api-key or OPENAI_COMPATIBLE_API_KEY"),
            model=require_value(model, "--model or OPENAI_COMPATIBLE_MODEL"),
        )
    elif client_name == "ragflow":
        base_url = args.base_url or os.getenv("RAGFLOW_BASE_URL")
        api_key = args.api_key or os.getenv("RAGFLOW_API_KEY")
        chat_id = args.chat_id or os.getenv("RAGFLOW_CHAT_ID")
        model = args.model or os.getenv("RAGFLOW_MODEL") or "model"
        client = RagFlowClient(
            base_url=require_value(base_url, "--base-url or RAGFLOW_BASE_URL"),
            api_key=require_value(api_key, "--api-key or RAGFLOW_API_KEY"),
            chat_id=require_value(chat_id, "--chat-id or RAGFLOW_CHAT_ID"),
            model=model,
        )
    else:
        raise SystemExit(f"Unsupported client: {client_name}")

    questions = load_questions(Path(args.questions))
    rows = evaluate(questions, client)
    report = render_report(rows, client_name=client_name)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(report, encoding="utf-8")

    if args.json_out:
        write_json_result(rows, Path(args.json_out), include_answers=args.include_answers)
    if args.html_out:
        html_out = Path(args.html_out)
        html_out.parent.mkdir(parents=True, exist_ok=True)
        html_out.write_text(render_eval_html(rows, summarize(rows), client_name=client_name), encoding="utf-8")

    print(f"Report written to {out}")
    if args.json_out:
        print(f"JSON result written to {args.json_out}")
    if args.html_out:
        print(f"HTML report written to {args.html_out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
