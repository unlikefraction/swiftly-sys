add_framework_django(){
    echo "adding django"
}

run_python_django(){
    echo "running django"
}

makeapp_python_django(){
    echo "making a django app"
}

custom() {
    echo "Running python custom function with arguments: $@"
    # Add your custom command handling logic here
}

# Check if a function exists and call it, otherwise call the custom function
if declare -f "$1" > /dev/null; then
    "$@"
else
    # Check if there's more than one argument
    if [ $# -gt 1 ]; then
        custom "${@:2}"  # Pass all arguments except the first one to custom
    fi
fi
