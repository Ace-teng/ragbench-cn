from __future__ import annotations

from typing import Sequence


GoldDocs = str | Sequence[str] | None


def normalize_gold_docs(gold_docs: GoldDocs) -> list[str]:
    if not gold_docs:
        return []
    if isinstance(gold_docs, str):
        return [gold_docs]
    return [str(item) for item in gold_docs if item]


def keyword_recall(answer: str, expected_keywords: list[str]) -> float:
    if not expected_keywords:
        return 1.0
    hit_count = sum(1 for keyword in expected_keywords if keyword in answer)
    return hit_count / len(expected_keywords)


def citation_hit(citations: list[str], gold_docs: GoldDocs) -> bool:
    normalized = normalize_gold_docs(gold_docs)
    if not normalized:
        return True
    return any(gold_doc in citation for gold_doc in normalized for citation in citations)


def retrieval_precision_at_k(retrieved: list[dict], gold_docs: GoldDocs) -> float | None:
    if not retrieved:
        return None
    normalized = normalize_gold_docs(gold_docs)
    if not normalized:
        return 1.0
    relevant_count = sum(
        1
        for item in retrieved
        if any(gold_doc in str(item.get("doc", "")) for gold_doc in normalized)
    )
    return relevant_count / len(retrieved)


def retrieval_recall_at_k(retrieved: list[dict], gold_docs: GoldDocs) -> float | None:
    if not retrieved:
        return None
    normalized = normalize_gold_docs(gold_docs)
    if not normalized:
        return 1.0
    hit_count = sum(
        1
        for gold_doc in normalized
        if any(gold_doc in str(item.get("doc", "")) for item in retrieved)
    )
    return hit_count / len(normalized)


def classify_failure(keyword_score: float, citation_ok: bool, answer: str) -> str:
    if not answer.strip():
        return "empty_answer"
    if not citation_ok and keyword_score < 0.5:
        return "retrieval_miss"
    if not citation_ok:
        return "citation_missing"
    if keyword_score < 0.5:
        return "keyword_missing"
    return "ok"
