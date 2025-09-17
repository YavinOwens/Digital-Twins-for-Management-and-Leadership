"""
Sidebar UI Components

This module contains sidebar-related UI components for the Streamlit application.
"""

import streamlit as st
from local_memory import get_memory_stats, clear_memory


def create_sidebar():
    """Create the sidebar with model configuration and memory management"""
    with st.sidebar:
        st.header("🔧 Model Configuration")
        
        # Memory management section
        st.header("🧠 Memory Management")
        
        # Display memory statistics
        try:
            stats = get_memory_stats()
            st.metric("Total Conversations", stats.get('total_conversations', 0))
            st.metric("Total Chunks", stats.get('total_chunks', 0))
            st.metric("Memory Size", f"{stats.get('memory_size_mb', 0):.2f} MB")
        except Exception as e:
            st.error(f"Failed to load memory stats: {e}")
        
        # Clear memory button
        if st.button("🗑️ Clear Memory", help="Clear all conversation memory"):
            try:
                clear_memory()
                st.success("Memory cleared successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"Failed to clear memory: {e}")
        
        # Workflow information
        st.header("ℹ️ Workflow Information")
        st.info("""
        **Available Workflows:**
        - **Standard**: Research → Analysis → Writing
        - **Two-Team**: + Data Strategy → DCAM → Tranch
        - **Three-Team**: + Compliance → Risk → Audit
        - **Four-Team**: + Information → Metadata → Quality
        - **Five-Team**: + Tender → Proposal → Compliance
        - **Six-Team**: + Engineering → Science → Architecture
        - **Seven-Team**: + Modeling → Code → Documentation
        """)
        
        # Performance tips
        st.header("⚡ Performance Tips")
        st.info("""
        - Use **Pre-search mode** for reliable results
        - **Native function calling** is experimental
        - Longer workflows take more time
        - Memory helps with context continuity
        """)
