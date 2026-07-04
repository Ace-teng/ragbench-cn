import unittest
from unittest.mock import Mock, patch

from ragbench.clients.ragflow import RagFlowClient


class RagFlowClientTest(unittest.TestCase):
    def test_ask_calls_ragflow_openai_endpoint(self) -> None:
        response = Mock()
        response.json.return_value = {
            "choices": [
                {
                    "message": {
                        "content": "RAGFlow answer",
                    }
                }
            ],
            "reference": [
                {
                    "doc_name": "rag_basics.md",
                }
            ],
        }

        with patch("ragbench.clients.ragflow.requests.post", return_value=response) as post:
            client = RagFlowClient(
                base_url="http://localhost:9380",
                api_key="ragflow-key",
                chat_id="chat-123",
                model="model",
            )
            result = client.ask("What is RAG?")

        response.raise_for_status.assert_called_once()
        post.assert_called_once()
        self.assertEqual(
            post.call_args.args[0],
            "http://localhost:9380/api/v1/openai/chat-123/chat/completions",
        )
        self.assertEqual(post.call_args.kwargs["headers"]["Authorization"], "Bearer ragflow-key")
        self.assertEqual(result["answer"], "RAGFlow answer")
        self.assertEqual(result["citations"], ["rag_basics.md"])


if __name__ == "__main__":
    unittest.main()
