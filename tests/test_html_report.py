import unittest

from ragbench.html_report import render_comparison_html, render_eval_html


class HtmlReportTest(unittest.TestCase):
    def test_eval_html_escapes_question_text(self) -> None:
        rows = [
            {
                "id": "q001",
                "question": "<script>alert(1)</script>",
                "keyword_recall": 0.5,
                "citation_hit": False,
                "latency_ms": 1.2,
                "failure_type": "keyword_missing",
            }
        ]
        summary = {
            "questions": 1,
            "citation_hit_rate": 0,
            "average_keyword_recall": 0.5,
            "average_latency_ms": 1.2,
            "failure_counts": {"keyword_missing": 1},
        }

        html = render_eval_html(rows, summary, client_name="local-keyword")

        self.assertIn("&lt;script&gt;alert(1)&lt;/script&gt;", html)
        self.assertNotIn("<script>alert(1)</script>", html)

    def test_comparison_html_contains_run_summary(self) -> None:
        runs = [
            {
                "name": "top_k=3",
                "summary": {
                    "citation_hit_rate": 1,
                    "average_keyword_recall": 0.75,
                    "average_latency_ms": 2.3,
                    "failure_counts": {"ok": 2},
                },
            }
        ]

        html = render_comparison_html(runs, title="Top-k Report", notes=["larger top-k returns more chunks"])

        self.assertIn("Top-k Report", html)
        self.assertIn("top_k=3", html)
        self.assertIn("ok=2", html)


if __name__ == "__main__":
    unittest.main()
