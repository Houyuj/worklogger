#!/usr/bin/env python3
"""
Sample Data Initialization Script
Creates sample projects, goals, tasks, and experiments for demonstration
"""

import sys
import os
from datetime import datetime, timedelta

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.database import SessionLocal, engine
from backend import models

def init_sample_data():
    """Initialize database with sample data"""

    # Create tables
    models.Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        # Check if data already exists
        if db.query(models.Project).count() > 0:
            print("Database already contains data. Skipping initialization.")
            return

        print("Initializing sample data...")

        # Create Projects
        project1 = models.Project(
            name="Platform Development",
            description="Core platform features and infrastructure"
        )
        project2 = models.Project(
            name="Research & Innovation",
            description="Technology evaluation and experimental features"
        )
        project3 = models.Project(
            name="Infrastructure Upgrade",
            description="DevOps and infrastructure improvements"
        )

        db.add_all([project1, project2, project3])
        db.commit()

        # Create Annual Goals for Project 1
        annual_goal1_1 = models.AnnualGoal(
            project_id=project1.id,
            name="User Authentication System",
            description="Complete authentication and authorization system",
            year=2025,
            total_tasks=40,
            completed_tasks=35
        )
        annual_goal1_2 = models.AnnualGoal(
            project_id=project1.id,
            name="API Development",
            description="RESTful and GraphQL API development",
            year=2025,
            total_tasks=30,
            completed_tasks=22
        )
        annual_goal1_3 = models.AnnualGoal(
            project_id=project1.id,
            name="Frontend Integration",
            description="User interface and frontend components",
            year=2025,
            total_tasks=25,
            completed_tasks=0
        )

        # Create Annual Goals for Project 2
        annual_goal2_1 = models.AnnualGoal(
            project_id=project2.id,
            name="Technology Evaluation",
            description="Framework and technology comparison",
            year=2025,
            total_tasks=20,
            completed_tasks=20
        )
        annual_goal2_2 = models.AnnualGoal(
            project_id=project2.id,
            name="Performance Optimization",
            description="System performance improvements",
            year=2025,
            total_tasks=15,
            completed_tasks=10
        )
        annual_goal2_3 = models.AnnualGoal(
            project_id=project2.id,
            name="Experimental Features",
            description="AI integration and advanced features",
            year=2025,
            total_tasks=12,
            completed_tasks=12
        )

        # Create Annual Goals for Project 3
        annual_goal3_1 = models.AnnualGoal(
            project_id=project3.id,
            name="CI/CD Pipeline",
            description="Automated testing and deployment",
            year=2025,
            total_tasks=10,
            completed_tasks=10
        )
        annual_goal3_2 = models.AnnualGoal(
            project_id=project3.id,
            name="Monitoring & Alerting",
            description="System monitoring and alerting infrastructure",
            year=2025,
            total_tasks=15,
            completed_tasks=10
        )

        db.add_all([
            annual_goal1_1, annual_goal1_2, annual_goal1_3,
            annual_goal2_1, annual_goal2_2, annual_goal2_3,
            annual_goal3_1, annual_goal3_2
        ])
        db.commit()

        # Create Monthly Goals
        monthly_goals = [
            # Project 1 - Goal 1
            models.MonthlyGoal(
                annual_goal_id=annual_goal1_1.id,
                name="JWT Implementation",
                description="JWT token-based authentication",
                start_week=40,
                end_week=44,
                status="completed",
                total_tasks=15,
                completed_tasks=15
            ),
            models.MonthlyGoal(
                annual_goal_id=annual_goal1_1.id,
                name="OAuth Integration",
                description="OAuth 2.0 provider integration",
                start_week=45,
                end_week=50,
                status="in-progress",
                total_tasks=15,
                completed_tasks=12
            ),
            # Project 1 - Goal 2
            models.MonthlyGoal(
                annual_goal_id=annual_goal1_2.id,
                name="REST Endpoints",
                description="RESTful API endpoints",
                start_week=44,
                end_week=48,
                status="completed",
                total_tasks=12,
                completed_tasks=12
            ),
            models.MonthlyGoal(
                annual_goal_id=annual_goal1_2.id,
                name="GraphQL Layer",
                description="GraphQL API layer",
                start_week=49,
                end_week=52,
                status="in-progress",
                total_tasks=8,
                completed_tasks=6
            ),
            # Project 2 - Goal 1
            models.MonthlyGoal(
                annual_goal_id=annual_goal2_1.id,
                name="Framework Comparison",
                description="Compare web frameworks",
                start_week=1,
                end_week=8,
                status="completed",
                total_tasks=10,
                completed_tasks=10
            ),
            models.MonthlyGoal(
                annual_goal_id=annual_goal2_1.id,
                name="Performance Testing",
                description="Load and performance testing",
                start_week=9,
                end_week=13,
                status="completed",
                total_tasks=10,
                completed_tasks=10
            ),
            # Project 2 - Goal 2
            models.MonthlyGoal(
                annual_goal_id=annual_goal2_2.id,
                name="Caching Strategy",
                description="Implement caching layer",
                start_week=14,
                end_week=22,
                status="completed",
                total_tasks=8,
                completed_tasks=8
            ),
            models.MonthlyGoal(
                annual_goal_id=annual_goal2_2.id,
                name="Database Optimization",
                description="Query and index optimization",
                start_week=23,
                end_week=26,
                status="terminated",
                total_tasks=7,
                completed_tasks=2
            ),
            # Project 2 - Goal 3
            models.MonthlyGoal(
                annual_goal_id=annual_goal2_3.id,
                name="AI Integration Prototype",
                description="AI/ML features prototype",
                start_week=27,
                end_week=39,
                status="completed",
                total_tasks=12,
                completed_tasks=12
            ),
            # Project 3 - Goal 1
            models.MonthlyGoal(
                annual_goal_id=annual_goal3_1.id,
                name="Pipeline Setup",
                description="CI/CD pipeline configuration",
                start_week=1,
                end_week=9,
                status="completed",
                total_tasks=10,
                completed_tasks=10
            ),
            # Project 3 - Goal 2
            models.MonthlyGoal(
                annual_goal_id=annual_goal3_2.id,
                name="Metrics Collection",
                description="System metrics and dashboards",
                start_week=10,
                end_week=22,
                status="completed",
                total_tasks=8,
                completed_tasks=8
            ),
            models.MonthlyGoal(
                annual_goal_id=annual_goal3_2.id,
                name="Alert System",
                description="Alerting and notification system",
                start_week=49,
                end_week=52,
                status="in-progress",
                total_tasks=7,
                completed_tasks=2
            ),
        ]

        db.add_all(monthly_goals)
        db.commit()

        # Create Weekly Goals
        weekly_goals = [
            models.WeeklyGoal(name="Sprint 12 Tasks", description="Current sprint tasks"),
            models.WeeklyGoal(name="Bug Fixes Week 50", description="Bug fixing tasks"),
            models.WeeklyGoal(name="Code Review Tasks", description="Code review and QA"),
        ]

        db.add_all(weekly_goals)
        db.commit()

        # Create some sample tasks for today
        today = datetime.now()

        tasks = [
            models.Task(
                title="Implement JWT authentication middleware",
                description="Created login/signup endpoints and token validation logic",
                date=today,
                completed=True,
                completed_at=today - timedelta(hours=2),
                monthly_goal_id=monthly_goals[1].id,  # OAuth Integration
                weekly_goal_id=weekly_goals[0].id
            ),
            models.Task(
                title="Review pull request #234",
                description="",
                date=today,
                completed=False,
                monthly_goal_id=monthly_goals[1].id,
                weekly_goal_id=weekly_goals[2].id
            ),
            models.Task(
                title="Update API documentation",
                description="",
                date=today,
                completed=False,
                monthly_goal_id=monthly_goals[3].id,  # GraphQL Layer
                weekly_goal_id=None
            ),
            models.Task(
                title="Deploy v2.1.0 to production",
                description="",
                date=today,
                completed=True,
                completed_at=today - timedelta(hours=5),
                monthly_goal_id=monthly_goals[1].id,
                weekly_goal_id=None
            ),
        ]

        db.add_all(tasks)
        db.commit()

        # Create Custom Tags
        tags = [
            models.CustomTag(name="Performance"),
            models.CustomTag(name="Redis"),
            models.CustomTag(name="Caching"),
            models.CustomTag(name="Backend"),
            models.CustomTag(name="Database"),
            models.CustomTag(name="Indexes"),
            models.CustomTag(name="GraphQL"),
            models.CustomTag(name="API Design"),
            models.CustomTag(name="Research"),
        ]

        db.add_all(tags)
        db.commit()

        # Create Experiments
        experiment1 = models.Experiment(
            name="Cache Optimization Experiment",
            status="completed",
            annual_goal_id=annual_goal1_2.id,
            monthly_goal_id=monthly_goals[2].id,  # REST Endpoints
            hypothesis="Implementing Redis caching for frequently accessed API endpoints will reduce average response time by at least 30%.",
            methodology="""1. Identified top 10 most-called endpoints using production logs
2. Set up Redis cache with 5-minute TTL for read operations
3. Measured performance over 1,000+ requests with Apache Bench
4. Monitored database query counts and cache hit rates""",
            results="""{"table": [
                {"metric": "Avg Response Time", "before": "450ms", "after": "360ms", "improvement": "20%"},
                {"metric": "95th Percentile", "before": "650ms", "after": "480ms", "improvement": "26%"},
                {"metric": "DB Queries", "before": "1250/min", "after": "815/min", "improvement": "35%"},
                {"metric": "Cache Hit Rate", "before": "-", "after": "78%", "improvement": "-"}
            ]}""",
            conclusion="While the 20% improvement fell short of the 30% target, results are significant. Approved for production deployment with plans for further optimization through cache warming strategies."
        )
        experiment1.custom_tags = [tags[0], tags[1], tags[2], tags[3]]  # Performance, Redis, Caching, Backend

        experiment2 = models.Experiment(
            name="Database Query Optimization",
            status="in-progress",
            annual_goal_id=annual_goal1_2.id,
            monthly_goal_id=monthly_goals[2].id,
            hypothesis="Adding composite indexes on frequently queried columns will improve query performance by at least 40%.",
            methodology="",
            results="",
            conclusion="",
            progress_notes="""Day 1: Analyzed slow query logs - identified 23 problematic queries
Day 2: Created test database with production-like data volume
Day 3: Testing different index combinations..."""
        )
        experiment2.custom_tags = [tags[4], tags[0], tags[5]]  # Database, Performance, Indexes

        experiment3 = models.Experiment(
            name="GraphQL vs REST API Performance",
            status="planned",
            annual_goal_id=annual_goal2_1.id,
            monthly_goal_id=None,
            hypothesis="Migrating to GraphQL will reduce over-fetching and result in 25% smaller payload sizes.",
            methodology="""1. Implement GraphQL schema for existing REST endpoints
2. Create test scenarios
3. Measure payload sizes and response times
4. Evaluate developer experience""",
            results="",
            conclusion=""
        )
        experiment3.custom_tags = [tags[6], tags[7], tags[8]]  # GraphQL, API Design, Research

        # Link tasks to experiment
        experiment2.tasks = [tasks[0]]  # Link JWT task to DB optimization experiment

        db.add_all([experiment1, experiment2, experiment3])
        db.commit()

        print("✓ Created 3 projects")
        print("✓ Created 9 annual goals")
        print("✓ Created 12 monthly goals")
        print("✓ Created 3 weekly goals")
        print("✓ Created sample tasks")
        print("✓ Created 3 experiments with custom tags")
        print("\nSample data initialization completed successfully!")

    except Exception as e:
        print(f"Error initializing sample data: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    init_sample_data()
