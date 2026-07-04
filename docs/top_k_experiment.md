# Top-k Experiment

`top-k` 表示检索阶段返回多少个候选 chunk。

RAGBench-CN 现在支持用 `compare.py` 跑多组 top-k 对比：

```powershell
python -m ragbench.compare --questions examples/questions_zh.json --docs-dir examples/docs --top-k 1,3,5 --out reports/top_k_comparison.md --json-out reports/top_k_comparison.json
```

## 你要理解

top-k 不是越大越好。

- top-k 小：上下文更干净、延迟更低，但可能漏掉正确片段。
- top-k 大：召回可能更好，但可能引入噪声，也会增加真实 RAG 系统的上下文成本和延迟。

当前实验使用 `local-keyword`，所以延迟很低，不代表真实大模型系统延迟。

## 面试表达

可以说：

> 我把单次评测扩展成参数对比实验，先比较 top-k=1/3/5 下的引用命中率、关键词召回率、平均延迟和失败类型。这样可以用数据说明检索参数对 RAG 效果的影响，而不是凭感觉调参。

