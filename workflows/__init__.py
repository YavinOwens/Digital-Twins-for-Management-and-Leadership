"""
Workflows Package

This package contains all workflow execution functions for the CrewAI multi-agent system.
Each workflow function handles a specific number of teams working sequentially.

Available Workflows:
- run_crew_workflow: Single team (Research, Analysis, Writing)
- run_two_team_workflow: Research → Data Strategy
- run_three_team_workflow: Research → Data Strategy → Compliance & Risk
- run_four_team_workflow: Research → Data Strategy → Compliance & Risk → Information Management
- run_five_team_workflow: Research → Data Strategy → Compliance & Risk → Information Management → Tender Response
- run_six_team_workflow: Research → Data Strategy → Compliance & Risk → Information Management → Tender Response → Project Delivery
- run_seven_team_workflow: Research → Data Strategy → Compliance & Risk → Information Management → Tender Response → Project Delivery → Technical Documentation
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
