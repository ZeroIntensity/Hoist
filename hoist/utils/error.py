class Error:
    """Class for representing a custom server error."""
    def __init__(self, message: str, code: int = 500) -> None:
        """Class for representing a custom server error."""
        self._message = message
        self._code = code
    