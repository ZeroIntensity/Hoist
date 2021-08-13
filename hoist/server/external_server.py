import requests
from ..errors import ServerResponseError, ServerAuthenticationError
from typing import Union
from ..utils.error import Error

class ExternalServer:
    """Class for representing a hoist server."""
    def __init__(self, ip: str, port: int, protocol: str = 'http'):
        """Class for representing a hoist server."""
        self.__ip: str = ip
        self.__port: int = port
        self.__protocol: str = protocol
        self.__url: str = f'{protocol}://{ip}:{port}'
        self.__base: str = self.__url + '/hoist/send'

    @property
    def protocol(self) -> str:
        """Protocol of the server."""
        return self.__protocol

    @property
    def ip(self) -> str:
        """IP address of the server."""
        return self.__ip
    
    @property
    def port(self) -> int:
        """Port of the server."""
        return self.__port

    @property
    def url(self) -> str:
        """URL of the server."""
        return self.__url
    
    @property
    def base(self) -> str:
        """Base link for sending to the server."""
        return self.__base
    
    def send(self, message: str, key: str = "", raise_if_unauthorized: bool = True, raise_if_error: bool = True, return_error_object: bool = True, raw_response: bool = False) -> Union[str, Error]:
        """Send a message to the server."""
        
        resp = requests.post(self.__base, params = {'msg': message, "auth": key})
        try:
            json: dict = resp.json()
        except:
            raise ServerResponseError("the server did not respond, most likely due to an unhandled internal exception.")


        if not resp.status_code == 200:
    
            if raise_if_unauthorized and resp.status_code == 401:
                raise ServerAuthenticationError('invalid authentication key.')

            if not raise_if_error:
                if raw_response:
                    if return_error_object:
                        return Error(json, resp.status_code)
                    return json
                else:
                    if return_error_object:
                        return Error(json['ERROR'], resp.status_code)
                    return json['ERROR']
            else:
                raise ServerResponseError(f'the server responded with error "{json["ERROR"]}".')

        if raw_response:
            return json
        


    def check(self) -> bool:
        """Check if a server is online."""
        try:
            requests.get(self.__base)
        except:
            return False
        
        return True