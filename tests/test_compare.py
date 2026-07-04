import unittest

from ragbench.compare import parse_int_list, parse_optional_single_int, parse_str_list, run_chunk_size_comparison, run_client_comparison


class FakeEncoder:
    def encode(self, texts: list[str]) -> list[list[float]]:
        vectors = []
        for text in texts:
            if "RAG" in text or "retrieval" in text:
                vectors.append([1.0, 0.0])
            else:
                vectors.append([0.0, 1.0])
        return vectors


class CompareTest(unittest.TestCase):
    def test_parse_int_list(self) -> None:
        self.assertEqual(parse_int_list("1,3, 5"), [1, 3, 5])

    def test_parse_int_list_rejects_empty(self) -> None:
        with self.assertRaises(ValueError):
            parse_int_list("")

    def test_parse_str_list(self) -> None:
        self.assertEqual(parse_str_list("local-keyword, local-embedding"), ["local-keyword", "local-embedding"])

    def test_parse_optional_single_int(self) -> None:
        self.assertIsNone(parse_optional_single_int("120,300,600", "120,300,600"))
        self.assertEqual(parse_optional_single_int("300", "120,300,600"), 300)

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

    def test_run_client_comparison(self) -> None:
        from pathlib import Path
        from tempfile import TemporaryDirectory

        with TemporaryDirectory() as tmp:
            docs_dir = Path(tmp)
            (docs_dir / "rag.md").write_text("RAG uses retrieval before generation.", encoding="utf-8")
            questions = [
                {
                    "id": "q001",
                    "question": "How does retrieval help RAG?",
                    "expected_keywords": ["RAG", "retrieval"],
                    "gold_doc": "rag.md",
                }
            ]
            runs = run_client_comparison(
                questions,
                docs_dir,
                client_names=["local-keyword", "local-embedding"],
                top_k=1,
                embedding_encoder=FakeEncoder(),
            )
            self.assertEqual([run["name"] for run in runs], ["local-keyword", "local-embedding"])


if __name__ == "__main__":
    unittest.main()
