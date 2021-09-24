import hoist

client = hoist.Client()
mysock = client.create_server().create_socket('/ws')

@mysock.received()
def socke(msg) -> str:
    return input("return message: ")

server = client.find_server()
socket = server.find_socket('/ws')

@socket.connect()
async def connect(sock: hoist.SocketConnection):
    while True:
        resp = await sock.send(input('send message to socket: '))
        print(resp)