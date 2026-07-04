# GitHub Release Note

## Title

RAGBench-CN v0.2.0: retrieval comparison and paraphrase evaluation

## Summary

RAGBench-CN is a lightweight toolkit for evaluating Chinese RAG QA systems with structured question sets.

This release expands the first working version into a more complete evaluation project: HTML reports, retrieval precision@k / recall@k, per-question diagnosis, local embedding retrieval, client comparison, and a paraphrase experiment for testing semantic retrieval.

## Highlights

- Markdown, JSON, and HTML reports.
- `local-keyword` baseline for local Markdown retrieval.
- Optional `local-embedding` baseline with SentenceTransformers.
- `openai-compatible` and `ragflow` clients.
- Top-k, chunk-size, and client comparison modes.
- Retrieval precision@k and recall@k.
- Per-question diagnosis and worst case analysis.
- Retrieved chunk previews in reports.
- `gold_docs` support for multiple acceptable source documents.
- Paraphrase question set for testing semantic retrieval.
- Checked-in keyword vs embedding comparison reports.
- Unit tests and GitHub Actions CI.

## Example Finding

The default Chinese question set shows that keyword retrieval can be highly competitive when question and document wording overlap.

The paraphrase question set shows the opposite condition: when questions are rewritten in English while documents remain Chinese, embedding retrieval reaches much higher citation hit rate and keyword recall.

This is the intended lesson of the project: retrieval strategy should be evaluated under different data distributions instead of assumed from the method name.

## Known Limitations

- `keyword_recall` is a lightweight heuristic, not a full semantic correctness metric.
- RAGFlow adapter still needs a real smoke test.
- LLM-as-judge is not implemented yet.
- Retrieval relevance is currently document-level through `gold_doc` / `gold_docs`.

## Next

- Run real RAGFlow smoke test.
- Improve citation extraction.
- Add optional LLM-as-judge.
- Add charts to HTML reports.
