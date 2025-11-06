class NullDropError(Exception):
    """Base error for NullDrop SDK."""

class AuthenticationError(NullDropError):
    """Raised when authentication fails."""

class NotFoundError(NullDropError):
    """Raised when a resource is not found."""

class APIError(NullDropError):
    """Raised when NullDrop API returns an error."""
    def __init__(self, status_code, message="API Error occurred"):
        self.status_code = status_code
        self.message = message
        super().__init__(f"{message} (Status Code: {status_code})")