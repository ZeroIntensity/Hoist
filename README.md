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

ip = hoist.get_ip()
port = 5000

server = client.create_server(ip, port)

@server.received('hi')
def receive(message):
    return 'Hello!'
    
```

```py
# file2.py

import hoist

client = hoist.Client()
server = client.find_server(ip, port) # Assuming we have our ip and port from above

resp = server.send('hi')

print(resp) # Prints out "Hello!"
```

