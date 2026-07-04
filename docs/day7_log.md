# Day 7 Log

## Goal

Add a retrieval-side metric, not only answer-side metrics.

## Completed

- Added `retrieval_precision_at_k`.
- Local keyword baseline now returns retrieved chunk metadata.
- Evaluation reports include per-question precision@k.
- Summary reports include average precision@k.
- Comparison reports include average precision@k.
- HTML reports display precision@k.
- Added unit tests for precision@k and retrieved chunks.

## Learning Notes

`citation_hit_rate` answers: did we hit the expected source at least once?

`retrieval_precision_at_k` answers: among the retrieved chunks, how many are relevant?

These two metrics are related but not the same. A system can hit the right source while also returning many noisy chunks. Precision@k helps expose that noise.

This matters for RAG because retrieval quality affects generation quality. If the context contains too much unrelated content, the model may produce worse answers even when the correct document appears somewhere in the retrieved set.
