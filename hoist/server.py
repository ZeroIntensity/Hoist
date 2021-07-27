from flask import Flask, request
from typing import Callable, Union

class HoistServer:
    def __init__(self, app: Flask) -> None:
        self._app: Flask = app
        self._received_messages: list = [] # List of messages sent to the server
        self._for_receive: dict = {} # Dictionary of functions to be run when a certain message is received
        self._on_receive: set = set() # Set of functions to be run when a message is received.

    @property
    def received_messages(self) -> list:
        """Property for all received messages."""
        return self._received_messages
    

    def _received(self, message: str) -> str:
        """Function called when the flask app receives a message."""
        self._received_messages += message
        resp = None

        for i in self._for_receive:
            if i == message:
                resp = self._for_receive[i](message)
        
        for i in self._on_receive:
            if not resp:
                resp = i(message)
        
        return str(resp)
    
    def received(self, message: Union[str, bool] = None) -> None:
        """Decorator that adds a function to be called"""
        def decorator(func: Callable):
            if not message:
                self._on_receive.add(func)
            else:
                self._for_receive[message] = func
            return None
        return decorator

        

