from flask import Flask
import logging as logs
import os
from .flask_wrapper import FlaskWrapper
from .server.server import Server
from .server.external_server import ExternalServer
from .errors import InvalidServerError, ServerExistsError
import requests
from .utils.error import Error
from typing import Union

class Client:
    """Main entry point class for hoist."""
    @staticmethod
    def add_hoist(app: Flask, handle_errors: bool = True, auth: list = [""]) -> Flask:
        """Add hoist to a flask app."""

        if not isinstance(app, Flask):
            raise TypeError("argument \"app\" must be a Flask instance.")

        wrapper: FlaskWrapper = FlaskWrapper()
        wrapper.add_hoist(app, handle_errors, auth)

        return app

    @staticmethod
    def find_server(ip: str = "localhost", port: int = 5000, protocol: str = "http") -> ExternalServer:
        """Find a hoist server."""
        server: ExternalServer = ExternalServer(ip, port, protocol)

        if not server.check():
            raise InvalidServerError("specified server does not exist or does not have hoist setup.")
    
        return server

    def create_proxy(self,
    ip: str = "localhost",
    port: int = 5000,
    auth: list = [""],
    logging: bool = False,
    startup_message: bool = False,
    thread: bool = True,
    run: bool = True,
    handle_errors: bool = True
    ):
        raise NotImplemented('proxys are not yet supported')
        app: Flask = self.create_server(ip, port, [""], logging, startup_message, thread, run, handle_errors, True)
        wrapper = FlaskWrapper()
        server = app.HOIST_INTERNALSERVER
        
        @server.received()
        def catch_all(message):
            return Error('Sending messages to proxies is not allowed.', 403)
        
        wrapper.add_proxy(app, handle_errors, auth)

    def create_server(self, 
    ip: str = "localhost",
    port: int = 5000,
    auth: list = [""],
    logging: bool = False,
    startup_message: bool = False,
    thread: bool = True,
    run: bool = True,
    handle_errors: bool = True,
    return_flask_app: bool = False
) -> Union[Server, Flask]: # Function for creating flask app with hoist route
        """Creates a completely ready-to-go hoist app."""
        wrapper: FlaskWrapper = FlaskWrapper()
        app: Flask = wrapper.make_server()

        try:
            requests.get(f'http://{ip}:{port}')
            raise ServerExistsError(f'ip and port are already being used.')
        except:
            pass

        if not logging:
            log = logs.getLogger('werkzeug') # Get werkzeug logger
            log.disabled = True
        
        if not startup_message:
            os.environ["WERKZEUG_RUN_MAIN"] = "true" # Disable starting nessage
        

        wrapper.add_hoist(app, handle_errors, auth) # Add hoist to flask app
        if run:
            if thread:
                wrapper.thread_server(app, ip, port) # Run the flask app via thread instead of normally running it
            else:
                wrapper.run_server(app, ip, port)

        if not return_flask_app:
            return app.HOIST_INTERNALSERVER

        return app