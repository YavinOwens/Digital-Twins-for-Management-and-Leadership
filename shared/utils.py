"""
Shared Utilities

This module contains utility functions that are used across
multiple pages in the multi-page Streamlit application.
"""

import streamlit as st
import os
import time
from typing import Dict, Any, Optional
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_memory_stats() -> Dict[str, Any]:
    """
    Get memory statistics for the conversation memory system
    
    Returns:
        Dictionary containing memory statistics
    """
    try:
        from local_memory import get_memory_stats as local_get_memory_stats
        return local_get_memory_stats()
    except Exception as e:
        logger.error(f"Error getting memory stats: {e}")
        return {
            "total_conversations": 0,
            "persist_directory": "./memory_db",
            "collection_name": "conversation_memory",
            "error": str(e)
        }

def get_document_memory_stats() -> Dict[str, Any]:
    """
    Get document memory statistics
    
    Returns:
        Dictionary containing document memory statistics
    """
    try:
        from agent_tools.document_memory_manager import get_document_memory_stats as doc_get_memory_stats
        return doc_get_memory_stats()
    except Exception as e:
        logger.error(f"Error getting document memory stats: {e}")
        return {
            "total_chunks": 0,
            "total_documents": 0,
            "persist_directory": "./memory_db",
            "collection_name": "document_memory",
            "error": str(e)
        }

def get_system_info() -> Dict[str, Any]:
    """
    Get system information and status
    
    Returns:
        Dictionary containing system information
    """
    try:
        import psutil
        import platform
        
        return {
            "platform": platform.system(),
            "python_version": platform.python_version(),
            "cpu_count": psutil.cpu_count(),
            "memory_total": psutil.virtual_memory().total,
            "memory_available": psutil.virtual_memory().available,
            "disk_usage": psutil.disk_usage('/').percent,
            "uptime": time.time() - psutil.boot_time(),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting system info: {e}")
        return {
            "platform": "Unknown",
            "python_version": "Unknown",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

def initialize_llm(use_cloud: bool = True, api_key: Optional[str] = None) -> Optional[Any]:
    """
    Initialize LLM for use across pages
    
    Args:
        use_cloud: Whether to use cloud or local LLM
        api_key: API key for cloud LLM
        
    Returns:
        Initialized LLM object or None if failed
    """
    try:
        from agent_tools.robust_llm_v2 import create_robust_llm
        
        llm = create_robust_llm(use_cloud=use_cloud, api_key=api_key)
        logger.info(f"LLM initialized successfully: {type(llm)}")
        return llm
        
    except Exception as e:
        logger.error(f"Error initializing LLM: {e}")
        return None

def test_llm_connection(use_cloud: bool = True, api_key: Optional[str] = None) -> bool:
    """
    Test LLM connection
    
    Args:
        use_cloud: Whether to test cloud or local LLM
        api_key: API key for cloud LLM
        
    Returns:
        True if connection successful, False otherwise
    """
    try:
        llm = initialize_llm(use_cloud=use_cloud, api_key=api_key)
        if llm is None:
            return False
        
        # Test with a simple query
        test_messages = [{"role": "user", "content": "Hello, this is a test."}]
        response = llm.call(test_messages)
        
        if response and len(str(response).strip()) > 0:
            logger.info("LLM connection test successful")
            return True
        else:
            logger.warning("LLM connection test failed: empty response")
            return False
            
    except Exception as e:
        logger.error(f"LLM connection test failed: {e}")
        return False

def get_config(key: str, default: Any = None) -> Any:
    """
    Get configuration value from session state or environment
    
    Args:
        key: Configuration key
        default: Default value if key not found
        
    Returns:
        Configuration value
    """
    try:
        # Try session state first
        if key in st.session_state:
            return st.session_state[key]
        
        # Try environment variable
        env_value = os.getenv(key.upper())
        if env_value is not None:
            return env_value
        
        # Return default
        return default
        
    except Exception as e:
        logger.error(f"Error getting config {key}: {e}")
        return default

def set_config(key: str, value: Any) -> None:
    """
    Set configuration value in session state
    
    Args:
        key: Configuration key
        value: Configuration value
    """
    try:
        st.session_state[key] = value
        logger.info(f"Config set: {key} = {value}")
    except Exception as e:
        logger.error(f"Error setting config {key}: {e}")

def load_config_from_file(config_file: str = "config.json") -> Dict[str, Any]:
    """
    Load configuration from file
    
    Args:
        config_file: Path to configuration file
        
    Returns:
        Dictionary containing configuration
    """
    try:
        import json
        from pathlib import Path
        
        config_path = Path(config_file)
        if config_path.exists():
            with open(config_path, 'r') as f:
                config = json.load(f)
            logger.info(f"Configuration loaded from {config_file}")
            return config
        else:
            logger.warning(f"Configuration file {config_file} not found")
            return {}
            
    except Exception as e:
        logger.error(f"Error loading config from {config_file}: {e}")
        return {}

def save_config_to_file(config: Dict[str, Any], config_file: str = "config.json") -> bool:
    """
    Save configuration to file
    
    Args:
        config: Configuration dictionary
        config_file: Path to configuration file
        
    Returns:
        True if successful, False otherwise
    """
    try:
        import json
        from pathlib import Path
        
        config_path = Path(config_file)
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        
        logger.info(f"Configuration saved to {config_file}")
        return True
        
    except Exception as e:
        logger.error(f"Error saving config to {config_file}: {e}")
        return False

def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human readable format
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Formatted size string
    """
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"

def format_duration(seconds: float) -> str:
    """
    Format duration in human readable format
    
    Args:
        seconds: Duration in seconds
        
    Returns:
        Formatted duration string
    """
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f}m"
    else:
        hours = seconds / 3600
        return f"{hours:.1f}h"

def validate_api_key(api_key: str) -> bool:
    """
    Validate API key format
    
    Args:
        api_key: API key to validate
        
    Returns:
        True if valid format, False otherwise
    """
    if not api_key or not isinstance(api_key, str):
        return False
    
    # Basic validation - should be at least 20 characters
    if len(api_key) < 20:
        return False
    
    # Should contain alphanumeric characters
    if not api_key.replace('-', '').replace('_', '').isalnum():
        return False
    
    return True

def get_page_title(page_name: str) -> str:
    """
    Get formatted page title
    
    Args:
        page_name: Name of the page
        
    Returns:
        Formatted page title
    """
    titles = {
        "home": "Digital Twins Management System - Home",
        "workflows": "Digital Twins Management System - Workflows", 
        "documents": "Digital Twins Management System - Documents",
        "chat": "Digital Twins Management System - Chat",
        "analytics": "Digital Twins Management System - Analytics",
        "settings": "Digital Twins Management System - Settings",
        "help": "Digital Twins Management System - Help"
    }
    
    return titles.get(page_name.lower(), "Digital Twins Management System")

def create_breadcrumb(current_page: str) -> None:
    """
    Create breadcrumb navigation
    
    Args:
        current_page: Current page name
    """
    pages = [
        ("Home", "pages/1_🏠_Home.py"),
        ("Workflows", "pages/2_🤖_Workflows.py"),
        ("Documents", "pages/3_📁_Documents.py"),
        ("Chat", "pages/4_💬_Chat.py"),
        ("Analytics", "pages/5_📊_Analytics.py"),
        ("Settings", "pages/6_⚙️_Settings.py"),
        ("Help", "pages/7_📚_Help.py")
    ]
    
    breadcrumb_items = []
    for name, page in pages:
        if name.lower() == current_page.lower():
            breadcrumb_items.append(f"<strong>{name}</strong>")
            break
        else:
            breadcrumb_items.append(f'<a href="#" onclick="window.location.href=\'{page}\'">{name}</a>')
    
    breadcrumb_html = " > ".join(breadcrumb_items)
    
    st.markdown(f"""
    <div style="margin-bottom: 1rem; color: #666; font-size: 0.9rem;">
        {breadcrumb_html}
    </div>
    """, unsafe_allow_html=True)

def log_user_action(action: str, page: str, details: Optional[Dict[str, Any]] = None) -> None:
    """
    Log user actions for analytics
    
    Args:
        action: Action performed
        page: Page where action occurred
        details: Additional details
    """
    try:
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "page": page,
            "details": details or {},
            "session_id": st.session_state.get("session_id", "unknown")
        }
        
        logger.info(f"User action: {log_entry}")
        
        # Store in session state for analytics
        if "user_actions" not in st.session_state:
            st.session_state.user_actions = []
        
        st.session_state.user_actions.append(log_entry)
        
        # Keep only last 100 actions
        if len(st.session_state.user_actions) > 100:
            st.session_state.user_actions = st.session_state.user_actions[-100:]
            
    except Exception as e:
        logger.error(f"Error logging user action: {e}")

def get_user_actions() -> list:
    """
    Get user actions for analytics
    
    Returns:
        List of user actions
    """
    return st.session_state.get("user_actions", [])

def clear_user_actions() -> None:
    """Clear user actions history"""
    st.session_state.user_actions = []
    logger.info("User actions cleared")
