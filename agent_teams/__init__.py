"""
Agent Teams Module

This module contains all agent teams organized by functionality.
Each team has its own folder with agents and tasks.
"""

# Import agent creation functions from each team
from .research_analysis import (
    create_research_analysis_agents,
    create_research_analysis_agents_with_context,
    create_research_analysis_tasks,
    create_research_analysis_tasks_with_data
)

from .data_strategy import (
    create_data_strategy_agents,
    create_data_strategy_agents_with_context,
    create_data_strategy_tasks,
    create_data_strategy_tasks_with_data
)

from .compliance_risk import (
    create_compliance_risk_team,
    create_compliance_risk_agents_with_context,
    create_compliance_risk_tasks,
    create_compliance_risk_tasks_with_data
)

from .information_management import (
    create_information_management_team,
    create_information_management_agents_with_context,
    create_information_management_tasks,
    create_information_management_tasks_with_data
)

from .tender_response import (
    create_tender_response_team,
    create_tender_response_agents_with_context,
    create_tender_response_tasks,
    create_tender_response_tasks_with_data
)

from .project_delivery import (
    create_project_delivery_team,
    create_project_delivery_agents_with_context,
    create_project_delivery_tasks,
    create_project_delivery_tasks_with_data
)

from .technical_documentation import (
    create_technical_documentation_team,
    create_technical_documentation_agents_with_context,
    create_technical_documentation_tasks,
    create_technical_documentation_tasks_with_data
)

__all__ = [
    # Research & Analysis Team
    'create_research_analysis_agents',
    'create_research_analysis_agents_with_context',
    'create_research_analysis_tasks',
    'create_research_analysis_tasks_with_data',
    
    # Data Strategy Team
    'create_data_strategy_agents',
    'create_data_strategy_agents_with_context',
    'create_data_strategy_tasks',
    'create_data_strategy_tasks_with_data',
    
    # Compliance & Risk Team
    'create_compliance_risk_team',
    'create_compliance_risk_agents_with_context',
    'create_compliance_risk_tasks',
    'create_compliance_risk_tasks_with_data',
    
    # Information Management Team
    'create_information_management_team',
    'create_information_management_agents_with_context',
    'create_information_management_tasks',
    'create_information_management_tasks_with_data',
    
    # Tender Response Team
    'create_tender_response_team',
    'create_tender_response_agents_with_context',
    'create_tender_response_tasks',
    'create_tender_response_tasks_with_data',
    
    # Project Delivery Team
    'create_project_delivery_team',
    'create_project_delivery_agents_with_context',
    'create_project_delivery_tasks',
    'create_project_delivery_tasks_with_data',
    
    # Technical Documentation Team
    'create_technical_documentation_team',
    'create_technical_documentation_agents_with_context',
    'create_technical_documentation_tasks',
    'create_technical_documentation_tasks_with_data'
]
