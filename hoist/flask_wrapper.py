from flask import Flask, jsonify, request
from threading import Thread
from .server import HoistServer

class FlaskWrapper:
    @staticmethod
    def make_server() -> Flask:
        app: Flask = Flask(__name__)
        return app

    @staticmethod
    def add_hoist(app: Flask) -> Flask:
        app.HOIST_INTERNALSERVER = HoistServer(app)

        @app.route('/hoist/send')
        def hoist_route() -> dict: # Route to be added to flask instance
            HOIST_MESSAGE: str = request.args.get('msg')

            if HOIST_MESSAGE == None:
                return jsonify({'ERROR': 'no_message'})
            
            app.HOIST_INTERNALSERVER._received(HOIST_MESSAGE)
            return jsonify({'MESSAGE': HOIST_MESSAGE})

        return app
    
    @staticmethod
    def run_server(app: Flask, ip: str, port: int) -> Flask:
        app.run(ip, port)

        return app

    def thread_server(self, app: Flask, ip: str, port: int) -> Flask:
        server = Thread(target = self.run_server, args = (app, ip, port))
        server.start()

        return app