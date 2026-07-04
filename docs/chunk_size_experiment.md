# Chunk Size Experiment

`chunk size` 表示每个可检索文本片段的大小。

RAGBench-CN 可以用本地 baseline 对比不同 chunk size：

```powershell
python -m ragbench.compare --mode chunk-size --questions examples/questions_zh.json --docs-dir examples/docs --top-k 3 --chunk-size 120,300,600 --out reports/chunk_size_comparison.md --json-out reports/chunk_size_comparison.json
```

## Current Example

当前 chunk size 对比结果：

| Run | Citation Hit Rate | Avg Keyword Recall | Avg Precision@k | Avg Recall@k |
| --- | ---: | ---: | ---: | ---: |
| chunk_size=120 | 1.00 | 0.64 | 0.78 | 1.00 |
| chunk_size=300 | 1.00 | 0.66 | 0.82 | 1.00 |
| chunk_size=600 | 1.00 | 0.66 | 0.82 | 1.00 |

## How To Read

chunk size 控制的是“每块文档有多大”。

- chunk 太小：每块信息少，容易缺上下文。
- chunk 太大：每块信息多，但可能带入无关内容。

`top-k` 和 `chunk size` 是两个不同参数：

| Parameter | Controls |
| --- | --- |
| top-k | 返回多少个 chunk |
| chunk size | 每个 chunk 有多大 |

在当前示例中，`chunk_size=120` 的 keyword recall 和 precision@k 都更低，说明过细切分让一些问题缺少足够上下文，也更容易让相似噪声片段进入 top-k。

## Interview Notes

可以这样讲：

> 我把本地检索 baseline 扩展为可配置 chunk size，并比较 120、300、600 三种切分粒度下的 keyword recall、precision@k 和失败类型。这个实验说明文档切分策略会影响 RAG 检索质量，不能只靠经验设置。
