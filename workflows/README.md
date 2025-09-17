# Workflows Module

This module contains the individual workflow execution functions for each team configuration (1-7 teams). Each workflow is implemented as a separate module with specific team coordination and context passing logic.

## Structure

```
workflows/
├── __init__.py                    # Module initialization and exports
├── workflow_executor.py           # Single and two team workflows
├── three_team_workflow.py         # Three team workflow
├── run_four_team_workflow.py      # Four team workflow
├── run_five_team_workflow.py      # Five team workflow
├── run_six_team_workflow.py       # Six team workflow
├── run_seven_team_workflow.py     # Seven team workflow
└── README.md                      # This documentation
```

## Key Components

### Workflow Types
- **Single Team**: Research → Analysis → Writing
- **Two Teams**: Research → Data Strategy
- **Three Teams**: Research → Data Strategy → Compliance & Risk
- **Four Teams**: Research → Data Strategy → Compliance & Risk → Information Management
- **Five Teams**: Research → Data Strategy → Compliance & Risk → Information Management → Tender Response
- **Six Teams**: Research → Data Strategy → Compliance & Risk → Information Management → Tender Response → Project Delivery
- **Seven Teams**: Research → Data Strategy → Compliance & Risk → Information Management → Tender Response → Project Delivery → Technical Documentation

## Pseudocode Examples

### Three Team Workflow
```python
def run_three_team_workflow(query: str, llm, conversation_history: List[Any] = None) -> str:
    """
    Pseudocode for three team workflow execution
    """
    try:
        # 1. Perform pre-search
        presearch_results = perform_workflow_presearch(query, "three_team", conversation_history)
        
        # 2. Create first team (Research & Analysis)
        research_agents = create_research_analysis_agents_with_context(llm, conversation_history)
        research_tasks = create_research_analysis_tasks_with_data(
            research_agents['researcher'], research_agents['analyst'], research_agents['writer'],
            query, presearch_results.get('combined_context', ''), conversation_history
        )
        
        # 3. Execute first team
        research_crew = Crew(agents=list(research_agents.values()), tasks=research_tasks, process=Process.sequential, memory=False, max_rpm=5)
        research_result = research_crew.kickoff()
        time.sleep(10)  # Delay between teams
        
        # 4. Create second team (Data Strategy)
        data_strategy_agents = create_data_strategy_agents_with_context(llm, conversation_history)
        data_strategy_tasks = create_data_strategy_tasks_with_data(
            data_strategy_agents['data_governance_specialist'],
            data_strategy_agents['dcam_template_specialist'],
            data_strategy_agents['tranch_guidance_specialist'],
            query, str(research_result), conversation_history
        )
        
        # 5. Execute second team
        data_strategy_crew = Crew(agents=list(data_strategy_agents.values()), tasks=data_strategy_tasks, process=Process.sequential, memory=False, max_rpm=5)
        data_strategy_result = data_strategy_crew.kickoff()
        time.sleep(10)  # Delay between teams
        
        # 6. Create third team (Compliance & Risk)
        compliance_agents = create_compliance_risk_agents_with_context(llm, conversation_history)
        compliance_tasks = create_compliance_risk_tasks_with_data(
            compliance_agents['compliance_specialist'],
            compliance_agents['risk_management_specialist'],
            compliance_agents['audit_governance_specialist'],
            query, str(data_strategy_result), conversation_history
        )
        
        # 7. Execute third team
        compliance_crew = Crew(agents=list(compliance_agents.values()), tasks=compliance_tasks, process=Process.sequential, memory=False, max_rpm=5)
        compliance_result = compliance_crew.kickoff()
        
        # 8. Combine all results
        final_result = f"""# Three Team Workflow Results

## Research & Analysis Results
{research_result}

## Data Strategy Results
{data_strategy_result}

## Compliance & Risk Results
{compliance_result}"""
        
        # 9. Save to memory
        if presearch_results.get('memory_manager'):
            presearch_results['memory_manager'].save_conversation(query, final_result)
        
        return final_result
        
    except Exception as e:
        st.error(f"Three team workflow failed: {e}")
        return f"Error: {e}"
```

### Seven Team Workflow
```python
def run_seven_team_workflow(query: str, llm, conversation_history: List[Any] = None) -> str:
    """
    Pseudocode for seven team workflow execution
    """
    try:
        # 1. Perform pre-search
        presearch_results = perform_workflow_presearch(query, "seven_team", conversation_history)
        
        # 2. Initialize team results
        team_results = {}
        current_context = presearch_results.get('combined_context', '')
        
        # 3. Execute teams sequentially
        teams = [
            ('research_analysis', create_research_analysis_agents_with_context, create_research_analysis_tasks_with_data),
            ('data_strategy', create_data_strategy_agents_with_context, create_data_strategy_tasks_with_data),
            ('compliance_risk', create_compliance_risk_agents_with_context, create_compliance_risk_tasks_with_data),
            ('information_management', create_information_management_agents_with_context, create_information_management_tasks_with_data),
            ('tender_response', create_tender_response_agents_with_context, create_tender_response_tasks_with_data),
            ('project_delivery', create_project_delivery_agents_with_context, create_project_delivery_tasks_with_data),
            ('technical_documentation', create_technical_documentation_agents_with_context, create_technical_documentation_tasks_with_data)
        ]
        
        for team_name, agent_creator, task_creator in teams:
            # Create team agents and tasks
            agents = agent_creator(llm, conversation_history)
            tasks = task_creator(*list(agents.values()), query, current_context, conversation_history)
            
            # Execute team
            crew = Crew(agents=list(agents.values()), tasks=tasks, process=Process.sequential, memory=False, max_rpm=5)
            team_result = crew.kickoff()
            
            # Store result and update context
            team_results[team_name] = str(team_result)
            current_context = str(team_result)
            
            # Add delay between teams
            time.sleep(10)
        
        # 4. Combine all results
        final_result = combine_seven_team_results(team_results, query)
        
        # 5. Save to memory
        if presearch_results.get('memory_manager'):
            presearch_results['memory_manager'].save_conversation(query, final_result)
        
        return final_result
        
    except Exception as e:
        st.error(f"Seven team workflow failed: {e}")
        return f"Error: {e}"
```

### Result Combination
```python
def combine_seven_team_results(team_results: Dict[str, str], query: str) -> str:
    """
    Pseudocode for combining seven team results
    """
    # 1. Create header
    header = f"""# Seven Team Workflow Results

**Query:** {query}
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Executive Summary

This comprehensive analysis covers research, data strategy, compliance, information management, tender response, project delivery, and technical documentation.

"""
    
    # 2. Team result sections
    team_sections = {
        'research_analysis': 'Research & Analysis',
        'data_strategy': 'Data Strategy & DAMA Implementation',
        'compliance_risk': 'Compliance & Risk Management',
        'information_management': 'Information Management',
        'tender_response': 'Tender Response',
        'project_delivery': 'Project Delivery',
        'technical_documentation': 'Technical Documentation'
    }
    
    # 3. Add each team's results
    combined_results = [header]
    for team_key, team_name in team_sections.items():
        if team_key in team_results:
            section = f"## {team_name}\n\n{team_results[team_key]}\n\n"
            combined_results.append(section)
    
    # 4. Add footer
    footer = f"""
---

**Workflow completed:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Total teams:** {len(team_results)}
**Status:** Successfully completed
"""
    
    combined_results.append(footer)
    
    return "".join(combined_results)
```

## Usage Examples

### Basic Workflow Execution
```python
from workflows import run_three_team_workflow, run_seven_team_workflow

# Three team workflow
result = run_three_team_workflow(
    query="Analyze digital twins in education",
    llm=llm,
    conversation_history=conversation_history
)

# Seven team workflow
result = run_seven_team_workflow(
    query="Create comprehensive AI strategy for schools",
    llm=llm,
    conversation_history=conversation_history
)
```

### Workflow Selection
```python
def select_workflow(workflow_type: str, query: str, llm, conversation_history: List[Any]) -> str:
    """
    Pseudocode for workflow selection
    """
    workflow_functions = {
        'single_team': run_crew_workflow,
        'two_team': run_two_team_workflow,
        'three_team': run_three_team_workflow,
        'four_team': run_four_team_workflow,
        'five_team': run_five_team_workflow,
        'six_team': run_six_team_workflow,
        'seven_team': run_seven_team_workflow
    }
    
    if workflow_type in workflow_functions:
        return workflow_functions[workflow_type](query, llm, conversation_history)
    else:
        raise ValueError(f"Unknown workflow type: {workflow_type}")
```

## Configuration

### Workflow Settings
```python
WORKFLOW_SETTINGS = {
    'max_rpm': 5,
    'max_execution_time': 300,
    'team_delay': 10,  # seconds between teams
    'memory_enabled': True,
    'presearch_enabled': True,
    'error_retry_attempts': 3,
    'progress_tracking': True
}
```

## Testing

### Workflow Tests
```python
def test_three_team_workflow():
    """Test three team workflow execution"""
    result = run_three_team_workflow(
        query="Test query",
        llm=test_llm,
        conversation_history=[]
    )
    
    assert isinstance(result, str)
    assert "Research & Analysis" in result
    assert "Data Strategy" in result
    assert "Compliance & Risk" in result

def test_seven_team_workflow():
    """Test seven team workflow execution"""
    result = run_seven_team_workflow(
        query="Test query",
        llm=test_llm,
        conversation_history=[]
    )
    
    assert isinstance(result, str)
    assert len(result) > 1000  # Should be comprehensive
```