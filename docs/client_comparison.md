# Client Comparison

Client comparison keeps the same question set and documents while changing the retrieval strategy.

Use it to compare baselines such as:

- `local-keyword`
- `local-embedding`

## Usage

Lightweight example:

```powershell
ragbench-compare --mode client --clients local-keyword --questions examples/questions_zh.json --docs-dir examples/docs --top-k 3 --out reports/client_comparison.md --json-out reports/client_comparison.json --html-out reports/client_comparison.html
```

Embedding comparison after installing optional dependencies:

```powershell
pip install -e .[embedding]
ragbench-compare --mode client --clients local-keyword,local-embedding --questions examples/questions_zh.json --docs-dir examples/docs --top-k 3 --out reports/client_comparison.md --json-out reports/client_comparison.json --html-out reports/client_comparison.html
```

## Current Result

The checked-in example compares `local-keyword` and `local-embedding` with `top_k=3`.

| Run | Citation Hit Rate | Avg Keyword Recall | Avg Precision@k | Avg Recall@k | Avg Latency ms |
| --- | ---: | ---: | ---: | ---: | ---: |
| local-keyword | 1.00 | 0.66 | 0.82 | 1.00 | 0.02 |
| local-embedding | 1.00 | 0.65 | 0.73 | 1.00 | 12.99 |

## How To Read

Use the same metrics as other reports:

- keyword recall
- citation hit rate
- precision@k
- recall@k
- latency
- failure counts

The important comparison is not simply which client has the highest score.

In the current small dataset, `local-embedding` does not outperform `local-keyword`. It reaches the same recall@k, but has lower precision@k and higher latency. This is a valid result: semantic retrieval is not automatically better, especially when the dataset is small and contains intentionally similar noise documents.

A semantic retriever may improve recall on paraphrases and synonym-heavy questions, but it can also retrieve semantically similar noise. A keyword retriever may be faster and more predictable, but can miss semantic matches.

## Interview Notes

可以这样讲：

> 我把参数对比扩展成 client 对比，让同一套问题集可以比较不同检索策略。比如 `local-keyword` 按词面重合排序，`local-embedding` 按向量相似度排序。当前实验里 embedding baseline 没有直接超过 keyword baseline，反而 precision@k 更低、延迟更高，这说明语义检索不是默认更优，需要结合数据集和指标验证。
