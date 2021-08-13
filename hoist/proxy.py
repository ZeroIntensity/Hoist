from flask import Flask
from typing import Union
from .errors import ServerResponseError
from .error import Error

class Proxy:
    """Class for operating an internal proxy."""
    def __init__(self, app: Flask, handle_errors: bool = True) -> None:
        """Class for operating an internal proxy."""
        self._connections: set = set()
        self._app = app
        self._handle_errors = handle_errors
        self._on_connect = None
        self._on_disconnect = None

        raise NotImplementedError('proxys are not yet supported')

    

    def _connnect(self, data: list) -> None:
        """Function for handling connections to the proxy."""

        server_ip, server_port, protocol = data

        self._connections.add([server_ip, server_port, protocol])
        resp: Union[str, bool] = False
        success: bool = True
        
        try:
            resp = self._on_connect(server_ip, server_port, protocol)
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
    
    def _disconnnect(self, data: list) -> None:
        """Function for handling disconnections to the proxy."""

        server_ip, server_port, protocol = data

        self._connections.remove([server_ip, server_port, protocol])
        resp: Union[str, bool] = False
        success: bool = True
        
        try:
            resp = self._on_disconnect(server_ip, server_port, protocol)
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

    def _broadcast(self, message: str) -> None:
        """Function for broadcasting messages to connected servers."""

        for i in self._connections:
            ip, port = i
            
