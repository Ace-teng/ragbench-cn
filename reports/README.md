# Reports

This directory contains generated example reports.

The example documents include `retrieval_noise.md`, a similar but non-gold source used to demonstrate how precision@k can reveal retrieval noise.

## Files

| File | Purpose |
| --- | --- |
| `sample_report.md` | Mock client report. Validates the evaluation pipeline. |
| `sample_result.json` | Machine-readable mock result. |
| `local_keyword_report.md` | Local Markdown keyword retrieval baseline report. |
| `local_keyword_result.json` | Machine-readable local baseline result. |
| `local_keyword_report.html` | Browser-friendly local baseline report. |
| `top_k_comparison.md` | Comparison report for `top-k=1,3,5`. |
| `top_k_comparison.json` | Machine-readable top-k comparison result. |
| `top_k_comparison.html` | Browser-friendly top-k comparison report. |
| `chunk_size_comparison.md` | Comparison report for `chunk_size=120,300,600`. |
| `chunk_size_comparison.json` | Machine-readable chunk size comparison result. |
| `client_comparison.md` | Comparison report for retrieval clients. |
| `client_comparison.json` | Machine-readable client comparison result. |
| `client_comparison.html` | Browser-friendly client comparison report. |
| `paraphrase_client_comparison.md` | Keyword vs embedding comparison on paraphrased questions. |
| `paraphrase_client_comparison.json` | Machine-readable paraphrase comparison result. |
| `paraphrase_client_comparison.html` | Browser-friendly paraphrase comparison report. |

## Regenerate

```powershell
ragbench-eval --questions examples/questions_zh.json --out reports/sample_report.md --json-out reports/sample_result.json --mock
ragbench-eval --questions examples/questions_zh.json --out reports/local_keyword_report.md --json-out reports/local_keyword_result.json --html-out reports/local_keyword_report.html --client local-keyword --docs-dir examples/docs --top-k 3
ragbench-compare --questions examples/questions_zh.json --docs-dir examples/docs --top-k 1,3,5 --out reports/top_k_comparison.md --json-out reports/top_k_comparison.json --html-out reports/top_k_comparison.html
ragbench-compare --mode chunk-size --questions examples/questions_zh.json --docs-dir examples/docs --top-k 3 --chunk-size 120,300,600 --out reports/chunk_size_comparison.md --json-out reports/chunk_size_comparison.json
ragbench-compare --mode client --clients local-keyword --questions examples/questions_zh.json --docs-dir examples/docs --top-k 3 --out reports/client_comparison.md --json-out reports/client_comparison.json --html-out reports/client_comparison.html
```

To regenerate the checked-in keyword vs embedding client report, install optional dependencies first:

```powershell
pip install -e .[embedding]
ragbench-compare --mode client --clients local-keyword,local-embedding --questions examples/questions_zh.json --docs-dir examples/docs --top-k 3 --out reports/client_comparison.md --json-out reports/client_comparison.json --html-out reports/client_comparison.html
```

To regenerate the paraphrase experiment:

```powershell
pip install -e .[embedding]
ragbench-compare --mode client --clients local-keyword,local-embedding --questions examples/questions_paraphrase.json --docs-dir examples/docs --top-k 3 --out reports/paraphrase_client_comparison.md --json-out reports/paraphrase_client_comparison.json --html-out reports/paraphrase_client_comparison.html
```
