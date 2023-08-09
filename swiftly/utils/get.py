import configparser
import ast
from swiftly.core.config import CONFIG_FILE

def get_config(category, key):
    """
    Fetches the value of a key under a specified category from the 'config.ini' file.
    
    Args:
    - category (str): The category (or section) in the INI file.
    - key (str): The key whose value needs to be fetched.

    Returns:
    - str: The value of the specified key under the given category. Returns None if not found.
    """
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    
    try:
        return config[category][key]
    except KeyError:
        return None
    
def get_name():
    """
    Fetches the runtime name from swiftly.config file.

    Returns:
    - str: The value of the 'name' key under the 'SWIFTLY' category. Returns None if not found.
    """
    return get_config("SWIFTLY", "name")

def get_runtime():
    """
    Fetches the runtime name from swiftly.config file.

    Returns:
    - str: The value of the 'name' key under the 'RUNTIME' category. Returns None if not found.
    """
    return get_config("RUNTIME", "name")

def get_frameworks():
    """
    Fetches the frameworks from the swiftly.config file.

    Returns:
    - list: A list of frameworks under the 'RUNTIME' category. Returns None if not found.
    """
    frameworks_str = get_config("RUNTIME", "frameworks")
    if frameworks_str:
        return ast.literal_eval(frameworks_str)
    return []
