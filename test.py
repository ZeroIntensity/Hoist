import hoist

server = hoist.create_server('localhost', 5000)
listener = server.create_route('/hello')

@listener.received('hi')
async def hi(message) -> str:
    return 'hi', 500