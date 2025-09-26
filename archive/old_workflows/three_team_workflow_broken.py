"""
Three-Team Workflow

This module contains the three-team workflow execution function:
Research Team → Data Strategy Team → Compliance & Risk Team
"""

import time
from typing import List, Any
from crewai import Crew, Process, LLM

# Import agent and task creation functions
from agent_teams.research_analysis import (
    create_research_analysis_agents_with_context, 
    create_research_analysis_tasks_with_data,
    create_research_analysis_tasks
)
from agent_teams.data_strategy import create_data_strategy_agents_with_context, create_data_strategy_tasks_with_data
from agent_teams.compliance_risk import create_compliance_risk_agents_with_context, create_compliance_risk_tasks_with_data

# Import utility functions
from .workflow_executor import perform_workflow_presearch
from local_memory import add_to_memory


def run_three_team_workflow(query: str, llm, conversation_history: List[Any] = None, use_native_function_calling: bool = False) -> str:
    """
    Run the three-team workflow: Research Team → Data Strategy Team → Compliance & Risk Team
    """
    start_time = time.time()
    
    try:
        # Create LLM if not provided (using original working configuration)
        if llm is None:
            print("🔧 Creating LLM for three-team workflow...")
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
            print(f"🚀 Running three-team workflow with native function calling for: {query}")
            
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
            
            # Create third team (Compliance & Risk Team)
            compliance_risk_agents = create_compliance_risk_agents_with_context(llm, conversation_history, use_tools=False)
            compliance_agent = compliance_risk_agents['compliance_specialist']
            risk_agent = compliance_risk_agents['risk_management_specialist']
            audit_agent = compliance_risk_agents['audit_governance_specialist']
            
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
        
        # Wait to avoid rate limiting
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
        
        # Wait to avoid rate limiting
        print("⏳ Waiting 10 seconds to avoid rate limiting...")
        time.sleep(10)
        
        # Create third team tasks using second team results
        third_team_tasks = create_compliance_risk_tasks_with_data(
            compliance_agent, risk_agent, audit_agent,
            query, str(second_team_result), conversation_history
        )
        
        # Create third team crew
        third_team_crew = Crew(
            agents=[compliance_agent, risk_agent, audit_agent],
            tasks=third_team_tasks,
            process=Process.sequential,
            verbose=True,
            max_rpm=5,
            max_execution_time=300,  # 5 minute timeout for third team
            memory=False,
            share_crew=False
        )
        
        # Execute third team
        third_team_result = third_team_crew.kickoff()
        print(f"✅ Third team completed: {len(str(third_team_result))} characters")
        
        # Combine results
        combined_result = f"""
# Three-Team Workflow Results

## First Team: Research & Analysis
{str(first_team_result)}

---

## Second Team: Data Strategy & DAMA Implementation
{str(second_team_result)}

---

## Third Team: Compliance & Risk Management
{str(third_team_result)}
"""
        
        return str(combined_result)
        
    else:
        # Pre-search approach for three-team workflow
        search_data = perform_workflow_presearch(query, "three-team workflow", conversation_history)
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
            
            # Create third team (Compliance & Risk Team)
            print("🔧 Creating third team agents...")
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
            
            # Create third team tasks using second team results
            print("🔧 Creating third team tasks...")
            third_team_tasks = create_compliance_risk_tasks_with_data(
                compliance_agent, risk_agent, audit_agent,
                query, str(second_team_result), conversation_history
            )
            print(f"✅ Third team tasks created: {len(third_team_tasks)} tasks")
            
            # Create third team crew
            third_team_crew = Crew(
                agents=[compliance_agent, risk_agent, audit_agent],
                tasks=third_team_tasks,
                process=Process.sequential,
                verbose=True,
                max_rpm=5,
                max_execution_time=300,  # 5 minute timeout for third team
                memory=False,
                share_crew=False
            )
            
            # Execute third team
            print("🚀 Executing third team workflow...")
            third_team_result = third_team_crew.kickoff()
            print(f"✅ Third team completed: {len(str(third_team_result))} characters")
            
            # Combine results
            combined_result = f"""
# Three-Team Workflow Results

## First Team: Research & Analysis
{str(first_team_result)}

---

## Second Team: Data Strategy & DAMA Implementation
{str(second_team_result)}

---

## Third Team: Compliance & Risk Management
{str(third_team_result)}
"""
            
            # Save this conversation to local memory
            try:
                add_to_memory(
                    query=query,
                    response=str(combined_result),
                    metadata={
                        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                        "workflow_type": "three_team_workflow",
                        "use_native": use_native_function_calling
                    }
                )
                print("💾 Conversation saved to local memory")
            except Exception as mem_error:
                print(f"⚠️ Memory save failed: {mem_error}")
            
            # Log performance metrics
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
