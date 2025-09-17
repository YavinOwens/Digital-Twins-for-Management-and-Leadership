"""
Model Selection UI Components

This module contains model selection and configuration UI components.
"""

import streamlit as st
import os
from llm_manager import check_ollama_cloud_status, initialize_llm
from agent_test_functions import test_function_calling_support


def create_model_selection_ui():
    """Create the model selection and configuration UI"""
    
    # Model selection - Ollama Cloud (Turbo)
    model_option = "Ollama Cloud (Turbo)"
    
    # Check Ollama Cloud status
    status_ok, status_message = check_ollama_cloud_status()
    if status_ok:
        st.info(status_message)
    else:
        st.warning(status_message)
    
    st.subheader("🔑 API Configuration")
    # Try to get API key from environment first
    env_api_key = os.getenv('OLLAMA_API_KEY')
    api_key = st.text_input(
        "Ollama API Key:",
        value=env_api_key if env_api_key else "",
        type="password",
        help="Enter your Ollama Cloud API key. Get it from https://ollama.ai/settings"
    )
    
    if not api_key:
        st.warning("⚠️ Please enter your Ollama API key to use cloud models")
        st.stop()
    
    # Function calling test button
    if st.button("🧪 Test Function Calling Support"):
        test_llm = initialize_llm(use_cloud=True, api_key=api_key, _cache_key=f"test_cloud_{api_key[:8] if api_key else 'none'}")
        
        if test_llm:
            with st.spinner("Testing function calling capabilities..."):
                model_name = "gpt-oss:20b (Turbo)"
                success, message = test_function_calling_support(test_llm, model_name)
                
                if success:
                    st.success(f"✅ {model_name}: {message}")
                else:
                    st.error(f"❌ {model_name}: {message}")
        else:
            st.error("❌ Failed to initialize LLM for testing")
    
    # Show info about function calling
    st.info("ℹ️ **Default Mode**: Pre-search mode is enabled by default for reliable results. Native function calling is experimental and may not work with all models.")
    
    return api_key


def create_workflow_mode_ui():
    """Create the workflow mode selection UI"""
    st.subheader("⚙️ Workflow Mode")
    use_native = st.checkbox(
        "Use Native Function Calling",
        value=False,  # Always default to False (pre-search mode)
        help="If enabled, agents will try to call tools directly. If disabled, uses pre-search approach. Pre-search mode is recommended for reliable results."
    )
    
    if use_native:
        st.info("🚀 Native function calling mode - agents will call tools directly")
    else:
        st.info("🔍 Pre-search mode - data is searched first, then processed")
    
    return use_native
