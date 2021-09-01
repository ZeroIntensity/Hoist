from flask import Flask
from typing import Callable, Union, Tuple, Any
from .error import Error
from .errors import ServerResponseError

class Server:
    """Class for an internal hoist server."""
    def __init__(self, app: Flask, handle_errors: bool = True, force_catch_all: bool = False) -> None:
        """Class for an internal hoist server."""
        self._app: Flask = app
        self._received_messages: list = []
        self._for_receive: dict = {}
        self._on_receive: Union[Callable, bool] = False
        self._handle_errors = handle_errors
        self._block_requests: bool = False
        self._force_catch_all: bool = force_catch_all
        self._auto_return: dict = {}

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

    def remove_handler(self, handler_message: str = None) -> None:
        """Function to remove a registered callback."""
        if handler_message:
            del self._for_receive[handler_message]
        else:
            self._on_receive = None

    def remove_auto_return(self, key: Any = None) -> None:
        """Removes an auto return key."""
        if not key:
            self._auto_return = {}
        else:
            del self._auto_return[key]

    def add_auto_return(self, data: dict) -> None:
        """Adds an auto return dictionary."""
        for i in data:
            self._auto_return[i] = data[i]

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
            return Error('Server has blocked requests.', 403), False 

        self._received_messages += message
        resp: Union[str, bool] = False
        success: bool = True
        if message in self._auto_return:
            resp = self._auto_return[message]
        else:
            for i in self._for_receive:

                if i == message:
                    try:
                        resp = self._for_receive[i](message)
                    except Exception as error:
                        resp = 'Server encountered an internal error.'
                        success = False

                        if not self._handle_errors:
                            raise error
        if (not resp) or (self._force_catch_all == True):
            try:
                if self._force_catch_all:
                    self._on_receive(message)
                else:
                    if self._on_receive:
                        resp = self._on_receive(message)
            except Exception as error:
                resp = 'Server encountered an internal error.'
                success = False
        
                if not self._handle_errors:
                    raise error
        if not resp:
            resp = Error('No server response.', 404)

        if isinstance(resp, Error):
            return resp, False


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
    
    def add_handler(self, func: Callable, message: Union[str, bool] = None) -> None:
        """Function for adding a handler without using a decorator."""
        self.received(message)(func)
    

        

