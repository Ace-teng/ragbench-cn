# RAGBench-CN 面试必背文档

这份文档用于面试准备。目标不是背代码细节，而是能把项目讲成一个完整的工程故事：

- 为什么做这个项目
- 解决什么问题
- 我具体做了什么
- 技术方案如何设计
- 实验如何验证
- 有什么局限
- 面试官可能怎么追问

## 1. 一句话介绍

RAGBench-CN 是我做的一个轻量级中文 RAG 评测工具，用问题集批量测试知识库问答系统，并输出关键词召回率、引用命中率、延迟、失败类型和 worst cases，帮助判断 RAG 系统回答是否可靠。

## 2. 为什么做这个项目

### 可以这样讲

我一开始关注的是 RAG 应用，但发现很多项目只展示“能问答”，很少系统回答“答得准不准、引用对不对、参数调完有没有变好”。

所以我没有重复做一个 RAG 平台，而是做了一个评测工具。它可以接本地 baseline、OpenAI-compatible 服务或 RAGFlow，把不同系统的输出统一成可比较的报告。

### 我的思考

RAG 系统的问题不只是能不能生成答案，而是：

- 检索有没有找到正确文档
- 答案有没有覆盖关键点
- 引用来源是否正确
- 改 top-k / chunk size 后效果是否真的变好
- 哪些问题失败，失败原因是什么

### 可能追问

**问：为什么不直接做一个 RAG 问答系统？**

答：RAGFlow、Dify、FastGPT 这类工具已经能完成知识库问答链路。我这个项目关注评测层，用工程化方式衡量 RAG 输出质量。这样更容易体现我对 RAG 系统可靠性、指标设计和实验分析的理解。

## 3. 项目输入输出

### 可以这样讲

输入是一组结构化中文问题，每个问题包含：

- `question`：要问的问题
- `expected_keywords`：答案应该覆盖的关键词
- `gold_doc`：期望引用命中的文档

输出包括三种报告：

- Markdown：方便在 GitHub 上阅读
- JSON：方便程序继续分析
- HTML：方便浏览器展示、截图和演示

### 可能追问

**问：为什么需要 JSON？**

答：Markdown 和 HTML 面向人，JSON 面向程序。后续如果要做排行榜、可视化、自动回归测试，都应该基于结构化 JSON。

**问：为什么又加 HTML？**

答：HTML 不是新算法，而是展示层。它让评测结果更适合 demo 和截图，也说明我把评测逻辑和展示逻辑拆开了。

## 4. 我具体开发了什么

### 核心模块

- `ragbench/eval.py`：单次评测主流程
- `ragbench/compare.py`：top-k / chunk size 对比实验
- `ragbench/metrics.py`：指标计算
- `ragbench/clients/`：不同被测系统的适配器
- `ragbench/html_report.py`：HTML 报告生成
- `tests/`：单元测试
- `reports/`：示例输出

### 可以这样讲

我把项目拆成了几层：

- client 层负责调用被测系统
- eval 层负责批量跑问题和汇总结果
- metrics 层负责计算指标
- report 层负责输出 Markdown / JSON / HTML
- tests 负责保证核心逻辑稳定

这样做的好处是，如果以后换成真实 RAGFlow 或其他 LLM 服务，只需要替换 client，不需要重写评测逻辑。

### 可能追问

**问：你自己写了哪些，不是现成工具提供的？**

答：问题集格式、评测主流程、指标计算、Markdown/JSON/HTML 报告、local keyword baseline、top-k 和 chunk size 对比实验、client 适配层、单元测试和 GitHub Actions CI 都是我自己实现和组织的。RAGFlow 或 OpenAI-compatible 服务只是被测对象，不是项目核心。

## 5. 指标设计

## 5.1 keyword_recall

### 定义

```text
keyword_recall = 命中的 expected_keywords 数量 / expected_keywords 总数
```

### 可以这样讲

这个指标用来粗略判断答案有没有覆盖关键点。它简单、可解释、容易复现，适合 v0.1 阶段作为轻量评测指标。

### 局限

- 不能完整判断语义正确性
- 同义表达可能漏判
- 关键词命中不代表答案逻辑完全正确

### 可能追问

**问：keyword_recall 有什么问题？**

答：它是启发式指标，不是完整语义评测。比如答案用了同义词但没有命中关键词，可能被低估；反过来，答案堆了关键词但逻辑错了，也可能被高估。所以后续可以加入 embedding 相似度或 LLM-as-judge。

## 5.2 citation_hit_rate

### 定义

每个问题有一个 `gold_doc`。如果系统返回的 citations 中包含这个文档，就认为引用命中。

```text
citation_hit_rate = 引用命中的问题数 / 总问题数
```

### 可以这样讲

RAG 的一个关键价值是可溯源。答案看起来流畅不代表可靠，所以我单独评估引用是否命中预期文档。

### 可能追问

**问：引用命中了就代表答案正确吗？**

答：不一定。引用命中只能说明检索来源可能正确，答案是否完整还要看关键词覆盖、人工检查或更强的语义评测。

## 6. top-k 实验怎么讲

### 定义

top-k 表示检索阶段返回多少个 chunk。

### 可以这样讲

我做了 top-k 对比实验，比如 `top_k=1,3,5`。在当前 local keyword baseline 下，top-k 变大后返回的 chunk 更多，所以关键词覆盖率通常会提高。

但真实 RAG 系统里，top-k 不是越大越好。它可能带来：

- 更多噪声
- 更高上下文成本
- 更长延迟
- 更容易让模型被无关信息干扰

### 可能追问

**问：如果 top-k 越大召回越好，为什么不一直设很大？**

答：因为 RAG 不只看召回，还要看生成质量、上下文长度、成本和延迟。过大的 top-k 可能把无关 chunk 一起塞给模型，导致答案变差。

## 7. chunk size 实验怎么讲

### 定义

chunk size 表示每个可检索文本片段的大小。

### 可以这样讲

chunk 太小，可能丢上下文；chunk 太大，可能包含太多无关信息。这个项目支持 chunk size 对比，是为了观察不同切分粒度对结果的影响。

### 可能追问

**问：如何选择合适的 chunk size？**

答：要结合文档结构和任务类型。定义类、概念解释类问题可以用较短 chunk；复杂流程、长上下文依赖的问题可能需要更大的 chunk 或 chunk overlap。最终应该通过评测结果而不是感觉来调。

## 8. local keyword baseline 怎么讲

### 可以这样讲

local keyword baseline 是一个本地可运行的检索 baseline。它读取 Markdown 文档，切成 chunk，然后根据问题词和 chunk 的重合度排序，返回 top-k 片段。

它不是为了替代 embedding 检索，而是为了让项目在没有外部服务时也能完整跑通评测闭环。

### 可能追问

**问：为什么不用向量数据库？**

答：v0.1 阶段我先做最小可复现 baseline，保证问题集、评测、指标、报告和测试闭环成立。向量检索是后续增强方向，应该在基础评测框架稳定后再接入。

## 9. client 适配层怎么讲

### 可以这样讲

我把被测系统抽象成 client，只要求它提供 `ask(question)`，返回：

- `answer`
- `citations`
- `latency_ms`

这样评测逻辑不关心底层是 mock、本地 baseline、OpenAI-compatible 服务还是 RAGFlow。

### 可能追问

**问：如果 RAGFlow 返回格式变了怎么办？**

答：只需要改 `ragbench/clients/ragflow.py` 的解析逻辑，评测主流程和指标不需要改。这就是适配层的价值。

## 10. HTML 报告怎么讲

### 可以这样讲

HTML 报告是 v0.2 的展示层增强。它复用同一份评测结果，只是换一种更适合浏览器展示的格式。

实现时我单独建了 `ragbench/html_report.py`，没有把 HTML 字符串散落在 eval 和 compare 里。命令行通过 `--html-out` 控制是否生成 HTML。

### 安全细节

HTML 报告里会展示问题文本、失败类型、实验备注等内容。这些文本可能包含特殊字符，所以我用了 `html.escape` 做转义，避免把用户文本当成 HTML 或脚本执行。

### 可能追问

**问：为什么要做转义？**

答：因为报告内容可能来自外部问题集或模型输出。如果直接拼进 HTML，理论上可能造成 HTML 注入。虽然这是本地报告，但养成输出转义的习惯是基本工程安全意识。

## 11. 测试和 CI 怎么讲

### 可以这样讲

项目使用 `unittest` 做单元测试，覆盖指标、local baseline、compare、OpenAI-compatible client、RAGFlow client 和 HTML 报告。然后用 GitHub Actions 在 Python 3.10、3.11、3.12 上自动跑测试。

### 可能追问

**问：CI 的价值是什么？**

答：CI 保证每次 push 或 PR 后自动验证项目还能跑。它不是业务功能，但能体现工程规范，避免后续修改破坏已有行为。

## 12. worst cases 怎么讲

### 可以这样讲

平均指标只能说明整体趋势，worst cases 能指出具体失败样例。RAG 系统调优时，知道“平均分提高了”不够，还要知道哪些问题仍然失败，以及失败是因为关键词缺失、引用没命中还是答案为空。

### 可能追问

**问：为什么不只看平均分？**

答：平均分会掩盖局部问题。比如整体召回不错，但某类问题一直失败，只有 worst cases 才能帮助定位。

## 13. 当前局限

### 必须诚实讲

- local keyword baseline 不是语义检索
- keyword_recall 不能替代完整语义正确性评估
- RAGFlow client 还需要真实环境 smoke test
- 还没有 LLM-as-judge
- 示例数据集规模还比较小

### 可以这样收束

这个项目目前不是追求“大而全”，而是先把评测闭环做完整：问题集、client、指标、报告、对比实验、测试和 CI。后续增强可以围绕更真实的检索、更强的评测指标和更大的数据集展开。

## 14. 面试 1 分钟版本

RAGBench-CN 是我做的一个中文 RAG 评测工具。它不是重新做一个 RAG 平台，而是解决 RAG 系统搭好之后“怎么判断回答是否可靠”的问题。

项目输入是一组结构化中文问题，每个问题包含期望关键词和标准引用文档。工具会调用被测系统，比如本地检索 baseline、OpenAI-compatible 服务或 RAGFlow，然后统计关键词召回率、引用命中率、平均延迟、失败类型和 worst cases，并输出 Markdown、JSON 和 HTML 报告。

我还做了 top-k 和 chunk size 的对比实验，用来观察检索返回数量和文本切分粒度对结果的影响。工程上我把 client、评测流程、指标和报告生成拆开，并补了单元测试和 GitHub Actions CI。当前局限是 keyword_recall 还是轻量启发式指标，本地 baseline 不是语义检索，后续可以加入 embedding 检索和 LLM-as-judge。

## 15. 面试 3 分钟版本结构

1. 背景：RAG 应用常见，但评测不足。
2. 目标：做一个轻量中文 RAG 评测工具。
3. 输入输出：问题集输入，Markdown/JSON/HTML 报告输出。
4. 技术设计：client 适配层、eval 主流程、metrics、report、tests。
5. 指标：keyword_recall、citation_hit_rate、latency、failure_type、worst_cases。
6. 实验：top-k 和 chunk size 对比。
7. 工程化：pyproject、命令行入口、unittest、GitHub Actions、release。
8. 局限和改进：embedding 检索、真实 RAGFlow smoke test、LLM-as-judge、更大数据集。

## 16. 不要这样说

不要说：

> 我做了一个完整 RAG 系统。

更准确：

> 我做了一个 RAG 评测工具，并实现了本地检索 baseline 和多个 client 适配，用来评估 RAG 系统输出质量。

不要说：

> 我的指标能完全判断答案正确。

更准确：

> 当前指标是轻量、可解释、可复现的启发式指标，可以帮助发现问题，但不能完全替代人工评估或语义评测。

