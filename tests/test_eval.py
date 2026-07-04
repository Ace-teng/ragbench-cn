import unittest

from ragbench.eval import diagnose_result, evaluate


class FakeClient:
    def ask(self, question: str) -> dict:
        return {
            "answer": "RAG uses retrieval.",
            "citations": ["rag.md"],
            "retrieved": [
                {
                    "doc": "rag.md",
                    "score": 3,
                    "text": "RAG uses retrieval before generation.",
                },
                {
                    "doc": "noise.md",
                    "score": 1,
                    "text": "This is a noisy but similar chunk.",
                },
            ],
            "latency_ms": 1.5,
        }


class EvalTest(unittest.TestCase):
    def test_evaluate_includes_retrieval_metrics_and_chunks(self) -> None:
        rows = evaluate(
            [
                {
                    "id": "q001",
                    "question": "What is RAG?",
                    "expected_keywords": ["RAG", "retrieval"],
                    "gold_doc": "rag.md",
                }
            ],
            FakeClient(),
        )

        self.assertEqual(rows[0]["retrieval_precision_at_k"], 0.5)
        self.assertEqual(rows[0]["retrieval_recall_at_k"], 1.0)
        self.assertEqual(rows[0]["gold_docs"], ["rag.md"])
        self.assertEqual(rows[0]["retrieved"][0]["doc"], "rag.md")
        self.assertIn("text_preview", rows[0]["retrieved"][0])
        self.assertEqual(rows[0]["diagnosis"], "ok: answer passed the current lightweight checks")

    def test_evaluate_accepts_multiple_gold_docs(self) -> None:
        rows = evaluate(
            [
                {
                    "id": "q001",
                    "question": "What is RAG?",
                    "expected_keywords": ["RAG", "retrieval"],
                    "gold_docs": ["rag.md", "missing.md"],
                }
            ],
            FakeClient(),
        )

        self.assertEqual(rows[0]["gold_docs"], ["rag.md", "missing.md"])
        self.assertEqual(rows[0]["retrieval_precision_at_k"], 0.5)
        self.assertEqual(rows[0]["retrieval_recall_at_k"], 0.5)

    def test_diagnose_result_marks_retrieval_miss(self) -> None:
        self.assertEqual(
            diagnose_result(
                keyword_score=0.2,
                citation_ok=False,
                answer="partial",
                precision_at_k=0,
                recall_at_k=0,
            ),
            "retrieval_miss: gold source was not retrieved",
        )

    def test_diagnose_result_marks_noisy_retrieval(self) -> None:
        self.assertEqual(
            diagnose_result(
                keyword_score=0.8,
                citation_ok=True,
                answer="answer",
                precision_at_k=0.33,
                recall_at_k=1,
            ),
            "noisy_retrieval: gold source was retrieved but top-k contains many non-gold chunks",
        )


if __name__ == "__main__":
    unittest.main()
