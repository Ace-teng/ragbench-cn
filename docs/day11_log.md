# Day 11 Log

## Goal

Support questions with multiple expected source documents.

## Completed

- Added `gold_docs` support.
- Kept backward compatibility with existing `gold_doc`.
- Updated citation hit, precision@k, and recall@k to accept one or many gold documents.
- Added tests for multi-source metrics and evaluation rows.
- Updated README and metrics documentation.

## Learning Notes

Real RAG questions may be supported by more than one document.

With multiple gold docs:

- `citation_hit` passes if any expected source is cited.
- `precision@k` measures how many retrieved chunks come from any expected source.
- `recall@k` measures how many expected sources appeared in top-k.

This makes the evaluator more realistic without breaking the simple `gold_doc` format.
