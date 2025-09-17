"""
Data Analyst Agent for CrewAI Workflow

This module defines the Data Analyst agent responsible for analyzing research data
and providing strategic insights and recommendations.
"""

from crewai import Agent
from typing import List, Optional, Any
from agent_tools import AnalysisTool


def create_analyst_agent(llm, conversation_history: Optional[List[Any]] = None, use_tools: bool = True) -> Agent:
    """
    Create a Data Analyst agent for the CrewAI workflow
    
    Args:
        llm: The language model to use for the agent
        conversation_history: Previous conversation context for continuity
        use_tools: Whether to enable tool usage for the agent
        
    Returns:
        Agent: Configured Data Analyst agent
    """
    
    # Build context from conversation history
    context_info = ""
    if conversation_history and len(conversation_history) > 1:
        context_info = f"""
        
        CONVERSATION CONTEXT:
        This is part of an ongoing conversation. Previous topics discussed include:
        {chr(10).join([f"- {msg['content'][:100]}..." for msg in conversation_history[-3:] if msg['role'] == 'user'])}
        
        Please reference and build upon previous discussions when relevant, and maintain continuity 
        in the conversation flow. If the current question relates to previous topics, acknowledge 
        the connection and provide comparative or building insights.
        """
    
    # Determine tools based on use_tools parameter
    analyst_tools = [AnalysisTool()] if use_tools else []
    
    analyst = Agent(
        role='Data Analyst',
        goal='Analyze research data using analysis tools and provide insights while maintaining conversation continuity',
        backstory=f"""You are a skilled analyst who excels at processing information and extracting 
        meaningful patterns and insights. {'You MUST use the analysis_tool to process and analyze ' if use_tools else 'You will analyze the provided research data and '}
        research data. You have excellent memory of previous analyses and can draw connections 
        between current and past findings. You provide comparative analysis and build upon previous 
        insights to create deeper understanding.
        {'IMPORTANT: Always use the analysis_tool to process research data and extract insights.' if use_tools else 'IMPORTANT: Analyze the research data provided and extract key insights and patterns.'}
        {context_info}""",
        verbose=True,
        allow_delegation=False,
        tools=analyst_tools,
        llm=llm
    )
    
    return analyst
