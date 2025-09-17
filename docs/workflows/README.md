# Workflows Documentation

This directory contains detailed documentation for all workflow execution functions in the CrewAI Multi-Agent Workflow System.

## Overview

The system supports 7 different workflow types, each orchestrating multiple agent teams in sequential execution. Workflows are designed to handle complex business analysis and documentation tasks by leveraging specialized agent teams.

## Workflow Types

### 1. Single Team Workflow
**File**: `workflow_executor.py`
**Function**: `run_crew_workflow`
**Teams**: Research & Analysis
**Purpose**: Basic research and analysis tasks
**Execution Time**: ~5-10 minutes
**Use Cases**: Simple research questions, basic analysis, content creation

### 2. Two Team Workflow
**File**: `workflow_executor.py`
**Function**: `run_two_team_workflow`
**Teams**: Research & Analysis → Data Strategy
**Purpose**: Research with data governance strategy
**Execution Time**: ~10-15 minutes
**Use Cases**: Data strategy development, DAMA implementation, governance planning

### 3. Three Team Workflow
**File**: `three_team_workflow.py`
**Function**: `run_three_team_workflow`
**Teams**: Research & Analysis → Data Strategy → Compliance & Risk
**Purpose**: Research with strategy and compliance
**Execution Time**: ~15-20 minutes
**Use Cases**: Compliance planning, risk assessment, regulatory analysis

### 4. Four Team Workflow
**File**: `run_four_team_workflow.py`
**Function**: `run_four_team_workflow`
**Teams**: Research & Analysis → Data Strategy → Compliance & Risk → Information Management
**Purpose**: Complete data management lifecycle
**Execution Time**: ~20-25 minutes
**Use Cases**: Comprehensive data management, information governance, metadata management

### 5. Five Team Workflow
**File**: `run_five_team_workflow.py`
**Function**: `run_five_team_workflow`
**Teams**: Research & Analysis → Data Strategy → Compliance & Risk → Information Management → Tender Response
**Purpose**: Data management with tender response
**Execution Time**: ~25-30 minutes
**Use Cases**: Tender responses, proposal writing, competitive positioning

### 6. Six Team Workflow
**File**: `run_six_team_workflow.py`
**Function**: `run_six_team_workflow`
**Teams**: Research & Analysis → Data Strategy → Compliance & Risk → Information Management → Tender Response → Project Delivery
**Purpose**: Complete project lifecycle
**Execution Time**: ~30-35 minutes
**Use Cases**: Project delivery, technical implementation, end-to-end solutions

### 7. Seven Team Workflow
**File**: `run_seven_team_workflow.py`
**Function**: `run_seven_team_workflow`
**Teams**: Research & Analysis → Data Strategy → Compliance & Risk → Information Management → Tender Response → Project Delivery → Technical Documentation
**Purpose**: Complete solution with documentation
**Execution Time**: ~35-40 minutes
**Use Cases**: Comprehensive solutions, technical documentation, complete project delivery

## Workflow Execution Pattern

All workflows follow a consistent execution pattern:

```python
def run_workflow(query: str, llm, conversation_history: List[Any]) -> str:
    """
    Execute workflow with multiple teams
    """
    # 1. Pre-search phase
    presearch_results = perform_workflow_presearch(query, conversation_history)
    
    # 2. Team 1 execution
    team1_result = execute_team1(presearch_results)
    
    # 3. Team 2 execution (with Team 1 context)
    team2_result = execute_team2(team1_result)
    
    # 4. Continue with remaining teams...
    
    # 5. Return final result
    return final_result
```

## Pre-search Phase

All workflows begin with a pre-search phase that combines:

- **Web Search**: DuckDuckGo search for current information
- **Memory Search**: ChromaDB search for past conversations
- **Context Integration**: Combining search results with user query

```python
def perform_workflow_presearch(query: str, conversation_history: List[Any]) -> Dict[str, Any]:
    """
    Perform pre-search to gather comprehensive context
    """
    # Web search
    web_results = search_web(query)
    
    # Memory search
    memory_results = search_memory(query, conversation_history)
    
    # Combine results
    return {
        "query": query,
        "web_results": web_results,
        "memory_results": memory_results,
        "combined_context": f"{query}\n\nWeb Results:\n{web_results}\n\nMemory Results:\n{memory_results}"
    }
```

## Team Execution

Each team is executed using CrewAI's Crew system:

```python
def execute_team(agents: Dict[str, Agent], tasks: List[Task], team_name: str) -> str:
    """
    Execute a team of agents
    """
    # Create crew
    crew = Crew(
        agents=list(agents.values()),
        tasks=tasks,
        process=Process.sequential,
        memory=False,
        max_rpm=5
    )
    
    # Execute crew
    result = crew.kickoff()
    
    # Add delay between teams
    time.sleep(10)
    
    return result
```

## Context Passing

Context is passed between teams using the `context` parameter:

```python
# Team 1 creates context
team1_context = {
    "research_data": team1_result,
    "analysis_insights": analysis_output,
    "content_summary": content_output
}

# Team 2 receives context
team2_tasks = create_team2_tasks_with_data(
    agents, query, team1_context, conversation_history
)
```

## Error Handling

All workflows include comprehensive error handling:

```python
try:
    result = crew.kickoff()
    if result and result.strip():
        return result
    else:
        raise Exception("Empty response from crew")
except Exception as e:
    print(f"Error in {team_name} execution: {e}")
    # Implement fallback or retry logic
    raise
```

## Performance Optimization

Workflows are optimized for performance:

- **Rate Limiting**: `max_rpm=5` for all crews
- **Timeouts**: `max_execution_time=300` for all agents
- **Delays**: 10-second delays between teams
- **Memory Management**: Efficient memory usage
- **Caching**: Intelligent caching for repeated requests

## Memory Integration

All workflows integrate with the system's memory system:

- **Conversation History**: Past conversations for context
- **Search Results**: Web and memory search results
- **Team Outputs**: Previous team outputs
- **Metadata**: Workflow and execution metadata

## Output Management

Workflow outputs are managed through the team output system:

```python
# Save team outputs
team_outputs = {
    "team1": team1_result,
    "team2": team2_result,
    # ... other teams
}

save_team_outputs(
    workflow_type="seven_team",
    query=query,
    team_outputs=team_outputs,
    metadata={"execution_time": execution_time}
)
```

## Testing

Workflows can be tested independently:

```python
# Test single team workflow
from workflows.workflow_executor import run_crew_workflow

# Test multi-team workflow
from workflows.run_seven_team_workflow import run_seven_team_workflow

# Test with different queries
result = run_seven_team_workflow("Test query", llm, [])
```

## Configuration

Workflow behavior can be configured through environment variables:

- `DEFAULT_TEMPERATURE`: Model temperature
- `DEFAULT_MAX_TOKENS`: Maximum tokens per response
- `MAX_RPM`: Rate limiting
- `MAX_EXECUTION_TIME`: Task timeout
- `TEAM_DELAY`: Delay between teams

## Monitoring

Workflows include comprehensive monitoring:

- **Progress Tracking**: Real-time progress updates
- **Error Logging**: Detailed error logging
- **Performance Metrics**: Execution time and resource usage
- **Output Validation**: Result validation and quality checks

## Troubleshooting

Common workflow issues and solutions:

1. **Empty Responses**: Check LLM configuration and API keys
2. **Timeout Errors**: Increase timeout or optimize task complexity
3. **Memory Issues**: Check memory configuration and usage
4. **Context Loss**: Verify context passing between teams
5. **Performance Issues**: Check rate limiting and caching

## Best Practices

1. **Error Handling**: Include comprehensive error handling
2. **Progress Tracking**: Provide real-time progress updates
3. **Context Management**: Ensure proper context passing
4. **Performance**: Optimize for performance and reliability
5. **Testing**: Test thoroughly with different scenarios
6. **Documentation**: Keep documentation up to date
7. **Monitoring**: Include comprehensive monitoring and logging

## Extending Workflows

To add new workflows:

1. Create new file in `workflows/` directory
2. Follow existing function signature pattern
3. Import required agent and task creation functions
4. Add to `__init__.py` exports
5. Update main application to include new workflow
6. Test thoroughly with different scenarios

## Support

For issues with specific workflows:
1. Check the workflow-specific documentation
2. Review error logs and messages
3. Test with simplified scenarios
4. Verify configuration and dependencies
5. Check system requirements and resources
