"""
Database Configuration for Web Knowledge System
Oracle Database 23ai Configuration
"""

import os
from typing import Dict, Any

class DatabaseConfig:
    """Configuration class for Oracle Database 23ai"""
    
    # Docker container settings
    CONTAINER_NAME = "oracle-23ai"
    IMAGE_NAME = "container-registry.oracle.com/database/free:latest"
    
    # Port mappings
    DB_PORT = 1521
    EM_PORT = 5500
    
    # Database connection settings
    DB_HOST = "localhost"
    DB_SERVICE_NAME = "FREEPDB1"
    DB_PDB_NAME = "FREEPDB1"
    
    # Default credentials (should be overridden in production)
    DEFAULT_SYS_PASSWORD = "WebKnowledge2024!"
    DEFAULT_SYSTEM_PASSWORD = "WebKnowledge2024!"
    
    # Application database settings
    APP_USERNAME = "web_knowledge"
    APP_PASSWORD = "WebKnowledge2024!"
    APP_TABLESPACE = "USERS"
    APP_TEMP_TABLESPACE = "TEMP"
    APP_QUOTA = "500M"
    
    # Character set
    CHARACTER_SET = "AL32UTF8"
    
    # Volume settings
    VOLUME_NAME = "oracle_data"
    VOLUME_PATH = "/opt/oracle/oradata"
    
    @classmethod
    def get_docker_run_command(cls, password: str = None) -> str:
        """Generate the Docker run command for Oracle 23ai"""
        pwd = password or cls.DEFAULT_SYS_PASSWORD
        
        return f"""docker run -d \\
  --name {cls.CONTAINER_NAME} \\
  -p {cls.DB_PORT}:{cls.DB_PORT} \\
  -p {cls.EM_PORT}:{cls.EM_PORT} \\
  -e ORACLE_PWD={pwd} \\
  -e ORACLE_CHARACTERSET={cls.CHARACTER_SET} \\
  -v {cls.VOLUME_NAME}:{cls.VOLUME_PATH} \\
  {cls.IMAGE_NAME}"""
    
    @classmethod
    def get_connection_string(cls, username: str, password: str, service: str = None) -> str:
        """Generate Oracle connection string"""
        service_name = service or cls.DB_SERVICE_NAME
        return f"{username}/{password}@{cls.DB_HOST}:{cls.DB_PORT}/{service_name}"
    
    @classmethod
    def get_sqlplus_command(cls, username: str, password: str, service: str = None) -> str:
        """Generate SQL*Plus connection command"""
        conn_str = cls.get_connection_string(username, password, service)
        return f"docker exec -it {cls.CONTAINER_NAME} sqlplus {conn_str}"
    
    @classmethod
    def get_app_connection_config(cls) -> Dict[str, Any]:
        """Get application database connection configuration"""
        # Use environment variables if available (for Docker Compose)
        host = os.getenv("ORACLE_DB_HOST", cls.DB_HOST)
        port = int(os.getenv("ORACLE_DB_PORT", cls.DB_PORT))
        service_name = os.getenv("ORACLE_DB_SERVICE_NAME", cls.DB_SERVICE_NAME)
        username = os.getenv("ORACLE_DB_USER", cls.APP_USERNAME)
        password = os.getenv("ORACLE_DB_PASSWORD", cls.APP_PASSWORD)
        
        return {
            "host": host,
            "port": port,
            "service_name": service_name,
            "username": username,
            "password": password,
            "dsn": f"{host}:{port}/{service_name}"
        }
    
    @classmethod
    def get_pdb_connection_config(cls) -> Dict[str, Any]:
        """Get PDB connection configuration"""
        return {
            "host": cls.DB_HOST,
            "port": cls.DB_PORT,
            "service_name": cls.DB_PDB_NAME,
            "username": cls.APP_USERNAME,
            "password": cls.APP_PASSWORD,
            "dsn": f"{cls.DB_HOST}:{cls.DB_PORT}/{cls.DB_PDB_NAME}"
        }

# Environment-specific configurations
class DevelopmentConfig(DatabaseConfig):
    """Development environment configuration"""
    DEFAULT_SYS_PASSWORD = "DevPassword123!"
    APP_PASSWORD = "DevAppPassword123!"

class ProductionConfig(DatabaseConfig):
    """Production environment configuration"""
    # These should be set via environment variables in production
    DEFAULT_SYS_PASSWORD = os.getenv("ORACLE_SYS_PASSWORD", "ProdPassword123!")
    APP_PASSWORD = os.getenv("ORACLE_APP_PASSWORD", "ProdAppPassword123!")
    
    @classmethod
    def get_app_connection_config(cls) -> Dict[str, Any]:
        """Get production connection config with environment variables"""
        config = super().get_app_connection_config()
        config.update({
            "password": os.getenv("ORACLE_APP_PASSWORD", cls.APP_PASSWORD),
            "host": os.getenv("ORACLE_HOST", cls.DB_HOST),
            "port": int(os.getenv("ORACLE_PORT", cls.DB_PORT))
        })
        return config

# Default configuration
config = DatabaseConfig()
