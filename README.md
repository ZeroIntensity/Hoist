![PyPI](https://img.shields.io/pypi/v/hoist3?color=blue)
![PyPI - Status](https://img.shields.io/pypi/status/hoist3)
![PyPI - Downloads](https://img.shields.io/pypi/dm/hoist3)
![GitHub](https://img.shields.io/github/license/ZeroIntensity/Hoist)
![GitHub last commit](https://img.shields.io/github/last-commit/ZeroIntensity/Hoist?color=success)
![https://discord.gg/W9QwbpbUbJ](https://discord.com/api/guilds/882712747048058920/embed.png)

**Documentation coming in version `0.1.3`**

- [GitHub](https://github.com/ZeroIntensity/Hoist)
- [PyPI](https://pypi.org/project/hoist3)
- [Discord](https://discord.gg/W9QwbpbUbJ)

## Features

- Easy to use with object oriented syntax.
- Intellisense support with typehints and docstrings.
- High flexibility with configuration options.
- Supports newer versions of Python.
- Self explanatory error messages.

## Upcoming features

- Enhanced docstrings
- Documentation
- Proxys
- CLI

## Installation

To install hoist, run one of these commands, depending on your OS.

### Linux/Mac

```
python3 -m pip install -U hoist3
```

### Windows

```
py -3 -m pip install -U hoist3
```

## Credits

This project was developed by [ZeroIntensity](https://github.com/ZeroIntensity), under the MIT License.

### Dependencies

- [Flask](https://pypi.org/project/flask)
- [Requests](https://pypi.org/project/requests)

## Examples

### Basic Server Example

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
server = client.find_server('localhost', 5000)

resp = server.send('hi')
server.send('test') # Prints out "test was received" in file1

print(resp) # Prints out "Hello!"
```

### Basic API Example

```py
# file1.py
import hoist

client = hoist.Client()
server = client.create_server('localhost', 6000)

schema: dict = {
    'hello': 'hi',
    'hi': 'hello',
    'message', 'response'
}

server.add_auto_return(schema)

@server.received()
def not_found(message):
    return hoist.Error('not found', 404)
```

```py
# file2.py
import hoist

client = hoist.Client()
server = client.find_server('localhost', 6000)

resp = server.send('hi')
print(resp) # prints out "hello"

resp_2 = server.send('a') # raises "hoist.ServerResponseError"
```
