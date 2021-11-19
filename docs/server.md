# Creating a server

To create a server, you need to call the `hoist.create_server()` method, which will create a server on the specified ip and port and then return a `hoist.Server` object.

```py
import hoist

server = hoist.create_server('localhost', 5000)
# variable "server" is now a hoist.Server object
```
