# Web Knowledge System - Local Development Setup

This guide explains how to run the Web Knowledge System application locally while using the Oracle database in Docker.

## Architecture

- **Oracle Database**: Running in Docker container (oracle-23ai)
- **Web Application**: Running locally on your machine
- **pgAdmin**: Running in Docker container for database management

## Prerequisites

- Python 3.11+ installed locally
- Docker and Docker Compose installed
- Virtual environment set up

## Quick Start

### 1. Start the Database Services

```bash
# Start Oracle database and pgAdmin
docker-compose up -d

# Check if services are running
docker-compose ps
```

### 2. Start the Web Application

```bash
# Option 1: Use the startup script (recommended)
./start_app.sh

# Option 2: Manual startup
source venv/bin/activate
streamlit run streamlit_app_multi_page.py --server.port 8501 --server.address localhost
```

### 3. Access the Application

- **Web Application**: http://localhost:8501
- **Oracle Enterprise Manager**: http://localhost:5500/em
- **pgAdmin**: http://localhost:8080

## Database Configuration

The application connects to the Oracle database using the following configuration:

- **Host**: localhost
- **Port**: 1521
- **Service Name**: FREEPDB1
- **Username**: web_knowledge
- **Password**: WebKnowledge2024!

## Database Management

### Oracle Enterprise Manager Express
- URL: http://localhost:5500/em
- Username: sys
- Password: WebKnowledge2024!

### Command Line Access
```bash
# Connect to Oracle database
docker exec -it oracle-23ai sqlplus sys/WebKnowledge2024!@FREEPDB1 as sysdba

# Connect as application user
docker exec -it oracle-23ai sqlplus web_knowledge/WebKnowledge2024!@FREEPDB1
```

### pgAdmin (PostgreSQL tool - limited Oracle support)
- URL: http://localhost:8080
- Email: admin@webknowledge.com
- Password: admin123

**Note**: pgAdmin is designed for PostgreSQL and has limited Oracle support. Use Oracle Enterprise Manager or SQL Developer for full Oracle database management.

## Development Workflow

1. **Start Database**: `docker-compose up -d`
2. **Start App**: `./start_app.sh`
3. **Make Changes**: Edit code locally
4. **Test Changes**: Refresh browser
5. **Stop App**: Ctrl+C in terminal
6. **Stop Database**: `docker-compose down`

## Troubleshooting

### Database Connection Issues
```bash
# Test database connection
source venv/bin/activate
python -c "
from oracle_database.database_config import config
import oracledb
conn_config = config.get_app_connection_config()
dsn = f'{conn_config[\"host\"]}:{conn_config[\"port\"]}/{conn_config[\"service_name\"]}'
conn = oracledb.connect(user=conn_config['username'], password=conn_config['password'], dsn=dsn)
print('✅ Database connection successful!')
conn.close()
"
```

### Port Conflicts
If port 8501 is already in use:
```bash
# Find process using port 8501
lsof -i :8501

# Kill the process
kill -9 <PID>

# Or use a different port
streamlit run streamlit_app_multi_page.py --server.port 8502 --server.address localhost
```

### Database Initialization
If you need to reinitialize the database:
```bash
source venv/bin/activate
python oracle_database/init_database.py
```

## Environment Variables

You can override database settings using environment variables:

```bash
export ORACLE_DB_HOST=localhost
export ORACLE_DB_PORT=1521
export ORACLE_DB_SERVICE_NAME=FREEPDB1
export ORACLE_DB_USER=web_knowledge
export ORACLE_DB_PASSWORD=WebKnowledge2024!
```

## File Structure

```
web_knowledge/
├── oracle_database/          # Database configuration and scripts
│   ├── database_config.py    # Database connection settings
│   ├── database_manager.py   # Database operations
│   ├── init_database.py      # Database initialization
│   └── ...
├── streamlit_app_multi_page.py  # Main application
├── start_app.sh             # Startup script
├── docker-compose.yml       # Docker services (database only)
└── ...
```

## Benefits of This Setup

1. **Faster Development**: No need to rebuild Docker images for code changes
2. **Better Debugging**: Direct access to Python debugger and logs
3. **Hot Reload**: Streamlit automatically reloads on code changes
4. **Resource Efficient**: Only database runs in Docker
5. **Easy Testing**: Can run tests locally while using real database
