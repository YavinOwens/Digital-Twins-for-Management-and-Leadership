"""
Application Configuration Module

This module handles application configuration, environment setup, and initialization.
"""

import os
import logging
from dotenv import load_dotenv


def configure_streamlit():
    """Configure Streamlit page settings"""
    import streamlit as st
    
    st.set_page_config(
        page_title="CrewAI Workflow with Streamlit",
        page_icon="🤖",
        layout="wide"
    )


def load_environment():
    """Load environment variables from .env file"""
    load_dotenv()
    return {
        'ollama_api_key': os.getenv('OLLAMA_API_KEY'),
        'ollama_model': os.getenv('OLLAMA_MODEL', 'llama3.1:latest'),
        'max_memory_results': int(os.getenv('MAX_MEMORY_RESULTS', '3')),
        'max_execution_time': int(os.getenv('MAX_EXECUTION_TIME', '180')),
        'max_rpm': int(os.getenv('MAX_RPM', '20'))
    }


def setup_logging():
    """Configure logging for better debugging"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)
