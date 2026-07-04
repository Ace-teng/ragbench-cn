# RAGBench-CN Chunk Size Comparison

## Summary

| Run | Citation Hit Rate | Avg Keyword Recall | Avg Latency ms | Failure Counts |
| --- | ---: | ---: | ---: | --- |
| chunk_size=120 | 1.00 | 0.66 | 0.03 | keyword_missing=3, ok=17 |
| chunk_size=300 | 1.00 | 0.71 | 0.02 | keyword_missing=2, ok=18 |
| chunk_size=600 | 1.00 | 0.71 | 0.03 | keyword_missing=2, ok=18 |

## How To Read

- Higher top-k may improve recall because more chunks are returned.
- Higher top-k may also introduce noise and increase latency in real RAG systems.
- This report uses `local-keyword`, so latency is not representative of model-based RAG.

## Experiment Notes

- Chunk size controls how large each retrievable text fragment is.
- Small chunks may miss context; large chunks may carry more unrelated content.

## Worst Cases By Run

### chunk_size=120

| ID | Keyword Recall | Citation Hit | Failure Type | Question |
| --- | ---: | --- | --- | --- |
| q001 | 0.25 | True | keyword_missing | RAG 的基本流程是什么？ |
| q011 | 0.25 | True | keyword_missing | 如何判断一次 RAG 回答是检索失败？ |
| q017 | 0.25 | True | keyword_missing | 为什么 RAG 系统需要失败 case 分析？ |

### chunk_size=300

| ID | Keyword Recall | Citation Hit | Failure Type | Question |
| --- | ---: | --- | --- | --- |
| q001 | 0.25 | True | keyword_missing | RAG 的基本流程是什么？ |
| q011 | 0.25 | True | keyword_missing | 如何判断一次 RAG 回答是检索失败？ |
| q007 | 0.50 | True | ok | rerank 的作用是什么？ |

### chunk_size=600

| ID | Keyword Recall | Citation Hit | Failure Type | Question |
| --- | ---: | --- | --- | --- |
| q001 | 0.25 | True | keyword_missing | RAG 的基本流程是什么？ |
| q011 | 0.25 | True | keyword_missing | 如何判断一次 RAG 回答是检索失败？ |
| q007 | 0.50 | True | ok | rerank 的作用是什么？ |
