# Deployment Documentation

This directory contains detailed documentation for deploying the CrewAI Multi-Agent Workflow System.

## Overview

The deployment documentation covers different deployment scenarios, from local development to production cloud deployment. It includes setup guides, configuration instructions, and monitoring recommendations.

## Deployment Structure

```
deployment/
├── README.md                    # This overview
├── local_deployment.md          # Local deployment guide
├── cloud_deployment.md          # Cloud deployment guide
└── monitoring.md                # Monitoring and observability guide
```

## Deployment Types

### 1. Local Deployment
**Purpose**: Development and testing
**Requirements**: Local machine with Python and Ollama
**Key Features**:
- Local Ollama server
- Local ChromaDB storage
- Development-friendly configuration
- Easy debugging and testing

### 2. Cloud Deployment
**Purpose**: Production deployment
**Requirements**: Cloud infrastructure and Ollama Cloud API
**Key Features**:
- Ollama Cloud integration
- Scalable infrastructure
- Production-ready configuration
- Monitoring and logging

### 3. Hybrid Deployment
**Purpose**: Mixed local and cloud resources
**Requirements**: Local Ollama + Ollama Cloud API
**Key Features**:
- Local Ollama for development
- Ollama Cloud for production
- Flexible configuration
- Cost optimization

## Local Deployment

### Prerequisites

```bash
# System Requirements
- Python 3.8+
- 8GB+ RAM (for llama3.1 model)
- 10GB+ disk space
- Internet connection

# Required Software
- Python 3.8+
- pip (Python package manager)
- Ollama (local LLM server)
- Git (for cloning repository)
```

### Installation Steps

```bash
# 1. Clone Repository
git clone <repository_url>
cd web_knowledge

# 2. Create Virtual Environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install Dependencies
pip install -r local_requirements.txt

# 4. Install Ollama
# macOS
brew install ollama

# Linux
curl -fsSL https://ollama.ai/install.sh | sh

# Windows
# Download from https://ollama.ai/download

# 5. Start Ollama Server
ollama serve

# 6. Pull Required Models
ollama pull llama3.1

# 7. Configure Environment
cp .env.example .env
# Edit .env with your configuration

# 8. Run Application
streamlit run streamlit_app.py
```

### Configuration

```env
# Local Configuration
STREAMLIT_PORT=8501
STREAMLIT_ADDRESS=localhost
STREAMLIT_THEME=light

# Local Ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_LOCAL_MODEL=llama3.1

# Memory Database
MEMORY_DB_PATH=./memory_db
MAX_MEMORY_RESULTS=5

# Performance
MAX_RPM=5
MAX_EXECUTION_TIME=300
TEAM_DELAY=10
```

### Verification

```bash
# Check Ollama Status
ollama list

# Test Ollama API
curl http://localhost:11434/api/tags

# Check Application
curl http://localhost:8501

# Verify Dependencies
python -c "import streamlit, crewai, chromadb; print('All dependencies installed')"
```

## Cloud Deployment

### Prerequisites

```bash
# Cloud Requirements
- Cloud provider account (AWS, GCP, Azure)
- Ollama Cloud API key
- Domain name (optional)
- SSL certificate (for production)

# Infrastructure Requirements
- 4+ CPU cores
- 16GB+ RAM
- 50GB+ disk space
- Load balancer (for production)
```

### AWS Deployment

```bash
# 1. Create EC2 Instance
aws ec2 run-instances \
  --image-id ami-0c02fb55956c7d316 \
  --instance-type t3.large \
  --key-name your-key-pair \
  --security-group-ids sg-12345678 \
  --subnet-id subnet-12345678

# 2. Install Dependencies
sudo apt update
sudo apt install python3-pip git

# 3. Clone and Setup
git clone <repository_url>
cd web_knowledge
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 4. Configure Environment
cp .env.example .env
# Edit .env with Ollama Cloud configuration

# 5. Install Streamlit
pip install streamlit

# 6. Run Application
streamlit run streamlit_app.py --server.port 8501 --server.address 0.0.0.0
```

### Docker Deployment

```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl -fsSL https://ollama.ai/install.sh | sh

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8501

# Start application
CMD ["streamlit", "run", "streamlit_app.py", "--server.port", "8501", "--server.address", "0.0.0.0"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  web_knowledge:
    build: .
    ports:
      - "8501:8501"
    environment:
      - OLLAMA_API_KEY=${OLLAMA_API_KEY}
      - MEMORY_DB_PATH=/app/memory_db
    volumes:
      - ./memory_db:/app/memory_db
    restart: unless-stopped
```

### Kubernetes Deployment

```yaml
# k8s-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-knowledge
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web-knowledge
  template:
    metadata:
      labels:
        app: web-knowledge
    spec:
      containers:
      - name: web-knowledge
        image: web-knowledge:latest
        ports:
        - containerPort: 8501
        env:
        - name: OLLAMA_API_KEY
          valueFrom:
            secretKeyRef:
              name: ollama-secret
              key: api-key
        volumeMounts:
        - name: memory-db
          mountPath: /app/memory_db
      volumes:
      - name: memory-db
        persistentVolumeClaim:
          claimName: memory-db-pvc
---
apiVersion: v1
kind: Service
metadata:
  name: web-knowledge-service
spec:
  selector:
    app: web-knowledge
  ports:
  - port: 80
    targetPort: 8501
  type: LoadBalancer
```

## Monitoring

### Application Monitoring

```python
# monitoring.py
import logging
import time
from datetime import datetime
from typing import Dict, Any

class ApplicationMonitor:
    def __init__(self):
        self.metrics = {
            "requests": 0,
            "errors": 0,
            "response_times": [],
            "memory_usage": [],
            "cpu_usage": []
        }
        self.start_time = time.time()
    
    def record_request(self, response_time: float, success: bool = True):
        """
        Record request metrics
        """
        self.metrics["requests"] += 1
        self.metrics["response_times"].append(response_time)
        
        if not success:
            self.metrics["errors"] += 1
    
    def get_metrics(self) -> Dict[str, Any]:
        """
        Get application metrics
        """
        uptime = time.time() - self.start_time
        avg_response_time = sum(self.metrics["response_times"]) / max(len(self.metrics["response_times"]), 1)
        error_rate = self.metrics["errors"] / max(self.metrics["requests"], 1)
        
        return {
            "uptime": uptime,
            "requests": self.metrics["requests"],
            "errors": self.metrics["errors"],
            "error_rate": error_rate,
            "avg_response_time": avg_response_time,
            "timestamp": datetime.utcnow().isoformat()
        }
```

### Health Checks

```python
# health_check.py
import requests
import psutil
import time
from typing import Dict, Any

class HealthChecker:
    def __init__(self):
        self.checks = {
            "ollama": self.check_ollama,
            "memory": self.check_memory,
            "disk": self.check_disk,
            "cpu": self.check_cpu
        }
    
    def check_ollama(self) -> Dict[str, Any]:
        """
        Check Ollama service health
        """
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=5)
            return {
                "status": "healthy" if response.status_code == 200 else "unhealthy",
                "response_time": response.elapsed.total_seconds(),
                "status_code": response.status_code
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e)
            }
    
    def check_memory(self) -> Dict[str, Any]:
        """
        Check memory usage
        """
        memory = psutil.virtual_memory()
        return {
            "status": "healthy" if memory.percent < 90 else "warning",
            "usage_percent": memory.percent,
            "available_gb": memory.available / (1024**3)
        }
    
    def check_disk(self) -> Dict[str, Any]:
        """
        Check disk usage
        """
        disk = psutil.disk_usage('/')
        return {
            "status": "healthy" if disk.percent < 90 else "warning",
            "usage_percent": disk.percent,
            "free_gb": disk.free / (1024**3)
        }
    
    def check_cpu(self) -> Dict[str, Any]:
        """
        Check CPU usage
        """
        cpu_percent = psutil.cpu_percent(interval=1)
        return {
            "status": "healthy" if cpu_percent < 80 else "warning",
            "usage_percent": cpu_percent
        }
    
    def run_all_checks(self) -> Dict[str, Any]:
        """
        Run all health checks
        """
        results = {}
        for check_name, check_func in self.checks.items():
            results[check_name] = check_func()
        
        return results
```

### Logging Configuration

```python
# logging_config.py
import logging
import logging.handlers
from datetime import datetime
import os

def setup_logging(log_level: str = "INFO", log_file: str = "app.log"):
    """
    Setup application logging
    """
    # Create logs directory
    os.makedirs("logs", exist_ok=True)
    
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(f"logs/{log_file}"),
            logging.StreamHandler()
        ]
    )
    
    # Rotating file handler
    file_handler = logging.handlers.RotatingFileHandler(
        f"logs/{log_file}",
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    
    # Add handler to root logger
    logging.getLogger().addHandler(file_handler)
    
    return logging.getLogger(__name__)
```

## Performance Optimization

### Caching

```python
# caching.py
import redis
import json
from typing import Any, Optional
from datetime import timedelta

class CacheManager:
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        self.redis_client = redis.from_url(redis_url)
        self.default_ttl = 3600  # 1 hour
    
    def get(self, key: str) -> Optional[Any]:
        """
        Get value from cache
        """
        try:
            value = self.redis_client.get(key)
            return json.loads(value) if value else None
        except Exception as e:
            logging.error(f"Cache get error: {e}")
            return None
    
    def set(self, key: str, value: Any, ttl: int = None) -> bool:
        """
        Set value in cache
        """
        try:
            ttl = ttl or self.default_ttl
            self.redis_client.setex(key, ttl, json.dumps(value))
            return True
        except Exception as e:
            logging.error(f"Cache set error: {e}")
            return False
    
    def delete(self, key: str) -> bool:
        """
        Delete value from cache
        """
        try:
            self.redis_client.delete(key)
            return True
        except Exception as e:
            logging.error(f"Cache delete error: {e}")
            return False
```

### Load Balancing

```nginx
# nginx.conf
upstream web_knowledge {
    server 127.0.0.1:8501;
    server 127.0.0.1:8502;
    server 127.0.0.1:8503;
}

server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://web_knowledge;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Security

### SSL/TLS Configuration

```nginx
# ssl.conf
server {
    listen 443 ssl http2;
    server_name your-domain.com;
    
    ssl_certificate /path/to/certificate.crt;
    ssl_certificate_key /path/to/private.key;
    
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;
    ssl_prefer_server_ciphers off;
    
    location / {
        proxy_pass http://web_knowledge;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### API Key Security

```python
# security.py
import os
import hashlib
from typing import Dict, Any

class SecurityManager:
    def __init__(self):
        self.api_keys = {}
        self.load_api_keys()
    
    def load_api_keys(self):
        """
        Load API keys from environment variables
        """
        self.api_keys = {
            "ollama_cloud": os.getenv("OLLAMA_API_KEY"),
            "openai": os.getenv("OPENAI_API_KEY")
        }
    
    def validate_api_key(self, service: str, api_key: str) -> bool:
        """
        Validate API key
        """
        if not api_key:
            return False
        
        # Basic validation
        if len(api_key) < 10:
            return False
        
        # Service-specific validation
        if service == "ollama_cloud":
            return api_key.startswith("ollama-")
        elif service == "openai":
            return api_key.startswith("sk-")
        
        return True
    
    def mask_api_key(self, api_key: str) -> str:
        """
        Mask API key for display
        """
        if not api_key:
            return "Not set"
        
        return f"{api_key[:4]}...{api_key[-4:]}"
```

## Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Find process using port
   lsof -i :8501
   
   # Kill process
   kill -9 <PID>
   ```

2. **Ollama Not Starting**
   ```bash
   # Check Ollama status
   ollama list
   
   # Restart Ollama
   ollama serve
   ```

3. **Memory Issues**
   ```bash
   # Check memory usage
   free -h
   
   # Check process memory
   ps aux | grep streamlit
   ```

4. **Permission Issues**
   ```bash
   # Fix file permissions
   chmod -R 755 /path/to/app
   chown -R user:user /path/to/app
   ```

### Debugging

```python
# debug.py
import logging
import traceback
from typing import Any

def debug_application():
    """
    Debug application issues
    """
    print("Application Debug Information:")
    print(f"Python version: {sys.version}")
    print(f"Streamlit version: {streamlit.__version__}")
    print(f"CrewAI version: {crewai.__version__}")
    print(f"ChromaDB version: {chromadb.__version__}")
    
    # Check environment variables
    env_vars = [
        "OLLAMA_API_KEY",
        "MEMORY_DB_PATH",
        "STREAMLIT_PORT"
    ]
    
    for var in env_vars:
        value = os.getenv(var)
        print(f"{var}: {'Set' if value else 'Not set'}")
    
    # Check file permissions
    paths = ["./memory_db", "./team_outputs", "./logs"]
    for path in paths:
        if os.path.exists(path):
            print(f"{path}: Exists, Permissions: {oct(os.stat(path).st_mode)[-3:]}")
        else:
            print(f"{path}: Does not exist")
```

## Best Practices

### Deployment Best Practices

1. **Environment Separation**: Use different configurations for dev/staging/prod
2. **Security**: Secure API keys and sensitive data
3. **Monitoring**: Implement comprehensive monitoring
4. **Backup**: Regular backup of data and configuration
5. **Testing**: Test deployment in staging environment
6. **Documentation**: Keep deployment documentation up to date
7. **Automation**: Use CI/CD for automated deployment

### Performance Best Practices

1. **Caching**: Implement caching for frequently accessed data
2. **Load Balancing**: Use load balancing for high availability
3. **Resource Management**: Monitor and optimize resource usage
4. **Database Optimization**: Optimize database queries and indexes
5. **CDN**: Use CDN for static assets
6. **Compression**: Enable compression for responses
7. **Monitoring**: Monitor performance metrics

## Support

For deployment issues:
1. Check the deployment logs
2. Verify all prerequisites are met
3. Check configuration and environment variables
4. Review error messages and stack traces
5. Test with minimal configuration
6. Check system resources and permissions
