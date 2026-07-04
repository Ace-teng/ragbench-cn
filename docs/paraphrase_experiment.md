# Paraphrase Experiment

This experiment checks whether a semantic retriever helps when questions do not share many surface words with the Chinese source document.

The question set is:

```text
examples/questions_paraphrase.json
```

It uses English paraphrase questions against the same Chinese Markdown documents.

## Run

```powershell
pip install -e .[embedding]
ragbench-compare --mode client --clients local-keyword,local-embedding --questions examples/questions_paraphrase.json --docs-dir examples/docs --top-k 3 --out reports/paraphrase_client_comparison.md --json-out reports/paraphrase_client_comparison.json --html-out reports/paraphrase_client_comparison.html
```

## Why

The default Chinese question set has strong lexical overlap with `rag_basics.md`, so `local-keyword` is a strong baseline.

The paraphrase set intentionally reduces lexical overlap. It tests a different condition:

```text
same meaning, different wording
```

This is where embedding retrieval should have a better chance to help.

## Result

| Run | Citation Hit Rate | Avg Keyword Recall | Avg Precision@k | Avg Recall@k | Avg Latency ms | Failure Counts |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| local-keyword | 0.33 | 0.17 | 1.00 | 1.00 | 0.01 | empty_answer=4, keyword_missing=1, ok=1 |
| local-embedding | 1.00 | 0.92 | 0.67 | 1.00 | 13.92 | ok=6 |

## Interpretation

The result is intentionally different from the default Chinese question set.

On the default set, `local-keyword` is strong because the questions share many words with the source document. On this paraphrase set, `local-keyword` often returns no usable answer because English questions have little lexical overlap with Chinese documents.

`local-embedding` handles this condition better: it reaches 1.00 citation hit rate and 0.92 average keyword recall. Its precision@k is lower because semantic retrieval can still bring in similar but non-gold chunks. This is a useful tradeoff, not a contradiction.

Note: retrieval precision@k and recall@k are averaged over questions with returned retrieved chunks. Empty-answer cases are reflected by `empty_answer`, citation hit rate, and keyword recall.

## Interview Notes

可以这样讲：

> 我没有只用一组问题证明 embedding 好或不好，而是补了一组 paraphrase 问题。默认中文问题集词面重合度高，keyword baseline 很强；paraphrase 问题集降低词面重合，更适合观察 embedding retrieval 的优势边界。
