# RAGFlow Client

RAGBench-CN includes a minimal RAGFlow client.

It uses RAGFlow's OpenAI-compatible HTTP API:

```text
POST /api/v1/openai/{chat_id}/chat/completions
```

The older path `/api/v1/chats_openai/{chat_id}/chat/completions` is deprecated in current RAGFlow docs.

## Command

```powershell
ragbench-eval --client ragflow --questions examples/questions_zh.json --out reports/ragflow_report.md --json-out reports/ragflow_result.json --base-url http://localhost:9380 --api-key YOUR_RAGFLOW_KEY --chat-id YOUR_CHAT_ID --model model
```

Environment variables are also supported:

```powershell
$env:RAGFLOW_BASE_URL="http://localhost:9380"
$env:RAGFLOW_API_KEY="YOUR_RAGFLOW_KEY"
$env:RAGFLOW_CHAT_ID="YOUR_CHAT_ID"
$env:RAGFLOW_MODEL="model"

ragbench-eval --client ragflow --questions examples/questions_zh.json --out reports/ragflow_report.md --json-out reports/ragflow_result.json
```

## Current Scope

This adapter only handles non-streaming chat completion.

It extracts the answer from:

```text
choices[0].message.content
```

It tries to extract citations from fields such as:

```text
reference
references
citations
```

RAGFlow response formats may differ across versions. If citation extraction fails, the adapter may need small adjustments after a real smoke test.

