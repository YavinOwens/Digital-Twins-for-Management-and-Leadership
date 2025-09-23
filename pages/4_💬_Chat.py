"""
Chat Page - Conversational Interface

This page provides a clean chat interface for interacting with the Digital Twins system.
"""

import streamlit as st
import time
from datetime import datetime
from shared.components import create_header, create_footer, create_sidebar_info
from shared.utils import get_memory_stats, initialize_llm
from local_memory import add_to_memory, search_memory, clear_memory
from presearch import PreSearchManager
from workflows import run_crew_workflow

def main():
    """Main function for the Chat page"""
    
    # Page configuration
    st.set_page_config(
        page_title="Digital Twins Management System - Chat",
        page_icon="💬",
        layout="wide"
    )
    
    # Create header
    create_header("Conversational Interface", "💬")
    
    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.messages.append({
            "role": "assistant",
            "content": "Hello! I'm your Digital Twin assistant. I can help you with research, analysis, and strategic insights. What would you like to know?"
        })
    
    # Sidebar
    with st.sidebar:
        create_sidebar_info()
        
        st.header("💬 Chat Settings")
        
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
            help="Enter your Ollama Cloud API key"
        )
        
        if not api_key:
            st.warning("⚠️ Please enter your Ollama API key to use cloud models")
            st.stop()
        
        # Test LLM connection
        if st.button("🧪 Test LLM Connection"):
            with st.spinner("Testing connection..."):
                try:
                    test_llm = initialize_llm(use_cloud=True, api_key=api_key)
                    if test_llm:
                        st.success("✅ LLM connection successful!")
                    else:
                        st.error("❌ LLM connection failed!")
                except Exception as e:
                    st.error(f"❌ Connection error: {e}")
        
        # Chat settings
        st.subheader("⚙️ Chat Settings")
        use_memory = st.checkbox("Enable Memory", value=True, help="Remember previous conversations")
        use_presearch = st.checkbox("Enable Pre-search", value=True, help="Search web and memory before responding")
        
        # Memory management
        st.subheader("🧠 Memory Management")
        try:
            memory_stats = get_memory_stats()
            st.metric("Stored Conversations", memory_stats.get("total_conversations", 0))
        except Exception as e:
            st.warning(f"Memory stats unavailable: {e}")
        
        if st.button("🗑️ Clear Chat History"):
            st.session_state.messages = []
            st.session_state.messages.append({
                "role": "assistant",
                "content": "Chat cleared! How can I help you today?"
            })
            st.rerun()
        
        if st.button("🧠 Clear Memory"):
            try:
                clear_memory()
                st.success("Memory cleared!")
                st.rerun()
            except Exception as e:
                st.error(f"Failed to clear memory: {e}")
        
        # Conversation topics
        if "conversation_topics" in st.session_state and st.session_state.conversation_topics:
            st.subheader("💭 Recent Topics")
            for i, topic in enumerate(st.session_state.conversation_topics[-5:], 1):
                st.write(f"{i}. {topic}")
    
    # Main chat interface
    st.markdown("## 💬 Chat with Your Digital Twin Assistant")
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask your question here..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Track conversation topics
        if len(prompt) > 10:
            if "conversation_topics" not in st.session_state:
                st.session_state.conversation_topics = []
            st.session_state.conversation_topics.append(prompt[:50] + "...")
            # Keep only last 10 topics
            if len(st.session_state.conversation_topics) > 10:
                st.session_state.conversation_topics = st.session_state.conversation_topics[-10:]
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Display assistant response
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            response_placeholder.markdown("🔄 **Thinking...**")
            
            try:
                # Initialize LLM
                with st.spinner("Initializing AI model..."):
                    llm = initialize_llm(use_cloud=True, api_key=api_key)
                
                if not llm:
                    st.error("❌ Failed to initialize LLM. Please check your API key.")
                    return
                
                st.success("✅ AI model initialized successfully!")
                
                # Pre-search if enabled
                if use_presearch:
                    with st.expander("🔍 Gathering Context", expanded=False):
                        st.write("• 🔍 Searching web for current information...")
                        st.write("• 🧠 Searching memory for relevant context...")
                        st.write("• 📊 Analyzing and synthesizing information...")
                    
                    # Perform pre-search
                    presearch_manager = PreSearchManager(memory_enabled=use_memory, max_memory_results=3)
                    search_data = presearch_manager.search_and_combine_context(prompt, st.session_state.messages)
                    
                    # Show search results
                    if search_data.get('web_results'):
                        st.write("✅ Found web information")
                    if search_data.get('memory_results'):
                        st.write("✅ Found relevant memory context")
                
                # Run workflow
                with st.expander("🤖 Processing with AI Agents", expanded=False):
                    st.write("• 🔍 Research Specialist: Gathering information...")
                    time.sleep(1)
                    st.write("• 📊 Data Analyst: Analyzing findings...")
                    time.sleep(1)
                    st.write("• ✍️ Content Writer: Preparing response...")
                    time.sleep(1)
                
                # Execute workflow
                with st.spinner("Running AI workflow..."):
                    workflow_result = run_crew_workflow(
                        prompt, 
                        llm, 
                        st.session_state.messages, 
                        use_native_function_calling=False
                    )
                
                if not workflow_result or workflow_result.strip() == "":
                    workflow_result = "I apologize, but I couldn't generate a response. Please try rephrasing your question or check your API key."
                
                # Display the result
                response_placeholder.markdown(workflow_result)
                
                # Add to chat history
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": workflow_result
                })
                
                # Save to memory if enabled
                if use_memory:
                    try:
                        add_to_memory(
                            query=prompt,
                            response=workflow_result,
                            metadata={
                                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                                "workflow_type": "chat",
                                "use_presearch": use_presearch
                            }
                        )
                    except Exception as mem_error:
                        st.warning(f"⚠️ Memory save failed: {mem_error}")
                
            except Exception as e:
                error_message = f"❌ **Error occurred:** {str(e)}"
                response_placeholder.markdown(error_message)
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": error_message
                })
    
    # Quick actions
    st.markdown("### 🚀 Quick Actions")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🔍 Research Topic", use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": "Please research the latest trends in digital transformation for enterprise organizations."})
            st.rerun()
    
    with col2:
        if st.button("📊 Analyze Data", use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": "Help me analyze the key performance indicators for our digital transformation initiative."})
            st.rerun()
    
    with col3:
        if st.button("💡 Strategic Insights", use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": "Provide strategic insights on how to improve our organizational efficiency using digital twin technology."})
            st.rerun()
    
    with col4:
        if st.button("📋 Generate Report", use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": "Generate a comprehensive report on digital transformation best practices for senior executives."})
            st.rerun()
    
    # Create footer
    create_footer()

if __name__ == "__main__":
    main()
