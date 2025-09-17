"""
Workflow Manager Module

This module contains all workflow execution functions for the CrewAI multi-agent system.
Each workflow type is organized in its own module for better maintainability.
"""

from .workflow_executor import (
    run_crew_workflow,
    run_two_team_workflow,
    run_three_team_workflow,
    run_four_team_workflow,
    run_five_team_workflow,
    run_six_team_workflow,
    run_seven_team_workflow,
    perform_workflow_presearch
)

__all__ = [
    'run_crew_workflow',
    'run_two_team_workflow',
    'run_three_team_workflow',
    'run_four_team_workflow',
    'run_five_team_workflow',
    'run_six_team_workflow',
    'run_seven_team_workflow',
    'perform_workflow_presearch'
]
