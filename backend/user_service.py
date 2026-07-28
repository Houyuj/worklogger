from __future__ import annotations

from pathlib import Path

from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import Session, sessionmaker

from . import models


REQUIRED_IMPORT_TABLES = {
    "projects",
    "annual_goals",
    "monthly_goals",
    "weekly_goals",
    "tasks",
    "experiments",
    "custom_tags",
    "task_experiment_association",
    "experiment_tag_association",
}


def validate_sqlite_database(database_path: Path) -> None:
    if not database_path.exists() or database_path.stat().st_size < 100:
        raise ValueError("The selected database file is empty or invalid")
    with database_path.open("rb") as database_file:
        if database_file.read(16) != b"SQLite format 3\x00":
            raise ValueError("The selected file is not a SQLite database")

    source_engine = create_engine(f"sqlite:///{database_path.as_posix()}")
    try:
        available_tables = set(inspect(source_engine).get_table_names())
    finally:
        source_engine.dispose()
    missing_tables = REQUIRED_IMPORT_TABLES - available_tables
    if missing_tables:
        raise ValueError(
            "The database is not a compatible WorkLogger database. "
            f"Missing tables: {', '.join(sorted(missing_tables))}"
        )


def _unique_protocol_title(
    original_title: str,
    source_username: str,
    occupied_titles: set[str],
) -> tuple[str, bool]:
    title = (original_title or "Untitled Protocol").strip()
    if title.casefold() not in occupied_titles:
        occupied_titles.add(title.casefold())
        return title, False

    source_label = " ".join(source_username.split()) or "Imported user"
    candidate = f"{title} ({source_label})"
    counter = 2
    while candidate.casefold() in occupied_titles:
        candidate = f"{title} ({source_label} {counter})"
        counter += 1
    occupied_titles.add(candidate.casefold())
    return candidate, True


def merge_database(
    source_path: Path,
    destination_db: Session,
    source_username: str,
) -> dict:
    validate_sqlite_database(source_path)
    source_engine = create_engine(
        f"sqlite:///{source_path.as_posix()}",
        connect_args={"check_same_thread": False},
    )
    source_session_factory = sessionmaker(bind=source_engine)
    source_db = source_session_factory()

    counts = {
        "projects": 0,
        "annual_goals": 0,
        "monthly_goals": 0,
        "weekly_goals": 0,
        "tasks": 0,
        "protocols": 0,
        "renamed_protocols": 0,
        "custom_tags": 0,
    }
    project_ids: dict[int, int] = {}
    annual_ids: dict[int, int] = {}
    monthly_ids: dict[int, int] = {}
    weekly_ids: dict[int, int] = {}
    experiment_ids: dict[int, models.Experiment] = {}

    try:
        for source_project in source_db.query(models.Project).order_by(
            models.Project.id
        ):
            destination_project = models.Project(
                name=source_project.name,
                description=source_project.description,
                start_year=source_project.start_year,
                end_year=source_project.end_year,
                archived=source_project.archived,
                created_at=source_project.created_at,
            )
            destination_db.add(destination_project)
            destination_db.flush()
            project_ids[source_project.id] = destination_project.id
            counts["projects"] += 1

        for source_goal in source_db.query(models.AnnualGoal).order_by(
            models.AnnualGoal.id
        ):
            destination_goal = models.AnnualGoal(
                project_id=project_ids[source_goal.project_id],
                name=source_goal.name,
                description=source_goal.description,
                year=source_goal.year,
                total_tasks=source_goal.total_tasks,
                completed_tasks=source_goal.completed_tasks,
                archived=source_goal.archived,
                created_at=source_goal.created_at,
            )
            destination_db.add(destination_goal)
            destination_db.flush()
            annual_ids[source_goal.id] = destination_goal.id
            counts["annual_goals"] += 1

        for source_goal in source_db.query(models.MonthlyGoal).order_by(
            models.MonthlyGoal.id
        ):
            destination_goal = models.MonthlyGoal(
                annual_goal_id=annual_ids[source_goal.annual_goal_id],
                name=source_goal.name,
                description=source_goal.description,
                start_date=source_goal.start_date,
                end_date=source_goal.end_date,
                status=source_goal.status,
                total_tasks=source_goal.total_tasks,
                completed_tasks=source_goal.completed_tasks,
                archived=source_goal.archived,
                created_at=source_goal.created_at,
            )
            destination_db.add(destination_goal)
            destination_db.flush()
            monthly_ids[source_goal.id] = destination_goal.id
            counts["monthly_goals"] += 1

        for source_goal in source_db.query(models.WeeklyGoal).order_by(
            models.WeeklyGoal.id
        ):
            destination_goal = models.WeeklyGoal(
                name=source_goal.name,
                description=source_goal.description,
                week_number=source_goal.week_number,
                monthly_goal_id=monthly_ids.get(source_goal.monthly_goal_id),
                year=source_goal.year,
                week_start=source_goal.week_start,
                week_end=source_goal.week_end,
                status=source_goal.status,
                archived=source_goal.archived,
                created_at=source_goal.created_at,
            )
            destination_db.add(destination_goal)
            destination_db.flush()
            weekly_ids[source_goal.id] = destination_goal.id
            counts["weekly_goals"] += 1

        destination_tags = {
            tag.name.casefold(): tag
            for tag in destination_db.query(models.CustomTag).all()
        }
        tag_map: dict[int, models.CustomTag] = {}
        for source_tag in source_db.query(models.CustomTag).order_by(
            models.CustomTag.id
        ):
            destination_tag = destination_tags.get(source_tag.name.casefold())
            if not destination_tag:
                destination_tag = models.CustomTag(
                    name=source_tag.name,
                    created_at=source_tag.created_at,
                )
                destination_db.add(destination_tag)
                destination_db.flush()
                destination_tags[source_tag.name.casefold()] = destination_tag
                counts["custom_tags"] += 1
            tag_map[source_tag.id] = destination_tag

        occupied_titles = {
            experiment.name.casefold()
            for experiment in destination_db.query(models.Experiment).all()
        }
        for source_experiment in source_db.query(models.Experiment).order_by(
            models.Experiment.id
        ):
            title, renamed = _unique_protocol_title(
                source_experiment.name,
                source_username,
                occupied_titles,
            )
            destination_experiment = models.Experiment(
                name=title,
                status=source_experiment.status,
                annual_goal_id=annual_ids.get(source_experiment.annual_goal_id),
                monthly_goal_id=monthly_ids.get(source_experiment.monthly_goal_id),
                content=source_experiment.content,
                hypothesis=source_experiment.hypothesis,
                methodology=source_experiment.methodology,
                results=source_experiment.results,
                conclusion=source_experiment.conclusion,
                progress_notes=source_experiment.progress_notes,
                images_json=source_experiment.images_json,
                created_at=source_experiment.created_at,
                updated_at=source_experiment.updated_at,
            )
            destination_experiment.custom_tags = [
                tag_map[tag.id] for tag in source_experiment.custom_tags
            ]
            destination_db.add(destination_experiment)
            destination_db.flush()
            experiment_ids[source_experiment.id] = destination_experiment
            counts["protocols"] += 1
            if renamed:
                counts["renamed_protocols"] += 1

        for source_task in source_db.query(models.Task).order_by(models.Task.id):
            destination_task = models.Task(
                title=source_task.title,
                description=source_task.description,
                date=source_task.date,
                completed=source_task.completed,
                completed_at=source_task.completed_at,
                project_id=project_ids.get(source_task.project_id),
                annual_goal_id=annual_ids.get(source_task.annual_goal_id),
                monthly_goal_id=monthly_ids.get(source_task.monthly_goal_id),
                weekly_goal_id=weekly_ids.get(source_task.weekly_goal_id),
                priority=source_task.priority,
                workflow_status=source_task.workflow_status,
                is_inbox=source_task.is_inbox,
                created_at=source_task.created_at,
                updated_at=source_task.updated_at,
            )
            destination_task.experiments = [
                experiment_ids[experiment.id]
                for experiment in source_task.experiments
                if experiment.id in experiment_ids
            ]
            destination_db.add(destination_task)
            counts["tasks"] += 1

        destination_db.commit()
        return counts
    except Exception:
        destination_db.rollback()
        raise
    finally:
        source_db.close()
        source_engine.dispose()
