import hoist

server = hoist.create_server('localhost', 5000)
route = server.create_route('/hello')

@route.error(ValueError)
def value_error(exc):
    return 'a value error!', 200

@route.received('hi')
async def hi(message: hoist.Message) -> str:
    raise ValueError('hi')
    print(message.headers)
    return 'hi'
