# HTML Report

## Purpose

HTML reports make evaluation results easier to browse, demo, and screenshot.

Markdown reports are good for GitHub diffs. JSON reports are good for scripts. HTML reports are good for visual inspection.

## Usage

```powershell
ragbench-eval --questions examples/questions_zh.json --out reports/local_keyword_report.md --json-out reports/local_keyword_result.json --html-out reports/local_keyword_report.html --client local-keyword --docs-dir examples/docs --top-k 3
```

```powershell
ragbench-compare --questions examples/questions_zh.json --docs-dir examples/docs --top-k 1,3,5 --out reports/top_k_comparison.md --json-out reports/top_k_comparison.json --html-out reports/top_k_comparison.html
```

## Implementation

The HTML renderer lives in `ragbench/html_report.py`.

It uses the Python standard library only:

- `html.escape` escapes user-controlled text.
- Inline CSS keeps the generated file self-contained.
- The CLI writes HTML only when `--html-out` is provided.

## Interview Notes

This feature shows separation of concerns:

- Evaluation logic computes rows and summary.
- Markdown renderer formats developer-readable output.
- JSON writer produces machine-readable output.
- HTML renderer produces browser-friendly output.

The important security detail is escaping text before putting it into HTML. Question text, run names, failure types, and notes can contain special characters, so they should not be inserted as raw HTML.
