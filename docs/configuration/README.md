# Configuration Documentation

This directory contains detailed documentation for configuration management in the CrewAI Multi-Agent Workflow System.

## Overview

The configuration system manages application settings, environment variables, and system configuration. It provides a centralized way to configure the application behavior and ensures secure handling of sensitive information like API keys.

## Configuration Structure

```
configuration/
├── README.md                    # This overview
├── environment_setup.md         # Environment setup guide
└── security.md                  # Security configuration guide
```

## Core Components

### 1. Environment Variables
**Purpose**: Application configuration and settings
**File**: `.env`
**Key Features**:
- Secure API key management
- Application settings
- Model configuration
- Performance tuning

### 2. Configuration Manager
**Purpose**: Centralized configuration management
**File**: `config_manager/config.py`
**Key Features**:
- Environment variable loading
- Configuration validation
- Default value management
- Type conversion

### 3. Security Configuration
**Purpose**: Security settings and API key management
**Key Features**:
- API key validation
- Secure storage
- Access control
- Audit logging

## Environment Variables

### Core Configuration

```env
# Application Settings
STREAMLIT_PORT=8501
STREAMLIT_ADDRESS=localhost
STREAMLIT_THEME=light

# Model Configuration
DEFAULT_TEMPERATURE=0.7
DEFAULT_MAX_TOKENS=20000
DEFAULT_TOP_P=0.9

# Search Settings
DUCKDUCKGO_MAX_RESULTS=5
SEARCH_RETRY_ATTEMPTS=3
SEARCH_DELAY_SECONDS=1

# Memory Settings
MEMORY_DB_PATH="./memory_db"
MAX_MEMORY_RESULTS=5
MEMORY_SIMILARITY_THRESHOLD=0.7

# Performance Settings
MAX_RPM=5
MAX_EXECUTION_TIME=300
TEAM_DELAY=10
```

### Ollama Configuration

```env
# Local Ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_LOCAL_MODEL=llama3.1

# Ollama Cloud (Turbo)
OLLAMA_CLOUD_BASE_URL=https://api.ollama.ai
OLLAMA_CLOUD_MODEL=gpt-oss:20b
OLLAMA_API_KEY=your_api_key_here
```

### Database Configuration

```env
# ChromaDB Configuration
CHROMADB_PERSIST_DIRECTORY="./memory_db"
CHROMADB_COLLECTION_NAME="conversations"
CHROMADB_DISTANCE_FUNCTION="cosine"

# Embedding Configuration
EMBEDDING_MODEL="ONNXMiniLM_L6_V2"
EMBEDDING_DIMENSION=384
```

## Configuration Manager

### Basic Configuration

```python
class ConfigManager:
    def __init__(self, env_file: str = ".env"):
        self.env_file = env_file
        self.config = {}
        self.load_config()
    
    def load_config(self):
        """
        Load configuration from environment variables
        """
        # Load .env file
        load_dotenv(self.env_file)
        
        # Load configuration
        self.config = {
            # Application settings
            "streamlit_port": int(os.getenv("STREAMLIT_PORT", 8501)),
            "streamlit_address": os.getenv("STREAMLIT_ADDRESS", "localhost"),
            "streamlit_theme": os.getenv("STREAMLIT_THEME", "light"),
            
            # Model settings
            "default_temperature": float(os.getenv("DEFAULT_TEMPERATURE", 0.7)),
            "default_max_tokens": int(os.getenv("DEFAULT_MAX_TOKENS", 20000)),
            "default_top_p": float(os.getenv("DEFAULT_TOP_P", 0.9)),
            
            # Search settings
            "duckduckgo_max_results": int(os.getenv("DUCKDUCKGO_MAX_RESULTS", 5)),
            "search_retry_attempts": int(os.getenv("SEARCH_RETRY_ATTEMPTS", 3)),
            "search_delay_seconds": int(os.getenv("SEARCH_DELAY_SECONDS", 1)),
            
            # Memory settings
            "memory_db_path": os.getenv("MEMORY_DB_PATH", "./memory_db"),
            "max_memory_results": int(os.getenv("MAX_MEMORY_RESULTS", 5)),
            "memory_similarity_threshold": float(os.getenv("MEMORY_SIMILARITY_THRESHOLD", 0.7)),
            
            # Performance settings
            "max_rpm": int(os.getenv("MAX_RPM", 5)),
            "max_execution_time": int(os.getenv("MAX_EXECUTION_TIME", 300)),
            "team_delay": int(os.getenv("TEAM_DELAY", 10))
        }
```

### Ollama Configuration

```python
def get_ollama_config(self) -> Dict[str, Any]:
    """
    Get Ollama configuration
    """
    return {
        "local": {
            "base_url": os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
            "model": os.getenv("OLLAMA_LOCAL_MODEL", "llama3.1"),
            "temperature": self.config["default_temperature"],
            "max_tokens": self.config["default_max_tokens"],
            "top_p": self.config["default_top_p"]
        },
        "cloud": {
            "base_url": os.getenv("OLLAMA_CLOUD_BASE_URL", "https://api.ollama.ai"),
            "model": os.getenv("OLLAMA_CLOUD_MODEL", "gpt-oss:20b"),
            "api_key": os.getenv("OLLAMA_API_KEY"),
            "temperature": self.config["default_temperature"],
            "max_tokens": self.config["default_max_tokens"],
            "top_p": self.config["default_top_p"]
        }
    }
```

### Database Configuration

```python
def get_database_config(self) -> Dict[str, Any]:
    """
    Get database configuration
    """
    return {
        "chromadb": {
            "persist_directory": os.getenv("CHROMADB_PERSIST_DIRECTORY", "./memory_db"),
            "collection_name": os.getenv("CHROMADB_COLLECTION_NAME", "conversations"),
            "distance_function": os.getenv("CHROMADB_DISTANCE_FUNCTION", "cosine")
        },
        "embedding": {
            "model": os.getenv("EMBEDDING_MODEL", "ONNXMiniLM_L6_V2"),
            "dimension": int(os.getenv("EMBEDDING_DIMENSION", 384))
        }
    }
```

## Security Configuration

### API Key Management

```python
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
            "openai": os.getenv("OPENAI_API_KEY"),
            "anthropic": os.getenv("ANTHROPIC_API_KEY")
        }
    
    def validate_api_key(self, service: str, api_key: str) -> bool:
        """
        Validate API key for a service
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
        elif service == "anthropic":
            return api_key.startswith("sk-ant-")
        
        return True
    
    def mask_api_key(self, api_key: str) -> str:
        """
        Mask API key for display
        """
        if not api_key:
            return "Not set"
        
        if len(api_key) <= 8:
            return "***"
        
        return f"{api_key[:4]}...{api_key[-4:]}"
```

### Access Control

```python
class AccessControl:
    def __init__(self):
        self.permissions = {
            "admin": ["read", "write", "delete", "configure"],
            "user": ["read", "write"],
            "guest": ["read"]
        }
    
    def check_permission(self, user_role: str, action: str) -> bool:
        """
        Check if user has permission for action
        """
        if user_role not in self.permissions:
            return False
        
        return action in self.permissions[user_role]
    
    def get_allowed_actions(self, user_role: str) -> List[str]:
        """
        Get allowed actions for user role
        """
        return self.permissions.get(user_role, [])
```

## Configuration Validation

### Input Validation

```python
class ConfigValidator:
    def __init__(self):
        self.validators = {
            "port": self.validate_port,
            "temperature": self.validate_temperature,
            "max_tokens": self.validate_max_tokens,
            "api_key": self.validate_api_key
        }
    
    def validate_port(self, value: Any) -> bool:
        """
        Validate port number
        """
        try:
            port = int(value)
            return 1 <= port <= 65535
        except (ValueError, TypeError):
            return False
    
    def validate_temperature(self, value: Any) -> bool:
        """
        Validate temperature value
        """
        try:
            temp = float(value)
            return 0.0 <= temp <= 1.0
        except (ValueError, TypeError):
            return False
    
    def validate_max_tokens(self, value: Any) -> bool:
        """
        Validate max tokens value
        """
        try:
            tokens = int(value)
            return 1 <= tokens <= 100000
        except (ValueError, TypeError):
            return False
    
    def validate_api_key(self, value: Any) -> bool:
        """
        Validate API key format
        """
        if not value:
            return False
        
        return len(str(value)) >= 10
```

### Configuration Validation

```python
def validate_config(self) -> Dict[str, List[str]]:
    """
    Validate entire configuration
    """
    errors = {}
    
    # Validate application settings
    if not self.validate_port(self.config["streamlit_port"]):
        errors["streamlit_port"] = ["Invalid port number"]
    
    if not self.validate_temperature(self.config["default_temperature"]):
        errors["default_temperature"] = ["Temperature must be between 0.0 and 1.0"]
    
    if not self.validate_max_tokens(self.config["default_max_tokens"]):
        errors["default_max_tokens"] = ["Max tokens must be between 1 and 100000"]
    
    # Validate API keys
    ollama_config = self.get_ollama_config()
    if ollama_config["cloud"]["api_key"]:
        if not self.validate_api_key(ollama_config["cloud"]["api_key"]):
            errors["ollama_api_key"] = ["Invalid API key format"]
    
    return errors
```

## Configuration Loading

### Environment File Loading

```python
def load_environment_file(self, env_file: str = ".env"):
    """
    Load environment variables from file
    """
    if not os.path.exists(env_file):
        logger.warning(f"Environment file {env_file} not found")
        return
    
    try:
        load_dotenv(env_file)
        logger.info(f"Loaded environment file: {env_file}")
    except Exception as e:
        logger.error(f"Error loading environment file: {e}")
        raise
```

### Default Value Management

```python
def get_config_value(self, key: str, default: Any = None, required: bool = False) -> Any:
    """
    Get configuration value with validation
    """
    value = os.getenv(key, default)
    
    if required and not value:
        raise ValueError(f"Required configuration {key} not found")
    
    return value
```

## Configuration Updates

### Runtime Configuration Updates

```python
def update_config(self, updates: Dict[str, Any]):
    """
    Update configuration at runtime
    """
    for key, value in updates.items():
        if key in self.config:
            self.config[key] = value
            logger.info(f"Updated configuration: {key} = {value}")
        else:
            logger.warning(f"Unknown configuration key: {key}")
```

### Configuration Persistence

```python
def save_config(self, config_file: str = "config.json"):
    """
    Save configuration to file
    """
    try:
        with open(config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
        logger.info(f"Configuration saved to: {config_file}")
    except Exception as e:
        logger.error(f"Error saving configuration: {e}")
        raise
```

## Error Handling

### Configuration Errors

```python
class ConfigError(Exception):
    """Configuration error"""
    pass

class ValidationError(ConfigError):
    """Configuration validation error"""
    pass

class SecurityError(ConfigError):
    """Security configuration error"""
    pass

def handle_config_error(self, error: Exception):
    """
    Handle configuration errors
    """
    if isinstance(error, ValidationError):
        logger.error(f"Configuration validation error: {error}")
        return "Configuration validation failed"
    elif isinstance(error, SecurityError):
        logger.error(f"Security configuration error: {error}")
        return "Security configuration failed"
    else:
        logger.error(f"Configuration error: {error}")
        return "Configuration error occurred"
```

## Monitoring

### Configuration Monitoring

```python
class ConfigMonitor:
    def __init__(self):
        self.config_history = []
        self.change_count = 0
    
    def record_change(self, key: str, old_value: Any, new_value: Any):
        """
        Record configuration change
        """
        change = {
            "timestamp": datetime.utcnow().isoformat(),
            "key": key,
            "old_value": old_value,
            "new_value": new_value
        }
        
        self.config_history.append(change)
        self.change_count += 1
        
        logger.info(f"Configuration changed: {key} = {new_value}")
    
    def get_change_history(self) -> List[Dict[str, Any]]:
        """
        Get configuration change history
        """
        return self.config_history
```

## Best Practices

### Configuration Management

1. **Environment Variables**: Use environment variables for configuration
2. **Default Values**: Provide sensible default values
3. **Validation**: Validate all configuration values
4. **Security**: Secure handling of sensitive information
5. **Documentation**: Document all configuration options
6. **Testing**: Test configuration with different values
7. **Monitoring**: Monitor configuration changes

### Security Best Practices

1. **API Key Security**: Never commit API keys to version control
2. **Environment Files**: Use `.env` files for local development
3. **Access Control**: Implement proper access control
4. **Audit Logging**: Log configuration changes
5. **Encryption**: Encrypt sensitive configuration data
6. **Validation**: Validate all configuration inputs
7. **Backup**: Backup configuration files

## Troubleshooting

### Common Issues

1. **Missing Environment Variables**
   - Check `.env` file exists
   - Verify variable names
   - Check file permissions

2. **Invalid Configuration Values**
   - Validate input values
   - Check value ranges
   - Verify data types

3. **API Key Issues**
   - Verify API key format
   - Check API key validity
   - Ensure proper permissions

4. **Configuration Loading Errors**
   - Check file paths
   - Verify file permissions
   - Check JSON syntax

### Debugging

```python
def debug_configuration(self):
    """
    Debug configuration issues
    """
    print("Configuration Debug Information:")
    print(f"Environment file: {self.env_file}")
    print(f"Configuration keys: {list(self.config.keys())}")
    print(f"Ollama config: {self.get_ollama_config()}")
    print(f"Database config: {self.get_database_config()}")
    
    # Check environment variables
    env_vars = [
        "STREAMLIT_PORT",
        "OLLAMA_API_KEY",
        "MEMORY_DB_PATH"
    ]
    
    for var in env_vars:
        value = os.getenv(var)
        print(f"{var}: {'Set' if value else 'Not set'}")
```

## Support

For configuration issues:
1. Check the environment setup guide
2. Verify all required environment variables
3. Check file permissions and paths
4. Review error logs and messages
5. Test with minimal configuration
