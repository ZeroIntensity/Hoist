class ServerResponseError(Exception):
    """Exception raised when a server respons with invalid content or an error."""
    pass

class InvalidServerError(Exception):
    """Exception raised when a server does not exist or is not accessible to hoist."""
    pass

class ServerExistsError(Exception):
    """Exception raised when a server already exists."""
    pass

class HoistExistsError(Exception):
    """Raised when trying to init hoist on a server that is already setup."""
    pass

class ServerAuthenticationError(Exception):
    """Raised when authentication key is invalid."""
    pass

class SocketNotSupportedError(Exception):
    """Raised when trying to create a websocket on a non-fastapi server."""
    pass

class InvalidSocketError(Exception):
    """Raised when trying to connect to a non-websocket route or a socket does not exist."""
    pass

class SocketResponseError(Exception):
    """Raised when a socket response is invalid."""