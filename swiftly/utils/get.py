import os
import configparser
import ast
from swiftly.core.config import CONFIG_FILE, SWIFTLY_PROJECT_LOCATION_VAR

def get_config_file_path():
    """
    Determines the path to the config file. If SWIFTLY_PROJECT_LOCATION_VAR is set, 
    it returns the config file path from the project's location. Otherwise, it returns the default CONFIG_FILE path.

    Returns:
    - str: Path to the config file.
    """
    project_location = os.environ.get(f'{SWIFTLY_PROJECT_LOCATION_VAR}')
    if project_location:
        return os.path.join(project_location, CONFIG_FILE)
    return CONFIG_FILE

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
    config.read(get_config_file_path())
    
    try:
        return config[category][key]
    except KeyError:
        return None
    
def get_apps():
    """
    Fetches the apps from the swiftly.config file.

    Returns:
    - list: A list of apps under the 'SWIFTLY' category. Returns [] if not found.
    """
    apps_str = get_config("SWIFTLY", "apps")
    if apps_str:
        return ast.literal_eval(apps_str)
    return []

    
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


def get_all_runtimes():
    """
    Retrieves a list of all available runtimes.

    Returns:
    - list: Names of detected runtimes.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))

    runtime_dir = os.path.join(current_dir, '..', 'runtime')
    runtimes = [d for d in os.listdir(runtime_dir) if os.path.isdir(os.path.join(runtime_dir, d)) and not d.startswith('__')]
    
    return runtimes

def get_all_frameworks(runtime):
    """
    Retrieves a list of all available frameworks for a given runtime.

    Args:
    - runtime (str): The name of the runtime for which the frameworks should be fetched.

    Returns:
    - list: Names of detected frameworks for the specified runtime.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))

    framework_dir = os.path.join(current_dir, '..', 'runtime', runtime, 'frameworks')
    frameworks = [d for d in os.listdir(framework_dir) if os.path.isdir(os.path.join(framework_dir, d)) and not d.startswith('__')]
    
    return frameworks
