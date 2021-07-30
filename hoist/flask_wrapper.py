from flask import Flask, jsonify, request
from threading import Thread
from .server import HoistServer
from .errors import HoistExistsError
from .utils.error import Error
from .proxy import HoistProxy
from types import Callable

class FlaskWrapper:
    """Wrapper for Flask."""
    @staticmethod
    def make_server() -> Flask:
        """Generate a flask server."""
        app: Flask = Flask(__name__)
        return app

    def add_hoist(self, app: Flask, handle_errors: bool = True, auth: list = [""]) -> Flask:
        """Function for setting up hoist on an app."""
        if hasattr(app, 'HOIST_INTERNALSERVER'):
            raise HoistExistsError('hoist is already set up on app')

        app.HOIST_INTERNALSERVER = HoistServer(app, handle_errors)

        @app.route('/hoist/send', methods=['POST'])
        def hoist_route() -> str: # Route to be added to flask instance
            return self.get_response(app, auth, app.HOIST_INTERNALSERVER._received, 'msg')

        return app

    @staticmethod
    def get_response(app: Flask, auth: list, callback: Callable, argument: str) -> str:
        """Function for getting the response of a request."""
        ARG: str = request.args.get(argument)
        TOKEN = request.args.get('auth')

        if not TOKEN in auth:
            return jsonify({'ERROR': 'unauthorized'}), 401
            
        resp, success = callback(ARG)

        if isinstance(resp, Error):
            return jsonify({'ERROR': resp._message}), resp._code

        if not success:
            return jsonify({'ERROR': resp}), 500
            
        else:
            return jsonify({'RESPONSE': resp})


    def add_proxy(self, app: Flask, handle_errors: bool = True, auth: list = [""]) -> Flask:
        """Function for setting up a hoist proxy on an app."""

        raise NotImplemented('Proxys have not yet been implemented to Hoist.')

        if hasattr(app, 'HOIST_INTERNALPROXY'):
            raise HoistExistsError('hoist is already set up on app')


        app.HOIST_INTERNALPROXY = HoistProxy(app, handle_errors)

        @app.route('/hoist/proxy/connect', methods=['POST'])
        def hoist_proxy_connect() -> str:
            return self.get_response(app, auth, app.HOIST_INTERNALPROXY._connect, 'address')

        @app.route('/hoist/proxy/disconnect', methods=['POST'])
        def hoist_proxy_disconnect() -> str:
            return self.get_response(app, auth, app.HOIST_INTERNALPROXY._disconnect, 'address')


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