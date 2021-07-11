# Hoist
Communicate with other machines via the network.


**Note:** Project currently under development, not all features have been implemented.
## Credits
### Developer
This project was developed by [ZeroIntensity](https://github.com/ZeroIntensity), under the MIT License.
### Dependencies
- [Flask](https://pypi.org/project/flask)

[GitHub](https://github.com/ZeroIntensity/hoist)

## Example
**Note:** `file1.py` and `file2.py` can be on **different machines**.
```py
# file1.py

import hoist

client = hoist.Client()
ip, port = client.gen_ip_and_port()
server = client.create_server(ip, port)

@server.received()
def receive(message):
    print(f'Received "{message}"!')
```

```py
# file2.py

import hoist

client = hoist.Client()
ip, port = client.gen_ip_and_port()
server = client.find_server(ip, port)

server.send('sent') # Prints out 'Received "sent"!' in file1.py
```

## Docs coming soon!

