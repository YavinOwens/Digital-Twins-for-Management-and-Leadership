"""
LLM Initializer Module

This module handles LLM initialization, configuration, and status checking.
"""

import streamlit as st
from crewai import LLM
import ollama


@st.cache_resource
def initialize_llm(use_cloud=False, api_key=None, _cache_key=None):
    """Initialize Ollama LLM with original working configuration"""
    try:
        print(f"🔧 Creating LLM: use_cloud={use_cloud}, api_key={'***' if api_key else None}")
        
        if use_cloud and api_key:
            # Create LLM for Ollama Cloud (original working configuration)
            llm = LLM(
                model="ollama/gpt-oss:20b",
                base_url="https://ollama.com",
                headers={'Authorization': f'Bearer {api_key}'},
                temperature=0.5,
                max_tokens=8000,
                system_message="You are an expert business consultant and writer. When asked to write reports, you must provide complete, detailed content - never summaries or placeholders. Write comprehensive, actionable content that executives can use immediately for decision-making. NEVER use ellipsis (...), continuation phrases, or placeholders like '[Insert content here]' or '[The actual content would continue here]'. Always write the complete, final content for every section. ONLY use references from the actual research data provided - NEVER make up citations, author names, or publication details."
            )
        else:
            # Create LLM for local Ollama
            ollama.list()
            llm = LLM(
                model="ollama/llama3.1:latest",
                base_url="http://localhost:11434",
                temperature=0.5,
                max_tokens=8000,
                system_message="You are an expert business consultant and writer. When asked to write reports, you must provide complete, detailed content - never summaries or placeholders. Write comprehensive, actionable content that executives can use immediately for decision-making. NEVER use ellipsis (...), continuation phrases, or placeholders like '[Insert content here]' or '[The actual content would continue here]'. Always write the complete, final content for every section. ONLY use references from the actual research data provided - NEVER make up citations, author names, or publication details."
            )
        
        print(f"✅ LLM created: {type(llm)}")
        return llm
    except Exception as e:
        print(f"❌ Failed to create LLM: {e}")
        if use_cloud:
            st.error(f"Failed to connect to Ollama Cloud. Please check your API key: {e}")
        else:
            st.error(f"Failed to connect to local Ollama. Please ensure Ollama is running and llama3.1:latest model is available: {e}")
        return None


def check_ollama_cloud_status():
    """Check Ollama Cloud service status"""
    try:
        import requests
        status_response = requests.get("https://ollama.com/api/tags", timeout=5)
        if status_response.status_code == 200:
            return True, "🚀 **Using Ollama Cloud (Turbo)** - Access to 120B+ models with faster inference ✅"
        else:
            return False, "⚠️ **Ollama Cloud Status** - Service may be experiencing issues. Retry logic enabled."
    except:
        return False, "⚠️ **Ollama Cloud Status** - Unable to verify service status. Retry logic enabled."
