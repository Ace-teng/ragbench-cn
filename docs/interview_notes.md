# Interview Notes

## 一句话介绍

RAGBench-CN 是一个轻量中文 RAG 评测工具，用问题集批量测试知识库问答系统，统计关键词召回率、引用命中率、平均延迟和失败类型。

## 为什么不是直接做 RAG 平台

RAGFlow、Dify、FastGPT 已经能完成知识库问答链路。这个项目不重复造平台，而是解决评估问题：系统回答得是否可靠，引用是否命中正确文档，参数调整后效果是否变好。

## 我自己做了什么

- 设计问题集 JSON 格式。
- 实现批量评测脚本。
- 实现关键词召回率和引用命中率等基础指标。
- 实现 Markdown 报告生成。
- 编写中文 RAG 示例文档和测试问题。
- 预留真实 RAG 系统 client 接口。

## 当前版本的限制

- 目前使用 mock client。
- 关键词召回率只能做粗粒度判断，不能完全替代人工评估。
- 还没有接入真实 RAGFlow 接口。
- 还没有做 LLM-as-judge。

## 后续改进

- 接入 RAGFlow API。
- 支持 OpenAI-compatible RAG 服务。
- 增加 retrieval precision@k。
- 增加参数对比实验：top-k、chunk size、rerank。
- 增加 HTML 报告或可视化图表。

## 面试追问

1. RAGBench-CN 的输入输出是什么？
2. citation_hit_rate 怎么计算？
3. keyword_recall 有什么局限？
4. 为什么 RAG 回答流畅不代表正确？
5. top-k 变大会带来什么影响？
6. chunk size 太大或太小分别有什么问题？
7. RAGFlow 做了什么，你自己做了什么？
8. 如何把 mock client 替换成真实 RAGFlow client？

更多完整材料见 `docs/resume_and_interview.md`。
