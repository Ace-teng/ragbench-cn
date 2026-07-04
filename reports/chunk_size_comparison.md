# RAGBench-CN Chunk Size Comparison

## Summary

| Run | Citation Hit Rate | Avg Keyword Recall | Avg Precision@k | Avg Recall@k | Avg Latency ms | Failure Counts |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| chunk_size=120 | 1.00 | 0.64 | 0.78 | 1.00 | 0.03 | keyword_missing=4, ok=16 |
| chunk_size=300 | 1.00 | 0.66 | 0.82 | 1.00 | 0.02 | keyword_missing=2, ok=18 |
| chunk_size=600 | 1.00 | 0.66 | 0.82 | 1.00 | 0.02 | keyword_missing=2, ok=18 |

## How To Read

- Compare citation hit rate, keyword recall, precision@k, recall@k, latency, and failure counts together.
- Higher recall is not always better if precision drops sharply.
- Local baselines are useful for controlled experiments, but production RAG should be tested with real services.

## Experiment Notes

- Chunk size controls how large each retrievable text fragment is.
- Small chunks may miss context; large chunks may carry more unrelated content.

## Worst Cases By Run

### chunk_size=120

| ID | Keyword Recall | Precision@k | Recall@k | Citation Hit | Failure Type | Diagnosis | Question |
| --- | ---: | ---: | ---: | --- | --- | --- | --- |
| q003 | 0.25 | 0.33 | 1.00 | True | keyword_missing | noisy_retrieval: gold source was retrieved but top-k contains many non-gold chunks | chunk size 过小会带来什么问题？ |
| q011 | 0.25 | 1.00 | 1.00 | True | keyword_missing | keyword_missing: answer missed expected key concepts | 如何判断一次 RAG 回答是检索失败？ |
| q017 | 0.25 | 1.00 | 1.00 | True | keyword_missing | keyword_missing: answer missed expected key concepts | 为什么 RAG 系统需要失败 case 分析？ |

### chunk_size=300

| ID | Keyword Recall | Precision@k | Recall@k | Citation Hit | Failure Type | Diagnosis | Question |
| --- | ---: | ---: | ---: | --- | --- | --- | --- |
| q001 | 0.25 | 1.00 | 1.00 | True | keyword_missing | keyword_missing: answer missed expected key concepts | RAG 的基本流程是什么？ |
| q011 | 0.25 | 1.00 | 1.00 | True | keyword_missing | keyword_missing: answer missed expected key concepts | 如何判断一次 RAG 回答是检索失败？ |
| q003 | 0.50 | 0.33 | 1.00 | True | ok | noisy_retrieval: gold source was retrieved but top-k contains many non-gold chunks | chunk size 过小会带来什么问题？ |

### chunk_size=600

| ID | Keyword Recall | Precision@k | Recall@k | Citation Hit | Failure Type | Diagnosis | Question |
| --- | ---: | ---: | ---: | --- | --- | --- | --- |
| q001 | 0.25 | 1.00 | 1.00 | True | keyword_missing | keyword_missing: answer missed expected key concepts | RAG 的基本流程是什么？ |
| q011 | 0.25 | 1.00 | 1.00 | True | keyword_missing | keyword_missing: answer missed expected key concepts | 如何判断一次 RAG 回答是检索失败？ |
| q003 | 0.50 | 0.33 | 1.00 | True | ok | noisy_retrieval: gold source was retrieved but top-k contains many non-gold chunks | chunk size 过小会带来什么问题？ |
