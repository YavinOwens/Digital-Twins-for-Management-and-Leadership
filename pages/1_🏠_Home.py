"""
Home Page - Digital Twins Management & Leadership System

This is the landing page of the multi-page Streamlit application.
"""

import streamlit as st
import time
from datetime import datetime
from shared.components import create_header, create_footer, create_sidebar_info
from shared.utils import get_memory_stats, get_system_info

def main():
    """Main function for the Home page"""
    
    # Page configuration
    st.set_page_config(
        page_title="Digital Twins Management System - Home",
        page_icon="🏠",
        layout="wide"
    )
    
    # Create header
    create_header("Digital Twins Management & Leadership System", "🏠")
    
    # Main content
    st.markdown("""
    # Welcome to Your Digital Twin Management System
    
    Transform your organization with AI-powered digital replicas of management systems and leadership teams. 
    This comprehensive platform provides real-time insights, decision support, simulations, and executive coaching tools.
    """)
    
    # Key features overview
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 🤖 Multi-Agent Workflows
        - **1-7 Team Configurations**: From basic research to complete enterprise solutions
        - **Specialized Agents**: Research, Data Strategy, Compliance, Information Management
        - **Sequential Processing**: Context flows through teams in logical business sequence
        """)
    
    with col2:
        st.markdown("""
        ### 🧠 Advanced RAG System
        - **Document Processing**: 15+ file formats supported
        - **Vector Storage**: ChromaDB with semantic search
        - **Memory Management**: Conversation and document memory
        - **Quality Assurance**: Source validation and Harvard referencing
        """)
    
    with col3:
        st.markdown("""
        ### 🚀 Enterprise Features
        - **Hybrid AI**: Local Ollama + Cloud models
        - **Real-time Search**: DuckDuckGo integration
        - **PDF Generation**: Professional report templates
        - **Team Outputs**: Structured saving and management
        """)
    
    st.divider()
    
    # Quick start section
    st.markdown("## 🚀 Quick Start")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### Get Started in 3 Steps:
        1. **Configure Models** → Go to Settings to set up your AI models
        2. **Upload Documents** → Add your organizational data
        3. **Run Workflows** → Execute multi-agent analysis
        """)
        
        if st.button("⚙️ Go to Settings", type="primary", use_container_width=True):
            st.switch_page("pages/6_⚙️_Settings.py")
    
    with col2:
        st.markdown("""
        ### Ready to Analyze?
        - **Start with Research** → Basic analysis workflow
        - **Enterprise Solution** → Full 7-team workflow
        - **Document Analysis** → Upload and analyze your data
        """)
        
        if st.button("🤖 Start Workflow", type="secondary", use_container_width=True):
            st.switch_page("pages/2_🤖_Workflows.py")
    
    st.divider()
    
    # System status
    st.markdown("## 📊 System Status")
    
    try:
        memory_stats = get_memory_stats()
        system_info = get_system_info()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Stored Conversations", memory_stats.get("total_conversations", 0))
        
        with col2:
            st.metric("System Status", "🟢 Online")
        
        with col3:
            st.metric("Available Workflows", "7")
        
        with col4:
            st.metric("Document Formats", "15+")
        
    except Exception as e:
        st.warning(f"Unable to load system status: {e}")
    
    # Recent activity (placeholder)
    st.markdown("## 📈 Recent Activity")
    
    with st.expander("View Recent Activity", expanded=False):
        st.info("No recent activity to display. Start using the system to see your activity here!")
    
    # Create footer
    create_footer()

if __name__ == "__main__":
    main()
