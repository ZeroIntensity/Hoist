from flask import Flask
from typing import Callable, Union, Tuple
from ..utils.error import Error
from ..errors import ServerResponseError
class Server:
    """Class for an internal hoist server."""
    def __init__(self, app: Flask, handle_errors: bool = True) -> None:
        """Class for an internal hoist server."""
        self._app: Flask = app
        self._received_messages: list = []
        self._for_receive: dict = {}
        self._on_receive: Union[Callable, bool] = False
        self._handle_errors = handle_errors
        self._block_requests: bool = False

    @property
    def on_receive(self) -> Union[Callable, bool]:
        """Function called when the server receives a message and no function has been registered to be run when that message is received."""
        return self._for_receive

    @property
    def for_receive(self) -> dict:
        """Dictionary of functions to be run when a certain message is received."""
        return self._for_receive        

    @property
    def app(self) -> Flask:
        """Flask instance of server."""
        return self._app

    @property
    def received_messages(self) -> list:
        """All received messages."""
        return self._received_messages

    def clear_received_messages(self) -> None:
        """Clear all received messages."""
        self._received_messages = []

    def remove_callback(self, callback_message: str = None) -> None:
        """Function to remove a registered callback."""
        if callback_message:
            del self._for_receive[callback_message]
        else:
            self._on_receive = None

    def toggle_requests(self) -> bool:
        """Function to toggle requests."""

        if self._block_requests == True:
            self._block_requests = False
        else:
            self._block_requests = True
        
        return self._block_requests

    def _received(self, message: str) -> Tuple[str, bool]:
        """Function called when the flask app receives a message."""
        
        if self._block_requests:
            return Error('Server has blocked requests', 403), False 

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


        if isinstance(resp, Error):
            if self._handle_errors:
                return resp, False
            raise ServerResponseError(f"callback returned an error of {resp._message}")

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
    

        

