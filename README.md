# RAGBench-CN

[![Tests](https://github.com/Ace-teng/ragbench-cn/actions/workflows/tests.yml/badge.svg)](https://github.com/Ace-teng/ragbench-cn/actions/workflows/tests.yml)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Release](https://img.shields.io/github/v/release/Ace-teng/ragbench-cn)

RAGBench-CN is a lightweight Chinese RAG evaluation toolkit.

It evaluates knowledge-base QA systems with a question set and generates Markdown / JSON / HTML reports for keyword recall, retrieval precision@k, retrieval recall@k, citation hit rate, latency, failure types, diagnoses, and worst cases.

中文简介：

> RAGBench-CN 是一个轻量中文 RAG 评测工具。它用问题集批量测试知识库问答系统，输出关键词召回率、引用命中率、响应延迟、失败类型和 worst cases。

## Why

Many RAG demos can answer questions, but they often lack evaluation:

- Did the answer cite the expected source document?
- Did the answer cover the key concepts?
- Did changing `top-k` or `chunk size` improve the result?
- Which questions failed, and why?

RAGBench-CN does not rebuild a RAG platform. It evaluates outputs from RAGFlow, OpenAI-compatible services, or a local Markdown baseline.

## What You Get

- A reproducible RAG evaluation workflow.
- Local baselines for quick experiments before wiring real services.
- Comparison reports for `top-k`, `chunk size`, and retrieval clients.
- A concrete keyword-vs-embedding finding instead of a vague demo.
- Failure cases that can be inspected and discussed.

## Features

- Chinese question set format
- Markdown, JSON, and HTML reports
- `mock` client for pipeline validation
- `local-keyword` client for local Markdown retrieval baseline
- `local-embedding` client for optional local semantic retrieval baseline
- `openai-compatible` client for compatible `/chat/completions` services
- `ragflow` client for RAGFlow non-streaming chat completion
- Retrieval precision@k for clients that return retrieved chunks
- Retrieval recall@k and retrieved chunk previews
- Top-k comparison
- Chunk size comparison
- Keyword vs embedding client comparison
- Paraphrase question set for testing semantic retrieval
- Worst case analysis with diagnosis text

## Install

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .
```

Optional local embedding baseline:

```powershell
pip install -e .[embedding]
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

Run optional local embedding retrieval baseline:

```powershell
ragbench-eval --questions examples/questions_zh.json --out reports/local_embedding_report.md --json-out reports/local_embedding_result.json --client local-embedding --docs-dir examples/docs --top-k 3
```

Compare top-k settings:

```powershell
ragbench-compare --questions examples/questions_zh.json --docs-dir examples/docs --top-k 1,3,5 --out reports/top_k_comparison.md --json-out reports/top_k_comparison.json --html-out reports/top_k_comparison.html
```

Compare chunk sizes:

```powershell
ragbench-compare --mode chunk-size --questions examples/questions_zh.json --docs-dir examples/docs --top-k 3 --chunk-size 120,300,600 --out reports/chunk_size_comparison.md --json-out reports/chunk_size_comparison.json
```

Compare retrieval clients:

```powershell
ragbench-compare --mode client --clients local-keyword,local-embedding --questions examples/questions_zh.json --docs-dir examples/docs --top-k 3 --out reports/client_comparison.md --json-out reports/client_comparison.json --html-out reports/client_comparison.html
```

Compare keyword and embedding retrieval on paraphrased questions:

```powershell
ragbench-compare --mode client --clients local-keyword,local-embedding --questions examples/questions_paraphrase.json --docs-dir examples/docs --top-k 3 --out reports/paraphrase_client_comparison.md --json-out reports/paraphrase_client_comparison.json --html-out reports/paraphrase_client_comparison.html
```

Generated examples are listed in [reports/README.md](reports/README.md).

## Reproduce The Main Finding

Install the optional embedding dependency:

```powershell
pip install -e .[embedding]
```

Run the default Chinese comparison:

```powershell
ragbench-compare --mode client --clients local-keyword,local-embedding --questions examples/questions_zh.json --docs-dir examples/docs --top-k 3 --out reports/client_comparison.md --json-out reports/client_comparison.json --html-out reports/client_comparison.html
```

Run the paraphrase comparison:

```powershell
ragbench-compare --mode client --clients local-keyword,local-embedding --questions examples/questions_paraphrase.json --docs-dir examples/docs --top-k 3 --out reports/paraphrase_client_comparison.md --json-out reports/paraphrase_client_comparison.json --html-out reports/paraphrase_client_comparison.html
```

Read the two reports together:

- Default Chinese questions: keyword retrieval is competitive because wording overlap is high.
- English paraphrase questions: embedding retrieval works better because semantic matching matters more.
- This is the core point of the project: RAG retrieval strategy should be evaluated under different data distributions.

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

Paraphrase comparison on the same local documents:

| Run | Citation Hit Rate | Avg Keyword Recall | Avg Precision@k | Avg Recall@k | Avg Latency ms | Failure Counts |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| local-keyword | 0.33 | 0.17 | 1.00 | 1.00 | 0.01 | empty_answer=4, keyword_missing=1, ok=1 |
| local-embedding | 1.00 | 0.92 | 0.67 | 1.00 | 13.92 | ok=6 |

Interpretation:

- Keyword retrieval is strong when questions and documents share surface words.
- Embedding retrieval is more useful when questions are paraphrased or cross-lingual.
- The lower precision@k for embedding shows that semantic retrieval can still bring similar but noisy chunks.
- Retrieval precision@k and recall@k are averaged over questions with returned retrieved chunks.

## Question Format

```json
[
  {
    "id": "q001",
    "question": "RAG 中 chunk size 过大会带来什么问题？",
    "expected_keywords": ["噪声", "上下文", "召回", "精度"],
    "gold_doc": "rag_basics.md"
  },
  {
    "id": "q002",
    "question": "A question with multiple acceptable source documents",
    "expected_keywords": ["retrieval", "citation"],
    "gold_docs": ["rag_basics.md", "retrieval_noise.md"]
  }
]
```

Fields:

- `id`: question id
- `question`: user question
- `expected_keywords`: key concepts expected in the answer
- `gold_doc`: expected source document
- `gold_docs`: optional list of expected source documents. Use this when one question can be supported by multiple sources.

## Metrics

| Metric | Meaning |
| --- | --- |
| `citation_hit_rate` | Whether citations hit expected source documents |
| `keyword_recall` | How many expected keywords are covered |
| `retrieval_precision_at_k` | How many retrieved chunks come from expected source documents |
| `retrieval_recall_at_k` | How many expected source documents appear in retrieved chunks |
| `average_latency_ms` | Average response latency |
| `failure_type` | `retrieval_miss`, `citation_missing`, `keyword_missing`, etc. |
| `diagnosis` | Human-readable explanation of the likely issue |
| `worst_cases` | The most important failed or weak cases to inspect |

See [docs/metrics.md](docs/metrics.md) for details.

## Clients

| Client | Purpose |
| --- | --- |
| `mock` | Validate evaluation pipeline |
| `local-keyword` | Local Markdown retrieval baseline |
| `local-embedding` | Optional local semantic retrieval baseline with SentenceTransformers |
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
- Keyword vs embedding retrieval comparison works.
- Paraphrase experiment works.
- OpenAI-compatible client is wired.
- RAGFlow client is wired for non-streaming chat completion.
- Real RAGFlow smoke test is still pending.

See [CHANGELOG.md](CHANGELOG.md) and [docs/v0_2_checklist.md](docs/v0_2_checklist.md) for release status.

## Test

```powershell
python -m unittest discover -s tests
```

Check CLI version:

```powershell
ragbench-eval --version
ragbench-compare --version
```

## Roadmap

- Run a real RAGFlow smoke test.
- Improve citation extraction for different RAGFlow response formats.
- Add optional LLM-as-judge metrics.
- Add charts to HTML reports.
