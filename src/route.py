from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from typing import Coroutine, Dict, Any, Union, Tuple, List, Type
from .response import Response
from .message import Message

class Route:
    """Class representing a message listener on a route."""
    def __init__(self, server: FastAPI, url: str, auth: List[str] = []) -> None:
        """Constructor for the `Route` class.
server: property server
url: property url
auth: property auth
"""
        self.__server = server
        self._message_listeners: Dict[Union[str, None], Coroutine] = {}
        self.__url = url
        self._auth: List[str] = auth
        self._errors: Dict[Type[Exception], Coroutine] = {}
        self._error_codes: Dict[int, Coroutine] = {}

        server.middleware("http")(self.handle_exceptions)
        
        @server.exception_handler(RequestValidationError)
        async def invalid_args(request, exc) -> JSONResponse:
            return self.make_response('Invalid Arguments', 400, True)
    
    async def handle_exceptions(self, request: Request, call_next) -> None:
        """FastAPI method for handling exceptions."""
        print('1', self._errors)
        try:
            print('2, above call_next', self._errors)
            response = await call_next(request)
            print('3, below call_next', self._errors)
            #code = response.status_code
            #if code in self._error_codes:
                #resp: Response = await self.run_resolver(self._error_codes, code, [code], default_code = code)
                #return self.make_response(resp.message, resp.code, resp.failure)

            return response
        except Exception as e:
            #print(self._errors, e)
            resp: Response = await self.run_resolver(self._errors, e, [e], default_code = 500, no_response = 'Internal Server Error', no_response_code = 500)
            return self.make_response(resp.message, resp.code, resp.failure)

    @property
    def url(self) -> str:
        """URL the route is listening on."""
        return self.__url
    
    @property
    def server(self) -> FastAPI:
        """Server that the route is listening on."""
        return self.__server
    
    @property
    def message_listeners(self) -> Dict[Union[str, None], Coroutine]:
        """Dictionary of functions to be called when a message is received."""
        return self._message_listeners
    
    @message_listeners.setter
    def message_listeners(self, key: str, value: Coroutine) -> None:
        self._message_listeners[key] = value
    
    @property
    def auth(self) -> List[str]:
        """List of valid authentication keys."""
        return self._auth

    async def run_resolver(self, collection: Dict[str, Coroutine], key: str, resolver_args: List[Any] = [], resolver_kwargs: Dict[Any, Any] = {}, default_code: int = 200, no_response: str = 'Server did not respond.', no_response_code: int = 502) -> Response:
        """Function for running a resolver on the server.
collection: Collection to get the listener from.
key: Key to use when getting the listener from the collection.
resolver_args: Arguments to pass to the resolver.
resolver_kwargs: Kwargs to pass to the resolver.
default_code: Status code to use when the resolver doesn't explicitly set it.
no_response: Message to respond with when the resolver doesn't give any return value.
no_response_code: Status code to use when the resolver doesn't give any return value.
"""
        listener: Coroutine = collection.get(key)
        if listener:
            resolver: Union[str, Tuple[Union[str, int]]] = await listener(*resolver_args, **resolver_kwargs)
            
            code: int = resolver[1] if isinstance(resolver, tuple) else default_code
            msg: str = resolver[0]
            failure: bool = False if (code >= 200) and (code <= 300) else True

        return Response(no_response, no_response_code, True) if not listener else Response(message = msg, code = code, failure = failure)

    async def got_message(self, message: Message = None) -> Response:
        """Internal method for calling a message listener.
message: Message that was received.
"""
        return await self.run_resolver(self.message_listeners, message.content, [message])
    
    def received(self, message: Union[str, None] = None) -> None:
        """Decorator for adding a message resolver to the route.
message: Message to listen for.
example ```py
import hoist

server = hoist.create_server('localhost', 5000)
listener = server.create_route('/hello')

@listener.received('hi')
async def test_received(message: hoist.Message) -> str:
    return "hello!"

# now, when you send "hi" to the server it will respond with "hello!"
```
"""
        def decorator(coro: Coroutine):
            self.message_listeners[message] = coro
        return decorator

    def error(self, error: Union[Type[Exception], int]) -> None:
        """Decorator for adding an error handler to the route.
error: Error to listen for.
"""
        def decorator(coro: Coroutine):
            if isinstance(error, int):
                self._error_codes[error] = coro
            else:
                self._errors[error] = coro
        return decorator
    
    def make_response(self, message: str, code: int, failure: bool) -> JSONResponse:
        """Function for generating a JSON response.
message: Message to respond with.
code: Status code to respond with.
failure: Whether the response is an error.
"""
        return JSONResponse(
            Response(message, code, failure).make(), status_code = code
        )
        
