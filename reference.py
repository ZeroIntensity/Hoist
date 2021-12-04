import inspect
from hoist import *
from typing import get_type_hints, Any

objects: list = [Route, Server, Message, Response]
functions = [create_server]

resp: str = '# Reference'

def get_hint(value: Any) -> str:
    return value.__name__ if hasattr(value, "__name__") else value

def get_default_args(func):
    signature = inspect.signature(func)
    return {
        k: v.default
        for k, v in signature.parameters.items()
        if v.default is not inspect.Parameter.empty
    }



for i in objects:
    resp += f'\n## {i.__name__}\n**{i.__doc__}**\n'

    for x in dir(i):
        if x.startswith('_') and not x == '__init__':
            continue

        attr = getattr(i, x)
        c = callable(attr)

        resp += f'### {attr.__name__ if c else x}\n'

        if c:
            hints: dict = get_type_hints(attr)
            defaults: dict = get_default_args(attr)
            doc: str = attr.__doc__
            desc: str = doc.split('\n')[0]
            example = ' '.join(doc[doc.find('example '):].split(' ')[1:])
            resp += f'`#!python {attr.__name__}{inspect.signature(attr)}`\n\n**{desc}**\n\n**Returns:** `#!python {get_hint(hints["return"])}`\n'

            if not list(hints.keys()) == ['return']:
                resp += '#### Parameters\n| Name | Type | Description | Default |\n| ----------- | ----------- | ----------- | ----------- |\n'

            for key, value in hints.items():
                if key == 'return':
                    continue
                search: str = f'{key}: '
                find = doc.find(search)
                index = find + len(search)

                find_2 = doc[index:].find('\n')
                description: str = doc[index:find_2 + index]

                if description.startswith('property'):
                    description: str = getattr(i, description.split(' ')[1]).__doc__

                resp += f'| {key} | `#!python {get_hint(value)}` | {description} | {"Required" if key not in defaults else f"`#!python {repr(defaults[key])}`"} |\n'
            
            ex: str = "#### Example\n" + example if example else ""
            resp += f'\n\n{ex}'
        else:
            resp += f'\n**{attr.__doc__}**\n\n**Type:** `#!python {get_hint(get_type_hints(attr.fget)["return"])}`\n\n'

with open('./docs/reference.md', 'w') as f:
    f.write(resp)

