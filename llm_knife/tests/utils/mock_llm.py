import json
from pathlib import Path
from typing import Any, Dict, Optional, Union

import boto3
import responses
from moto import mock_bedrock


class MockLLMResponses:
    """Utility class for mocking LLM API responses."""

    @staticmethod
    def mock_azure_openai(
        response_text: str, status: int = 200, headers: Optional[Dict[str, str]] = None
    ):
        """
        Mock Azure OpenAI API response.

        :param response_text: The text response to return
        :param status: HTTP status code
        :param headers: Optional response headers
        """

        def request_callback(request):
            # Parse the request body
            body = json.loads(request.body)

            # Create response payload
            response_payload = {
                "id": "mock-response-id",
                "object": "chat.completion",
                "created": 1677858242,
                "model": body.get("model", "gpt-4"),
                "choices": [
                    {
                        "message": {"role": "assistant", "content": response_text},
                        "finish_reason": "stop",
                        "index": 0,
                    }
                ],
                "usage": {
                    "prompt_tokens": 10,
                    "completion_tokens": len(response_text.split()),
                    "total_tokens": 10 + len(response_text.split()),
                },
            }

            return (status, headers or {}, json.dumps(response_payload))

        # Add the mock response
        responses.add_callback(
            responses.POST,
            "https://api.openai.com/v1/chat/completions",
            callback=request_callback,
            content_type="application/json",
        )

    @staticmethod
    def mock_aws_anthropic(
        response_text: str, model_id: str = "anthropic.claude-3-sonnet-20240229-v1:0"
    ):
        """
        Mock AWS Bedrock Anthropic API response.

        :param response_text: The text response to return
        :param model_id: The model ID to mock
        """

        @mock_bedrock
        def mock_bedrock_response():
            bedrock = boto3.client(
                service_name="bedrock-runtime", region_name="us-east-1"
            )

            # Create mock response
            response_body = {
                "content": [{"type": "text", "text": response_text}],
                "id": "mock-response-id",
                "model": model_id,
                "role": "assistant",
                "stop_reason": "end_turn",
                "stop_sequence": None,
                "usage": {
                    "input_tokens": 10,
                    "output_tokens": len(response_text.split()),
                },
            }

            # Mock the invoke_model response
            bedrock.invoke_model = lambda **kwargs: {
                "body": json.dumps(response_body),
                "contentType": "application/json",
            }

            return bedrock

        return mock_bedrock_response()


class MockLLMData:
    """Utility class for managing mock LLM test data."""

    @staticmethod
    def load_mock_responses(file_path: Union[str, Path]) -> Dict[str, Any]:
        """
        Load mock responses from a JSON file.

        :param file_path: Path to the JSON file containing mock responses
        :return: Dictionary of mock responses
        """
        with open(file_path, "r") as f:
            return json.load(f)

    @staticmethod
    def save_mock_responses(data: Dict[str, Any], file_path: Union[str, Path]):
        """
        Save mock responses to a JSON file.

        :param data: Dictionary of mock responses
        :param file_path: Path to save the JSON file
        """
        with open(file_path, "w") as f:
            json.dump(data, f, indent=2)


# Example usage:
"""
# Mock Azure OpenAI
with responses.RequestsMock() as rsps:
    MockLLMResponses.mock_azure_openai("This is a mock response")
    # Your test code here

# Mock AWS Anthropic
with MockLLMResponses.mock_aws_anthropic("This is a mock response") as bedrock:
    # Your test code here

# Using mock data files
mock_data = MockLLMData.load_mock_responses("tests/data/mock_responses.json")
"""
