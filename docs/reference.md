# Reference
## Route
**Class representing a message listener on a route.**
### __init__
`#!python __init__(self, server: fastapi.applications.FastAPI, url: str, auth: List[str] = []) -> None`

**Constructor for the `Route` class.**

**Returns:** `#!python NoneType`
#### Parameters
| Name | Type | Description | Default |
| ----------- | ----------- | ----------- | ----------- |
| server | `#!python FastAPI` | Server that the route is listening on. | Required |
| url | `#!python str` | URL the route is listening on. | Required |
| auth | `#!python typing.List[str]` | List of valid authentication keys. | `#!python []` |


### auth

**List of valid authentication keys.**

**Type:** `#!python typing.List[str]`

### error
`#!python error(self, error: Union[Type[Exception], int]) -> None`

**Decorator for adding an error handler to the route.**

**Returns:** `#!python NoneType`
#### Parameters
| Name | Type | Description | Default |
| ----------- | ----------- | ----------- | ----------- |
| error | `#!python typing.Union[typing.Type[Exception], int]` | Error to listen for. | Required |


### got_message
`#!python got_message(self, message: hoist.message.Message = None) -> hoist.response.Response`

**Internal method for calling a message listener.**

**Returns:** `#!python Response`
#### Parameters
| Name | Type | Description | Default |
| ----------- | ----------- | ----------- | ----------- |
| message | `#!python typing.Union[hoist.message.Message, NoneType]` | Message that was received. | `#!python None` |


### handle_exceptions
`#!python handle_exceptions(self, request: starlette.requests.Request, call_next) -> None`

**FastAPI method for handling exceptions.**

**Returns:** `#!python NoneType`
#### Parameters
| Name | Type | Description | Default |
| ----------- | ----------- | ----------- | ----------- |
| request | `#!python Request` |  | Required |


### make_response
`#!python make_response(self, message: str, code: int, failure: bool) -> starlette.responses.JSONResponse`

**Function for generating a JSON response.**

**Returns:** `#!python JSONResponse`
#### Parameters
| Name | Type | Description | Default |
| ----------- | ----------- | ----------- | ----------- |
| message | `#!python str` | Message to respond with. | Required |
| code | `#!python int` | Status code to respond with. | Required |
| failure | `#!python bool` | Whether the response is an error. | Required |


### message_listeners

**Dictionary of functions to be called when a message is received.**

**Type:** `#!python typing.Dict[typing.Union[str, NoneType], typing.Coroutine]`

### received
`#!python received(self, message: Union[str, NoneType] = None) -> None`

**Decorator for adding a message resolver to the route.**

**Returns:** `#!python NoneType`
#### Parameters
| Name | Type | Description | Default |
| ----------- | ----------- | ----------- | ----------- |
| message | `#!python typing.Union[str, NoneType]` | Message to listen for. | `#!python None` |


#### Example
```py
import hoist

server = hoist.create_server('localhost', 5000)
listener = server.create_route('/hello')

@listener.received('hi')
async def test_received(message: hoist.Message) -> str:
    return "hello!"

# now, when you send "hi" to the server it will respond with "hello!"
```
### run_resolver
`#!python run_resolver(self, collection: Dict[str, Coroutine], key: str, resolver_args: List[Any] = [], resolver_kwargs: Dict[Any, Any] = {}, default_code: int = 200, no_response: str = 'Server did not respond.', no_response_code: int = 502) -> hoist.response.Response`

**Function for running a resolver on the server.**

**Returns:** `#!python Response`
#### Parameters
| Name | Type | Description | Default |
| ----------- | ----------- | ----------- | ----------- |
| collection | `#!python typing.Dict[str, typing.Coroutine]` | Collection to get the listener from. | Required |
| key | `#!python str` | Key to use when getting the listener from the collection. | Required |
| resolver_args | `#!python typing.List[typing.Any]` | Arguments to pass to the resolver. | `#!python []` |
| resolver_kwargs | `#!python typing.Dict[typing.Any, typing.Any]` | Kwargs to pass to the resolver. | `#!python {}` |
| default_code | `#!python int` | Status code to use when the resolver doesn't explicitly set it. | `#!python 200` |
| no_response | `#!python str` | Message to respond with when the resolver doesn't give any return value. | `#!python 'Server did not respond.'` |
| no_response_code | `#!python int` | Status code to use when the resolver doesn't give any return value. | `#!python 502` |


### server

**Server that the route is listening on.**

**Type:** `#!python FastAPI`

### url

**URL the route is listening on.**

**Type:** `#!python str`


## Server
**None**
### __init__
`#!python __init__(self, *args, **kwargs) -> None`

**Constructor for the `Server` class.**

**Returns:** `#!python NoneType`


### auth

**List of valid authentication keys.**

**Type:** `#!python typing.List[str]`

### create_route
`#!python create_route(self, path: str, auth: List[str] = []) -> hoist.route.Route`

**Function for adding a route to the server.**

**Returns:** `#!python Route`
#### Parameters
| Name | Type | Description | Default |
| ----------- | ----------- | ----------- | ----------- |
| path | `#!python str` | Path to create the route object for. | Required |
| auth | `#!python typing.List[str]` | List of valid authentication tokens for that route. | `#!python []` |


#### Example
```py
import hoist

server = hoist.create_server('localhost', 5000)
route = server.create_route('/hello') # creates a route at path '/hello'
```
### error
`#!python error(self, error: Union[Type[Exception], int]) -> None`

**Decorator for adding an error handler to the route.**

**Returns:** `#!python NoneType`
#### Parameters
| Name | Type | Description | Default |
| ----------- | ----------- | ----------- | ----------- |
| error | `#!python typing.Union[typing.Type[Exception], int]` | Error to listen for. | Required |


### got_message
`#!python got_message(self, message: hoist.message.Message = None) -> hoist.response.Response`

**Internal method for calling a message listener.**

**Returns:** `#!python Response`
#### Parameters
| Name | Type | Description | Default |
| ----------- | ----------- | ----------- | ----------- |
| message | `#!python typing.Union[hoist.message.Message, NoneType]` | Message that was received. | `#!python None` |


### handle_exceptions
`#!python handle_exceptions(self, request: starlette.requests.Request, call_next) -> None`

**FastAPI method for handling exceptions.**

**Returns:** `#!python NoneType`
#### Parameters
| Name | Type | Description | Default |
| ----------- | ----------- | ----------- | ----------- |
| request | `#!python Request` |  | Required |


### make_response
`#!python make_response(self, message: str, code: int, failure: bool) -> starlette.responses.JSONResponse`

**Function for generating a JSON response.**

**Returns:** `#!python JSONResponse`
#### Parameters
| Name | Type | Description | Default |
| ----------- | ----------- | ----------- | ----------- |
| message | `#!python str` | Message to respond with. | Required |
| code | `#!python int` | Status code to respond with. | Required |
| failure | `#!python bool` | Whether the response is an error. | Required |


### message_listeners

**Dictionary of functions to be called when a message is received.**

**Type:** `#!python typing.Dict[typing.Union[str, NoneType], typing.Coroutine]`

### received
`#!python received(self, message: Union[str, NoneType] = None) -> None`

**Decorator for adding a message resolver to the route.**

**Returns:** `#!python NoneType`
#### Parameters
| Name | Type | Description | Default |
| ----------- | ----------- | ----------- | ----------- |
| message | `#!python typing.Union[str, NoneType]` | Message to listen for. | `#!python None` |


#### Example
```py
import hoist

server = hoist.create_server('localhost', 5000)
listener = server.create_route('/hello')

@listener.received('hi')
async def test_received(message: hoist.Message) -> str:
    return "hello!"

# now, when you send "hi" to the server it will respond with "hello!"
```
### routes

**List of routes on the server.**

**Type:** `#!python typing.List[hoist.route.Route]`

### run_resolver
`#!python run_resolver(self, collection: Dict[str, Coroutine], key: str, resolver_args: List[Any] = [], resolver_kwargs: Dict[Any, Any] = {}, default_code: int = 200, no_response: str = 'Server did not respond.', no_response_code: int = 502) -> hoist.response.Response`

**Function for running a resolver on the server.**

**Returns:** `#!python Response`
#### Parameters
| Name | Type | Description | Default |
| ----------- | ----------- | ----------- | ----------- |
| collection | `#!python typing.Dict[str, typing.Coroutine]` | Collection to get the listener from. | Required |
| key | `#!python str` | Key to use when getting the listener from the collection. | Required |
| resolver_args | `#!python typing.List[typing.Any]` | Arguments to pass to the resolver. | `#!python []` |
| resolver_kwargs | `#!python typing.Dict[typing.Any, typing.Any]` | Kwargs to pass to the resolver. | `#!python {}` |
| default_code | `#!python int` | Status code to use when the resolver doesn't explicitly set it. | `#!python 200` |
| no_response | `#!python str` | Message to respond with when the resolver doesn't give any return value. | `#!python 'Server did not respond.'` |
| no_response_code | `#!python int` | Status code to use when the resolver doesn't give any return value. | `#!python 502` |


### server

**Server that the route is listening on.**

**Type:** `#!python FastAPI`

### url

**URL the route is listening on.**

**Type:** `#!python str`


## Message
**Class representing a message.**
### __init__
`#!python __init__(self, content: str, headers: Dict[str, str]) -> None`

**Constructor for the `Message` class.**

**Returns:** `#!python NoneType`
#### Parameters
| Name | Type | Description | Default |
| ----------- | ----------- | ----------- | ----------- |
| content | `#!python str` | Content of the message. | Required |
| headers | `#!python typing.Dict[str, str]` | Headers that came with the message request. | Required |


### content

**Content of the message.**

**Type:** `#!python str`

### headers

**Headers that came with the message request.**

**Type:** `#!python typing.Dict[str, str]`


## Response
**Class representing a server response.**
### __init__
`#!python __init__(self, message: str, code: int = 200, failure: bool = False) -> None`

**Constructor for the `Response` class.**

**Returns:** `#!python NoneType`
#### Parameters
| Name | Type | Description | Default |
| ----------- | ----------- | ----------- | ----------- |
| message | `#!python str` | Message that the server responded with. | Required |
| code | `#!python int` | Status code that the server responded with. | `#!python 200` |
| failure | `#!python bool` | Whether the server responded with an error. | `#!python False` |


### code

**Status code that the server responded with.**

**Type:** `#!python int`

### failure

**Whether the server responded with an error.**

**Type:** `#!python bool`

### make
`#!python make(self) -> dict`

**Function for turning the object into the HTTP response.**

**Returns:** `#!python dict`


### message

**Message that the server responded with.**

**Type:** `#!python str`

