"""
Analysis Task for CrewAI Workflow

This module defines the analysis task that instructs the Data Analyst
agent to analyze research data and provide strategic insights.
"""

from crewai import Task
from typing import List, Optional, Any


def create_analysis_task(analyst_agent, query: str, conversation_history: Optional[List[Any]] = None, use_tools: bool = True) -> Task:
    """
    Create an analysis task for the Data Analyst agent
    
    Args:
        analyst_agent: The Data Analyst agent
        query: The analysis query/topic
        conversation_history: Previous conversation context for continuity
        use_tools: Whether the agent should use analysis tools
        
    Returns:
        Task: Configured analysis task
    """
    
    # Build conversation context for tasks
    context_instruction = ""
    if conversation_history and len(conversation_history) > 1:
        recent_topics = [msg['content'][:50] + "..." for msg in conversation_history[-3:] if msg['role'] == 'user']
        context_instruction = f"""
        
        CONVERSATION CONTEXT: This question is part of an ongoing conversation. Recent topics discussed include: {', '.join(recent_topics)}
        
        When analyzing, consider how this topic relates to previous discussions and provide context-aware insights that build upon earlier conversations.
        """
    
    task_description = f"""Analyze the research findings and provide strategic insights:
        {context_instruction}
        
        IMPORTANT: Analyze the research data from the previous task and extract meaningful insights.
        
        Focus on the most critical insights for executive decision-making:
        - Key themes and patterns (top 3-5 most important)
        - Strategic opportunities and competitive advantages
        - Main challenges and risk factors
        - ROI considerations and business impact
        - Implementation feasibility (high-level assessment)
        
        Keep the analysis concise but actionable. Focus on insights that senior leaders can immediately use for strategic planning.
        Analyze the research data provided and extract key insights and patterns."""
    
    expected_output = "A concise analytical summary (500-1000 words) with key strategic insights, top opportunities, main challenges, and actionable recommendations for executive decision-making. Focus on the most critical insights that senior leaders need to know."
    
    return Task(
        description=task_description,
        expected_output=expected_output,
        agent=analyst_agent,
        timeout=90,  # 1.5 minute timeout for analysis task
    )
