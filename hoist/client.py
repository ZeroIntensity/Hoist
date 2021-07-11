from flask import Flask
import logging as logs
import os
from .flask_wrapper import FlaskWrapper
from .server import HoistServer
from .external_server import ExternalServer
import socket

class Client:

    @staticmethod
    def add_hoist(app) -> Flask: # Function for adding hoist route to existing flask app
        wrapper: FlaskWrapper = FlaskWrapper()
        wrapper.add_hoist(app)

        return app

    @staticmethod
    def get_ip() -> str:
        un = socket.gethostname()
        ip = socket.gethostbyname(un)

        return ip

    def gen_ip_and_port(self) -> str:
        ip = self.get_ip()
        port = 5000
        
        return (ip, port)

    @staticmethod
    def find_server(ip: str, port: int) -> ExternalServer:
        return ExternalServer(ip, port)

    def create_server(self, ip: str = "", port: int = 0, logging: bool = False, startup_message: bool = False, thread: bool = True, run = True) -> HoistServer: # Function for creating flask app with hoist route
        wrapper: FlaskWrapper = FlaskWrapper()
        app: Flask = wrapper.make_server()

        if not logging:
            log = logs.getLogger('werkzeug') # Get werkzeug logger
            log.disabled = True
        
        if not startup_message:
            os.environ["WERKZEUG_RUN_MAIN"] = "true" # Disable starting nessage
        

        wrapper.add_hoist(app)
        if run:
            if thread:
                wrapper.thread_server(app, ip, port) # Run the flask app via thread instead of normally running it
            else:
                wrapper.run_server(app, ip, port)

        return app.HOIST_INTERNALSERVER