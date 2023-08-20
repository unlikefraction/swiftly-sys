import os
import subprocess

import questionary

from swiftly.utils.loader import Loader
from swiftly.utils.get import get_config
from swiftly.utils.cli import clireturn
from swiftly.utils.do import add_to_config
from swiftly.utils.check import is_swiftly, is_online, is_using_git
from swiftly.core.config import SWIFTLY_PROJECT_LOCATION_VAR, SWIFTLY_PROJECT_NAME_VAR

"""
ACTIVATE:
"""

def check_swiftly():
    """check if it's swiftly project, and tell what to do next"""
    if not is_swiftly():
        answer = questionary.confirm("This is not a swiftly project. Do you want to convert it to a swiftly project?").ask()
        if answer:
            clireturn("init")
        else:
            clireturn("exit")
    else:
        clireturn("continue")

        
def update_swiftly(show_load=True):
    """Update and install the latest version of swiftly-sys."""
    if not is_online():
        return
    
    loader = Loader()
    
    # Determine the appropriate python command based on the platform
    python_command = "python3" if os.name == "posix" else "python"
    
    # Start the loader with a message
    if show_load:
        loader.start("Checking swiftly")
    
    try:
        # Execute pip install to update swiftly-sys and check for errors
        subprocess.run([python_command, "-m", "pip", "install", "swiftly-sys", "--upgrade", "--break-system-packages"], check=True, stdout=subprocess.PIPE)
        if show_load:
            loader.end("Checked swiftly")
        
    except subprocess.CalledProcessError:
        if show_load:
            loader.end("Failed to update swiftly", failed=True)


"""
INIT
"""

def init():
    """Initialize the project."""
    # Check if it's a swiftly project
    pass


"""
MAKEAPP
"""

def makeapp():
    """Create a new app."""
    # get_runtime
    # get frameworks
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
