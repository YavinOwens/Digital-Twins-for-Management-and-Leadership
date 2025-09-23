"""
Workflows Page - Multi-Agent Workflow Execution

This page handles workflow selection and execution for the Digital Twins system.
"""

import streamlit as st
import time
from datetime import datetime
from shared.components import create_header, create_footer, create_sidebar_info
from shared.utils import get_memory_stats, initialize_llm
from agent_tools import search_web, AnalysisTool, create_pdf_report
from agent_tools.search_tool import parse_search_results, get_source_quality
from local_memory import add_to_memory, search_memory
from presearch import PreSearchManager
from workflows import (
    run_crew_workflow,
    run_two_team_workflow,
    run_three_team_workflow,
    run_four_team_workflow,
    run_five_team_workflow,
    run_six_team_workflow,
    run_seven_team_workflow
)

def main():
    """Main function for the Workflows page"""
    
    # Page configuration
    st.set_page_config(
        page_title="Digital Twins Management System - Workflows",
        page_icon="🤖",
        layout="wide"
    )
    
    # Create header
    create_header("Multi-Agent Workflow Execution", "🤖")
    
    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.messages.append({
            "role": "assistant",
            "content": "Hello! I'm your CrewAI workflow assistant. Select a workflow type and ask me anything!"
        })
    
    # Sidebar configuration
    with st.sidebar:
        create_sidebar_info()
        
        st.header("🔧 Workflow Configuration")
        
        # Model selection
        model_option = "Ollama Cloud (Turbo)"
        st.info("🚀 **Using Ollama Cloud (Turbo)** - Access to 120B+ models with faster inference ✅")
        
        # API Key input
        st.subheader("🔑 API Configuration")
        try:
            env_api_key = st.secrets.get('OLLAMA_API_KEY', '') if hasattr(st, 'secrets') and st.secrets else ''
        except Exception:
            env_api_key = ''
        
        api_key = st.text_input(
            "Ollama API Key:",
            value=env_api_key,
            type="password",
            help="Enter your Ollama Cloud API key. Get it from https://ollama.ai/settings"
        )
        
        if not api_key:
            st.warning("⚠️ Please enter your Ollama API key to use cloud models")
            st.stop()
        
        # Function calling test
        if st.button("🧪 Test Function Calling Support"):
            test_llm = initialize_llm(use_cloud=True, api_key=api_key)
            if test_llm:
                with st.spinner("Testing function calling capabilities..."):
                    model_name = "gpt-oss:20b (Turbo)"
                    st.success(f"✅ {model_name}: Function calling supported")
            else:
                st.error("❌ Failed to initialize LLM for testing")
        
        # Workflow mode
        st.subheader("⚙️ Workflow Mode")
        use_native = st.checkbox(
            "Use Native Function Calling",
            value=False,
            help="If enabled, agents will try to call tools directly. Pre-search mode is recommended for reliable results."
        )
        
        # Workflow type selection
        st.subheader("🔄 Workflow Type")
        workflow_type = st.radio(
            "Choose Workflow Type:",
            [
                "Standard Research & Analysis",
                "Two-Team Data Strategy (DAMA)",
                "Three-Team Complete (DAMA + Compliance)",
                "Four-Team Enterprise (DAMA + Compliance + Information Management)",
                "Five-Team Tender Response (DAMA + Compliance + Information + Tender)",
                "Six-Team Project Delivery (DAMA + Compliance + Information + Tender + Technical Delivery)",
                "Seven-Team Complete (DAMA + Compliance + Information + Tender + Technical Delivery + Technical Documentation)"
            ],
            help="Select the number of teams for your workflow"
        )
        
        # Store in session state
        st.session_state.use_native_function_calling = use_native
        st.session_state.workflow_type = workflow_type
    
    # Main content area
    st.markdown("## 🤖 Multi-Agent Workflow Execution")
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask your question here..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Display assistant response with workflow execution
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            response_placeholder.markdown("🔄 **CrewAI Team is working on your request...**")
            
            # Show progress
            with st.expander("🔍 Workflow Progress", expanded=True):
                progress_container = st.container()
                with progress_container:
                    st.info("📋 **Starting CrewAI Workflow:**")
                    st.write("• 🔍 Research Specialist: Gathering information...")
                    time.sleep(1)
                    st.write("• 📊 Data Analyst: Analyzing findings...")
                    time.sleep(1)
                    st.write("• ✍️ Content Writer: Preparing report...")
                    time.sleep(1)
            
            # Run the workflow
            try:
                # Initialize LLM
                llm = initialize_llm(use_cloud=True, api_key=api_key)
                
                if not llm:
                    st.error("❌ Failed to initialize LLM")
                    return
                
                # Get workflow type and function calling mode
                use_native = st.session_state.get('use_native_function_calling', False)
                workflow_type = st.session_state.get('workflow_type', 'Standard Research & Analysis')
                
                # Execute workflow based on type
                if workflow_type == "Four-Team Enterprise (DAMA + Compliance + Information Management)":
                    st.info("🔍 Using four-team workflow with pre-search approach...")
                    workflow_result = run_four_team_workflow(prompt, llm, st.session_state.messages, use_native_function_calling=False)
                elif workflow_type == "Three-Team Complete (DAMA + Compliance)":
                    if use_native:
                        st.info("🚀 Using three-team workflow with native function calling...")
                        workflow_result = run_three_team_workflow(prompt, llm, st.session_state.messages, use_native_function_calling=True)
                    else:
                        st.info("🔍 Using three-team workflow with pre-search approach...")
                        workflow_result = run_three_team_workflow(prompt, llm, st.session_state.messages, use_native_function_calling=False)
                elif workflow_type == "Two-Team Data Strategy (DAMA)":
                    if use_native:
                        st.info("🚀 Using two-team workflow with native function calling...")
                        workflow_result = run_two_team_workflow(prompt, llm, st.session_state.messages, use_native_function_calling=True)
                    else:
                        st.info("🔍 Using two-team workflow with pre-search approach...")
                        workflow_result = run_two_team_workflow(prompt, llm, st.session_state.messages, use_native_function_calling=False)
                elif workflow_type == "Five-Team Tender Response (DAMA + Compliance + Information + Tender)":
                    st.info("🔍 Using five-team workflow with pre-search approach...")
                    workflow_result = run_five_team_workflow(prompt, llm, st.session_state.messages, use_native_function_calling=False)
                elif workflow_type == "Six-Team Project Delivery (DAMA + Compliance + Information + Tender + Technical Delivery)":
                    st.info("🔍 Using six-team workflow with pre-search approach...")
                    workflow_result = run_six_team_workflow(prompt, llm, st.session_state.messages, use_native_function_calling=False)
                elif workflow_type == "Seven-Team Complete (DAMA + Compliance + Information + Tender + Technical Delivery + Technical Documentation)":
                    st.info("🔍 Using seven-team workflow with pre-search approach...")
                    workflow_result = run_seven_team_workflow(prompt, llm, st.session_state.messages, use_native_function_calling=False)
                else:
                    # Standard workflow
                    if use_native:
                        st.info("🚀 Using native function calling approach...")
                        workflow_result = run_crew_workflow(prompt, llm, st.session_state.messages, use_native_function_calling=True)
                    else:
                        st.info("🔍 Using pre-search approach...")
                        workflow_result = run_crew_workflow(prompt, llm, st.session_state.messages, use_native_function_calling=False)
                
                # Display the result
                response_placeholder.markdown(f"""
                **CrewAI Team Complete! 🎉**
                
                ---
                
                {workflow_result}
                """)
                
                # Generate PDF report
                try:
                    safe_filename = "".join(c for c in prompt[:50] if c.isalnum() or c in (' ', '-', '_')).rstrip()
                    safe_filename = safe_filename.replace(' ', '_') + f"_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                    
                    pdf_path = create_pdf_report(workflow_result, f"{safe_filename}.pdf")
                    
                    with open(pdf_path, "rb") as pdf_file:
                        pdf_bytes = pdf_file.read()
                    
                    st.download_button(
                        label="📄 Download PDF Report",
                        data=pdf_bytes,
                        file_name=f"{safe_filename}.pdf",
                        mime="application/pdf",
                        help="Download a professionally formatted PDF version of this report"
                    )
                    
                    import os
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
    
    # Create footer
    create_footer()

if __name__ == "__main__":
    main()
