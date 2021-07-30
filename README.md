[GitHub](https://github.com/ZeroIntensity/hoist)


## Features
- Easy to use with object oriented syntax.
- Intellisense support with typehints and docstrings.
- High flexibility with configuration options.
- Supports newer versions of Python.
- Self explanatory error messages.

## Upcoming features
- Enhanced docstrings
- Documentation
- Support for using servers across multiple files.
- Proxys

## Credits

This project was developed by [ZeroIntensity](https://github.com/ZeroIntensity), under the MIT License.
### Dependencies
- [Flask](https://pypi.org/project/flask)
- [Requests](https://pypi.org/project/requests)

## Example

```py
# file1.py

import hoist

client = hoist.Client()

server = client.create_server('localhost', 5000)

@server.received('hi')
def receive(message):
    return 'Hello!'

@server.received()
def catch_all(message):
    print(f'{message} was received.')

```

```py
# file2.py

import hoist

client = hoist.Client()
server = client.find_server('localhost', 5000) # Assuming we have our ip and port from above

resp = server.send('hi')
server.send('test') # Prints out "test was received" in file1

print(resp) # Prints out "Hello!"
```

