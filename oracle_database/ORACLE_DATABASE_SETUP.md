# Oracle Database 23ai Setup Guide

This guide explains how to set up Oracle Database 23ai for the Web Knowledge System using Docker.

## Prerequisites

- Docker installed and running
- At least 4GB RAM available for the Oracle container
- At least 10GB free disk space

## Quick Setup

### 1. Run the Setup Script

The easiest way to set up Oracle Database 23ai is to use the provided setup script:

```bash
./setup_oracle_db.sh
```

This script will:
- Pull the Oracle Database 23ai Docker image
- Create and start the container
- Wait for the database to be ready
- Create the application user
- Display connection information

### 2. Initialize the Database Schema

After the container is running, initialize the database schema:

```bash
python init_database.py
```

This will create all necessary tables, indexes, and initial configuration data.

## Manual Setup

If you prefer to set up the database manually:

### 1. Pull the Oracle Image

```bash
docker pull container-registry.oracle.com/database/free:latest
```

### 2. Create and Start the Container

```bash
docker run -d \
  --name oracle-23ai \
  -p 1521:1521 \
  -p 5500:5500 \
  -e ORACLE_PWD=YourPassword \
  -e ORACLE_CHARACTERSET=AL32UTF8 \
  -v oracle_data:/opt/oracle/oradata \
  container-registry.oracle.com/database/free:latest
```

### 3. Wait for Database to be Ready

The database takes several minutes to initialize on first startup. You can check the status with:

```bash
docker logs oracle-23ai
```

### 4. Connect to the Database

```bash
docker exec -it oracle-23ai sqlplus sys/YourPassword@FREE as sysdba
```

### 5. Create Application User

```sql
-- Connect to PDB
ALTER SESSION SET CONTAINER=FREEPDB1;

-- Create application user
CREATE USER web_knowledge IDENTIFIED BY WebKnowledge2024!
DEFAULT TABLESPACE users
TEMPORARY TABLESPACE temp
QUOTA 500M ON users;

-- Grant privileges
GRANT CONNECT, RESOURCE TO web_knowledge;
GRANT CREATE SESSION TO web_knowledge;
GRANT CREATE TABLE TO web_knowledge;
GRANT CREATE SEQUENCE TO web_knowledge;
GRANT CREATE PROCEDURE TO web_knowledge;
GRANT CREATE TRIGGER TO web_knowledge;
GRANT CREATE VIEW TO web_knowledge;
```

## Connection Information

### Database Details
- **Host**: localhost
- **Port**: 1521
- **Service Name**: FREE (CDB) or FREEPDB1 (PDB)
- **Username**: web_knowledge
- **Password**: WebKnowledge2024!

### Default Accounts
- **SYS**: sys/YourPassword@FREE as sysdba
- **SYSTEM**: system/YourPassword@FREE
- **PDBADMIN**: pdbadmin/YourPassword@FREEPDB1

### Enterprise Manager Express
- **URL**: http://localhost:5500/em
- **Username**: sys
- **Password**: YourPassword

## Using the Database in Your Application

### Basic Connection

```python
from database_manager import get_db_manager

# Get database manager instance
db = get_db_manager()

# Save a document
doc_id = db.save_document(
    filename="example.pdf",
    file_path="/path/to/file",
    file_type="pdf",
    file_size=1024000,
    created_by="user123"
)

# Get document
document = db.get_document(doc_id)
```

### Configuration Management

```python
# Get configuration value
max_file_size = db.get_config("max_file_size")

# Set configuration value
db.set_config("new_setting", "value", "STRING", "Description")
```

### Agent Memory

```python
# Save agent memory
db.save_memory("research_agent", "context", "last_topic", "AI Research")

# Retrieve agent memory
memory = db.get_memory("research_agent", "context", "last_topic")
```

## Database Schema

The system creates the following main tables:

- **documents**: Document metadata and file information
- **document_chunks**: Text chunks for vector processing
- **agent_tasks**: Agent task management
- **workflow_executions**: Workflow execution tracking
- **agent_memory**: Agent memory storage
- **research_results**: Research findings
- **user_sessions**: User session management
- **system_config**: System configuration

## Useful Commands

### Container Management
```bash
# Check container status
docker ps

# View container logs
docker logs oracle-23ai

# Stop container
docker stop oracle-23ai

# Start container
docker start oracle-23ai

# Remove container
docker rm oracle-23ai
```

### Database Connection
```bash
# Connect as SYS
docker exec -it oracle-23ai sqlplus sys/YourPassword@FREE as sysdba

# Connect as application user
docker exec -it oracle-23ai sqlplus web_knowledge/WebKnowledge2024!@FREEPDB1

# Connect to PDB
docker exec -it oracle-23ai sqlplus pdbadmin/YourPassword@FREEPDB1
```

### Database Operations
```sql
-- Check database status
SELECT status FROM v$instance;

-- List all tables
SELECT table_name FROM user_tables;

-- Check tablespace usage
SELECT tablespace_name, bytes/1024/1024 as size_mb 
FROM user_segments 
GROUP BY tablespace_name;
```

## Troubleshooting

### Container Won't Start
- Ensure Docker has enough memory (4GB+)
- Check if ports 1521 and 5500 are available
- Verify Docker is running

### Database Connection Issues
- Wait for database initialization to complete (5-10 minutes)
- Check container logs: `docker logs oracle-23ai`
- Verify password is correct
- Ensure container is running: `docker ps`

### Performance Issues
- Increase Docker memory allocation
- Monitor disk space usage
- Check Oracle alert logs in the container

### Reset Database
```bash
# Stop and remove container
docker stop oracle-23ai
docker rm oracle-23ai

# Remove volume (WARNING: This deletes all data)
docker volume rm oracle_data

# Run setup script again
./setup_oracle_db.sh
```

## Security Considerations

- Change default passwords in production
- Use environment variables for sensitive configuration
- Consider using Oracle Wallet for password management
- Enable Oracle Database Vault for additional security
- Regularly update the Oracle container image

## Production Deployment

For production deployment:

1. Use environment variables for passwords
2. Set up proper backup procedures
3. Configure Oracle Enterprise Manager
4. Implement monitoring and alerting
5. Use Oracle RAC for high availability
6. Enable Oracle Data Guard for disaster recovery

## Support

For issues related to:
- Oracle Database: Check Oracle documentation
- Docker: Check Docker documentation
- Application integration: Check the application logs and database_manager.py
