# Day 12 Log

## Goal

Start v0.3 by adding a semantic retrieval baseline.

## Completed

- Added `LocalEmbeddingClient`.
- Added optional `sentence-transformers` dependency group.
- Added `--client local-embedding`.
- Added `--embedding-model`.
- Added tests with a fake encoder, so CI does not download real models.
- Added local embedding documentation.

## Learning Notes

Keyword retrieval ranks chunks by lexical overlap.

Embedding retrieval ranks chunks by vector similarity.

The embedding baseline is optional because local models add heavier dependencies and may need a model download on first run.
