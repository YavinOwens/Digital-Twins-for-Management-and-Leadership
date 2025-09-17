# Workflow Manager Module

This module handles the execution and management of CrewAI multi-agent workflows. It provides the core workflow execution logic, team coordination, and result processing for the multi-agent system.

## Structure

```
workflow_manager/
├── __init__.py                    # Module initialization
└── workflow_executor.py           # Main workflow execution functionality
```

## Key Components

### Workflow Executor
- **Single Team Workflow**: Basic research, analysis, and writing workflow
- **Two Team Workflow**: Research → Data Strategy workflow
- **Multi-Team Coordination**: Sequential team execution with context passing
- **Pre-search Integration**: Web and memory search before workflow execution

### Team Coordination
- **Sequential Execution**: Teams execute in order with context passing
- **Context Management**: Passing outputs between teams
- **Error Handling**: Graceful handling of team execution failures
- **Progress Tracking**: Real-time progress monitoring

## Pseudocode Examples

### Single Team Workflow
```python
def run_crew_workflow(query: str, llm, conversation_history=None, use_native_function_calling=False) -> str:
    """
    Pseudocode for single team workflow execution
    """
    try:
        # 1. Perform pre-search
        presearch_results = perform_workflow_presearch(query, "single_team", conversation_history)
        
        # 2. Create research analysis agents
        agents = create_research_analysis_agents_with_context(llm, conversation_history)
        
        # 3. Create research analysis tasks
        tasks = create_research_analysis_tasks_with_data(
            agents['researcher'], agents['analyst'], agents['writer'],
            query, presearch_results.get('combined_context', ''), conversation_history
        )
        
        # 4. Create crew
        crew = Crew(
            agents=list(agents.values()),
            tasks=tasks,
            process=Process.sequential,
            memory=False,
            max_rpm=5
        )
        
        # 5. Execute workflow
        result = crew.kickoff()
        
        # 6. Save to memory
        if presearch_results.get('memory_manager'):
            presearch_results['memory_manager'].save_conversation(query, str(result))
        
        return str(result)
        
    except Exception as e:
        st.error(f"Single team workflow failed: {e}")
        return f"Error: {e}"
```

### Two Team Workflow
```python
def run_two_team_workflow(query: str, llm, conversation_history: List[Any] = None, use_native_function_calling: bool = False) -> str:
    """
    Pseudocode for two team workflow execution
    """
    try:
        # 1. Perform pre-search
        presearch_results = perform_workflow_presearch(query, "two_team", conversation_history)
        
        # 2. Create first team (Research & Analysis)
        research_agents = create_research_analysis_agents_with_context(llm, conversation_history)
        research_tasks = create_research_analysis_tasks_with_data(
            research_agents['researcher'], research_agents['analyst'], research_agents['writer'],
            query, presearch_results.get('combined_context', ''), conversation_history
        )
        
        # 3. Execute first team
        research_crew = Crew(
            agents=list(research_agents.values()),
            tasks=research_tasks,
            process=Process.sequential,
            memory=False,
            max_rpm=5
        )
        
        research_result = research_crew.kickoff()
        
        # 4. Create second team (Data Strategy)
        data_strategy_agents = create_data_strategy_agents_with_context(llm, conversation_history)
        data_strategy_tasks = create_data_strategy_tasks_with_data(
            data_strategy_agents['data_governance_specialist'],
            data_strategy_agents['dcam_template_specialist'],
            data_strategy_agents['tranch_guidance_specialist'],
            query, str(research_result), conversation_history
        )
        
        # 5. Execute second team
        data_strategy_crew = Crew(
            agents=list(data_strategy_agents.values()),
            tasks=data_strategy_tasks,
            process=Process.sequential,
            memory=False,
            max_rpm=5
        )
        
        data_strategy_result = data_strategy_crew.kickoff()
        
        # 6. Combine results
        final_result = f"# Research & Analysis Results\n\n{research_result}\n\n# Data Strategy Results\n\n{data_strategy_result}"
        
        # 7. Save to memory
        if presearch_results.get('memory_manager'):
            presearch_results['memory_manager'].save_conversation(query, final_result)
        
        return final_result
        
    except Exception as e:
        st.error(f"Two team workflow failed: {e}")
        return f"Error: {e}"
```

### Pre-search Integration
```python
def perform_workflow_presearch(query: str, workflow_name: str, conversation_history: Optional[List[Any]] = None) -> Dict[str, Any]:
    """
    Pseudocode for pre-search functionality
    """
    try:
        # 1. Initialize pre-search manager
        presearch_manager = PreSearchManager(memory_enabled=True)
        
        # 2. Perform search and combine context
        search_results = presearch_manager.search_and_combine_context(query, conversation_history)
        
        # 3. Return structured results
        return {
            'combined_context': search_results.get('combined_context', ''),
            'web_results': search_results.get('web_results'),
            'memory_results': search_results.get('memory_results'),
            'memory_manager': presearch_manager.memory_manager,
            'search_metadata': search_results.get('search_metadata', {})
        }
        
    except Exception as e:
        logging.error(f"Pre-search failed: {e}")
        return {
            'combined_context': '',
            'web_results': None,
            'memory_results': None,
            'memory_manager': None,
            'search_metadata': {}
        }
```

### Multi-Team Workflow Pattern
```python
def run_multi_team_workflow(query: str, llm, team_configs: List[Dict], conversation_history: List[Any] = None) -> str:
    """
    Pseudocode for multi-team workflow execution
    """
    try:
        # 1. Perform pre-search
        presearch_results = perform_workflow_presearch(query, "multi_team", conversation_history)
        
        # 2. Initialize results
        team_results = {}
        current_context = presearch_results.get('combined_context', '')
        
        # 3. Execute teams sequentially
        for i, team_config in enumerate(team_configs, 1):
            # Create team agents
            agents = team_config['agent_creator'](llm, conversation_history)
            
            # Create team tasks
            tasks = team_config['task_creator'](
                *list(agents.values()),
                query, current_context, conversation_history
            )
            
            # Execute team
            crew = Crew(
                agents=list(agents.values()),
                tasks=tasks,
                process=Process.sequential,
                memory=False,
                max_rpm=5
            )
            
            team_result = crew.kickoff()
            team_results[f"team_{i}"] = str(team_result)
            
            # Update context for next team
            current_context = str(team_result)
            
            # Add delay between teams
            time.sleep(10)
        
        # 4. Combine all results
        final_result = combine_team_results(team_results, query)
        
        # 5. Save to memory
        if presearch_results.get('memory_manager'):
            presearch_results['memory_manager'].save_conversation(query, final_result)
        
        return final_result
        
    except Exception as e:
        st.error(f"Multi-team workflow failed: {e}")
        return f"Error: {e}"
```

### Result Combination
```python
def combine_team_results(team_results: Dict[str, str], query: str) -> str:
    """
    Pseudocode for combining team results
    """
    # 1. Create header
    header = f"# Multi-Agent Workflow Results\n\n**Query:** {query}\n\n"
    
    # 2. Add team results
    combined_results = []
    for team_name, team_result in team_results.items():
        team_section = f"## {team_name.replace('_', ' ').title()}\n\n{team_result}\n\n"
        combined_results.append(team_section)
    
    # 3. Combine all sections
    return header + "".join(combined_results)
```

### Error Handling and Recovery
```python
def handle_workflow_error(error: Exception, workflow_type: str) -> str:
    """
    Pseudocode for workflow error handling
    """
    error_message = str(error).lower()
    
    if "timeout" in error_message:
        return f"⏱️ {workflow_type} workflow timed out. Please try with a shorter query."
    
    elif "rate limit" in error_message:
        return f"⚠️ Rate limit exceeded for {workflow_type} workflow. Please wait and try again."
    
    elif "connection" in error_message:
        return f"🔌 Connection failed for {workflow_type} workflow. Please check your internet connection."
    
    elif "memory" in error_message:
        return f"💾 Memory error in {workflow_type} workflow. Please try again."
    
    else:
        return f"❌ {workflow_type} workflow failed: {error}"
```

### Progress Tracking
```python
def track_workflow_progress(workflow_type: str, current_team: int, total_teams: int) -> None:
    """
    Pseudocode for workflow progress tracking
    """
    # 1. Calculate progress percentage
    progress = (current_team / total_teams) * 100
    
    # 2. Create progress bar
    progress_bar = st.progress(progress / 100)
    
    # 3. Display status
    status_text = f"Executing {workflow_type}: Team {current_team}/{total_teams}"
    st.text(status_text)
    
    # 4. Update progress
    progress_bar.progress(progress / 100)
```

## Usage Examples

### Basic Workflow Execution
```python
from workflow_manager import run_crew_workflow, run_two_team_workflow

# Single team workflow
result = run_crew_workflow(
    query="Analyze digital twins in education",
    llm=llm,
    conversation_history=conversation_history
)

# Two team workflow
result = run_two_team_workflow(
    query="Create a data strategy for AI implementation",
    llm=llm,
    conversation_history=conversation_history
)
```

### Pre-search Integration
```python
from workflow_manager import perform_workflow_presearch

# Perform pre-search
presearch_results = perform_workflow_presearch(
    query="Digital transformation in schools",
    workflow_name="three_team",
    conversation_history=conversation_history
)

# Use combined context
combined_context = presearch_results['combined_context']
```

## Configuration

### Workflow Settings
```python
WORKFLOW_CONFIG = {
    'max_rpm': 5,
    'max_execution_time': 300,
    'team_delay': 10,  # seconds between teams
    'memory_enabled': True,
    'presearch_enabled': True,
    'error_retry_attempts': 3
}
```

### Team Configuration
```python
TEAM_CONFIGS = {
    'research_analysis': {
        'agent_creator': create_research_analysis_agents_with_context,
        'task_creator': create_research_analysis_tasks_with_data,
        'team_name': 'Research & Analysis'
    },
    'data_strategy': {
        'agent_creator': create_data_strategy_agents_with_context,
        'task_creator': create_data_strategy_tasks_with_data,
        'team_name': 'Data Strategy'
    }
    # ... other teams
}
```

## Testing

### Workflow Tests
```python
def test_single_team_workflow():
    """Test single team workflow execution"""
    result = run_crew_workflow(
        query="Test query",
        llm=test_llm,
        conversation_history=[]
    )
    
    assert isinstance(result, str)
    assert len(result) > 0

def test_two_team_workflow():
    """Test two team workflow execution"""
    result = run_two_team_workflow(
        query="Test query",
        llm=test_llm,
        conversation_history=[]
    )
    
    assert isinstance(result, str)
    assert "Research & Analysis" in result
    assert "Data Strategy" in result
```
