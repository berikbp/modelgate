#Rules every provider must follow

from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseProvider(ABC):

    @abstractmethod
    def list_models(self) -> list[Dict[str, Any]]:
        """List available models for the provider."""
        pass
    @abstractmethod
    def generate_response(self, model: str, prompt: str) -> str:
        """Generate a response from the specified model given a prompt."""
        pass

    