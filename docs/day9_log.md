# Day 9 Log

## Goal

Complete the retrieval metric pair: precision@k and recall@k.

## Completed

- Added `retrieval_recall_at_k`.
- Evaluation rows now include recall@k.
- Summary reports include average recall@k.
- JSON output includes compact retrieved chunk previews.
- Markdown reports show retrieved chunks for worst cases.
- Comparison reports include average recall@k.
- HTML reports include average recall@k.
- Added tests for recall@k and eval retrieval metadata.

## Learning Notes

`retrieval_recall_at_k` asks whether the gold source appears anywhere in the retrieved top-k chunks.

`retrieval_precision_at_k` asks how much of the retrieved top-k set is relevant.

Together:

- High recall@k and low precision@k means the right source is present, but there is noise.
- Low recall@k means the retriever missed the expected source.
- High precision@k and high recall@k is the ideal local retrieval result.

Retrieved chunk previews make reports easier to debug because they show what evidence the system actually used.
