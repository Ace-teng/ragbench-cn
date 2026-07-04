# GitHub Release Note Draft

## Title

RAGBench-CN v0.1.0: lightweight Chinese RAG evaluation toolkit

## Summary

RAGBench-CN is a lightweight toolkit for evaluating Chinese RAG QA systems with structured question sets.

It supports Markdown / JSON reports, local keyword retrieval baseline, top-k comparison, chunk size comparison, worst case analysis, OpenAI-compatible services, and a minimal RAGFlow adapter.

## Highlights

- Chinese question set format
- `ragbench-eval` command
- `ragbench-compare` command
- Mock client
- Local Markdown keyword retrieval baseline
- OpenAI-compatible client
- RAGFlow client
- Keyword recall
- Citation hit rate
- Average latency
- Failure type analysis
- Worst cases
- Top-k comparison
- Chunk size comparison
- Unit tests

## Known Limitations

- Local keyword baseline is not semantic retrieval.
- `keyword_recall` is a lightweight heuristic, not a full semantic correctness metric.
- RAGFlow adapter still needs a real smoke test.
- LLM-as-judge is not implemented yet.

## Next

- Run real RAGFlow smoke test.
- Improve citation extraction.
- Add optional LLM-as-judge.
- Add HTML report or charts.

