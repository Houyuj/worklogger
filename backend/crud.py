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

def get_projects(db: Session, year: Optional[int] = None, include_archived: bool = False):
    query = db.query(models.Project)
    if not include_archived:
        query = query.filter(models.Project.archived == False)
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

def get_annual_goals(db: Session, project_id: Optional[int] = None, year: Optional[int] = None, include_archived: bool = False):
    query = db.query(models.AnnualGoal)
    if not include_archived:
        query = query.filter(models.AnnualGoal.archived == False)
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

def get_monthly_goals(db: Session, annual_goal_id: Optional[int] = None, include_archived: bool = False):
    query = db.query(models.MonthlyGoal)
    if not include_archived:
        query = query.filter(models.MonthlyGoal.archived == False)
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
    goal_data = goal.model_dump()
    if goal_data.get('week_start') and goal_data.get('week_end') and goal_data['week_start'] > goal_data['week_end']:
        raise ValueError('Weekly plan end date must be on or after its start date')
    if goal_data.get('week_start') and not goal_data.get('year'):
        goal_data['year'] = goal_data['week_start'].year
    if goal_data.get('monthly_goal_id') and not get_monthly_goal(db, goal_data['monthly_goal_id']):
        raise ValueError('Monthly goal not found')
    db_goal = models.WeeklyGoal(**goal_data)
    db.add(db_goal)
    db.commit()
    db.refresh(db_goal)
    return db_goal

def get_weekly_goals(db: Session, monthly_goal_id: Optional[int] = None, year: Optional[int] = None, include_archived: bool = False):
    query = db.query(models.WeeklyGoal)
    if not include_archived:
        query = query.filter(models.WeeklyGoal.archived == False)
    if monthly_goal_id is not None:
        query = query.filter(models.WeeklyGoal.monthly_goal_id == monthly_goal_id)
    if year is not None:
        query = query.filter(models.WeeklyGoal.year == year)
    return query.order_by(models.WeeklyGoal.week_start.asc(), models.WeeklyGoal.created_at.desc()).all()

def get_weekly_goal(db: Session, goal_id: int):
    return db.query(models.WeeklyGoal).filter(models.WeeklyGoal.id == goal_id).first()

def update_weekly_goal(db: Session, goal_id: int, goal_update: schemas.WeeklyGoalUpdate):
    db_goal = get_weekly_goal(db, goal_id)
    if not db_goal:
        return None
    update_data = goal_update.model_dump(exclude_unset=True)
    start_date = update_data.get('week_start', db_goal.week_start)
    end_date = update_data.get('week_end', db_goal.week_end)
    if start_date and end_date and start_date > end_date:
        raise ValueError('Weekly plan end date must be on or after its start date')
    if update_data.get('monthly_goal_id') and not get_monthly_goal(db, update_data['monthly_goal_id']):
        raise ValueError('Monthly goal not found')
    for key, value in update_data.items():
        setattr(db_goal, key, value)
    if start_date and not db_goal.year:
        db_goal.year = start_date.year
    db.commit()
    db.refresh(db_goal)
    return db_goal

# ========== Task CRUD ==========
def _resolve_task_hierarchy(db: Session, values: dict):
    """Complete and validate a task's project -> annual -> monthly -> weekly chain."""
    project_id = values.get('project_id')
    annual_goal_id = values.get('annual_goal_id')
    monthly_goal_id = values.get('monthly_goal_id')
    weekly_goal_id = values.get('weekly_goal_id')

    if weekly_goal_id:
        weekly_goal = get_weekly_goal(db, weekly_goal_id)
        if not weekly_goal:
            raise ValueError('Weekly plan not found')
        if weekly_goal.monthly_goal_id:
            if monthly_goal_id and monthly_goal_id != weekly_goal.monthly_goal_id:
                raise ValueError('Weekly plan belongs to a different monthly goal')
            monthly_goal_id = weekly_goal.monthly_goal_id

    if monthly_goal_id:
        monthly_goal = get_monthly_goal(db, monthly_goal_id)
        if not monthly_goal:
            raise ValueError('Monthly goal not found')
        if annual_goal_id and annual_goal_id != monthly_goal.annual_goal_id:
            raise ValueError('Monthly goal belongs to a different annual goal')
        annual_goal_id = monthly_goal.annual_goal_id

    if annual_goal_id:
        annual_goal = get_annual_goal(db, annual_goal_id)
        if not annual_goal:
            raise ValueError('Annual goal not found')
        if project_id and project_id != annual_goal.project_id:
            raise ValueError('Annual goal belongs to a different project')
        project_id = annual_goal.project_id

    if project_id and not get_project(db, project_id):
        raise ValueError('Project not found')

    has_specific_goal = bool(annual_goal_id or monthly_goal_id or weekly_goal_id)
    if not has_specific_goal:
        # A project alone is useful context, but does not count as a planned
        # research goal. Keep unclassified tasks independent so they are easy
        # to find and cannot silently enter goal reporting.
        project_id = None

    values.update({
        'project_id': project_id,
        'annual_goal_id': annual_goal_id,
        'monthly_goal_id': monthly_goal_id,
        'weekly_goal_id': weekly_goal_id,
    })
    values['is_inbox'] = False
    # Planning status is derived from the hierarchy, rather than chosen in a
    # separate control. Completion still overrides this later in update_task.
    if not has_specific_goal:
        values['workflow_status'] = 'unclassified'
    elif values.get('workflow_status') not in ('blocked', 'waiting', 'completed'):
        values['workflow_status'] = 'planned'
    return values


def _set_task_experiments(db: Session, db_task, experiment_ids):
    if experiment_ids is None:
        return
    experiments = db.query(models.Experiment).filter(
        models.Experiment.id.in_(experiment_ids)
    ).all()
    if len(experiments) != len(set(experiment_ids)):
        raise ValueError('One or more linked protocols were not found')
    db_task.experiments = experiments


def _apply_task_values(db: Session, db_task, update_data: dict, experiment_ids=None):
    hierarchy_values = {
        field: update_data.get(field, getattr(db_task, field))
        for field in ('project_id', 'annual_goal_id', 'monthly_goal_id', 'weekly_goal_id')
    }
    hierarchy_values['workflow_status'] = update_data.get('workflow_status', db_task.workflow_status)
    update_data = {**update_data, **_resolve_task_hierarchy(db, hierarchy_values)}

    if update_data.get('completed') is True:
        update_data['completed_at'] = datetime.utcnow()
        update_data['workflow_status'] = 'completed'
    elif update_data.get('completed') is False:
        update_data['completed_at'] = None
        if update_data.get('workflow_status') == 'completed':
            update_data['workflow_status'] = 'todo'

    for key, value in update_data.items():
        setattr(db_task, key, value)
    _set_task_experiments(db, db_task, experiment_ids)
    return db_task


def create_task(db: Session, task: schemas.TaskCreate):
    task_data = _resolve_task_hierarchy(db, task.model_dump(exclude={'experiment_ids'}))
    db_task = models.Task(**task_data)
    _set_task_experiments(db, db_task, task.experiment_ids)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    if db_task.monthly_goal_id:
        update_goal_task_counts(db, db_task.monthly_goal_id)
    return db_task


def get_tasks(
    db: Session,
    date: Optional[datetime] = None,
    completed: Optional[bool] = None,
    inbox: Optional[bool] = None
):
    query = db.query(models.Task)
    if date:
        query = query.filter(func.date(models.Task.date) == date.date())
    if completed is not None:
        query = query.filter(models.Task.completed == completed)
    if inbox is not None:
        query = query.filter(models.Task.is_inbox == inbox)
    return query.order_by(models.Task.date.desc()).all()


def get_task(db: Session, task_id: int):
    return db.query(models.Task).filter(models.Task.id == task_id).first()


def update_task(db: Session, task_id: int, task_update: schemas.TaskUpdate):
    db_task = get_task(db, task_id)
    if db_task:
        old_monthly_goal_id = db_task.monthly_goal_id
        update_data = task_update.model_dump(exclude_unset=True, exclude={'experiment_ids'})
        _apply_task_values(db, db_task, update_data, task_update.experiment_ids)
        db.commit()
        db.refresh(db_task)
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
        'content': source_experiment.content,
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
    tasks = get_tasks(db, date=date, inbox=False)
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
            models.Task.date <= week_end,
            models.Task.is_inbox == False
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
            ).order_by(models.MonthlyGoal.start_date, models.MonthlyGoal.id).all()

            monthly_goal_data = []
            for monthly_goal in monthly_goals:
                weekly_goals = db.query(models.WeeklyGoal).filter(
                    models.WeeklyGoal.monthly_goal_id == monthly_goal.id
                ).order_by(models.WeeklyGoal.week_start, models.WeeklyGoal.id).all()

                weekly_goal_data = []
                for weekly_goal in weekly_goals:
                    task_range = db.query(
                        func.min(models.Task.date),
                        func.max(models.Task.date)
                    ).filter(models.Task.weekly_goal_id == weekly_goal.id).one()
                    earliest_task_date, latest_task_date = task_range
                    weekly_goal_data.append({
                        'id': weekly_goal.id,
                        'name': weekly_goal.name,
                        'status': weekly_goal.status,
                        'task_start_date': earliest_task_date.date().isoformat() if earliest_task_date else None,
                        'task_end_date': latest_task_date.date().isoformat() if latest_task_date else None,
                    })

                monthly_goal_data.append({
                    'id': monthly_goal.id,
                    'name': monthly_goal.name,
                    'start_date': monthly_goal.start_date.isoformat() if monthly_goal.start_date else None,
                    'end_date': monthly_goal.end_date.isoformat() if monthly_goal.end_date else None,
                    'status': monthly_goal.status,
                    'total_tasks': monthly_goal.total_tasks,
                    'completed_tasks': monthly_goal.completed_tasks,
                    'weekly_goals': weekly_goal_data,
                })

            goal_data = {
                'id': goal.id,
                'name': goal.name,
                'total_tasks': goal.total_tasks,
                'completed_tasks': goal.completed_tasks,
                'monthly_goals': monthly_goal_data
            }
            project_data['annual_goals'].append(goal_data)

        gantt_data.append(project_data)

    return gantt_data

# ========== Delete Functions ==========
def delete_project(db: Session, project_id: int):
    """Delete only an empty project; historic work must be archived instead."""
    db_project = get_project(db, project_id)
    if db_project:
        has_annual_goals = db.query(models.AnnualGoal.id).filter(models.AnnualGoal.project_id == project_id).first()
        has_tasks = db.query(models.Task.id).filter(models.Task.project_id == project_id).first()
        if has_annual_goals or has_tasks:
            raise ValueError('Only empty projects can be deleted. Archive this project to preserve its history.')

        db.delete(db_project)
        db.commit()
        return True
    return False

def delete_annual_goal(db: Session, goal_id: int):
    """Delete only an empty annual goal; historic work must be archived instead."""
    db_goal = get_annual_goal(db, goal_id)
    if db_goal:
        has_monthly_goals = db.query(models.MonthlyGoal.id).filter(models.MonthlyGoal.annual_goal_id == goal_id).first()
        has_tasks = db.query(models.Task.id).filter(models.Task.annual_goal_id == goal_id).first()
        if has_monthly_goals or has_tasks:
            raise ValueError('Only empty annual goals can be deleted. Archive this goal to preserve its history.')

        db.delete(db_goal)
        db.commit()
        return True
    return False

def delete_monthly_goal(db: Session, goal_id: int):
    """Delete only an empty monthly goal; historic work must be archived instead."""
    db_goal = get_monthly_goal(db, goal_id)
    if db_goal:
        has_weekly_goals = db.query(models.WeeklyGoal.id).filter(models.WeeklyGoal.monthly_goal_id == goal_id).first()
        has_tasks = db.query(models.Task.id).filter(models.Task.monthly_goal_id == goal_id).first()
        if has_weekly_goals or has_tasks:
            raise ValueError('Only empty monthly goals can be deleted. Archive this goal to preserve its history.')

        db.delete(db_goal)
        db.commit()
        return True
    return False

def delete_weekly_goal(db: Session, goal_id: int):
    """Delete only an empty weekly goal; historic work must be archived instead."""
    db_goal = get_weekly_goal(db, goal_id)
    if db_goal:
        has_tasks = db.query(models.Task.id).filter(models.Task.weekly_goal_id == goal_id).first()
        if has_tasks:
            raise ValueError('Only empty weekly goals can be deleted. Archive this goal to preserve its history.')

        db.delete(db_goal)
        db.commit()
        return True
    return False
