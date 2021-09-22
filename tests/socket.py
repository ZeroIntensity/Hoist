import hoist

client = hoist.Client()
server = client.create_server()
socket = server.create_socket('/ws')

@socket.received('test')
def test(message):
    return input('send resp to socket: ')

@socket.connected()
def connect() -> None:
    print('A client connected!')