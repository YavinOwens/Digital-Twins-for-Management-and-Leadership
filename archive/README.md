# Archive Folder

This folder contains archived files and folders that are no longer actively used in the main application.

## 📁 **Archived Contents**

### **Agents Folder** (`agents/`)
- **Status**: ARCHIVED
- **Reason**: Replaced by modular `agent_teams/` structure
- **Contains**: 
  - Original agent files (individual and team-based)
  - Legacy agent factory
  - Migration documentation
- **Replacement**: `agent_teams/` package

### **Agent Tasks Folder** (`agent_tasks/`)
- **Status**: ARCHIVED
- **Reason**: Replaced by modular `agent_teams/` structure (tasks now included with agents)
- **Contains**: 
  - Original task files (individual and team-based)
  - Task factory and optimization files
  - Migration documentation
- **Replacement**: `agent_teams/` package (each team contains both agents and tasks)

### **PDF Test Outputs** (`_pdf_test_outputs/`)
- **Status**: ARCHIVED
- **Reason**: Test files for PDF generation functionality
- **Contains**: Sample PDF outputs from testing

### **Test Files** (`_tests/`)
- **Status**: ARCHIVED
- **Reason**: Development and debugging test files
- **Contains**: Various test scripts and debugging tools

## 🚨 **Important Notes**

1. **These files are ARCHIVED and no longer maintained**
2. **Do NOT use these files for new development**
3. **All functionality has been moved to active packages**
4. **These files are kept for reference only**

## 🔄 **Active Replacements**

| Archived | Active Replacement |
|----------|-------------------|
| `agents/` | `agent_teams/` |
| `agent_tasks/` | `agent_teams/` (tasks included with agents) |
| `_pdf_test_outputs/` | `team_outputs/` |
| `_tests/` | Individual test files in respective packages |

## 🗑️ **Cleanup**

These files can be safely deleted once you've confirmed that:
1. All code has been migrated to active packages
2. No references to these files remain
3. The new structure is working correctly
4. You no longer need reference access to old code

## 📚 **Documentation**

- **Agents Migration**: See `agents/README.md`
- **Agent Tasks Migration**: See `agent_tasks/README.md`
- **Agent Teams**: See `agent_teams/README.md`
- **Team Outputs**: See `team_outputs/README.md`

---

**Archived Date**: January 2025  
**Status**: ARCHIVED  
**Purpose**: Reference and historical preservation
