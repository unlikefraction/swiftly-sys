import os
import subprocess

from swiftly.utils.loader import Loader
from swiftly.utils.check import is_using_git
from swiftly.core.config import SWIFTLY_PROJECT_LOCATION_VAR

def git_pull():
    """Pull changes from git for the active swiftly project."""
    loader = Loader()
    
    # Navigate to swiftly project location
    os.chdir(os.environ[SWIFTLY_PROJECT_LOCATION_VAR])
    
    # Check if the project uses git
    if not is_using_git():
        return
    
    # Start the loader with a message
    loader.start("Pulling changes from git...")
    
    try:
        # Execute git pull and check for errors
        subprocess.run(["git", "pull"], check=True)
        loader.end("Git pull completed successfully!")
        
    except subprocess.CalledProcessError:
        loader.end("Failed to pull changes from git!", failed=True)
