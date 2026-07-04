import unittest

from ragbench.eval import evaluate


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
        self.assertEqual(rows[0]["retrieved"][0]["doc"], "rag.md")
        self.assertIn("text_preview", rows[0]["retrieved"][0])


if __name__ == "__main__":
    unittest.main()
