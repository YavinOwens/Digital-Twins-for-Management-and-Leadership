# Agent Teams Documentation

This directory contains detailed documentation for all agent teams in the CrewAI Multi-Agent Workflow System.

## Overview

The system includes 7 specialized agent teams, each designed to handle specific aspects of business analysis, research, and documentation. Teams work sequentially, with each team building upon the work of previous teams.

## Team Structure

Each agent team follows a consistent structure:

```
agent_teams/
├── team_name/
│   ├── __init__.py          # Module initialization and exports
│   ├── agents.py            # Agent definitions and configurations
│   └── tasks.py             # Task definitions and workflows
```

## Team Descriptions

### 1. Research & Analysis Team
**Purpose**: Conduct comprehensive research and analysis on given topics
**Agents**: Research Specialist, Data Analyst, Content Writer
**Key Capabilities**:
- Web search and information gathering
- Data analysis and insight extraction
- Content synthesis and writing
- Citation and reference management

### 2. Data Strategy Team
**Purpose**: Develop data governance strategies and DAMA implementation
**Agents**: Data Governance Specialist, DCAM Template Specialist, Tranch Guidance Specialist
**Key Capabilities**:
- Data governance framework development
- DCAM template creation
- Tranch guidance for phased implementation
- DAMA-DMBOK compliance

### 3. Compliance & Risk Team
**Purpose**: Ensure regulatory compliance and risk management
**Agents**: Compliance Specialist, Risk Management Specialist, Audit & Governance Specialist
**Key Capabilities**:
- Regulatory compliance assessment
- Risk identification and mitigation
- Audit framework development
- Governance structure design

### 4. Information Management Team
**Purpose**: Manage information lifecycle and data quality
**Agents**: Information Governance Specialist, Metadata Management Specialist, Data Quality Specialist
**Key Capabilities**:
- Information lifecycle management
- Metadata cataloging and lineage
- Data quality assessment and remediation
- Data classification and retention

### 5. Tender Response Team
**Purpose**: Create compelling tender responses and proposals
**Agents**: Tender Response Specialist, Proposal Writer, Compliance Expert
**Key Capabilities**:
- Tender analysis and response strategy
- Proposal writing and formatting
- Compliance verification
- Competitive positioning

### 6. Project Delivery Team
**Purpose**: Execute technical projects and manage delivery
**Agents**: Data Engineer, Data Scientist, Data Architect, DevOps Engineer, Project Manager
**Key Capabilities**:
- Technical architecture design
- Data pipeline development
- Infrastructure management
- Project coordination and delivery

### 7. Technical Documentation Team
**Purpose**: Create comprehensive technical documentation
**Agents**: Data Modeling Specialist, Python Code Specialist, SQL Code Specialist, PySpark Code Specialist, Technical Writer
**Key Capabilities**:
- Data model design and documentation
- Code generation (Python, SQL, PySpark)
- Technical writing and documentation
- Diagram and visualization creation

## Agent Configuration

All agents follow a consistent configuration pattern:

```python
Agent(
    role="Agent Role",
    goal="Specific goal for this agent",
    backstory="Detailed background and expertise",
    verbose=True,
    allow_delegation=False,
    llm=llm,
    max_iter=3,
    max_rpm=5,
    max_execution_time=300,
    memory=False
)
```

### Configuration Parameters

- **role**: The agent's role in the team
- **goal**: What the agent aims to achieve
- **backstory**: Agent's background and expertise
- **verbose**: Enable detailed logging
- **allow_delegation**: Prevent task delegation
- **llm**: Language model instance
- **max_iter**: Maximum iterations per task
- **max_rpm**: Rate limiting (requests per minute)
- **max_execution_time**: Task timeout in seconds
- **memory**: Disable persistent memory (handled by system)

## Task Configuration

Tasks are designed to work with specific agents and follow this pattern:

```python
Task(
    description="What the agent needs to do",
    expected_output="What the agent should produce",
    agent=agent,
    timeout=200
)
```

### Task Parameters

- **description**: Detailed task description
- **expected_output**: Clear output specification
- **agent**: Which agent will execute the task
- **timeout**: Task timeout in seconds

## Context Passing

Teams pass context between each other using the `context` parameter:

```python
# Team 1 creates context
team1_context = {
    "research_data": research_results,
    "analysis_insights": analysis_output,
    "content_summary": content_output
}

# Team 2 receives context
team2_tasks = create_team2_tasks_with_data(
    agents, query, team1_context, conversation_history
)
```

## Memory Integration

All teams integrate with the system's memory system:

- **Conversation History**: Past conversations for context
- **Search Results**: Web and memory search results
- **Team Outputs**: Previous team outputs
- **Metadata**: Workflow and execution metadata

## Error Handling

Each team includes robust error handling:

- **Retry Logic**: Automatic retry for failed tasks
- **Graceful Degradation**: Fallback mechanisms
- **Error Recovery**: Automatic error recovery
- **Progress Tracking**: Real-time progress monitoring

## Performance Optimization

Teams are optimized for performance:

- **Rate Limiting**: Built-in request throttling
- **Caching**: Intelligent caching for repeated requests
- **Parallel Processing**: Concurrent task execution where possible
- **Memory Management**: Efficient memory usage

## Testing

Each team can be tested independently:

```python
# Test individual agents
from agent_teams.research_analysis.agents import create_research_analysis_agents_with_context

# Test team workflows
from agent_teams.research_analysis.tasks import create_research_analysis_tasks_with_data

# Test complete team execution
from workflows.workflow_executor import run_crew_workflow
```

## Extending Teams

To add new teams:

1. Create new directory in `agent_teams/`
2. Add `agents.py` and `tasks.py` files
3. Follow existing patterns for agent and task creation
4. Update workflow files to include new team
5. Add team to main application

## Best Practices

1. **Consistent Naming**: Use consistent naming conventions
2. **Clear Roles**: Define clear, specific roles for agents
3. **Detailed Tasks**: Provide detailed task descriptions
4. **Error Handling**: Include comprehensive error handling
5. **Testing**: Test thoroughly with different scenarios
6. **Documentation**: Keep documentation up to date
7. **Performance**: Optimize for performance and reliability

## Troubleshooting

Common issues and solutions:

1. **Agent Not Responding**: Check LLM configuration and API keys
2. **Task Timeout**: Increase timeout or optimize task complexity
3. **Memory Issues**: Check memory configuration and usage
4. **Context Loss**: Verify context passing between teams
5. **Performance Issues**: Check rate limiting and caching

## Support

For issues with specific teams:
1. Check the team-specific documentation
2. Review error logs and messages
3. Test with simplified scenarios
4. Verify configuration and dependencies
5. Check system requirements and resources
