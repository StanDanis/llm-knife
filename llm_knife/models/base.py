from abc import ABC, abstractmethod
from typing import Iterator, Union


class BaseLLM(ABC):
    @abstractmethod
    def generate(self, prompt: str, context: str = None, **kwargs) -> str:
        """
        Generate text output from the model.

        :param prompt: Input prompt to generate from.
        :param context: Optional system or contextual information.
        :param kwargs: Additional model-specific parameters.
        :return: Generated text as a string.
        """
        pass

    def ask(self, prompt: str, context: str = None, **kwargs) -> str:
        """
        Alias for generate(), for conversational style.
        """
        return self.generate(prompt, context, **kwargs)
