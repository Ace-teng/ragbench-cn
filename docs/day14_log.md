# Day 14 Log

## Goal

Make comparison reports as useful for debugging as single-run reports.

## Completed

- Upgraded comparison report worst cases.
- Added precision@k, recall@k, and diagnosis to comparison Markdown reports.
- Added worst cases by run to comparison HTML reports.
- Added HTML escaping coverage for comparison worst cases.
- Regenerated comparison example reports.

## Learning Notes

Comparison reports should not stop at averages.

When comparing top-k, chunk size, or retrieval clients, the most useful debugging signal is often the worst cases for each run.

Adding diagnosis to comparison reports makes it possible to see whether a run got worse because of missing key concepts, retrieval miss, citation miss, or noisy retrieval.
