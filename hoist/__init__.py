"""
# Hoist
## WebSocket and HTTP Library
Hoist is a library for easily creating and managing HTTP and WebSocket connections.

### Quick Example

```py
import hoist

server = hoist.create_server('localhost', 5000, log_level="error")
listener = server.create_route('/hello')

@listener.received('hi')
async def hi(message) -> str:
    return 'hi', 500
```

"""

from .response import Response
from .route import Route
from .message import Message, MessageBody
from .create_server import create_server