# RAGBench-CN Project Brief

## 项目是什么

RAGBench-CN 是一个轻量中文 RAG 评测工具。

它不是聊天机器人，也不是新的 RAG 平台。它的目标是用一套问题集自动测试知识库问答系统，输出关键词召回率、引用命中率、检索 precision@k / recall@k、平均延迟、失败类型、诊断信息和 worst cases 报告。

## 为什么做

很多 RAG demo 能回答问题，但缺少评估：

- 不知道是否引用了正确文档。
- 不知道答案是否覆盖关键点。
- 不知道 top-k、chunk size、retriever 调整后有没有变好。
- 面试时很难讲清失败 case 和优化依据。

RAGBench-CN 关注的是“RAG 系统到底准不准”，不是只做一个看起来能回答的 demo。

## 目标用户

- 学生和实习候选人。
- 正在搭 RAGFlow、Dify、FastGPT 或 LangChain 知识库的人。
- 想快速评估中文 RAG 项目效果的人。

## v0.2 边界

当前版本聚焦命令行评测工具：

- 读取结构化问题集。
- 调用 mock、本地 Markdown baseline、OpenAI-compatible 服务或 RAGFlow。
- 支持 keyword retrieval 和 optional embedding retrieval。
- 计算 citation hit rate、keyword recall、retrieval precision@k、retrieval recall@k、latency、failure type 和 diagnosis。
- 输出 Markdown、JSON、HTML 报告。
- 支持 top-k、chunk size、client 和 paraphrase 对比实验。

暂时不做：

- Web UI。
- 完整 RAG 平台。
- 复杂 LLM-as-judge。
- 多平台深度适配。
- 大规模真实数据集。

## 核心实验结论

默认中文问题集里，问题和文档词面重合高，所以 keyword baseline 很有竞争力。

paraphrase 问题集里，问题被改写成英文，文档仍然是中文，词面重合明显降低。这时 embedding retrieval 明显更适合。

这个项目的重点不是证明某个检索方法永远更好，而是用可复现指标解释不同数据分布下的 retrieval tradeoff。

## 简历表达

设计并实现轻量中文 RAG 评测工具，支持批量问题集测试、引用命中率、关键词召回率、检索 precision@k / recall@k、平均延迟、失败类型和 worst cases 分析；实现本地 keyword / embedding baseline、OpenAI-compatible client 和 RAGFlow client，并输出 Markdown / JSON / HTML 评估报告。
