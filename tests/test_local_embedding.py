from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from ragbench.clients.local_embedding import LocalEmbeddingClient, cosine_similarity


class FakeEncoder:
    def encode(self, texts: list[str]) -> list[list[float]]:
        vectors = []
        for text in texts:
            lowered = text.lower()
            if "rag" in lowered or "retrieval" in lowered:
                vectors.append([1.0, 0.0])
            elif "cooking" in lowered:
                vectors.append([0.0, 1.0])
            else:
                vectors.append([0.2, 0.2])
        return vectors


class LocalEmbeddingClientTest(unittest.TestCase):
    def test_cosine_similarity(self) -> None:
        self.assertEqual(cosine_similarity([1, 0], [1, 0]), 1.0)
        self.assertEqual(cosine_similarity([1, 0], [0, 1]), 0.0)
        self.assertEqual(cosine_similarity([0, 0], [1, 0]), 0.0)

    def test_client_returns_semantic_match(self) -> None:
        with TemporaryDirectory() as tmp:
            docs_dir = Path(tmp)
            (docs_dir / "rag.md").write_text("RAG uses retrieval before generation.", encoding="utf-8")
            (docs_dir / "cooking.md").write_text("Cooking uses heat and ingredients.", encoding="utf-8")

            client = LocalEmbeddingClient(docs_dir, top_k=1, encoder=FakeEncoder())
            result = client.ask("How does retrieval help RAG?")

            self.assertEqual(result["citations"], ["rag.md"])
            self.assertEqual(result["retrieved"][0]["doc"], "rag.md")
            self.assertGreater(result["retrieved"][0]["score"], 0)


if __name__ == "__main__":
    unittest.main()
