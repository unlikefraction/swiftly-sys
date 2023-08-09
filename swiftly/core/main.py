import subprocess

import questionary

from swiftly.utils.loader import Loader
from swiftly.utils.get import get_config
from swiftly.utils.do import add_to_config
from swiftly.utils.check import is_swiftly, is_online, is_using_git
from swiftly.core.config import SWIFTLY_PROJECT_LOCATION_VAR, SWIFTLY_PROJECT_NAME_VAR

"""
ACTIVATE:

PART 1: 
"""

def check_swiftly():
    """check if it's swiftly project, and tell what to do next"""
    
    if not is_swiftly():
        answer = questionary.confirm("This is not a swiftly project. Do you want to convert it to a swiftly project?").ask()
        if answer:
            return "init"
        else:
            return "exit"

    return "continue"

def activate():
    """Start the project setup."""
    loader = Loader()
    # Fetch runtime and frameworks from config
    runtime = get_config("CONFIG", "runtime")
    frameworks = get_config("CONFIG", "frameworks")
    
    # Pull changes if the project uses git
    if is_using_git():
        loader.start("Pulling changes from git...")
        try:
            subprocess.run(["git", "pull"], check=True)
            loader.end("Git pull completed!")
        except subprocess.CalledProcessError:
            loader.end("✗", "Failed to pull changes from git!", failed=True)
            
"""
INIT
"""

def init():
    """Initialize the project."""
    # Check if it's a swiftly project
    if is_swiftly():
        activate()
    else:
        print("This is not a swiftly project. Please convert it first.")
        
def makeapp():
    """Create a new app."""
    # Logic for creating a new app goes here
    pass

def install():
    """Install the necessary dependencies."""
    # Logic for installing dependencies goes here
    pass

def uninstall():
    """Uninstall the project."""
    # Logic for uninstalling the project goes here
    pass

def run():
    """Run the project."""
    # Logic for running the project goes here
    pass

def add_framework():
    """Add a new framework to the project."""
    # Logic for adding a new framework goes here
    pass

def custom():
    """Handle custom operations."""
    # Logic for custom operations goes here
    pass
