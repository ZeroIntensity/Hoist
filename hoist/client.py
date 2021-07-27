from flask import Flask
import logging as logs
import os
from .flask_wrapper import FlaskWrapper
from .server import HoistServer
from .external_server import ExternalServer
from .errors import InvalidServerError

class Client:
    @staticmethod
    def add_hoist(app: Flask, handle_errors: bool = True, auth: list = [""]) -> Flask:
        """Add hoist to a flask app."""

        if not isinstance(app, Flask):
            raise TypeError("argument \"app\" must be a Flask instance.")

        wrapper: FlaskWrapper = FlaskWrapper()
        wrapper.add_hoist(app, auth)

        return app


    @staticmethod
    def find_server(ip: str = "localhost", port: int = 5000) -> ExternalServer:
        """Find a hoist server."""
        server: ExternalServer = ExternalServer(ip, port)

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
    handle_errors: bool = True
) -> HoistServer: # Function for creating flask app with hoist route
        """Create a completely ready-to-go hoist app."""
        wrapper: FlaskWrapper = FlaskWrapper()
        app: Flask = wrapper.make_server()

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

        return app.HOIST_INTERNALSERVER