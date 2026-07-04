# Changelog

## v0.2.0 - 2026-07-04

### Added

- HTML report output for `ragbench-eval` via `--html-out`.
- HTML comparison report output for `ragbench-compare` via `--html-out`.
- Example HTML reports.
- HTML report documentation.
- Retrieval precision@k metric for clients that return retrieved chunks.
- Retrieval recall@k metric for clients that return retrieved chunks.
- Retrieved chunk metadata in the local keyword baseline.
- Retrieval noise example document for precision@k experiments.
- Retrieved chunk previews in JSON and Markdown reports.
- Per-question diagnosis text for failure analysis.
- Multiple expected source documents through `gold_docs`.
- Optional local embedding retrieval baseline with `local-embedding`.
- Client comparison mode for comparing retrieval clients.
- Diagnosis and retrieval metrics in comparison report worst cases.
- Checked-in keyword vs embedding client comparison report.
- Paraphrase question set for testing semantic retrieval.
- Checked-in paraphrase keyword vs embedding comparison report.

### Changed

- Clarified retrieval precision@k and recall@k aggregation when a question has no returned chunks.

## v0.1.0 - 2026-07-04

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
