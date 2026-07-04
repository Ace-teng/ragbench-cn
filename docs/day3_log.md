# Day 3 Log

日期：2026-07-04

## 今日目标

在 mock 之外增加一个真实读取本地文档的检索 baseline，帮助理解 RAG 里的 retrieval。

## 已完成

- 新增 `ragbench/clients/local_keyword.py`。
- `eval.py` 支持 `--client mock/local-keyword`。
- `eval.py` 支持 `--docs-dir` 和 `--top-k`。
- 新增 `docs/local_keyword_baseline.md`。
- 新增 `tests/test_local_keyword.py`。

## 你需要理解

`mock` 是固定返回答案，只验证评测流程。

`local-keyword` 会读取本地 Markdown 文档，按简单词项重叠检索相关 chunk。它是一个 baseline，不是最终 RAG。

这个 baseline 的意义是让你先掌握：

- 文档如何被切成 chunk。
- 问题如何和 chunk 做匹配。
- top-k 如何影响返回片段数量。
- citation_hit 为什么依赖检索结果。

## 已验证命令

```powershell
python -m ragbench.eval --questions examples/questions_zh.json --out reports/local_keyword_report.md --json-out reports/local_keyword_result.json --client local-keyword --docs-dir examples/docs --top-k 3
python -m unittest discover -s tests
```

