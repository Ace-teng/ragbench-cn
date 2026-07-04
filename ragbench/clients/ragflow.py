from __future__ import annotations

import time
from typing import Any

import requests


class RagFlowClient:
    def __init__(self, base_url: str, api_key: str, chat_id: str, model: str = "model") -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.chat_id = chat_id
        self.model = model

    def ask(self, question: str) -> dict[str, Any]:
        start = time.perf_counter()
        response = requests.post(
            f"{self.base_url}/api/v1/openai/{self.chat_id}/chat/completions",
            headers={"Authorization": f"Bearer {self.api_key}"},
            json={
                "model": self.model,
                "messages": [{"role": "user", "content": question}],
                "stream": False,
            },
            timeout=120,
        )
        response.raise_for_status()
        data = response.json()
        answer = data["choices"][0]["message"]["content"]
        citations = self._extract_citations(data)
        return {
            "answer": answer,
            "citations": citations,
            "latency_ms": round((time.perf_counter() - start) * 1000, 2),
        }

    def _extract_citations(self, data: dict[str, Any]) -> list[str]:
        references = data.get("reference") or data.get("references") or data.get("citations") or []
        citations: list[str] = []
        if isinstance(references, list):
            for item in references:
                if isinstance(item, str):
                    citations.append(item)
                elif isinstance(item, dict):
                    value = (
                        item.get("doc_name")
                        or item.get("document_name")
                        or item.get("dataset_name")
                        or item.get("source")
                        or item.get("id")
                    )
                    if value:
                        citations.append(str(value))
        elif isinstance(references, dict):
            chunks = references.get("chunks") or references.get("doc_aggs") or []
            for item in chunks:
                if isinstance(item, dict):
                    value = item.get("doc_name") or item.get("document_name") or item.get("source") or item.get("id")
                    if value:
                        citations.append(str(value))
        return list(dict.fromkeys(citations))
