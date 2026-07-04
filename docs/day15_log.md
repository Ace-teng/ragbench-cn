# Day 15 Log

## Goal

Run a real keyword vs embedding comparison instead of only wiring the feature.

## Completed

- Installed optional embedding dependencies with `pip install -e .[embedding]`.
- Loaded `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`.
- Ran `local-keyword` vs `local-embedding` with the same questions, docs, and `top_k=3`.
- Fixed a real JSON serialization bug where embedding scores could be `numpy.float32`.
- Regenerated `reports/client_comparison.*`.
- Updated client comparison documentation.

## Result

| Run | Citation Hit Rate | Avg Keyword Recall | Avg Precision@k | Avg Recall@k | Avg Latency ms |
| --- | ---: | ---: | ---: | ---: | ---: |
| local-keyword | 1.00 | 0.66 | 0.82 | 1.00 | 0.02 |
| local-embedding | 1.00 | 0.65 | 0.73 | 1.00 | 12.99 |

## Learning Notes

Embedding retrieval is not automatically better.

In this small controlled dataset, the embedding baseline found the gold source but also retrieved more non-gold chunks. That lowered precision@k and increased latency.

This is a stronger project result than forcing embedding to win. It shows the evaluator can reveal tradeoffs between retrieval strategies.
