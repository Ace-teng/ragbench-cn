# Local Embedding Baseline

`local-embedding` is an optional local semantic retrieval baseline.

It reads local Markdown documents, splits them into chunks, embeds each chunk with a SentenceTransformers model, and ranks chunks by cosine similarity to the question embedding.

## Install

The main package keeps embedding dependencies optional.

```powershell
pip install -e .[embedding]
```

## Usage

```powershell
ragbench-eval --questions examples/questions_zh.json --out reports/local_embedding_report.md --json-out reports/local_embedding_result.json --client local-embedding --docs-dir examples/docs --top-k 3
```

Use a different model:

```powershell
ragbench-eval --questions examples/questions_zh.json --out reports/local_embedding_report.md --client local-embedding --docs-dir examples/docs --embedding-model paraphrase-multilingual-MiniLM-L12-v2
```

## How It Works

1. Read Markdown files from `--docs-dir`.
2. Split documents into chunks.
3. Encode chunks with a local embedding model.
4. Encode the question.
5. Rank chunks by cosine similarity.
6. Return top-k chunks, citations, and retrieved metadata.

## Why It Matters

`local-keyword` is useful as a simple reproducible baseline, but it does not understand semantic similarity.

`local-embedding` is closer to a real RAG retriever because it compares dense vectors instead of keyword overlap.

## Limitations

- It requires installing `sentence-transformers`.
- First run may download the embedding model.
- Model choice affects quality, speed, and memory usage.
- It is still only a retriever baseline; it does not call an LLM to synthesize a new answer.

## Interview Notes

可以这样讲：

> 我先做了 keyword baseline 保证评测闭环可复现，然后增加 local embedding baseline，用向量相似度替代关键词重合度。这样可以比较 keyword retrieval 和 semantic retrieval 的差异，也更接近真实 RAG 系统的检索阶段。
