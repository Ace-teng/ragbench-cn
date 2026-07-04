# RAGBench-CN Sample Report

## Summary

- Client: local-keyword
- Questions: 20
- Citation hit rate: 1.00
- Average keyword recall: 0.66
- Average retrieval precision@k: 0.82
- Average retrieval recall@k: 1.00
- Average latency: 0.03 ms

## Failure Types

| Type | Count |
| --- | ---: |
| keyword_missing | 2 |
| ok | 18 |

## Details

| ID | Keyword Recall | Precision@k | Recall@k | Citation Hit | Latency ms | Failure Type | Question |
| --- | ---: | ---: | ---: | --- | ---: | --- | --- |
| q001 | 0.25 | 1.00 | 1.00 | True | 0.03 | keyword_missing | RAG 的基本流程是什么？ |
| q002 | 0.75 | 0.67 | 1.00 | True | 0.03 | ok | RAG 中 chunk size 过大会带来什么问题？ |
| q003 | 0.50 | 0.33 | 1.00 | True | 0.03 | ok | chunk size 过小会带来什么问题？ |
| q004 | 0.75 | 0.67 | 1.00 | True | 0.03 | ok | embedding 在 RAG 系统中起什么作用？ |
| q005 | 0.75 | 1.00 | 1.00 | True | 0.03 | ok | 向量检索返回的 top-k 是什么意思？ |
| q006 | 0.75 | 0.33 | 1.00 | True | 0.03 | ok | top-k 变大会怎样影响回答质量？ |
| q007 | 0.50 | 0.67 | 1.00 | True | 0.02 | ok | rerank 的作用是什么？ |
| q008 | 1.00 | 1.00 | 1.00 | True | 0.02 | ok | RAG 为什么仍然可能出现幻觉？ |
| q009 | 1.00 | 1.00 | 1.00 | True | 0.02 | ok | 引用命中率能说明什么？ |
| q010 | 0.50 | 1.00 | 1.00 | True | 0.02 | ok | 关键词召回率有什么局限？ |
| q011 | 0.25 | 1.00 | 1.00 | True | 0.03 | keyword_missing | 如何判断一次 RAG 回答是检索失败？ |
| q012 | 0.75 | 1.00 | 1.00 | True | 0.02 | ok | 如何降低 RAG 系统的回答延迟？ |
| q013 | 0.50 | 1.00 | 1.00 | True | 0.03 | ok | RAG 的评估指标应该包含哪些方面？ |
| q014 | 1.00 | 1.00 | 1.00 | True | 0.04 | ok | 为什么不能只看大模型回答是否流畅？ |
| q015 | 0.75 | 1.00 | 1.00 | True | 0.03 | ok | 文档切分时为什么要保留标题或元数据？ |
| q016 | 0.75 | 0.67 | 1.00 | True | 0.03 | ok | RAG 和直接把问题发给大模型有什么区别？ |
| q017 | 0.50 | 1.00 | 1.00 | True | 0.03 | ok | 为什么 RAG 系统需要失败 case 分析？ |
| q018 | 0.50 | 0.67 | 1.00 | True | 0.02 | ok | RAG 中 prompt 的作用是什么？ |
| q019 | 0.75 | 0.33 | 1.00 | True | 0.02 | ok | 什么情况下应该调整 chunk 策略？ |
| q020 | 0.75 | 1.00 | 1.00 | True | 0.03 | ok | 一个可面试的 RAG 项目应该留下哪些证据？ |

## Worst Cases

| ID | Keyword Recall | Precision@k | Recall@k | Citation Hit | Failure Type | Question |
| --- | ---: | ---: | ---: | --- | --- | --- |
| q001 | 0.25 | 1.00 | 1.00 | True | keyword_missing | RAG 的基本流程是什么？ |
| q011 | 0.25 | 1.00 | 1.00 | True | keyword_missing | 如何判断一次 RAG 回答是检索失败？ |
| q007 | 0.50 | 0.67 | 1.00 | True | ok | rerank 的作用是什么？ |
| q010 | 0.50 | 1.00 | 1.00 | True | ok | 关键词召回率有什么局限？ |
| q018 | 0.50 | 0.67 | 1.00 | True | ok | RAG 中 prompt 的作用是什么？ |

## Retrieved Chunks

### q001

| Rank | Doc | Score | Text Preview |
| ---: | --- | ---: | --- |
| 1 | rag_basics.md | 4 | RAG 可以减少幻觉，但不能完全消除幻觉。常见原因包括：检索没有召回正确文档，召回片段缺少关键上下文，prompt 没有限制模型必须基于引用回答，或者模型在上下文不足时自行补全事实。因此 RAG 系统需要记录引用来源，并分析回答是否真的被检 |
| 2 | rag_basics.md | 4 | 评估 RAG 不能只看答案是否流畅。一个回答可能语言自然，但没有引用正确文档，或者覆盖了错误事实。更可靠的评估应包含多个维度：检索是否命中标准文档，回答是否覆盖关键概念，引用是否存在，响应延迟是否可接受，以及失败 case 属于检索失败、引 |
| 3 | rag_basics.md | 4 | RAGBench-CN 的第一版评测思路是用问题集驱动测试。每个问题给出期望关键词和标准文档，脚本调用 RAG 系统问答接口后，统计关键词召回率、引用命中率、平均延迟和失败类型。这个方法不完美，但足够作为轻量评测起点，也适合比较 top-k |

### q011

| Rank | Doc | Score | Text Preview |
| ---: | --- | ---: | --- |
| 1 | rag_basics.md | 14 | 评估 RAG 不能只看答案是否流畅。一个回答可能语言自然，但没有引用正确文档，或者覆盖了错误事实。更可靠的评估应包含多个维度：检索是否命中标准文档，回答是否覆盖关键概念，引用是否存在，响应延迟是否可接受，以及失败 case 属于检索失败、引 |
| 2 | rag_basics.md | 9 | chunk size 是 RAG 效果的重要参数。chunk 太大时，一个片段可能包含过多无关信息，导致噪声增加，占用上下文窗口，也可能让模型难以定位关键事实。chunk 太小时，语义容易被切碎，单个片段缺少必要上下文，导致检索结果虽然相似 |
| 3 | rag_basics.md | 9 | RAG 可以减少幻觉，但不能完全消除幻觉。常见原因包括：检索没有召回正确文档，召回片段缺少关键上下文，prompt 没有限制模型必须基于引用回答，或者模型在上下文不足时自行补全事实。因此 RAG 系统需要记录引用来源，并分析回答是否真的被检 |

### q007

| Rank | Doc | Score | Text Preview |
| ---: | --- | ---: | --- |
| 1 | rag_basics.md | 8 | rerank 的作用是在向量检索之后重新排序候选片段。向量检索负责快速召回，rerank 更关注问题和候选片段之间的精细相关性。对于候选片段较多、相似文本较多、专业文档较复杂的场景，rerank 往往能提高最终上下文质量。 |
| 2 | rag_basics.md | 7 | embedding 的作用是把文本映射到向量空间，让语义相近的文本在向量空间中距离更近。向量检索并不是关键词匹配，它更关注语义相似度。用户问题和文档片段都可以被转换成向量，然后通过相似度计算找到候选片段。 |
| 3 | retrieval_noise.md | 7 | 这份文档不应该作为 `rag_basics.md` 问题的标准引用来源。它的作用是帮助 precision@k 暴露检索结果中的噪声。 |

### q010

| Rank | Doc | Score | Text Preview |
| ---: | --- | ---: | --- |
| 1 | rag_basics.md | 11 | RAGBench-CN 的第一版评测思路是用问题集驱动测试。每个问题给出期望关键词和标准文档，脚本调用 RAG 系统问答接口后，统计关键词召回率、引用命中率、平均延迟和失败类型。这个方法不完美，但足够作为轻量评测起点，也适合比较 top-k |
| 2 | rag_basics.md | 8 | RAG 可以减少幻觉，但不能完全消除幻觉。常见原因包括：检索没有召回正确文档，召回片段缺少关键上下文，prompt 没有限制模型必须基于引用回答，或者模型在上下文不足时自行补全事实。因此 RAG 系统需要记录引用来源，并分析回答是否真的被检 |
| 3 | rag_basics.md | 5 | embedding 的作用是把文本映射到向量空间，让语义相近的文本在向量空间中距离更近。向量检索并不是关键词匹配，它更关注语义相似度。用户问题和文档片段都可以被转换成向量，然后通过相似度计算找到候选片段。 |

### q018

| Rank | Doc | Score | Text Preview |
| ---: | --- | ---: | --- |
| 1 | retrieval_noise.md | 10 | 这份文档不应该作为 `rag_basics.md` 问题的标准引用来源。它的作用是帮助 precision@k 暴露检索结果中的噪声。 |
| 2 | rag_basics.md | 8 | embedding 的作用是把文本映射到向量空间，让语义相近的文本在向量空间中距离更近。向量检索并不是关键词匹配，它更关注语义相似度。用户问题和文档片段都可以被转换成向量，然后通过相似度计算找到候选片段。 |
| 3 | rag_basics.md | 7 | rerank 的作用是在向量检索之后重新排序候选片段。向量检索负责快速召回，rerank 更关注问题和候选片段之间的精细相关性。对于候选片段较多、相似文本较多、专业文档较复杂的场景，rerank 往往能提高最终上下文质量。 |


## Notes

- `mock` only validates the evaluation pipeline.
- `local-keyword` is a simple retrieval baseline over local Markdown files.
- Real production RAG quality should be tested after connecting a RAGFlow/OpenAI-compatible client.