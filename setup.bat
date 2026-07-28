@echo off
setlocal
cd /d "%~dp0"

echo ========================================
echo Work Logger - Windows Setup
echo ========================================
echo.

where py >nul 2>&1
if not errorlevel 1 (
    py -3.12 --version >nul 2>&1
    if not errorlevel 1 (
        set "PYTHON=py -3.12"
    ) else (
        py -3.11 --version >nul 2>&1
        if not errorlevel 1 (
            set "PYTHON=py -3.11"
        ) else (
            py -3.10 --version >nul 2>&1
            if not errorlevel 1 (
                set "PYTHON=py -3.10"
            )
        )
    )
)

if not defined PYTHON (
    where python >nul 2>&1
    if errorlevel 1 (
        echo ERROR: Python 3.10, 3.11, or 3.12 is required.
        echo Install Python 3.12 from https://www.python.org/downloads/windows/
        exit /b 1
    )
    set "PYTHON=python"
)

%PYTHON% --version
if errorlevel 1 (
    echo ERROR: A working Python 3 installation was not found.
    exit /b 1
)

%PYTHON% -c "import sys; raise SystemExit(0 if (3, 10) <= sys.version_info[:2] <= (3, 12) else 1)"
if errorlevel 1 (
    echo ERROR: Work Logger supports Python 3.10, 3.11, or 3.12.
    echo Install Python 3.12, then run setup.bat again.
    exit /b 1
)

if exist ".venv\Scripts\python.exe" (
    ".venv\Scripts\python.exe" -c "import sys; raise SystemExit(0 if (3, 10) <= sys.version_info[:2] <= (3, 12) else 1)"
    if errorlevel 1 (
        echo ERROR: .venv was created with an unsupported Python version.
        echo Delete the .venv folder, then run setup.bat again.
        exit /b 1
    )
)

if not exist ".venv\Scripts\python.exe" (
    echo Creating virtual environment...
    %PYTHON% -m venv .venv
    if errorlevel 1 (
        echo ERROR: Could not create .venv.
        exit /b 1
    )
)

call ".venv\Scripts\activate.bat"
python -m pip install --upgrade pip
if errorlevel 1 exit /b 1

python -m pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies.
    exit /b 1
)

python verify_setup.py
if errorlevel 1 exit /b 1

echo.
echo Setup completed. Start the application with run.bat.
