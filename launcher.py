#!/usr/bin/env python3
"""
Work Logger Application Launcher
This script starts the FastAPI server and opens the application in the default web browser.
"""

import os
import sys
import time
import webbrowser
import subprocess
from pathlib import Path


def get_user_data_dir():
    """Return a persistent, user-writable directory for packaged builds."""
    if getattr(sys, "frozen", False):
        local_app_data = os.environ.get("LOCALAPPDATA")
        if local_app_data:
            return Path(local_app_data) / "WorkLogger" / "data"
        return Path.home() / "AppData" / "Local" / "WorkLogger" / "data"
    return Path(__file__).parent / "data"

def check_dependencies():
    """Check if required packages are installed"""
    try:
        import fastapi
        import uvicorn
        import sqlalchemy
        return True
    except ImportError:
        return False

def install_dependencies():
    """Install required dependencies"""
    print("Installing required dependencies...")
    requirements_file = Path(__file__).parent / "requirements.txt"
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", str(requirements_file)])
    print("Dependencies installed successfully!")

def start_server():
    """Start the FastAPI server"""
    os.environ.setdefault("WORKLOGGER_DATA_DIR", str(get_user_data_dir()))

    import uvicorn
    from backend.main import app

    # Get the host and port
    host = "127.0.0.1"
    port = 8000

    print(f"\n{'='*60}")
    print(f"  Work Logger Application Starting...")
    print(f"{'='*60}")
    print(f"  Server: http://{host}:{port}")
    print(f"  Opening browser in 2 seconds...")
    print(f"{'='*60}\n")

    # Open browser after a short delay
    def open_browser():
        time.sleep(2)
        webbrowser.open(f"http://{host}:{port}")

    import threading
    threading.Thread(target=open_browser, daemon=True).start()

    # Start the server
    uvicorn.run(app, host=host, port=port, log_level="info")

def main():
    """Main entry point"""
    # Change to script directory
    os.chdir(Path(__file__).parent)

    # Check and install dependencies if needed
    if not check_dependencies():
        print("Required dependencies not found.")
        response = input("Would you like to install them now? (y/n): ")
        if response.lower() == 'y':
            install_dependencies()
        else:
            print("Cannot start application without dependencies.")
            print(f"Please run: pip install -r requirements.txt")
            sys.exit(1)

    # Start the server
    try:
        start_server()
    except KeyboardInterrupt:
        print("\n\nShutting down Work Logger...")
        print("Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\nError starting server: {e}")
        print("\nPress Enter to exit...")
        input()
        sys.exit(1)

if __name__ == "__main__":
    main()
