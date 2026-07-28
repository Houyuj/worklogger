@echo off
setlocal
title Work Logger Application
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo ERROR: The local environment has not been set up.
    echo Run setup.bat first.
    exit /b 1
)

call ".venv\Scripts\activate.bat"
echo Starting Work Logger Application...
python launcher.py
set "EXIT_CODE=%ERRORLEVEL%"
call deactivate
exit /b %EXIT_CODE%
