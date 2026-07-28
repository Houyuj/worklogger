from __future__ import annotations

import json
import os
import shutil
import sys
import threading
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from fastapi import Header, HTTPException, Query
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker


BASE_DIR = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DEFAULT_DATA_DIR = BASE_DIR / "data"

if getattr(sys, "frozen", False):
    DEFAULT_DATA_DIR = (
        Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
        / "WorkLogger"
        / "data"
    )

DATA_DIR = Path(os.environ.get("WORKLOGGER_DATA_DIR", DEFAULT_DATA_DIR))
DATABASE_PATH = DATA_DIR / "worklogger.db"
USER_REGISTRY_PATH = DATA_DIR / "users.json"
USER_DATABASE_DIR = DATA_DIR / "users"
RETAINED_DATABASE_DIR = DATA_DIR / "retained"

for directory in (DATA_DIR, USER_DATABASE_DIR, RETAINED_DATABASE_DIR):
    directory.mkdir(parents=True, exist_ok=True)

_registry_lock = threading.RLock()
_engine_lock = threading.RLock()
_engines: dict[str, Engine] = {}


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _default_registry() -> dict:
    return {
        "version": 1,
        "users": [
            {
                "id": "default",
                "name": "User",
                "database_path": "worklogger.db",
                "created_at": _utc_now(),
            }
        ],
        "retained": [],
    }


def _write_registry(registry: dict) -> None:
    temporary_path = USER_REGISTRY_PATH.with_suffix(".json.tmp")
    temporary_path.write_text(
        json.dumps(registry, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    temporary_path.replace(USER_REGISTRY_PATH)


def _load_registry() -> dict:
    with _registry_lock:
        if not USER_REGISTRY_PATH.exists():
            registry = _default_registry()
            _write_registry(registry)
            return registry

        registry = json.loads(USER_REGISTRY_PATH.read_text(encoding="utf-8"))
        registry.setdefault("version", 1)
        registry.setdefault("users", [])
        registry.setdefault("retained", [])
        if not registry["users"]:
            registry["users"] = _default_registry()["users"]
            _write_registry(registry)
        return registry


def _database_path(record: dict) -> Path:
    relative_path = Path(record["database_path"])
    resolved = (DATA_DIR / relative_path).resolve()
    if DATA_DIR.resolve() not in resolved.parents and resolved != DATA_DIR.resolve():
        raise ValueError("Invalid user database path")
    return resolved


def _make_engine(path: Path) -> Engine:
    path.parent.mkdir(parents=True, exist_ok=True)
    return create_engine(
        f"sqlite:///{path.as_posix()}",
        connect_args={"check_same_thread": False},
    )


def list_users() -> list[dict]:
    registry = _load_registry()
    return [dict(user) for user in registry["users"]]


def list_retained_databases() -> list[dict]:
    registry = _load_registry()
    return [dict(record) for record in registry["retained"]]


def get_user_record(user_id: Optional[str] = None) -> dict:
    users = _load_registry()["users"]
    if user_id:
        user = next((item for item in users if item["id"] == user_id), None)
        if user:
            return dict(user)
        raise KeyError(user_id)
    return dict(users[0])


def get_retained_record(record_id: str) -> dict:
    retained = _load_registry()["retained"]
    record = next((item for item in retained if item["id"] == record_id), None)
    if not record:
        raise KeyError(record_id)
    return dict(record)


def get_user_database_path(user_id: str) -> Path:
    return _database_path(get_user_record(user_id))


def get_retained_database_path(record_id: str) -> Path:
    return _database_path(get_retained_record(record_id))


def get_user_engine(user_id: Optional[str] = None) -> Engine:
    user = get_user_record(user_id)
    with _engine_lock:
        if user["id"] not in _engines:
            _engines[user["id"]] = _make_engine(_database_path(user))
        return _engines[user["id"]]


def apply_schema_migrations(bind: Optional[Engine] = None) -> None:
    """Apply additive SQLite migrations needed by existing local databases."""
    target_engine = bind or engine
    inspector = inspect(target_engine)
    tables = set(inspector.get_table_names())
    if not {"tasks", "weekly_goals"}.issubset(tables):
        return

    task_columns = {column["name"] for column in inspector.get_columns("tasks")}
    project_columns = (
        {column["name"] for column in inspector.get_columns("projects")}
        if "projects" in tables
        else set()
    )
    annual_columns = (
        {column["name"] for column in inspector.get_columns("annual_goals")}
        if "annual_goals" in tables
        else set()
    )
    monthly_columns = (
        {column["name"] for column in inspector.get_columns("monthly_goals")}
        if "monthly_goals" in tables
        else set()
    )
    weekly_columns = {
        column["name"] for column in inspector.get_columns("weekly_goals")
    }
    experiment_columns = (
        {column["name"] for column in inspector.get_columns("experiments")}
        if "experiments" in tables
        else set()
    )
    task_additions = {
        "project_id": "INTEGER",
        "annual_goal_id": "INTEGER",
        "priority": "VARCHAR(20) NOT NULL DEFAULT 'normal'",
        "workflow_status": "VARCHAR(20) NOT NULL DEFAULT 'unclassified'",
        "is_inbox": "BOOLEAN NOT NULL DEFAULT 0",
    }
    weekly_additions = {
        "monthly_goal_id": "INTEGER",
        "year": "INTEGER",
        "week_start": "DATE",
        "week_end": "DATE",
        "status": "VARCHAR(50) NOT NULL DEFAULT 'planned'",
    }
    experiment_additions = {
        "content": "TEXT",
    }

    with target_engine.begin() as connection:
        for name, definition in task_additions.items():
            if name not in task_columns:
                connection.execute(
                    text(f"ALTER TABLE tasks ADD COLUMN {name} {definition}")
                )
        for name, definition in weekly_additions.items():
            if name not in weekly_columns:
                connection.execute(
                    text(f"ALTER TABLE weekly_goals ADD COLUMN {name} {definition}")
                )
        for name, definition in experiment_additions.items():
            if name not in experiment_columns:
                connection.execute(
                    text(f"ALTER TABLE experiments ADD COLUMN {name} {definition}")
                )
        for table, columns in {
            "projects": project_columns,
            "annual_goals": annual_columns,
            "monthly_goals": monthly_columns,
            "weekly_goals": weekly_columns,
        }.items():
            if "archived" not in columns:
                connection.execute(
                    text(
                        f"ALTER TABLE {table} ADD COLUMN "
                        "archived BOOLEAN NOT NULL DEFAULT 0"
                    )
                )

        connection.execute(
            text(
                """
                UPDATE tasks
                SET annual_goal_id = (
                    SELECT annual_goal_id FROM monthly_goals
                    WHERE monthly_goals.id = tasks.monthly_goal_id
                )
                WHERE monthly_goal_id IS NOT NULL AND annual_goal_id IS NULL
                """
            )
        )
        connection.execute(
            text(
                """
                UPDATE tasks
                SET project_id = (
                    SELECT annual_goals.project_id
                    FROM annual_goals
                    WHERE annual_goals.id = tasks.annual_goal_id
                )
                WHERE annual_goal_id IS NOT NULL AND project_id IS NULL
                """
            )
        )
        connection.execute(text("UPDATE tasks SET is_inbox = 0"))
        connection.execute(
            text("UPDATE tasks SET workflow_status = 'completed' WHERE completed = 1")
        )
        connection.execute(
            text(
                """
                UPDATE tasks
                SET project_id = NULL, workflow_status = 'unclassified'
                WHERE completed = 0
                  AND annual_goal_id IS NULL
                  AND monthly_goal_id IS NULL
                  AND weekly_goal_id IS NULL
                """
            )
        )
        connection.execute(
            text(
                """
                UPDATE tasks
                SET workflow_status = 'planned'
                WHERE completed = 0
                  AND (
                    annual_goal_id IS NOT NULL
                    OR monthly_goal_id IS NOT NULL
                    OR weekly_goal_id IS NOT NULL
                  )
                  AND workflow_status NOT IN ('blocked', 'waiting')
                """
            )
        )
        connection.execute(
            text(
                "CREATE INDEX IF NOT EXISTS ix_tasks_inbox_status "
                "ON tasks (is_inbox, workflow_status)"
            )
        )
        connection.execute(
            text(
                "CREATE INDEX IF NOT EXISTS ix_tasks_project_id "
                "ON tasks (project_id)"
            )
        )
        connection.execute(
            text(
                "CREATE INDEX IF NOT EXISTS ix_tasks_annual_goal_id "
                "ON tasks (annual_goal_id)"
            )
        )
        connection.execute(
            text(
                "CREATE INDEX IF NOT EXISTS ix_weekly_goals_monthly_goal_id "
                "ON weekly_goals (monthly_goal_id)"
            )
        )
        connection.execute(
            text(
                "CREATE INDEX IF NOT EXISTS ix_projects_archived "
                "ON projects (archived)"
            )
        )
        connection.execute(
            text(
                "CREATE INDEX IF NOT EXISTS ix_annual_goals_archived "
                "ON annual_goals (archived)"
            )
        )
        connection.execute(
            text(
                "CREATE INDEX IF NOT EXISTS ix_monthly_goals_archived "
                "ON monthly_goals (archived)"
            )
        )
        connection.execute(
            text(
                "CREATE INDEX IF NOT EXISTS ix_weekly_goals_archived "
                "ON weekly_goals (archived)"
            )
        )


def initialize_all_user_databases(base) -> None:
    for user in list_users():
        user_engine = get_user_engine(user["id"])
        base.metadata.create_all(bind=user_engine)
        apply_schema_migrations(user_engine)


def create_user(name: str, base) -> dict:
    cleaned_name = " ".join(name.split())
    if not cleaned_name:
        raise ValueError("User name is required")
    if len(cleaned_name) > 80:
        raise ValueError("User name must be 80 characters or fewer")

    with _registry_lock:
        registry = _load_registry()
        if any(
            user["name"].casefold() == cleaned_name.casefold()
            for user in registry["users"]
        ):
            raise ValueError("A user with this name already exists")

        user_id = uuid.uuid4().hex
        user = {
            "id": user_id,
            "name": cleaned_name,
            "database_path": f"users/{user_id}.db",
            "created_at": _utc_now(),
        }
        user_engine = _make_engine(_database_path(user))
        try:
            base.metadata.create_all(bind=user_engine)
            apply_schema_migrations(user_engine)
        except Exception:
            user_engine.dispose()
            _database_path(user).unlink(missing_ok=True)
            raise

        with _engine_lock:
            _engines[user_id] = user_engine
        registry["users"].append(user)
        _write_registry(registry)
        return dict(user)


def delete_user(user_id: str, keep_database: bool = True) -> dict:
    with _registry_lock:
        registry = _load_registry()
        if len(registry["users"]) <= 1:
            raise ValueError("Create another user before deleting the last user")
        user = next(
            (item for item in registry["users"] if item["id"] == user_id),
            None,
        )
        if not user:
            raise KeyError(user_id)

        with _engine_lock:
            user_engine = _engines.pop(user_id, None)
            if user_engine:
                user_engine.dispose()

        source_path = _database_path(user)
        retained_record = None
        if keep_database and source_path.exists():
            retained_id = uuid.uuid4().hex
            retained_path = RETAINED_DATABASE_DIR / f"{retained_id}.db"
            shutil.move(str(source_path), str(retained_path))
            retained_record = {
                "id": retained_id,
                "name": user["name"],
                "original_user_id": user["id"],
                "database_path": str(retained_path.relative_to(DATA_DIR)).replace(
                    "\\", "/"
                ),
                "created_at": user["created_at"],
                "deleted_at": _utc_now(),
            }
            registry["retained"].append(retained_record)
        elif source_path.exists():
            source_path.unlink()

        registry["users"] = [
            item for item in registry["users"] if item["id"] != user_id
        ]
        _write_registry(registry)
        return {
            "deleted_user_id": user_id,
            "kept_database": bool(retained_record),
            "retained": retained_record,
            "fallback_user": dict(registry["users"][0]),
        }


def get_db(
    x_worklogger_user: Optional[str] = Header(
        default=None,
        alias="X-WorkLogger-User",
    ),
    user_id: Optional[str] = Query(default=None),
):
    try:
        user = get_user_record(x_worklogger_user or user_id)
    except KeyError:
        raise HTTPException(status_code=409, detail="Selected user no longer exists")

    session_factory = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=get_user_engine(user["id"]),
    )
    db = session_factory()
    db.info["worklogger_user"] = user
    try:
        yield db
    finally:
        db.close()


# Kept for compatibility with existing one-off migration scripts.
engine = get_user_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DATABASE_PATH.as_posix()}"
