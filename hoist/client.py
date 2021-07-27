from flask import Flask
import logging as logs
import os
from .flask_wrapper import FlaskWrapper
from .server import HoistServer
from .external_server import ExternalServer


class Client:
    @staticmethod
    def add_hoist(app: Flask) -> Flask:
        """py:staticmethod:: add_hoist(app: Flask) -> Flask

    Setup hoist on a flask app.

    :param flask.Flask app: app to setup hoist on.
    :raises TypeError: if app is not a Flask app.
    :return: app passed in to "app".
    :rtype: flask.Flask

    """
        if not isinstance(app, Flask):
            raise TypeError("argument \"app\" must be a Flask instance.")

        wrapper: FlaskWrapper = FlaskWrapper()
        wrapper.add_hoist(app)

        return app


    @staticmethod
    def find_server(ip: str, port: int) -> ExternalServer:
        """py:staticmethod:: find_server(ip: str, port: int) -> ExternalServer

            Get a server object via a url and port.

            :param str ip: ip of the server to find.
            :param int port: port of the server to find.
            :raises ValueError: if server is not found and/or hoist is not setup.
            :return: ExternalServer object.
            :rtype: hoist.ExternalServer

            """
        server: ExternalServer = ExternalServer(ip, port)
        if not server.check():
            raise ValueError("specified server does not exist or does not have hoist setup.")
    
        return server

    def create_server(self, ip: str = "", port: int = 0, logging: bool = False, startup_message: bool = False, thread: bool = True, run = True) -> HoistServer: # Function for creating flask app with hoist route
        wrapper: FlaskWrapper = FlaskWrapper()
        app: Flask = wrapper.make_server()

        if not logging:
            log = logs.getLogger('werkzeug') # Get werkzeug logger
            log.disabled = True
        
        if not startup_message:
            os.environ["WERKZEUG_RUN_MAIN"] = "true" # Disable starting nessage
        

        wrapper.add_hoist(app) # Add hoist to flask app
        if run:
            if thread:
                wrapper.thread_server(app, ip, port) # Run the flask app via thread instead of normally running it
            else:
                wrapper.run_server(app, ip, port)

        return app.HOIST_INTERNALSERVER