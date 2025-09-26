#!/bin/bash

# Web Knowledge System - Local Development Startup Script
# This script starts the Streamlit application locally while connecting to the Docker Oracle database

echo "🚀 Starting Web Knowledge System..."
echo "=================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run: python3 -m venv venv"
    exit 1
fi

# Activate virtual environment
echo "📦 Activating virtual environment..."
source venv/bin/activate

# Check if Oracle database is running
echo "🔍 Checking Oracle database status..."
if ! docker-compose ps oracle-db | grep -q "Up.*healthy"; then
    echo "⚠️  Oracle database is not running or not healthy."
    echo "   Starting Oracle database..."
    docker-compose up -d oracle-db
    echo "   Waiting for database to be ready..."
    sleep 30
fi

# Test database connection
echo "🔗 Testing database connection..."
python -c "
from oracle_database.database_config import config
import oracledb
try:
    conn_config = config.get_app_connection_config()
    dsn = f'{conn_config[\"host\"]}:{conn_config[\"port\"]}/{conn_config[\"service_name\"]}'
    conn = oracledb.connect(
        user=conn_config['username'],
        password=conn_config['password'],
        dsn=dsn
    )
    print('✅ Database connection successful!')
    conn.close()
except Exception as e:
    print('❌ Database connection failed:', e)
    exit(1)
"

if [ $? -ne 0 ]; then
    echo "❌ Database connection failed. Please check your Oracle database setup."
    exit 1
fi

# Start Streamlit application
echo "🌐 Starting Streamlit application..."
echo "   Application will be available at: http://localhost:8501"
echo "   Press Ctrl+C to stop the application"
echo ""

streamlit run streamlit_app_multi_page.py --server.port 8501 --server.address localhost
