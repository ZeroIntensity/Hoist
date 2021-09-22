from fastapi import FastAPI, Response, WebSocket, WebSocketDisconnect
from threading import Thread
from .server import Server
from .errors import HoistExistsError
from .error import Error
from .version import __version__
from .flask_wrapper import HTML
import uvicorn
from typing import List, Callable
from fastapi.responses import HTMLResponse, JSONResponse

class FastAPIWrapper:
    """Wrapper for FastAPI."""
    @staticmethod
    def make_server(*args, **kwargs) -> FastAPI:
        """Generate a FastAPI server."""
        return FastAPI(*args, **kwargs)

    def get_response(self, auth: str, tokens: List[str], callback: Callable, arg: str, response: Response) -> dict:
        if not auth in tokens:
                response.status_code = 401
                return {'ERROR': 'unauthorized'}
        
        resp, success = callback(arg)

        if isinstance(resp, Error):
            response.status_code = resp.code
            return {'ERROR': resp.message}

        if not success:
            response.status_code = 500
            return {'ERROR': resp}
        else:
            return {'RESPONSE': resp}

    def add_hoist(self, app: FastAPI, handle_errors: bool = True, auth: list = [""], premade_pages: bool = True) -> FastAPI:
        """Function for setting up hoist on an app."""
        if hasattr(app, 'HOIST_INTERNALSERVER'):
            raise HoistExistsError('hoist is already set up on app')

        app.HOIST_INTERNALSERVER = Server(app, handle_errors)
        tokens: List[str] = auth.copy() # to stop collisions
        app.HOIST_AUTH = tokens
        app.HOIST_WRAPPER = self
        

        @app.exception_handler(422)
        def invalid_args(req, exc) -> JSONResponse:
            print('a')
            return JSONResponse({"ERROR": "Invalid arguments."}, status_code = 400)


        @app.post('/hoist/send')
        def http_send(msg: str, auth: str, response: Response) -> dict:
            return self.get_response(auth, tokens, app.HOIST_INTERNALSERVER._received, msg, response)
            

        if premade_pages:
            @app.get('/hoist')
            def home_get() -> str:
                return HTMLResponse(
                    HTML.replace('{{ version }}', __version__)
                )
            
            @app.post('/hoist')
            def hoist_post() -> str:
                return {'RESPONSE': f'Version {__version__}'}       

        return app

    
    @staticmethod
    def run_server(app: FastAPI, ip: str, port: int) -> None:
        """Function for running a FastAPI server."""
        uvicorn.run(app, host = ip, port = port)

    def thread_server(self, app: FastAPI, ip: str, port: int) -> FastAPI:
        """Function for running a flask app with a thread."""
        server: Thread = Thread(target = self.run_server, args = (app, ip, port))
        server.start()

        return app
    
    def add_socket(self, app: FastAPI, route: str) -> None:
        """Function for adding a socket to a FastAPI server."""

        @app.websocket(route)
        async def ws(websocket: WebSocket, response: Response):
            sock = app.HOIST_SOCKETS[route]
            for i in sock.connect:
                i()

            await websocket.accept()

            while True:
                try:
                    data = await websocket.receive_text()
                    resp = self.get_response("", app.HOIST_AUTH, sock._received, data, response)
                    await websocket.send_json(resp)
                except WebSocketDisconnect:
                    for i in sock.disconnect:
                        i()
                    break
