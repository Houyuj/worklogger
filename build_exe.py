"""
Build script to create standalone executable
Run: python build_exe.py
"""

import os
import sys
import subprocess
from pathlib import Path

def build_executable():
    """Build standalone executable using PyInstaller"""

    print("Building Work Logger executable...")
    print("This may take a few minutes...\n")

    # Check if PyInstaller is installed
    try:
        import PyInstaller
    except ImportError:
        print("PyInstaller not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

    project_root = Path(__file__).parent
    frontend_data = f"frontend{os.pathsep}frontend"

    # PyInstaller uses ';' on Windows and ':' on POSIX for --add-data.
    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--name=WorkLogger",
        "--onefile",
        "--windowed",  # No console window
        "--add-data",
        frontend_data,
        "--noconfirm",
        "--clean",
        "launcher.py"
    ]

    # Run PyInstaller
    try:
        subprocess.check_call(cmd, cwd=project_root)
        print("\n" + "="*60)
        print("Build completed successfully!")
        print("="*60)
        print("\nExecutable location: dist/WorkLogger.exe")
        print("\nTo distribute:")
        print("1. Copy dist/WorkLogger.exe to the target Windows computer")
        print("2. Users can run WorkLogger.exe directly")
        print("\nApplication data is stored in %LOCALAPPDATA%\\WorkLogger\\data.")

    except subprocess.CalledProcessError as e:
        print(f"\nBuild failed: {e}")
        return False

    return True

if __name__ == "__main__":
    build_executable()
