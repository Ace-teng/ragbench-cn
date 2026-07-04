# RAGBench-CN Client Comparison

## Summary

| Run | Citation Hit Rate | Avg Keyword Recall | Avg Precision@k | Avg Recall@k | Avg Latency ms | Failure Counts |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| local-keyword | 0.33 | 0.17 | 1.00 | 1.00 | 0.01 | empty_answer=4, keyword_missing=1, ok=1 |
| local-embedding | 1.00 | 0.92 | 0.67 | 1.00 | 13.92 | ok=6 |

## How To Read

- Compare citation hit rate, keyword recall, precision@k, recall@k, latency, and failure counts together.
- Higher recall is not always better if precision drops sharply.
- Local baselines are useful for controlled experiments, but production RAG should be tested with real services.

## Experiment Notes

- Client comparison keeps the same questions and docs while changing retrieval strategy.
- `local-keyword` ranks chunks by lexical overlap.
- `local-embedding` ranks chunks by vector similarity and requires the optional embedding dependency.

## Worst Cases By Run

### local-keyword

| ID | Keyword Recall | Precision@k | Recall@k | Citation Hit | Failure Type | Diagnosis | Question |
| --- | ---: | ---: | ---: | --- | --- | --- | --- |
| p003 | 0.00 | N/A | N/A | False | empty_answer | empty_answer: no answer was returned | What is the role of dense vectors in finding relevant passages? |
| p004 | 0.00 | N/A | N/A | False | empty_answer | empty_answer: no answer was returned | Why is fluent wording not enough to trust an answer from a knowledge-base QA system? |
| p006 | 0.00 | N/A | N/A | False | empty_answer | empty_answer: no answer was returned | How can candidate passages be reordered after the first retrieval step? |

### local-embedding

| ID | Keyword Recall | Precision@k | Recall@k | Citation Hit | Failure Type | Diagnosis | Question |
| --- | ---: | ---: | ---: | --- | --- | --- | --- |
| p002 | 0.75 | 0.67 | 1.00 | True | ok | ok: answer passed the current lightweight checks | Why can giving a model more retrieved passages make the answer worse? |
| p006 | 0.75 | 0.67 | 1.00 | True | ok | ok: answer passed the current lightweight checks | How can candidate passages be reordered after the first retrieval step? |
| p005 | 1.00 | 1.00 | 1.00 | True | ok | ok: answer passed the current lightweight checks | What evidence should an interview-ready RAG project keep? |
