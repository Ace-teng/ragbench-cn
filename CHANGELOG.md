# Changelog

## v0.1.0 - Draft

Initial working version of RAGBench-CN.

### Added

- Chinese question set format.
- Markdown and JSON report output.
- `ragbench-eval` command.
- `ragbench-compare` command.
- Mock client.
- Local Markdown keyword retrieval baseline.
- OpenAI-compatible client.
- Minimal RAGFlow client.
- Keyword recall metric.
- Citation hit rate metric.
- Average latency metric.
- Failure type classification.
- Worst case analysis.
- Top-k comparison.
- Chunk size comparison.
- Unit tests.
- Example reports.

### Known Limitations

- Local keyword baseline is not semantic retrieval.
- `keyword_recall` is a lightweight heuristic.
- RAGFlow adapter still needs a real smoke test.
- LLM-as-judge is not implemented.

