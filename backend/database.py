from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
import sys
from pathlib import Path

# Database file path
BASE_DIR = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DEFAULT_DATA_DIR = BASE_DIR / 'data'

if getattr(sys, 'frozen', False):
    DEFAULT_DATA_DIR = Path(os.environ.get('LOCALAPPDATA', Path.home() / 'AppData' / 'Local')) / 'WorkLogger' / 'data'

DATA_DIR = Path(os.environ.get('WORKLOGGER_DATA_DIR', DEFAULT_DATA_DIR))
DATABASE_PATH = DATA_DIR / 'worklogger.db'

# Ensure data directory exists
DATA_DIR.mkdir(parents=True, exist_ok=True)

# SQLite database URL
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DATABASE_PATH.as_posix()}"

# Create engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}  # Needed for SQLite
)

# Create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def apply_schema_migrations():
    """Apply additive SQLite migrations needed by existing local databases."""
    inspector = inspect(engine)
    tables = set(inspector.get_table_names())
    if not {'tasks', 'weekly_goals'}.issubset(tables):
        return

    task_columns = {column['name'] for column in inspector.get_columns('tasks')}
    project_columns = {column['name'] for column in inspector.get_columns('projects')} if 'projects' in tables else set()
    annual_columns = {column['name'] for column in inspector.get_columns('annual_goals')} if 'annual_goals' in tables else set()
    monthly_columns = {column['name'] for column in inspector.get_columns('monthly_goals')} if 'monthly_goals' in tables else set()
    weekly_columns = {column['name'] for column in inspector.get_columns('weekly_goals')}
    experiment_columns = {column['name'] for column in inspector.get_columns('experiments')} if 'experiments' in tables else set()
    task_additions = {
        'project_id': 'INTEGER',
        'annual_goal_id': 'INTEGER',
        'priority': "VARCHAR(20) NOT NULL DEFAULT 'normal'",
        'workflow_status': "VARCHAR(20) NOT NULL DEFAULT 'unclassified'",
        'is_inbox': 'BOOLEAN NOT NULL DEFAULT 0',
    }
    weekly_additions = {
        'monthly_goal_id': 'INTEGER',
        'year': 'INTEGER',
        'week_start': 'DATE',
        'week_end': 'DATE',
        'status': "VARCHAR(50) NOT NULL DEFAULT 'planned'",
    }
    experiment_additions = {
        'content': 'TEXT',
    }

    with engine.begin() as connection:
        for name, definition in task_additions.items():
            if name not in task_columns:
                connection.execute(text(f'ALTER TABLE tasks ADD COLUMN {name} {definition}'))
        for name, definition in weekly_additions.items():
            if name not in weekly_columns:
                connection.execute(text(f'ALTER TABLE weekly_goals ADD COLUMN {name} {definition}'))
        for name, definition in experiment_additions.items():
            if name not in experiment_columns:
                connection.execute(text(f'ALTER TABLE experiments ADD COLUMN {name} {definition}'))
        for table, columns in {
            'projects': project_columns,
            'annual_goals': annual_columns,
            'monthly_goals': monthly_columns,
            'weekly_goals': weekly_columns,
        }.items():
            if 'archived' not in columns:
                connection.execute(text(f'ALTER TABLE {table} ADD COLUMN archived BOOLEAN NOT NULL DEFAULT 0'))

        connection.execute(text('''
            UPDATE tasks
            SET annual_goal_id = (
                SELECT annual_goal_id FROM monthly_goals
                WHERE monthly_goals.id = tasks.monthly_goal_id
            )
            WHERE monthly_goal_id IS NOT NULL AND annual_goal_id IS NULL
        '''))
        connection.execute(text('''
            UPDATE tasks
            SET project_id = (
                SELECT annual_goals.project_id
                FROM annual_goals
                WHERE annual_goals.id = tasks.annual_goal_id
            )
            WHERE annual_goal_id IS NOT NULL AND project_id IS NULL
        '''))
        # Inbox was removed from the product workflow. Keep all tasks visible,
        # but align legacy records with the current planning state machine.
        connection.execute(text("UPDATE tasks SET is_inbox = 0"))
        connection.execute(text("UPDATE tasks SET workflow_status = 'completed' WHERE completed = 1"))
        connection.execute(text('''
            UPDATE tasks
            SET project_id = NULL, workflow_status = 'unclassified'
            WHERE completed = 0
              AND annual_goal_id IS NULL
              AND monthly_goal_id IS NULL
              AND weekly_goal_id IS NULL
        '''))
        connection.execute(text('''
            UPDATE tasks
            SET workflow_status = 'planned'
            WHERE completed = 0
              AND (annual_goal_id IS NOT NULL OR monthly_goal_id IS NOT NULL OR weekly_goal_id IS NOT NULL)
              AND workflow_status NOT IN ('blocked', 'waiting')
        '''))
        connection.execute(text('CREATE INDEX IF NOT EXISTS ix_tasks_inbox_status ON tasks (is_inbox, workflow_status)'))
        connection.execute(text('CREATE INDEX IF NOT EXISTS ix_tasks_project_id ON tasks (project_id)'))
        connection.execute(text('CREATE INDEX IF NOT EXISTS ix_tasks_annual_goal_id ON tasks (annual_goal_id)'))
        connection.execute(text('CREATE INDEX IF NOT EXISTS ix_weekly_goals_monthly_goal_id ON weekly_goals (monthly_goal_id)'))
        connection.execute(text('CREATE INDEX IF NOT EXISTS ix_projects_archived ON projects (archived)'))
        connection.execute(text('CREATE INDEX IF NOT EXISTS ix_annual_goals_archived ON annual_goals (archived)'))
        connection.execute(text('CREATE INDEX IF NOT EXISTS ix_monthly_goals_archived ON monthly_goals (archived)'))
        connection.execute(text('CREATE INDEX IF NOT EXISTS ix_weekly_goals_archived ON weekly_goals (archived)'))

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
