"""
Research & Analysis Team Agents

This module contains the agent definitions for the Research & Analysis team.
"""

from crewai import Agent
from typing import List, Optional, Any, Tuple


def create_research_analysis_agents(llm, conversation_history: Optional[List[Any]] = None, use_tools: bool = True) -> Tuple[Agent, Agent, Agent]:
    """
    Create Research & Analysis team agents.
    
    Args:
        llm: The language model to use for all agents
        conversation_history: Previous conversation context for continuity
        use_tools: Whether to enable tool usage for the agents
        
    Returns:
        Tuple of (researcher, analyst, writer) agents
    """
    
    # Research Specialist Agent
    researcher = Agent(
        role="Research Specialist",
        goal="Conduct comprehensive web research to gather current, relevant information on the given topic",
        backstory="""You are an expert research specialist with extensive experience in gathering 
        and synthesizing information from multiple sources. You excel at finding the most 
        current and relevant information, understanding complex topics, and presenting 
        findings in a clear, organized manner. You have access to web search tools and 
        can navigate through various information sources to provide comprehensive coverage 
        of any topic.""",
        verbose=True,
        allow_delegation=False,
        llm=llm,
        max_iter=3,
        max_rpm=5,
        max_execution_time=300,
        memory=False
    )
    
    # Data Analyst Agent
    analyst = Agent(
        role="Data Analyst",
        goal="Analyze research findings to identify patterns, trends, and key insights",
        backstory="""You are a skilled data analyst with expertise in processing and interpreting 
        complex information. You excel at identifying patterns, trends, and relationships in data, 
        and can provide actionable insights based on your analysis. You have a keen eye for detail 
        and can spot important information that others might miss.""",
        verbose=True,
        allow_delegation=False,
        llm=llm,
        max_iter=3,
        max_rpm=5,
        max_execution_time=300,
        memory=False
    )
    
    # Content Writer Agent
    writer = Agent(
        role="Content Writer",
        goal="Create well-structured, engaging content based on research and analysis",
        backstory="""You are a professional content writer with expertise in creating clear, 
        compelling, and well-structured content. You excel at taking complex information and 
        presenting it in an accessible, engaging way. You have a strong understanding of 
        different content formats and can adapt your writing style to suit various audiences 
        and purposes.""",
        verbose=True,
        allow_delegation=False,
        llm=llm,
        max_iter=3,
        max_rpm=5,
        max_execution_time=300,
        memory=False
    )
    
    return researcher, analyst, writer


def create_research_analysis_agents_with_context(llm, conversation_history: Optional[List[Any]] = None, use_tools: bool = True) -> dict:
    """
    Create Research & Analysis team agents and return them as a dictionary.
    
    Args:
        llm: The language model to use for all agents
        conversation_history: Previous conversation context for continuity
        use_tools: Whether to enable tool usage for the agents
        
    Returns:
        dict: Dictionary containing research analysis agents with descriptive keys
    """
    
    researcher, analyst, writer = create_research_analysis_agents(llm, conversation_history, use_tools)
    
    return {
        'researcher': researcher,
        'analyst': analyst,
        'writer': writer,
        'research_specialist': researcher,  # Alternative key
        'data_analyst': analyst,           # Alternative key
        'content_writer': writer           # Alternative key
    }
