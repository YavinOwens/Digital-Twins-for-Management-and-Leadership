"""
Research & Analysis Team Tasks

This module contains the task definitions for the Research & Analysis team.
"""

from crewai import Task
from typing import List, Optional, Any


def create_research_analysis_tasks(
    researcher_agent,
    analyst_agent, 
    writer_agent,
    query: str,
    search_results: Optional[str] = None,
    conversation_history: Optional[List[Any]] = None
) -> List[Task]:
    """
    Create Research & Analysis team tasks.
    
    Args:
        researcher_agent: The research specialist agent
        analyst_agent: The data analyst agent
        writer_agent: The content writer agent
        query: The user's query
        search_results: Pre-searched results (optional)
        conversation_history: Previous conversation context
        
    Returns:
        List of tasks for the Research & Analysis team
    """
    
    # Research Task
    research_task = Task(
        description=f"""
        Conduct comprehensive research on the following topic: {query}
        
        **Your Task:**
        1. Use web search tools to gather current, relevant information
        2. Focus on finding authoritative sources and recent developments
        3. Look for multiple perspectives and viewpoints
        4. Gather quantitative data, statistics, and concrete examples
        5. Identify key stakeholders, trends, and implications
        
        **Search Results Available:** {'Yes' if search_results else 'No'}
        {f'**Pre-searched Data:** {search_results}' if search_results else ''}
        
        **Deliverables:**
        - Comprehensive research findings
        - Key statistics and data points
        - Source citations and references
        - Current trends and developments
        """,
        expected_output="""
        Detailed research report including:
        1. Executive summary of findings
        2. Key statistics and data points
        3. Current trends and developments
        4. Source citations and references
        5. Multiple perspectives on the topic
        """,
        agent=researcher_agent
    )
    
    # Analysis Task
    analysis_task = Task(
        description=f"""
        Analyze the research findings to extract key insights and patterns.
        
        **Research Context:** Based on research findings about: {query}
        
        **Your Task:**
        1. Review and synthesize the research findings
        2. Identify patterns, trends, and relationships
        3. Extract key insights and implications
        4. Analyze strengths, weaknesses, opportunities, and threats
        5. Provide data-driven conclusions
        
        **Deliverables:**
        - Pattern analysis and trend identification
        - Key insights and implications
        - SWOT analysis
        - Data-driven conclusions
        """,
        expected_output="""
        Comprehensive analysis including:
        1. Pattern and trend analysis
        2. Key insights and implications
        3. SWOT analysis
        4. Data-driven conclusions
        5. Strategic recommendations
        """,
        agent=analyst_agent
    )
    
    # Writing Task
    writing_task = Task(
        description=f"""
        Create a well-structured, comprehensive report based on the research and analysis.
        
        **Topic:** {query}
        **Context:** Based on research findings and analysis
        
        **Your Task:**
        1. Synthesize research findings and analysis into a coherent report
        2. Structure the content logically with clear sections
        3. Write in a professional, engaging style
        4. Include executive summary, key findings, and recommendations
        5. Ensure proper formatting and readability
        
        **Deliverables:**
        - Executive summary
        - Structured report with clear sections
        - Key findings and recommendations
        - Professional formatting
        """,
        expected_output="""
        Professional report including:
        1. Executive summary
        2. Introduction and background
        3. Key findings and analysis
        4. Recommendations and next steps
        5. Conclusion
        """,
        agent=writer_agent
    )
    
    return [research_task, analysis_task, writing_task]


def create_research_analysis_tasks_with_data(
    researcher_agent,
    analyst_agent,
    writer_agent,
    query: str,
    search_results: str,
    conversation_history: Optional[List[Any]] = None
) -> List[Task]:
    """
    Create Research & Analysis team tasks with pre-searched data.
    
    Args:
        researcher_agent: The research specialist agent
        analyst_agent: The data analyst agent
        writer_agent: The content writer agent
        query: The user's query
        search_results: Pre-searched results
        conversation_history: Previous conversation context
        
    Returns:
        List of tasks for the Research & Analysis team
    """
    
    return create_research_analysis_tasks(
        researcher_agent, analyst_agent, writer_agent, query, search_results, conversation_history
    )
