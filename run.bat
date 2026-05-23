@echo off
title Work Logger Application

conda --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Conda is not installed or not in PATH
    echo Please install Anaconda or Miniconda
    pause
    exit /b 1
)

echo Activating conda environment 'worklogger'...
call conda activate worklogger

if errorlevel 1 (
    echo.
    echo ERROR: Environment 'worklogger' not found
    echo Please run setup.bat first to create the environment
    pause
    exit /b 1
)

echo Starting Work Logger Application...
python launcher.py

call conda deactivate

if errorlevel 1 (
    echo.
    echo Application closed with an error.
    pause
)
