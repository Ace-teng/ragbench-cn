# Day 10 Log

## Goal

Make failure analysis easier to explain and debug.

## Completed

- Added per-question `diagnosis`.
- Markdown reports now show diagnosis in details and worst cases.
- JSON output includes diagnosis.
- HTML reports include diagnosis.
- Failure analysis documentation was updated.
- Added tests for diagnosis rules and HTML escaping.

## Learning Notes

Metrics tell us what happened numerically. Diagnosis explains what likely happened in words.

Examples:

- `retrieval_miss`: the gold source was not retrieved.
- `noisy_retrieval`: the gold source was retrieved, but top-k contains many non-gold chunks.
- `keyword_missing`: the source was hit, but expected concepts were missing from the answer.

This is useful because RAG debugging usually needs both numbers and evidence.
