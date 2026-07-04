# Day 8 Log

## Goal

Make retrieval precision@k visible in the example experiments.

## Completed

- Added `examples/docs/retrieval_noise.md`.
- Regenerated local baseline, top-k, and chunk-size reports.
- Updated README example results.
- Rewrote top-k and chunk-size experiment notes.

## Learning Notes

The new noise document contains terms similar to the gold RAG document, but it is not the standard source for the question set.

This makes the experiment more realistic:

- top-k gets larger
- keyword recall improves
- citation hit rate improves or stays high
- precision@k can drop because more non-gold chunks enter the result set

This is a useful interview point because it shows why RAG evaluation should look at both recall-style metrics and precision-style metrics.
