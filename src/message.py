from typing import Dict, Optional
from dataclasses import dataclass
class Message:
    """Class representing a message."""
    def __init__(self, content: str, headers: Dict[str, str]) -> None:
        """Constructor for the `Message` class.
content: property content
headers: property headers
"""
        self._content = content
        self._headers = headers
    
    @property
    def content(self) -> str:
        """Content of the message."""
        return self._content
    
    
    @property
    def headers(self) -> Dict[str, str]:
        """Headers that came with the message request."""
        return self._headers

@dataclass
class MessageBody:
    """Class for representing the FastAPI message body."""
    message: Optional[str] = None
    auth: Optional[str] = None