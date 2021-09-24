from websockets import WebSocketClientProtocol
from typing import Dict
from .errors import SocketResponseError
import json

class SocketConnection:
    """Class representing a socket connection."""
    def __init__(self, socket: WebSocketClientProtocol, use_json: bool = False, handle_errors: bool = False) -> None:
        """Class representing a socket connection."""
        self._socket = socket
        self._use_json = use_json
        self._handle_errors = handle_errors
    
    @property
    def handle_errors(self) -> bool:
        """Whether to handle server response errors."""
        return self._handle_errors

    @property
    def use_json(self) -> bool:
        """Whether to return the socket response as JSON."""
        return self._use_json

    @property
    def socket(self) -> WebSocketClientProtocol:
        """WebSocket client."""
        return self._socket
    
    async def send(self, message: str) -> Dict[str, str]:
        """Function for sending a message to the socket."""
        socket = self._socket
        await socket.send(message)
        resp = await socket.recv()
        resp = json.loads(resp) # because recv() was returning str

        if 'ERROR' in resp:
            if not self._handle_errors:
                raise SocketResponseError(f'socket responded with error "{resp["ERROR"]}"')

        if self._use_json:
            return resp
        
        if 'ERROR' in resp:
            return resp['ERROR']
        else:
            return resp['RESPONSE']
