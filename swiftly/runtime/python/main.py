import os
import subprocess
import platform
import questionary

from swiftly.utils.loader import Loader
from swiftly.utils.get import get_config
from swiftly.utils.do import add_to_config
from swiftly.utils.check import is_using_git
from swiftly.core.config import SWIFTLY_PROJECT_LOCATION_VAR, SWIFTLY_PROJECT_NAME_VAR

def detect_python():
    """Detect if the current directory is a Python project."""
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.py'):
                return True
    return False

def run_command(command, loader, success_message, error_message):
    """Execute a shell command and handle its output with a loader."""
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode == 0:
        loader.end(success_message)
    else:
        loader.end(result.stderr + "\n" + error_message)

def start():
    """Start the project setup by upgrading swiftly-sys, pulling git changes, and installing requirements."""
    loader = Loader()
    
    # Upgrade swiftly-sys
    loader.start("Upgrading swiftly-sys...")
    run_command(["pip", "install", "swiftly-sys", "--upgrade"], loader, "swiftly-sys upgraded successfully!", "Failed to upgrade swiftly-sys!")
    
    # Navigate to project location
    os.chdir(os.environ[SWIFTLY_PROJECT_LOCATION_VAR])
    
    # Pull changes if the project uses git
    if is_using_git():
        loader.start("Pulling changes from git...")
        run_command(["git", "pull"], loader, "Git pull completed!", "Failed to pull changes from git!")
    
    # Determine platform-specific commands
    venv_command = "source" if platform.system() in ["Linux", "Darwin"] else "."
    python_command = "python3" if platform.system() in ["Linux", "Darwin"] else "python"
    
    # Activate virtual environment
    project_name = os.environ[SWIFTLY_PROJECT_NAME_VAR]
    venv_name = f"venv{project_name}"
    subprocess.run([venv_command, f"{venv_name}/bin/activate"])
    
    # Upgrade swiftly-sys inside virtual environment
    loader.start("Upgrading swiftly-sys in virtual environment...")
    run_command([python_command, "-m", "pip", "install", "swiftly-sys", "--upgrade"], loader, "swiftly-sys in virtual environment upgraded successfully!", "Failed to upgrade swiftly-sys in virtual environment!")
    
    # Install project requirements
    if os.path.exists("requirements.txt"):
        loader.start("Installing requirements...")
        run_command([python_command, "-m", "pip", "install", "-r", "requirements.txt"], loader, "Requirements installed successfully!", "Failed to install requirements!")

def init():
    """Initialize the project by creating a virtual environment and setting up the app."""
    os.chdir(os.environ[SWIFTLY_PROJECT_LOCATION_VAR])
    
    # Create virtual environment
    project_name = os.environ[SWIFTLY_PROJECT_NAME_VAR]
    venv_name = f"venv{project_name}"
    python_command = "python3" if platform.system() in ["Linux", "Darwin"] else "python"
    
    loader = Loader()
    loader.start("Creating virtual environment...")
    run_command([python_command, "-m", "venv", venv_name], loader, "Virtual environment created successfully!", "Failed to create virtual environment!")
    
    # Start project setup
    start()
    
    # Check for object-oriented configuration and prompt user if needed
    object_oriented = get_config("CONFIG", "object_oriented")
    if not object_oriented:
        answer = questionary.select("Do you want to use object-oriented programming?", choices=["Yes", "No"]).ask()
        object_oriented = True if answer == "Yes" else False
        add_to_config("CONFIG", "object_oriented", object_oriented)
    
    # Create the main app
    makeapp(project_name)

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
