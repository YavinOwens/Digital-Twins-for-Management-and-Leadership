# Oracle Database Module

This module contains all Oracle Database 23ai related files for the Web Knowledge System.

## Files Overview

- **`database_config.py`** - Configuration management for Oracle Database 23ai
- **`database_manager.py`** - High-level database operations and connection utilities
- **`init_database.py`** - Database schema initialization script
- **`setup_oracle_db.sh`** - Automated Docker setup script for Oracle container
- **`install_oracle_deps.sh`** - Dependency installation script
- **`ORACLE_DATABASE_SETUP.md`** - Comprehensive setup and usage documentation

## Quick Start

1. **Install Dependencies:**
   ```bash
   cd oracle_database
   ./install_oracle_deps.sh
   ```

2. **Set Up Database:**
   ```bash
   ./setup_oracle_db.sh
   ```

3. **Initialize Schema:**
   ```bash
   python init_database.py
   ```

4. **Use in Your Application:**
   ```python
   from oracle_database.database_manager import get_db_manager
   db = get_db_manager()
   ```

## Database Connection Details

- **Host**: localhost
- **Port**: 1521
- **Service**: FREE (CDB) / FREEPDB1 (PDB)
- **User**: web_knowledge
- **Password**: WebKnowledge2024!

## Features

- ✅ Automated Docker container setup
- ✅ Complete database schema for Web Knowledge System
- ✅ Connection pooling and management
- ✅ Document processing support
- ✅ Agent memory storage
- ✅ Task and workflow tracking
- ✅ Configuration management
- ✅ Production-ready features

For detailed setup instructions, see `ORACLE_DATABASE_SETUP.md`.
