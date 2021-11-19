from dataclasses import dataclass
from typing import Dict, Optional

@dataclass
class Message:
    """Class representing a message."""
    content: str
    headers: Dict[str, str]

@dataclass
class MessageBody:
    """Class for representing the FastAPI message body."""
    message: Optional[str] = None
    auth: Optional[str] = None