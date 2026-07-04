from __future__ import annotations

import math
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

from ragbench.clients.local_keyword import split_markdown_with_size


class Encoder(Protocol):
    def encode(self, texts: list[str]) -> list[list[float]]:
        pass


class SentenceTransformerEncoder:
    def __init__(self, model_name: str) -> None:
        try:
            from sentence_transformers import SentenceTransformer
        except ImportError as exc:
            raise ImportError(
                "local-embedding requires sentence-transformers. "
                "Install it with: pip install -e .[embedding]"
            ) from exc
        self.model = SentenceTransformer(model_name)

    def encode(self, texts: list[str]) -> list[list[float]]:
        vectors = self.model.encode(texts, normalize_embeddings=False)
        return [list(vector) for vector in vectors]


@dataclass(frozen=True)
class EmbeddingChunk:
    doc: str
    text: str
    vector: list[float]


def cosine_similarity(left: list[float], right: list[float]) -> float:
    dot = sum(a * b for a, b in zip(left, right))
    left_norm = math.sqrt(sum(value * value for value in left))
    right_norm = math.sqrt(sum(value * value for value in right))
    if left_norm == 0 or right_norm == 0:
        return 0.0
    return dot / (left_norm * right_norm)


class LocalEmbeddingClient:
    """Local semantic retrieval baseline over Markdown files.

    This client uses an embedding model to rank chunks by cosine similarity.
    It is optional because local embedding models add heavier dependencies.
    """

    def __init__(
        self,
        docs_dir: Path,
        top_k: int = 3,
        chunk_size: int | None = None,
        model_name: str = "paraphrase-multilingual-MiniLM-L12-v2",
        encoder: Encoder | None = None,
    ) -> None:
        self.docs_dir = docs_dir
        self.top_k = top_k
        self.chunk_size = chunk_size
        self.model_name = model_name
        self.encoder = encoder or SentenceTransformerEncoder(model_name)
        self.chunks = self._load_chunks(docs_dir)

    def ask(self, question: str) -> dict:
        start = time.perf_counter()
        query_vector = self.encoder.encode([question])[0]
        ranked = sorted(
            (
                (cosine_similarity(query_vector, chunk.vector), chunk)
                for chunk in self.chunks
            ),
            key=lambda item: item[0],
            reverse=True,
        )
        selected_items = [(score, chunk) for score, chunk in ranked[: self.top_k] if score > 0]
        selected = [chunk for score, chunk in selected_items]
        if not selected:
            return {
                "answer": "",
                "citations": [],
                "retrieved": [],
                "latency_ms": round((time.perf_counter() - start) * 1000, 2),
            }

        answer = "\n\n".join(chunk.text for chunk in selected)
        citations = list(dict.fromkeys(chunk.doc for chunk in selected))
        retrieved = [
            {
                "doc": chunk.doc,
                "score": float(round(score, 4)),
                "text": chunk.text,
            }
            for score, chunk in selected_items
        ]
        return {
            "answer": answer,
            "citations": citations,
            "retrieved": retrieved,
            "latency_ms": round((time.perf_counter() - start) * 1000, 2),
        }

    def _load_chunks(self, docs_dir: Path) -> list[EmbeddingChunk]:
        raw_chunks: list[tuple[str, str]] = []
        for path in sorted(docs_dir.rglob("*.md")):
            relative_doc = path.relative_to(docs_dir).as_posix()
            text = path.read_text(encoding="utf-8")
            for raw_chunk in split_markdown_with_size(text, self.chunk_size):
                raw_chunks.append((relative_doc, raw_chunk))
        if not raw_chunks:
            raise ValueError(f"No Markdown documents found in {docs_dir}")

        vectors = self.encoder.encode([text for _, text in raw_chunks])
        return [
            EmbeddingChunk(doc=doc, text=text, vector=list(vector))
            for (doc, text), vector in zip(raw_chunks, vectors)
        ]
