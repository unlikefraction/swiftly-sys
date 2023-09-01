@echo off
setlocal enabledelayedexpansion

@call swiftly-utils.bat

:: Check if the first argument is "activate"
if "%~1"=="activate" (
    call :activate
    exit /b 0
)

if "%~1"=="makealive" (
    call :makealive
    exit /b 0
)


:: Define the activate function
:activate
    :: Run check_swiftly from swiftly.core.main.py
    for /f %%i in ('python3 -c "from swiftly.core.main import check_swiftly; check_swiftly()"') do set result=%%i
    echo check_swiftly done successfully

    :: Handle the result
    if "%result%"=="makealive" (
        call :makealive
        exit /b 0
    )

    if "%result%"=="exit" (
        exit /b 0
    )

    if "%result%"=="continue" (
        echo continue
        :: Continue with the rest of the script
        goto :eof
    )

    echo Unexpected result from check_swiftly: %result%
    exit /b 1

    echo handeled the results successfully

    :: Update swiftly
    python3 -c "from swiftly.core.main import update_swiftly; update_swiftly()"
    echo swiftly_updated successfully

    :: Get swiftly project name
    for /f %%i in ('python3 -c "from swiftly.utils.get import get_name; print(get_name())"') do set project_name=%%i
    set SWIFTLY_PROJECT_NAME=%project_name%
    set SWIFTLY_PROJECT_LOCATION=%cd%
    echo get_swiftly_name done successfully

    :: Modify the shell prompt (Note: This might not work as expected in Batch)
    set OLD_PS1=%PROMPT%
    :: git pull
    python3 -c "from swiftly.utils.git import git_pull; git_pull()"
    echo git pull done successfully

    :: Get swiftly project runtime
    for /f %%i in ('python3 -c "from swiftly.utils.get import get_runtime; print(get_runtime())"') do set runtime=%%i
    echo get_runtime done successfully

    :: Source the appropriate script and run the activate function
    call swiftly-%runtime%.bat
    call :activate_%runtime%
    echo called activate_runtime successfully

    :: Modify the prompt (Note: This might not work as expected in Batch)
    set PROMPT=(swiftly %SWIFTLY_PROJECT_NAME%) %OLD_PS1%
    set SWIFTLY_ACTIVATED=true
    echo SWIFTLY_ACTIVATED successfully done successfully
goto :eof

:makealive
    echo makealive running -_-

