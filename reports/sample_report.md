# RAGBench-CN Sample Report

## Summary

- Client: mock
- Questions: 20
- Citation hit rate: 1.00
- Average keyword recall: 0.47
- Average latency: 0.00 ms

## Failure Types

| Type | Count |
| --- | ---: |
| keyword_missing | 8 |
| ok | 12 |

## Details

| ID | Keyword Recall | Citation Hit | Latency ms | Failure Type | Question |
| --- | ---: | --- | ---: | --- | --- |
| q001 | 0.75 | True | 0.00 | ok | RAG 的基本流程是什么？ |
| q002 | 0.75 | True | 0.00 | ok | RAG 中 chunk size 过大会带来什么问题？ |
| q003 | 0.50 | True | 0.00 | ok | chunk size 过小会带来什么问题？ |
| q004 | 0.25 | True | 0.00 | keyword_missing | embedding 在 RAG 系统中起什么作用？ |
| q005 | 0.25 | True | 0.00 | keyword_missing | 向量检索返回的 top-k 是什么意思？ |
| q006 | 1.00 | True | 0.00 | ok | top-k 变大会怎样影响回答质量？ |
| q007 | 0.00 | True | 0.00 | keyword_missing | rerank 的作用是什么？ |
| q008 | 0.50 | True | 0.00 | ok | RAG 为什么仍然可能出现幻觉？ |
| q009 | 0.50 | True | 0.00 | ok | 引用命中率能说明什么？ |
| q010 | 0.25 | True | 0.00 | keyword_missing | 关键词召回率有什么局限？ |
| q011 | 0.50 | True | 0.00 | ok | 如何判断一次 RAG 回答是检索失败？ |
| q012 | 0.75 | True | 0.00 | ok | 如何降低 RAG 系统的回答延迟？ |
| q013 | 0.75 | True | 0.00 | ok | RAG 的评估指标应该包含哪些方面？ |
| q014 | 0.00 | True | 0.00 | keyword_missing | 为什么不能只看大模型回答是否流畅？ |
| q015 | 0.25 | True | 0.00 | keyword_missing | 文档切分时为什么要保留标题或元数据？ |
| q016 | 0.50 | True | 0.00 | ok | RAG 和直接把问题发给大模型有什么区别？ |
| q017 | 0.25 | True | 0.00 | keyword_missing | 为什么 RAG 系统需要失败 case 分析？ |
| q018 | 0.75 | True | 0.00 | ok | RAG 中 prompt 的作用是什么？ |
| q019 | 0.75 | True | 0.00 | ok | 什么情况下应该调整 chunk 策略？ |
| q020 | 0.25 | True | 0.00 | keyword_missing | 一个可面试的 RAG 项目应该留下哪些证据？ |

## Worst Cases

| ID | Keyword Recall | Citation Hit | Failure Type | Question |
| --- | ---: | --- | --- | --- |
| q007 | 0.00 | True | keyword_missing | rerank 的作用是什么？ |
| q014 | 0.00 | True | keyword_missing | 为什么不能只看大模型回答是否流畅？ |
| q004 | 0.25 | True | keyword_missing | embedding 在 RAG 系统中起什么作用？ |
| q005 | 0.25 | True | keyword_missing | 向量检索返回的 top-k 是什么意思？ |
| q010 | 0.25 | True | keyword_missing | 关键词召回率有什么局限？ |

## Notes

- `mock` only validates the evaluation pipeline.
- `local-keyword` is a simple retrieval baseline over local Markdown files.
- Real production RAG quality should be tested after connecting a RAGFlow/OpenAI-compatible client.