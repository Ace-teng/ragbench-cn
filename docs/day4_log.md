# Day 4 Log

日期：2026-07-04

## 今日目标

把单次评测扩展成参数对比实验。

## 已完成

- 新增 `ragbench/compare.py`。
- 支持 `--top-k 1,3,5` 形式的多组实验。
- 支持 `--mode chunk-size` 对比不同 chunk size。
- 输出 Markdown 对比报告。
- 输出 JSON 对比结果。
- 报告中加入 worst cases，用于分析具体失败样例。
- 新增 `docs/top_k_experiment.md`。
- 新增 `docs/chunk_size_experiment.md`。
- 新增 `docs/failure_analysis.md`。
- 新增 `tests/test_compare.py`。

## 你需要理解

`eval.py` 做单次评测。

`compare.py` 做多组实验。

这两个脚本分开，是为了让项目职责清楚：

- `eval`：回答“这一次效果怎么样？”
- `compare`：回答“参数变了之后效果怎么变？”

两个核心参数：

- `top-k`：返回多少个 chunk。
- `chunk size`：每个 chunk 有多大。
- `worst cases`：最值得优先排查的失败样例。
