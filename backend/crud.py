from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, extract, func
from datetime import datetime, timedelta
from typing import List, Optional
import json

from . import models, schemas

# ========== Project CRUD ==========
def create_project(db: Session, project: schemas.ProjectCreate):
    db_project = models.Project(**project.model_dump())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

def get_projects(db: Session, year: Optional[int] = None):
    query = db.query(models.Project)
    if year:
        # Filter projects where year falls within range
        query = query.filter(
            or_(
                # Projects with no year constraints
                and_(
                    models.Project.start_year.is_(None),
                    models.Project.end_year.is_(None)
                ),
                # Projects where year falls within start_year and end_year
                and_(
                    models.Project.start_year <= year,
                    or_(
                        models.Project.end_year.is_(None),
                        models.Project.end_year >= year
                    )
                )
            )
        )
    return query.all()

def get_project(db: Session, project_id: int):
    return db.query(models.Project).filter(models.Project.id == project_id).first()

def update_project(db: Session, project_id: int, project_update: schemas.ProjectUpdate):
    db_project = get_project(db, project_id)
    if db_project:
        update_data = project_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_project, key, value)
        db.commit()
        db.refresh(db_project)
    return db_project

# ========== Annual Goal CRUD ==========
def create_annual_goal(db: Session, goal: schemas.AnnualGoalCreate):
    db_goal = models.AnnualGoal(**goal.model_dump())
    db.add(db_goal)
    db.commit()
    db.refresh(db_goal)
    return db_goal

def get_annual_goals(db: Session, project_id: Optional[int] = None, year: Optional[int] = None):
    query = db.query(models.AnnualGoal)
    if project_id:
        query = query.filter(models.AnnualGoal.project_id == project_id)
    if year:
        query = query.filter(models.AnnualGoal.year == year)
    return query.all()

def get_annual_goal(db: Session, goal_id: int):
    return db.query(models.AnnualGoal).filter(models.AnnualGoal.id == goal_id).first()

def update_annual_goal(db: Session, goal_id: int, goal_update: schemas.AnnualGoalUpdate):
    db_goal = get_annual_goal(db, goal_id)
    if db_goal:
        update_data = goal_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_goal, key, value)
        db.commit()
        db.refresh(db_goal)
    return db_goal

# ========== Monthly Goal CRUD ==========
def create_monthly_goal(db: Session, goal: schemas.MonthlyGoalCreate):
    db_goal = models.MonthlyGoal(**goal.model_dump())
    db.add(db_goal)
    db.commit()
    db.refresh(db_goal)
    return db_goal

def get_monthly_goals(db: Session, annual_goal_id: Optional[int] = None):
    query = db.query(models.MonthlyGoal)
    if annual_goal_id:
        query = query.filter(models.MonthlyGoal.annual_goal_id == annual_goal_id)
    return query.all()

def get_monthly_goal(db: Session, goal_id: int):
    return db.query(models.MonthlyGoal).filter(models.MonthlyGoal.id == goal_id).first()

def update_monthly_goal_status(db: Session, goal_id: int, status: str):
    db_goal = get_monthly_goal(db, goal_id)
    if db_goal:
        db_goal.status = status
        db.commit()
        db.refresh(db_goal)
    return db_goal

def update_monthly_goal(db: Session, goal_id: int, goal_update: schemas.MonthlyGoalUpdate):
    db_goal = get_monthly_goal(db, goal_id)
    if db_goal:
        update_data = goal_update.model_dump(exclude_unset=True)

        # If dates are being changed, validate no conflicts with existing tasks
        if 'start_date' in update_data or 'end_date' in update_data:
            new_start = update_data.get('start_date', db_goal.start_date)
            new_end = update_data.get('end_date', db_goal.end_date)

            # Check for tasks outside the new date range
            tasks_outside = db.query(models.Task).filter(
                models.Task.monthly_goal_id == goal_id,
                or_(
                    models.Task.date < new_start,
                    models.Task.date > new_end
                )
            ).all()

            if tasks_outside:
                # Format task dates for error message
                task_dates = [t.date.strftime('%Y-%m-%d') for t in tasks_outside[:3]]
                task_list = ', '.join(task_dates)
                if len(tasks_outside) > 3:
                    task_list += f', and {len(tasks_outside) - 3} more'

                raise ValueError(
                    f"Cannot shorten date range. {len(tasks_outside)} task(s) fall outside "
                    f"the new range (dates: {task_list}). "
                    f"Please delete or reassign these tasks first."
                )

        for key, value in update_data.items():
            setattr(db_goal, key, value)
        db.commit()
        db.refresh(db_goal)
    return db_goal

# ========== Weekly Goal CRUD ==========
def create_weekly_goal(db: Session, goal: schemas.WeeklyGoalCreate):
    db_goal = models.WeeklyGoal(**goal.model_dump())
    db.add(db_goal)
    db.commit()
    db.refresh(db_goal)
    return db_goal

def get_weekly_goals(db: Session):
    return db.query(models.WeeklyGoal).all()

def get_weekly_goal(db: Session, goal_id: int):
    return db.query(models.WeeklyGoal).filter(models.WeeklyGoal.id == goal_id).first()

# ========== Task CRUD ==========
def create_task(db: Session, task: schemas.TaskCreate):
    task_data = task.model_dump(exclude={'experiment_ids'})
    db_task = models.Task(**task_data)

    # Link to experiments if provided
    if task.experiment_ids:
        experiments = db.query(models.Experiment).filter(
            models.Experiment.id.in_(task.experiment_ids)
        ).all()
        db_task.experiments = experiments

    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    # Update monthly goal task count
    if db_task.monthly_goal_id:
        update_goal_task_counts(db, db_task.monthly_goal_id)

    return db_task

def get_tasks(db: Session, date: Optional[datetime] = None, completed: Optional[bool] = None):
    query = db.query(models.Task)
    if date:
        query = query.filter(func.date(models.Task.date) == date.date())
    if completed is not None:
        query = query.filter(models.Task.completed == completed)
    return query.order_by(models.Task.date.desc()).all()

def get_task(db: Session, task_id: int):
    return db.query(models.Task).filter(models.Task.id == task_id).first()

def update_task(db: Session, task_id: int, task_update: schemas.TaskUpdate):
    db_task = get_task(db, task_id)
    if db_task:
        old_monthly_goal_id = db_task.monthly_goal_id

        # Exclude experiment_ids from direct assignment
        update_data = task_update.model_dump(exclude_unset=True, exclude={'experiment_ids'})

        # Handle completion timestamp
        if 'completed' in update_data:
            if update_data['completed'] and not db_task.completed:
                db_task.completed_at = datetime.utcnow()
            elif not update_data['completed']:
                db_task.completed_at = None

        for key, value in update_data.items():
            setattr(db_task, key, value)

        # Update experiment links
        if task_update.experiment_ids is not None:
            experiments = db.query(models.Experiment).filter(
                models.Experiment.id.in_(task_update.experiment_ids)
            ).all()
            db_task.experiments = experiments

        db.commit()
        db.refresh(db_task)

        # Update task counts for affected monthly goals
        if old_monthly_goal_id:
            update_goal_task_counts(db, old_monthly_goal_id)
        if db_task.monthly_goal_id and db_task.monthly_goal_id != old_monthly_goal_id:
            update_goal_task_counts(db, db_task.monthly_goal_id)

    return db_task

def delete_task(db: Session, task_id: int):
    db_task = get_task(db, task_id)
    if db_task:
        monthly_goal_id = db_task.monthly_goal_id
        db.delete(db_task)
        db.commit()
        if monthly_goal_id:
            update_goal_task_counts(db, monthly_goal_id)
        return True
    return False

def update_goal_task_counts(db: Session, monthly_goal_id: int):
    """Update task counts for monthly and annual goals"""
    monthly_goal = get_monthly_goal(db, monthly_goal_id)
    if monthly_goal:
        tasks = db.query(models.Task).filter(models.Task.monthly_goal_id == monthly_goal_id).all()
        monthly_goal.total_tasks = len(tasks)
        monthly_goal.completed_tasks = sum(1 for t in tasks if t.completed)

        # Update annual goal counts
        annual_goal = monthly_goal.annual_goal
        if annual_goal:
            all_tasks = db.query(models.Task).join(models.MonthlyGoal).filter(
                models.MonthlyGoal.annual_goal_id == annual_goal.id
            ).all()
            annual_goal.total_tasks = len(all_tasks)
            annual_goal.completed_tasks = sum(1 for t in all_tasks if t.completed)

        db.commit()

def search_tasks(db: Session, query: str, page: int = 1, limit: int = 5):
    """Search tasks by title or description across all time ranges"""
    from sqlalchemy import or_
    from sqlalchemy.orm import joinedload

    # Build query
    search_filter = or_(
        models.Task.title.ilike(f'%{query}%'),
        models.Task.description.ilike(f'%{query}%')
    )

    # Get total count
    total_count = db.query(models.Task).filter(search_filter).count()

    # Get paginated results sorted by date (newest first) with experiments loaded
    offset = (page - 1) * limit
    tasks = db.query(models.Task).options(joinedload(models.Task.experiments))\
        .filter(search_filter)\
        .order_by(models.Task.date.desc())\
        .offset(offset)\
        .limit(limit)\
        .all()

    total_pages = (total_count + limit - 1) // limit

    return {
        'tasks': tasks,
        'total_count': total_count,
        'page': page,
        'limit': limit,
        'total_pages': total_pages,
        'has_next': page < total_pages,
        'has_prev': page > 1
    }

# ========== Experiment CRUD ==========
def create_experiment(db: Session, experiment: schemas.ExperimentCreate):
    experiment_data = experiment.model_dump(exclude={'custom_tag_names'})
    db_experiment = models.Experiment(**experiment_data)

    # Handle custom tags
    if experiment.custom_tag_names:
        tags = []
        for tag_name in experiment.custom_tag_names:
            tag = db.query(models.CustomTag).filter(models.CustomTag.name == tag_name).first()
            if not tag:
                tag = models.CustomTag(name=tag_name)
                db.add(tag)
            tags.append(tag)
        db_experiment.custom_tags = tags

    db.add(db_experiment)
    db.commit()
    db.refresh(db_experiment)
    return db_experiment

def get_experiments(db: Session, status: Optional[str] = None):
    query = db.query(models.Experiment)
    if status:
        query = query.filter(models.Experiment.status == status)
    return query.order_by(models.Experiment.created_at.desc()).all()

def get_experiment(db: Session, experiment_id: int):
    return db.query(models.Experiment).filter(models.Experiment.id == experiment_id).first()

def update_experiment(db: Session, experiment_id: int, experiment_update: schemas.ExperimentUpdate):
    db_experiment = get_experiment(db, experiment_id)
    if db_experiment:
        update_data = experiment_update.model_dump(exclude_unset=True, exclude={'custom_tag_names'})

        for key, value in update_data.items():
            setattr(db_experiment, key, value)

        # Update custom tags if provided
        if experiment_update.custom_tag_names is not None:
            tags = []
            for tag_name in experiment_update.custom_tag_names:
                tag = db.query(models.CustomTag).filter(models.CustomTag.name == tag_name).first()
                if not tag:
                    tag = models.CustomTag(name=tag_name)
                    db.add(tag)
                tags.append(tag)
            db_experiment.custom_tags = tags

        db.commit()
        db.refresh(db_experiment)
    return db_experiment

def get_experiment_tasks(db: Session, experiment_id: int):
    experiment = get_experiment(db, experiment_id)
    if experiment:
        return experiment.tasks
    return []

def delete_experiment(db: Session, experiment_id: int):
    """Delete an experiment"""
    db_experiment = get_experiment(db, experiment_id)
    if db_experiment:
        # Clear the custom_tags relationship (many-to-many)
        db_experiment.custom_tags = []
        # Clear the tasks relationship (many-to-many)
        db_experiment.tasks = []
        db.delete(db_experiment)
        db.commit()
        return True
    return False

def duplicate_experiment(db: Session, experiment_id: int):
    """Duplicate an experiment"""
    from datetime import datetime

    source_experiment = get_experiment(db, experiment_id)
    if not source_experiment:
        return None

    # Generate unique title with timestamp
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    base_title = f"{source_experiment.name} - Copy {timestamp}"

    # Check for duplicate titles and add counter if needed
    duplicate_title = base_title
    counter = 2
    while db.query(models.Experiment).filter(models.Experiment.name == duplicate_title).first():
        duplicate_title = f"{base_title} ({counter})"
        counter += 1

    # Create duplicate with copied fields
    duplicate_data = {
        'name': duplicate_title,
        'status': 'planned',  # Always set to planned
        'hypothesis': source_experiment.hypothesis,
        'methodology': source_experiment.methodology,
        'results': source_experiment.results,
        'conclusion': source_experiment.conclusion,
        'progress_notes': source_experiment.progress_notes,
        'images_json': source_experiment.images_json,
        'annual_goal_id': None,  # Clear goal relationships
        'monthly_goal_id': None
    }

    db_experiment = models.Experiment(**duplicate_data)

    # Copy custom tags
    db_experiment.custom_tags = list(source_experiment.custom_tags)

    db.add(db_experiment)
    db.commit()
    db.refresh(db_experiment)

    return db_experiment

# ========== Custom Tag CRUD ==========
def get_custom_tags(db: Session):
    return db.query(models.CustomTag).all()

# ========== Report Generation ==========
def get_daily_report(db: Session, date: datetime):
    tasks = get_tasks(db, date=date)
    return {
        'date': date.strftime('%Y-%m-%d'),
        'total_tasks': len(tasks),
        'completed_tasks': sum(1 for t in tasks if t.completed),
        'pending_tasks': sum(1 for t in tasks if not t.completed),
        'tasks': tasks
    }

def get_weekly_report(db: Session, week_start: datetime):
    week_end = week_start + timedelta(days=6)
    tasks = db.query(models.Task).filter(
        and_(
            models.Task.date >= week_start,
            models.Task.date <= week_end
        )
    ).all()

    total = len(tasks)
    completed = sum(1 for t in tasks if t.completed)

    return {
        'week_start': week_start.strftime('%Y-%m-%d'),
        'week_end': week_end.strftime('%Y-%m-%d'),
        'week_number': week_start.isocalendar()[1],
        'total_tasks': total,
        'completed_tasks': completed,
        'completion_rate': (completed / total * 100) if total > 0 else 0,
        'tasks': tasks
    }

def get_gantt_data(db: Session, year: int):
    """Get data for Gantt chart visualization"""
    # Filter projects by year
    projects = get_projects(db, year=year)
    gantt_data = []

    # Calculate year date range
    year_start = datetime(year, 1, 1).date()
    year_end = datetime(year, 12, 31).date()

    for project in projects:
        # Get annual goals that either match the year OR have monthly goals overlapping with the year
        all_annual_goals = db.query(models.AnnualGoal).filter(
            models.AnnualGoal.project_id == project.id
        ).all()

        annual_goals = []
        for ag in all_annual_goals:
            # Include if year matches
            if ag.year == year:
                annual_goals.append(ag)
                continue

            # Include if any monthly goal overlaps with the selected year
            has_overlap = db.query(models.MonthlyGoal).filter(
                and_(
                    models.MonthlyGoal.annual_goal_id == ag.id,
                    models.MonthlyGoal.end_date >= year_start,
                    models.MonthlyGoal.start_date <= year_end
                )
            ).first() is not None

            if has_overlap:
                annual_goals.append(ag)

        # Skip projects with no annual goals for this year
        if not annual_goals:
            continue

        project_data = {
            'id': project.id,
            'name': project.name,
            'start_year': project.start_year,
            'end_year': project.end_year,
            'annual_goals': []
        }

        for goal in annual_goals:
            monthly_goals = db.query(models.MonthlyGoal).filter(
                models.MonthlyGoal.annual_goal_id == goal.id
            ).all()

            goal_data = {
                'id': goal.id,
                'name': goal.name,
                'total_tasks': goal.total_tasks,
                'completed_tasks': goal.completed_tasks,
                'monthly_goals': [
                    {
                        'id': mg.id,
                        'name': mg.name,
                        'start_date': mg.start_date.isoformat() if mg.start_date else None,
                        'end_date': mg.end_date.isoformat() if mg.end_date else None,
                        'status': mg.status,
                        'total_tasks': mg.total_tasks,
                        'completed_tasks': mg.completed_tasks
                    }
                    for mg in monthly_goals
                ]
            }
            project_data['annual_goals'].append(goal_data)

        gantt_data.append(project_data)

    return gantt_data

# ========== Delete Functions ==========
def delete_project(db: Session, project_id: int):
    """Delete a project and all its associated goals and tasks"""
    db_project = get_project(db, project_id)
    if db_project:
        # First delete all annual goals (which will cascade to monthly goals and tasks)
        annual_goals = db.query(models.AnnualGoal).filter(models.AnnualGoal.project_id == project_id).all()
        for goal in annual_goals:
            delete_annual_goal(db, goal.id)

        # Now delete the project
        db.delete(db_project)
        db.commit()
        return True
    return False

def delete_annual_goal(db: Session, goal_id: int):
    """Delete an annual goal and all its associated monthly goals and tasks"""
    db_goal = get_annual_goal(db, goal_id)
    if db_goal:
        # First delete all monthly goals (which will cascade to tasks)
        monthly_goals = db.query(models.MonthlyGoal).filter(models.MonthlyGoal.annual_goal_id == goal_id).all()
        for mg in monthly_goals:
            delete_monthly_goal(db, mg.id)

        # Now delete the annual goal
        db.delete(db_goal)
        db.commit()
        return True
    return False

def delete_monthly_goal(db: Session, goal_id: int):
    """Delete a monthly goal and unlink associated tasks"""
    db_goal = get_monthly_goal(db, goal_id)
    if db_goal:
        # Unlink all tasks from this monthly goal (don't delete tasks, just unlink)
        tasks = db.query(models.Task).filter(models.Task.monthly_goal_id == goal_id).all()
        for task in tasks:
            task.monthly_goal_id = None

        # Delete the monthly goal
        db.delete(db_goal)
        db.commit()
        return True
    return False

def delete_weekly_goal(db: Session, goal_id: int):
    """Delete a weekly goal and unlink associated tasks"""
    db_goal = get_weekly_goal(db, goal_id)
    if db_goal:
        # Unlink all tasks from this weekly goal (don't delete tasks, just unlink)
        tasks = db.query(models.Task).filter(models.Task.weekly_goal_id == goal_id).all()
        for task in tasks:
            task.weekly_goal_id = None

        # Delete the weekly goal
        db.delete(db_goal)
        db.commit()
        return True
    return False
