import streamlit as st
import time
import os
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional
import json
from pathlib import Path

# Configure logging for better debugging
logging.basicConfig(level=logging.INFO)
from crewai import Agent, Task, Crew, Process
from crewai import LLM
from agent_tools.robust_llm_v2 import create_robust_llm
from crewai.tools import BaseTool
from crewai.tools import tool
from ddgs import DDGS
import ollama
from dotenv import load_dotenv

# Import tools from agent_tools package
from agent_tools import search_web, AnalysisTool, create_pdf_report
from agent_tools.search_tool import parse_search_results, get_source_quality

# Import agents from agent_teams package
from agent_teams.research_analysis import create_research_analysis_agents_with_context
from agent_teams.data_strategy import create_data_strategy_agents_with_context
from agent_teams.compliance_risk import create_compliance_risk_agents_with_context
from agent_teams.information_management import create_information_management_agents_with_context
from agent_teams.tender_response import create_tender_response_agents_with_context
from agent_teams.project_delivery import create_project_delivery_agents_with_context
from agent_teams.technical_documentation import create_technical_documentation_agents_with_context

# Import tasks from agent_teams package
from agent_teams.research_analysis import create_research_analysis_tasks_with_data
from agent_teams.data_strategy import create_data_strategy_tasks_with_data
from agent_teams.compliance_risk import create_compliance_risk_tasks_with_data
from agent_teams.information_management import create_information_management_tasks_with_data
from agent_teams.tender_response import create_tender_response_tasks_with_data
from agent_teams.project_delivery import create_project_delivery_tasks_with_data
from agent_teams.technical_documentation import create_technical_documentation_tasks_with_data

# Import test functions from agent_test_functions package
from agent_test_functions import test_function_calling_support, quick_test

# Import local memory management
from local_memory import add_to_memory, search_memory, get_memory_stats, clear_memory

# Import presearch functionality
from presearch import PreSearchManager

# Import workflow functions from workflows package
from workflows import (
    run_crew_workflow,
    run_two_team_workflow,
    run_three_team_workflow,
    run_four_team_workflow,
    run_five_team_workflow,
    run_six_team_workflow,
    run_seven_team_workflow,
    perform_workflow_presearch
)

# Import team output management
from team_outputs import TeamOutputManager

# Load environment variables
load_dotenv()


# Configure Streamlit page
st.set_page_config(
    page_title="CrewAI Workflow with Streamlit",
    page_icon="🤖",
    layout="wide"
)

# Initialize Ollama LLM for CrewAI (Original Working Configuration)
@st.cache_resource
def initialize_llm(use_cloud=False, api_key=None, _cache_key=None):
    """Initialize Ollama LLM with original working configuration"""
    try:
        print(f"🔧 Creating LLM: use_cloud={use_cloud}, api_key={'***' if api_key else None}")
        
        # Use RobustLLM v2 with built-in retry logic for rate limiting
        llm = create_robust_llm(use_cloud=use_cloud, api_key=api_key)
        
        print(f"✅ LLM created: {type(llm)}")
        return llm
    except Exception as e:
        print(f"❌ Failed to create LLM: {e}")
        if use_cloud:
            st.error(f"Failed to connect to Ollama Cloud. Please check your API key: {e}")
        else:
            st.error(f"Failed to connect to local Ollama. Please ensure Ollama is running and llama3.1:latest model is available: {e}")
        return None

# Tools are now imported from agent_tools package
# Agent definitions are now imported from agents package
# Task definitions are now imported from agent_tasks package
# Workflow functions are now imported from workflows package

def main():
    st.title("🤖 CrewAI Workflow Assistant")
    st.subheader("Powered by Ollama (Local & Cloud) and Streamlit")
    
    # Model selection in sidebar
    with st.sidebar:
        st.header("🔧 Model Configuration")
        
    # Model selection - Ollama Cloud (Turbo)
    model_option = "Ollama Cloud (Turbo)"
    
    # Check Ollama Cloud status
    try:
        import requests
        status_response = requests.get("https://ollama.com/api/tags", timeout=5)
        if status_response.status_code == 200:
            st.info("🚀 **Using Ollama Cloud (Turbo)** - Access to 120B+ models with faster inference ✅")
        else:
            st.warning("⚠️ **Ollama Cloud Status** - Service may be experiencing issues. Retry logic enabled.")
    except:
        st.warning("⚠️ **Ollama Cloud Status** - Unable to verify service status. Retry logic enabled.")
    
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
    
    # Function calling mode toggle
    st.subheader("⚙️ Workflow Mode")
    use_native = st.checkbox(
        "Use Native Function Calling",
        value=False,  # Always default to False (pre-search mode)
        help="If enabled, agents will try to call tools directly. If disabled, uses pre-search approach. Pre-search mode is recommended for reliable results."
    )
    
    # Four-team workflow option
    st.subheader("🔄 Workflow Type")
    workflow_type = st.radio(
        "Choose Workflow Type:",
        ["Standard Research & Analysis", "Two-Team Data Strategy (DAMA)", "Three-Team Complete (DAMA + Compliance)", "Four-Team Enterprise (DAMA + Compliance + Information Management)", "Five-Team Tender Response (DAMA + Compliance + Information + Tender)", "Six-Team Project Delivery (DAMA + Compliance + Information + Tender + Technical Delivery)", "Seven-Team Complete (DAMA + Compliance + Information + Tender + Technical Delivery + Technical Documentation)"],
        help="Standard: Research → Analysis → Writing. Two-Team: Research → Analysis → Writing → Data Strategy → DCAM Templates → Tranch Guidance. Three-Team: All above + Compliance → Risk Management → Audit & Governance. Four-Team: All above + Information Governance → Metadata Management → Data Quality. Five-Team: All above + Tender Analysis → Proposal Writing → Compliance Verification. Six-Team: All above + Data Engineering → Data Science → Data Architecture → DevOps → Project Management. Seven-Team: All above + Data Modeling → Python Code → SQL Code → PySpark Code → Technical Writing"
    )
    st.session_state.use_native_function_calling = use_native
    st.session_state.workflow_type = workflow_type
    
    if use_native:
        st.info("🚀 Native function calling mode - agents will call tools directly")
    else:
        st.info("🔍 Pre-search mode - data is searched first, then processed")

    # Initialize LLM - Ollama Cloud (Turbo)
    llm = initialize_llm(use_cloud=True, api_key=api_key, _cache_key=f"cloud_{api_key[:8] if api_key else 'none'}")
    
    # Debug: Check LLM initialization
    print(f"🔍 DEBUG: LLM initialized: {type(llm)}")
    if llm:
        print(f"🔍 DEBUG: LLM model: {getattr(llm, 'model', 'No model attr')}")
        print(f"🔍 DEBUG: LLM base_url: {getattr(llm, 'base_url', 'No base_url attr')}")
    else:
        print("🔍 DEBUG: LLM initialization failed!")
    
    if not llm:
        st.stop()
    
    # Initialize chat history and conversation memory
    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.messages.append({
            "role": "assistant",
            "content": "Hello! I'm your CrewAI workflow assistant with conversation memory. Ask me anything and I'll have my team of AI agents research, analyze, and provide you with comprehensive insights! I'll remember our conversation and build upon previous discussions."
        })
    
    # Initialize conversation topics tracking
    if "conversation_topics" not in st.session_state:
        st.session_state.conversation_topics = []
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask your question here..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Track conversation topics
        if len(prompt) > 10:  # Only track substantial questions
            st.session_state.conversation_topics.append(prompt[:50] + "...")
            # Keep only last 5 topics
            if len(st.session_state.conversation_topics) > 5:
                st.session_state.conversation_topics = st.session_state.conversation_topics[-5:]
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Display assistant response with workflow execution
        with st.chat_message("assistant"):
            # Create a placeholder for streaming response
            response_placeholder = st.empty()
            
            # Show working message
            response_placeholder.markdown("🔄 **CrewAI Team is working on your request...**")
            
            # Add progress information
            with st.expander("🔍 Workflow Progress", expanded=True):
                progress_container = st.container()
                
                with progress_container:
                    st.info("📋 **Starting CrewAI Workflow:**")
                    st.write("• 🔍 Research Specialist: Gathering information...")
                    time.sleep(1)  # Simulate processing time
                    
                    st.write("• 📊 Data Analyst: Analyzing findings...")
                    time.sleep(1)
                    
                    st.write("• ✍️ Content Writer: Preparing report...")
                    time.sleep(1)
            
            # Run the actual CrewAI workflow with conversation context
            try:
                # Check workflow type and function calling mode
                use_native = st.session_state.get('use_native_function_calling', False)
                workflow_type = st.session_state.get('workflow_type', 'Standard Research & Analysis')
                
                
                if workflow_type == "Four-Team Enterprise (DAMA + Compliance + Information Management)":
                    # Four-team workflow - always use pre-search approach for reliability
                    st.info("🔍 Using four-team workflow with pre-search approach (most reliable)...")
                    workflow_result = run_four_team_workflow(prompt, llm, st.session_state.messages, use_native_function_calling=False)
                elif workflow_type == "Three-Team Complete (DAMA + Compliance)":
                    # Three-team workflow
                    if use_native:
                        st.info("🚀 Using three-team workflow with native function calling...")
                        workflow_result = run_three_team_workflow(prompt, llm, st.session_state.messages, use_native_function_calling=True)
                    else:
                        st.info("🔍 Using three-team workflow with pre-search approach...")
                        workflow_result = run_three_team_workflow(prompt, llm, st.session_state.messages, use_native_function_calling=False)
                elif workflow_type == "Two-Team Data Strategy (DAMA)":
                    # Two-team workflow
                    if use_native:
                        st.info("🚀 Using two-team workflow with native function calling...")
                        workflow_result = run_two_team_workflow(prompt, llm, st.session_state.messages, use_native_function_calling=True)
                    else:
                        st.info("🔍 Using two-team workflow with pre-search approach...")
                        workflow_result = run_two_team_workflow(prompt, llm, st.session_state.messages, use_native_function_calling=False)
                elif workflow_type == "Five-Team Tender Response (DAMA + Compliance + Information + Tender)":
                    # Five-team workflow - always use pre-search approach for reliability
                    st.info("🔍 Using five-team workflow with pre-search approach (most reliable)...")
                    workflow_result = run_five_team_workflow(prompt, llm, st.session_state.messages, use_native_function_calling=False)
                elif workflow_type == "Six-Team Project Delivery (DAMA + Compliance + Information + Tender + Technical Delivery)":
                    # Six-team workflow - always use pre-search approach for reliability
                    st.info("🔍 Using six-team workflow with pre-search approach (most reliable)...")
                    # Debug: Check LLM before passing to workflow
                    print(f"🔍 DEBUG: LLM being passed to workflow: {type(llm)}")
                    if llm:
                        print(f"🔍 DEBUG: LLM model: {getattr(llm, 'model', 'No model attr')}")
                        print(f"🔍 DEBUG: LLM base_url: {getattr(llm, 'base_url', 'No base_url attr')}")
                    else:
                        print("🔍 DEBUG: LLM is None!")
                    workflow_result = run_six_team_workflow(prompt, llm, st.session_state.messages, use_native_function_calling=False)
                elif workflow_type == "Seven-Team Complete (DAMA + Compliance + Information + Tender + Technical Delivery + Technical Documentation)":
                    # Seven-team workflow - always use pre-search approach for reliability
                    st.info("🔍 Using seven-team workflow with pre-search approach (most reliable)...")
                    workflow_result = run_seven_team_workflow(prompt, llm, st.session_state.messages, use_native_function_calling=False)
                elif use_native:
                    # Try native function calling approach (standard workflow)
                    st.info("🚀 Using native function calling approach...")
                    workflow_result = run_crew_workflow(prompt, llm, st.session_state.messages, use_native_function_calling=True)
                else:
                    # Use pre-search approach with visualization
                    st.info("🔍 Using pre-search approach with enhanced visualization...")
                    
                    # Pre-search to get structured data for visualization
                    search_data = search_web.run(prompt)
                    parsed_search = parse_search_results(search_data)
                    
                    # Display search results visualization
                    with st.expander("🔍 Search Results Analysis", expanded=True):
                        col1, col2, col3, col4 = st.columns(4)
                        
                        with col1:
                            st.metric("Sources Found", parsed_search['total_sources'])
                        with col2:
                            avg_quality = sum(s['quality_score'] for s in parsed_search['sources']) / max(len(parsed_search['sources']), 1)
                            st.metric("Avg Quality", f"{avg_quality:.1f}/10")
                        with col3:
                            domains = set(s['domain'] for s in parsed_search['sources'])
                            st.metric("Unique Domains", len(domains))
                        with col4:
                            total_chars = sum(len(s['content']) for s in parsed_search['sources'])
                            st.metric("Content Length", f"{total_chars:,} chars")
                        
                        # Source quality indicators
                        st.subheader("📊 Source Quality Analysis")
                        for i, source in enumerate(parsed_search['sources'], 1):
                            with st.container():
                                col1, col2, col3 = st.columns([3, 1, 1])
                                
                                with col1:
                                    st.write(f"**{i}. {source['title']}**")
                                    st.write(f"🌐 {source['domain']} | {source['organization']}")
                                    st.write(f"📝 {source['content'][:150]}...")
                                    if source['url'] != 'No URL':
                                        st.write(f"🔗 [View Source]({source['url']})")
                                
                                with col2:
                                    # Quality score visualization
                                    quality_color = "green" if source['quality_score'] >= 7 else "orange" if source['quality_score'] >= 5 else "red"
                                    st.markdown(f"**Quality:** :{quality_color}[{source['quality_score']}/10]")
                                
                                with col3:
                                    # Quality indicators
                                    if source['quality_score'] >= 8:
                                        st.success("🏆 High Quality")
                                    elif source['quality_score'] >= 6:
                                        st.info("✅ Good Quality")
                                    else:
                                        st.warning("⚠️ Basic Quality")
                                
                                st.divider()
                        
                        # References section
                        if parsed_search['references']:
                            st.subheader("📚 References (Harvard Style)")
                            for i, ref in enumerate(parsed_search['references'], 1):
                                st.write(f"{i}. {ref}")
                    
                    # Run the full workflow
                    workflow_result = run_crew_workflow(prompt, llm, st.session_state.messages, use_native_function_calling=False)
                
                # Display the final result
                response_placeholder.markdown(f"""
                **CrewAI Team Complete! 🎉**
                
                ---
                
                {workflow_result}
                """)
                
                # Generate PDF report
                try:
                    # Create a clean filename based on the query
                    safe_filename = "".join(c for c in prompt[:50] if c.isalnum() or c in (' ', '-', '_')).rstrip()
                    safe_filename = safe_filename.replace(' ', '_') + f"_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                    
                    # Generate PDF
                    pdf_path = create_pdf_report(workflow_result, f"{safe_filename}.pdf")
                    
                    # Read the PDF file for download
                    with open(pdf_path, "rb") as pdf_file:
                        pdf_bytes = pdf_file.read()
                    
                    # Add download button
                    st.download_button(
                        label="📄 Download PDF Report",
                        data=pdf_bytes,
                        file_name=f"{safe_filename}.pdf",
                        mime="application/pdf",
                        help="Download a professionally formatted PDF version of this report"
                    )
                    
                    # Clean up the temporary file
                    os.remove(pdf_path)
                    
                except Exception as pdf_error:
                    st.warning(f"⚠️ PDF generation failed: {pdf_error}")
                
                # Add to chat history
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": f"**CrewAI Team Complete! 🎉**\n\n---\n\n{workflow_result}"
                })
                
            except Exception as e:
                error_message = f"❌ **Error occurred:** {str(e)}"
                response_placeholder.markdown(error_message)
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": error_message
                })
    
    # Sidebar with information
    with st.sidebar:
        st.header("🛠️ System Info")
        
        # Show workflow info based on selected type
        workflow_type = st.session_state.get('workflow_type', 'Standard Research & Analysis')
        
        if workflow_type == "Four-Team Enterprise (DAMA + Compliance + Information Management)":
            st.info("""
            **Four-Team CrewAI Workflow:**
            
            **Team 1 - Research & Analysis:**
            - 🔍 **Research Specialist**: Conducts web research, gathers current information, and provides comprehensive data on the topic
            - 📊 **Data Analyst**: Analyzes research findings, identifies patterns, and provides data-driven insights
            - ✍️ **Content Writer**: Creates well-structured reports, summaries, and actionable recommendations
            
            **Team 2 - Data Strategy:**
            - 🏛️ **Data Governance Specialist**: Creates DAMA-DMBOK frameworks, data policies, and governance structures
            - 📋 **DCAM Template Specialist**: Develops Data Capability Assessment Model templates and maturity frameworks
            - 🗓️ **Tranch Guidance Specialist**: Designs phased implementation roadmaps and delivery tranches
            
            **Team 3 - Compliance & Risk:**
            - ⚖️ **Compliance Specialist**: Ensures regulatory compliance (GDPR, CCPA, SOX, HIPAA, FERPA) and creates compliance frameworks
            - 🛡️ **Risk Management Specialist**: Conducts risk assessments, creates mitigation strategies, and business continuity plans
            - 🔍 **Audit & Governance Specialist**: Designs audit frameworks, oversight procedures, and governance controls
            
            **Team 4 - Information Management:**
            - 📋 **Information Governance Specialist**: Manages information lifecycle, classification, retention, and disposal policies
            - 🏷️ **Metadata Management Specialist**: Creates metadata frameworks, data cataloging, and lineage tracking systems
            - ✅ **Data Quality Specialist**: Establishes data quality standards, monitoring, and remediation frameworks
            
            **Model:** Ollama Cloud (Turbo)
            """)
        elif workflow_type == "Three-Team Complete (DAMA + Compliance)":
            st.info("""
            **Three-Team CrewAI Workflow:**
            
            **Team 1 - Research & Analysis:**
            - 🔍 **Research Specialist**: Conducts web research, gathers current information, and provides comprehensive data on the topic
            - 📊 **Data Analyst**: Analyzes research findings, identifies patterns, and provides data-driven insights
            - ✍️ **Content Writer**: Creates well-structured reports, summaries, and actionable recommendations
            
            **Team 2 - Data Strategy:**
            - 🏛️ **Data Governance Specialist**: Creates DAMA-DMBOK frameworks, data policies, and governance structures
            - 📋 **DCAM Template Specialist**: Develops Data Capability Assessment Model templates and maturity frameworks
            - 🗓️ **Tranch Guidance Specialist**: Designs phased implementation roadmaps and delivery tranches
            
            **Team 3 - Compliance & Risk:**
            - ⚖️ **Compliance Specialist**: Ensures regulatory compliance (GDPR, CCPA, SOX, HIPAA, FERPA) and creates compliance frameworks
            - 🛡️ **Risk Management Specialist**: Conducts risk assessments, creates mitigation strategies, and business continuity plans
            - 🔍 **Audit & Governance Specialist**: Designs audit frameworks, oversight procedures, and governance controls
            
            **Model:** Ollama Cloud (Turbo)
            """)
        elif workflow_type == "Two-Team Data Strategy (DAMA)":
            st.info("""
            **Two-Team CrewAI Workflow:**
            
            **Team 1 - Research & Analysis:**
            - 🔍 **Research Specialist**: Conducts web research, gathers current information, and provides comprehensive data on the topic
            - 📊 **Data Analyst**: Analyzes research findings, identifies patterns, and provides data-driven insights
            - ✍️ **Content Writer**: Creates well-structured reports, summaries, and actionable recommendations
            
            **Team 2 - Data Strategy:**
            - 🏛️ **Data Governance Specialist**: Creates DAMA-DMBOK frameworks, data policies, and governance structures
            - 📋 **DCAM Template Specialist**: Develops Data Capability Assessment Model templates and maturity frameworks
            - 🗓️ **Tranch Guidance Specialist**: Designs phased implementation roadmaps and delivery tranches
            
            **Model:** Ollama Cloud (Turbo)
            """)
        elif workflow_type == "Five-Team Tender Response (DAMA + Compliance + Information + Tender)":
            st.info("""
            **Five-Team CrewAI Workflow:**
            
            **Team 1 - Research & Analysis:**
            - 🔍 **Research Specialist**: Conducts web research, gathers current information, and provides comprehensive data on the topic
            - 📊 **Data Analyst**: Analyzes research findings, identifies patterns, and provides data-driven insights
            - ✍️ **Content Writer**: Creates well-structured reports, summaries, and actionable recommendations
            
            **Team 2 - Data Strategy:**
            - 🏛️ **Data Governance Specialist**: Creates DAMA-DMBOK frameworks, data policies, and governance structures
            - 📋 **DCAM Template Specialist**: Develops Data Capability Assessment Model templates and maturity frameworks
            - 🗓️ **Tranch Guidance Specialist**: Designs phased implementation roadmaps and delivery tranches
            
            **Team 3 - Compliance & Risk:**
            - ⚖️ **Compliance Specialist**: Ensures regulatory compliance (GDPR, CCPA, SOX, HIPAA, FERPA) and creates compliance frameworks
            - 🛡️ **Risk Management Specialist**: Conducts risk assessments, creates mitigation strategies, and business continuity plans
            - 🔍 **Audit & Governance Specialist**: Designs audit frameworks, oversight procedures, and governance controls
            
            **Team 4 - Information Management:**
            - 📋 **Information Governance Specialist**: Manages information lifecycle, classification, retention, and disposal policies
            - 🏷️ **Metadata Management Specialist**: Creates metadata frameworks, data cataloging, and lineage tracking systems
            - ✅ **Data Quality Specialist**: Establishes data quality standards, monitoring, and remediation frameworks
            
            **Team 5 - Tender Response:**
            - 📝 **Tender Response Specialist**: Analyzes tender requirements, creates response strategies, and competitive positioning
            - ✍️ **Proposal Writer**: Creates compelling tender responses, technical specifications, and value propositions
            - ✅ **Compliance Expert**: Ensures tender compliance with procurement regulations and evaluation criteria
            
            **Model:** Ollama Cloud (Turbo)
            """)
        elif workflow_type == "Six-Team Project Delivery (DAMA + Compliance + Information + Tender + Technical Delivery)":
            st.info("""
            **Six-Team CrewAI Workflow:**
            
            **Team 1 - Research & Analysis:**
            - 🔍 **Research Specialist**: Conducts web research, gathers current information, and provides comprehensive data on the topic
            - 📊 **Data Analyst**: Analyzes research findings, identifies patterns, and provides data-driven insights
            - ✍️ **Content Writer**: Creates well-structured reports, summaries, and actionable recommendations
            
            **Team 2 - Data Strategy:**
            - 🏛️ **Data Governance Specialist**: Creates DAMA-DMBOK frameworks, data policies, and governance structures
            - 📋 **DCAM Template Specialist**: Develops Data Capability Assessment Model templates and maturity frameworks
            - 🗓️ **Tranch Guidance Specialist**: Designs phased implementation roadmaps and delivery tranches
            
            **Team 3 - Compliance & Risk:**
            - ⚖️ **Compliance Specialist**: Ensures regulatory compliance (GDPR, CCPA, SOX, HIPAA, FERPA) and creates compliance frameworks
            - 🛡️ **Risk Management Specialist**: Conducts risk assessments, creates mitigation strategies, and business continuity plans
            - 🔍 **Audit & Governance Specialist**: Designs audit frameworks, oversight procedures, and governance controls
            
            **Team 4 - Information Management:**
            - 📋 **Information Governance Specialist**: Manages information lifecycle, classification, retention, and disposal policies
            - 🏷️ **Metadata Management Specialist**: Creates metadata frameworks, data cataloging, and lineage tracking systems
            - ✅ **Data Quality Specialist**: Establishes data quality standards, monitoring, and remediation frameworks
            
            **Team 5 - Tender Response:**
            - 📝 **Tender Response Specialist**: Analyzes tender requirements, creates response strategies, and competitive positioning
            - ✍️ **Proposal Writer**: Creates compelling tender responses, technical specifications, and value propositions
            - ✅ **Compliance Expert**: Ensures tender compliance with procurement regulations and evaluation criteria
            
            **Team 6 - Project Delivery:**
            - 🔧 **Data Engineer**: Designs data pipelines, ETL processes, and data infrastructure for digital twin systems
            - 🧠 **Data Scientist**: Develops analytics models, machine learning algorithms, and predictive analytics
            - 🏗️ **Data Architect**: Designs comprehensive data architectures, data models, and integration strategies
            - ⚙️ **DevOps Engineer**: Implements CI/CD pipelines, infrastructure automation, and operational monitoring
            - 📋 **Project Manager**: Coordinates technical delivery, manages resources, and ensures successful implementation
            
            **Model:** Ollama Cloud (Turbo)
            """)
        elif workflow_type == "Seven-Team Complete (DAMA + Compliance + Information + Tender + Technical Delivery + Technical Documentation)":
            st.info("""
            **Seven-Team CrewAI Workflow:**
            
            **Team 1 - Research & Analysis:**
            - 🔍 **Research Specialist**: Conducts web research, gathers current information, and provides comprehensive data on the topic
            - 📊 **Data Analyst**: Analyzes research findings, identifies patterns, and provides data-driven insights
            - ✍️ **Content Writer**: Creates well-structured reports, summaries, and actionable recommendations
            
            **Team 2 - Data Strategy:**
            - 🏛️ **Data Governance Specialist**: Creates DAMA-DMBOK frameworks, data policies, and governance structures
            - 📋 **DCAM Template Specialist**: Develops Data Capability Assessment Model templates and maturity frameworks
            - 🗓️ **Tranch Guidance Specialist**: Designs phased implementation roadmaps and delivery tranches
            
            **Team 3 - Compliance & Risk:**
            - ⚖️ **Compliance Specialist**: Ensures regulatory compliance (GDPR, CCPA, SOX, HIPAA, FERPA) and creates compliance frameworks
            - 🛡️ **Risk Management Specialist**: Conducts risk assessments, creates mitigation strategies, and business continuity plans
            - 🔍 **Audit & Governance Specialist**: Designs audit frameworks, oversight procedures, and governance controls
            
            **Team 4 - Information Management:**
            - 📋 **Information Governance Specialist**: Manages information lifecycle, classification, retention, and disposal policies
            - 🏷️ **Metadata Management Specialist**: Creates metadata frameworks, data cataloging, and lineage tracking systems
            - ✅ **Data Quality Specialist**: Establishes data quality standards, monitoring, and remediation frameworks
            
            **Team 5 - Tender Response:**
            - 📝 **Tender Response Specialist**: Analyzes tender requirements, creates response strategies, and competitive positioning
            - ✍️ **Proposal Writer**: Creates compelling tender responses, technical specifications, and value propositions
            - ✅ **Compliance Expert**: Ensures tender compliance with procurement regulations and evaluation criteria
            
            **Team 6 - Project Delivery:**
            - 🔧 **Data Engineer**: Designs data pipelines, ETL processes, and data infrastructure for digital twin systems
            - 🧠 **Data Scientist**: Develops analytics models, machine learning algorithms, and predictive analytics
            - 🏗️ **Data Architect**: Designs comprehensive data architectures, data models, and integration strategies
            - ⚙️ **DevOps Engineer**: Implements CI/CD pipelines, infrastructure automation, and operational monitoring
            - 📋 **Project Manager**: Coordinates technical delivery, manages resources, and ensures successful implementation
            
            **Team 7 - Technical Documentation:**
            - 📊 **Data Modeling Specialist**: Creates data models, ER diagrams, and data architecture visualizations
            - 🐍 **Python Code Specialist**: Generates Python code, scripts, and data processing pipelines
            - 🗃️ **SQL Code Specialist**: Creates SQL queries, database schemas, and data manipulation scripts
            - ⚡ **PySpark Code Specialist**: Develops PySpark code for big data processing and distributed computing
            - 📝 **Technical Writer**: Creates comprehensive technical documentation, API docs, and implementation guides
            
            **Model:** Ollama Cloud (Turbo)
            """)
        else:
            st.info("""
            **Standard CrewAI Workflow:**
            
            **Team 1 - Research & Analysis:**
            - 🔍 **Research Specialist**: Conducts web research, gathers current information, and provides comprehensive data on the topic
            - 📊 **Data Analyst**: Analyzes research findings, identifies patterns, and provides data-driven insights
            - ✍️ **Content Writer**: Creates well-structured reports, summaries, and actionable recommendations
            
            **Model:** Ollama Cloud (Turbo)
            """)
        
        st.header("🎯 How it works")
        
        # Show workflow steps based on selected type
        workflow_type = st.session_state.get('workflow_type', 'Standard Research & Analysis')
        
        if workflow_type == "Four-Team Enterprise (DAMA + Compliance + Information Management)":
            st.markdown("""
            **Four-Team Workflow:**
            
            **Team 1 - Research & Analysis:**
            1. **Research Agent** gathers information
            2. **Analyst Agent** processes findings
            3. **Writer Agent** creates initial report
            
            **Team 2 - Data Strategy:**
            4. **Governance Agent** creates DAMA framework
            5. **DCAM Agent** develops capability templates
            6. **Tranch Agent** designs implementation phases
            
            **Team 3 - Compliance & Risk:**
            7. **Compliance Agent** ensures regulatory compliance
            8. **Risk Agent** conducts risk assessments
            9. **Audit Agent** designs governance oversight
            
            **Team 4 - Information Management:**
            10. **Information Governance Agent** manages information lifecycle
            11. **Metadata Agent** creates metadata frameworks
            12. **Data Quality Agent** ensures data quality standards
            13. **Combined results** appear in chat interface
            """)
        elif workflow_type == "Three-Team Complete (DAMA + Compliance)":
            st.markdown("""
            **Three-Team Workflow:**
            
            **Team 1 - Research & Analysis:**
            1. **Research Agent** gathers information
            2. **Analyst Agent** processes findings
            3. **Writer Agent** creates initial report
            
            **Team 2 - Data Strategy:**
            4. **Governance Agent** creates DAMA framework
            5. **DCAM Agent** develops capability templates
            6. **Tranch Agent** designs implementation phases
            
            **Team 3 - Compliance & Risk:**
            7. **Compliance Agent** ensures regulatory compliance
            8. **Risk Agent** conducts risk assessments
            9. **Audit Agent** designs governance oversight
            10. **Combined results** appear in chat interface
            """)
        elif workflow_type == "Two-Team Data Strategy (DAMA)":
            st.markdown("""
            **Two-Team Workflow:**
            
            **Team 1 - Research & Analysis:**
            1. **Research Agent** gathers information
            2. **Analyst Agent** processes findings
            3. **Writer Agent** creates initial report
            
            **Team 2 - Data Strategy:**
            4. **Governance Agent** creates DAMA framework
            5. **DCAM Agent** develops capability templates
            6. **Tranch Agent** designs implementation phases
            7. **Combined results** appear in chat interface
            """)
        elif workflow_type == "Five-Team Tender Response (DAMA + Compliance + Information + Tender)":
            st.markdown("""
            **Five-Team Workflow:**
            
            **Team 1 - Research & Analysis:**
            1. **Research Agent** gathers information
            2. **Analyst Agent** processes findings
            3. **Writer Agent** creates initial report
            
            **Team 2 - Data Strategy:**
            4. **Governance Agent** creates DAMA framework
            5. **DCAM Agent** develops capability templates
            6. **Tranch Agent** designs implementation phases
            
            **Team 3 - Compliance & Risk:**
            7. **Compliance Agent** ensures regulatory compliance
            8. **Risk Agent** conducts risk assessments
            9. **Audit Agent** designs governance oversight
            
            **Team 4 - Information Management:**
            10. **Information Governance Agent** manages information lifecycle
            11. **Metadata Agent** creates metadata frameworks
            12. **Data Quality Agent** ensures data quality standards
            
            **Team 5 - Tender Response:**
            13. **Tender Specialist** analyzes requirements
            14. **Proposal Writer** creates compelling responses
            15. **Compliance Expert** verifies compliance
            16. **Combined results** appear in chat interface
            """)
        elif workflow_type == "Six-Team Project Delivery (DAMA + Compliance + Information + Tender + Technical Delivery)":
            st.markdown("""
            **Six-Team Workflow:**
            
            **Team 1 - Research & Analysis:**
            1. **Research Agent** gathers information
            2. **Analyst Agent** processes findings
            3. **Writer Agent** creates initial report
            
            **Team 2 - Data Strategy:**
            4. **Governance Agent** creates DAMA framework
            5. **DCAM Agent** develops capability templates
            6. **Tranch Agent** designs implementation phases
            
            **Team 3 - Compliance & Risk:**
            7. **Compliance Agent** ensures regulatory compliance
            8. **Risk Agent** conducts risk assessments
            9. **Audit Agent** designs governance oversight
            
            **Team 4 - Information Management:**
            10. **Information Governance Agent** manages information lifecycle
            11. **Metadata Agent** creates metadata frameworks
            12. **Data Quality Agent** ensures data quality standards
            
            **Team 5 - Tender Response:**
            13. **Tender Specialist** analyzes requirements
            14. **Proposal Writer** creates compelling responses
            15. **Compliance Expert** verifies compliance
            
            **Team 6 - Project Delivery:**
            16. **Data Engineer** designs data infrastructure
            17. **Data Scientist** develops analytics models
            18. **Data Architect** creates system architecture
            19. **DevOps Engineer** implements deployment
            20. **Project Manager** coordinates delivery
            21. **Combined results** appear in chat interface
            """)
        elif workflow_type == "Seven-Team Complete (DAMA + Compliance + Information + Tender + Technical Delivery + Technical Documentation)":
            st.markdown("""
            **Seven-Team Workflow:**
            
            **Team 1 - Research & Analysis:**
            1. **Research Agent** gathers information
            2. **Analyst Agent** processes findings
            3. **Writer Agent** creates initial report
            
            **Team 2 - Data Strategy:**
            4. **Governance Agent** creates DAMA framework
            5. **DCAM Agent** develops capability templates
            6. **Tranch Agent** designs implementation phases
            
            **Team 3 - Compliance & Risk:**
            7. **Compliance Agent** ensures regulatory compliance
            8. **Risk Agent** conducts risk assessments
            9. **Audit Agent** designs governance oversight
            
            **Team 4 - Information Management:**
            10. **Information Governance Agent** manages information lifecycle
            11. **Metadata Agent** creates metadata frameworks
            12. **Data Quality Agent** ensures data quality standards
            
            **Team 5 - Tender Response:**
            13. **Tender Specialist** analyzes requirements
            14. **Proposal Writer** creates compelling responses
            15. **Compliance Expert** verifies compliance
            
            **Team 6 - Project Delivery:**
            16. **Data Engineer** designs data infrastructure
            17. **Data Scientist** develops analytics models
            18. **Data Architect** creates system architecture
            19. **DevOps Engineer** implements deployment
            20. **Project Manager** coordinates delivery
            
            **Team 7 - Technical Documentation:**
            21. **Data Modeling Specialist** creates diagrams and data models
            22. **Python Code Specialist** generates Python scripts and pipelines
            23. **SQL Code Specialist** creates database schemas and queries
            24. **PySpark Code Specialist** develops big data processing code
            25. **Technical Writer** creates comprehensive documentation
            26. **Combined results** appear in chat interface
            """)
        else:
            st.markdown("""
            **Standard Workflow:**
            1. **Ask a question** in the chat
            2. **Research Agent** gathers information
            3. **Analyst Agent** processes findings
            4. **Writer Agent** creates final report
            5. **Results** appear in chat interface
            """)
        
        # Memory statistics
        try:
            memory_stats = get_memory_stats()
            st.header("🧠 Memory Stats")
            st.metric("Stored Conversations", memory_stats["total_conversations"])
            st.caption(f"Database: {memory_stats['persist_directory']}")
        except Exception as e:
            st.warning(f"Memory stats unavailable: {e}")
        
        if st.button("🗑️ Clear Chat"):
            st.session_state.messages = []
            st.session_state.conversation_topics = []
            st.session_state.messages.append({
                "role": "assistant",
                "content": "Chat cleared! Ask me anything and I'll have my team get to work! I'll remember our conversation as we go."
            })
            st.rerun()
        
        if st.button("🧠 Clear Memory"):
            try:
                clear_memory()
                st.success("Memory cleared!")
                st.rerun()
            except Exception as e:
                st.error(f"Failed to clear memory: {e}")
        
        # Show conversation topics if any
        if st.session_state.conversation_topics:
            st.header("💭 Conversation Topics")
            for i, topic in enumerate(st.session_state.conversation_topics, 1):
                st.write(f"{i}. {topic}")
        
        # Search analytics section
        st.header("📊 Search Analytics")
        st.markdown("""
        **Quality Scoring:**
        - 🏆 High (8-10): Academic, gov, edu domains
        - ✅ Good (6-7): Reputable .com, .org sites  
        - ⚠️ Basic (5-6): General web sources
        
        **Source Types:**
        - Educational institutions (.edu)
        - Government (.gov)
        - Organizations (.org)
        - Commercial (.com, .net)
        """)
        
        # Add search tips
        st.header("💡 Search Tips")
        st.markdown("""
        - Ask specific questions for better results
        - Include industry or domain context
        - Use keywords like "benefits", "challenges", "trends"
        - Be specific about timeframes (e.g., "2024 trends")
        """)

if __name__ == "__main__":
    main()
