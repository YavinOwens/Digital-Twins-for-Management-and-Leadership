"""
Enhanced Workflow with Research Validation

This module contains enhanced workflow execution functions that include
research validation and Harvard referencing for all outputs.
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
from agent_teams.research_validation import (
    create_research_validation_agents_with_context,
    create_research_validation_tasks_with_data
)

# Import utility functions
from .workflow_executor import perform_workflow_presearch
from team_outputs.output_manager import TeamOutputManager
from local_memory import add_to_memory


def run_enhanced_research_workflow(query: str, llm, conversation_history: List[Any] = None, use_native_function_calling: bool = False, document_context: str = None) -> str:
    """
    Run enhanced research workflow with validation: Research Team → Validation Team
    
    Args:
        query: User query
        llm: Language model instance
        conversation_history: Previous conversation context
        use_native_function_calling: Whether to use native function calling
        document_context: Document context from uploaded files
        
    Returns:
        Enhanced research results with validation
    """
    start_time = time.time()
    
    try:
        # Create LLM if not provided
        if llm is None:
            print("🔧 Creating LLM for enhanced research workflow...")
            import os
            api_key = os.getenv('OLLAMA_API_KEY')
            llm = LLM(
                model="ollama/gpt-oss:20b",
                base_url="https://ollama.com",
                headers={'Authorization': f'Bearer {api_key}'},
                temperature=0.5,
                max_tokens=8000,
                system_message="You are an expert business consultant and writer. When asked to write reports, you must provide complete, detailed content - never summaries or placeholders. Write comprehensive, actionable content that executives can use immediately for decision-making. NEVER use ellipsis (...), continuation phrases, or placeholders like '[Insert content here]' or '[The actual content would continue here]'. Always write the complete, final content for every section. ONLY use references from the actual research data provided - NEVER make up citations, author names, or publication details. Always use proper Harvard referencing and ensure all sources are validated."
            )
            print(f"✅ LLM created: {type(llm)}")
        
        if use_native_function_calling:
            # Native function calling mode
            print(f"🚀 Running enhanced research workflow with native function calling for: {query}")
            
            # Create research team
            research_agents = create_research_analysis_agents_with_context(llm, conversation_history, use_tools=True)
            researcher = research_agents['research_specialist']
            analyst = research_agents['data_analyst']
            writer = research_agents['content_writer']
            
            # Create validation team
            validation_agents = create_research_validation_agents_with_context(llm, conversation_history, use_tools=True)
            validator = validation_agents['research_validation_specialist']
            
            # Create research tasks
            research_tasks = create_research_analysis_tasks(researcher, analyst, writer, query, conversation_history)
            
            # Create research team crew
            research_crew = Crew(
                agents=[researcher, analyst, writer],
                tasks=research_tasks,
                process=Process.sequential,
                verbose=True,
                max_rpm=5,
                max_execution_time=180,
                memory=False,
                share_crew=False
            )
            
            # Execute research team
            research_result = research_crew.kickoff()
            print(f"✅ Research team completed: {len(str(research_result))} characters")
            
            # Create validation tasks using research results
            validation_tasks = create_research_validation_tasks_with_data(
                validator, query, str(research_result), conversation_history, document_context
            )
            
            # Create validation team crew
            validation_crew = Crew(
                agents=[validator],
                tasks=validation_tasks,
                process=Process.sequential,
                verbose=True,
                max_rpm=5,
                max_execution_time=240,
                memory=False,
                share_crew=False
            )
            
            # Execute validation team
            validation_result = validation_crew.kickoff()
            print(f"✅ Validation team completed: {len(str(validation_result))} characters")
            
            # Combine results
            combined_result = f"""
# Enhanced Research Workflow Results

## Research & Analysis
{str(research_result)}

---

## Research Validation & Quality Assurance
{str(validation_result)}

---

## Final Output
This enhanced workflow ensures all information is verified, properly referenced, and meets the highest standards of academic integrity and factual accuracy.
"""
            
            return str(combined_result)
            
        else:
            # Pre-search approach
            search_data = perform_workflow_presearch(query, "enhanced research workflow", conversation_history)
            search_results = search_data['web_results']
            
            # Create research team
            print("🔧 Creating research team agents...")
            research_agents = create_research_analysis_agents_with_context(llm, conversation_history, use_tools=False)
            researcher = research_agents['research_specialist']
            analyst = research_agents['data_analyst']
            writer = research_agents['content_writer']
            print(f"✅ Research team created: {researcher.role}, {analyst.role}, {writer.role}")
            
            # Create validation team
            print("🔧 Creating validation team agents...")
            validation_agents = create_research_validation_agents_with_context(llm, conversation_history, use_tools=False)
            validator = validation_agents['research_validation_specialist']
            print(f"✅ Validation team created: {validator.role}")
            
            # Create research tasks
            print("🔧 Creating research tasks...")
            research_tasks = create_research_analysis_tasks_with_data(researcher, analyst, writer, query, search_results, conversation_history, document_context)
            print(f"✅ Research tasks created: {len(research_tasks)} tasks")
            
            # Create research team crew
            research_crew = Crew(
                agents=[researcher, analyst, writer],
                tasks=research_tasks,
                process=Process.sequential,
                verbose=True,
                max_rpm=5,
                max_execution_time=180,
                memory=False,
                share_crew=False
            )
            
            # Execute research team
            print("🚀 Executing research team workflow...")
            research_result = research_crew.kickoff()
            print(f"✅ Research team completed: {len(str(research_result))} characters")
            
            # Create validation tasks using research results
            print("🔧 Creating validation tasks...")
            validation_tasks = create_research_validation_tasks_with_data(
                validator, query, str(research_result), conversation_history, document_context
            )
            print(f"✅ Validation tasks created: {len(validation_tasks)} tasks")
            
            # Create validation team crew
            validation_crew = Crew(
                agents=[validator],
                tasks=validation_tasks,
                process=Process.sequential,
                verbose=True,
                max_rpm=5,
                max_execution_time=240,
                memory=False,
                share_crew=False
            )
            
            # Execute validation team
            print("🚀 Executing validation team workflow...")
            validation_result = validation_crew.kickoff()
            print(f"✅ Validation team completed: {len(str(validation_result))} characters")
            
            # Combine results
            combined_result = f"""
# Enhanced Research Workflow Results

## Research & Analysis
{str(research_result)}

---

## Research Validation & Quality Assurance
{str(validation_result)}

---

## Final Output
This enhanced workflow ensures all information is verified, properly referenced, and meets the highest standards of academic integrity and factual accuracy.
"""
            
            # Save to memory
            try:
                add_to_memory(
                    query=query,
                    response=str(combined_result),
                    metadata={
                        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                        "workflow_type": "enhanced_research_workflow",
                        "use_native": use_native_function_calling,
                        "validated": True
                    }
                )
                print("💾 Conversation saved to local memory")
            except Exception as mem_error:
                print(f"⚠️ Memory save failed: {mem_error}")
            
            # Log performance metrics
            elapsed_time = time.time() - start_time
            print(f"⏱️ Enhanced research workflow completed in {elapsed_time:.2f} seconds")
            
            return str(combined_result)
        
    except Exception as e:
        elapsed_time = time.time() - start_time
        print(f"❌ Enhanced research workflow failed after {elapsed_time:.2f} seconds")
        print(f"❌ Error details: {str(e)}")
        import traceback
        print(f"❌ Full traceback: {traceback.format_exc()}")
        return f"Error in enhanced research workflow execution: {str(e)}"
