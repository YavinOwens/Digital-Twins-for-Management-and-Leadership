"""
Writing Task for CrewAI Workflow

This module defines the writing task that instructs the Content Writer
agent to create comprehensive executive reports.
"""

from crewai import Task
from typing import List, Optional, Any


def create_writing_task(writer_agent, query: str, conversation_history: Optional[List[Any]] = None, search_data: Optional[str] = None) -> Task:
    """
    Create a writing task for the Content Writer agent
    
    Args:
        writer_agent: The Content Writer agent
        query: The writing query/topic
        conversation_history: Previous conversation context for continuity
        search_data: Optional pre-searched data to include in the task
        
    Returns:
        Task: Configured writing task
    """
    
    # Build conversation context for tasks
    context_instruction = ""
    if conversation_history and len(conversation_history) > 1:
        recent_topics = [msg['content'][:50] + "..." for msg in conversation_history[-3:] if msg['role'] == 'user']
        context_instruction = f"""
        
        CONVERSATION CONTEXT: This question is part of an ongoing conversation. Recent topics discussed include: {', '.join(recent_topics)}
        
        When writing, consider how this topic relates to previous discussions and provide context-aware insights that build upon earlier conversations.
        """
    
    # Build research data section if provided
    research_data_section = ""
    if search_data:
        research_data_section = f"""
        
        RESEARCH DATA PROVIDED:
        {search_data}"""
    
    task_description = f"""Write a comprehensive executive report for: "{query}"
        {context_instruction}{research_data_section}
        
        Create a well-structured report with these sections:
        
        1. **Executive Summary** - Key findings and recommendations (200-300 words)
        2. **Key Findings** - Top 5-7 insights with supporting data
        3. **Strategic Analysis** - Opportunities, challenges, and implications
        4. **Recommendations** - 3-5 actionable steps for executives
        5. **Implementation Roadmap** - Timeline and key milestones
        
        Requirements:
        - Target length: 1000-1500 words for optimal readability
        - Focus on actionable insights for C-suite executives
        - Use data and examples from the research provided
        - Include proper citations in Harvard style (Author, Year)
        - Be concise but comprehensive
        - No placeholders or incomplete sections"""
    
    expected_output = "A complete executive report (1000-1500 words) with all sections fully written, containing actionable insights, strategic analysis, and implementation guidance for senior leadership. Must include proper citations from the research data provided."
    
    return Task(
        description=task_description,
        expected_output=expected_output,
        agent=writer_agent,
        timeout=120,  # 2 minute timeout for writing task
    )
