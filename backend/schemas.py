from pydantic import BaseModel
from typing import Literal, Optional, List
from datetime import datetime, date

# Local user schemas
class UserCreate(BaseModel):
    name: str

# Project schemas
class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    start_year: Optional[int] = None
    end_year: Optional[int] = None

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    start_year: Optional[int] = None
    end_year: Optional[int] = None
    archived: Optional[bool] = None

class Project(ProjectBase):
    id: int
    created_at: datetime
    archived: bool = False

    class Config:
        from_attributes = True

# Annual Goal schemas
class AnnualGoalBase(BaseModel):
    name: str
    description: Optional[str] = None
    year: int
    project_id: int

class AnnualGoalCreate(AnnualGoalBase):
    pass

class AnnualGoalUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    year: Optional[int] = None
    archived: Optional[bool] = None

class AnnualGoal(AnnualGoalBase):
    id: int
    total_tasks: int
    completed_tasks: int
    created_at: datetime
    archived: bool = False

    class Config:
        from_attributes = True

# Monthly Goal schemas
class MonthlyGoalBase(BaseModel):
    name: str
    description: Optional[str] = None
    annual_goal_id: int
    start_date: date
    end_date: date
    status: str = 'in-progress'

class MonthlyGoalCreate(MonthlyGoalBase):
    pass

class MonthlyGoalUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: Optional[str] = None
    archived: Optional[bool] = None

class MonthlyGoal(MonthlyGoalBase):
    id: int
    total_tasks: int
    completed_tasks: int
    created_at: datetime
    archived: bool = False

    class Config:
        from_attributes = True

# Weekly Goal schemas
class WeeklyGoalBase(BaseModel):
    name: str
    description: Optional[str] = None
    week_number: Optional[int] = None
    monthly_goal_id: Optional[int] = None
    year: Optional[int] = None
    week_start: Optional[date] = None
    week_end: Optional[date] = None
    status: Literal['planned', 'in-progress', 'completed', 'terminated'] = 'planned'

class WeeklyGoalCreate(WeeklyGoalBase):
    pass

class WeeklyGoalUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    monthly_goal_id: Optional[int] = None
    year: Optional[int] = None
    week_start: Optional[date] = None
    week_end: Optional[date] = None
    status: Optional[Literal['planned', 'in-progress', 'completed', 'terminated']] = None
    archived: Optional[bool] = None

class WeeklyGoal(WeeklyGoalBase):
    id: int
    created_at: datetime
    archived: bool = False

    class Config:
        from_attributes = True

# Task schemas
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    date: Optional[datetime] = None
    project_id: Optional[int] = None
    annual_goal_id: Optional[int] = None
    monthly_goal_id: Optional[int] = None
    weekly_goal_id: Optional[int] = None
    priority: Literal['low', 'normal', 'high'] = 'normal'
    workflow_status: Literal['unclassified', 'planned', 'todo', 'blocked', 'waiting', 'completed'] = 'unclassified'

class TaskCreate(TaskBase):
    experiment_ids: Optional[List[int]] = []

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    date: Optional[datetime] = None
    completed: Optional[bool] = None
    project_id: Optional[int] = None
    annual_goal_id: Optional[int] = None
    monthly_goal_id: Optional[int] = None
    weekly_goal_id: Optional[int] = None
    priority: Optional[Literal['low', 'normal', 'high']] = None
    workflow_status: Optional[Literal['unclassified', 'planned', 'todo', 'blocked', 'waiting', 'completed']] = None
    experiment_ids: Optional[List[int]] = None

class Task(TaskBase):
    id: int
    completed: bool
    completed_at: Optional[datetime] = None
    is_inbox: bool
    created_at: datetime
    updated_at: datetime
    experiments: List['Experiment'] = []

    class Config:
        from_attributes = True

# Experiment schemas
class ExperimentBase(BaseModel):
    name: str
    status: str = 'planned'
    annual_goal_id: Optional[int] = None
    monthly_goal_id: Optional[int] = None
    content: Optional[str] = None
    hypothesis: Optional[str] = None
    methodology: Optional[str] = None
    results: Optional[str] = None
    conclusion: Optional[str] = None
    progress_notes: Optional[str] = None
    images_json: Optional[str] = '[]'

class ExperimentCreate(ExperimentBase):
    custom_tag_names: Optional[List[str]] = []

class ExperimentUpdate(BaseModel):
    name: Optional[str] = None
    status: Optional[str] = None
    content: Optional[str] = None
    hypothesis: Optional[str] = None
    methodology: Optional[str] = None
    results: Optional[str] = None
    conclusion: Optional[str] = None
    progress_notes: Optional[str] = None
    images_json: Optional[str] = None
    custom_tag_names: Optional[List[str]] = None

class Experiment(ExperimentBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Custom Tag schemas
class CustomTagBase(BaseModel):
    name: str

class CustomTagCreate(CustomTagBase):
    pass

class CustomTag(CustomTagBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Report schemas
class DailyReport(BaseModel):
    date: str
    total_tasks: int
    completed_tasks: int
    pending_tasks: int
    tasks: List[Task]

class WeeklyReport(BaseModel):
    week_start: str
    week_end: str
    week_number: int
    total_tasks: int
    completed_tasks: int
    completion_rate: float
    tasks_by_goal: dict

class MonthlyReport(BaseModel):
    month: str
    year: int
    total_tasks: int
    completed_tasks: int
    completion_rate: float
    goals_progress: List[dict]
