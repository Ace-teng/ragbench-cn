from __future__ import annotations

from html import escape


def _style() -> str:
    return """
body {
  color: #172033;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  line-height: 1.5;
  margin: 0;
  background: #f6f7f9;
}
main {
  max-width: 1120px;
  margin: 0 auto;
  padding: 32px 20px 56px;
}
h1, h2, h3 {
  line-height: 1.2;
}
.summary {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 12px;
  margin: 24px 0;
}
.metric, section {
  background: #fff;
  border: 1px solid #dfe3ea;
  border-radius: 8px;
}
.metric {
  padding: 16px;
}
.metric span {
  color: #5f6b7a;
  display: block;
  font-size: 13px;
}
.metric strong {
  display: block;
  font-size: 28px;
  margin-top: 6px;
}
section {
  margin-top: 20px;
  overflow-x: auto;
  padding: 18px;
}
table {
  border-collapse: collapse;
  min-width: 760px;
  width: 100%;
}
th, td {
  border-bottom: 1px solid #e6e9ef;
  padding: 10px 12px;
  text-align: left;
  vertical-align: top;
}
th {
  color: #4c5968;
  font-size: 13px;
}
.num {
  text-align: right;
}
.ok {
  color: #137333;
  font-weight: 600;
}
.bad {
  color: #b3261e;
  font-weight: 600;
}
""".strip()


def _page(title: str, body: str) -> str:
    safe_title = escape(title)
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{safe_title}</title>
  <style>{_style()}</style>
</head>
<body>
  <main>
{body}
  </main>
</body>
</html>
"""


def _failure_counts_text(summary: dict) -> str:
    counts = summary.get("failure_counts", {})
    if not counts:
        return "-"
    return ", ".join(f"{escape(str(key))}={value}" for key, value in sorted(counts.items()))


def render_eval_html(rows: list[dict], summary: dict, client_name: str) -> str:
    detail_rows = []
    for row in rows:
        citation_class = "ok" if row["citation_hit"] else "bad"
        precision = (
            f"{row['retrieval_precision_at_k']:.2f}"
            if row.get("retrieval_precision_at_k") is not None
            else "N/A"
        )
        recall = (
            f"{row['retrieval_recall_at_k']:.2f}"
            if row.get("retrieval_recall_at_k") is not None
            else "N/A"
        )
        detail_rows.append(
            "<tr>"
            f"<td>{escape(str(row['id']))}</td>"
            f"<td class=\"num\">{row['keyword_recall']:.2f}</td>"
            f"<td class=\"num\">{precision}</td>"
            f"<td class=\"num\">{recall}</td>"
            f"<td class=\"{citation_class}\">{row['citation_hit']}</td>"
            f"<td class=\"num\">{row['latency_ms']:.2f}</td>"
            f"<td>{escape(str(row['failure_type']))}</td>"
            f"<td>{escape(str(row.get('diagnosis', '')))}</td>"
            f"<td>{escape(str(row['question']))}</td>"
            "</tr>"
        )

    failure_rows = []
    for failure_type, count in sorted(summary["failure_counts"].items()):
        failure_rows.append(f"<tr><td>{escape(str(failure_type))}</td><td class=\"num\">{count}</td></tr>")

    average_precision = (
        f"{summary['average_retrieval_precision_at_k']:.2f}"
        if summary["average_retrieval_precision_at_k"] is not None
        else "N/A"
    )
    average_recall = (
        f"{summary['average_retrieval_recall_at_k']:.2f}"
        if summary["average_retrieval_recall_at_k"] is not None
        else "N/A"
    )
    body = f"""
    <h1>RAGBench-CN Evaluation Report</h1>
    <p>Client: <strong>{escape(client_name)}</strong></p>
    <div class="summary">
      <div class="metric"><span>Questions</span><strong>{summary['questions']}</strong></div>
      <div class="metric"><span>Citation Hit Rate</span><strong>{summary['citation_hit_rate']:.2f}</strong></div>
      <div class="metric"><span>Avg Keyword Recall</span><strong>{summary['average_keyword_recall']:.2f}</strong></div>
      <div class="metric"><span>Avg Precision@k</span><strong>{average_precision}</strong></div>
      <div class="metric"><span>Avg Recall@k</span><strong>{average_recall}</strong></div>
      <div class="metric"><span>Avg Latency</span><strong>{summary['average_latency_ms']:.2f} ms</strong></div>
    </div>
    <section>
      <h2>Failure Types</h2>
      <table>
        <thead><tr><th>Type</th><th class="num">Count</th></tr></thead>
        <tbody>{''.join(failure_rows)}</tbody>
      </table>
    </section>
    <section>
      <h2>Details</h2>
      <table>
        <thead>
          <tr><th>ID</th><th class="num">Keyword Recall</th><th class="num">Precision@k</th><th class="num">Recall@k</th><th>Citation Hit</th><th class="num">Latency ms</th><th>Failure Type</th><th>Diagnosis</th><th>Question</th></tr>
        </thead>
        <tbody>{''.join(detail_rows)}</tbody>
      </table>
    </section>
"""
    return _page("RAGBench-CN Evaluation Report", body)


def render_comparison_html(runs: list[dict], title: str, notes: list[str]) -> str:
    run_rows = []
    worst_case_sections = []
    for run in runs:
        summary = run["summary"]
        precision = (
            f"{summary['average_retrieval_precision_at_k']:.2f}"
            if summary.get("average_retrieval_precision_at_k") is not None
            else "N/A"
        )
        recall = (
            f"{summary['average_retrieval_recall_at_k']:.2f}"
            if summary.get("average_retrieval_recall_at_k") is not None
            else "N/A"
        )
        run_rows.append(
            "<tr>"
            f"<td>{escape(str(run['name']))}</td>"
            f"<td class=\"num\">{summary['citation_hit_rate']:.2f}</td>"
            f"<td class=\"num\">{summary['average_keyword_recall']:.2f}</td>"
            f"<td class=\"num\">{precision}</td>"
            f"<td class=\"num\">{recall}</td>"
            f"<td class=\"num\">{summary['average_latency_ms']:.2f}</td>"
            f"<td>{_failure_counts_text(summary)}</td>"
            "</tr>"
        )
        worst_rows = []
        for row in run.get("worst_cases", []):
            precision = (
                f"{row['retrieval_precision_at_k']:.2f}"
                if row.get("retrieval_precision_at_k") is not None
                else "N/A"
            )
            recall = (
                f"{row['retrieval_recall_at_k']:.2f}"
                if row.get("retrieval_recall_at_k") is not None
                else "N/A"
            )
            citation_class = "ok" if row.get("citation_hit") else "bad"
            worst_rows.append(
                "<tr>"
                f"<td>{escape(str(row['id']))}</td>"
                f"<td class=\"num\">{row['keyword_recall']:.2f}</td>"
                f"<td class=\"num\">{precision}</td>"
                f"<td class=\"num\">{recall}</td>"
                f"<td class=\"{citation_class}\">{row.get('citation_hit')}</td>"
                f"<td>{escape(str(row.get('failure_type', '')))}</td>"
                f"<td>{escape(str(row.get('diagnosis', '')))}</td>"
                f"<td>{escape(str(row.get('question', '')))}</td>"
                "</tr>"
            )
        worst_case_sections.append(
            f"""
      <h3>{escape(str(run['name']))}</h3>
      <table>
        <thead>
          <tr><th>ID</th><th class="num">Keyword Recall</th><th class="num">Precision@k</th><th class="num">Recall@k</th><th>Citation Hit</th><th>Failure Type</th><th>Diagnosis</th><th>Question</th></tr>
        </thead>
        <tbody>{''.join(worst_rows)}</tbody>
      </table>
"""
        )

    note_items = "".join(f"<li>{escape(note)}</li>" for note in notes)
    body = f"""
    <h1>{escape(title)}</h1>
    <section>
      <h2>Summary</h2>
      <table>
        <thead>
          <tr><th>Run</th><th class="num">Citation Hit Rate</th><th class="num">Avg Keyword Recall</th><th class="num">Avg Precision@k</th><th class="num">Avg Recall@k</th><th class="num">Avg Latency ms</th><th>Failure Counts</th></tr>
        </thead>
        <tbody>{''.join(run_rows)}</tbody>
      </table>
    </section>
    <section>
      <h2>Experiment Notes</h2>
      <ul>{note_items}</ul>
    </section>
    <section>
      <h2>Worst Cases By Run</h2>
      {''.join(worst_case_sections)}
    </section>
"""
    return _page(title, body)
