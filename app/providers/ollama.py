'''
so here initially using httpx.get() and httpx.post() to interact with the Ollama API. 
but the problem is that when we try to access to the Ollama API,
we always recreate the httpx client for each request, which is not efficient and can lead to performance issues.
to fix this use reusable httpx client , which speeds up repeated API calls
via connection pooling and keep-alive connections.
'''
import httpx

from app.providers.base import BaseProvider
from app.providers.exceptions import ProviderError, ProviderUnavailableError, ModelNotFoundError

class OllamaProvider(BaseProvider):
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        self.client = httpx.Client(base_url=self.base_url, timeout=60.0)
        
    def list_models(self) -> list[dict]:
        try:
            response = self.client.get(
                f"{self.base_url}/api/tags",
                timeout=5.0,
            )

            response.raise_for_status()

        except httpx.RequestError as error:
            raise ProviderUnavailableError(
                "Ollama is unavailable"
            ) from error

        except httpx.HTTPStatusError as error:
            raise ProviderUnavailableError(
                f"Ollama returned HTTP {error.response.status_code}"
            ) from error

        data = response.json()

        return [
            {
                "name": model["name"],
                "version": "local",
            }
            for model in data["models"]
        ]

    def generate_response(self, model: str, prompt: str) -> str:
        try:
            response = self.client.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": False,
                },
                timeout=60.0,
            )

            if response.status_code == 404:
                raise ModelNotFoundError(
                    f"Model {model} doesn't exist in Ollama"
                )

            response.raise_for_status()

        except httpx.RequestError as error:
            raise ProviderUnavailableError(
                "Ollama is unavailable"
            ) from error

        except httpx.HTTPStatusError as error:
            raise ProviderUnavailableError(
                f"Ollama returned HTTP {error.response.status_code}"
            ) from error

        data = response.json()

        return data["response"]