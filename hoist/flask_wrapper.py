from flask import Flask, jsonify, request
from threading import Thread
from .server import HoistServer

class FlaskWrapper:
    @staticmethod
    def make_server() -> Flask:
        """Generate a flask server."""
        app: Flask = Flask(__name__)
        return app

    @staticmethod
    def add_hoist(app: Flask, handle_errors: bool = True, auth: list = [""]) -> Flask:
        """Function for setting up hoist on an app."""

        app.HOIST_INTERNALSERVER = HoistServer(app, handle_errors)

        @app.route('/hoist/send')
        def hoist_route() -> dict: # Route to be added to flask instance
            HOIST_MESSAGE: str = request.args.get('msg')
            TOKEN = request.args.get('auth')

            if not TOKEN in auth:
                return jsonify({'ERROR': 'unauthorized'}), 401

            if HOIST_MESSAGE == None:
                return jsonify({'ERROR': 'no_message'})
            
            resp, success = app.HOIST_INTERNALSERVER._received(HOIST_MESSAGE)

            if not success:
                return jsonify({'ERROR': resp}), 500
            
            else:
                return jsonify({'RESPONSE': resp})

        return app
    
    @staticmethod
    def run_server(app: Flask, ip: str, port: int) -> Flask:
        """Function for running a flask app."""
        app.run(ip, port)

        return app

    def thread_server(self, app: Flask, ip: str, port: int) -> Flask:
        """Function for running a flask app with a thread."""
        server: Thread = Thread(target = self.run_server, args = (app, ip, port))
        server.start()

        return app