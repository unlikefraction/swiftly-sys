import os
import socket
import re

from swiftly.core.config import CONFIG_FILE

def is_swiftly():
    """
    Checks if 'swiftly.config' is in the current directory and if the file is not empty.
    Returns True if both conditions are met, else returns False.
    """
    if os.path.exists(CONFIG_FILE) and os.path.getsize(CONFIG_FILE) > 0:
        return True
    return False

def is_empty_dir():
    """
    Checks if the current directory is empty.
    Returns True if the directory is empty, else returns False.
    """
    return not bool(os.listdir('.'))

def is_using_git():
    """
    Checks if the current directory is a git repository.
    Returns True if it's a git repository, else returns False.
    """
    return os.path.isdir('.git')

def is_online():
    """
    Checks if the user is connected to the internet or not... on the assumption that all these services won't go down all at once 😂
    Returns True if connected, else returns False.
    """
    hosts = ["www.google.com", "www.amazon.com", "www.microsoft.com", "www.github.com"]
    for host in hosts:
        try:
            # connect to the host -- tells us if the host is actually reachable
            socket.create_connection((host, 80))
            return True
        except OSError:
            pass
    return False

def is_git_url(link):
    # Regular expression to match general git URLs
    pattern = r"^(https?://|git@|git://).+\.git$"
    return bool(re.match(pattern, link))
