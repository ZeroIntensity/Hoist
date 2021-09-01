import hoist

client = hoist.Client()
server = client.create_server(handle_errors=False)

@server.received('a')
def a(message):
    return hoist.Error('a')

