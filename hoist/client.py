from flask import Flask
import logging as logs
import os
from .flask_wrapper import FlaskWrapper
from .server import Server
from .external_server import ExternalServer
from .errors import InvalidServerError, ServerExistsError
import requests
from typing import Union, List
from .fastapi_wrapper import FastAPIWrapper
from fastapi import FastAPI

class Client:
    """Main entry point class for hoist."""
    @staticmethod
    def add_hoist(app: Union[Flask, FastAPI], handle_errors: bool = True, auth: List[str] = [""], premade_pages: bool = True) -> Flask:
        """Add hoist to a flask app."""

        if (not isinstance(app, Flask)) and (not isinstance(app, FastAPI)):
            raise TypeError("argument \"app\" must be a Flask or FastAPI instance.")

        wrapper: FlaskWrapper = FlaskWrapper()
        wrapper.add_hoist(app, handle_errors, auth, premade_pages)

        return app

    @staticmethod
    def find_server(ip: str = "localhost", port: int = 5000, protocol: str = "http") -> ExternalServer:
        """Find a hoist server."""
        server: ExternalServer = ExternalServer(ip, port, protocol)

        if not server.check():
            raise InvalidServerError("specified server does not exist or does not have hoist setup.")
    
        return server


    def create_server(self, 
    ip: str = "localhost",
    port: int = 5000,
    auth: list = [""],
    logging: bool = False,
    startup_message: bool = False,
    thread: bool = True,
    run: bool = True,
    handle_errors: bool = True,
    return_app: bool = False,
    premade_pages: bool = True,
    server_type: str = 'fastapi'
) -> Union[Server, Flask]:
        """Creates a completely ready-to-go hoist app."""

        if server_type == 'flask':
            wrapper = FlaskWrapper()

            if not logging:
                log = logs.getLogger('werkzeug')
                log.disabled = True
            
            if not startup_message:
                os.environ["WERKZEUG_RUN_MAIN"] = "true" 

        elif server_type == 'fastapi':
            if not logging:
                log = logs.getLogger("uvicorn")

            wrapper = FastAPIWrapper()
        else:
            raise ValueError('argument "server_type" must be either "flask" or "fastapi"')

        app = wrapper.make_server()

        try:
            requests.get(f'http://{ip}:{port}')
            raise ServerExistsError(f'ip and port are already being used.')
        except:
            pass
        

        wrapper.add_hoist(app, handle_errors, auth, premade_pages)

        if run:
            if thread:
                wrapper.thread_server(app, ip, port)
            else:
                wrapper.run_server(app, ip, port)
        
        if not return_app:
            return app.HOIST_INTERNALSERVER

        return app