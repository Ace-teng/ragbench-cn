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

## How To Read

Use the same metrics as other reports:

- keyword recall
- citation hit rate
- precision@k
- recall@k
- latency
- failure counts

The important comparison is not simply which client has the highest score. A semantic retriever may improve recall but add latency. A keyword retriever may be faster and more predictable, but miss semantic matches.

## Interview Notes

可以这样讲：

> 我把参数对比扩展成 client 对比，让同一套问题集可以比较不同检索策略。比如 `local-keyword` 按词面重合排序，`local-embedding` 按向量相似度排序。这样可以用同一套指标比较 keyword retrieval 和 semantic retrieval 的差异。
