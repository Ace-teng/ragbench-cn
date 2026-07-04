# Day 2 Log

日期：2026-07-04

## 今日目标

把 Day 1 的脚本推进成更像开源项目的最小版本：报告更清楚，结果可被程序读取，指标有文档和测试。

## 已完成

- 给 `ragbench/eval.py` 增加 summary 统计。
- 给 Markdown 报告增加 Failure Types 汇总。
- 增加 `--json-out`，支持输出机器可读 JSON。
- 新增 `docs/metrics.md`，解释指标含义、计算方式和局限。
- 新增 `tests/test_metrics.py`，用标准库 `unittest` 验证核心指标函数。

## 你需要理解

RAGBench-CN 的评测结果分成两层：

- Markdown：给人看，适合 GitHub README、报告和面试展示。
- JSON：给程序看，后续可以做图表、对比实验和自动化分析。

当前指标不是完美答案评判器，而是轻量诊断工具。

测试命令：

```powershell
python -m unittest discover -s tests
```

## 今日重点概念

- `keyword_recall`：答案覆盖了多少预期关键词。
- `citation_hit`：引用是否命中标准文档。
- `failure_type`：把失败粗略分成检索失败、引用缺失、关键词缺失等类型。
