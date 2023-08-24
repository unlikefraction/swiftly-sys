import os
import subprocess
import re

from swiftly.utils.loader import Loader
from swiftly.utils.get import get_config
from swiftly.utils.check import is_online
from swiftly.core.config import SWIFTLY_PROJECT_LOCATION_VAR

def detect_python():
    """Detect if the current directory is a Python project."""
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.py'):
                return True
    return False

def run_check(arg=None):
    if arg is None:
        return True
    
    if '.py' in arg:
        return True
    else:
        return False

def run_command(command, loader, success_message, error_message):
    """Execute a shell command and handle its output with a loader."""
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode == 0:
        loader.end(success_message)
    else:
        loader.end(result.stderr + "\n" + error_message)

"""
ACTIVATE
"""

def add_to_reqtxt():
    """Add top-level packages to requirements.txt using pipdeptree."""
    os.chdir(os.environ[SWIFTLY_PROJECT_LOCATION_VAR])
    
    try:
        # Use pipdeptree to get packages in freeze format
        result = subprocess.run(["pipdeptree", "--freeze", "--warn", "silence"], capture_output=True, text=True, check=True)
        
        # Filter the output using regex to get top-level packages
        top_level_packages = re.findall(r'^[a-zA-Z0-9\-]+', result.stdout, re.MULTILINE)
        
        # Write top-level packages to requirements.txt
        with open("requirements.txt", "w") as f:
            for package in top_level_packages:
                f.write(f"{package}\n")
                
    except subprocess.CalledProcessError:
        print("Failed to generate requirements.txt using pipdeptree.")


def install_requirements():
    """Install requirements from requirements.txt."""
    os.chdir(os.environ[SWIFTLY_PROJECT_LOCATION_VAR])
    
    # Check if requirements.txt exists, if not, create it
    if not os.path.exists("requirements.txt"):
        with open("requirements.txt", "w") as f:
            pass  # Just create an empty file
    
    if not is_online():
        print("You are not online. Please check your internet connection and try again.")
        return
    
    loader = Loader()
    
    # Determine the appropriate python command based on the platform
    python_command = "python3" if os.name == "posix" else "python"
    
    loader.start("Installing requirements")
    
    # Install requirements from requirements.txt
    try:
        subprocess.run([python_command, "-m", "pip", "install", "-r", "requirements.txt"], check=True, stdout=subprocess.PIPE)
        loader.end("Requirements installed successfully!")
    except subprocess.CalledProcessError:
        loader.end("Failed to install requirements!", failed=True)
        return
    
    # Update requirements.txt with top-level packages
    add_to_reqtxt()

"""
INIT
"""

# def init():
#     """Initialize the project by creating a virtual environment and setting up the app."""
#     os.chdir(os.environ[SWIFTLY_PROJECT_LOCATION_VAR])
    
#     # Create virtual environment
#     project_name = os.environ[SWIFTLY_PROJECT_NAME_VAR]
#     venv_name = f"venv{project_name}"
#     python_command = "python3" if platform.system() in ["Linux", "Darwin"] else "python"
    
#     loader = Loader()
#     loader.start("Creating virtual environment...")
#     run_command([python_command, "-m", "venv", venv_name], loader, "Virtual environment created successfully!", "Failed to create virtual environment!")
    
#     # Check for object-oriented configuration and prompt user if needed
#     object_oriented = get_config("CONFIG", "object_oriented")
#     if not object_oriented:
#         answer = questionary.select("Do you want to use object-oriented programming?", choices=["Yes", "No"]).ask()
#         object_oriented = True if answer == "Yes" else False
#         add_to_config("CONFIG", "object_oriented", object_oriented)
    
#     # Create the main app
#     makeapp(project_name)

def makeapp(app_name):
    """Create a new app with the given name and set up the necessary files."""
    os.makedirs(app_name, exist_ok=True)
    
    # Create __init__.py
    with open(f"{app_name}/__init__.py", "w") as f:
        f.write(f"from .{app_name} import *\n\n")
    
    # Create __main__.py
    with open(f"{app_name}/__main__.py", "w") as f:
        f.write(f"from .{app_name} import *\n\n# Run and try your code here, use `swiftly run {app_name}` to run the code inside __main__\n")
    
    # Create the main app file
    with open(f"{app_name}/{app_name}.py", "w") as f:
        if get_config("CONFIG", "object_oriented") == "True":
            f.write(f"class {app_name.capitalize()}:\n    pass\n")
        else:
            f.write(f"def {app_name}")

def makealive():
    print("running makealive for python")
    pass