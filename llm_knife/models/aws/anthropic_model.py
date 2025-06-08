import json
import os
from typing import Any, Dict, Optional

import boto3
from botocore.exceptions import ClientError

from llm_knife.config.settings import config
from llm_knife.models.base import BaseLLM


class AnthropicModel(BaseLLM):
    """Implementation of Anthropic models through AWS Bedrock."""

    def __init__(self, model_id: Optional[str] = None):
        """
        Initialize the Anthropic model through AWS Bedrock.

        :param model_id: Optional model ID override (defaults to config value)
        """
        self.model_id = model_id or config.get("aws.bedrock.anthropic.model_id")
        self.bedrock = boto3.client(
            service_name="bedrock-runtime", region_name=config.get("aws.region")
        )

    def generate(self, prompt: str, context: str = None, **kwargs) -> str:
        """
        Generate text using the Anthropic model through AWS Bedrock.

        :param prompt: Input prompt to generate from
        :param context: Optional system or contextual information
        :param kwargs: Additional parameters for the model
        :return: Generated text as a string
        """
        try:
            # Get default parameters from config
            max_tokens = kwargs.get(
                "max_tokens", config.get("aws.bedrock.anthropic.max_tokens")
            )
            temperature = kwargs.get(
                "temperature", config.get("aws.bedrock.anthropic.temperature")
            )

            # Prepare the request body
            request_body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": max_tokens,
                "temperature": temperature,
                "messages": [{"role": "user", "content": prompt}],
            }

            # Add system message if context is provided
            if context:
                request_body["messages"].insert(
                    0, {"role": "system", "content": context}
                )

            # Make the API call
            response = self.bedrock.invoke_model(
                modelId=self.model_id, body=json.dumps(request_body)
            )

            # Parse the response
            response_body = json.loads(response["body"].read())
            return response_body["content"][0]["text"]

        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            error_message = e.response["Error"]["Message"]
            raise Exception(f"AWS Bedrock API error ({error_code}): {error_message}")
        except Exception as e:
            raise Exception(f"Error generating text: {str(e)}")
