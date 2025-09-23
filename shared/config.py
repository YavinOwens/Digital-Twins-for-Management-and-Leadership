"""
Configuration Management

This module handles configuration management for the multi-page
Streamlit application.
"""

import os
import json
import streamlit as st
from typing import Dict, Any, Optional
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Default configuration
DEFAULT_CONFIG = {
    "app": {
        "name": "Digital Twins Management System",
        "version": "1.0.0",
        "description": "AI-powered digital replicas of management systems and leadership teams",
        "author": "Digital Twins Team",
        "url": "https://digitaltwins.com"
    },
    "ai_models": {
        "default_provider": "ollama_cloud",
        "ollama_cloud": {
            "enabled": True,
            "base_url": "https://ollama.com",
            "model": "gpt-oss:20b",
            "temperature": 0.7,
            "max_tokens": 8000,
            "top_p": 0.9
        },
        "ollama_local": {
            "enabled": False,
            "base_url": "http://localhost:11434",
            "model": "llama3.1:latest",
            "temperature": 0.7,
            "max_tokens": 8000,
            "top_p": 0.9
        },
        "openai": {
            "enabled": False,
            "base_url": "https://api.openai.com/v1",
            "model": "gpt-4",
            "temperature": 0.7,
            "max_tokens": 8000,
            "top_p": 0.9
        }
    },
    "workflows": {
        "default_workflow": "Standard Research & Analysis",
        "max_concurrent": 3,
        "timeout_minutes": 10,
        "enable_memory": True,
        "enable_presearch": True,
        "max_memory_results": 3
    },
    "documents": {
        "max_file_size_mb": 100,
        "supported_formats": ["pdf", "docx", "csv", "xlsx", "json", "txt", "md"],
        "chunk_size": 1000,
        "chunk_overlap": 200,
        "enable_auto_processing": True
    },
    "search": {
        "max_results": 5,
        "timeout_seconds": 30,
        "enable_web_search": True,
        "enable_memory_search": True,
        "enable_document_search": True
    },
    "security": {
        "enable_encryption": True,
        "enable_audit_logging": True,
        "data_retention_days": 30,
        "enable_user_authentication": False
    },
    "performance": {
        "enable_caching": True,
        "cache_ttl_minutes": 60,
        "max_memory_gb": 8,
        "max_cpu_percent": 80,
        "enable_monitoring": True
    },
    "ui": {
        "theme": "auto",
        "primary_color": "#1f77b4",
        "secondary_color": "#ff7f0e",
        "accent_color": "#2ca02c",
        "sidebar_width": 300,
        "content_width": "wide",
        "show_sidebar": True,
        "show_footer": True
    },
    "export": {
        "default_format": "pdf",
        "include_metadata": True,
        "include_timestamps": True,
        "quality": "high",
        "compress": False
    }
}

def get_config(key: Optional[str] = None, default: Any = None) -> Any:
    """
    Get configuration value
    
    Args:
        key: Configuration key (dot notation supported)
        default: Default value if key not found
        
    Returns:
        Configuration value
    """
    try:
        # Load config from session state or file
        config = load_config()
        
        if key is None:
            return config
        
        # Navigate through nested keys
        keys = key.split('.')
        value = config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
        
    except Exception as e:
        logger.error(f"Error getting config {key}: {e}")
        return default

def set_config(key: str, value: Any) -> bool:
    """
    Set configuration value
    
    Args:
        key: Configuration key (dot notation supported)
        value: Configuration value
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Load current config
        config = load_config()
        
        # Navigate to the parent of the target key
        keys = key.split('.')
        target = config
        
        for k in keys[:-1]:
            if k not in target:
                target[k] = {}
            target = target[k]
        
        # Set the value
        target[keys[-1]] = value
        
        # Save config
        return save_config(config)
        
    except Exception as e:
        logger.error(f"Error setting config {key}: {e}")
        return False

def load_config() -> Dict[str, Any]:
    """
    Load configuration from session state or file
    
    Returns:
        Configuration dictionary
    """
    try:
        # Try session state first
        if "app_config" in st.session_state:
            return st.session_state.app_config
        
        # Try loading from file
        config_file = "config/app_config.json"
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                config = json.load(f)
                st.session_state.app_config = config
                return config
        
        # Use default config
        st.session_state.app_config = DEFAULT_CONFIG.copy()
        return st.session_state.app_config
        
    except Exception as e:
        logger.error(f"Error loading config: {e}")
        return DEFAULT_CONFIG.copy()

def save_config(config: Dict[str, Any]) -> bool:
    """
    Save configuration to session state and file
    
    Args:
        config: Configuration dictionary
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Save to session state
        st.session_state.app_config = config
        
        # Save to file
        config_file = "config/app_config.json"
        os.makedirs(os.path.dirname(config_file), exist_ok=True)
        
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        
        logger.info("Configuration saved successfully")
        return True
        
    except Exception as e:
        logger.error(f"Error saving config: {e}")
        return False

def reset_config() -> bool:
    """
    Reset configuration to defaults
    
    Returns:
        True if successful, False otherwise
    """
    try:
        st.session_state.app_config = DEFAULT_CONFIG.copy()
        return save_config(DEFAULT_CONFIG)
    except Exception as e:
        logger.error(f"Error resetting config: {e}")
        return False

def get_environment_config() -> Dict[str, Any]:
    """
    Get configuration from environment variables
    
    Returns:
        Dictionary of environment-based configuration
    """
    env_config = {}
    
    # AI Model settings
    if os.getenv('OLLAMA_API_KEY'):
        env_config['ai_models'] = {
            'ollama_cloud': {
                'api_key': os.getenv('OLLAMA_API_KEY'),
                'base_url': os.getenv('OLLAMA_CLOUD_BASE_URL', 'https://ollama.com'),
                'model': os.getenv('OLLAMA_CLOUD_MODEL', 'gpt-oss:20b')
            }
        }
    
    # App settings
    if os.getenv('APP_NAME'):
        env_config['app'] = {
            'name': os.getenv('APP_NAME'),
            'version': os.getenv('APP_VERSION', '1.0.0')
        }
    
    # Performance settings
    if os.getenv('MAX_MEMORY_GB'):
        env_config['performance'] = {
            'max_memory_gb': int(os.getenv('MAX_MEMORY_GB'))
        }
    
    return env_config

def merge_configs(base_config: Dict[str, Any], override_config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Merge two configuration dictionaries
    
    Args:
        base_config: Base configuration
        override_config: Override configuration
        
    Returns:
        Merged configuration
    """
    merged = base_config.copy()
    
    for key, value in override_config.items():
        if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
            merged[key] = merge_configs(merged[key], value)
        else:
            merged[key] = value
    
    return merged

def validate_config(config: Dict[str, Any]) -> tuple[bool, list]:
    """
    Validate configuration
    
    Args:
        config: Configuration to validate
        
    Returns:
        Tuple of (is_valid, error_messages)
    """
    errors = []
    
    try:
        # Validate AI models
        if 'ai_models' in config:
            ai_config = config['ai_models']
            if 'default_provider' not in ai_config:
                errors.append("AI models: default_provider is required")
            
            for provider in ['ollama_cloud', 'ollama_local', 'openai']:
                if provider in ai_config:
                    provider_config = ai_config[provider]
                    if provider_config.get('enabled', False):
                        if 'model' not in provider_config:
                            errors.append(f"AI models {provider}: model is required when enabled")
        
        # Validate workflows
        if 'workflows' in config:
            workflow_config = config['workflows']
            if 'max_concurrent' in workflow_config:
                if not isinstance(workflow_config['max_concurrent'], int) or workflow_config['max_concurrent'] < 1:
                    errors.append("Workflows: max_concurrent must be a positive integer")
        
        # Validate documents
        if 'documents' in config:
            doc_config = config['documents']
            if 'max_file_size_mb' in doc_config:
                if not isinstance(doc_config['max_file_size_mb'], (int, float)) or doc_config['max_file_size_mb'] <= 0:
                    errors.append("Documents: max_file_size_mb must be a positive number")
        
        # Validate UI
        if 'ui' in config:
            ui_config = config['ui']
            if 'theme' in ui_config:
                if ui_config['theme'] not in ['light', 'dark', 'auto']:
                    errors.append("UI: theme must be 'light', 'dark', or 'auto'")
        
        return len(errors) == 0, errors
        
    except Exception as e:
        errors.append(f"Configuration validation error: {e}")
        return False, errors

def export_config(config: Dict[str, Any], format: str = 'json') -> str:
    """
    Export configuration to string
    
    Args:
        config: Configuration to export
        format: Export format ('json', 'yaml')
        
    Returns:
        Exported configuration string
    """
    try:
        if format.lower() == 'json':
            return json.dumps(config, indent=2)
        elif format.lower() == 'yaml':
            import yaml
            return yaml.dump(config, default_flow_style=False)
        else:
            raise ValueError(f"Unsupported format: {format}")
    except Exception as e:
        logger.error(f"Error exporting config: {e}")
        return ""

def import_config(config_string: str, format: str = 'json') -> tuple[bool, Dict[str, Any]]:
    """
    Import configuration from string
    
    Args:
        config_string: Configuration string
        format: Import format ('json', 'yaml')
        
    Returns:
        Tuple of (success, config_dict)
    """
    try:
        if format.lower() == 'json':
            config = json.loads(config_string)
        elif format.lower() == 'yaml':
            import yaml
            config = yaml.safe_load(config_string)
        else:
            raise ValueError(f"Unsupported format: {format}")
        
        # Validate the imported config
        is_valid, errors = validate_config(config)
        if not is_valid:
            logger.warning(f"Imported config validation errors: {errors}")
        
        return True, config
        
    except Exception as e:
        logger.error(f"Error importing config: {e}")
        return False, {}

def get_config_schema() -> Dict[str, Any]:
    """
    Get configuration schema for validation
    
    Returns:
        Configuration schema dictionary
    """
    return {
        "type": "object",
        "properties": {
            "app": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "version": {"type": "string"},
                    "description": {"type": "string"}
                },
                "required": ["name", "version"]
            },
            "ai_models": {
                "type": "object",
                "properties": {
                    "default_provider": {"type": "string", "enum": ["ollama_cloud", "ollama_local", "openai"]},
                    "ollama_cloud": {"type": "object"},
                    "ollama_local": {"type": "object"},
                    "openai": {"type": "object"}
                },
                "required": ["default_provider"]
            },
            "workflows": {
                "type": "object",
                "properties": {
                    "max_concurrent": {"type": "integer", "minimum": 1},
                    "timeout_minutes": {"type": "integer", "minimum": 1}
                }
            }
        },
        "required": ["app", "ai_models"]
    }
