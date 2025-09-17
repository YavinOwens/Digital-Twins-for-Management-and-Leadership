"""
Workflow Executor Module

This module contains all workflow execution functions for the CrewAI multi-agent system.
Each workflow type handles different team compositions and execution patterns.
"""

import time
from typing import Dict, Any, List, Optional
from crewai import Crew, Process

# Import agents from agent_teams package
from agent_teams.research_analysis import create_research_analysis_agents_with_context, create_research_analysis_tasks_with_data
from agent_teams.data_strategy import create_data_strategy_agents_with_context, create_data_strategy_tasks_with_data
from agent_teams.compliance_risk import create_compliance_risk_agents_with_context, create_compliance_risk_tasks_with_data
from agent_teams.information_management import create_information_management_agents_with_context, create_information_management_tasks_with_data
from agent_teams.tender_response import create_tender_response_agents_with_context, create_tender_response_tasks_with_data
from agent_teams.project_delivery import create_project_delivery_agents_with_context, create_project_delivery_tasks_with_data
from agent_teams.technical_documentation import create_technical_documentation_agents_with_context, create_technical_documentation_tasks_with_data

# Import tools and utilities
from agent_tools import search_web
from local_memory import add_to_memory, search_memory
from presearch import PreSearchManager
from team_outputs import TeamOutputManager

# Import legacy functions for backward compatibility
from archive.agents.agent_factory import create_crew_agents
from archive.agent_tasks.task_factory import create_crew_tasks, create_crew_tasks_with_data


def run_crew_workflow(query: str, llm, conversation_history=None, use_native_function_calling=False) -> str:
    """Run the CrewAI workflow and return results with conversation context"""
    
    start_time = time.time()
    
    try:
        if use_native_function_calling:
            # Try native function calling approach
            print(f"🔍 Using native function calling for: {query}")
            
            # Create agents with tools for native function calling
            researcher, analyst, writer = create_crew_agents(llm, conversation_history, use_tools=True)
            tasks = create_crew_tasks(researcher, analyst, writer, query, conversation_history)
            
            # Create crew with tools
            crew = Crew(
                agents=[researcher, analyst, writer],
                tasks=tasks,
                process=Process.sequential,
                verbose=True
            )
            
            # Execute the workflow
            result = crew.kickoff()
            return str(result)
            
        else:
            # Use pre-search approach (current working method)
            print(f"🔍 Pre-searching data for: {query}")
            
            # Search for similar past conversations
            similar_conversations = search_memory(query, n_results=3)
            if similar_conversations:
                print(f"🧠 Found {len(similar_conversations)} similar past conversations")
            
            search_results = search_web.run(query)
            print(f"✅ Search completed, {len(search_results)} characters retrieved")
            
            # Create agents and tasks with conversation context and pre-searched data
            print("🔧 Creating agents...")
            researcher, analyst, writer = create_crew_agents(llm, conversation_history, use_tools=False)
            print(f"✅ Agents created: {researcher.role}, {analyst.role}, {writer.role}")
            
            print("🔧 Creating tasks...")
            # Use tasks with dependencies for better performance
            tasks = create_crew_tasks_with_data(researcher, analyst, writer, query, search_results, conversation_history)
            print(f"✅ Tasks created: {len(tasks)} tasks")
            
            # Create crew with optimized configuration and memory
            crew = Crew(
                agents=[researcher, analyst, writer],
                tasks=tasks,
                process=Process.sequential,
                verbose=True,
                max_rpm=20,  # Increased for better throughput
                max_execution_time=180,  # 3 minute timeout
                memory=False,  # Disable CrewAI memory (using local memory instead)
                share_crew=False  # Disable sharing for faster execution
            )
            
            # Execute the workflow with timeout
            result = crew.kickoff()
            
            # Save this conversation to local memory
            try:
                add_to_memory(
                    query=query,
                    response=str(result),
                    metadata={
                        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                        "workflow_type": "crew_workflow",
                        "use_native": use_native_function_calling
                    }
                )
                print("💾 Conversation saved to local memory")
            except Exception as mem_error:
                print(f"⚠️ Memory save failed: {mem_error}")
            
            # Log performance metrics
            elapsed_time = time.time() - start_time
            print(f"⏱️ Workflow completed in {elapsed_time:.2f} seconds")
            
            return str(result)
        
    except Exception as e:
        elapsed_time = time.time() - start_time
        print(f"❌ Workflow failed after {elapsed_time:.2f} seconds")
        print(f"❌ Error details: {str(e)}")
        import traceback
        print(f"❌ Full traceback: {traceback.format_exc()}")
        return f"Error in workflow execution: {str(e)}"


def perform_workflow_presearch(query: str, workflow_name: str, conversation_history: Optional[List[Any]] = None) -> Dict[str, Any]:
    """
    Perform pre-search for any workflow using the PreSearchManager.
    
    Args:
        query: The user's query
        workflow_name: Name of the workflow for logging
        conversation_history: Previous conversation context
        
    Returns:
        Dict containing search results and context
    """
    print(f"🔍 Pre-searching data for {workflow_name}: {query}")
    
    # Initialize pre-search manager
    presearch_manager = PreSearchManager(memory_enabled=True, max_memory_results=3)
    
    # Perform comprehensive pre-search
    search_data = presearch_manager.search_and_combine_context(query, conversation_history)
    
    return search_data


# Note: The remaining workflow functions (run_two_team_workflow, run_three_team_workflow, etc.)
# are very large and will be extracted in a separate step to keep this file manageable.
# For now, this module provides the basic workflow infrastructure.

def run_two_team_workflow(query: str, llm, conversation_history: List[Any] = None, use_native_function_calling: bool = False) -> str:
    """
    Run the two-team workflow: Research Team → Data Strategy Team
    """
    start_time = time.time()
    
    try:
        # Pre-search approach for two-team workflow
        search_data = perform_workflow_presearch(query, "two-team workflow", conversation_history)
        search_results = search_data['web_results']
        
        # Create first team (Research Team)
        print("🔧 Creating first team agents...")
        research_analysis_agents = create_research_analysis_agents_with_context(llm, conversation_history, use_tools=False)
        researcher = research_analysis_agents['researcher']
        analyst = research_analysis_agents['analyst']
        writer = research_analysis_agents['writer']
        print(f"✅ First team created: {researcher.role}, {analyst.role}, {writer.role}")
        
        # Create second team (Data Strategy Team)
        data_strategy_agents = create_data_strategy_agents_with_context(llm, conversation_history, use_tools=False)
        governance_agent = data_strategy_agents['data_governance_specialist']
        dcam_agent = data_strategy_agents['dcam_template_specialist']
        tranch_agent = data_strategy_agents['tranch_guidance_specialist']
        print(f"✅ Second team created: {governance_agent.role}, {dcam_agent.role}, {tranch_agent.role}")
        
        # Create first team tasks
        print("🔧 Creating first team tasks...")
        first_team_tasks = create_research_analysis_tasks_with_data(researcher, analyst, writer, query, search_results, conversation_history)
        print(f"✅ First team tasks created: {len(first_team_tasks)} tasks")
        
        # Create first team crew
        first_team_crew = Crew(
            agents=[researcher, analyst, writer],
            tasks=first_team_tasks,
            process=Process.sequential,
            verbose=True,
            max_rpm=20,
            max_execution_time=180,
            memory=False,
            share_crew=False
        )
        
        # Execute first team
        print("🚀 Executing first team...")
        first_team_result = first_team_crew.kickoff()
        print(f"✅ First team completed: {len(str(first_team_result))} characters")
        
        # Create second team tasks with data from first team
        print("🔧 Creating second team tasks...")
        second_team_tasks = create_data_strategy_tasks_with_data(
            governance_agent, dcam_agent, tranch_agent, query, str(first_team_result), conversation_history
        )
        print(f"✅ Second team tasks created: {len(second_team_tasks)} tasks")
        
        # Create second team crew
        second_team_crew = Crew(
            agents=[governance_agent, dcam_agent, tranch_agent],
            tasks=second_team_tasks,
            process=Process.sequential,
            verbose=True,
            max_rpm=20,
            max_execution_time=180,
            memory=False,
            share_crew=False
        )
        
        # Execute second team
        print("🚀 Executing second team...")
        second_team_result = second_team_crew.kickoff()
        print(f"✅ Second team completed: {len(str(second_team_result))} characters")
        
        # Combine results
        combined_result = f"""
# Two-Team Workflow Results

## Research & Analysis Team Results
{str(first_team_result)}

---

## Data Strategy & DAMA Implementation Team Results
{str(second_team_result)}

---

**Workflow completed successfully with two specialized teams working sequentially.**
"""
        
        # Save team outputs to structured folders
        try:
            output_manager = TeamOutputManager()
            team_outputs = {
                "Team 1 - Research & Analysis": str(first_team_result),
                "Team 2 - Data Strategy & DAMA Implementation": str(second_team_result)
            }
            output_path = output_manager.save_workflow_outputs(
                "two_team_workflow", 
                query, 
                team_outputs,
                {
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "workflow_type": "two_team_workflow",
                    "use_native": use_native_function_calling,
                    "execution_time": f"{time.time() - start_time:.2f} seconds"
                }
            )
            print(f"📁 Team outputs saved to: {output_path}")
        except Exception as output_error:
            print(f"⚠️ Team output save failed: {output_error}")
        
        # Save this conversation to local memory
        try:
            add_to_memory(query=query, response=str(combined_result), metadata={"timestamp": time.strftime("%Y-%m-%d %H:%M:%S"), "workflow_type": "two_team_workflow", "use_native": use_native_function_calling})
            print("💾 Conversation saved to local memory")
        except Exception as mem_error:
            print(f"⚠️ Memory save failed: {mem_error}")
        
        elapsed_time = time.time() - start_time
        print(f"⏱️ Two-team workflow completed in {elapsed_time:.2f} seconds")
        return str(combined_result)
        
    except Exception as e:
        elapsed_time = time.time() - start_time
        print(f"❌ Two-team workflow failed after {elapsed_time:.2f} seconds")
        print(f"❌ Error details: {str(e)}")
        import traceback
        print(f"❌ Full traceback: {traceback.format_exc()}")
        return f"Error in two-team workflow execution: {str(e)}"


def run_three_team_workflow(query: str, llm, conversation_history: List[Any] = None, use_native_function_calling: bool = False) -> str:
    """Run the three-team workflow: Research Team → Data Strategy Team → Compliance & Risk Team"""
    start_time = time.time()
    
    try:
        # Pre-search approach for three-team workflow
        search_data = perform_workflow_presearch(query, "three-team workflow", conversation_history)
        search_results = search_data['web_results']
        
        # Create first team (Research Team)
        print("🔧 Creating first team agents...")
        research_analysis_agents = create_research_analysis_agents_with_context(llm, conversation_history, use_tools=False)
        researcher = research_analysis_agents['researcher']
        analyst = research_analysis_agents['analyst']
        writer = research_analysis_agents['writer']
        print(f"✅ First team created: {researcher.role}, {analyst.role}, {writer.role}")
        
        # Create second team (Data Strategy Team)
        data_strategy_agents = create_data_strategy_agents_with_context(llm, conversation_history, use_tools=False)
        governance_agent = data_strategy_agents['data_governance_specialist']
        dcam_agent = data_strategy_agents['dcam_template_specialist']
        tranch_agent = data_strategy_agents['tranch_guidance_specialist']
        print(f"✅ Second team created: {governance_agent.role}, {dcam_agent.role}, {tranch_agent.role}")
        
        # Create third team (Compliance & Risk Team)
        compliance_risk_agents = create_compliance_risk_agents_with_context(llm, conversation_history, use_tools=False)
        compliance_agent = compliance_risk_agents['compliance_specialist']
        risk_agent = compliance_risk_agents['risk_management_specialist']
        audit_agent = compliance_risk_agents['audit_governance_specialist']
        print(f"✅ Third team created: {compliance_agent.role}, {risk_agent.role}, {audit_agent.role}")
        
        # Create first team tasks
        print("🔧 Creating first team tasks...")
        first_team_tasks = create_research_analysis_tasks_with_data(researcher, analyst, writer, query, search_results, conversation_history)
        print(f"✅ First team tasks created: {len(first_team_tasks)} tasks")
        
        # Create first team crew
        first_team_crew = Crew(
            agents=[researcher, analyst, writer],
            tasks=first_team_tasks,
            process=Process.sequential,
            verbose=True,
            max_rpm=20,
            max_execution_time=180,
            memory=False,
            share_crew=False
        )
        
        # Execute first team
        print("🚀 Executing first team...")
        first_team_result = first_team_crew.kickoff()
        print(f"✅ First team completed: {len(str(first_team_result))} characters")
        
        # Create second team tasks with data from first team
        print("🔧 Creating second team tasks...")
        second_team_tasks = create_data_strategy_tasks_with_data(
            governance_agent, dcam_agent, tranch_agent, query, str(first_team_result), conversation_history
        )
        print(f"✅ Second team tasks created: {len(second_team_tasks)} tasks")
        
        # Create second team crew
        second_team_crew = Crew(
            agents=[governance_agent, dcam_agent, tranch_agent],
            tasks=second_team_tasks,
            process=Process.sequential,
            verbose=True,
            max_rpm=20,
            max_execution_time=240,
            memory=False,
            share_crew=False
        )
        
        # Execute second team
        print("🚀 Executing second team...")
        second_team_result = second_team_crew.kickoff()
        print(f"✅ Second team completed: {len(str(second_team_result))} characters")
        
        # Create third team tasks with data from second team
        print("🔧 Creating third team tasks...")
        third_team_tasks = create_compliance_risk_tasks_with_data(
            compliance_agent, risk_agent, audit_agent, query, str(second_team_result), conversation_history
        )
        print(f"✅ Third team tasks created: {len(third_team_tasks)} tasks")
        
        # Create third team crew
        third_team_crew = Crew(
            agents=[compliance_agent, risk_agent, audit_agent],
            tasks=third_team_tasks,
            process=Process.sequential,
            verbose=True,
            max_rpm=20,
            max_execution_time=300,
            memory=False,
            share_crew=False
        )
        
        # Execute third team
        print("🚀 Executing third team...")
        third_team_result = third_team_crew.kickoff()
        print(f"✅ Third team completed: {len(str(third_team_result))} characters")
        
        # Combine results
        combined_result = f"""
# Three-Team Workflow Results

## Team 1 - Research & Analysis
{str(first_team_result)}

---

## Team 2 - Data Strategy & DAMA Implementation
{str(second_team_result)}

---

## Team 3 - Compliance & Risk Management
{str(third_team_result)}

---

**Workflow completed successfully with three specialized teams working sequentially.**
"""
        
        # Save team outputs to structured folders
        try:
            output_manager = TeamOutputManager()
            team_outputs = {
                "Team 1 - Research & Analysis": str(first_team_result),
                "Team 2 - Data Strategy & DAMA Implementation": str(second_team_result),
                "Team 3 - Compliance & Risk Management": str(third_team_result)
            }
            output_path = output_manager.save_workflow_outputs(
                "three_team_workflow", 
                query, 
                team_outputs,
                {
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "workflow_type": "three_team_workflow",
                    "use_native": use_native_function_calling,
                    "execution_time": f"{time.time() - start_time:.2f} seconds"
                }
            )
            print(f"📁 Team outputs saved to: {output_path}")
        except Exception as output_error:
            print(f"⚠️ Team output save failed: {output_error}")
        
        # Save this conversation to local memory
        try:
            add_to_memory(query=query, response=str(combined_result), metadata={"timestamp": time.strftime("%Y-%m-%d %H:%M:%S"), "workflow_type": "three_team_workflow", "use_native": use_native_function_calling})
            print("💾 Conversation saved to local memory")
        except Exception as mem_error:
            print(f"⚠️ Memory save failed: {mem_error}")
        
        elapsed_time = time.time() - start_time
        print(f"⏱️ Three-team workflow completed in {elapsed_time:.2f} seconds")
        return str(combined_result)
        
    except Exception as e:
        elapsed_time = time.time() - start_time
        print(f"❌ Three-team workflow failed after {elapsed_time:.2f} seconds")
        print(f"❌ Error details: {str(e)}")
        import traceback
        print(f"❌ Full traceback: {traceback.format_exc()}")
        return f"Error in three-team workflow execution: {str(e)}"


# Note: The remaining workflow functions (four, five, six, seven team) are very large
# and would make this file too long. For now, they return placeholder messages.
# In a production environment, these would be extracted to separate files.

def run_four_team_workflow(query: str, llm, conversation_history: List[Any] = None, use_native_function_calling: bool = False) -> str:
    """Run the four-team workflow: Research → Data Strategy → Compliance & Risk → Information Management"""
    return "Four-team workflow implementation in progress. Please use the original streamlit_app.py for now."


def run_five_team_workflow(query: str, llm, conversation_history: List[Any] = None, use_native_function_calling: bool = False) -> str:
    """Run the five-team workflow: Research → Data Strategy → Compliance & Risk → Information Management → Tender Response"""
    return "Five-team workflow implementation in progress. Please use the original streamlit_app.py for now."


def run_six_team_workflow(query: str, llm, conversation_history: List[Any] = None, use_native_function_calling: bool = False) -> str:
    """Run the six-team workflow: Research → Data Strategy → Compliance & Risk → Information Management → Tender Response → Project Delivery"""
    return "Six-team workflow implementation in progress. Please use the original streamlit_app.py for now."


def run_seven_team_workflow(query: str, llm, conversation_history: List[Any] = None, use_native_function_calling: bool = False) -> str:
    """Run the seven-team workflow: Research → Data Strategy → Compliance & Risk → Information Management → Tender Response → Project Delivery → Technical Documentation"""
    return "Seven-team workflow implementation in progress. Please use the original streamlit_app.py for now."
