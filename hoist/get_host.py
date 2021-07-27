import socket

def get_host() -> str:
    """Function for getting the host name."""
    un: str = socket.gethostname()
    return un