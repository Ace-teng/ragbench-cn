from __future__ import annotations

import time


class MockRagClient:
    """Local deterministic client used before a real RAG service is connected."""

    def ask(self, question: str) -> dict:
        start = time.perf_counter()
        answer = (
            "RAG 的核心流程是先从知识库检索相关片段，再把检索上下文交给大模型生成回答。"
            "chunk size、top-k 和 rerank 会影响召回、噪声、上下文质量和延迟。"
            "评估时应记录引用命中、关键词召回、平均延迟和失败 case。"
        )
        return {
            "answer": answer,
            "citations": ["rag_basics.md"],
            "latency_ms": round((time.perf_counter() - start) * 1000, 2),
        }

