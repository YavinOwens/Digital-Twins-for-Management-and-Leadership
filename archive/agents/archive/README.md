# Archived Agent Files

This folder contains the original agent files that have been moved to the new modular `agent_teams/` structure.

## 📁 **Archived Files**

### **Individual Agent Files**
- `researcher_agent.py` → Now in `agent_teams/research_analysis/agents.py`
- `analyst_agent.py` → Now in `agent_teams/research_analysis/agents.py`
- `writer_agent.py` → Now in `agent_teams/research_analysis/agents.py`

### **Team Agent Files**
- `data_strategy_agents.py` → Now in `agent_teams/data_strategy/agents.py`
- `compliance_risk_agents.py` → Now in `agent_teams/compliance_risk/agents.py`
- `information_management_agents.py` → Now in `agent_teams/information_management/agents.py`
- `tender_response_agents.py` → Now in `agent_teams/tender_response/agents.py`
- `project_delivery_agents.py` → Now in `agent_teams/project_delivery/agents.py`
- `technical_documentation_agents.py` → Now in `agent_teams/technical_documentation/agents.py`

## 🚨 **Important Notes**

1. **These files are ARCHIVED and no longer maintained**
2. **Do NOT use these files for new development**
3. **All functionality has been moved to `agent_teams/`**
4. **These files are kept for reference only**

## 🔄 **Migration**

If you need to reference the old code:

1. **Find the equivalent team** in `agent_teams/`
2. **Use the new modular structure**
3. **Update your imports** to use `agent_teams/`

## 📚 **New Structure**

```
agent_teams/
├── research_analysis/          # Contains researcher, analyst, writer
├── data_strategy/              # Contains data strategy agents
├── compliance_risk/            # Contains compliance & risk agents
├── information_management/     # Contains information management agents
├── tender_response/            # Contains tender response agents
├── project_delivery/           # Contains project delivery agents
└── technical_documentation/    # Contains technical documentation agents
```

## 🗑️ **Cleanup**

These files can be safely deleted once you've confirmed that:
1. All code has been migrated to `agent_teams/`
2. No references to these files remain
3. The new structure is working correctly

---

**Archived Date**: January 2025  
**Status**: ARCHIVED  
**Replacement**: `agent_teams/` package
