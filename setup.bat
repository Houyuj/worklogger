@echo off
echo ========================================
echo Work Logger - First Time Setup
echo ========================================
echo.
echo This will create conda environment and install dependencies...
echo.

conda --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Conda is not installed or not in PATH
    echo Please install Anaconda or Miniconda from:
    echo https://docs.conda.io/en/latest/miniconda.html
    pause
    exit /b 1
)

echo Creating conda environment 'worklogger'...
conda env create -f environment.yml

if errorlevel 1 (
    echo.
    echo ERROR: Failed to create environment
    echo If environment already exists, run: conda env update -f environment.yml
    pause
    exit /b 1
)

echo.
echo ========================================
echo Setup completed successfully!
echo ========================================
echo.
echo Conda environment 'worklogger' has been created.
echo.
echo You can now run the application using:
echo   - run.bat (Windows)
echo   - ./run.sh (Linux/Mac)
echo.
pause
