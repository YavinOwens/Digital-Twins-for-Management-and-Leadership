"""
Research Specialist Agent for CrewAI Workflow

This module defines the Research Specialist agent responsible for conducting
thorough research on given topics using web search tools.
"""

from crewai import Agent
from typing import List, Optional, Any
from agent_tools import search_web


def create_researcher_agent(llm, conversation_history: Optional[List[Any]] = None, use_tools: bool = True) -> Agent:
    """
    Create a Research Specialist agent for the CrewAI workflow
    
    Args:
        llm: The language model to use for the agent
        conversation_history: Previous conversation context for continuity
        use_tools: Whether to enable tool usage for the agent
        
    Returns:
        Agent: Configured Research Specialist agent
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
    researcher_tools = [search_web] if use_tools else []
    
    researcher = Agent(
        role='Research Specialist',
        goal='Conduct thorough research on given topics using web search tools while considering conversation context and building on previous discussions',
        backstory=f"""You are an expert researcher with a keen eye for finding relevant information 
        and identifying key insights from various sources. {'You MUST use the search_web tool to ' if use_tools else 'You will work with pre-searched data to '}
        perform actual web searches for every research task. You excel at connecting new research 
        with previous conversation topics and providing context-aware insights. You always consider 
        the broader conversation flow and reference relevant previous discussions when appropriate.
        
        {'CRITICAL: You MUST call the search_web tool with the exact query provided. Do NOT just ' if use_tools else 'IMPORTANT: You will work with pre-searched data provided to you. '}
        describe what you would search for - actually perform the search and return the results.
        Never make up information - only use data from actual web searches.
        
        {'IMPORTANT: When given a research task, immediately call search_web.run(query) and return ' if use_tools else 'IMPORTANT: When given a research task, analyze the provided research data and return '}
        the complete results. Do not provide any other response until you have performed the search.
        
        {context_info}""",
        verbose=True,
        allow_delegation=False,
        tools=researcher_tools,
        llm=llm
    )
    
    return researcher
