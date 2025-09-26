# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libaio-dev \
    wget \
    unzip \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Oracle Instant Client (simplified approach)
RUN mkdir -p /opt/oracle && \
    echo "Using oracledb thin mode - no Oracle Instant Client required"

# Set Oracle environment variables
ENV ORACLE_HOME=/opt/oracle/instantclient
ENV LD_LIBRARY_PATH=$ORACLE_HOME:$LD_LIBRARY_PATH
ENV PATH=$ORACLE_HOME:$PATH

# Copy requirements first for better caching
COPY core_requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r core_requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p uploads team_outputs memory_db

# Set permissions
RUN chmod +x oracle_database/*.sh

# Create healthcheck script for Oracle
RUN mkdir -p oracle_database/init_scripts
RUN echo "SELECT 1 FROM DUAL;" > oracle_database/init_scripts/healthcheck.sql

# Expose Streamlit port
EXPOSE 8501

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Default command
CMD ["streamlit", "run", "streamlit_app_multi_page.py", "--server.port=8501", "--server.address=0.0.0.0"]
