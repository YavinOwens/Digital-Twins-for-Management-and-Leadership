"""
Agent Tasks Package for CrewAI Multi-Agent Workflow

This package contains all the CrewAI tasks used in the multi-agent workflow.
Each task is organized in its own module for better maintainability and reusability.
"""

from .research_task import create_research_task
from .analysis_task import create_analysis_task
from .writing_task import create_writing_task
from .task_factory import create_crew_tasks, create_crew_tasks_with_data

__all__ = [
    'create_research_task',
    'create_analysis_task',
    'create_writing_task',
    'create_crew_tasks',
    'create_crew_tasks_with_data'
]
