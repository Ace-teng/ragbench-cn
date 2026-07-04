# Resume And Interview Notes

## 这个项目和简历的关系

RAGBench-CN 不是用来生成简历的工具。

它本身是你可以写进简历的项目。

简历里的项目应该证明一件事：

> 你不仅知道 RAG / LLM 这些词，而且能用工程方式评估一个 RAG 系统。

这个项目证明的能力包括：

- Python 工具开发
- 命令行工具设计
- JSON 问题集格式设计
- RAG 基础理解
- 检索评估指标设计
- 参数对比实验
- 失败样例分析
- Markdown / JSON 报告生成
- client 适配设计

## 这个项目和面试的关系

面试官不会只看你简历上写了什么。

他会追问：

- 你为什么做这个项目？
- 这个工具输入输出是什么？
- 你怎么定义评测指标？
- `top-k` 和 `chunk size` 分别影响什么？
- 为什么要看 worst cases？
- 哪些是你自己实现的？
- 哪些是 RAGFlow / OpenAI-compatible 服务提供的？
- 如果真实 RAGFlow 返回格式变了，你怎么适配？
- 这个项目目前有什么局限？

所以这个项目的面试价值在于：

> 它能让你围绕一个真实工程问题讲清楚设计、实现、实验、局限和后续改进。

## 简历 4 行版本

项目名：

> RAGBench-CN：中文 RAG 知识库评测工具

项目描述：

> 设计并实现轻量中文 RAG 评测工具，支持通过问题集批量测试知识库问答系统，输出关键词召回率、引用命中率、平均延迟、失败类型和 worst cases。  
> 实现 `mock`、本地 Markdown 检索 baseline、OpenAI-compatible 和 RAGFlow client，支持 Markdown / JSON 报告导出。  
> 设计 top-k 与 chunk size 参数对比实验，分析不同检索参数对关键词覆盖、失败样例和响应延迟的影响。  
> 使用 Python、requests、unittest 和 pyproject 打包项目，提供命令行入口 `ragbench-eval` / `ragbench-compare`，沉淀可复现实验报告和测试用例。

## 面试一分钟介绍

RAGBench-CN 是我做的一个中文 RAG 评测工具。它不是重新做一个 RAG 平台，而是解决 RAG 系统搭好之后“到底准不准”的问题。

工具输入是一组中文问题，每个问题包含期望关键词和标准引用文档。工具会调用被测系统，比如本地检索 baseline、OpenAI-compatible 服务或 RAGFlow，然后统计关键词召回率、引用命中率、平均延迟和失败类型，并生成 Markdown 和 JSON 报告。

我还做了 top-k 和 chunk size 的参数对比实验，用来观察检索返回数量和文档切分粒度对结果的影响。报告里不仅有平均指标，也会列出 worst cases，方便定位具体失败问题。

## 面试追问准备

### 1. 为什么不直接做一个 RAG 问答系统？

因为 RAGFlow、Dify、FastGPT 已经能完成知识库问答。我的项目关注的是评测层：系统回答得是否可靠，引用是否命中正确文档，参数调整后效果是否变好。

### 2. 你自己实现了什么？

我实现了问题集格式、评测主流程、指标计算、Markdown / JSON 报告、worst cases 分析、本地检索 baseline、参数对比实验、OpenAI-compatible client、RAGFlow client 和测试用例。

### 3. keyword_recall 怎么算？

它计算回答覆盖了多少期望关键词：

```text
keyword_recall = 命中的关键词数量 / 期望关键词总数
```

它简单、可解释，但不能完全判断答案语义是否正确。

### 4. citation_hit_rate 怎么算？

每个问题有一个 `gold_doc`。如果系统返回的 citations 里包含这个文档，就认为引用命中。

整体命中率是：

```text
命中引用的问题数 / 总问题数
```

### 5. top-k 影响什么？

top-k 控制检索返回多少个 chunk。

top-k 小，上下文更干净，但可能漏掉正确片段。

top-k 大，召回可能更好，但可能引入噪声、增加上下文成本和真实系统延迟。

### 6. chunk size 影响什么？

chunk size 控制每个可检索文本片段有多大。

太小容易丢上下文，太大容易带入无关信息。

### 7. worst cases 有什么用？

平均分只能说明整体趋势，worst cases 能指出具体哪些问题最差，方便后续排查是检索失败、引用缺失，还是答案没覆盖关键点。

### 8. 当前项目有什么局限？

- `keyword_recall` 只是关键词匹配，不能完全替代语义评估。
- 本地 baseline 不是 embedding 检索。
- RAGFlow client 还需要真实环境 smoke test。
- 还没有接入 LLM-as-judge。

## 你要避免的说法

不要说：

> 我做了一个完整 RAG 系统。

更准确的说法是：

> 我做了一个 RAG 评测工具，并实现了本地检索 baseline 和多个 client 适配，用来评估 RAG 系统输出。

