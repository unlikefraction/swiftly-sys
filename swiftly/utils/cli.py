import os
import tempfile

def clireturn(value):
    """Write a value to a temporary file for CLI scripts to read."""
    temp_dir = tempfile.gettempdir()
    result_file_path = os.path.join(temp_dir, 'swiftly_cli_result.txt')
    
    with open(result_file_path, 'w') as f:
        f.write(value)
