# RAGBench-CN Client Comparison

## Summary

| Run | Citation Hit Rate | Avg Keyword Recall | Avg Precision@k | Avg Recall@k | Avg Latency ms | Failure Counts |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| local-keyword | 1.00 | 0.66 | 0.82 | 1.00 | 0.03 | keyword_missing=2, ok=18 |

## How To Read

- Compare citation hit rate, keyword recall, precision@k, recall@k, latency, and failure counts together.
- Higher recall is not always better if precision drops sharply.
- Local baselines are useful for controlled experiments, but production RAG should be tested with real services.

## Experiment Notes

- Client comparison keeps the same questions and docs while changing retrieval strategy.
- `local-keyword` ranks chunks by lexical overlap.
- `local-embedding` ranks chunks by vector similarity and requires the optional embedding dependency.

## Worst Cases By Run

### local-keyword

| ID | Keyword Recall | Citation Hit | Failure Type | Question |
| --- | ---: | --- | --- | --- |
| q011 | 0.25 | True | keyword_missing | 如何判断一次 RAG 回答是检索失败？ |
| q001 | 0.25 | True | keyword_missing | RAG 的基本流程是什么？ |
| q007 | 0.50 | True | ok | rerank 的作用是什么？ |
