import requests

class ExternalServer:
    def __init__(self, ip: str, port: int):
        self.ip = ip
        self.port = port
        self.url = f'http://{ip}:{port}'
        self.base = self.url + '/hoist/send'
    
    def send(self, message: str) -> None:
        requests.get(self.base, params = {'msg': message})