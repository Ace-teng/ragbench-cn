# Chunk Size Experiment

`chunk size` 表示每个可检索文本片段的大小。

RAGBench-CN 现在可以用本地 baseline 对比不同 chunk size：

```powershell
python -m ragbench.compare --mode chunk-size --questions examples/questions_zh.json --docs-dir examples/docs --top-k 3 --chunk-size 120,300,600 --out reports/chunk_size_comparison.md --json-out reports/chunk_size_comparison.json
```

## 你要理解

chunk size 控制的是“每块文档有多大”。

- chunk 太小：每块信息少，容易缺上下文。
- chunk 太大：每块信息多，但可能带入无关内容。

`top-k` 和 `chunk size` 是两件事：

| 参数 | 控制什么 |
| --- | --- |
| top-k | 返回多少个 chunk |
| chunk size | 每个 chunk 有多大 |

## 面试表达

可以说：

> 我把本地检索 baseline 扩展为可配置 chunk size，并比较 120、300、600 三种切分粒度下的关键词召回率和失败类型。这个实验用来说明文档切分策略会影响 RAG 检索质量。

