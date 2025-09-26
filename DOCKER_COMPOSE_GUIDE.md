# Docker Compose Setup for Web Knowledge System with Oracle Database 23ai

This guide explains how to run the Web Knowledge System with Oracle Database 23ai using Docker Compose.

## Prerequisites

- Docker installed and running
- Docker Compose installed
- At least 8GB RAM available
- At least 20GB free disk space

## Quick Start

### 1. Clone and Setup

```bash
git clone <your-repo>
cd web_knowledge
```

### 2. Configure Environment (Optional)

```bash
cp env.example .env
# Edit .env file with your preferred settings
```

### 3. Start Services

```bash
# Start all services
docker-compose up -d

# Or start with Oracle Enterprise Manager
docker-compose --profile em up -d
```

### 4. Access the Application

- **Web Knowledge System**: http://localhost:8501
- **pgAdmin**: http://localhost:8080 (Note: pgAdmin is for PostgreSQL, not Oracle)
- **Oracle Enterprise Manager**: http://localhost:5500/em (if enabled)

## Services Overview

### Oracle Database 23ai (`oracle-db`)
- **Image**: `container-registry.oracle.com/database/free:latest`
- **Ports**: 1521 (database), 5500 (EM Express)
- **Volume**: `oracle_data` for persistent storage
- **Health Check**: Built-in Oracle health monitoring

### Web Knowledge Application (`web-knowledge-app`)
- **Build**: Custom Dockerfile with Oracle Instant Client
- **Port**: 8501 (Streamlit)
- **Dependencies**: Waits for Oracle database to be healthy
- **Auto-initialization**: Runs database schema setup on startup

### pgAdmin (`pgadmin`) - Database Management
- **Image**: `dpage/pgadmin4:latest`
- **Port**: 8080
- **Purpose**: Database management interface
- **Note**: pgAdmin is designed for PostgreSQL, not Oracle databases

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `ORACLE_PASSWORD` | `WebKnowledge2024!` | Oracle database password |
| `STREAMLIT_SERVER_PORT` | `8501` | Streamlit server port |
| `ORACLE_HOST` | `oracle-db` | Database host (internal) |
| `ORACLE_PORT` | `1521` | Database port |
| `ORACLE_SERVICE_NAME` | `FREE` | Oracle service name |
| `PGADMIN_EMAIL` | `admin@webknowledge.com` | pgAdmin login email |
| `PGADMIN_PASSWORD` | `admin123` | pgAdmin login password |

## Useful Commands

### Start Services
```bash
# Start all services
docker-compose up -d

# Start with logs
docker-compose up

# Start with Oracle EM
docker-compose --profile em up -d
```

### Stop Services
```bash
# Stop all services
docker-compose down

# Stop and remove volumes (WARNING: deletes all data)
docker-compose down -v
```

### View Logs
```bash
# All services
docker-compose logs

# Specific service
docker-compose logs oracle-db
docker-compose logs web-knowledge-app
```

### Database Operations
```bash
# Connect to Oracle database
docker-compose exec oracle-db sqlplus sys/WebKnowledge2024!@FREE as sysdba

# Connect as application user
docker-compose exec oracle-db sqlplus web_knowledge/WebKnowledge2024!@FREEPDB1

# Run database initialization manually
docker-compose exec web-knowledge-app python oracle_database/init_database.py
```

### Application Operations
```bash
# Access application shell
docker-compose exec web-knowledge-app bash

# Restart application only
docker-compose restart web-knowledge-app

# Rebuild application
docker-compose build web-knowledge-app
docker-compose up -d web-knowledge-app
```

## Troubleshooting

### Database Connection Issues
```bash
# Check database health
docker-compose ps
docker-compose logs oracle-db

# Test database connection
docker-compose exec oracle-db sqlplus sys/WebKnowledge2024!@FREE as sysdba
```

### Application Issues
```bash
# Check application logs
docker-compose logs web-knowledge-app

# Check application health
curl http://localhost:8501/_stcore/health
```

### Performance Issues
- Ensure Docker has at least 8GB RAM allocated
- Monitor disk space usage
- Check Oracle alert logs: `docker-compose exec oracle-db tail -f /opt/oracle/diag/rdbms/free/FREE/trace/alert_FREE.log`

### Reset Everything
```bash
# Stop and remove everything including data
docker-compose down -v
docker system prune -a

# Start fresh
docker-compose up -d
```

## Production Considerations

### Security
- Change default passwords in `.env` file
- Use Docker secrets for sensitive data
- Enable Oracle Database Vault
- Configure firewall rules

### Monitoring
- Set up monitoring for Oracle database
- Monitor application health endpoints
- Configure log aggregation
- Set up alerting

### Backup
- Regular Oracle database backups
- Volume snapshots
- Application data backups

### Scaling
- Use Oracle RAC for high availability
- Load balancer for application
- Database connection pooling
- Caching strategies

## Development

### Local Development
```bash
# Run only Oracle database
docker-compose up -d oracle-db

# Run application locally
python streamlit_app_multi_page.py
```

### Debugging
```bash
# Access application container
docker-compose exec web-knowledge-app bash

# Access Oracle container
docker-compose exec oracle-db bash

# View Oracle logs
docker-compose exec oracle-db tail -f /opt/oracle/diag/rdbms/free/FREE/trace/alert_FREE.log
```

## Support

For issues:
1. Check service logs: `docker-compose logs <service-name>`
2. Verify service health: `docker-compose ps`
3. Test database connectivity
4. Check resource usage
5. Review Oracle documentation
