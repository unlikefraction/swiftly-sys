#!/bin/bash

activate_python() {
    # Get the project name from the environment variable
    local project_name="$SWIFTLY_PROJECT_NAME"

    # Check if the virtual environment exists
    if [[ ! -d "venv${project_name}" ]]; then
        echo "Error: Virtual environment 'venv${project_name}' not found."
        return 1
    fi

    # Source the virtual environment's activate script
    source venv${project_name}/bin/activate

    # install and keep swiftly up-to-date
    python3 -m pip install --upgrade pip > /dev/null 2>&1
    python3 -m pip install swiftly-sys --upgrade > /dev/null 2>&1

    # Install the requirements using the Python function
    python3 -c "from swiftly.runtime.python.main import install_requirements; install_requirements()"
}

deactivate_python() {
    # Check if the virtual environment is activated
    if [[ -z "$VIRTUAL_ENV" ]]; then
        echo "Error: No virtual environment is currently activated."
        return 1
    fi

    # Source the activate file to get the deactivate function
    source "./venv${SWIFTLY_PROJECT_NAME}/bin/activate"

    # Call the deactivate function from the activate file
    deactivate
}

init_python(){
    python3 -c "from swiftly.runtime.python.main import init; init()"
}

run_python(){
    from_base=$(python3 -c "from swiftly.runtime.python.main import run_from_base; run_from_base('$@')")

    # Check if changing base is needed
    if [[ "$from_base" == "True" ]]; then
        cd $SWIFTLY_PROJECT_LOCATION
    fi

    python3 -c "from swiftly.runtime.python.main import run; run('$@')"

    local to_run="$(read_cli_result)"
    python3 $to_run
}

makeapp_python(){
    python3 -c "from swiftly.runtime.python.main import makeapp; makeapp('$1')"
}

install_pkg_python(){
    python3 -m pip install "$@"
    python3 -c "from swiftly.runtime.python.main import add_to_reqtxt; add_to_reqtxt()"
}

uninstall_pkg_python(){
    python3 -m pip uninstall "$@"
    python3 -c "from swiftly.runtime.python.main import add_to_reqtxt; add_to_reqtxt()"
}

makealive_python(){
    python3 -c "from swiftly.runtime.python.main import makealive; makealive()"
}

# Check if a function exists and call it, otherwise call the custom function
if declare -f "$1" > /dev/null; then
    "$@"
fi
