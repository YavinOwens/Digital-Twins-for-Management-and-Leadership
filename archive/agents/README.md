# Agents Package - ARCHIVED

⚠️ **IMPORTANT NOTICE**: This package has been **ARCHIVED** and is no longer actively maintained.

## 🚀 **Use the New Modular Structure Instead**

The application now uses the **`agent_teams/`** folder for all agent-related functionality. This new structure provides better organization, maintainability, and scalability.

### **New Location**: `agent_teams/`

```
agent_teams/
├── research_analysis/          # Team 1: Research & Analysis
├── data_strategy/              # Team 2: Data Strategy & DAMA
├── compliance_risk/            # Team 3: Compliance & Risk
├── information_management/     # Team 4: Information Management
├── tender_response/            # Team 5: Tender Response
├── project_delivery/           # Team 6: Project Delivery
└── technical_documentation/    # Team 7: Technical Documentation
```

## 📋 **Migration Guide**

### **Old Import (Deprecated)**
```python
from agents import create_crew_agents
from agents.agent_factory import create_data_strategy_agents_with_context
```

### **New Import (Recommended)**
```python
from agent_teams.research_analysis import create_research_analysis_agents_with_context
from agent_teams.data_strategy import create_data_strategy_agents_with_context
```

## 🔄 **What Changed**

| Old Structure | New Structure |
|---------------|---------------|
| `agents/researcher_agent.py` | `agent_teams/research_analysis/agents.py` |
| `agents/data_strategy_agents.py` | `agent_teams/data_strategy/agents.py` |
| `agents/compliance_risk_agents.py` | `agent_teams/compliance_risk/agents.py` |
| `agents/information_management_agents.py` | `agent_teams/information_management/agents.py` |
| `agents/tender_response_agents.py` | `agent_teams/tender_response/agents.py` |
| `agents/project_delivery_agents.py` | `agent_teams/project_delivery/agents.py` |
| `agents/technical_documentation_agents.py` | `agent_teams/technical_documentation/agents.py` |

## 🎯 **Benefits of the New Structure**

### **🧹 Modularity**
- Each team is self-contained
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
- **Old Agent Files**: 📦 Moved to `agents/archive/` folder
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
| Research & Analysis agents | `agent_teams/research_analysis/` |
| Data Strategy agents | `agent_teams/data_strategy/` |
| Compliance & Risk agents | `agent_teams/compliance_risk/` |
| Information Management agents | `agent_teams/information_management/` |
| Tender Response agents | `agent_teams/tender_response/` |
| Project Delivery agents | `agent_teams/project_delivery/` |
| Technical Documentation agents | `agent_teams/technical_documentation/` |

---

**Last Updated**: January 2025  
**Status**: ARCHIVED  
**Replacement**: `agent_teams/` package
