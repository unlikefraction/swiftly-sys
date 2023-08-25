import os
import subprocess
import re

from swiftly.utils.loader import Loader
from swiftly.utils.get import get_config, get_apps
from swiftly.utils.check import is_online
from swiftly.utils.do import add_to_config, add_app
from swiftly.utils.template import render_template
from swiftly.utils.cli import clireturn
from swiftly.core.config import SWIFTLY_PROJECT_LOCATION_VAR

def detect_python():
    """Detect if the current directory is a Python project."""
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.py'):
                return True
    return False

def run_check(arg=""):
    apps = get_apps()
    
    if arg:
        if arg in apps:
            return True
        
        if '.py' in arg:
            return True
    
    return False

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

def init():
    name = get_config("SWIFTLY", "name")
    add_to_config("RUNTIME", "object_oriented", "False")
    
    # Create config.py
    with open("config.py", "w") as f:
        f.write("# configs here 🛠️\n")
    
    # Create requirements.txt
    with open("requirements.txt", "w") as f:
        f.write("")
        
    loader = Loader()
    loader.start("Creating virtual environment")
    
    # Create a virtual environment
    venv_name = f"venv{name}"
    
    python_command = "python3" if os.name == "posix" else "python"
    
    subprocess.run([python_command, "-m", "venv", venv_name])
    loader.end("Virtual environment created")
    
    # Render the .gitignore content
    gitignore_content = render_template("gitignore.txt", {"venv_name": venv_name})
    
    # Merge with existing .gitignore content if it exists
    if os.path.exists(".gitignore"):
        with open(".gitignore", "r") as f:
            existing_content = set(f.readlines())
        
        merged_content = existing_content.union(set(gitignore_content.splitlines(True)))
        gitignore_content = "".join(merged_content)
    
    # Create or update .gitignore file
    with open(".gitignore", "w") as f:
        f.write(gitignore_content)

"""
MAKEAPP
"""

def makeapp(app_name):
    """Create a new app with the given name and set up the necessary files."""
    loader = Loader()
    
    # Split the app_name by '.' to handle nested modules
    parts = app_name.split('.')
    
    # Create directories and files recursively
    current_path = ''
    for index, part in enumerate(parts):
        current_path = os.path.join(current_path, part)
        
        # Create directory if it doesn't exist
        os.makedirs(current_path, exist_ok=True)
        
        # Create __init__.py if it doesn't exist
        init_file = os.path.join(current_path, '__init__.py')
        if not os.path.exists(init_file):
            with open(init_file, 'w') as f:
                f.write(f'from .{part} import *\n\n')
                
        # Create tests.py if it doesn't exist
        init_file = os.path.join(current_path, 'tests.py')
        if not os.path.exists(init_file):
            with open(init_file, 'w') as f:
                f.write(f'from .{part} import *\n\n# May all your tests pass\n')
        
        # If it's the last part of the app_name, create __main__.py and the main app file
        if index == len(parts) - 1:
            main_file = os.path.join(current_path, '__main__.py')
            if not os.path.exists(main_file):
                with open(main_file, 'w') as f:
                    f.write(f"from .{part} import *\n\n# Run and try your code here, use `swiftly run {app_name}` to run the code inside __main__\n")
            
            app_file = os.path.join(current_path, f"{part}.py")
            if not os.path.exists(app_file):
                with open(app_file, 'w') as f:
                    if get_config("RUNTIME", "object_oriented") == "True":
                        f.write(f"class {part.capitalize()}:\n")
                        f.write(f"    def __init__(self):\n")
                        f.write(f"        pass\n\n")
                    else:
                        f.write(f"def {part}():\n")
                        f.write(f"    print('Hello from {part} 👋')\n\n")

"""
MAKEALIVE
"""

def get_gitignore():
    """Return a list of patterns from .gitignore."""
    gitignore_patterns = []
    if os.path.exists('.gitignore'):
        with open('.gitignore', 'r') as f:
            gitignore_patterns = f.read().splitlines()
    return gitignore_patterns

def is_ignored(path, gitignore_patterns):
    """Check if a given path matches any of the .gitignore patterns."""
    for pattern in gitignore_patterns:
        if os.path.basename(path) == pattern:
            return True
    return False

def makealive():
    apps = []
    gitignore_patterns = get_gitignore()
    
    def explore_dir(directory, current_app):
        """Recursively explore directories and build app names."""
        # Skip directories listed in .gitignore
        if is_ignored(directory, gitignore_patterns):
            return

        # Check if the current directory contains any .py files
        if any(fname.endswith('.py') for fname in os.listdir(directory)):
            if current_app:
                app_name = f"{current_app}.{os.path.basename(directory)}"
            else:
                app_name = os.path.basename(directory)
            
            apps.append(app_name)
            
            # Add __init__.py and __main__.py if they don't exist
            init_file = os.path.join(directory, '__init__.py')
            main_file = os.path.join(directory, '__main__.py')
            
            if not os.path.exists(init_file):
                with open(init_file, 'w') as f:
                    f.write('')
            
            if not os.path.exists(main_file):
                with open(main_file, 'w') as f:
                    f.write(f"# Run and try your code here, use `swiftly run {app_name}` to run the code inside __main__\n")
        else:
            app_name = current_app

        # Explore subdirectories
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            if os.path.isdir(item_path):
                explore_dir(item_path, app_name)

    # Start exploring from the current directory
    explore_dir(os.getcwd(), "")

    # Add all apps to config
    for app in apps:
        add_app(app)
        
    init()


"""
RUN
"""

def run_from_base(arg=None):
    """weather to run from SWIFTLY_PROJECT_LOCATION or not"""
    apps = get_apps()
    
    if arg in apps:
        return True
    
    if '.py' in arg:
        return False
    

def run(arg=None):
    """Tell how to run the python script"""
    apps = get_apps()
    
    if arg in apps:
        clireturn(f"-m {arg}")
        return
    
    if '.py' in arg:
        clireturn(arg)
        return


