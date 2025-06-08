from typing import Iterator

import openai

from llm_knife.models.base import BaseLLM


class OpenAIModel(BaseLLM):
    def __init__(self, model: str = "gpt-4"):
        self.model = model

    def generate(
        self, prompt: str, context: str = None, stream: bool = False, **kwargs
    ) -> Union[str, Iterator[str]]:
        messages = []
        if context:
            messages.append({"role": "system", "content": context})
        messages.append({"role": "user", "content": prompt})

        if not stream:
            response = openai.ChatCompletion.create(
                model=self.model, messages=messages, **kwargs
            )
            return response["choices"][0]["message"]["content"].strip()
        else:
            response = openai.ChatCompletion.create(
                model=self.model, messages=messages, stream=True, **kwargs
            )

            def stream_generator():
                for chunk in response:
                    content = chunk["choices"][0].get("delta", {}).get("content")
                    if content:
                        yield content

            return stream_generator()
