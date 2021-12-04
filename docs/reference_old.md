# Reference

## Functions

### _create_server_

`#!python def create_server(ip: str, port: int, *args, **kwargs) -> hoist.Server`

Function for creating a new hoist server.

**Member Of:** None

**Returns:** [hoist.Server](#server)

**Raises:**

- None

#### Parameters

| Name               | Type                  | Description                                          | Default      |
| ------------------ | --------------------- | ---------------------------------------------------- | ------------ |
| ip                 | `#!python str`        | IP to run the server on.                             | Required     |
| port               | `#!python int`        | Port to run the server on.                           | Required     |
| \*args, \*\*kwargs | `#!python list, dict` | Args and kwargs to pass into the `uvicorn.run` call. | `None, None` |

#### Example

```py
import hoist

server = hoist.create_server('localhost', 5000)
```

### _make_response_

`#!python def make_response(self, message: str, code: int, failure: bool) -> fastapi.responses.JSONResponse`

**This is an internal utility function. There is no purpose for it being called manually.**

Function for generating a JSON response.

**Member Of:** [hoist.Route](#route)

**Returns:** `fastapi.responses.JSONResponse`

**Raises:**

- None

#### Example

```py
# hoist/route.py

class Route:
    ...

    async def handle_exceptions(self, request: Request, call_next):
        ...

        resp: Response = await self.run_resolver(self._errors, e, [e], default_code = 500, no_response = 'Internal Server Error', no_response_code = 500)
        return self.make_response(resp.message, resp.code, resp.failure)

```

#### Parameters

| Name    | Type            | Description                                                                         | Default  |
| ------- | --------------- | ----------------------------------------------------------------------------------- | -------- |
| message | `#!python str`  | Message that the server will use in the `"message"` key of the response.            | Required |
| code    | `#!python int`  | Status code of the request that will be used in the `"status"` key of the response. | Required |
| failure | `#!python bool` | Whether the response should use an `"error"` key instead of `"message"`.            | `False`  |

### _received_

`#!python def received(self, message: Union[str, None] = None) -> None:`

**This function is a decorator.**

Decorator for adding a message resolver to the route.

**Member Of:** [hoist.Route](#route)

**Returns:** `None`

**Raises:**

- None

#### Parameters

| Name    | Type                 | Description                                                                                                  | Default |
| ------- | -------------------- | ------------------------------------------------------------------------------------------------------------ | ------- |
| message | `#!python str, None` | Message to resolve. If this argument is `None`, then the decorated function will be called on every request. | `None`  |

#### Decorated Function Specifications

Functions decorated with this method will be called when the server receives a message matching the argument passed into `message`. The function must have one parameter, and a [hoist.Message](#message) instance will be passed into it when called. Then, the function should return something of type `str` OR of type `#!python Sequence[Union[str, int]]`. If the return value is just a `str` object, then the server will respond with that value and a status of 200. If the return value is `#!python Sequence[Union[str, int]]`, then the server will respond with the value at index 0 of the iterable, using the value at index 1 as the status code.

#### Example

```py
import hoist
from typing import Tuple, Union

server = hoist.create_server('localhost', 5000)

@server.received('create')
def handler(message: hoist.Message) -> Tuple[Union[str, int]]:
    ...

    return 'created successfully!', 203 # status 203

@server.received('hello')
def hello(message: hoist.Message) -> str:
    return 'hi' # status 200
```

### _error_

`#!python def error(self, error: Union[Type[Exception], int]) -> None`

**This function is a decorator.**

Decorator for adding an error handler to the route.

**Member Of:** [hoist.Route](#route)

**Returns:** `None`

**Raises:**

- None

#### Parameters

| Name  | Type                            | Description                                                                                                                                                                                                                       | Default  |
| ----- | ------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------- |
| error | `#!python Type[Exception], int` | Error to handle. If the argument is of type `int`, then it will call the decorated function when the route gets that HTTP status code. Otherwise, it's registered as an error handler for the exception passed into the argument. | Required |

#### Decorated Function Specifications

Functions that this method decorates should always take one parameter, which will be the error or status code that was passed into the `error` argument. This functions return value follows the same rules as [Route.received](#received), please see that for more info.

#### Example

```py
import hoist

server = hoist.create_server('localhost', 5000)

@server.error(ValueError)
def handler(exc: ValueError) -> str:
    return 'a value error!'
```

## Objects

### _Server_

`#!python class Server(Route)`

### _Route_

```py
class Route:
    def __init__(self, server: FastAPI, url: str, auth: List[str] = []) -> None:
        ...

    async def handle_exceptions(self, request: Request, call_next):
        ...

    @property
    def url(self) -> str:
        ...

    @property
    def server(self) -> FastAPI:
        ...

    @property
    def message_listeners(self) -> Dict[Union[str, None], Coroutine]:
        ...

    @message_listeners.setter
    def message_listeners(self, key: str, value: Coroutine) -> None:
        ...

    @property
    def auth(self) -> List[str]:
        ...

    async def run_resolver(self, collection: Dict[str, Coroutine], key: str, resolver_args: List[Any] = [], resolver_kwargs: Dict[Any, Any] = {}, default_code: int = 200, no_response: str = 'Server did not respond.', no_response_code: int = 502) -> Response:
        ...

    async def got_message(self, message: Message = None) -> Response:
        ...

    def received(self, message: Union[str, None] = None) -> None:
        ...


    def error(self, error: Union[Type[Exception], int]) -> None:
        ...


    def make_response(self, message: str, code: int, failure: bool) -> JSONResponse:
        ...

```

Class representing a message listener on a route

#### Constructor Parameters

| Name   | Type                       | Description                          | Default  |
| ------ | -------------------------- | ------------------------------------ | -------- |
| server | `#!python fastapi.FastAPI` | Server that the route is running on. | Required |
| url    | `#!python str`             | URL of the server.                   | Required |
| auth   | `#!python list`            | List of valid authentication keys.   | `[]`     |

#### Members

##### Properties

| Name              | Type                                         | Description                                             | Mutable? |
| ----------------- | -------------------------------------------- | ------------------------------------------------------- | -------- |
| url               | `#!python str`                               | URL of the route.                                       | No       |
| server            | `fastapi.FastAPI`                            | FastAPI object of the server.                           | No       |
| message_listeners | `#!python Dict[Union[str, None], Coroutine]` | Dictionary of resolvers for when a message is received. | Yes      |

##### Functions

### _Response_

```py
@dataclass
class Response:
    message: str
    code: int
    failure: bool
```

**This is a dataclass.**

Class representing a server response.

#### Constructor Parameters

| Name    | Type            | Description                                | Default  |
| ------- | --------------- | ------------------------------------------ | -------- |
| message | `#!python str`  | Message that will be used in the response. | Required |
| code    | `#!python int`  | Status code of the response.               | `200`    |
| failure | `#!python bool` | Whether the response failed or not.        | `False`  |

### _Message_

```py
@dataclass
class Message:
    content: str
    headers: Dict[str, str]
```

**This is a dataclass.**

Class representing a message.

#### Constructor Parameters

| Name    | Type            | Description             | Default  |
| ------- | --------------- | ----------------------- | -------- |
| content | `#!python str`  | Content of the message. | Required |
| content | `#!python dict` | Headers of the request. | Required |

### _MessageBody_

```py
@dataclass
class Message:
    message: Optional[str] = None
    auth: Optional[str] = None
```

**This is an internal utility class. It has no purpose to be initialized directly.**

Class for representing the FastAPI message body.

#### Constructor Parameters

| Name    | Type           | Description                                | Default |
| ------- | -------------- | ------------------------------------------ | ------- |
| message | `#!python str` | Message to send to the server.             | `None`  |
| auth    | `#!python str` | Authentication key to use for the request. | `None`  |
