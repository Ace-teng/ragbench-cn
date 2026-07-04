# Top-k Experiment

`top-k` 表示检索阶段返回多少个候选 chunk。

RAGBench-CN 支持用 `ragbench-compare` 对比多组 top-k：

```powershell
python -m ragbench.compare --questions examples/questions_zh.json --docs-dir examples/docs --top-k 1,3,5 --out reports/top_k_comparison.md --json-out reports/top_k_comparison.json --html-out reports/top_k_comparison.html
```

## Current Example

当前示例文档中包含一个标准来源 `rag_basics.md`，也包含一个相似但非标准来源 `retrieval_noise.md`。

这能模拟真实知识库中的常见情况：检索器既可能返回正确资料，也可能返回主题相近但不该作为标准答案依据的噪声文档。

当前 top-k 对比结果：

| Run | Citation Hit Rate | Avg Keyword Recall | Avg Precision@k |
| --- | ---: | ---: | ---: |
| top_k=1 | 0.90 | 0.41 | 0.90 |
| top_k=3 | 1.00 | 0.66 | 0.82 |
| top_k=5 | 1.00 | 0.76 | 0.80 |

## How To Read

top-k 变大后，关键词召回率提高了，因为系统拿到了更多 chunk。

但 precision@k 下降了，因为更多相似但非标准来源的 chunk 被一起返回。

这说明 top-k 不是越大越好。真实 RAG 系统需要在召回、噪声、上下文成本和延迟之间权衡。

## Interview Notes

可以这样讲：

> 我没有只看 top-k 变大后 recall 是否提高，还加入了 precision@k 来观察噪声。实验里 top-k 从 1 到 5 时，keyword recall 提高，但 precision@k 下降，说明更多上下文确实带来了更多非标准来源内容。这个现象更接近真实 RAG 调参，而不是简单认为 top-k 越大越好。
