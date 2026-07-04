# Reports

This directory contains generated example reports.

## Files

| File | Purpose |
| --- | --- |
| `sample_report.md` | Mock client report. Validates the evaluation pipeline. |
| `sample_result.json` | Machine-readable mock result. |
| `local_keyword_report.md` | Local Markdown keyword retrieval baseline report. |
| `local_keyword_result.json` | Machine-readable local baseline result. |
| `top_k_comparison.md` | Comparison report for `top-k=1,3,5`. |
| `top_k_comparison.json` | Machine-readable top-k comparison result. |
| `chunk_size_comparison.md` | Comparison report for `chunk_size=120,300,600`. |
| `chunk_size_comparison.json` | Machine-readable chunk size comparison result. |

## Regenerate

```powershell
ragbench-eval --questions examples/questions_zh.json --out reports/sample_report.md --json-out reports/sample_result.json --mock
ragbench-eval --questions examples/questions_zh.json --out reports/local_keyword_report.md --json-out reports/local_keyword_result.json --client local-keyword --docs-dir examples/docs --top-k 3
ragbench-compare --questions examples/questions_zh.json --docs-dir examples/docs --top-k 1,3,5 --out reports/top_k_comparison.md --json-out reports/top_k_comparison.json
ragbench-compare --mode chunk-size --questions examples/questions_zh.json --docs-dir examples/docs --top-k 3 --chunk-size 120,300,600 --out reports/chunk_size_comparison.md --json-out reports/chunk_size_comparison.json
```

