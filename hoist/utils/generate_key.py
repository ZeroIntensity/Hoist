import random, string
from typing import Union

def generate_key(length: int = 100, letters: list = string.ascii_letters, is_list: bool = False, list_length: int = 1) -> Union[str, list]:
    """Generate a random key that can be used for authentication."""
    if not is_list:
        return ''.join(random.choice(letters) for i in range(length))
    else:
        resp: list = []

        for i in range(list_length):
            text: str = ''.join(random.choice(letters) for x in range(length))
            resp.append(text)
        
        return resp
