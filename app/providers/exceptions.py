class ProviderError(Exception):
    """Base class for all provider-related errors."""
    pass

class ProviderUnavailableError(ProviderError):
    """Raised when a provider cannot be reached."""
    pass


class ModelNotFoundError(ProviderError):
    """Raised when a requested model does not exist."""
    pass