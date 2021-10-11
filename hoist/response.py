from dataclasses import dataclass

@dataclass
class Response:
    """Class representing a server response."""
    message: str
    code: int = 200
    failure: bool = False
