from flask import Flask
from typing import Union
from .errors import ServerResponseError
from .utils.error import Error

class HoistProxy:
    """Class for operating an internal proxy."""
    def __init__(self, app: Flask, handle_errors: bool = True) -> None:
        self._connections: set = set()
        self._app = app
        self._handle_errors = handle_errors
        self._on_connect = None
        self._on_disconnect = None

        raise NotImplemented('Proxys have not yet been implemented to Hoist.')
        

    def _connnect(self, server_address: str) -> None:
        """Function for handling connections to the proxy."""
        self._connections.add(server_address)
        resp: Union[str, bool] = False
        success: bool = True
        
        try:
            resp = self._on_connect(server_address)
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
    
    def _disconnnect(self, server_address: str) -> None:
        """Function for handling disconnections to the proxy."""
        self._connections.remove(server_address)
        resp: Union[str, bool] = False
        success: bool = True
        
        try:
            resp = self._on_disconnect(server_address)
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
