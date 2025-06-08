from llm_knife.models.azure import openai_model  # Import other models as you implement


class LLMManager:
    def __init__(self, model_name: str):
        self.model_name = model_name.lower()
        self.model = self._load_model()

    def _load_model(self):
        if self.model_name.startswith("openai"):
            return openai_model.OpenAIModel()
        # Add more model loaders here
        else:
            raise ValueError(f"Unknown model '{self.model_name}'")

    def generate(self, prompt: str, context: str = None, **kwargs):
        return self.model.generate(prompt, context, **kwargs)

    def ask(self, prompt: str, context: str = None, **kwargs):
        return self.generate(prompt, context, **kwargs)
