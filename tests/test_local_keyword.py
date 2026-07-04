from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from ragbench.clients.local_keyword import LocalKeywordClient, split_by_char_size, split_markdown, tokenize


class LocalKeywordClientTest(unittest.TestCase):
    def test_tokenize_keeps_ascii_terms_and_chinese_bigrams(self) -> None:
        terms = tokenize("RAG 的 top-k 检索")
        self.assertIn("rag", terms)
        self.assertIn("top-k", terms)
        self.assertIn("检索", terms)

    def test_split_markdown_by_blank_lines(self) -> None:
        chunks = split_markdown("A\n\nB\nC\n\nD")
        self.assertEqual(chunks, ["A", "B\nC", "D"])

    def test_split_by_char_size(self) -> None:
        chunks = split_by_char_size("abcdef", 2)
        self.assertEqual(chunks, ["ab", "cd", "ef"])

    def test_client_returns_matching_doc_citation(self) -> None:
        with TemporaryDirectory() as tmp:
            docs_dir = Path(tmp)
            (docs_dir / "rag.md").write_text("RAG 使用检索增强生成。", encoding="utf-8")
            client = LocalKeywordClient(docs_dir)
            result = client.ask("什么是 RAG 检索？")
            self.assertEqual(result["citations"], ["rag.md"])
            self.assertIn("检索", result["answer"])

    def test_client_supports_chunk_size(self) -> None:
        with TemporaryDirectory() as tmp:
            docs_dir = Path(tmp)
            (docs_dir / "rag.md").write_text("第一段包含检索。\n\n第二段包含生成。", encoding="utf-8")
            client = LocalKeywordClient(docs_dir, top_k=2, chunk_size=6)
            self.assertGreaterEqual(len(client.chunks), 2)


if __name__ == "__main__":
    unittest.main()
