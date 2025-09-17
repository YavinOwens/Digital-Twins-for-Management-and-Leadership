# Agent Teams Module

This module contains all agent teams organized by functionality. Each team has its own folder with agents and tasks, making the codebase more modular and maintainable.

## Structure

```
agent_teams/
├── __init__.py                           # Main module initialization
├── research_analysis/                    # Team 1: Research & Analysis
│   ├── __init__.py
│   ├── agents.py                        # Research, Analyst, Writer agents
│   └── tasks.py                         # Research, Analysis, Writing tasks
├── data_strategy/                        # Team 2: Data Strategy & DAMA
│   ├── __init__.py
│   ├── agents.py                        # Governance, DCAM, Tranch agents
│   └── tasks.py                         # Data governance, DCAM, Tranch tasks
├── compliance_risk/                      # Team 3: Compliance & Risk
│   ├── __init__.py
│   ├── agents.py                        # Compliance, Risk, Audit agents
│   └── tasks.py                         # Compliance, Risk, Audit tasks
├── information_management/               # Team 4: Information Management
│   ├── __init__.py
│   ├── agents.py                        # Info Governance, Metadata, Data Quality agents
│   └── tasks.py                         # Information management tasks
├── tender_response/                      # Team 5: Tender Response
│   ├── __init__.py
│   ├── agents.py                        # Tender, Proposal, Compliance agents
│   └── tasks.py                         # Tender response tasks
├── project_delivery/                     # Team 6: Project Delivery
│   ├── __init__.py
│   ├── agents.py                        # Data Engineer, Scientist, Architect, DevOps, PM agents
│   └── tasks.py                         # Project delivery tasks
├── technical_documentation/              # Team 7: Technical Documentation
│   ├── __init__.py
│   ├── agents.py                        # Data Modeling, Python, SQL, PySpark, Tech Writer agents
│   └── tasks.py                         # Technical documentation tasks
└── test_modular_structure.py            # Test script for the modular structure
```

## Pseudocode Examples

### Agent Creation Pattern
```python
def create_agent(role: str, goal: str, backstory: str, llm) -> Agent:
    """
    Pseudocode for creating any agent
    """
    return Agent(
        role=role,                    # Agent's role (e.g., "Research Specialist")
        goal=goal,                    # What the agent aims to achieve
        backstory=backstory,          # Agent's background and expertise
        verbose=True,                 # Enable detailed logging
        allow_delegation=False,       # Prevent task delegation
        llm=llm,                     # Language model instance
        max_iter=3,                  # Maximum iterations per task
        max_rpm=5,                   # Rate limiting (requests per minute)
        max_execution_time=300,      # Task timeout in seconds
        memory=False                 # Disable persistent memory
    )
```

### Task Creation Pattern
```python
def create_task(agent: Agent, description: str, expected_output: str) -> Task:
    """
    Pseudocode for creating any task
    """
    return Task(
        description=description,      # What the agent needs to do
        expected_output=expected_output,  # What the agent should produce
        agent=agent,                 # Which agent will execute this task
        timeout=200                  # Task timeout in seconds
    )
```

### Team Workflow Pattern
```python
def run_team_workflow(query: str, llm, conversation_history: List[Any]) -> str:
    """
    Pseudocode for running any team workflow
    """
    # 1. Create agents for the team
    agents = create_team_agents_with_context(llm, conversation_history)
    
    # 2. Create tasks for the team
    tasks = create_team_tasks_with_data(
        agents, query, previous_team_data, conversation_history
    )
    
    # 3. Create crew with agents and tasks
    crew = Crew(
        agents=list(agents.values()),
        tasks=tasks,
        process=Process.sequential,
        memory=False,
        max_rpm=5
    )
    
    # 4. Execute the crew
    result = crew.kickoff()
    
    # 5. Return the result
    return result
```

## Team Descriptions

### Team 1 - Research & Analysis
- **Research Specialist**: Conducts web research and gathers information
- **Data Analyst**: Analyzes findings and provides insights
- **Content Writer**: Creates structured reports and summaries

### Team 2 - Data Strategy & DAMA
- **Data Governance Specialist**: Creates DAMA-DMBOK frameworks
- **DCAM Template Specialist**: Develops capability assessment templates
- **Tranch Guidance Specialist**: Designs implementation roadmaps

### Team 3 - Compliance & Risk
- **Compliance Specialist**: Ensures regulatory compliance
- **Risk Management Specialist**: Conducts risk assessments
- **Audit & Governance Specialist**: Designs governance frameworks

### Team 4 - Information Management
- **Information Governance Specialist**: Manages information lifecycle
- **Metadata Management Specialist**: Creates metadata frameworks
- **Data Quality Specialist**: Establishes quality standards

### Team 5 - Tender Response
- **Tender Response Specialist**: Analyzes tender requirements
- **Proposal Writer**: Creates compelling responses
- **Compliance Expert**: Ensures tender compliance

### Team 6 - Project Delivery
- **Data Engineer**: Designs data infrastructure
- **Data Scientist**: Develops analytics models
- **Data Architect**: Creates system architecture
- **DevOps Engineer**: Implements deployment
- **Project Manager**: Coordinates delivery

### Team 7 - Technical Documentation
- **Data Modeling Specialist**: Creates diagrams and data models
- **Python Code Specialist**: Generates Python code
- **SQL Code Specialist**: Creates SQL queries and schemas
- **PySpark Code Specialist**: Develops big data processing code
- **Technical Writer**: Creates comprehensive documentation

## Usage

### Importing Teams
```python
# Import specific team
from agent_teams.research_analysis import create_research_analysis_agents_with_context

# Import all teams
from agent_teams import ResearchAnalysisTeam, DataStrategyTeam, etc.
```

### Creating Agents
```python
# Create research analysis agents
research_agents = create_research_analysis_agents_with_context(llm, conversation_history)

# Access specific agents
researcher = research_agents['researcher']
analyst = research_agents['analyst']
writer = research_agents['writer']
```

### Creating Tasks
```python
# Create research analysis tasks
tasks = create_research_analysis_tasks_with_data(
    researcher, analyst, writer, query, search_results, conversation_history
)
```

## Benefits

### 🧹 **Modularity**
- Each team is self-contained with its own agents and tasks
- Easy to add, remove, or modify individual teams
- Clear separation of concerns

### 🔧 **Maintainability**
- Changes to one team don't affect others
- Easier to debug and test individual components
- Clear file organization

### 📈 **Scalability**
- Easy to add new teams
- Simple to extend existing teams
- Flexible team composition

### 🧪 **Testability**
- Each team can be tested independently
- Clear interfaces between teams
- Isolated functionality

## File Organization

### agents.py
Contains agent definitions for the team:
- Agent role, goal, and backstory
- Agent configuration and parameters
- Helper functions for agent creation

### tasks.py
Contains task definitions for the team:
- Task descriptions and expected outputs
- Task dependencies and context
- Helper functions for task creation

### __init__.py
Exports the team's public interface:
- Agent creation functions
- Task creation functions
- Team-specific utilities

## Testing

Run the test script to verify the modular structure:
```bash
python agent_teams/test_modular_structure.py
```

This will test:
- All team modules can be imported
- Required files exist in each team directory
- Team structure is properly organized

## Migration from Old Structure

The old `agents/` and `agent_tasks/` folders have been reorganized into this modular structure:

- **Old**: `agents/research_agent.py` → **New**: `agent_teams/research_analysis/agents.py`
- **Old**: `agent_tasks/research_task.py` → **New**: `agent_teams/research_analysis/tasks.py`

All imports have been updated in `streamlit_app.py` to use the new modular structure.
