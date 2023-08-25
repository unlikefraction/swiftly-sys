from swiftly.runtime.python.main import detect_python, run_check

RUNTIME_CONFIG = {
    "name": "python",
    
    # a python function that detects if runtime is the current runtime (in this case, detect if it's a python runtime)
    "detect": detect_python,
    
    # a list of custom functions. "command": "shell/bat function name"
    "custom": {},
    
    "run_check": run_check,
    
    # Allowed framework types, and it's configuration
    "allowed_framework_types": [
        {
            "name": "web",
            "exclusive": True, # only one of a kind in every project
        },
        
        {
            "name": "ai",
            "exclusive": False,
        },
        
        {
            "name": "others",
            "exclusive": False,
        },
    ]
}