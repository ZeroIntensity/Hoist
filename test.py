import hoist

client = hoist.Client()
server = client.create_server()

@server.received()
def catch_all(message):
    return hoist.Error('test', 500)

test = client.find_server()

resp = test.send('a')
print(resp)