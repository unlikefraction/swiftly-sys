#!/bin/bash

read_cli_result() {
    # Get the system's temporary directory using Python
    local temp_dir=$(python3 -c "import tempfile; print(tempfile.gettempdir())")

    local result_file_path="${temp_dir}/swiftly_cli_result.txt"
    
    # Check if the result file exists
    if [[ ! -f "$result_file_path" ]]; then
        echo "Error: Result file not found!"
        return 1
    fi
    
    # Read the result
    local result=$(cat "$result_file_path")
    
    # Remove the temporary file
    rm "$result_file_path"
    
    # Return the result
    echo "$result"
}

is_sourced() {
    [[ $- == *i* ]]
}