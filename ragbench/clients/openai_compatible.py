from __future__ import annotations

import time
from typing import Any

import requests


class OpenAICompatibleClient:
    def __init__(self, base_url: str, api_key: str, model: str) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.model = model

    def ask(self, question: str) -> dict[str, Any]:
        start = time.perf_counter()
        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers={"Authorization": f"Bearer {self.api_key}"},
            json={
                "model": self.model,
                "messages": [{"role": "user", "content": question}],
                "temperature": 0.2,
            },
            timeout=60,
        )
        response.raise_for_status()
        data = response.json()
        answer = data["choices"][0]["message"]["content"]
        citations = data.get("citations", [])
        return {
            "answer": answer,
            "citations": citations,
            "latency_ms": round((time.perf_counter() - start) * 1000, 2),
        }
