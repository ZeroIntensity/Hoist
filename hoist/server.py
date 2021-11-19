from .route import Route
from typing import List
from .message import MessageBody, Message
from .response import Response
from fastapi import Request, Response

class Server(Route):
    def __init__(self, *args, **kwargs) -> None:
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
        """Function for adding a route to the server."""
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
            resp_type: str = 'response' if not resp.failure else 'error'

            response.status_code = resp.code

            return {
                resp_type: resp.message,
                'status': resp.code
            }

        self.routes.append(route)
        return route
    