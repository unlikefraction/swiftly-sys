add_framework_django(){
    echo "adding django"
}

run_python_django(){
    echo "running django"
}

makeapp_python_django(){
    echo "making a django app"
}

manage_django_commands(){
    cd $SWIFTLY_PROJECT_LOCATION
    python3 manage.py "$@"
}

# Check if a function exists and call it, otherwise call the custom function
if declare -f "$1" > /dev/null; then
    "$@"
fi
