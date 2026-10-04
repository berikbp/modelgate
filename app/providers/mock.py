# Current fake implementation

from app.providers.base import BaseProvider

class MockProvider(BaseProvider):
    
    MODELS = [
        {"name": "Claude", "version": "latest"},
        {"name": "GPT-4", "version": "latest"},
        {"name": "LLaMA", "version": "latest"},
        {"name": "Mistral", "version": "latest"},
        {"name": "Falcon", "version": "latest"},
    ]

    def list_models(self) -> list[dict]:
        """List available models for the provider."""
        return self.MODELS

    def generate_response(self, model: str, prompt: str) -> str:
        """Generate a response from the specified model given a prompt."""
        if model not in [m['name'] for m in self.MODELS]:
            raise ValueError(f"Model {model} doesn't exist")
        return f"Response from {model} for prompt: {prompt}"