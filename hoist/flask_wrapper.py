from flask import Flask, jsonify, request
from threading import Thread
from .server import Server
from .errors import HoistExistsError
from .error import Error
#from .proxy.proxy import Proxy
from typing import Callable
from .version import __version__

HTML: str = '''
<!DOCTYPE html>
<html lang="en">
	<head>
		<title>Hoist V{{ version }}</title>
		<meta charset="utf-8" />
		<meta name="viewport" content="width=device-width, initial-scale=1" />
		<link
			rel="stylesheet"
			href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css"
		/>
		<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
		<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.16.0/umd/popper.min.js"></script>
		<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
	</head>
	<body>
		<style text="text/css">
			.nav-link {
				font-size: 18px;
				color: black;
			}

			.nav-link:hover {
				color: #32cd32;
			}
		</style>

		<nav class="navbar navbar-expand-sm bg-light justify-content-center">
			<ul class="navbar-nav">
				<li class="nav-item">
					<a class="nav-link" href="https://github.com/ZeroIntensity/Hoist"
						>GitHub</a
					>
				</li>
				<li class="nav-item">
					<a class="nav-link" href="https://pypi.org/project/hoist3">PyPI</a>
				</li>
				<li class="nav-item">
					<a class="nav-link" href="https://discord.gg/W9QwbpbUbJ">Discord</a>
				</li>
			</ul>
		</nav>
		<br />

		<div class="container-fluid text-center" style="margin-top: 10%">
			<h3 class="display-4" style="font-size: 60px">Hoist V{{ version }}</h3>
			<p style="font-size: 20px">App running successfully!</p>
		</div>
		<script type="text/javascript">
			const serverUrl = window.location.href;
			var auth = "";

			async function httpPost(url) {
				return await fetch(url, {
					method: "post",
					headers: {
						Accept: "application/json",
						"Content-Type": "application/json",
					},
				}).then(response => {
					return response.json();
				});
			}

			async function clicked() {
				const input = document.getElementById("message").value;
				const url = `${serverUrl}/send?msg=${input}&auth=${auth}`;
				var resp = httpPost(url, input);

				resp.then(json => {
					var element = document.getElementById("response");

					if (json.hasOwnProperty("ERROR")) {
						element.innerHTML = `<div class="container">
              <div class="alert alert-danger alert-dismissible">
<button type="button" class="close" data-dismiss="alert">&times;</button>
<strong>Error</strong> Server responded with error "${json["ERROR"]}"
</div></div>
              `;
					} else {
						element.innerHTML = `
              <div class="container">
              <div class="alert alert-success alert-dismissible">
<button type="button" class="close" data-dismiss="alert">&times;</button>
<strong>Response</strong> ${json["RESPONSE"]}
</div></div>
              `;
					}
				});

				return false;
			}
		</script>
	</body>
	<div class="container">
		<p style="font-size: 20px">Send Message To Server</p>
		<form>
			<div class="form-group">
				<input
					type="message"
					class="form-control"
					placeholder="Enter message..."
					name="message"
					id="message"
				/>
			</div>

			<button
				onclick="clicked(); return false;"
				type="submit"
				class="btn btn-success"
			>
				Send
			</button>
		</form>
		<div class="container" style="margin-top: 4%" id="response"></div>
	</div>
</html>

'''

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
                
                html = HTML.replace('{{ version }}', __version__).replace('{{ serverUrl }}', request.base_url)

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