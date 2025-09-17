# Agent Tasks Package - ARCHIVED

⚠️ **IMPORTANT NOTICE**: This package has been **ARCHIVED** and is no longer actively maintained.

## 🚀 **Use the New Modular Structure Instead**

The application now uses the **`agent_teams/`** folder for all task-related functionality. Each team now contains both agents and tasks in a single, cohesive module.

### **New Location**: `agent_teams/`

```
agent_teams/
├── research_analysis/
│   ├── agents.py          # Research, Analyst, Writer agents
│   └── tasks.py           # Research, Analysis, Writing tasks
├── data_strategy/
│   ├── agents.py          # Data Strategy agents
│   └── tasks.py           # Data Strategy tasks
├── compliance_risk/
│   ├── agents.py          # Compliance & Risk agents
│   └── tasks.py           # Compliance & Risk tasks
├── information_management/
│   ├── agents.py          # Information Management agents
│   └── tasks.py           # Information Management tasks
├── tender_response/
│   ├── agents.py          # Tender Response agents
│   └── tasks.py           # Tender Response tasks
├── project_delivery/
│   ├── agents.py          # Project Delivery agents
│   └── tasks.py           # Project Delivery tasks
└── technical_documentation/
    ├── agents.py          # Technical Documentation agents
    └── tasks.py           # Technical Documentation tasks
```

## 📋 **Migration Guide**

### **Old Import (Deprecated)**
```python
from agent_tasks import create_crew_tasks, create_crew_tasks_with_data
from agent_tasks.task_factory import create_data_strategy_tasks_with_data
```

### **New Import (Recommended)**
```python
from agent_teams.research_analysis import create_research_analysis_tasks_with_data
from agent_teams.data_strategy import create_data_strategy_tasks_with_data
```

## 🔄 **What Changed**

| Old Structure | New Structure |
|---------------|---------------|
| `agent_tasks/research_task.py` | `agent_teams/research_analysis/tasks.py` |
| `agent_tasks/data_strategy_tasks.py` | `agent_teams/data_strategy/tasks.py` |
| `agent_tasks/compliance_risk_tasks.py` | `agent_teams/compliance_risk/tasks.py` |
| `agent_tasks/information_management_tasks.py` | `agent_teams/information_management/tasks.py` |
| `agent_tasks/tender_response_tasks.py` | `agent_teams/tender_response/tasks.py` |
| `agent_tasks/project_delivery_tasks.py` | `agent_teams/project_delivery/tasks.py` |
| `agent_tasks/technical_documentation_tasks.py` | `agent_teams/technical_documentation/tasks.py` |

## 🎯 **Benefits of the New Structure**

### **🧹 Modularity**
- Each team contains both agents and tasks
- Clear separation of concerns
- Easy to add/remove teams

### **🔧 Maintainability**
- Changes to one team don't affect others
- Easier debugging and testing
- Better code organization

### **📈 Scalability**
- Simple to add new teams
- Easy to extend existing teams
- Flexible team composition

### **🧪 Testability**
- Each team can be tested independently
- Clear interfaces between teams
- Isolated functionality

## 📁 **Current Status**

- **Streamlit Application**: ✅ Uses `agent_teams/` structure
- **Old Task Files**: 📦 Moved to `archive/agent_tasks/` folder
- **Backward Compatibility**: ⚠️ Limited - use new structure for new development

## 🚨 **Important Notes**

1. **Do NOT use this package for new development**
2. **All new features should use `agent_teams/`**
3. **Existing code may still work but is not maintained**
4. **Migration to new structure is recommended**

## 📚 **Documentation**

- **New Structure**: See `agent_teams/README.md`
- **Migration Guide**: See above
- **Team Descriptions**: See `agent_teams/README.md`

## 🔍 **Finding What You Need**

| Looking For | Go To |
|-------------|-------|
| Research & Analysis tasks | `agent_teams/research_analysis/tasks.py` |
| Data Strategy tasks | `agent_teams/data_strategy/tasks.py` |
| Compliance & Risk tasks | `agent_teams/compliance_risk/tasks.py` |
| Information Management tasks | `agent_teams/information_management/tasks.py` |
| Tender Response tasks | `agent_teams/tender_response/tasks.py` |
| Project Delivery tasks | `agent_teams/project_delivery/tasks.py` |
| Technical Documentation tasks | `agent_teams/technical_documentation/tasks.py` |

## 📦 **Archived Files**

This package contained the following files:
- `__init__.py` - Package initialization
- `analysis_task.py` - Analysis task definitions
- `compliance_risk_tasks.py` - Compliance & Risk task definitions
- `data_strategy_tasks.py` - Data Strategy task definitions
- `information_management_tasks.py` - Information Management task definitions
- `optimized_task_factory.py` - Optimized task factory
- `project_delivery_tasks.py` - Project Delivery task definitions
- `research_task.py` - Research task definitions
- `task_factory.py` - Main task factory
- `technical_documentation_tasks.py` - Technical Documentation task definitions
- `tender_response_tasks.py` - Tender Response task definitions
- `writing_task.py` - Writing task definitions

---

**Last Updated**: January 2025  
**Status**: ARCHIVED  
**Replacement**: `agent_teams/` package
