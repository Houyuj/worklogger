"""
Logging utility with file rotation for Work Logger application.
Stores logs in a dedicated folder with automatic rotation (keeps only 20 most recent logs).
"""
import os
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any
import threading


class LogRotator:
    """
    A logging class that stores logs in daily files and rotates to keep only recent logs.
    """

    def __init__(self, log_dir: str = "logs", max_logs: int = 20):
        """
        Initialize the LogRotator.

        Args:
            log_dir: Directory to store log files
            max_logs: Maximum number of log files to keep
        """
        self.log_dir = Path(log_dir)
        self.max_logs = max_logs
        self._lock = threading.Lock()

        # Ensure log directory exists
        self.log_dir.mkdir(parents=True, exist_ok=True)

    def _get_log_file_path(self, date: Optional[datetime] = None) -> Path:
        """Get the log file path for a specific date."""
        if date is None:
            date = datetime.now()
        filename = f"worklogger_{date.strftime('%Y-%m-%d')}.log"
        return self.log_dir / filename

    def _rotate_logs(self):
        """Remove old log files to keep only max_logs most recent."""
        try:
            log_files = sorted(
                self.log_dir.glob("worklogger_*.log"),
                key=lambda f: f.stat().st_mtime,
                reverse=True
            )

            # Remove files beyond max_logs
            for old_file in log_files[self.max_logs:]:
                try:
                    old_file.unlink()
                except Exception:
                    pass  # Ignore deletion errors
        except Exception:
            pass  # Ignore rotation errors

    def write_log(
        self,
        level: str,
        message: str,
        source: str = "backend",
        data: Optional[Dict[str, Any]] = None
    ):
        """
        Write a log entry to the current day's log file.

        Args:
            level: Log level (DEBUG, INFO, WARN, ERROR)
            message: Log message
            source: Source of the log (backend/frontend)
            data: Optional additional data to include
        """
        with self._lock:
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "level": level.upper(),
                "source": source,
                "message": message,
            }

            if data:
                log_entry["data"] = data

            try:
                log_file = self._get_log_file_path()

                # Append to log file
                with open(log_file, "a", encoding="utf-8") as f:
                    f.write(json.dumps(log_entry) + "\n")

                # Rotate logs after write
                self._rotate_logs()

            except Exception as e:
                # Fallback to console if file write fails
                print(f"[LOG ERROR] Failed to write log: {e}")
                print(f"[{level}] {message}")

    def debug(self, message: str, source: str = "backend", data: Optional[Dict] = None):
        """Log a DEBUG message."""
        self.write_log("DEBUG", message, source, data)

    def info(self, message: str, source: str = "backend", data: Optional[Dict] = None):
        """Log an INFO message."""
        self.write_log("INFO", message, source, data)

    def warn(self, message: str, source: str = "backend", data: Optional[Dict] = None):
        """Log a WARN message."""
        self.write_log("WARN", message, source, data)

    def error(self, message: str, source: str = "backend", data: Optional[Dict] = None):
        """Log an ERROR message."""
        self.write_log("ERROR", message, source, data)

    def get_logs(
        self,
        date: Optional[str] = None,
        level: Optional[str] = None,
        source: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """
        Retrieve logs from file(s).

        Args:
            date: Specific date (YYYY-MM-DD) or None for today
            level: Filter by log level
            source: Filter by source (backend/frontend)
            limit: Maximum number of logs to return
            offset: Number of logs to skip

        Returns:
            List of log entries
        """
        logs = []

        try:
            if date:
                # Get logs from specific date
                date_obj = datetime.strptime(date, "%Y-%m-%d")
                log_file = self._get_log_file_path(date_obj)
                if log_file.exists():
                    logs = self._read_log_file(log_file)
            else:
                # Get logs from today
                log_file = self._get_log_file_path()
                if log_file.exists():
                    logs = self._read_log_file(log_file)

            # Apply filters
            if level:
                logs = [l for l in logs if l.get("level") == level.upper()]
            if source:
                logs = [l for l in logs if l.get("source") == source]

            # Sort by timestamp descending (most recent first)
            logs.sort(key=lambda x: x.get("timestamp", ""), reverse=True)

            # Apply pagination
            return logs[offset:offset + limit]

        except Exception as e:
            print(f"[LOG ERROR] Failed to read logs: {e}")
            return []

    def _read_log_file(self, file_path: Path) -> List[Dict[str, Any]]:
        """Read and parse a log file."""
        logs = []
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        try:
                            logs.append(json.loads(line))
                        except json.JSONDecodeError:
                            pass  # Skip malformed lines
        except Exception:
            pass
        return logs

    def get_log_files(self) -> List[Dict[str, Any]]:
        """
        Get list of available log files.

        Returns:
            List of log file info (name, date, size)
        """
        files = []
        try:
            for log_file in sorted(
                self.log_dir.glob("worklogger_*.log"),
                key=lambda f: f.stat().st_mtime,
                reverse=True
            ):
                try:
                    stat = log_file.stat()
                    # Extract date from filename
                    date_str = log_file.stem.replace("worklogger_", "")
                    files.append({
                        "filename": log_file.name,
                        "date": date_str,
                        "size": stat.st_size,
                        "modified": datetime.fromtimestamp(stat.st_mtime).isoformat()
                    })
                except Exception:
                    pass
        except Exception:
            pass
        return files

    def clear_logs(self, date: Optional[str] = None) -> bool:
        """
        Clear logs for a specific date or all logs.

        Args:
            date: Specific date (YYYY-MM-DD) or None for all logs

        Returns:
            True if successful, False otherwise
        """
        try:
            if date:
                date_obj = datetime.strptime(date, "%Y-%m-%d")
                log_file = self._get_log_file_path(date_obj)
                if log_file.exists():
                    log_file.unlink()
            else:
                for log_file in self.log_dir.glob("worklogger_*.log"):
                    log_file.unlink()
            return True
        except Exception as e:
            print(f"[LOG ERROR] Failed to clear logs: {e}")
            return False


# Global logger instance
logger = LogRotator()
