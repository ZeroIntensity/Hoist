from fastapi import FastAPI
from typing import Coroutine, Dict, Callable, Union
from .response import Response
from .message import Message

class Route:
    """Class representing a message listener on a route."""
    def __init__(self, server: FastAPI, url: str) -> None:
        """Class representing a message listener on a route."""
        self.__server = server
        self._message_listeners: Dict[Union[str, None], Coroutine] = {}
        self.__url = url
    
    @property
    def url(self) -> str:
        """URL the route is listening on."""
        return self.__url
    
    @property
    def server(self) -> FastAPI:
        """Server that the route is listening on."""
        return self.__server
    
    @property
    def message_listeners(self) -> Dict[Union[str, None], Coroutine]:
        """Dictionary of functions to be called when a message is received."""
        return self._message_listeners
    
    @message_listeners.setter
    def message_listeners(self, key: str, value: Coroutine) -> None:
        self._message_listeners[key] = value
    
    async def got_message(self, message: Message = None) -> str:
        """Internal method for calling a message listener."""
        listener: Callable = self.message_listeners.get(message.content)

        if not listener:
            return Response('Server did not respond.', 502, True)
        else:
            function_resp = await listener(message)
            return Response(*function_resp)
    
    def received(self, message: Union[str, None] = None) -> None:
        """Decorator that adds a function to be called when a message is received."""
        def decorator(coro: Coroutine):
            self.message_listeners[message] = coro
        return decorator
