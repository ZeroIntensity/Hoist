import requests

class ExternalServer:
    def __init__(self, ip: str, port: int):
        self.ip: str = ip
        self.port: int = port
        self.url: str = f'http://{ip}:{port}'
        self.base: str = self.url + '/hoist/send'
    
    def send(self, message: str) -> str:
        """Send a message to the server."""
        
        resp = requests.get(self.base, params = {'msg': message})
        json: dict = resp.json()

        return json['RESPONSE']

    def check(self) -> bool:
        """Check if a server is online."""
        try:
            requests.get(self.base)
        except:
            return False
        
        return True