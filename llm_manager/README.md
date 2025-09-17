# LLM Manager Module

This module handles Language Model (LLM) initialization, configuration, and management for the CrewAI multi-agent workflow system. It provides centralized LLM management with support for both local and cloud-based models.

## Structure

```
llm_manager/
├── __init__.py                    # Module initialization
└── llm_initializer.py             # LLM initialization and configuration
```

## Key Components

### LLM Initialization
- **Model Selection**: Support for local Ollama and Ollama Cloud models
- **Configuration Management**: Centralized LLM parameter configuration
- **Caching**: Streamlit caching for LLM instances
- **Error Handling**: Graceful handling of LLM initialization failures

### Model Support
- **Local Ollama**: llama3.1:latest and other local models
- **Ollama Cloud**: gpt-oss:20b and other cloud models
- **API Key Management**: Secure handling of cloud API keys
- **Fallback Mechanisms**: Automatic fallback to local models

## Pseudocode Examples

### LLM Initialization with Caching
```python
@st.cache_resource
def initialize_llm(use_cloud=False, api_key=None, _cache_key=None):
    """
    Pseudocode for LLM initialization with Streamlit caching
    """
    try:
        # 1. Determine model configuration
        if use_cloud and api_key:
            model_config = {
                'model': 'ollama/gpt-oss:20b',
                'base_url': 'https://ollama.com',
                'headers': {'Authorization': f'Bearer {api_key}'},
                'temperature': 0.5,
                'max_tokens': 8000
            }
        else:
            model_config = {
                'model': 'ollama/llama3.1:latest',
                'base_url': 'http://localhost:11434',
                'temperature': 0.5,
                'max_tokens': 8000
            }
        
        # 2. Create LLM instance
        llm = LLM(**model_config)
        
        # 3. Test connectivity
        test_message = [{"role": "user", "content": "Hello"}]
        response = llm.call(test_message)
        
        if response and response.strip():
            st.success(f"✅ LLM initialized: {model_config['model']}")
            return llm
        else:
            raise Exception("Empty response from LLM")
            
    except Exception as e:
        st.error(f"❌ Failed to initialize LLM: {e}")
        return None
```

### Cloud Status Checking
```python
def check_ollama_cloud_status():
    """
    Pseudocode for checking Ollama Cloud connectivity
    """
    try:
        # 1. Make test request to Ollama Cloud
        response = requests.get(
            'https://ollama.com/api/tags',
            timeout=10,
            headers={'Authorization': f'Bearer {api_key}'}
        )
        
        # 2. Check response status
        if response.status_code == 200:
            return True, "Ollama Cloud is accessible"
        else:
            return False, f"Ollama Cloud returned status {response.status_code}"
            
    except requests.exceptions.Timeout:
        return False, "Ollama Cloud request timed out"
    except requests.exceptions.ConnectionError:
        return False, "Cannot connect to Ollama Cloud"
    except Exception as e:
        return False, f"Ollama Cloud check failed: {str(e)}"
```

### Model Configuration Factory
```python
def create_model_config(use_cloud: bool, api_key: str = None) -> Dict[str, Any]:
    """
    Pseudocode for creating model configuration
    """
    base_config = {
        'temperature': 0.5,
        'max_tokens': 8000,
        'system_message': "You are an expert business consultant and writer..."
    }
    
    if use_cloud and api_key:
        return {
            **base_config,
            'model': 'ollama/gpt-oss:20b',
            'base_url': 'https://ollama.com',
            'headers': {'Authorization': f'Bearer {api_key}'}
        }
    else:
        return {
            **base_config,
            'model': 'ollama/llama3.1:latest',
            'base_url': 'http://localhost:11434'
        }
```

### LLM Health Check
```python
def check_llm_health(llm) -> Tuple[bool, str]:
    """
    Pseudocode for LLM health checking
    """
    try:
        # 1. Test basic functionality
        test_message = [{"role": "user", "content": "Respond with 'OK'"}]
        start_time = time.time()
        
        response = llm.call(test_message)
        response_time = time.time() - start_time
        
        # 2. Validate response
        if not response or not response.strip():
            return False, "Empty response from LLM"
        
        if response_time > 30:
            return False, f"LLM response too slow: {response_time:.2f}s"
        
        # 3. Check response quality
        if len(response) < 5:
            return False, "LLM response too short"
        
        return True, f"LLM healthy (response time: {response_time:.2f}s)"
        
    except Exception as e:
        return False, f"LLM health check failed: {str(e)}"
```

### Model Switching Logic
```python
def switch_model(current_llm, use_cloud: bool, api_key: str = None):
    """
    Pseudocode for switching between models
    """
    try:
        # 1. Clear cache to force reinitialization
        initialize_llm.clear()
        
        # 2. Create new LLM instance
        new_llm = initialize_llm(use_cloud=use_cloud, api_key=api_key)
        
        # 3. Validate new LLM
        if new_llm is None:
            st.error("Failed to switch model")
            return current_llm
        
        # 4. Test new LLM
        is_healthy, message = check_llm_health(new_llm)
        if not is_healthy:
            st.warning(f"New model has issues: {message}")
            return current_llm
        
        st.success(f"Successfully switched to {'cloud' if use_cloud else 'local'} model")
        return new_llm
        
    except Exception as e:
        st.error(f"Model switching failed: {e}")
        return current_llm
```

### Error Recovery
```python
def recover_from_llm_error(llm, error: Exception) -> Optional[LLM]:
    """
    Pseudocode for LLM error recovery
    """
    try:
        # 1. Log the error
        logging.error(f"LLM error occurred: {error}")
        
        # 2. Determine recovery strategy
        if "unauthorized" in str(error).lower():
            st.error("API key issue. Please check your Ollama Cloud API key.")
            return None
        
        elif "connection" in str(error).lower():
            st.warning("Connection issue. Trying local model...")
            return initialize_llm(use_cloud=False)
        
        elif "timeout" in str(error).lower():
            st.warning("Request timeout. Retrying with shorter timeout...")
            # Retry with modified configuration
            return retry_with_timeout(llm)
        
        else:
            st.error(f"Unknown LLM error: {error}")
            return None
            
    except Exception as recovery_error:
        st.error(f"Error recovery failed: {recovery_error}")
        return None
```

## Usage Examples

### Basic LLM Initialization
```python
from llm_manager import initialize_llm

# Initialize local LLM
local_llm = initialize_llm(use_cloud=False)

# Initialize cloud LLM
cloud_llm = initialize_llm(use_cloud=True, api_key="your_api_key")
```

### LLM Health Monitoring
```python
from llm_manager import check_llm_health

# Check LLM health
is_healthy, message = check_llm_health(llm)
if is_healthy:
    st.success(f"LLM is healthy: {message}")
else:
    st.error(f"LLM health issue: {message}")
```

### Model Switching
```python
from llm_manager import switch_model

# Switch to cloud model
new_llm = switch_model(current_llm, use_cloud=True, api_key=api_key)

# Switch to local model
new_llm = switch_model(current_llm, use_cloud=False)
```

## Configuration Options

### Model Parameters
```python
MODEL_CONFIGS = {
    'local': {
        'model': 'ollama/llama3.1:latest',
        'base_url': 'http://localhost:11434',
        'temperature': 0.5,
        'max_tokens': 8000
    },
    'cloud': {
        'model': 'ollama/gpt-oss:20b',
        'base_url': 'https://ollama.com',
        'temperature': 0.5,
        'max_tokens': 8000
    }
}
```

### System Messages
```python
SYSTEM_MESSAGES = {
    'default': "You are an expert business consultant and writer...",
    'research': "You are a research specialist with expertise in...",
    'analysis': "You are a data analyst with experience in...",
    'writing': "You are a professional content writer specializing in..."
}
```

## Error Handling

### Common Error Scenarios
```python
def handle_llm_errors(error: Exception) -> str:
    """
    Pseudocode for handling common LLM errors
    """
    error_message = str(error).lower()
    
    if "unauthorized" in error_message:
        return "❌ Authentication failed. Check your API key."
    
    elif "rate limit" in error_message:
        return "⚠️ Rate limit exceeded. Please wait and try again."
    
    elif "timeout" in error_message:
        return "⏱️ Request timed out. The model may be overloaded."
    
    elif "connection" in error_message:
        return "🔌 Connection failed. Check your internet connection."
    
    elif "model not found" in error_message:
        return "🤖 Model not found. Please check the model name."
    
    else:
        return f"❌ Unknown error: {error}"
```

### Retry Logic
```python
def retry_llm_call(llm, messages, max_retries=3):
    """
    Pseudocode for retrying LLM calls
    """
    for attempt in range(max_retries):
        try:
            response = llm.call(messages)
            if response and response.strip():
                return response
            else:
                raise Exception("Empty response")
                
        except Exception as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff
                time.sleep(wait_time)
                continue
            else:
                raise e
```

## Testing

### LLM Initialization Tests
```python
def test_llm_initialization():
    """Test LLM initialization"""
    llm = initialize_llm(use_cloud=False)
    assert llm is not None
    assert llm.model == 'ollama/llama3.1:latest'

def test_cloud_llm_initialization():
    """Test cloud LLM initialization"""
    llm = initialize_llm(use_cloud=True, api_key="test_key")
    assert llm is not None
    assert llm.model == 'ollama/gpt-oss:20b'

def test_llm_health_check():
    """Test LLM health checking"""
    llm = initialize_llm(use_cloud=False)
    is_healthy, message = check_llm_health(llm)
    assert isinstance(is_healthy, bool)
    assert isinstance(message, str)
```

### Error Handling Tests
```python
def test_error_recovery():
    """Test error recovery mechanisms"""
    # Test with invalid API key
    llm = initialize_llm(use_cloud=True, api_key="invalid_key")
    # Should handle error gracefully
    assert llm is None or isinstance(llm, LLM)
```
