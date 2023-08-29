@echo off
setlocal enabledelayedexpansion

:add_framework_django
    echo adding django
goto :eof

:run_python_django
    echo running django
goto :eof

:makeapp_python_django
    echo making a django app
goto :eof

:manage_django_commands
    cd %SWIFTLY_PROJECT_LOCATION%
    python3 manage.py %*
goto :eof

:: Check if a function exists and call it
if "%1"=="" (
    echo No function specified.
    exit /b 1
)

call :%1 %*
