# Day 16 Log

## Goal

Add a targeted paraphrase experiment to test when embedding retrieval may help.

## Completed

- Added `examples/questions_paraphrase.json`.
- Added paraphrase experiment documentation.
- Prepared a client comparison command for `local-keyword` vs `local-embedding`.
- Ran the real paraphrase client comparison.
- Added Markdown, JSON, and HTML paraphrase reports.

## Result

| Run | Citation Hit Rate | Avg Keyword Recall | Avg Precision@k | Avg Recall@k | Avg Latency ms |
| --- | ---: | ---: | ---: | ---: | ---: |
| local-keyword | 0.33 | 0.17 | 1.00 | 1.00 | 0.01 |
| local-embedding | 1.00 | 0.92 | 0.67 | 1.00 | 13.92 |

## Learning Notes

The default question set has high lexical overlap with the Chinese source document, so keyword retrieval is a strong baseline.

A paraphrase question set reduces lexical overlap. This is a better test for semantic retrieval.

This keeps the project honest: instead of claiming embedding is always better, we test the conditions where it should be more useful.

The two client-comparison experiments should be read together:

- Default Chinese questions: keyword is competitive because lexical overlap is high.
- English paraphrase questions: embedding is better because semantic matching matters more.

This is the core lesson: retrieval quality depends on the data distribution, not only on whether the retriever sounds more advanced.
