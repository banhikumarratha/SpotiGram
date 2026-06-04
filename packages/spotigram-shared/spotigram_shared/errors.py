class SpotigramError(Exception):
    """Base exception for all Spotigram errors."""
    pass

class ResourceNotFoundError(SpotigramError):
    """Raised when a resource is not found."""
    pass

class IntegrationError(SpotigramError):
    """Raised when an external integration fails."""
    pass
