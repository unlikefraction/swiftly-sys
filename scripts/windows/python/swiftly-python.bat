@echo off
setlocal enabledelayedexpansion

:activate_python
    set project_name=%SWIFTLY_PROJECT_NAME%

    if not exist "venv%project_name%" (
        echo Error: Virtual environment 'venv%project_name%' not found.
        exit /b 1
    )

    call venv%project_name%\Scripts\activate.bat

    python3 -m pip install --upgrade pip >nul 2>&1
    python3 -m pip install swiftly-sys --upgrade >nul 2>&1

    python3 -c "from swiftly.runtime.python.main import install_requirements; install_requirements()"
goto :eof

:deactivate_python
    if "%VIRTUAL_ENV%"=="" (
        echo Error: No virtual environment is currently activated.
        exit /b 1
    )

    call "%VIRTUAL_ENV%\Scripts\deactivate.bat"
goto :eof

:init_python
    python3 -c "from swiftly.runtime.python.main import init; init()"
goto :eof

:run_python
    for /f %%i in ('python3 -c "from swiftly.runtime.python.main import run_from_base; run_from_base('%*')"') do set from_base=%%i

    if "%from_base%"=="True" (
        cd %SWIFTLY_PROJECT_LOCATION%
    )

    python3 -c "from swiftly.runtime.python.main import run; run('%*')"

    :: Assuming you have a read_cli_result.bat function to get the result
    call read_cli_result.bat
    set to_run=!result!
    python3 !to_run!
goto :eof

:makeapp_python
    python3 -c "from swiftly.runtime.python.main import makeapp; makeapp('%1')"
goto :eof

:install_pkg_python
    python3 -m pip install %*
    python3 -c "from swiftly.runtime.python.main import add_to_reqtxt; add_to_reqtxt()"
goto :eof

:uninstall_pkg_python
    python3 -m pip uninstall %*
    python3 -c "from swiftly.runtime.python.main import add_to_reqtxt; add_to_reqtxt()"
goto :eof

:makealive_python
    python3 -c "from swiftly.runtime.python.main import makealive; makealive()"
goto :eof

:: Check if a function exists and call it
if "%1"=="" (
    echo No function specified.
    exit /b 1
)

call :%1 %*
