# Day 5 Log

日期：2026-07-04

## 今日目标

控制 JSON 输出体积，让默认结果更适合保存、对比和提交。

## 已完成

- `eval.py` 增加 `--include-answers`。
- `compare.py` 增加 `--include-answers`。
- 默认 JSON 不再保存完整 `answer` 字段。
- 需要调试具体回答时，可以显式加 `--include-answers`。
- 新增 `pyproject.toml`。
- 增加 `ragbench-eval` 和 `ragbench-compare` 命令行入口。
- 接入 `openai-compatible` client 到 `ragbench-eval`。
- 支持通过命令行参数或环境变量配置 `base_url`、`api_key` 和 `model`。
- 接入最小 RAGFlow client，使用新版 `/api/v1/openai/{chat_id}/chat/completions` 路径。
- 清理 `reports/` 目录，只保留代表性示例报告。
- 新增 `reports/README.md` 说明每份报告的用途和再生成命令。
- 重写 `README.md`，改成更适合 GitHub 首屏展示的结构：Why、Features、Install、Quick Start、Example Result、Metrics、Clients、Roadmap。
- 新增 `docs/resume_and_interview.md`，整理简历项目描述和面试追问。
- 新增 `docs/github_release_note.md`，准备 v0.1 发布说明草稿。
- 新增 `LICENSE`、`CHANGELOG.md` 和 `docs/v0_1_checklist.md`，补齐 v0.1 开源发布基础文件。

## 你需要理解

评测工具通常有两类输出：

- 报告：给人看，重点是摘要、表格和 worst cases。
- JSON：给程序看，重点是结构化指标和可对比数据。

完整回答文本很长，默认放进 JSON 会让文件变大，也会干扰后续对比。更合理的做法是默认输出轻量结果，需要排查时再加 `--include-answers`。

`pyproject.toml` 的作用是让项目可以被 Python 当成包安装。安装后，用户不必记住 `python -m ragbench.eval`，可以直接使用 `ragbench-eval` 和 `ragbench-compare`。

`openai-compatible` 的作用是连接真实模型或服务。注意：如果目标服务不返回引用信息，`citation_hit` 会失败，这是目标服务输出格式限制，不是评测脚本错误。

RAGFlow client 目前只支持非流式 chat completion。引用字段会根据常见的 `reference` / `references` / `citations` 尝试提取，真实环境跑通后可能还要按具体返回结构调整。
