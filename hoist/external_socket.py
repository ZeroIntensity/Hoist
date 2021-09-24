import asyncio
import websockets
from types import coroutine as Coroutine
from .socket_connection import SocketConnection


class ExternalSocket:
    """Class representing a websocket connection."""
    def __init__(self, url: str, route: str) -> None:
        """Class representing a websocket connection."""
        self._url = url
        self._route = route
        self._full_url = url + route
    
    @property
    def base_url(self) -> str:
        """Base URL of the server."""
        return self._url

    @property
    def url(self) -> str:
        """URL of the websocket."""
        return self._full_url
    
    @property
    def route(self) -> str:
        """Route of the websocket."""
        return self._route

    async def socket_connect(self, coro: Coroutine, json: bool = False, handle_errors: bool = False) -> str:
        """Internal method to connect to the socket."""
        async with websockets.connect(self.url) as websocket:
            socket = SocketConnection(websocket, json, handle_errors)
            await coro(socket)
            
    def connect(self, json: bool = False, handle_errors: bool = False) -> None:
        """Decorator for connecting to the socket."""
        def decorator(coro: Coroutine):
            asyncio.run(self.socket_connect(coro, json, handle_errors))
        return decorator
    
    