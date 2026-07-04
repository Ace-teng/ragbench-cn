# OpenAI-Compatible Client

RAGBench-CN 现在支持 `openai-compatible` client。

它适合连接任何兼容 OpenAI `/chat/completions` 格式的服务。

## 命令示例

```powershell
ragbench-eval --client openai-compatible --questions examples/questions_zh.json --out reports/openai_report.md --json-out reports/openai_result.json --base-url http://localhost:8000/v1 --api-key YOUR_KEY --model YOUR_MODEL
```

也可以使用环境变量：

```powershell
$env:OPENAI_COMPATIBLE_BASE_URL="http://localhost:8000/v1"
$env:OPENAI_COMPATIBLE_API_KEY="YOUR_KEY"
$env:OPENAI_COMPATIBLE_MODEL="YOUR_MODEL"

ragbench-eval --client openai-compatible --questions examples/questions_zh.json --out reports/openai_report.md --json-out reports/openai_result.json
```

## 当前限制

OpenAI-compatible 接口通常只返回答案，不一定返回引用。

如果服务没有返回 `citations` 字段，`citation_hit` 通常会失败。这不是评测脚本错误，而是目标服务没有提供引用信息。

## 你需要理解

`local-keyword` 是本地检索 baseline。

`openai-compatible` 是外部模型/API 调用接口。

它们的区别：

| Client | 作用 |
| --- | --- |
| mock | 验证评测流程 |
| local-keyword | 验证本地检索和引用 |
| openai-compatible | 连接真实模型或服务 |

