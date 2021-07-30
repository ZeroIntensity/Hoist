import socket
from .get_host import get_host

def get_ip() -> str:
    """Function for getting the IP address of the current machine."""
    un = get_host()
    ip: str = socket.gethostbyname(un)

    return ip