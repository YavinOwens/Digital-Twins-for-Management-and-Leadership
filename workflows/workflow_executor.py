"""
Workflow Executor

This module contains all workflow execution functions for the CrewAI multi-agent system.
Each function handles a specific number of teams working sequentially.
"""

import time
from typing import List, Any, Dict, Optional
from crewai import Crew, Process, LLM

# Import agent and task creation functions
from agent_teams.research_analysis import create_research_analysis_agents_with_context, create_research_analysis_tasks_with_data
from agent_teams.data_strategy import create_data_strategy_agents_with_context, create_data_strategy_tasks_with_data
from agent_teams.compliance_risk import create_compliance_risk_agents_with_context, create_compliance_risk_tasks_with_data
from agent_teams.information_management import create_information_management_agents_with_context, create_information_management_tasks_with_data
from agent_teams.tender_response import create_tender_response_agents_with_context, create_tender_response_tasks_with_data
from agent_teams.project_delivery import create_project_delivery_agents_with_context, create_project_delivery_tasks_with_data
from agent_teams.technical_documentation import create_technical_documentation_agents_with_context, create_technical_documentation_tasks_with_data

# Import research analysis functions for standard workflow
from agent_teams.research_analysis import (
    create_research_analysis_agents_with_context, 
    create_research_analysis_tasks_with_data,
    create_research_analysis_tasks
)

# Import utility functions
from presearch.presearch_manager import PreSearchManager
from team_outputs.output_manager import TeamOutputManager
from local_memory import add_to_memory, search_memory
from agent_tools import search_web


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


def run_crew_workflow(query: str, llm, conversation_history=None, use_native_function_calling=False) -> str:
    """Run the CrewAI workflow and return results with conversation context"""
    
    start_time = time.time()
    
    try:
        # Create LLM if not provided (using original working configuration)
        if llm is None:
            print("🔧 Creating LLM for crew workflow...")
            import os
            api_key = os.getenv('OLLAMA_API_KEY')
            llm = LLM(
                model="ollama/gpt-oss:20b",
                base_url="https://ollama.com",
                headers={'Authorization': f'Bearer {api_key}'},
                temperature=0.5,
                max_tokens=8000,
                system_message="You are an expert business consultant and writer. When asked to write reports, you must provide complete, detailed content - never summaries or placeholders. Write comprehensive, actionable content that executives can use immediately for decision-making. NEVER use ellipsis (...), continuation phrases, or placeholders like '[Insert content here]' or '[The actual content would continue here]'. Always write the complete, final content for every section. ONLY use references from the actual research data provided - NEVER make up citations, author names, or publication details."
            )
            print(f"✅ LLM created: {type(llm)}")
        
        if use_native_function_calling:
            # Try native function calling approach
            print(f"🔍 Using native function calling for: {query}")
            
            # Create agents with tools for native function calling
            research_agents = create_research_analysis_agents_with_context(llm, conversation_history, use_tools=True)
            researcher = research_agents['research_specialist']
            analyst = research_agents['data_analyst']
            writer = research_agents['content_writer']
            tasks = create_research_analysis_tasks(researcher, analyst, writer, query, conversation_history)
            
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
            research_agents = create_research_analysis_agents_with_context(llm, conversation_history, use_tools=False)
            researcher = research_agents['research_specialist']
            analyst = research_agents['data_analyst']
            writer = research_agents['content_writer']
            print(f"✅ Agents created: {researcher.role}, {analyst.role}, {writer.role}")
            
            print("🔧 Creating tasks...")
            # Use tasks with dependencies for better performance
            tasks = create_research_analysis_tasks_with_data(researcher, analyst, writer, query, search_results, conversation_history)
            print(f"✅ Tasks created: {len(tasks)} tasks")
            
            # Create crew with optimized configuration and memory
            crew = Crew(
                agents=[researcher, analyst, writer],
                tasks=tasks,
                process=Process.sequential,
                verbose=True,
                max_rpm=5,  # Reduced to avoid rate limiting
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


def run_two_team_workflow(query: str, llm, conversation_history: List[Any] = None, use_native_function_calling: bool = False) -> str:
    """
    Run the two-team workflow: Research Team → Data Strategy Team
    """
    start_time = time.time()
    
    try:
        # Create LLM if not provided (using original working configuration)
        if llm is None:
            print("🔧 Creating LLM for two-team workflow...")
            import os
            api_key = os.getenv('OLLAMA_API_KEY')
            llm = LLM(
                model="ollama/gpt-oss:20b",
                base_url="https://ollama.com",
                headers={'Authorization': f'Bearer {api_key}'},
                temperature=0.5,
                max_tokens=8000,
                system_message="You are an expert business consultant and writer. When asked to write reports, you must provide complete, detailed content - never summaries or placeholders. Write comprehensive, actionable content that executives can use immediately for decision-making. NEVER use ellipsis (...), continuation phrases, or placeholders like '[Insert content here]' or '[The actual content would continue here]'. Always write the complete, final content for every section. ONLY use references from the actual research data provided - NEVER make up citations, author names, or publication details."
            )
            print(f"✅ LLM created: {type(llm)}")
        
        if use_native_function_calling:
            # Native function calling mode (experimental)
            print(f"🚀 Running two-team workflow with native function calling for: {query}")
            
            # Create first team (Research Team)
            research_agents = create_research_analysis_agents_with_context(llm, conversation_history, use_tools=True)
            researcher = research_agents['research_specialist']
            analyst = research_agents['data_analyst']
            writer = research_agents['content_writer']
            
            # Create second team (Data Strategy Team)
            data_strategy_agents = create_data_strategy_agents_with_context(llm, conversation_history, use_tools=False)
            governance_agent = data_strategy_agents['data_governance_specialist']
            dcam_agent = data_strategy_agents['dcam_template_specialist']
            tranch_agent = data_strategy_agents['tranch_guidance_specialist']
            
            # Create first team tasks
            first_team_tasks = create_research_analysis_tasks(researcher, analyst, writer, query, conversation_history)
            
            # Create first team crew
            first_team_crew = Crew(
                agents=[researcher, analyst, writer],
                tasks=first_team_tasks,
                process=Process.sequential,
                verbose=True,
                max_rpm=5,
                max_execution_time=180,
                memory=False,
                share_crew=False
            )
            
            # Execute first team
            first_team_result = first_team_crew.kickoff()
            print(f"✅ First team completed: {len(str(first_team_result))} characters")
            
            # Wait to avoid rate limiting before second team
            print("⏳ Waiting 10 seconds to avoid rate limiting...")
            time.sleep(10)
            
            # Create second team tasks using first team results
            second_team_tasks = create_data_strategy_tasks_with_data(
                governance_agent, dcam_agent, tranch_agent, 
                query, str(first_team_result), conversation_history
            )
            
            # Create second team crew
            second_team_crew = Crew(
                agents=[governance_agent, dcam_agent, tranch_agent],
                tasks=second_team_tasks,
                process=Process.sequential,
                verbose=True,
                max_rpm=5,
                max_execution_time=240,  # 4 minute timeout for second team
                memory=False,
                share_crew=False
            )
            
            # Execute second team
            second_team_result = second_team_crew.kickoff()
            print(f"✅ Second team completed: {len(str(second_team_result))} characters")
            
            # Combine results
            combined_result = f"""
# Two-Team Workflow Results

## First Team: Research & Analysis
{str(first_team_result)}

---

## Second Team: Data Strategy & DAMA Implementation
{str(second_team_result)}
"""
            
            return str(combined_result)
            
        else:
            # Pre-search approach for two-team workflow
            search_data = perform_workflow_presearch(query, "two-team workflow", conversation_history)
            search_results = search_data['web_results']
            
            # Create first team (Research Team)
            print("🔧 Creating first team agents...")
            research_agents = create_research_analysis_agents_with_context(llm, conversation_history, use_tools=False)
            researcher = research_agents['research_specialist']
            analyst = research_agents['data_analyst']
            writer = research_agents['content_writer']
            print(f"✅ First team created: {researcher.role}, {analyst.role}, {writer.role}")
            
            # Create second team (Data Strategy Team)
            print("🔧 Creating second team agents...")
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
                max_rpm=5,
                max_execution_time=180,
                memory=False,
                share_crew=False
            )
            
            # Execute first team
            print("🚀 Executing first team workflow...")
            first_team_result = first_team_crew.kickoff()
            print(f"✅ First team completed: {len(str(first_team_result))} characters")
            
            # Create second team tasks using first team results
            print("🔧 Creating second team tasks...")
            second_team_tasks = create_data_strategy_tasks_with_data(
                governance_agent, dcam_agent, tranch_agent, 
                query, str(first_team_result), conversation_history
            )
            print(f"✅ Second team tasks created: {len(second_team_tasks)} tasks")
            
            # Create second team crew
            second_team_crew = Crew(
                agents=[governance_agent, dcam_agent, tranch_agent],
                tasks=second_team_tasks,
                process=Process.sequential,
                verbose=True,
                max_rpm=5,
                max_execution_time=240,  # 4 minute timeout for second team
                memory=False,
                share_crew=False
            )
            
            # Execute second team
            print("🚀 Executing second team workflow...")
            second_team_result = second_team_crew.kickoff()
            print(f"✅ Second team completed: {len(str(second_team_result))} characters")
            
            # Combine results
            combined_result = f"""
# Two-Team Workflow Results

## First Team: Research & Analysis
{str(first_team_result)}

---

## Second Team: Data Strategy & DAMA Implementation
{str(second_team_result)}
"""
            
            # Save this conversation to local memory
            try:
                add_to_memory(
                    query=query,
                    response=str(combined_result),
                    metadata={
                        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                        "workflow_type": "two_team_workflow",
                        "use_native": use_native_function_calling
                    }
                )
                print("💾 Conversation saved to local memory")
            except Exception as mem_error:
                print(f"⚠️ Memory save failed: {mem_error}")
            
            # Log performance metrics
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


# Import additional workflow functions from separate files
from .three_team_workflow import run_three_team_workflow
from .run_four_team_workflow import run_four_team_workflow
from .run_five_team_workflow import run_five_team_workflow
from .run_six_team_workflow import run_six_team_workflow
from .run_seven_team_workflow import run_seven_team_workflow
