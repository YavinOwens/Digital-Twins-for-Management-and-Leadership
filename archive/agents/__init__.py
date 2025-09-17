"""
Agents Package for CrewAI Multi-Agent Workflow - ARCHIVED

⚠️  IMPORTANT: This package has been ARCHIVED and is no longer actively maintained.

🚀 NEW LOCATION: Use the agent_teams package instead for all agent functionality.

This package contains archived agent files that are no longer used in the main application.
All agent functionality has been moved to the modular agent_teams structure.

For new development, use:
    from agent_teams.research_analysis import create_research_analysis_agents_with_context
    from agent_teams.data_strategy import create_data_strategy_agents_with_context
    # etc.

See agents/README.md for complete migration guide.
"""

# Legacy agent factory (still available for backward compatibility)
from .agent_factory import create_crew_agents

# Note: All individual agent files have been moved to agents/archive/
# The agent_teams package is now the primary source for all agent functionality

__all__ = [
    # Legacy factory (only remaining function)
    'create_crew_agents'
]
