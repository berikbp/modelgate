from app.providers.base import BaseProvider

class ProviderRegistry:
    def __init__(self):
        self.providers: dict[str, BaseProvider] = {}

    def register(self, name: str, provider: BaseProvider):
        """Register a new provider."""
        self.providers[name] = provider

    def list_models(self) -> list[dict]:
        models = []

        for provider_name, provider in self.providers.items():
            for model in provider.list_models():
                models.append(
                    {
                        **model,
                        'provider': provider_name
                    }
                )

        return models

    def get_provider_for_model(self, model_name: str) -> BaseProvider:
        for provider in self.providers.values():
            model_names = [
                model["name"]
                for model in provider.list_models()
            ]

            if model_name in model_names:
                return provider

        raise ValueError(f"Model {model_name} doesn't exist")

    def generate_response(self, model: str, prompt: str) -> str:
        provider = self.get_provider_for_model(model)

        return provider.generate_response(model, prompt)

    