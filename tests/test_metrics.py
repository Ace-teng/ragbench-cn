import unittest

from ragbench.eval import worst_cases
from ragbench.metrics import citation_hit, classify_failure, keyword_recall, retrieval_precision_at_k


class MetricsTest(unittest.TestCase):
    def test_keyword_recall_counts_expected_keywords(self) -> None:
        answer = "top-k 变大会提高召回，但也可能引入噪声并增加延迟。"
        score = keyword_recall(answer, ["召回", "噪声", "延迟", "精度"])
        self.assertEqual(score, 0.75)

    def test_keyword_recall_without_expected_keywords_is_full_score(self) -> None:
        self.assertEqual(keyword_recall("any answer", []), 1.0)

    def test_citation_hit_matches_gold_doc_substring(self) -> None:
        self.assertTrue(citation_hit(["docs/rag_basics.md"], "rag_basics.md"))

    def test_citation_hit_fails_when_gold_doc_missing(self) -> None:
        self.assertFalse(citation_hit(["docs/other.md"], "rag_basics.md"))

    def test_retrieval_precision_at_k_counts_relevant_chunks(self) -> None:
        retrieved = [
            {"doc": "rag_basics.md"},
            {"doc": "other.md"},
            {"doc": "rag_basics.md"},
        ]
        self.assertEqual(retrieval_precision_at_k(retrieved, "rag_basics.md"), 2 / 3)

    def test_retrieval_precision_at_k_returns_none_without_retrieved_chunks(self) -> None:
        self.assertIsNone(retrieval_precision_at_k([], "rag_basics.md"))

    def test_classify_failure_retrieval_miss(self) -> None:
        self.assertEqual(classify_failure(0.25, False, "partial answer"), "retrieval_miss")

    def test_classify_failure_keyword_missing(self) -> None:
        self.assertEqual(classify_failure(0.25, True, "partial answer"), "keyword_missing")

    def test_worst_cases_prioritizes_failures(self) -> None:
        rows = [
            {
                "id": "ok",
                "keyword_recall": 1.0,
                "citation_hit": True,
                "latency_ms": 1,
                "failure_type": "ok",
            },
            {
                "id": "bad",
                "keyword_recall": 0.25,
                "citation_hit": True,
                "latency_ms": 1,
                "failure_type": "keyword_missing",
            },
        ]
        self.assertEqual(worst_cases(rows, limit=1)[0]["id"], "bad")


if __name__ == "__main__":
    unittest.main()
