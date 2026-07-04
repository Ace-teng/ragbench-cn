# v0.2 Checklist

## Code

- [x] `ragbench-eval` works.
- [x] `ragbench-compare` works.
- [x] Mock client works.
- [x] Local keyword baseline works.
- [x] Optional local embedding baseline works.
- [x] OpenAI-compatible client is wired.
- [x] RAGFlow client is wired.
- [x] Unit tests pass.

## Metrics

- [x] Keyword recall.
- [x] Citation hit rate.
- [x] Retrieval precision@k.
- [x] Retrieval recall@k.
- [x] Average latency.
- [x] Failure type classification.
- [x] Per-question diagnosis.
- [x] Worst case analysis.

## Reports

- [x] Markdown report.
- [x] JSON report.
- [x] HTML report.
- [x] Retrieved chunk previews.
- [x] Top-k comparison report.
- [x] Chunk-size comparison report.
- [x] Keyword vs embedding comparison report.
- [x] Paraphrase comparison report.

## Docs

- [x] README.
- [x] Metrics explanation.
- [x] Local keyword baseline explanation.
- [x] Local embedding baseline explanation.
- [x] Top-k experiment explanation.
- [x] Chunk-size experiment explanation.
- [x] Client comparison explanation.
- [x] Paraphrase experiment explanation.
- [x] Failure analysis explanation.
- [x] Release note draft.
- [x] Changelog.

## Still Pending

- [ ] Real RAGFlow smoke test.
- [ ] LLM-as-judge metrics.
- [ ] HTML charts.
- [ ] Larger real-world dataset.

## v0.2 Definition

v0.2 is ready when:

1. A new user can install the project with `pip install -e .`.
2. A new user can run mock, local keyword, and local embedding examples.
3. Reports can be regenerated from README and reports documentation.
4. Keyword, embedding, top-k, chunk-size, and paraphrase experiments are documented.
5. Tests pass.
6. Known limitations are clearly documented.
