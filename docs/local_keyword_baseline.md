# Local Keyword Baseline

`local-keyword` 是一个本地 Markdown 检索 baseline。

它的作用不是替代 RAGFlow，也不是生成高质量答案。它用于演示 RAG 评测链路中最基本的一步：

```text
问题 -> 检索本地文档片段 -> 返回引用 -> 计算评测指标
```

## 为什么需要它

在接入 RAGFlow 之前，我们需要先理解两件事：

- 检索系统如何从文档中找候选片段。
- 评测工具如何根据回答和引用计算指标。

`mock` client 固定返回答案，只能验证脚本能跑。

`local-keyword` 会真正读取 `examples/docs` 里的 Markdown 文件，按简单的关键词和字符重叠打分，返回相关片段和引用。

## 它怎么工作

1. 读取 `docs-dir` 下的 Markdown 文件。
2. 按空行切分成 chunk。
3. 对问题和 chunk 做简单 tokenize。
4. 计算问题 terms 和 chunk terms 的交集数量。
5. 返回分数最高的 top-k 个 chunk。

运行示例：

```powershell
python -m ragbench.eval --questions examples/questions_zh.json --out reports/local_keyword_report.md --json-out reports/local_keyword_result.json --client local-keyword --docs-dir examples/docs --top-k 3
```

## 局限

- 它不是语义检索。
- 它不能理解同义词。
- 它不会调用大模型生成新答案。
- 它只适合作为 baseline。

## 面试时怎么讲

可以说：

> 我先实现了一个本地关键词检索 baseline，用来验证评测链路。它读取 Markdown 文档、切分 chunk、按问题和 chunk 的词项重叠排序，并返回引用。这个 baseline 很简单，但能帮助我理解 RAG 中 retrieval、top-k、citation hit 和 failure type 的关系。后续再接入 RAGFlow 或 embedding 检索。

