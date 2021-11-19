# Welcome to Hoist's Documentation!

Hoist is a library for easily creating and managing HTTP and WebSocket connections.

## Features

- Easy to use with object oriented syntax
- Asynn
- Full typehints with docstrings

## Quick Example

```py
import hoist

server = hoist.create_server('localhost', 5000)
listener = server.create_route('/hello')

@listener.received('hi')
async def hi(message) -> str:
    return 'hi', 500
```
