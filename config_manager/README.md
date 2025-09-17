# Config Manager Module

This module handles application configuration, environment setup, and logging configuration for the CrewAI multi-agent workflow system. It provides centralized configuration management and environment variable handling.

## Structure

```
config_manager/
├── __init__.py                    # Module initialization
└── app_config.py                  # Application configuration and setup
```

## Key Components

### Configuration Management
- **Environment Variables**: Secure handling of API keys and settings
- **Streamlit Configuration**: Page setup and UI configuration
- **Logging Setup**: Centralized logging configuration
- **Default Values**: Fallback configuration values

### Environment Setup
- **API Key Management**: Secure loading of API keys
- **Model Configuration**: LLM model settings and parameters
- **Database Configuration**: Memory database settings
- **Feature Flags**: Enable/disable application features

## Pseudocode Examples

### Streamlit Configuration
```python
def configure_streamlit():
    """
    Pseudocode for Streamlit page configuration
    """
    # 1. Set page configuration
    st.set_page_config(
        page_title="CrewAI Multi-Agent Workflow",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # 2. Configure custom CSS
    st.markdown("""
        <style>
        .main-header {
            font-size: 2.5rem;
            color: #1f77b4;
            text-align: center;
            margin-bottom: 2rem;
        }
        .metric-card {
            background-color: #f0f2f6;
            padding: 1rem;
            border-radius: 0.5rem;
            margin: 0.5rem 0;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # 3. Set session state defaults
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []
    
    if 'workflow_results' not in st.session_state:
        st.session_state.workflow_results = {}
```

### Environment Variable Loading
```python
def load_environment():
    """
    Pseudocode for loading environment variables
    """
    # 1. Load .env file if it exists
    env_file = Path('.env')
    if env_file.exists():
        load_dotenv(env_file)
    
    # 2. Define configuration schema
    config = {
        'ollama_api_key': os.getenv('OLLAMA_API_KEY'),
        'ollama_base_url': os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434'),
        'ollama_cloud_url': os.getenv('OLLAMA_CLOUD_URL', 'https://ollama.com'),
        'default_model': os.getenv('DEFAULT_MODEL', 'llama3.1:latest'),
        'cloud_model': os.getenv('CLOUD_MODEL', 'gpt-oss:20b'),
        'max_tokens': int(os.getenv('MAX_TOKENS', '8000')),
        'temperature': float(os.getenv('TEMPERATURE', '0.5')),
        'max_rpm': int(os.getenv('MAX_RPM', '5')),
        'memory_enabled': os.getenv('MEMORY_ENABLED', 'true').lower() == 'true',
        'debug_mode': os.getenv('DEBUG_MODE', 'false').lower() == 'true'
    }
    
    # 3. Validate required configurations
    required_configs = ['ollama_api_key']
    for config_key in required_configs:
        if not config[config_key]:
            st.warning(f"⚠️ {config_key.upper()} not found in environment variables")
    
    return config
```

### Logging Configuration
```python
def setup_logging():
    """
    Pseudocode for logging configuration
    """
    # 1. Create logs directory
    log_dir = Path('logs')
    log_dir.mkdir(exist_ok=True)
    
    # 2. Configure logging format
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'
    
    # 3. Set up file and console handlers
    file_handler = logging.FileHandler(
        log_dir / 'app.log',
        mode='a',
        encoding='utf-8'
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(log_format, date_format))
    
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    console_handler.setFormatter(logging.Formatter(log_format, date_format))
    
    # 4. Configure root logger
    logging.basicConfig(
        level=logging.INFO,
        handlers=[file_handler, console_handler],
        format=log_format,
        datefmt=date_format
    )
    
    # 5. Set specific logger levels
    logging.getLogger('crewai').setLevel(logging.WARNING)
    logging.getLogger('httpx').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)
```

### Configuration Validation
```python
def validate_configuration(config: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    Pseudocode for configuration validation
    """
    errors = []
    
    # 1. Validate API key format
    if config.get('ollama_api_key'):
        if not config['ollama_api_key'].startswith('ollama_'):
            errors.append("Invalid Ollama API key format")
    
    # 2. Validate numeric values
    if config.get('max_tokens', 0) <= 0:
        errors.append("MAX_TOKENS must be positive")
    
    if not 0 <= config.get('temperature', 0) <= 2:
        errors.append("TEMPERATURE must be between 0 and 2")
    
    if config.get('max_rpm', 0) <= 0:
        errors.append("MAX_RPM must be positive")
    
    # 3. Validate URL formats
    try:
        if config.get('ollama_base_url'):
            from urllib.parse import urlparse
            parsed = urlparse(config['ollama_base_url'])
            if not parsed.scheme or not parsed.netloc:
                errors.append("Invalid OLLAMA_BASE_URL format")
    except Exception:
        errors.append("Invalid OLLAMA_BASE_URL format")
    
    # 4. Return validation result
    return len(errors) == 0, errors
```

### Feature Flag Management
```python
class FeatureFlags:
    """
    Pseudocode for feature flag management
    """
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.flags = {
            'memory_enabled': config.get('memory_enabled', True),
            'debug_mode': config.get('debug_mode', False),
            'pdf_generation': config.get('pdf_generation', True),
            'web_search': config.get('web_search', True),
            'function_calling': config.get('function_calling', True),
            'rate_limiting': config.get('rate_limiting', True)
        }
    
    def is_enabled(self, feature: str) -> bool:
        """
        Check if a feature is enabled
        """
        return self.flags.get(feature, False)
    
    def enable_feature(self, feature: str):
        """
        Enable a feature
        """
        self.flags[feature] = True
    
    def disable_feature(self, feature: str):
        """
        Disable a feature
        """
        self.flags[feature] = False
```

### Configuration Caching
```python
from functools import lru_cache

@lru_cache(maxsize=1)
def get_cached_config() -> Dict[str, Any]:
    """
    Pseudocode for cached configuration loading
    """
    # 1. Load environment variables
    config = load_environment()
    
    # 2. Validate configuration
    is_valid, errors = validate_configuration(config)
    
    if not is_valid:
        st.error(f"Configuration errors: {', '.join(errors)}")
        return {}
    
    # 3. Return validated config
    return config

def clear_config_cache():
    """
    Clear configuration cache
    """
    get_cached_config.cache_clear()
```

## Usage Examples

### Basic Configuration Loading
```python
from config_manager import load_environment, configure_streamlit

# Configure Streamlit
configure_streamlit()

# Load environment configuration
config = load_environment()

# Use configuration
api_key = config['ollama_api_key']
model_name = config['default_model']
```

### Feature Flag Usage
```python
from config_manager import FeatureFlags

# Initialize feature flags
flags = FeatureFlags(config)

# Check if features are enabled
if flags.is_enabled('memory_enabled'):
    # Enable memory functionality
    pass

if flags.is_enabled('debug_mode'):
    # Enable debug logging
    logging.getLogger().setLevel(logging.DEBUG)
```

### Configuration Validation
```python
from config_manager import validate_configuration

# Validate configuration
is_valid, errors = validate_configuration(config)

if not is_valid:
    st.error("Configuration errors found:")
    for error in errors:
        st.error(f"  - {error}")
else:
    st.success("Configuration is valid")
```

## Environment Variables

### Required Variables
```bash
# Ollama API Key (required for cloud usage)
OLLAMA_API_KEY=ollama_your_api_key_here
```

### Optional Variables
```bash
# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_CLOUD_URL=https://ollama.com
DEFAULT_MODEL=llama3.1:latest
CLOUD_MODEL=gpt-oss:20b

# LLM Parameters
MAX_TOKENS=8000
TEMPERATURE=0.5
MAX_RPM=5

# Feature Flags
MEMORY_ENABLED=true
DEBUG_MODE=false
PDF_GENERATION=true
WEB_SEARCH=true
FUNCTION_CALLING=true
RATE_LIMITING=true
```

## Error Handling

### Configuration Error Handling
```python
def safe_config_loading():
    """
    Pseudocode for safe configuration loading
    """
    try:
        config = load_environment()
        is_valid, errors = validate_configuration(config)
        
        if not is_valid:
            st.warning("Configuration issues detected:")
            for error in errors:
                st.warning(f"  - {error}")
            
            # Use default configuration
            config = get_default_config()
        
        return config
        
    except Exception as e:
        st.error(f"Failed to load configuration: {e}")
        return get_default_config()

def get_default_config() -> Dict[str, Any]:
    """
    Get default configuration values
    """
    return {
        'ollama_api_key': None,
        'ollama_base_url': 'http://localhost:11434',
        'ollama_cloud_url': 'https://ollama.com',
        'default_model': 'llama3.1:latest',
        'cloud_model': 'gpt-oss:20b',
        'max_tokens': 8000,
        'temperature': 0.5,
        'max_rpm': 5,
        'memory_enabled': True,
        'debug_mode': False
    }
```

## Testing

### Configuration Tests
```python
def test_configuration_loading():
    """Test configuration loading"""
    config = load_environment()
    assert isinstance(config, dict)
    assert 'ollama_api_key' in config

def test_configuration_validation():
    """Test configuration validation"""
    valid_config = {
        'ollama_api_key': 'ollama_test_key',
        'max_tokens': 8000,
        'temperature': 0.5
    }
    
    is_valid, errors = validate_configuration(valid_config)
    assert is_valid
    assert len(errors) == 0

def test_feature_flags():
    """Test feature flag functionality"""
    config = {'memory_enabled': True, 'debug_mode': False}
    flags = FeatureFlags(config)
    
    assert flags.is_enabled('memory_enabled')
    assert not flags.is_enabled('debug_mode')
```
