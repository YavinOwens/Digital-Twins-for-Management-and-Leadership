"""
Research Task for CrewAI Workflow

This module defines the research task that instructs the Research Specialist
agent to conduct thorough research on given topics.
"""

from crewai import Task
from typing import List, Optional, Any


def create_research_task(researcher_agent, query: str, conversation_history: Optional[List[Any]] = None, use_tools: bool = True) -> Task:
    """
    Create a research task for the Research Specialist agent
    
    Args:
        researcher_agent: The Research Specialist agent
        query: The research query/topic
        conversation_history: Previous conversation context for continuity
        use_tools: Whether the agent should use web search tools
        
    Returns:
        Task: Configured research task
    """
    
    # Build conversation context for tasks
    context_instruction = ""
    if conversation_history and len(conversation_history) > 1:
        recent_topics = [msg['content'][:50] + "..." for msg in conversation_history[-3:] if msg['role'] == 'user']
        context_instruction = f"""
        
        CONVERSATION CONTEXT: This question is part of an ongoing conversation. Recent topics discussed include: {', '.join(recent_topics)}
        
        When researching, consider how this topic relates to previous discussions and provide context-aware insights that build upon earlier conversations.
        """
    
    if use_tools:
        # Task with web search tools
        task_description = f"""Conduct thorough research on: {query}
        {context_instruction}
        
        CRITICAL: You MUST call the search_web tool with the exact query "{query}" to perform actual web searches for current, real information.
        Do NOT just describe what you would search for - actually call the search_web tool and return the results.
        NEVER make up information - only use data from actual web searches.
        
        STEP 1: Call search_web.run("{query}")
        STEP 2: Return the complete search results
        STEP 3: Do not provide any other response until you have performed the search
        
        EXAMPLE: search_web.run("{query}")
        
        Provide comprehensive information including:
        - Key concepts and definitions
        - Current trends and developments in the field
        - Important statistics, data points, and metrics
        - Real-world examples and case studies
        - Industry best practices and success stories
        - Challenges and pain points
        - Future outlook and emerging trends
        - Connections to previous conversation topics (if relevant)
        
        Focus on information that would be valuable for senior executives and decision-makers.
        Call the search_web tool to get real, current data from the web."""
        
        expected_output = "A comprehensive research report with detailed findings, statistics, examples, and insights relevant to executive decision-making, with context-aware connections to previous discussions. Must include real web search results from search_web tool."
    
    else:
        # Task for pre-searched data analysis
        task_description = f"""Analyze the provided research data for: {query}
        {context_instruction}
        
        RESEARCH DATA PROVIDED:
        [Research data will be provided by the system]
        
        Your task is to analyze this research data and provide comprehensive information including:
        - Key concepts and definitions
        - Current trends and developments in the field
        - Important statistics, data points, and metrics
        - Real-world examples and case studies
        - Industry best practices and success stories
        - Challenges and pain points
        - Future outlook and emerging trends
        - Connections to previous conversation topics (if relevant)
        
        Focus on information that would be valuable for senior executives and decision-makers.
        Use ONLY the provided research data - do not make up information."""
        
        expected_output = "A comprehensive research analysis with detailed findings, statistics, examples, and insights relevant to executive decision-making, with context-aware connections to previous discussions. Must be based on the provided research data only."
    
    return Task(
        description=task_description,
        expected_output=expected_output,
        agent=researcher_agent,
        timeout=60,  # 1 minute timeout for research task
        async_execution=False  # Research must complete before analysis
    )


def create_research_task_with_data(researcher_agent, query: str, search_data: str, conversation_history: Optional[List[Any]] = None) -> Task:
    """
    Create a research task with pre-searched data for the Research Specialist agent
    
    Args:
        researcher_agent: The Research Specialist agent
        query: The research query/topic
        search_data: Pre-searched research data
        conversation_history: Previous conversation context for continuity
        
    Returns:
        Task: Configured research task with data
    """
    
    # Build context information for conversation continuity
    if conversation_history and len(conversation_history) > 0:
        recent_topics = [item.get('query', '') for item in conversation_history[-3:]]
        context_instruction = f"""
        CONVERSATION CONTEXT: This question is part of an ongoing conversation. Recent topics discussed include: {', '.join(recent_topics)}
        
        When researching, consider how this topic relates to previous discussions and provide context-aware insights that build upon earlier conversations.
        """
    else:
        context_instruction = ""
    
    return Task(
        description=f"""Analyze the provided research data for: {query}
        {context_instruction}
        
        RESEARCH DATA PROVIDED:
        {search_data}
        
        Your task is to analyze this research data and provide comprehensive information including:
        - Key concepts and definitions
        - Current trends and developments in the field
        - Important statistics, data points, and metrics
        - Real-world examples and case studies
        - Industry best practices and success stories
        - Challenges and pain points
        - Future outlook and emerging trends
        - Connections to previous conversation topics (if relevant)
        
        Focus on information that would be valuable for senior executives and decision-makers.
        Use ONLY the provided research data - do not make up information.""",
        expected_output="A comprehensive research analysis with detailed findings, statistics, examples, and insights relevant to executive decision-making, with context-aware connections to previous discussions. Must be based on the provided research data only.",
        agent=researcher_agent,
        timeout=60,  # 1 minute timeout for research task
        async_execution=False  # Research must complete before analysis
    )
