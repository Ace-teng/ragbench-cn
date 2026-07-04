import unittest

from ragbench.compare import parse_int_list, run_chunk_size_comparison


class CompareTest(unittest.TestCase):
    def test_parse_int_list(self) -> None:
        self.assertEqual(parse_int_list("1,3, 5"), [1, 3, 5])

    def test_parse_int_list_rejects_empty(self) -> None:
        with self.assertRaises(ValueError):
            parse_int_list("")

    def test_run_chunk_size_comparison(self) -> None:
        from pathlib import Path
        from tempfile import TemporaryDirectory

        with TemporaryDirectory() as tmp:
            docs_dir = Path(tmp)
            (docs_dir / "rag.md").write_text("RAG 使用检索增强生成。", encoding="utf-8")
            questions = [
                {
                    "id": "q001",
                    "question": "什么是 RAG 检索？",
                    "expected_keywords": ["检索"],
                    "gold_doc": "rag.md",
                }
            ]
            runs = run_chunk_size_comparison(questions, docs_dir, top_k=1, chunk_sizes=[10, 50])
            self.assertEqual([run["name"] for run in runs], ["chunk_size=10", "chunk_size=50"])


if __name__ == "__main__":
    unittest.main()
