# RAGBench-CN

[![Tests](https://github.com/Ace-teng/ragbench-cn/actions/workflows/tests.yml/badge.svg)](https://github.com/Ace-teng/ragbench-cn/actions/workflows/tests.yml)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

RAGBench-CN is a lightweight Chinese RAG evaluation toolkit.

It evaluates knowledge-base QA systems with a question set and generates Markdown / JSON reports for keyword recall, retrieval precision@k, retrieval recall@k, citation hit rate, latency, failure types, and worst cases.

中文简介：

> RAGBench-CN 是一个轻量中文 RAG 评测工具。它用问题集批量测试知识库问答系统，输出关键词召回率、引用命中率、响应延迟、失败类型和 worst cases。

## Why

Many RAG demos can answer questions, but they often lack evaluation:

- Did the answer cite the expected source document?
- Did the answer cover the key concepts?
- Did changing `top-k` or `chunk size` improve the result?
- Which questions failed, and why?

RAGBench-CN does not rebuild a RAG platform. It evaluates outputs from RAGFlow, OpenAI-compatible services, or a local Markdown baseline.

## Features

- Chinese question set format
- Markdown, JSON, and HTML reports
- `mock` client for pipeline validation
- `local-keyword` client for local Markdown retrieval baseline
- `openai-compatible` client for compatible `/chat/completions` services
- `ragflow` client for RAGFlow non-streaming chat completion
- Retrieval precision@k for clients that return retrieved chunks
- Retrieval recall@k and retrieved chunk previews
- Top-k comparison
- Chunk size comparison
- Worst case analysis

## Install

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .
```

## Quick Start

Validate the evaluation pipeline with mock data:

```powershell
ragbench-eval --questions examples/questions_zh.json --out reports/sample_report.md --json-out reports/sample_result.json --mock
```

Run local Markdown retrieval baseline:

```powershell
ragbench-eval --questions examples/questions_zh.json --out reports/local_keyword_report.md --json-out reports/local_keyword_result.json --html-out reports/local_keyword_report.html --client local-keyword --docs-dir examples/docs --top-k 3
```

Compare top-k settings:

```powershell
ragbench-compare --questions examples/questions_zh.json --docs-dir examples/docs --top-k 1,3,5 --out reports/top_k_comparison.md --json-out reports/top_k_comparison.json --html-out reports/top_k_comparison.html
```

Compare chunk sizes:

```powershell
ragbench-compare --mode chunk-size --questions examples/questions_zh.json --docs-dir examples/docs --top-k 3 --chunk-size 120,300,600 --out reports/chunk_size_comparison.md --json-out reports/chunk_size_comparison.json
```

Generated examples are listed in [reports/README.md](reports/README.md).

## Example Result

Top-k comparison on the local Markdown baseline:

| Run | Citation Hit Rate | Avg Keyword Recall | Avg Precision@k | Avg Recall@k | Avg Latency ms | Failure Counts |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| top_k=1 | 0.90 | 0.41 | 0.90 | 0.90 | 0.02 | keyword_missing=8, ok=10, retrieval_miss=2 |
| top_k=3 | 1.00 | 0.66 | 0.82 | 1.00 | 0.02 | keyword_missing=2, ok=18 |
| top_k=5 | 1.00 | 0.76 | 0.80 | 1.00 | 0.02 | keyword_missing=1, ok=19 |

Interpretation:

- Larger `top-k` returns more chunks.
- More chunks may improve keyword coverage.
- More chunks may also reduce precision@k when similar but non-gold documents are retrieved.
- In real RAG systems, larger `top-k` may also add noise, context cost, and latency.

## Question Format

```json
[
  {
    "id": "q001",
    "question": "RAG 中 chunk size 过大会带来什么问题？",
    "expected_keywords": ["噪声", "上下文", "召回", "精度"],
    "gold_doc": "rag_basics.md"
  }
]
```

Fields:

- `id`: question id
- `question`: user question
- `expected_keywords`: key concepts expected in the answer
- `gold_doc`: expected source document

## Metrics

| Metric | Meaning |
| --- | --- |
| `citation_hit_rate` | Whether citations hit expected source documents |
| `keyword_recall` | How many expected keywords are covered |
| `average_latency_ms` | Average response latency |
| `failure_type` | `retrieval_miss`, `citation_missing`, `keyword_missing`, etc. |
| `worst_cases` | The most important failed or weak cases to inspect |

See [docs/metrics.md](docs/metrics.md) for details.

## Clients

| Client | Purpose |
| --- | --- |
| `mock` | Validate evaluation pipeline |
| `local-keyword` | Local Markdown retrieval baseline |
| `openai-compatible` | Any OpenAI-compatible `/chat/completions` service |
| `ragflow` | RAGFlow non-streaming chat completion |

OpenAI-compatible example:

```powershell
ragbench-eval --client openai-compatible --questions examples/questions_zh.json --out reports/openai_report.md --json-out reports/openai_result.json --base-url http://localhost:8000/v1 --api-key YOUR_KEY --model YOUR_MODEL
```

RAGFlow example:

```powershell
ragbench-eval --client ragflow --questions examples/questions_zh.json --out reports/ragflow_report.md --json-out reports/ragflow_result.json --base-url http://localhost:9380 --api-key YOUR_RAGFLOW_KEY --chat-id YOUR_CHAT_ID --model model
```

## Current Status

- Mock evaluation works.
- Local Markdown keyword retrieval baseline works.
- Markdown / JSON report export works.
- Top-k and chunk size comparison work.
- Worst case analysis works.
- OpenAI-compatible client is wired.
- RAGFlow client is wired for non-streaming chat completion.
- Real RAGFlow smoke test is still pending.

See [CHANGELOG.md](CHANGELOG.md) and [docs/v0_1_checklist.md](docs/v0_1_checklist.md) for release status.

## Test

```powershell
python -m unittest discover -s tests
```

## Roadmap

- Run a real RAGFlow smoke test.
- Improve citation extraction for different RAGFlow response formats.
- Add optional LLM-as-judge metrics.
- Add HTML report or charts.
