"""
Chat Interface UI Components

This module contains chat interface and conversation management UI components.
"""

import streamlit as st
from typing import List, Any


def create_chat_interface():
    """Create the chat interface UI"""
    
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
    
    return st.session_state.messages


def create_chat_input():
    """Create the chat input interface"""
    
    # Chat input
    if prompt := st.chat_input("Ask me anything about your research needs..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        return prompt
    
    return None


def display_workflow_results(result: str, workflow_type: str):
    """Display workflow results in the chat interface"""
    
    # Display assistant response
    with st.chat_message("assistant"):
        st.markdown(result)
        
        # Add download button for results
        if result and len(result) > 100:  # Only show download for substantial results
            st.download_button(
                label="📥 Download Results",
                data=result,
                file_name=f"{workflow_type.replace(' ', '_').lower()}_results_{st.session_state.get('timestamp', 'unknown')}.txt",
                mime="text/plain"
            )
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": result})


def create_conversation_topics_sidebar():
    """Create conversation topics display for sidebar"""
    
    if st.session_state.conversation_topics:
        st.header("💬 Conversation Topics")
        
        for i, topic in enumerate(st.session_state.conversation_topics[-5:], 1):  # Show last 5 topics
            st.write(f"{i}. {topic}")
        
        if st.button("🗑️ Clear Topics"):
            st.session_state.conversation_topics = []
            st.rerun()
    else:
        st.header("💬 Conversation Topics")
        st.info("No topics yet. Start a conversation to see topics here.")


def extract_conversation_topics(prompt: str) -> List[str]:
    """Extract key topics from user prompt for conversation tracking"""
    
    # Simple topic extraction - can be enhanced with NLP
    topics = []
    
    # Common research topics
    research_keywords = [
        "digital twin", "data strategy", "compliance", "risk management",
        "information governance", "metadata", "data quality", "tender",
        "proposal", "project delivery", "technical documentation",
        "data engineering", "data science", "data architecture"
    ]
    
    prompt_lower = prompt.lower()
    for keyword in research_keywords:
        if keyword in prompt_lower:
            topics.append(keyword.title())
    
    # Add to conversation topics if not already present
    for topic in topics:
        if topic not in st.session_state.conversation_topics:
            st.session_state.conversation_topics.append(topic)
    
    return topics
