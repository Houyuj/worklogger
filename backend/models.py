from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Date, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

# Association table for task-experiment relationship
task_experiment_association = Table(
    'task_experiment_association',
    Base.metadata,
    Column('task_id', Integer, ForeignKey('tasks.id')),
    Column('experiment_id', Integer, ForeignKey('experiments.id'))
)

# Association table for experiment custom tags
experiment_tag_association = Table(
    'experiment_tag_association',
    Base.metadata,
    Column('experiment_id', Integer, ForeignKey('experiments.id')),
    Column('tag_id', Integer, ForeignKey('custom_tags.id'))
)

class Project(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    start_year = Column(Integer, nullable=True)
    end_year = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    annual_goals = relationship('AnnualGoal', back_populates='project', cascade='all, delete-orphan')

class AnnualGoal(Base):
    __tablename__ = 'annual_goals'

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    year = Column(Integer, nullable=False)
    total_tasks = Column(Integer, default=0)
    completed_tasks = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    project = relationship('Project', back_populates='annual_goals')
    monthly_goals = relationship('MonthlyGoal', back_populates='annual_goal', cascade='all, delete-orphan')

class MonthlyGoal(Base):
    __tablename__ = 'monthly_goals'

    id = Column(Integer, primary_key=True, index=True)
    annual_goal_id = Column(Integer, ForeignKey('annual_goals.id'), nullable=False)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    start_date = Column(Date, nullable=False)  # Date range instead of week numbers
    end_date = Column(Date, nullable=False)    # Date range instead of week numbers
    status = Column(String(50), default='planned')  # planned, in-progress, completed, terminated
    total_tasks = Column(Integer, default=0)
    completed_tasks = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    annual_goal = relationship('AnnualGoal', back_populates='monthly_goals')
    tasks = relationship('Task', back_populates='monthly_goal')

class WeeklyGoal(Base):
    __tablename__ = 'weekly_goals'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    week_number = Column(Integer)  # Optional week number
    created_at = Column(DateTime, default=datetime.utcnow)

    tasks = relationship('Task', back_populates='weekly_goal')

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(300), nullable=False)
    description = Column(Text)
    date = Column(DateTime, nullable=False, default=datetime.utcnow)
    completed = Column(Boolean, default=False)
    completed_at = Column(DateTime, nullable=True)

    # Goal relationships
    monthly_goal_id = Column(Integer, ForeignKey('monthly_goals.id'))
    weekly_goal_id = Column(Integer, ForeignKey('weekly_goals.id'))

    monthly_goal = relationship('MonthlyGoal', back_populates='tasks')
    weekly_goal = relationship('WeeklyGoal', back_populates='tasks')
    experiments = relationship('Experiment', secondary=task_experiment_association, back_populates='tasks')

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Experiment(Base):
    __tablename__ = 'experiments'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(300), nullable=False)
    status = Column(String(50), default='planned')  # planned, in-progress, completed

    # Goal relationships
    annual_goal_id = Column(Integer, ForeignKey('annual_goals.id'))
    monthly_goal_id = Column(Integer, ForeignKey('monthly_goals.id'))

    # Experiment content
    hypothesis = Column(Text)
    methodology = Column(Text)
    results = Column(Text)  # Can store JSON for table data
    conclusion = Column(Text)
    progress_notes = Column(Text)
    images_json = Column(Text, default='[]')  # JSON array of {id, filename, data} for embedded images

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    tasks = relationship('Task', secondary=task_experiment_association, back_populates='experiments')
    custom_tags = relationship('CustomTag', secondary=experiment_tag_association, back_populates='experiments')

class CustomTag(Base):
    __tablename__ = 'custom_tags'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    experiments = relationship('Experiment', secondary=experiment_tag_association, back_populates='custom_tags')
