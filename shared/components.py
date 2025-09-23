"""
Shared UI Components

This module contains reusable UI components that are used across
multiple pages in the multi-page Streamlit application.
"""

import streamlit as st
from datetime import datetime
from typing import Optional, Dict, Any

def create_header(title: str, icon: str = "🤖") -> None:
    """
    Create a consistent header for all pages
    
    Args:
        title: The page title
        icon: The page icon (emoji)
    """
    st.markdown(f"""
    <div style="text-align: center; padding: 1rem 0; border-bottom: 2px solid #e0e0e0; margin-bottom: 2rem;">
        <h1 style="margin: 0; color: #1f77b4; font-size: 2.5rem;">
            {icon} {title}
        </h1>
        <p style="margin: 0.5rem 0 0 0; color: #666; font-size: 1.1rem;">
            Digital Twins Management & Leadership System
        </p>
    </div>
    """, unsafe_allow_html=True)

def create_footer() -> None:
    """Create a consistent footer for all pages"""
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0; border-top: 1px solid #e0e0e0; margin-top: 3rem; color: #666;">
        <p style="margin: 0;">
            © 2024 Digital Twins Management System | 
            <a href="#" style="color: #1f77b4; text-decoration: none;">Privacy Policy</a> | 
            <a href="#" style="color: #1f77b4; text-decoration: none;">Terms of Service</a> | 
            <a href="#" style="color: #1f77b4; text-decoration: none;">Support</a>
        </p>
        <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem;">
            Powered by AI • Built with Streamlit • Enhanced with CrewAI
        </p>
    </div>
    """, unsafe_allow_html=True)

def create_sidebar_info() -> None:
    """Create consistent sidebar information for all pages"""
    
    # System status
    st.markdown("### 📊 System Status")
    
    try:
        from .utils import get_memory_stats, get_document_memory_stats
        
        memory_stats = get_memory_stats()
        doc_stats = get_document_memory_stats()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Conversations", memory_stats.get("total_conversations", 0))
        
        with col2:
            st.metric("Documents", doc_stats.get("total_documents", 0))
        
        st.markdown("**Status:** 🟢 Online")
        
    except Exception as e:
        st.warning(f"Status unavailable: {e}")
    
    st.divider()
    
    # Quick actions
    st.markdown("### 🚀 Quick Actions")
    
    if st.button("🔄 Refresh", use_container_width=True):
        st.rerun()
    
    if st.button("🧹 Clear Cache", use_container_width=True):
        st.cache_data.clear()
        st.success("Cache cleared!")
        st.rerun()
    
    # Page info
    st.markdown("### ℹ️ Page Info")
    st.markdown(f"**Current Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    st.markdown(f"**Version:** 1.0.0")
    st.markdown(f"**Environment:** Production")

def create_workflow_card(workflow_name: str, description: str, teams: int, 
                        duration: str, complexity: str, use_case: str) -> None:
    """
    Create a workflow card component
    
    Args:
        workflow_name: Name of the workflow
        description: Description of the workflow
        teams: Number of teams in the workflow
        duration: Expected duration
        complexity: Complexity level
        use_case: Primary use case
    """
    with st.container():
        st.markdown(f"""
        <div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 1rem; margin: 0.5rem 0; background: #f9f9f9;">
            <h3 style="margin: 0 0 0.5rem 0; color: #1f77b4;">{workflow_name}</h3>
            <p style="margin: 0 0 1rem 0; color: #666;">{description}</p>
            <div style="display: flex; gap: 1rem; font-size: 0.9rem; color: #666;">
                <span>👥 {teams} Teams</span>
                <span>⏱️ {duration}</span>
                <span>📊 {complexity}</span>
            </div>
            <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem; color: #888;">{use_case}</p>
        </div>
        """, unsafe_allow_html=True)

def create_metric_card(title: str, value: str, delta: Optional[str] = None, 
                      delta_color: str = "normal") -> None:
    """
    Create a metric card component
    
    Args:
        title: Title of the metric
        value: Value to display
        delta: Delta value (optional)
        delta_color: Color of the delta ("normal", "inverse", "off")
    """
    delta_html = ""
    if delta:
        color = "#2ca02c" if delta_color == "normal" else "#d62728" if delta_color == "inverse" else "#666"
        delta_html = f'<span style="color: {color}; font-size: 0.8rem;">{delta}</span>'
    
    st.markdown(f"""
    <div style="text-align: center; padding: 1rem; border: 1px solid #e0e0e0; border-radius: 8px; background: white;">
        <h4 style="margin: 0 0 0.5rem 0; color: #666; font-size: 0.9rem;">{title}</h4>
        <h2 style="margin: 0 0 0.5rem 0; color: #1f77b4; font-size: 2rem;">{value}</h2>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)

def create_info_box(title: str, content: str, box_type: str = "info") -> None:
    """
    Create an info box component
    
    Args:
        title: Title of the info box
        content: Content of the info box
        box_type: Type of box ("info", "success", "warning", "error")
    """
    colors = {
        "info": "#1f77b4",
        "success": "#2ca02c", 
        "warning": "#ff7f0e",
        "error": "#d62728"
    }
    
    color = colors.get(box_type, colors["info"])
    
    st.markdown(f"""
    <div style="border-left: 4px solid {color}; padding: 1rem; margin: 1rem 0; background: #f9f9f9;">
        <h4 style="margin: 0 0 0.5rem 0; color: {color};">{title}</h4>
        <p style="margin: 0; color: #666;">{content}</p>
    </div>
    """, unsafe_allow_html=True)

def create_progress_bar(current: int, total: int, label: str = "Progress") -> None:
    """
    Create a progress bar component
    
    Args:
        current: Current progress value
        total: Total progress value
        label: Label for the progress bar
    """
    percentage = (current / total) * 100 if total > 0 else 0
    
    st.markdown(f"""
    <div style="margin: 1rem 0;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
            <span style="font-weight: bold;">{label}</span>
            <span style="color: #666;">{current}/{total} ({percentage:.1f}%)</span>
        </div>
        <div style="background: #e0e0e0; border-radius: 4px; height: 8px; overflow: hidden;">
            <div style="background: #1f77b4; height: 100%; width: {percentage}%; transition: width 0.3s ease;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_feature_card(title: str, description: str, icon: str, 
                       features: list, action_text: str = "Learn More") -> None:
    """
    Create a feature card component
    
    Args:
        title: Title of the feature
        description: Description of the feature
        icon: Icon for the feature
        features: List of feature items
        action_text: Text for the action button
    """
    features_html = "".join([f"<li>{feature}</li>" for feature in features])
    
    st.markdown(f"""
    <div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 1.5rem; margin: 1rem 0; background: white; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
        <div style="text-align: center; margin-bottom: 1rem;">
            <span style="font-size: 3rem;">{icon}</span>
            <h3 style="margin: 0.5rem 0; color: #1f77b4;">{title}</h3>
            <p style="margin: 0; color: #666;">{description}</p>
        </div>
        <ul style="margin: 1rem 0; padding-left: 1.5rem; color: #666;">
            {features_html}
        </ul>
        <div style="text-align: center; margin-top: 1.5rem;">
            <button style="background: #1f77b4; color: white; border: none; padding: 0.5rem 1rem; border-radius: 4px; cursor: pointer;">
                {action_text}
            </button>
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_status_indicator(status: str, message: str) -> None:
    """
    Create a status indicator component
    
    Args:
        status: Status type ("success", "warning", "error", "info")
        message: Status message
    """
    colors = {
        "success": "#2ca02c",
        "warning": "#ff7f0e",
        "error": "#d62728",
        "info": "#1f77b4"
    }
    
    icons = {
        "success": "✅",
        "warning": "⚠️",
        "error": "❌",
        "info": "ℹ️"
    }
    
    color = colors.get(status, colors["info"])
    icon = icons.get(status, icons["info"])
    
    st.markdown(f"""
    <div style="display: flex; align-items: center; padding: 0.5rem; background: #f9f9f9; border-radius: 4px; margin: 0.5rem 0;">
        <span style="font-size: 1.2rem; margin-right: 0.5rem;">{icon}</span>
        <span style="color: {color}; font-weight: bold;">{message}</span>
    </div>
    """, unsafe_allow_html=True)
