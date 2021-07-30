import requests
from .errors import ServerResponseError

class ExternalServer:
    """Class for representing a hoist server."""
    def __init__(self, ip: str, port: int):
        self.ip: str = ip
        self.port: int = port
        self.url: str = f'http://{ip}:{port}'
        self.base: str = self.url + '/hoist/send'
    
    def send(self, message: str, key: str = "", raise_if_error: bool = True, raw_response: bool = False) -> str:
        """Send a message to the server."""
        
        resp = requests.post(self.base, params = {'msg': message, "auth": key})
        try:
            json: dict = resp.json()
        except:
            raise ServerResponseError("the server did not respond, most likely due to an unhandled internal exception.")

        if not resp.status_code == 200:
            if not raise_if_error:

                if raw_response:
                    return json
                else:
                    print('a')
                    return json['ERROR']
            else:
                raise ServerResponseError(f'the server responded with error "{json["ERROR"]}"')

        if raw_response:
            return json
        


    def check(self) -> bool:
        """Check if a server is online."""
        try:
            requests.get(self.base)
        except:
            return False
        
        return True