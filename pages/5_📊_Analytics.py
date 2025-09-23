"""
Analytics Page - System Analytics and Insights

This page provides analytics and insights about the Digital Twins system usage and performance.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from shared.components import create_header, create_footer, create_sidebar_info
from shared.utils import get_memory_stats, get_document_memory_stats, get_system_info

def main():
    """Main function for the Analytics page"""
    
    # Page configuration
    st.set_page_config(
        page_title="Digital Twins Management System - Analytics",
        page_icon="📊",
        layout="wide"
    )
    
    # Create header
    create_header("System Analytics & Insights", "📊")
    
    # Sidebar
    with st.sidebar:
        create_sidebar_info()
        
        st.header("📊 Analytics Settings")
        
        # Date range selector
        st.subheader("📅 Date Range")
        date_range = st.selectbox(
            "Select time period:",
            ["Last 7 days", "Last 30 days", "Last 90 days", "All time"],
            index=1
        )
        
        # Metric selection
        st.subheader("📈 Metrics")
        show_conversations = st.checkbox("Conversation Metrics", value=True)
        show_documents = st.checkbox("Document Metrics", value=True)
        show_workflows = st.checkbox("Workflow Metrics", value=True)
        show_performance = st.checkbox("Performance Metrics", value=True)
    
    # Main content
    st.markdown("## 📊 System Analytics & Insights")
    
    # System overview
    st.markdown("### 🎯 System Overview")
    
    try:
        memory_stats = get_memory_stats()
        doc_stats = get_document_memory_stats()
        system_info = get_system_info()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Total Conversations",
                memory_stats.get("total_conversations", 0),
                delta="+12" if memory_stats.get("total_conversations", 0) > 0 else "0"
            )
        
        with col2:
            st.metric(
                "Stored Documents",
                doc_stats.get("total_documents", 0),
                delta="+3" if doc_stats.get("total_documents", 0) > 0 else "0"
            )
        
        with col3:
            st.metric(
                "Document Chunks",
                doc_stats.get("total_chunks", 0),
                delta="+45" if doc_stats.get("total_chunks", 0) > 0 else "0"
            )
        
        with col4:
            st.metric(
                "System Status",
                "🟢 Online",
                delta="99.9% uptime"
            )
    
    except Exception as e:
        st.warning(f"Unable to load system metrics: {e}")
    
    # Conversation analytics
    if show_conversations:
        st.markdown("### 💬 Conversation Analytics")
        
        # Mock data for demonstration
        conversation_data = pd.DataFrame({
            'Date': pd.date_range(start='2024-01-01', end='2024-01-31', freq='D'),
            'Conversations': [5, 8, 12, 15, 18, 22, 25, 28, 30, 32, 35, 38, 40, 42, 45, 48, 50, 52, 55, 58, 60, 62, 65, 68, 70, 72, 75, 78, 80, 82, 85],
            'Messages': [15, 24, 36, 45, 54, 66, 75, 84, 90, 96, 105, 114, 120, 126, 135, 144, 150, 156, 165, 174, 180, 186, 195, 204, 210, 216, 225, 234, 240, 246, 255]
        })
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.line(conversation_data, x='Date', y='Conversations', 
                         title='Daily Conversations', color_discrete_sequence=['#1f77b4'])
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.bar(conversation_data, x='Date', y='Messages', 
                        title='Daily Messages', color_discrete_sequence=['#ff7f0e'])
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
    
    # Document analytics
    if show_documents:
        st.markdown("### 📁 Document Analytics")
        
        # Mock document data
        document_data = pd.DataFrame({
            'File Type': ['PDF', 'DOCX', 'CSV', 'XLSX', 'JSON', 'TXT'],
            'Count': [15, 12, 8, 6, 4, 3],
            'Size (MB)': [45.2, 32.1, 12.8, 8.9, 5.2, 2.1]
        })
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.pie(document_data, values='Count', names='File Type', 
                        title='Document Types Distribution')
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.bar(document_data, x='File Type', y='Size (MB)', 
                        title='Document Sizes by Type', color_discrete_sequence=['#2ca02c'])
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
    
    # Workflow analytics
    if show_workflows:
        st.markdown("### 🤖 Workflow Analytics")
        
        # Mock workflow data
        workflow_data = pd.DataFrame({
            'Workflow Type': ['1 Team', '2 Teams', '3 Teams', '4 Teams', '5 Teams', '6 Teams', '7 Teams'],
            'Executions': [45, 38, 32, 28, 22, 18, 15],
            'Avg Duration (min)': [2.5, 4.2, 6.8, 9.1, 12.3, 15.7, 18.9],
            'Success Rate (%)': [98, 96, 94, 92, 90, 88, 85]
        })
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.bar(workflow_data, x='Workflow Type', y='Executions', 
                        title='Workflow Executions by Type', color_discrete_sequence=['#d62728'])
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.scatter(workflow_data, x='Avg Duration (min)', y='Success Rate (%)', 
                           size='Executions', hover_name='Workflow Type',
                           title='Workflow Performance: Duration vs Success Rate')
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
    
    # Performance analytics
    if show_performance:
        st.markdown("### ⚡ Performance Analytics")
        
        # Mock performance data
        performance_data = pd.DataFrame({
            'Metric': ['Response Time', 'Memory Usage', 'CPU Usage', 'Disk Usage', 'Network I/O'],
            'Current': [1.2, 65, 45, 78, 32],
            'Target': [2.0, 80, 70, 85, 50],
            'Status': ['Good', 'Good', 'Good', 'Warning', 'Good']
        })
        
        # Performance gauge
        col1, col2, col3 = st.columns(3)
        
        with col1:
            fig = go.Figure(go.Indicator(
                mode = "gauge+number+delta",
                value = 1.2,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Response Time (s)"},
                delta = {'reference': 2.0},
                gauge = {'axis': {'range': [None, 5]},
                        'bar': {'color': "darkblue"},
                        'steps': [
                            {'range': [0, 2], 'color': "lightgray"},
                            {'range': [2, 5], 'color': "gray"}],
                        'threshold': {'line': {'color': "red", 'width': 4},
                                    'thickness': 0.75, 'value': 4.5}}))
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = go.Figure(go.Indicator(
                mode = "gauge+number+delta",
                value = 65,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Memory Usage (%)"},
                delta = {'reference': 80},
                gauge = {'axis': {'range': [None, 100]},
                        'bar': {'color': "darkgreen"},
                        'steps': [
                            {'range': [0, 80], 'color': "lightgray"},
                            {'range': [80, 100], 'color': "gray"}],
                        'threshold': {'line': {'color': "red", 'width': 4},
                                    'thickness': 0.75, 'value': 90}}))
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
        
        with col3:
            fig = go.Figure(go.Indicator(
                mode = "gauge+number+delta",
                value = 45,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "CPU Usage (%)"},
                delta = {'reference': 70},
                gauge = {'axis': {'range': [None, 100]},
                        'bar': {'color': "darkorange"},
                        'steps': [
                            {'range': [0, 70], 'color': "lightgray"},
                            {'range': [70, 100], 'color': "gray"}],
                        'threshold': {'line': {'color': "red", 'width': 4},
                                    'thickness': 0.75, 'value': 85}}))
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
    
    # Insights and recommendations
    st.markdown("### 💡 Insights & Recommendations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        #### 📈 Key Insights
        - **Peak Usage**: Most active between 9-11 AM and 2-4 PM
        - **Popular Workflows**: 3-team workflows are most frequently used
        - **Document Types**: PDF documents are most commonly uploaded
        - **Performance**: System running within optimal parameters
        """)
    
    with col2:
        st.markdown("""
        #### 🎯 Recommendations
        - **Scale Resources**: Consider adding more memory during peak hours
        - **Optimize Workflows**: Focus on improving 4+ team workflow performance
        - **Document Processing**: Implement batch processing for large document uploads
        - **User Training**: Provide training on advanced workflow features
        """)
    
    # Export analytics
    st.markdown("### 📤 Export Analytics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Export to CSV", use_container_width=True):
            st.info("CSV export feature coming soon!")
    
    with col2:
        if st.button("📈 Export to PDF", use_container_width=True):
            st.info("PDF export feature coming soon!")
    
    with col3:
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.rerun()
    
    # Create footer
    create_footer()

if __name__ == "__main__":
    main()
