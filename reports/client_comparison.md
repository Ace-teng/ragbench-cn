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

| ID | Keyword Recall | Precision@k | Recall@k | Citation Hit | Failure Type | Diagnosis | Question |
| --- | ---: | ---: | ---: | --- | --- | --- | --- |
| q001 | 0.25 | 1.00 | 1.00 | True | keyword_missing | keyword_missing: answer missed expected key concepts | RAG 的基本流程是什么？ |
| q011 | 0.25 | 1.00 | 1.00 | True | keyword_missing | keyword_missing: answer missed expected key concepts | 如何判断一次 RAG 回答是检索失败？ |
| q003 | 0.50 | 0.33 | 1.00 | True | ok | noisy_retrieval: gold source was retrieved but top-k contains many non-gold chunks | chunk size 过小会带来什么问题？ |
