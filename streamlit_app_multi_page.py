"""
Digital Twins Management & Leadership System - Multi-Page Application

This is the main entry point for the multi-page Streamlit application.
It provides navigation and routing to different pages of the system.
"""

import streamlit as st
import os
from pathlib import Path
from shared.components import create_header, create_footer
from shared.utils import get_config, set_config, load_config_from_file
from shared.config import DEFAULT_CONFIG, load_config, save_config

def main():
    """Main function for the multi-page application"""
    
    # Page configuration
    st.set_page_config(
        page_title="Digital Twins Management System",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize session state
    initialize_session_state()
    
    # Load configuration
    config = load_config()
    
    # Create main header
    create_header("Digital Twins Management & Leadership System", "🤖")
    
    # Main content
    st.markdown("""
    # Welcome to Your Digital Twin Management System
    
    Transform your organization with AI-powered digital replicas of management systems and leadership teams. 
    This comprehensive platform provides real-time insights, decision support, simulations, and executive coaching tools.
    """)
    
    # Navigation cards
    st.markdown("## 🚀 Get Started")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 🤖 Workflows
        Execute multi-agent workflows with 1-7 specialized teams for comprehensive analysis and insights.
        """)
        if st.button("Go to Workflows", use_container_width=True, type="primary"):
            st.switch_page("pages/2_🤖_Workflows.py")
    
    with col2:
        st.markdown("""
        ### 📁 Documents
        Upload and manage your organizational documents with advanced processing and semantic search.
        """)
        if st.button("Go to Documents", use_container_width=True, type="primary"):
            st.switch_page("pages/3_📁_Documents.py")
    
    with col3:
        st.markdown("""
        ### 💬 Chat
        Interact with your Digital Twin through an intuitive conversational interface.
        """)
        if st.button("Go to Chat", use_container_width=True, type="primary"):
            st.switch_page("pages/4_💬_Chat.py")
    
    st.divider()
    
    # Additional navigation
    st.markdown("## 🛠️ System Tools")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📊 Analytics", use_container_width=True):
            st.switch_page("pages/5_📊_Analytics.py")
    
    with col2:
        if st.button("⚙️ Settings", use_container_width=True):
            st.switch_page("pages/6_⚙️_Settings.py")
    
    with col3:
        if st.button("📚 Help", use_container_width=True):
            st.switch_page("pages/7_📚_Help.py")
    
    with col4:
        if st.button("🏠 Home", use_container_width=True):
            st.switch_page("pages/1_🏠_Home.py")
    
    st.divider()
    
    # System overview
    st.markdown("## 📊 System Overview")
    
    try:
        from shared.utils import get_memory_stats, get_document_memory_stats, get_system_info
        
        memory_stats = get_memory_stats()
        doc_stats = get_document_memory_stats()
        system_info = get_system_info()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Stored Conversations", memory_stats.get("total_conversations", 0))
        
        with col2:
            st.metric("Stored Documents", doc_stats.get("total_documents", 0))
        
        with col3:
            st.metric("System Status", "🟢 Online")
        
        with col4:
            st.metric("Available Workflows", "7")
        
    except Exception as e:
        st.warning(f"Unable to load system overview: {e}")
    
    # Quick start guide
    st.markdown("## 🎯 Quick Start Guide")
    
    with st.expander("📋 Step-by-Step Setup", expanded=False):
        st.markdown("""
        **1. Configure Your AI Models**
        - Go to Settings → AI Models
        - Enter your Ollama Cloud API key
        - Test the connection
        
        **2. Upload Your Documents**
        - Navigate to Documents page
        - Upload your organizational data
        - Documents will be automatically processed
        
        **3. Start Your First Workflow**
        - Go to Workflows page
        - Select a workflow type
        - Ask your first question
        
        **4. Explore Analytics**
        - Check the Analytics page
        - Monitor system performance
        - View usage insights
        """)
    
    # Recent activity (placeholder)
    with st.expander("📈 Recent Activity", expanded=False):
        st.info("No recent activity to display. Start using the system to see your activity here!")
    
    # System information
    with st.expander("ℹ️ System Information", expanded=False):
        st.markdown(f"""
        **Application:** {config.get('app', {}).get('name', 'Digital Twins Management System')}
        **Version:** {config.get('app', {}).get('version', '1.0.0')}
        **Description:** {config.get('app', {}).get('description', 'AI-powered digital replicas of management systems')}
        **Platform:** {system_info.get('platform', 'Unknown')}
        **Python Version:** {system_info.get('python_version', 'Unknown')}
        """)
    
    # Create footer
    create_footer()

def initialize_session_state():
    """Initialize session state variables"""
    
    # Initialize session ID
    if "session_id" not in st.session_state:
        import uuid
        st.session_state.session_id = str(uuid.uuid4())
    
    # Initialize user actions
    if "user_actions" not in st.session_state:
        st.session_state.user_actions = []
    
    # Initialize configuration
    if "app_config" not in st.session_state:
        st.session_state.app_config = load_config()
    
    # Initialize chat messages
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Initialize conversation topics
    if "conversation_topics" not in st.session_state:
        st.session_state.conversation_topics = []
    
    # Initialize uploaded documents
    if "uploaded_documents" not in st.session_state:
        st.session_state.uploaded_documents = {}
    
    # Initialize workflow settings
    if "workflow_type" not in st.session_state:
        st.session_state.workflow_type = "Standard Research & Analysis"
    
    if "use_native_function_calling" not in st.session_state:
        st.session_state.use_native_function_calling = False

def check_system_requirements():
    """Check if system meets requirements"""
    
    requirements_met = True
    issues = []
    
    # Check Python version
    import sys
    if sys.version_info < (3, 8):
        requirements_met = False
        issues.append("Python 3.8 or higher is required")
    
    # Check required packages
    required_packages = [
        "streamlit",
        "crewai", 
        "chromadb",
        "pandas",
        "plotly"
    ]
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            requirements_met = False
            issues.append(f"Package '{package}' is not installed")
    
    # Check memory directory
    memory_dir = Path("memory_db")
    if not memory_dir.exists():
        try:
            memory_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            requirements_met = False
            issues.append(f"Cannot create memory directory: {e}")
    
    return requirements_met, issues

def display_system_status():
    """Display system status and requirements"""
    
    requirements_met, issues = check_system_requirements()
    
    if not requirements_met:
        st.error("⚠️ System Requirements Not Met")
        for issue in issues:
            st.error(f"• {issue}")
        
        st.markdown("""
        **To fix these issues:**
        1. Install missing packages: `pip install -r requirements.txt`
        2. Ensure Python 3.8+ is installed
        3. Check file system permissions
        """)
        return False
    
    return True

if __name__ == "__main__":
    # Check system requirements
    if not display_system_status():
        st.stop()
    
    # Run main application
    main()
