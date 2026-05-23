#!/usr/bin/env python3
"""
Verification script to check if the Work Logger application is properly set up
"""

import os
import sys
from pathlib import Path

def check_file(path, description):
    """Check if a file exists"""
    if os.path.exists(path):
        print(f"✓ {description}")
        return True
    else:
        print(f"✗ {description} - NOT FOUND")
        return False

def check_directory(path, description):
    """Check if a directory exists"""
    if os.path.isdir(path):
        print(f"✓ {description}")
        return True
    else:
        print(f"✗ {description} - NOT FOUND")
        return False

def main():
    print("=" * 60)
    print("Work Logger - Installation Verification")
    print("=" * 60)
    print()

    base_dir = Path(__file__).parent
    all_good = True

    # Check directories
    print("Checking Directories:")
    all_good &= check_directory(base_dir / "backend", "Backend directory")
    all_good &= check_directory(base_dir / "frontend", "Frontend directory")
    all_good &= check_directory(base_dir / "data", "Data directory")
    print()

    # Check backend files
    print("Checking Backend Files:")
    all_good &= check_file(base_dir / "backend" / "main.py", "FastAPI application")
    all_good &= check_file(base_dir / "backend" / "models.py", "Database models")
    all_good &= check_file(base_dir / "backend" / "crud.py", "CRUD operations")
    all_good &= check_file(base_dir / "backend" / "schemas.py", "Pydantic schemas")
    all_good &= check_file(base_dir / "backend" / "database.py", "Database config")
    print()

    # Check frontend files
    print("Checking Frontend Files:")
    all_good &= check_file(base_dir / "frontend" / "index.html", "Index page")
    all_good &= check_file(base_dir / "frontend" / "dashboard.html", "Dashboard page")
    all_good &= check_file(base_dir / "frontend" / "reports.html", "Reports page")
    all_good &= check_file(base_dir / "frontend" / "gantt.html", "Gantt chart page")
    all_good &= check_file(base_dir / "frontend" / "experiments.html", "Experiments page")
    all_good &= check_file(base_dir / "frontend" / "api.js", "API client")
    print()

    # Check launcher files
    print("Checking Launcher Files:")
    all_good &= check_file(base_dir / "launcher.py", "Python launcher")
    all_good &= check_file(base_dir / "run.bat", "Windows launcher")
    all_good &= check_file(base_dir / "run.sh", "Linux/Mac launcher")
    all_good &= check_file(base_dir / "setup.bat", "Windows setup")
    print()

    # Check configuration files
    print("Checking Configuration Files:")
    all_good &= check_file(base_dir / "environment.yml", "Conda environment file")
    all_good &= check_file(base_dir / "requirements.txt", "Requirements file")
    print()

    # Check documentation
    print("Checking Documentation:")
    all_good &= check_file(base_dir / "README.md", "README documentation")
    all_good &= check_file(base_dir / "QUICKSTART.md", "Quick start guide")
    all_good &= check_file(base_dir / "PROJECT_SUMMARY.md", "Project summary")
    print()

    # Check database
    print("Checking Database:")
    db_path = base_dir / "data" / "worklogger.db"
    if check_file(db_path, "SQLite database"):
        size = os.path.getsize(db_path)
        print(f"  Database size: {size:,} bytes")
    print()

    # Check conda environment
    print("Checking Conda Environment:")
    try:
        import subprocess
        result = subprocess.run(
            ["conda", "env", "list"],
            capture_output=True,
            text=True
        )
        if "worklogger" in result.stdout:
            print("✓ Conda environment 'worklogger' exists")
        else:
            print("✗ Conda environment 'worklogger' not found")
            print("  Run: conda env create -f environment.yml")
            all_good = False
    except Exception as e:
        print(f"✗ Could not check conda environment: {e}")
        all_good = False
    print()

    # Try importing key packages
    print("Checking Python Packages:")
    try:
        import fastapi
        print(f"✓ FastAPI {fastapi.__version__}")
    except ImportError:
        print("✗ FastAPI not installed")
        all_good = False

    try:
        import uvicorn
        print(f"✓ Uvicorn {uvicorn.__version__}")
    except ImportError:
        print("✗ Uvicorn not installed")
        all_good = False

    try:
        import sqlalchemy
        print(f"✓ SQLAlchemy {sqlalchemy.__version__}")
    except ImportError:
        print("✗ SQLAlchemy not installed")
        all_good = False

    try:
        import pydantic
        print(f"✓ Pydantic {pydantic.__version__}")
    except ImportError:
        print("✗ Pydantic not installed")
        all_good = False

    print()
    print("=" * 60)
    if all_good:
        print("✅ All checks passed! Application is ready to run.")
        print()
        print("To start the application:")
        print("  Windows: run.bat")
        print("  Linux/Mac: ./run.sh")
        print("  Or: conda activate worklogger && python launcher.py")
    else:
        print("❌ Some checks failed. Please review the errors above.")
        print()
        print("To fix:")
        print("  1. Ensure all files are present")
        print("  2. Run: conda env create -f environment.yml")
        print("  3. Run this script again")
    print("=" * 60)

if __name__ == "__main__":
    main()
