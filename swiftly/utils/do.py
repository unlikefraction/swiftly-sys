import configparser
import os
from swiftly.core.config import CONFIG_FILE
from swiftly.utils.get import get_frameworks

def add_to_config(category, key, value):
    """
    Adds or updates a key-value pair under a specified category in the configuration file.
    
    Args:
    - category (str): The category (or section) in the INI file.
    - key (str): The key to be added or updated.
    - value (str or list): The value to be set for the key.
    """
    config = configparser.ConfigParser()

    # Check if CONFIG_FILE exists, if not, create it
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'w') as f:
            pass  # Just create the file

    config.read(CONFIG_FILE)
    
    if not config.has_section(category):
        config.add_section(category)
    
    if isinstance(value, list):
        config[category][key] = str(value)
    else:
        config[category][key] = value
    
    with open(CONFIG_FILE, 'w') as configfile:
        config.write(configfile)

def add_runtime(name):
    """
    Adds a runtime name to the configuration file and initializes an empty framework list.
    
    Args:
    - name (str): The runtime name to be added.
    """
    add_to_config("RUNTIME", "name", name)
    add_to_config("RUNTIME", "frameworks", "[]")
    
def add_app(name):
    """
    Adds an app to the list of apps in the configuration file.
    
    Args:
    - name (str): The app name to be added.
    """
    apps = get_frameworks()
    if name not in apps:
        apps.append(name)
    add_to_config("SWIFTLY", "apps", apps)

def add_framework(name):
    """
    Adds a framework to the list of frameworks in the configuration file.
    
    Args:
    - name (str): The framework name to be added.
    """
    frameworks = get_frameworks()
    if name not in frameworks:
        frameworks.append(name)
    add_to_config("RUNTIME", "frameworks", frameworks)

def remove_from_config(category, key):
    """
    Removes a key from a specified category in the configuration file.
    
    Args:
    - category (str): The category (or section) in the INI file.
    - key (str): The key to be removed.
    """
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    
    if config.has_section(category) and key in config[category]:
        config[category].pop(key)
    
    with open(CONFIG_FILE, 'w') as configfile:
        config.write(configfile)

def remove_framework(name):
    """
    Removes a framework from the list of frameworks in the configuration file.
    
    Args:
    - name (str): The framework name to be removed.
    """
    frameworks = get_frameworks()
    if name in frameworks:
        frameworks.remove(name)
    add_to_config("RUNTIME", "frameworks", frameworks)
