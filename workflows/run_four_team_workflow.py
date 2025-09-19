"""
Run Four Team Workflow

This module contains the run four team workflow execution function.
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
from agent_teams.information_management import create_information_management_agents_with_context, create_information_management_tasks_with_data
from agent_teams.tender_response import create_tender_response_agents_with_context, create_tender_response_tasks_with_data
from agent_teams.project_delivery import create_project_delivery_agents_with_context, create_project_delivery_tasks_with_data
from agent_teams.technical_documentation import create_technical_documentation_agents_with_context, create_technical_documentation_tasks_with_data

# Import utility functions
from .workflow_executor import perform_workflow_presearch
from team_outputs.output_manager import TeamOutputManager
from local_memory import add_to_memory

def run_four_team_workflow(query: str, llm, conversation_history: List[Any] = None, use_native_function_calling: bool = False, document_context: str = None) -> str:
    """
    Run the four-team workflow: Research Team → Data Strategy Team → Compliance & Risk Team → Information Management Team
    """
    start_time = time.time()
    
    try:
        # Create LLM if not provided (using original working configuration)
        if llm is None:
            print("🔧 Creating LLM for four-team workflow...")
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
            print(f"🚀 Running four-team workflow with native function calling for: {query}")
            
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
            
            # Create fourth team (Information Management Team)
            information_management_agents = create_information_management_agents_with_context(llm, conversation_history, use_tools=False)
            info_governance_agent = information_management_agents['information_governance_specialist']
            metadata_agent = information_management_agents['metadata_management_specialist']
            data_quality_agent = information_management_agents['data_quality_specialist']
            
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
            
            # Create fourth team tasks using third team results
            fourth_team_tasks = create_information_management_tasks_with_data(
                info_governance_agent, metadata_agent, data_quality_agent,
                query, str(third_team_result), conversation_history
            )
            
            # Create fourth team crew
            fourth_team_crew = Crew(
                agents=[info_governance_agent, metadata_agent, data_quality_agent],
                tasks=fourth_team_tasks,
                process=Process.sequential,
                verbose=True,
                max_rpm=5,
                max_execution_time=360,  # 6 minute timeout for fourth team
                memory=False,
                share_crew=False
            )
            
            # Execute fourth team
            fourth_team_result = fourth_team_crew.kickoff()
            print(f"✅ Fourth team completed: {len(str(fourth_team_result))} characters")
            
            # Combine results
            combined_result = f"""
# Four-Team Workflow Results

## First Team: Research & Analysis
{str(first_team_result)}

---

## Second Team: Data Strategy & DAMA Implementation
{str(second_team_result)}

---

## Third Team: Compliance & Risk Management
{str(third_team_result)}

---

## Fourth Team: Information Management
{str(fourth_team_result)}
"""
            
            return str(combined_result)
            
        else:
            # Pre-search approach for four-team workflow
            search_data = perform_workflow_presearch(query, "four-team workflow", conversation_history)
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
            
            # Create fourth team (Information Management Team)
            print("🔧 Creating fourth team agents...")
            information_management_agents = create_information_management_agents_with_context(llm, conversation_history, use_tools=False)
            info_governance_agent = information_management_agents['information_governance_specialist']
            metadata_agent = information_management_agents['metadata_management_specialist']
            data_quality_agent = information_management_agents['data_quality_specialist']
            print(f"✅ Fourth team created: {info_governance_agent.role}, {metadata_agent.role}, {data_quality_agent.role}")
            
            # Create first team tasks
            print("🔧 Creating first team tasks...")
            first_team_tasks = create_research_analysis_tasks_with_data(researcher, analyst, writer, query, search_results, conversation_history, document_context)
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
            
            # Create fourth team tasks using third team results
            print("🔧 Creating fourth team tasks...")
            fourth_team_tasks = create_information_management_tasks_with_data(
                info_governance_agent, metadata_agent, data_quality_agent,
                query, str(third_team_result), conversation_history
            )
            print(f"✅ Fourth team tasks created: {len(fourth_team_tasks)} tasks")
            
            # Create fourth team crew
            fourth_team_crew = Crew(
                agents=[info_governance_agent, metadata_agent, data_quality_agent],
                tasks=fourth_team_tasks,
                process=Process.sequential,
                verbose=True,
                max_rpm=5,
                max_execution_time=360,  # 6 minute timeout for fourth team
                memory=False,
                share_crew=False
            )
            
            # Execute fourth team
            print("🚀 Executing fourth team workflow...")
            fourth_team_result = fourth_team_crew.kickoff()
            print(f"✅ Fourth team completed: {len(str(fourth_team_result))} characters")
            
            # Combine results
            combined_result = f"""
# Four-Team Workflow Results

## First Team: Research & Analysis
{str(first_team_result)}

---

## Second Team: Data Strategy & DAMA Implementation
{str(second_team_result)}

---

## Third Team: Compliance & Risk Management
{str(third_team_result)}

---

## Fourth Team: Information Management
{str(fourth_team_result)}
"""
            
            # Save this conversation to local memory
            try:
                add_to_memory(
                    query=query,
                    response=str(combined_result),
                    metadata={
                        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                        "workflow_type": "four_team_workflow",
                        "use_native": use_native_function_calling
                    }
                )
                print("💾 Conversation saved to local memory")
            except Exception as mem_error:
                print(f"⚠️ Memory save failed: {mem_error}")
            
            # Log performance metrics
            elapsed_time = time.time() - start_time
            print(f"⏱️ Four-team workflow completed in {elapsed_time:.2f} seconds")
            
            return str(combined_result)
        
    except Exception as e:
        elapsed_time = time.time() - start_time
        print(f"❌ Four-team workflow failed after {elapsed_time:.2f} seconds")
        print(f"❌ Error details: {str(e)}")
        import traceback
        print(f"❌ Full traceback: {traceback.format_exc()}")
        return f"Error in four-team workflow execution: {str(e)}"


