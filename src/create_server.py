import uvicorn
from .server import Server
from fastapi import FastAPI
from threading import Thread

def create_server(*args, **kwargs) -> Server:
    """Function for creating a new hoist server."""
    app = FastAPI()
    ip = kwargs.get('ip') or args[0]
    port = kwargs.get('port') or args[1]

    kwargs['host'] = ip
    kwargs['port'] = port
    kwargs['log_level'] = kwargs.get('log_level') or 'error'

    url: str = f'http://{ip}:{port}'
    
    Thread(target = uvicorn.run, args = [app], kwargs = kwargs).start()

    return Server(app, url)