"""
Dynamic Workflow Executor

This module provides dynamic workflow execution based on user-selected agents and teams.
Replaces the fixed workflow functions with flexible agent selection.
"""

import time
from typing import List, Dict, Any, Optional
from crewai import Crew, Process
from agent_configuration import agent_config, AgentTeam
from local_memory import add_to_memory, search_memory
from agent_tools import search_web

# Import agent creation functions
from agent_teams.research_analysis.agents import create_research_analysis_agents_with_context
from agent_teams.data_strategy.agents import create_data_strategy_agents_with_context
from agent_teams.compliance_risk.agents import create_compliance_risk_agents_with_context
from agent_teams.information_management.agents import create_information_management_agents_with_context
from agent_teams.tender_response.agents import create_tender_response_agents_with_context
from agent_teams.project_delivery.agents import create_project_delivery_agents_with_context
from agent_teams.technical_documentation.agents import create_technical_documentation_agents_with_context

# Import task creation functions
from agent_teams.research_analysis.tasks import create_research_analysis_tasks_with_data
from agent_teams.data_strategy.tasks import create_data_strategy_tasks_with_data
from agent_teams.compliance_risk.tasks import create_compliance_risk_tasks_with_data
from agent_teams.information_management.tasks import create_information_management_tasks_with_data
from agent_teams.tender_response.tasks import create_tender_response_tasks_with_data
from agent_teams.project_delivery.tasks import create_project_delivery_tasks_with_data
from agent_teams.technical_documentation.tasks import create_technical_documentation_tasks_with_data

class DynamicWorkflowExecutor:
    """Executes workflows based on user-selected agents and teams"""
    
    def __init__(self):
        self.agent_creators = {
            AgentTeam.RESEARCH_ANALYSIS: create_research_analysis_agents_with_context,
            AgentTeam.DATA_STRATEGY: create_data_strategy_agents_with_context,
            AgentTeam.COMPLIANCE_RISK: create_compliance_risk_agents_with_context,
            AgentTeam.INFORMATION_MANAGEMENT: create_information_management_agents_with_context,
            AgentTeam.TENDER_RESPONSE: create_tender_response_agents_with_context,
            AgentTeam.PROJECT_DELIVERY: create_project_delivery_agents_with_context,
            AgentTeam.TECHNICAL_DOCUMENTATION: create_technical_documentation_agents_with_context
        }
        
        self.task_creators = {
            AgentTeam.RESEARCH_ANALYSIS: create_research_analysis_tasks_with_data,
            AgentTeam.DATA_STRATEGY: create_data_strategy_tasks_with_data,
            AgentTeam.COMPLIANCE_RISK: create_compliance_risk_tasks_with_data,
            AgentTeam.INFORMATION_MANAGEMENT: create_information_management_tasks_with_data,
            AgentTeam.TENDER_RESPONSE: create_tender_response_tasks_with_data,
            AgentTeam.PROJECT_DELIVERY: create_project_delivery_tasks_with_data,
            AgentTeam.TECHNICAL_DOCUMENTATION: create_technical_documentation_tasks_with_data
        }
    
    def execute_dynamic_workflow(
        self, 
        query: str, 
        llm, 
        conversation_history: Optional[List[Any]] = None,
        use_native_function_calling: bool = False,
        document_context: Optional[str] = None,
        custom_team_selection: Optional[List[AgentTeam]] = None
    ) -> str:
        """
        Execute a dynamic workflow based on selected teams
        
        Args:
            query: User query
            llm: Language model
            conversation_history: Previous conversation context
            use_native_function_calling: Whether to use native function calling
            document_context: Document context
            custom_team_selection: Custom team selection (if None, uses enabled teams)
        
        Returns:
            Workflow execution result
        """
        
        try:
            print(f"🚀 Starting dynamic workflow execution for: {query}")
            
            # Determine which teams to use
            if custom_team_selection:
                teams_to_execute = custom_team_selection
            else:
                teams_to_execute = [team.team for team in agent_config.get_workflow_order()]
            
            if not teams_to_execute:
                return "❌ No teams are enabled. Please enable at least one team in the agent configuration."
            
            print(f"📋 Executing teams: {[team.value for team in teams_to_execute]}")
            
            # Perform pre-search
            print("🔍 Pre-searching data...")
            similar_conversations = search_memory(query, n_results=3)
            if similar_conversations:
                print(f"🧠 Found {len(similar_conversations)} similar past conversations")
            
            search_results = search_web.run(query)
            print(f"✅ Search completed, {len(search_results)} characters retrieved")
            
            # Execute teams sequentially
            previous_result = None
            
            for i, team_enum in enumerate(teams_to_execute):
                print(f"\n🔧 Executing Team {i+1}/{len(teams_to_execute)}: {team_enum.value}")
                
                # Create agents for this team
                if team_enum not in self.agent_creators:
                    print(f"⚠️ No agent creator found for team: {team_enum.value}")
                    continue
                
                agents_dict = self.agent_creators[team_enum](llm, conversation_history, use_tools=False)
                agents_list = list(agents_dict.values())
                
                print(f"✅ Created {len(agents_list)} agents for {team_enum.value}")
                
                # Create tasks for this team
                if team_enum not in self.task_creators:
                    print(f"⚠️ No task creator found for team: {team_enum.value}")
                    continue
                
                # Use previous result as input for subsequent teams
                input_data = previous_result if previous_result else search_results
                
                tasks = self.task_creators[team_enum](
                    *agents_list, 
                    query, 
                    str(input_data), 
                    conversation_history,
                    document_context
                )
                
                print(f"✅ Created {len(tasks)} tasks for {team_enum.value}")
                
                # Create and execute crew
                crew = Crew(
                    agents=agents_list,
                    tasks=tasks,
                    process=Process.sequential,
                    verbose=True,
                    max_rpm=5,
                    max_execution_time=240,  # 4 minute timeout per team
                    memory=False,
                    share_crew=False
                )
                
                # Execute team
                team_result = crew.kickoff()
                previous_result = team_result
                
                print(f"✅ Team {team_enum.value} completed: {len(str(team_result))} characters")
                
                # Add delay between teams to avoid rate limiting
                if i < len(teams_to_execute) - 1:
                    print("⏳ Waiting 10 seconds before next team...")
                    time.sleep(10)
            
            # Save to memory
            if previous_result:
                add_to_memory(query, str(previous_result))
                print("💾 Result saved to memory")
            
            return str(previous_result) if previous_result else "❌ Workflow execution failed"
            
        except Exception as e:
            error_msg = f"❌ Dynamic workflow execution failed: {str(e)}"
            print(error_msg)
            return error_msg
    
    def get_workflow_preview(self, custom_team_selection: Optional[List[AgentTeam]] = None) -> Dict[str, Any]:
        """
        Get a preview of what the workflow will execute
        
        Args:
            custom_team_selection: Custom team selection (if None, uses enabled teams)
        
        Returns:
            Workflow preview information
        """
        
        if custom_team_selection:
            teams_to_execute = custom_team_selection
        else:
            teams_to_execute = [team.team for team in agent_config.get_workflow_order()]
        
        preview = {
            "total_teams": len(teams_to_execute),
            "teams": [],
            "estimated_duration": len(teams_to_execute) * 4,  # 4 minutes per team
            "total_agents": 0
        }
        
        for team_enum in teams_to_execute:
            team_info = agent_config.teams[team_enum]
            enabled_agents = agent_config.get_enabled_agents_for_team(team_enum)
            
            preview["teams"].append({
                "name": team_info.name,
                "team": team_enum.value,
                "agents": len(enabled_agents),
                "agent_names": [agent.role for agent in enabled_agents]
            })
            
            preview["total_agents"] += len(enabled_agents)
        
        return preview

# Global executor instance
dynamic_executor = DynamicWorkflowExecutor()

# Convenience functions for backward compatibility
def run_dynamic_workflow(
    query: str, 
    llm, 
    conversation_history: Optional[List[Any]] = None,
    use_native_function_calling: bool = False,
    document_context: Optional[str] = None,
    custom_team_selection: Optional[List[AgentTeam]] = None
) -> str:
    """Run a dynamic workflow with selected agents"""
    return dynamic_executor.execute_dynamic_workflow(
        query, llm, conversation_history, use_native_function_calling, 
        document_context, custom_team_selection
    )

def get_workflow_preview(custom_team_selection: Optional[List[AgentTeam]] = None) -> Dict[str, Any]:
    """Get workflow preview"""
    return dynamic_executor.get_workflow_preview(custom_team_selection)
