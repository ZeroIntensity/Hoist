from .server import Server
from fastapi import FastAPI
import uvicorn
from threading import Thread

class Client:
    def __init__(self):
        pass

    @staticmethod
    def start_server(app: FastAPI, port: int, ip: str) -> None:
        uvicorn.run(app, host = ip, port = port)

    def create_server(self, ip: str, port: int) -> None:
        app = FastAPI()
        url: str = f'http://{ip}:{port}'
        
        Thread(target = self.start_server, args = (app, port, ip)).start()

        return Server(app, url)