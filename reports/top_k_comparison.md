# RAGBench-CN Top-k Comparison

## Summary

| Run | Citation Hit Rate | Avg Keyword Recall | Avg Precision@k | Avg Recall@k | Avg Latency ms | Failure Counts |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| top_k=1 | 0.90 | 0.41 | 0.90 | 0.90 | 0.02 | keyword_missing=8, ok=10, retrieval_miss=2 |
| top_k=3 | 1.00 | 0.66 | 0.82 | 1.00 | 0.04 | keyword_missing=2, ok=18 |
| top_k=5 | 1.00 | 0.76 | 0.80 | 1.00 | 0.03 | keyword_missing=1, ok=19 |

## How To Read

- Higher top-k may improve recall because more chunks are returned.
- Higher top-k may also introduce noise and increase latency in real RAG systems.
- This report uses `local-keyword`, so latency is not representative of model-based RAG.

## Experiment Notes

- Top-k controls how many retrieved chunks are returned.
- In real RAG systems, larger top-k may improve recall but can add noise and latency.

## Worst Cases By Run

### top_k=1

| ID | Keyword Recall | Citation Hit | Failure Type | Question |
| --- | ---: | --- | --- | --- |
| q004 | 0.00 | True | keyword_missing | embedding 在 RAG 系统中起什么作用？ |
| q017 | 0.00 | True | keyword_missing | 为什么 RAG 系统需要失败 case 分析？ |
| q006 | 0.25 | False | retrieval_miss | top-k 变大会怎样影响回答质量？ |

### top_k=3

| ID | Keyword Recall | Citation Hit | Failure Type | Question |
| --- | ---: | --- | --- | --- |
| q011 | 0.25 | True | keyword_missing | 如何判断一次 RAG 回答是检索失败？ |
| q001 | 0.25 | True | keyword_missing | RAG 的基本流程是什么？ |
| q018 | 0.50 | True | ok | RAG 中 prompt 的作用是什么？ |

### top_k=5

| ID | Keyword Recall | Citation Hit | Failure Type | Question |
| --- | ---: | --- | --- | --- |
| q011 | 0.25 | True | keyword_missing | 如何判断一次 RAG 回答是检索失败？ |
| q007 | 0.50 | True | ok | rerank 的作用是什么？ |
| q010 | 0.50 | True | ok | 关键词召回率有什么局限？ |
