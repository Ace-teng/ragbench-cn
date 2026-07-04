from __future__ import annotations

import re
import time
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Chunk:
    doc: str
    text: str
    terms: set[str]


def tokenize(text: str) -> set[str]:
    text = text.lower()
    ascii_terms = re.findall(r"[a-z0-9][a-z0-9\-]+", text)
    chinese_chars = re.findall(r"[\u4e00-\u9fff]", text)
    chinese_bigrams = [
        chinese_chars[index] + chinese_chars[index + 1]
        for index in range(len(chinese_chars) - 1)
    ]
    return set(ascii_terms + chinese_chars + chinese_bigrams)


def split_markdown(text: str) -> list[str]:
    chunks = []
    current: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            if current:
                chunks.append("\n".join(current))
                current = []
            continue
        current.append(stripped)
    if current:
        chunks.append("\n".join(current))
    return chunks


def split_by_char_size(text: str, chunk_size: int) -> list[str]:
    if chunk_size <= 0:
        return [text]
    compact = re.sub(r"\s+", " ", text).strip()
    if not compact:
        return []
    return [
        compact[index : index + chunk_size].strip()
        for index in range(0, len(compact), chunk_size)
        if compact[index : index + chunk_size].strip()
    ]


def split_markdown_with_size(text: str, chunk_size: int | None = None) -> list[str]:
    paragraph_chunks = split_markdown(text)
    if not chunk_size:
        return paragraph_chunks
    chunks: list[str] = []
    for paragraph in paragraph_chunks:
        chunks.extend(split_by_char_size(paragraph, chunk_size))
    return chunks


class LocalKeywordClient:
    """Small retrieval baseline over local Markdown files.

    It is intentionally simple: no embedding, no rerank, no LLM. The goal is to
    expose the retrieval/evaluation loop before wiring a real RAG system.
    """

    def __init__(self, docs_dir: Path, top_k: int = 3, chunk_size: int | None = None) -> None:
        self.docs_dir = docs_dir
        self.top_k = top_k
        self.chunk_size = chunk_size
        self.chunks = self._load_chunks(docs_dir)

    def ask(self, question: str) -> dict:
        start = time.perf_counter()
        query_terms = tokenize(question)
        ranked = sorted(
            (
                (self._score(query_terms, chunk), chunk)
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
                "score": score,
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

    def _load_chunks(self, docs_dir: Path) -> list[Chunk]:
        chunks: list[Chunk] = []
        for path in sorted(docs_dir.rglob("*.md")):
            relative_doc = path.relative_to(docs_dir).as_posix()
            text = path.read_text(encoding="utf-8")
            for raw_chunk in split_markdown_with_size(text, self.chunk_size):
                chunks.append(
                    Chunk(
                        doc=relative_doc,
                        text=raw_chunk,
                        terms=tokenize(raw_chunk),
                    )
                )
        if not chunks:
            raise ValueError(f"No Markdown documents found in {docs_dir}")
        return chunks

    def _score(self, query_terms: set[str], chunk: Chunk) -> int:
        return len(query_terms.intersection(chunk.terms))
