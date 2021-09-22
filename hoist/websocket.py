from fastapi import FastAPI
from typing import Union, Callable, Tuple, List, Dict
from .error import Error

class Socket:
    """Class representing a websocket."""
    def __init__(self, app: FastAPI, route: str, handle_errors: bool = True, force_catch_all: bool = False) -> None:
        """Class representing a websocket."""
        self._app = app
        self._route = route
        self._for_receive: Dict[str, Callable] = {}
        self._on_receive: Union[Callable, bool] = False
        self._handle_errors: bool = handle_errors
        self._force_catch_all: bool = force_catch_all
        self._disconnect: List[Callable] = []
        self._connect: List[Callable] = []
    
    @property
    def app(self) -> FastAPI:
        """Application socket is defined under."""
        return self._app
    
    @property
    def route(self) -> str:
        """Route of the websocket."""
        return self._route

    @property
    def for_receive(self) -> Dict[str, Callable]:
        """Functions to be called when a specified message is received."""
        return self._for_receive

    @property
    def on_receive(self) -> Dict[str, Callable]:
        """Function to be called when a message is received."""
        return self._on_receive
    
    @property
    def handle_errors(self) -> bool:
        """Whether to handle internal errors."""
        return self._handle_errors
    
    @property
    def force_catch_all(self) -> bool:
        """Whether to always run the catch all function when a message is received."""
        return self._force_catch_all
    
    @property
    def connect(self) -> List[Callable]:
        """List of functions to be called when a connection is established."""
        return self._connect
    
    @property
    def disconnect(self) -> List[Callable]:
        """List of functions to be called when a connection is ended."""
        return self._disconnect

    def _received(self, message: str) -> Tuple[str, bool]:
        """Function called when the app receives a message."""
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
        if (not resp) or (self._force_catch_all == True):
            try:
                if self._force_catch_all and self._on_receive:
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
    
    def disconnected(self) -> None:
        """Decorator that adds a function to be called when a connection to the socket is established."""
        def decorator(func: Callable):
            self._connect.append(func)
        return decorator
    
    def connected(self) -> None:
        """Decorator that adds a function to be called when a connection to the socket ends."""
        def decorator(func: Callable):
            self._disconnect.append(func)
        return decorator
    