# Metrics

RAGBench-CN 第一版只使用简单、可解释的指标。目标不是一次性判断答案绝对正确，而是快速发现 RAG 系统的明显问题。

## keyword_recall

含义：回答覆盖了多少期望关键词。

计算方式：

```text
命中的关键词数量 / 期望关键词总数
```

例子：

```json
{
  "expected_keywords": ["噪声", "上下文", "召回", "精度"]
}
```

如果回答中出现了 `噪声`、`上下文`、`召回`，但没有出现 `精度`，则：

```text
keyword_recall = 3 / 4 = 0.75
```

局限：

- 不能识别同义词。
- 不能判断答案逻辑是否正确。
- 关键词出现不代表事实一定正确。

用途：

- 快速检查回答是否覆盖关键概念。
- 对比不同参数下回答是否遗漏重点。

## citation_hit_rate

含义：回答引用是否命中标准文档。

单条问题先计算 `citation_hit`：

```text
gold_doc 是否出现在 citations 中
```

整体再计算：

```text
命中引用的问题数 / 总问题数
```

局限：

- 标准文档可能不止一个。
- 引用命中不代表回答一定正确。
- 没有引用结构的 RAG 系统需要先适配输出格式。

用途：

- 判断检索是否找到了正确来源。
- 分析回答是否有事实支撑。

## retrieval_precision_at_k

含义：检索返回的 top-k chunks 中，有多少比例来自标准文档。

计算方式：

```text
relevant retrieved chunks / retrieved chunks
```

例如 top-k 返回 3 个 chunk，其中 2 个来自 `gold_doc`，则：

```text
retrieval_precision_at_k = 2 / 3 = 0.67
```

用途：

- 衡量返回结果里相关 chunk 的纯度。
- 和 `citation_hit_rate` 互补：citation hit 只看有没有命中，precision@k 看返回结果里相关内容占比。
- 分析 top-k 变大时是否引入更多噪声。

局限：

- 当前用 `gold_doc` 判断相关性，粒度仍然比较粗。
- 如果一个文档内部有相关和不相关片段，文档级 gold label 不能完全区分。
- 外部 client 需要返回 `retrieved` chunks 才能计算该指标。
## avg_latency

含义：平均响应时间。

计算方式：

```text
所有问题 latency_ms 的平均值
```

用途：

- 对比 top-k、rerank、模型选择对速度的影响。
- 判断系统是否适合交互式问答。

## failure_type

当前分类：

| 类型 | 含义 |
| --- | --- |
| ok | 引用命中，关键词覆盖足够 |
| empty_answer | 没有回答 |
| retrieval_miss | 引用未命中，关键词覆盖也差 |
| citation_missing | 关键词覆盖尚可，但引用没命中 |
| keyword_missing | 引用命中，但关键词覆盖不足 |

这个分类是粗粒度的，但适合第一版定位问题。

## 面试时要会讲

这几个指标不是完美评测，只是轻量起点。

更完整的 RAG 评测还可以加入：

- answer faithfulness
- answer relevance
- LLM-as-judge
- 人工标注正确率

