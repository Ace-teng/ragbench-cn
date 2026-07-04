import unittest
from unittest.mock import Mock, patch

from ragbench.clients.openai_compatible import OpenAICompatibleClient


class OpenAICompatibleClientTest(unittest.TestCase):
    def test_ask_calls_chat_completions(self) -> None:
        response = Mock()
        response.json.return_value = {
            "choices": [
                {
                    "message": {
                        "content": "RAG uses retrieval and generation.",
                    }
                }
            ],
            "citations": ["rag_basics.md"],
        }

        with patch("ragbench.clients.openai_compatible.requests.post", return_value=response) as post:
            client = OpenAICompatibleClient(
                base_url="http://localhost:8000/v1",
                api_key="test-key",
                model="test-model",
            )
            result = client.ask("What is RAG?")

        response.raise_for_status.assert_called_once()
        post.assert_called_once()
        request_kwargs = post.call_args.kwargs
        self.assertEqual(request_kwargs["headers"]["Authorization"], "Bearer test-key")
        self.assertEqual(request_kwargs["json"]["model"], "test-model")
        self.assertEqual(result["answer"], "RAG uses retrieval and generation.")
        self.assertEqual(result["citations"], ["rag_basics.md"])


if __name__ == "__main__":
    unittest.main()
