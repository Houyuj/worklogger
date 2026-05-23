"""
Migration: Add start_year and end_year to projects

This migration adds year range fields to the projects table and auto-assigns
values based on existing annual goals.
"""

from sqlalchemy import text
from backend.database import engine

def migrate():
    """Run the migration"""
    print("Starting migration: Add start_year and end_year to projects...")

    with engine.connect() as conn:
        # Add columns to projects table
        print("Adding start_year column...")
        conn.execute(text("ALTER TABLE projects ADD COLUMN start_year INTEGER"))

        print("Adding end_year column...")
        conn.execute(text("ALTER TABLE projects ADD COLUMN end_year INTEGER"))

        # Auto-assign year ranges based on annual goals
        print("Auto-populating year ranges from annual goals...")
        conn.execute(text("""
            UPDATE projects
            SET start_year = (
                SELECT MIN(year)
                FROM annual_goals
                WHERE annual_goals.project_id = projects.id
            ),
            end_year = (
                SELECT MAX(year)
                FROM annual_goals
                WHERE annual_goals.project_id = projects.id
            )
        """))

        conn.commit()
        print("Migration completed successfully!")

        # Show summary
        result = conn.execute(text("""
            SELECT
                COUNT(*) as total_projects,
                COUNT(start_year) as projects_with_start,
                COUNT(end_year) as projects_with_end
            FROM projects
        """))
        row = result.fetchone()
        print(f"\nSummary:")
        print(f"  Total projects: {row[0]}")
        print(f"  Projects with start_year: {row[1]}")
        print(f"  Projects with end_year: {row[2]}")

def rollback():
    """Rollback the migration"""
    print("Rolling back migration: Removing start_year and end_year from projects...")

    with engine.connect() as conn:
        print("Dropping start_year column...")
        conn.execute(text("ALTER TABLE projects DROP COLUMN start_year"))

        print("Dropping end_year column...")
        conn.execute(text("ALTER TABLE projects DROP COLUMN end_year"))

        conn.commit()
        print("Rollback completed successfully!")

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "rollback":
        rollback()
    else:
        migrate()
