"""
Build script to create standalone executable
Run: python build_exe.py
"""

import os
import sys
import subprocess

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

    # PyInstaller command
    cmd = [
        "pyinstaller",
        "--name=WorkLogger",
        "--onefile",
        "--windowed",  # No console window
        "--add-data=frontend:frontend",
        "--add-data=backend:backend",
        "--icon=NONE",  # Add icon file if available
        "launcher.py"
    ]

    # Run PyInstaller
    try:
        subprocess.check_call(cmd)
        print("\n" + "="*60)
        print("Build completed successfully!")
        print("="*60)
        print("\nExecutable location: dist/WorkLogger.exe")
        print("\nTo distribute:")
        print("1. Copy the dist/WorkLogger.exe file")
        print("2. Copy the frontend folder")
        print("3. Users can run WorkLogger.exe directly")
        print("\nNote: First-time users will need to wait for")
        print("dependencies to install automatically.")

    except subprocess.CalledProcessError as e:
        print(f"\nBuild failed: {e}")
        return False

    return True

if __name__ == "__main__":
    build_executable()
