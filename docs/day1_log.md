# Day 1 Log

日期：2026-07-04

## 今日目标

把 RAGBench-CN 项目立起来，形成一个可以本地运行的最小版本。

## 已完成

- 创建项目目录 `ragbench-cn`。
- 编写 `README.md`。
- 编写 20 条中文 RAG 测试问题：`examples/questions_zh.json`。
- 编写 RAG 基础文档：`examples/docs/rag_basics.md`。
- 编写基础评测脚本：`ragbench/eval.py`。
- 编写指标函数：`ragbench/metrics.py`。
- 编写 mock client：`ragbench/clients/mock.py`。
- 预留 OpenAI-compatible client 和 RAGFlow client。
- 生成示例报告：`reports/sample_report.md`。
- 添加 `.gitignore`。

## 已验证命令

```powershell
python -m ragbench.eval --questions examples/questions_zh.json --out reports/sample_report.md --mock
```

结果：命令可运行，并生成 Markdown 报告。

## 当前理解

RAGBench-CN 的输入是问题集，输出是评估报告。

当前版本使用 mock client，不代表真实 RAG 系统效果。下一步需要接入真实被测系统，比如 RAGFlow 或 OpenAI-compatible API。

## 明日建议

- 打磨 README，让别人 3 分钟能看懂并跑起来。
- 优化 `sample_report.md` 的展示格式。
- 给 `questions_zh.json` 增加字段说明。
- 设计 RAGFlow client 的实际接口方案。

