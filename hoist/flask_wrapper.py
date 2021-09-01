from flask import Flask, jsonify, request
from threading import Thread
from .server import Server
from .errors import HoistExistsError
from .error import Error
#from .proxy.proxy import Proxy
from typing import Callable
from .version import __version__

class FlaskWrapper:
    """Wrapper for Flask."""
    @staticmethod
    def make_server() -> Flask:
        """Generate a flask server."""
        app: Flask = Flask(__name__)
        return app

    def add_hoist(self, app: Flask, handle_errors: bool = True, auth: list = [""], premade_pages: bool = True) -> Flask:
        """Function for setting up hoist on an app."""
        if hasattr(app, 'HOIST_INTERNALSERVER'):
            raise HoistExistsError('hoist is already set up on app')

        app.HOIST_INTERNALSERVER = Server(app, handle_errors)

        @app.route('/hoist/send', methods=['POST'])
        def hoist_send() -> str:
            return self.get_response(app, auth, app.HOIST_INTERNALSERVER._received, 'msg')

        if premade_pages:
            @app.route('/hoist', methods=['POST', 'GET'])
            def hoist_home() -> str:
                if request.method == 'POST':
                    return jsonify({'RESPONSE': f'Version {__version__}'})

                # done with html instead of flask.render_template so i dont have to touch the apps template_folder property
                with open('./hoist/home.html') as f:
                    html: str = f.read()
                
                html = html.replace('{{ version }}', __version__).replace('{{ serverUrl }}', request.base_url)

                return html
                

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
        raise NotImplemented('proxys are not yet supported')
        if hasattr(app, 'HOIST_INTERNALPROXY'):
            raise HoistExistsError('hoist is already set up on app')


        app.HOIST_INTERNALPROXY = HoistProxy(app, handle_errors)

        @app.route('/hoist/proxy/connect', methods=['POST'])
        def hoist_proxy_connect() -> str:
            return self.get_response(app, auth, app.HOIST_INTERNALPROXY._connect, 'data')

        @app.route('/hoist/proxy/disconnect', methods=['POST'])
        def hoist_proxy_disconnect() -> str:
            return self.get_response(app, auth, app.HOIST_INTERNALPROXY._disconnect, 'data')


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