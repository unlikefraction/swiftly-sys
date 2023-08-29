@echo off

REM Check and remove dist directory
if exist dist rmdir /s /q dist

REM Check and remove build directory
if exist build rmdir /s /q build

REM Check and remove swiftly_windows.egg-info file
if exist swiftly_windows.egg-info del /q swiftly_windows.egg-info

REM Build the package
python setup.py sdist bdist_wheel

REM Upload the package using twine
twine upload dist\*
