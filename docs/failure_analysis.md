# Failure Analysis

Average metrics show the overall trend, but they do not explain what went wrong for a specific question.

RAGBench-CN reports three layers of failure analysis:

- `failure_type`: coarse category for sorting and counting.
- `diagnosis`: short human-readable explanation.
- retrieved chunk previews: evidence for debugging retrieval behavior.

## Failure Type

Current coarse categories:

| Type | Meaning |
| --- | --- |
| ok | Citation hit and keyword recall are acceptable under current lightweight checks. |
| empty_answer | The client returned no answer. |
| retrieval_miss | Citation did not hit and keyword recall is low. |
| citation_missing | Keyword recall is acceptable, but the expected source was not cited. |
| keyword_missing | Citation hit, but the answer missed expected key concepts. |

## Diagnosis

`diagnosis` combines multiple signals into a readable explanation.

Examples:

| Diagnosis | Meaning |
| --- | --- |
| `retrieval_miss: gold source was not retrieved` | The expected source did not appear in retrieved chunks. |
| `noisy_retrieval: gold source was retrieved but top-k contains many non-gold chunks` | Recall is fine, but precision@k is low. |
| `citation_missing: answer did not cite the expected source` | The answer did not cite the gold source. |
| `keyword_missing: answer missed expected key concepts` | The answer did not cover enough expected keywords. |
| `ok: answer passed the current lightweight checks` | The current checks did not detect an issue. |

`failure_type` and `diagnosis` are intentionally separate. A row can have `failure_type=ok` but still receive a noisy retrieval diagnosis. That means the answer passed the lightweight answer checks, but the retrieved context still contains too much noise.

## Retrieved Chunks

For worst cases, the Markdown report includes retrieved chunk previews:

- rank
- source document
- retrieval score
- text preview

This makes debugging more concrete. Instead of only seeing that a question failed, you can inspect which chunks were returned and whether the context was missing, noisy, or poorly ranked.

## Interview Notes

可以这样讲：

> 我没有只输出平均分，而是把失败分析拆成 failure_type、diagnosis 和 retrieved chunks。failure_type 用来统计，diagnosis 用来解释，retrieved chunks 用来定位证据。这样能区分漏召回、引用缺失、关键词缺失和噪声检索，而不是只说这个问题答错了。
