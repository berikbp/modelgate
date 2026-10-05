import httpx

from app.providers.base import BaseProvider

class OllamaProvider(BaseProvider):
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url

    def list_models(self) -> list[dict]:
        response = httpx.get(
            f"{self.base_url}/api/tags",
            timeout=5.0,
        )

        response.raise_for_status()

        data = response.json()

        return [
            {
                "name": model["name"],
                "version": "local",
            }
            for model in data["models"]
        ]

    def generate_response(self, model: str, prompt: str) -> str:
        response = httpx.post(
            f'{self.base_url}/api/generate',
            json={
                "model": model,
                "prompt": prompt,
                "stream": False,
            },
            timeout=60.0,
        )

        response.raise_for_status()

        data = response.json()

        return data["response"]

    