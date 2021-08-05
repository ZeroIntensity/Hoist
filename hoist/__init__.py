"""
# Hoist
Library for managing websockets and sending messages over a network.
Written by [ZeroIntensity](https://github.com/ZeroIntensity), under the MIT License.


## Quick Example
```py
import hoist

client = hoist.Client()
server = client.create_server() # Create a server

@server.received()
def catch_all(message):
    print(f'Received {message}') 

server2 = client.find_server() # Finds the server from above
server2.send('hi') # Prints "Received hi"
```
"""

from .client import Client
from .flask_wrapper import FlaskWrapper
from .server.external_server import ExternalServer
from .server.server import Server
from .utils.get_ip import get_ip
from .utils.get_host import get_host
from .utils.generate_key import generate_key
from .utils.error import Error
from .errors import ServerResponseError, HoistExistsError, InvalidServerError, ServerExistsError
from .proxy.external_proxy import ExternalProxy