from __future__ import annotations


def keyword_recall(answer: str, expected_keywords: list[str]) -> float:
    if not expected_keywords:
        return 1.0
    hit_count = sum(1 for keyword in expected_keywords if keyword in answer)
    return hit_count / len(expected_keywords)


def citation_hit(citations: list[str], gold_doc: str | None) -> bool:
    if not gold_doc:
        return True
    return any(gold_doc in citation for citation in citations)


def retrieval_precision_at_k(retrieved: list[dict], gold_doc: str | None) -> float | None:
    if not retrieved:
        return None
    if not gold_doc:
        return 1.0
    relevant_count = sum(1 for item in retrieved if gold_doc in str(item.get("doc", "")))
    return relevant_count / len(retrieved)


def retrieval_recall_at_k(retrieved: list[dict], gold_doc: str | None) -> float | None:
    if not retrieved:
        return None
    if not gold_doc:
        return 1.0
    return 1.0 if any(gold_doc in str(item.get("doc", "")) for item in retrieved) else 0.0


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
