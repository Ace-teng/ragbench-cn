from __future__ import annotations

import argparse
import json
from pathlib import Path

from ragbench.clients import LocalEmbeddingClient, LocalKeywordClient
from ragbench.eval import compact_rows, evaluate, load_questions, summarize, worst_cases
from ragbench.html_report import render_comparison_html


def parse_int_list(raw: str) -> list[int]:
    values = []
    for item in raw.split(","):
        item = item.strip()
        if item:
            values.append(int(item))
    if not values:
        raise ValueError("expected at least one integer")
    return values


def parse_str_list(raw: str) -> list[str]:
    values = [item.strip() for item in raw.split(",") if item.strip()]
    if not values:
        raise ValueError("expected at least one value")
    return values


def parse_optional_single_int(raw: str, default_raw: str) -> int | None:
    if raw == default_raw:
        return None
    values = parse_int_list(raw)
    if len(values) != 1:
        raise ValueError("expected exactly one integer")
    return values[0]


def run_top_k_comparison(
    questions: list[dict],
    docs_dir: Path,
    top_k_values: list[int],
    chunk_size: int | None = None,
) -> list[dict]:
    runs = []
    for top_k in top_k_values:
        client = LocalKeywordClient(docs_dir, top_k=top_k, chunk_size=chunk_size)
        rows = evaluate(questions, client)
        runs.append(
            {
                "name": f"top_k={top_k}",
                "client": "local-keyword",
                "top_k": top_k,
                "summary": summarize(rows),
                "worst_cases": worst_cases(rows, limit=3),
            }
        )
    return runs


def run_chunk_size_comparison(
    questions: list[dict],
    docs_dir: Path,
    top_k: int,
    chunk_sizes: list[int],
) -> list[dict]:
    runs = []
    for chunk_size in chunk_sizes:
        client = LocalKeywordClient(docs_dir, top_k=top_k, chunk_size=chunk_size)
        rows = evaluate(questions, client)
        runs.append(
            {
                "name": f"chunk_size={chunk_size}",
                "client": "local-keyword",
                "top_k": top_k,
                "chunk_size": chunk_size,
                "summary": summarize(rows),
                "worst_cases": worst_cases(rows, limit=3),
            }
        )
    return runs


def run_client_comparison(
    questions: list[dict],
    docs_dir: Path,
    client_names: list[str],
    top_k: int,
    chunk_size: int | None = None,
    embedding_model: str = "paraphrase-multilingual-MiniLM-L12-v2",
    embedding_encoder=None,
) -> list[dict]:
    runs = []
    for client_name in client_names:
        if client_name == "local-keyword":
            client = LocalKeywordClient(docs_dir, top_k=top_k, chunk_size=chunk_size)
        elif client_name == "local-embedding":
            client = LocalEmbeddingClient(
                docs_dir,
                top_k=top_k,
                chunk_size=chunk_size,
                model_name=embedding_model,
                encoder=embedding_encoder,
            )
        else:
            raise ValueError(f"unsupported comparison client: {client_name}")

        rows = evaluate(questions, client)
        runs.append(
            {
                "name": client_name,
                "client": client_name,
                "top_k": top_k,
                "chunk_size": chunk_size,
                "summary": summarize(rows),
                "worst_cases": worst_cases(rows, limit=3),
            }
        )
    return runs


def render_comparison_report(runs: list[dict], title: str, notes: list[str]) -> str:
    lines = [
        f"# {title}",
        "",
        "## Summary",
        "",
        "| Run | Citation Hit Rate | Avg Keyword Recall | Avg Precision@k | Avg Recall@k | Avg Latency ms | Failure Counts |",
        "| --- | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for run in runs:
        summary = run["summary"]
        failure_counts = ", ".join(
            f"{key}={value}" for key, value in sorted(summary["failure_counts"].items())
        )
        lines.append(
            "| {name} | {citation:.2f} | {keyword:.2f} | {precision} | {recall} | {latency:.2f} | {failures} |".format(
                name=run["name"],
                citation=summary["citation_hit_rate"],
                keyword=summary["average_keyword_recall"],
                precision=(
                    f"{summary['average_retrieval_precision_at_k']:.2f}"
                    if summary.get("average_retrieval_precision_at_k") is not None
                    else "N/A"
                ),
                recall=(
                    f"{summary['average_retrieval_recall_at_k']:.2f}"
                    if summary.get("average_retrieval_recall_at_k") is not None
                    else "N/A"
                ),
                latency=summary["average_latency_ms"],
                failures=failure_counts or "-",
            )
        )
    lines.extend(
        [
            "",
            "## How To Read",
            "",
            "- Compare citation hit rate, keyword recall, precision@k, recall@k, latency, and failure counts together.",
            "- Higher recall is not always better if precision drops sharply.",
            "- Local baselines are useful for controlled experiments, but production RAG should be tested with real services.",
        ]
    )
    if notes:
        lines.extend(["", "## Experiment Notes", ""])
        lines.extend(f"- {note}" for note in notes)
    lines.extend(["", "## Worst Cases By Run", ""])
    for run in runs:
        lines.extend([f"### {run['name']}", ""])
        lines.extend(
            [
                "| ID | Keyword Recall | Citation Hit | Failure Type | Question |",
                "| --- | ---: | --- | --- | --- |",
            ]
        )
        for row in run.get("worst_cases", []):
            lines.append(
                "| {id} | {keyword_recall:.2f} | {citation_hit} | {failure_type} | {question} |".format(
                    **row
                )
            )
        lines.append("")
    return "\n".join(lines)


def compact_runs(runs: list[dict], include_answers: bool = False) -> list[dict]:
    compacted = []
    for run in runs:
        item = dict(run)
        item["worst_cases"] = compact_rows(run.get("worst_cases", []), include_answers=include_answers)
        compacted.append(item)
    return compacted


def write_json(runs: list[dict], out: Path, include_answers: bool = False) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        json.dumps({"runs": compact_runs(runs, include_answers=include_answers)}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def main() -> int:
    default_chunk_sizes = "120,300,600"
    parser = argparse.ArgumentParser(description="Compare RAG evaluation settings.")
    parser.add_argument("--questions", required=True, help="Path to question set JSON.")
    parser.add_argument("--docs-dir", default="examples/docs", help="Markdown docs dir.")
    parser.add_argument(
        "--mode",
        choices=["top-k", "chunk-size", "client"],
        default="top-k",
        help="Comparison mode.",
    )
    parser.add_argument("--clients", default="local-keyword,local-embedding", help="Comma-separated clients for client mode.")
    parser.add_argument("--top-k", default="1,3,5", help="Comma-separated top-k values.")
    parser.add_argument("--chunk-size", default=default_chunk_sizes, help="Comma-separated chunk sizes.")
    parser.add_argument(
        "--embedding-model",
        default="paraphrase-multilingual-MiniLM-L12-v2",
        help="SentenceTransformers model name for local-embedding client.",
    )
    parser.add_argument("--out", required=True, help="Path to Markdown comparison report.")
    parser.add_argument("--json-out", help="Optional path to machine-readable JSON result.")
    parser.add_argument("--html-out", help="Optional path to HTML comparison report.")
    parser.add_argument("--include-answers", action="store_true", help="Include full answers in JSON output.")
    args = parser.parse_args()

    questions = load_questions(Path(args.questions))
    if args.mode == "top-k":
        runs = run_top_k_comparison(
            questions=questions,
            docs_dir=Path(args.docs_dir),
            top_k_values=parse_int_list(args.top_k),
        )
        title = "RAGBench-CN Top-k Comparison"
        notes = [
            "Top-k controls how many retrieved chunks are returned.",
            "In real RAG systems, larger top-k may improve recall but can add noise and latency.",
        ]
    elif args.mode == "chunk-size":
        top_k_values = parse_int_list(args.top_k)
        if len(top_k_values) != 1:
            raise SystemExit("--mode chunk-size expects exactly one --top-k value")
        runs = run_chunk_size_comparison(
            questions=questions,
            docs_dir=Path(args.docs_dir),
            top_k=top_k_values[0],
            chunk_sizes=parse_int_list(args.chunk_size),
        )
        title = "RAGBench-CN Chunk Size Comparison"
        notes = [
            "Chunk size controls how large each retrievable text fragment is.",
            "Small chunks may miss context; large chunks may carry more unrelated content.",
        ]
    else:
        top_k_values = parse_int_list(args.top_k)
        if len(top_k_values) != 1:
            raise SystemExit("--mode client expects exactly one --top-k value")
        runs = run_client_comparison(
            questions=questions,
            docs_dir=Path(args.docs_dir),
            client_names=parse_str_list(args.clients),
            top_k=top_k_values[0],
            chunk_size=parse_optional_single_int(args.chunk_size, default_chunk_sizes),
            embedding_model=args.embedding_model,
        )
        title = "RAGBench-CN Client Comparison"
        notes = [
            "Client comparison keeps the same questions and docs while changing retrieval strategy.",
            "`local-keyword` ranks chunks by lexical overlap.",
            "`local-embedding` ranks chunks by vector similarity and requires the optional embedding dependency.",
        ]

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render_comparison_report(runs, title=title, notes=notes), encoding="utf-8")
    if args.json_out:
        write_json(runs, Path(args.json_out), include_answers=args.include_answers)
    if args.html_out:
        html_out = Path(args.html_out)
        html_out.parent.mkdir(parents=True, exist_ok=True)
        html_out.write_text(render_comparison_html(runs, title=title, notes=notes), encoding="utf-8")

    print(f"Comparison report written to {out}")
    if args.json_out:
        print(f"JSON result written to {args.json_out}")
    if args.html_out:
        print(f"HTML report written to {args.html_out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
