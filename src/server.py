from .route import Route
from typing import List
from .message import MessageBody, Message
from .response import Response
from fastapi import Request, Response

class Server(Route):
    def __init__(self, *args, **kwargs) -> None:
        """Constructor for the `Server` class."""
        super().__init__(*args, **kwargs)
        self._routes: List[Route] = []
    
    @property
    def routes(self) -> List[Route]:
        """List of routes on the server."""
        return self._routes
    
    @routes.setter
    def routes(self, route: Route) -> None:
        self._routes.append(route)

    def create_route(self, path: str, auth: List[str] = []) -> Route:
        """Function for adding a route to the server.
path: Path to create the route object for.
auth: List of valid authentication tokens for that route.
example ```py
import hoist

server = hoist.create_server('localhost', 5000)
route = server.create_route('/hello') # creates a route at path '/hello'
```
"""
        route = Route(self.server, self.url + path, auth)

        @self.server.post(path)
        async def rt(body: MessageBody, request: Request, response: Response) -> None:
            msg = Message(body.message, request.headers)

            if auth:
                if not body.auth in auth:
                    response.status_code = 401
                    return {
                        'error': 'Invalid authentication token.',
                        'status': 401
                    }

            resp: Response = await route.got_message(msg)
            response.status_code = resp.code

            return resp.make()

        self.routes.append(route)
        return route
    