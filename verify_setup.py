#!/usr/bin/env python3
"""Check that a local Work Logger installation is ready to run."""

import os
import sys
from pathlib import Path


def check_path(path: Path, description: str, directory: bool = False) -> bool:
    exists = path.is_dir() if directory else path.is_file()
    status = "OK" if exists else "MISSING"
    print(f"[{status}] {description}: {path}")
    return exists


def check_package(package_name: str, module_name: str) -> bool:
    try:
        module = __import__(module_name)
        version = getattr(module, "__version__", "installed")
        print(f"[OK] {package_name}: {version}")
        return True
    except ImportError:
        print(f"[MISSING] {package_name}")
        return False


def main() -> int:
    print("=" * 60)
    print("Work Logger - Installation Verification")
    print("=" * 60)

    base_dir = Path(__file__).resolve().parent
    checks = [
        check_path(base_dir / "backend", "Backend directory", directory=True),
        check_path(base_dir / "frontend", "Frontend directory", directory=True),
        check_path(base_dir / "data", "Data directory", directory=True),
        check_path(base_dir / "backend" / "main.py", "FastAPI application"),
        check_path(base_dir / "frontend" / "index.html", "Index page"),
        check_path(base_dir / "launcher.py", "Application launcher"),
        check_path(base_dir / "run.bat", "Windows launcher"),
        check_path(base_dir / "setup.bat", "Windows setup script"),
        check_path(base_dir / "requirements.txt", "Requirements file"),
    ]

    database_path = base_dir / "data" / "worklogger.db"
    if database_path.exists():
        print(f"[OK] SQLite database: {database_path} ({database_path.stat().st_size:,} bytes)")
    else:
        print("[INFO] SQLite database will be created on first start")

    print(f"Python interpreter: {sys.executable}")
    package_checks = [
        check_package("FastAPI", "fastapi"),
        check_package("Uvicorn", "uvicorn"),
        check_package("SQLAlchemy", "sqlalchemy"),
        check_package("Pydantic", "pydantic"),
        check_package("openpyxl", "openpyxl"),
        check_package("ReportLab", "reportlab"),
        check_package("python-docx", "docx"),
    ]

    ready = all(checks) and all(package_checks)
    print("=" * 60)
    if ready:
        print("All checks passed. Start the application with run.bat.")
        return 0

    print("Setup is incomplete. Run setup.bat and try again.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
