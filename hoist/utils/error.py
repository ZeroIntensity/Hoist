

class Error:
    """Class for representing a custom server error."""
    def __init__(self, message: str, code: int = 500) -> None:
        """Class for representing a custom server error."""
        self._message = message
        self._code = code
    
    @property
    def message(self) -> str:
        """Error message that server responded with."""
        return self._message
    
    @property
    def code(self) -> int:
        """Error code that server responded with."""
        return self._code
    
    def __repr__(self) -> str:
        return f'Error(message={self.message}, code={self.code}'
    
    def __str__(self) -> str:
        return self._message
    
