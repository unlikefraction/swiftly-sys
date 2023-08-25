import os
import sys
import subprocess
import re

import questionary
from questionary import Choice
import importlib

from swiftly.utils.loader import Loader
from swiftly.utils.get import get_config, get_frameworks, get_runtime, get_all_frameworks, get_all_runtimes
from swiftly.utils.cli import clireturn
from swiftly.utils.do import add_to_config, add_framework, add_runtime, add_app
from swiftly.utils.check import is_swiftly, is_online, is_using_git
from swiftly.core.config import SWIFTLY_PROJECT_LOCATION_VAR, SWIFTLY_PROJECT_NAME_VAR, CONFIG_FILE

"""
ACTIVATE:
"""

def check_swiftly():
    """check if it's swiftly project, and tell what to do next"""
    if not is_swiftly():
        answer = questionary.confirm("This is not a swiftly project. Do you want to convert it to a swiftly project?").ask()
        if answer:
            clireturn("makealive")
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

def get_git_name(link):
    # Regular expression to match the repository name in a git URL
    pattern = r".*/(.+?)\.git$"
    match = re.search(pattern, link)
    return match.group(1) if match else None


def validate_project_name(name):
    """Validate the project name."""
    if len(name) <= 1:
        return "Name should be at least 2 characters long."
    if not re.match(r'^[a-zA-Z0-9_]+$', name):
        return "Name can only contain letters, numbers, and underscores."
    return True

def init(name=None, runtime=None, frameworks=[], inPlace=False):
    """Initialize the project."""
    # Get or confirm project name
    name = questionary.text(
        "Swiftly project name:",
        default=name if name else "",
        validate=validate_project_name
    ).ask()

    # Get the directory of the currently executing file
    current_dir = os.getcwd()  # Get the current working directory of the user
    
    # If runtime is not specified, ask the user. Otherwise, use the provided runtime.
    if not runtime:
        runtimes = get_all_runtimes()
        runtime = questionary.select(
            "Choose a runtime:",
            choices=runtimes
        ).ask()

    # Even if frameworks are specified, always confirm with the user.
    available_frameworks = get_all_frameworks(runtime)
    
    # Filter the frameworks to only include those that are in available_frameworks
    valid_frameworks = [f for f in (frameworks) if f in available_frameworks]
    
    frameworks = questionary.checkbox(
        "Select frameworks (choose one or more, or none):",
        choices=[Choice(f, checked=(f in valid_frameworks)) for f in available_frameworks],
    ).ask()

    if not inPlace:
        # Create a directory with the usable name in the user's current directory
        project_dir = os.path.join(current_dir, name)
        os.makedirs(project_dir, exist_ok=True)

        # Navigate inside the new directory
        os.chdir(project_dir)
    else:
        # If inPlace is True, simply set the project_dir to the current_dir
        project_dir = current_dir

    # Add configurations inside the new directory's config file
    add_to_config('SWIFTLY', 'name', name)
    add_runtime(runtime)
    for framework in frameworks:
        add_framework(framework)
        
    clireturn(f"{name}<=====>" + ",".join([runtime] + [framework for framework in frameworks]))


"""
MAKEAPP
"""

def validate_app_name(name):
    """Validate the project name."""
    if len(name) <= 1:
        return "Name should be at least 2 characters long."
    if not re.match(r'^[a-zA-Z0-9_.]+$', name):
        return "Name can only contain letters, numbers, and underscores."
    return True

def makeapp(name=None, confirmed=False):
    """Create a new app."""
    # Get runtime and frameworks
    runtime_name = get_runtime()
    frameworks = get_frameworks()
    
    if not runtime_name:
        raise RuntimeError("No runtime found")

    execute = [runtime_name]

    # For each framework, get the FRAMEWORK_CONFIG
    for framework in frameworks:
        module_name = f"swiftly.runtime.{runtime_name}.frameworks.{framework}.config"
        config_module = importlib.import_module(module_name)
        FRAMEWORK_CONFIG = getattr(config_module, "FRAMEWORK_CONFIG", None)

        if FRAMEWORK_CONFIG and "makeapp" in FRAMEWORK_CONFIG.get("framework_commands", []):
            execute.append(framework)
            
    # Ask for app name if not provided or confirm if provided
    if not confirmed:
        if name:
            name = questionary.text("Confirm or modify the app name:", default=name, validate=validate_app_name).ask()
        else:
            name = questionary.text("Enter the name of the app:", validate=validate_app_name).ask()

    executionList = []

    # Depending on the size of the execute list, prompt user accordingly
        # Depending on the size of the execute list, prompt user accordingly
    choices = ["run makeapp", "customize makeapp"]
    
    if len(execute) > 1:
        if not confirmed:
            choice = questionary.select(
                "How to execute:",
                choices=choices
            ).ask()
        else:
            choice = choices[0]

        if choice == choices[0]:
            executionList.extend(execute)
        elif choice == choices[1]:
            # Ensure at least one option is selected
            while True:
                custom_choices = questionary.checkbox(
                    "Select what to makeapp with:",
                    choices=execute,
                    validate=lambda x: True if len(x) > 0 else "You must select at least one option!"
                ).ask()
                if custom_choices:
                    break
            executionList.extend(custom_choices)
    else:
        executionList.append(execute[0])

    # Print the final execution list
    clireturn(f"{name}<=====>" + ",".join(executionList))


def install():
    """Install the necessary dependencies."""
    # Logic for installing dependencies goes here
    pass

def uninstall():
    """Uninstall the project."""
    # Logic for uninstalling the project goes here
    pass

def run(arg=None):
    """Run the project."""
    # Get runtime and frameworks
    runtime_name = get_runtime()
    frameworks = get_frameworks()

    run = []

    # Check if "run" is supported by the runtime
    runtime_module_name = f"swiftly.runtime.{runtime_name}.config"
    runtime_config_module = importlib.import_module(runtime_module_name)
    RUNTIME_CONFIG = getattr(runtime_config_module, "RUNTIME_CONFIG", None)

    if RUNTIME_CONFIG:
        run_check_function = RUNTIME_CONFIG.get("run_check")
        if run_check_function and run_check_function(arg):
            run.append(runtime_name)

    # Check if "run" is in each framework's config
    for framework in frameworks:
        module_name = f"swiftly.runtime.{runtime_name}.frameworks.{framework}.config"
        config_module = importlib.import_module(module_name)
        FRAMEWORK_CONFIG = getattr(config_module, "FRAMEWORK_CONFIG", None)

        if FRAMEWORK_CONFIG and "run" in FRAMEWORK_CONFIG.get("framework_commands", []):
            run_check_function = FRAMEWORK_CONFIG.get("run_check")
            if run_check_function and run_check_function(arg):
                run.append(framework)

    # If the run list has more than one item, ask the user which runtime/framework they want to use
    if len(run) > 1:
        choice = questionary.select(
            "What do you wanna run your code with:",
            choices=run
        ).ask()
    else:
        choice = run[0] if run else None
        
    if choice == None:
        clireturn("exit")
        return

    # Format the choice to return as runtime or runtime-framework
    clireturn(choice if choice == runtime_name else f"{runtime_name}-{choice}")
    
def makealive():
    detected_runtimes = []
    frameworks = []
    project_name = ''
    
    def get_current_directory_name():
        current_path = os.getcwd()
        dir_name = os.path.basename(current_path)
        return dir_name.replace("-", "_").replace(" ", "_")
        
    project_name = get_current_directory_name()

    # Get all available runtimes
    available_runtimes = get_all_runtimes()

    # Detect runtimes
    for potential_runtime in available_runtimes:
        runtime_config_module = importlib.import_module(f'swiftly.runtime.{potential_runtime}.config')
        RUNTIME_CONFIG = getattr(runtime_config_module, 'RUNTIME_CONFIG', {})
        detect_function = RUNTIME_CONFIG.get('detect')
        if detect_function:
            detect_result = detect_function()
            if detect_result:
                detected_runtimes.append(potential_runtime)

    # If multiple runtimes are detected, ask user to choose one
    if len(detected_runtimes) > 1:
        runtime = questionary.select(
            "Multiple runtimes detected. Please choose one:",
            choices=detected_runtimes
        ).ask()
    elif len(detected_runtimes) == 1:
        # Confirm the detected runtime with the user
        confirmed = questionary.confirm(f"Detected runtime: {detected_runtimes[0]}. Do you want to use this runtime?").ask()
        if confirmed:
            runtime = detected_runtimes[0]
        else:
            return None  # or handle this scenario differently
    else:
        print("No runtime detected.")
        return

    # After getting a runtime, detect the frameworks
    available_frameworks = get_all_frameworks(runtime)
    for potential_framework in available_frameworks:
        framework_config_module = importlib.import_module(f'swiftly.runtime.{runtime}.frameworks.{potential_framework}.config')
        FRAMEWORK_CONFIG = getattr(framework_config_module, 'FRAMEWORK_CONFIG', {})
        detect_function = FRAMEWORK_CONFIG.get('detect')
        if detect_function:
            detect_result = detect_function()
            if detect_result:
                frameworks.append(potential_framework)

    init(project_name, runtime, frameworks, inPlace=True)  # Use 'runtime' here instead of 'detected_runtimes'


def add_new_framework(name=None):
    """Add a new framework to the project."""
    
    runtime = get_runtime()
    all_available_frameworks = get_all_frameworks(runtime)
    
    # Check if the provided name is a valid framework
    if name and name in all_available_frameworks:
        clireturn(name)
        return
    
    print(f"The framework '{name}' was not found.")
    show_all = questionary.confirm("Do you want to see all available frameworks?").ask()
    if not show_all:
        clireturn("exit")
        return

    # Ask the user to select a framework
    selected_framework = questionary.select(
        "Select which framework to use:",
        choices=all_available_frameworks
    ).ask()
    
    if selected_framework:
        clireturn(selected_framework)
    else:
        clireturn("exit")
        

def custom(command):
    """Handle custom operations."""
    runtime  = get_runtime()
    frameworks = get_frameworks()
    
    possible_executors = []

    # Get RUNTIME_CONFIG dict from swiftly.runtime.{runtime}.config.py
    runtime_config_module = importlib.import_module(f'swiftly.runtime.{runtime}.config')
    RUNTIME_CONFIG = getattr(runtime_config_module, 'RUNTIME_CONFIG', {})
    custom_runtime_commands = RUNTIME_CONFIG.get('custom', {})
    if command in custom_runtime_commands:
        possible_executors.append((runtime, custom_runtime_commands[command]))

    # For all frameworks in frameworks
    for framework in frameworks:
        # Get FRAMEWORK_CONFIG from swiftly.runtime.{runtime}.frameworks.{framework}.config.py
        framework_config_module = importlib.import_module(f'swiftly.runtime.{runtime}.frameworks.{framework}.config')
        FRAMEWORK_CONFIG = getattr(framework_config_module, 'FRAMEWORK_CONFIG', {})
        custom_framework_commands = FRAMEWORK_CONFIG.get('custom', {})
        if command in custom_framework_commands:
            possible_executors.append((f"{runtime}-{framework}", custom_framework_commands[command]))

    # If there are multiple possible executors, ask the user to choose one
    if len(possible_executors) > 1:
        choices = [executor[0].split('-')[1] if '-' in executor[0] else executor[0] for executor in possible_executors]
        selected_executor = questionary.select(
            "Multiple executors detected. Please choose one:",
            choices=choices
        ).ask()
    elif possible_executors:
        selected_executor = possible_executors[0][0]
    else:
        print(f"umm... what? 🤨: {command}")
        clireturn("exit")
        return
    
    selected_executor = selected_executor if selected_executor == runtime else f"{runtime}-{selected_executor}" if "-" not in selected_executor else selected_executor
    for executor in possible_executors:
        if executor[0] == selected_executor:
            selected_executor_command = executor[1]
    clireturn(f"{selected_executor}<=====>{selected_executor_command}")
