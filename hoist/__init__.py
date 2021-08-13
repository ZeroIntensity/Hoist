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
from .external_server import ExternalServer
from .server import Server
from .get_ip import get_ip
from .get_host import get_host
from .generate_key import generate_key
from .error import Error
from .errors import ServerResponseError, HoistExistsError, InvalidServerError, ServerExistsError, ServerAuthenticationError

__VERSION__ = '0.1.1'