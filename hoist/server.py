from flask import Flask, request
from typing import Callable, Union, Tuple

class HoistServer:
    def __init__(self, app: Flask, handle_errors: bool = True) -> None:
        self._app: Flask = app
        self._received_messages: list = [] # List of messages sent to the server
        self._for_receive: dict = {} # Dictionary of functions to be run when a certain message is received
        self._on_receive: Callable = None
        self._handle_errors = handle_errors

    @property
    def received_messages(self) -> list:
        """Property for all received messages."""
        return self._received_messages
    

    def _received(self, message: str) -> Tuple[str, bool]:
        """Function called when the flask app receives a message."""
        self._received_messages += message
        resp: Union[str, bool] = False
        success: bool = True

        for i in self._for_receive:
            if i == message:
                try:
                    resp = self._for_receive[i](message)
                except Exception as error:
                    resp = 'Server encountered an internal error.'
                    success = False

                    if not self._handle_errors:
                        raise error
        
            if not resp:
                try:
                    resp = self._on_receive(message)
                except Exception as error:
                    resp = 'Server encountered an internal error.'
                    success = False
        
                    if not self._handle_errors:
                        raise error
        
        return str(resp), success
    
    def received(self, message: Union[str, bool] = None) -> None:
        """Decorator that adds a function to be called when a message is received."""
        def decorator(func: Callable):
            if not message:
                self._on_receive = func
            else:
                self._for_receive[message] = func
            return None
        return decorator
    

        

