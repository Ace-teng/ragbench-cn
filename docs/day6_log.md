# Day 6 Log

## Goal

Start v0.2 by improving report presentation.

## Completed

- Added `ragbench/html_report.py`.
- Added `--html-out` to `ragbench-eval`.
- Added `--html-out` to `ragbench-compare`.
- Generated example HTML reports:
  - `reports/local_keyword_report.html`
  - `reports/top_k_comparison.html`
- Added tests for HTML escaping and comparison report rendering.
- Updated README and report index.

## Learning Notes

HTML report is not a new metric. It is a presentation layer.

The same evaluation result can be exposed in different forms:

- Markdown: easy to read in GitHub.
- JSON: easy for programs to parse.
- HTML: easy to browse, demo, and screenshot.

When generating HTML, raw text should be escaped before rendering. This prevents question text or other user-controlled fields from being interpreted as HTML tags or scripts.
