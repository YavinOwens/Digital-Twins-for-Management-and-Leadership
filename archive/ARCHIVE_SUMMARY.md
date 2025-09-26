# Archive Summary

This document summarizes the files that have been moved to the archive folder for cleanup and organization.

## Archived Files and Folders

### Development Files (`archive/development_files/`)
- `test_llm_direct.py` - Direct LLM testing script
- `test_retry_llm.py` - LLM retry mechanism testing
- `test_robust_llm_v2.py` - Robust LLM v2 testing
- `test_workflow_complete.py` - Complete workflow testing
- `test_modular_structure.py` - Modular structure testing (from agent_teams/)
- `test_presearch.py` - Pre-search functionality testing (from presearch/)

### Old Workflows (`archive/old_workflows/`)
- `three_team_workflow.py` - Original three-team workflow
- `three_team_workflow_broken.py` - Broken version of three-team workflow
- `three_team_workflow_clean.py` - Clean version of three-team workflow
- `workflow_manager/` - Entire old workflow manager directory
  - `README.md`
  - `__init__.py`
  - `workflow_executor.py`

### Research Documents (`archive/`)
- `DT_research.md` - Digital Twins research document

## Reason for Archiving

### Development Files
These test files were used during development and testing phases but are not needed for production use. They contain:
- LLM testing scripts
- Workflow testing utilities
- Modular structure validation
- Pre-search functionality tests

### Old Workflows
These workflow files were replaced by the new dynamic workflow executor system:
- Old workflow implementations that are no longer used
- Duplicate workflow files
- Broken or incomplete workflow versions
- Old workflow manager that was superseded

### Research Documents
- Research documents that are not part of the core application functionality

## Current Active Files

The following files remain active and are part of the current system:
- `agent_configuration.py` - New agent selection system
- `dynamic_workflow_executor.py` - New dynamic workflow executor
- `oracle_database/` - Oracle database integration
- `docker-compose.yml` - Docker Compose configuration
- `pages/8_🗄️_Database.py` - Database management page
- All other core application files

## Benefits of Archiving

1. **Cleaner Repository**: Removes clutter from the main directory
2. **Better Organization**: Groups related files together
3. **Preserved History**: Keeps old files for reference
4. **Easier Maintenance**: Focuses on current active files
5. **Reduced Confusion**: Prevents confusion between old and new implementations

## Accessing Archived Files

Archived files can still be accessed if needed:
- All files are preserved in the archive folder
- Git history maintains the full development timeline
- Files can be restored if needed for reference

This archiving approach maintains a clean, organized codebase while preserving the development history and allowing for future reference if needed.
