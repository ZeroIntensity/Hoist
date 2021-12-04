class Response:
    """Class representing a server response."""
    def __init__(self, message: str, code: int = 200, failure: bool = False) -> None:
        """Constructor for the `Response` class.
message: property message
code: property code
failure: property failure
"""
        self._message = message
        self._code = code
        self._failure = failure

    @property
    def message(self) -> str:
        """Message that the server responded with."""
        return self._message
    
    @message.setter
    def message(self, value: str) -> None:
        self._message = value

    @property
    def code(self) -> int:
        """Status code that the server responded with."""
        return self._code
    
    @code.setter
    def code(self, value: int) -> None:
        self._code = value
    
    @property
    def failure(self) -> bool:
        """Whether the server responded with an error."""
        return self._failure
    
    @failure.setter
    def failure(self, value: bool) -> None:
        self._failure = value
    
    def __dict__(self):
        return {
            'message': self.message,
            'code': self.code,
            'failure': self.failure 
        }
    
    def make(self) -> dict:
        """Function for turning the object into the HTTP response."""
        return {
            'message' if not self.failure else 'error': self.message,
            'status': self.code
        }

    
