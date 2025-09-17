"""
Optimized Task Factory for CrewAI Multi-Agent Workflow

This module provides optimized task creation with proper dependencies
and async execution for better performance.
"""

from typing import List, Optional, Any
from crewai import Task
from .research_task import create_research_task, create_research_task_with_data
from .analysis_task import create_analysis_task
from .writing_task import create_writing_task


def create_optimized_crew_tasks(researcher_agent, analyst_agent, writer_agent, query: str, conversation_history: Optional[List[Any]] = None, use_tools: bool = True) -> List[Any]:
    """
    Create optimized CrewAI tasks with proper dependencies
    
    Args:
        researcher_agent: The Research Specialist agent
        analyst_agent: The Data Analyst agent
        writer_agent: The Content Writer agent
        query: The main query/topic for the workflow
        conversation_history: Previous conversation context for continuity
        use_tools: Whether to enable tool usage for the agents
        
    Returns:
        List[Task]: List of configured tasks with dependencies
    """
    
    # Create research task (must complete first)
    research_task = create_research_task(researcher_agent, query, conversation_history, use_tools)
    
    # Create analysis task that depends on research
    analysis_task = Task(
        description=f"""Analyze the research findings from the previous task.
        
        Focus on extracting:
        - Top 3-5 key insights
        - Strategic opportunities
        - Main challenges
        - Actionable recommendations
        
        Keep analysis concise (500-750 words) for executive consumption.""",
        expected_output="A concise strategic analysis with key insights and recommendations.",
        agent=analyst_agent,
        context=[research_task],  # Depends on research task output
        timeout=60,
        async_execution=False
    )
    
    # Create writing task that depends on both research and analysis
    writing_task = Task(
        description=f"""Create an executive report based on the research and analysis.
        
        Structure:
        1. Executive Summary (200 words)
        2. Key Findings (5 bullet points)
        3. Strategic Recommendations (3-5 actions)
        4. Implementation Timeline
        
        Target length: 800-1200 words
        Style: Professional, actionable, data-driven""",
        expected_output="A concise executive report with actionable insights.",
        agent=writer_agent,
        context=[research_task, analysis_task],  # Depends on both previous tasks
        timeout=90,
        async_execution=False
    )
    
    return [research_task, analysis_task, writing_task]


def create_optimized_crew_tasks_with_data(researcher_agent, analyst_agent, writer_agent, query: str, search_data: str, conversation_history: Optional[List[Any]] = None) -> List[Any]:
    """
    Create optimized tasks with pre-searched data and dependencies
    
    Args:
        researcher_agent: The Research Specialist agent
        analyst_agent: The Data Analyst agent
        writer_agent: The Content Writer agent
        query: The main query/topic for the workflow
        search_data: Pre-searched research data
        conversation_history: Previous conversation context for continuity
        
    Returns:
        List[Task]: List of configured tasks with dependencies
    """
    
    # Create research task with pre-searched data
    research_task = create_research_task_with_data(researcher_agent, query, search_data, conversation_history)
    
    # Create analysis task with dependency
    analysis_task = Task(
        description=f"""Analyze the research data for strategic insights.
        
        Extract:
        - Top 3-5 themes
        - Key opportunities
        - Critical challenges
        - Quick wins vs long-term initiatives
        
        Be concise and actionable.""",
        expected_output="Strategic analysis with prioritized insights.",
        agent=analyst_agent,
        context=[research_task],
        timeout=60,
        async_execution=False
    )
    
    # Create writing task with dependencies
    writing_task = Task(
        description=f"""Write a focused executive report.
        
        Include:
        - Executive Summary
        - 5 Key Findings
        - 3-5 Recommendations
        - Next Steps
        
        Length: 800-1200 words
        Tone: Executive-friendly""",
        expected_output="Concise executive report.",
        agent=writer_agent,
        context=[research_task, analysis_task],
        timeout=90,
        async_execution=False
    )
    
    return [research_task, analysis_task, writing_task]
