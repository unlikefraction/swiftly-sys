from swiftly.runtime.python.main import detect_python

RUNTIME_CONFIG = {
    "name": "python",
    
    # function to run from shell / bat script
    "init": "init",
    "start": "start",
    "run": "run",
    "makeapp": "makeapp",
    "install": "install",
    "uninstall": "uninstall",
    
    # a python function that detects if runtime is the current runtime (in this case, detect if it's a python runtime)
    "detect": detect_python,
    
    # a list of custom functions. "command": "shell/bat function name"
    "custom": [],
    
    # Allowed framework types, and it's configuration
    "allowed_framework_types": [
        {
            "name": "web",
            "exclusive": True, # only one of a kind in every project
            "allow_override": ["run"],
        },
        
        {
            "name": "ai",
            "exclusive": False,
            "allow_override": ["run", "makeapp"],
        },
        
        {
            "name": "others",
            "exclusive": False,
            "allow_override": ["run", "makeapp"],
        },
    ]
}