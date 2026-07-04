# Day 13 Log

## Goal

Make the embedding baseline useful in experiments.

## Completed

- Added `--mode client` to `ragbench-compare`.
- Added `--clients`.
- Added `run_client_comparison`.
- Generated `reports/client_comparison.*`.
- Added tests for client comparison with a fake embedding encoder.
- Added client comparison documentation.

## Learning Notes

Adding a new client is only half the work. To make it useful, the project also needs an experiment path that compares it against existing baselines.

Client comparison answers:

```text
same questions + same docs + same top-k, different retriever
```

This is the right setup for comparing keyword retrieval and embedding retrieval.
