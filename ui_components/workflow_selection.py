"""
Workflow Selection UI Components

This module contains workflow type selection UI components.
"""

import streamlit as st


def create_workflow_selection_ui():
    """Create the workflow type selection UI"""
    st.subheader("🔄 Workflow Type")
    
    workflow_options = [
        "Standard Research & Analysis",
        "Two-Team Data Strategy (DAMA)",
        "Three-Team Complete (DAMA + Compliance)",
        "Four-Team Enterprise (DAMA + Compliance + Information Management)",
        "Five-Team Tender Response (DAMA + Compliance + Information + Tender)",
        "Six-Team Project Delivery (DAMA + Compliance + Information + Tender + Technical Delivery)",
        "Seven-Team Complete (DAMA + Compliance + Information + Tender + Technical Delivery + Technical Documentation)"
    ]
    
    workflow_descriptions = {
        "Standard Research & Analysis": "Research → Analysis → Writing",
        "Two-Team Data Strategy (DAMA)": "Research → Analysis → Writing → Data Strategy → DCAM Templates → Tranch Guidance",
        "Three-Team Complete (DAMA + Compliance)": "All above + Compliance → Risk Management → Audit & Governance",
        "Four-Team Enterprise (DAMA + Compliance + Information Management)": "All above + Information Governance → Metadata Management → Data Quality",
        "Five-Team Tender Response (DAMA + Compliance + Information + Tender)": "All above + Tender Analysis → Proposal Writing → Compliance Verification",
        "Six-Team Project Delivery (DAMA + Compliance + Information + Tender + Technical Delivery)": "All above + Data Engineering → Data Science → Data Architecture → DevOps → Project Management",
        "Seven-Team Complete (DAMA + Compliance + Information + Tender + Technical Delivery + Technical Documentation)": "All above + Data Modeling → Python Code → SQL Code → PySpark Code → Technical Writing"
    }
    
    workflow_type = st.radio(
        "Choose Workflow Type:",
        workflow_options,
        help="Select the workflow type based on your needs. More teams provide more comprehensive analysis but take longer to execute."
    )
    
    # Display workflow description
    if workflow_type in workflow_descriptions:
        st.info(f"**Selected Workflow**: {workflow_descriptions[workflow_type]}")
    
    return workflow_type


def create_workflow_info_sidebar():
    """Create workflow information for the sidebar"""
    st.header("ℹ️ Workflow Information")
    
    workflow_info = {
        "Standard Research & Analysis": {
            "teams": 1,
            "agents": ["Research Specialist", "Data Analyst", "Content Writer"],
            "description": "Basic research and analysis workflow"
        },
        "Two-Team Data Strategy (DAMA)": {
            "teams": 2,
            "agents": ["Research Team", "Data Strategy Team"],
            "description": "Includes DAMA-DMBOK frameworks and data governance"
        },
        "Three-Team Complete (DAMA + Compliance)": {
            "teams": 3,
            "agents": ["Research Team", "Data Strategy Team", "Compliance & Risk Team"],
            "description": "Adds compliance, risk management, and audit capabilities"
        },
        "Four-Team Enterprise (DAMA + Compliance + Information Management)": {
            "teams": 4,
            "agents": ["Research Team", "Data Strategy Team", "Compliance & Risk Team", "Information Management Team"],
            "description": "Includes information governance and metadata management"
        },
        "Five-Team Tender Response (DAMA + Compliance + Information + Tender)": {
            "teams": 5,
            "agents": ["Research Team", "Data Strategy Team", "Compliance & Risk Team", "Information Management Team", "Tender Response Team"],
            "description": "Adds tender analysis and proposal writing capabilities"
        },
        "Six-Team Project Delivery (DAMA + Compliance + Information + Tender + Technical Delivery)": {
            "teams": 6,
            "agents": ["Research Team", "Data Strategy Team", "Compliance & Risk Team", "Information Management Team", "Tender Response Team", "Project Delivery Team"],
            "description": "Includes technical delivery and project management"
        },
        "Seven-Team Complete (DAMA + Compliance + Information + Tender + Technical Delivery + Technical Documentation)": {
            "teams": 7,
            "agents": ["Research Team", "Data Strategy Team", "Compliance & Risk Team", "Information Management Team", "Tender Response Team", "Project Delivery Team", "Technical Documentation Team"],
            "description": "Complete workflow with technical documentation and code generation"
        }
    }
    
    # Display current workflow info
    if hasattr(st.session_state, 'workflow_type') and st.session_state.workflow_type in workflow_info:
        info = workflow_info[st.session_state.workflow_type]
        st.metric("Teams", info['teams'])
        st.metric("Total Agents", len(info['agents']))
        st.info(f"**Description**: {info['description']}")
        
        with st.expander("View Team Composition"):
            for i, agent in enumerate(info['agents'], 1):
                st.write(f"**Team {i}**: {agent}")
    
    return workflow_info
