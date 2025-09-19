"""
Research & Analysis Team Agents

This module contains the agent definitions for the Research & Analysis team.
"""

from crewai import Agent
from typing import List, Optional, Any, Tuple
from agent_tools.document_access_tool import (
    access_uploaded_documents,
    analyze_document_data,
    query_document_data,
    get_document_summary,
    search_document_content,
    get_document_metadata,
    compare_documents,
    extract_document_insights,
    search_documents_semantically,
    get_document_from_memory_tool,
    list_documents_in_memory_tool
)
from agent_tools.research_validation_tool import (
    validate_research_source,
    add_harvard_citation,
    create_harvard_reference,
    validate_all_references,
    generate_reference_list_tool,
    fact_check_claim,
    check_academic_integrity
)


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
    researcher_tools = []
    if use_tools:
        researcher_tools = [
            access_uploaded_documents,
            analyze_document_data,
            query_document_data,
            get_document_summary,
            search_document_content,
            get_document_metadata,
            compare_documents,
            extract_document_insights,
            search_documents_semantically,
            get_document_from_memory_tool,
            list_documents_in_memory_tool,
            validate_research_source,
            add_harvard_citation,
            create_harvard_reference,
            validate_all_references,
            generate_reference_list_tool,
            fact_check_claim,
            check_academic_integrity
        ]
    
    researcher = Agent(
        role="Research Specialist",
        goal="Conduct comprehensive web research to gather current, relevant information on the given topic",
        backstory="""You are an expert research specialist with extensive experience in gathering 
        and synthesizing information from multiple sources. You excel at finding the most 
        current and relevant information, understanding complex topics, and presenting 
        findings in a clear, organized manner. You have access to web search tools and 
        document analysis tools to provide comprehensive coverage of any topic.""",
        verbose=True,
        allow_delegation=False,
        llm=llm,
        max_iter=3,
        max_rpm=5,
        max_execution_time=300,
        memory=False,
        tools=researcher_tools
    )
    
    # Data Analyst Agent
    analyst_tools = []
    if use_tools:
        analyst_tools = [
            access_uploaded_documents,
            analyze_document_data,
            query_document_data,
            get_document_summary,
            search_document_content,
            get_document_metadata,
            compare_documents,
            extract_document_insights,
            search_documents_semantically,
            get_document_from_memory_tool,
            list_documents_in_memory_tool,
            validate_research_source,
            add_harvard_citation,
            create_harvard_reference,
            validate_all_references,
            generate_reference_list_tool,
            fact_check_claim,
            check_academic_integrity
        ]
    
    analyst = Agent(
        role="Data Analyst",
        goal="Analyze research findings to identify patterns, trends, and key insights",
        backstory="""You are a skilled data analyst with expertise in processing and interpreting 
        complex information. You excel at identifying patterns, trends, and relationships in data, 
        and can provide actionable insights based on your analysis. You have a keen eye for detail 
        and can spot important information that others might miss. You have access to document 
        analysis tools to work with uploaded data.""",
        verbose=True,
        allow_delegation=False,
        llm=llm,
        max_iter=3,
        max_rpm=5,
        max_execution_time=300,
        memory=False,
        tools=analyst_tools
    )
    
    # Content Writer Agent
    writer_tools = []
    if use_tools:
        writer_tools = [
            access_uploaded_documents,
            analyze_document_data,
            query_document_data,
            get_document_summary,
            search_document_content,
            get_document_metadata,
            compare_documents,
            extract_document_insights,
            search_documents_semantically,
            get_document_from_memory_tool,
            list_documents_in_memory_tool,
            validate_research_source,
            add_harvard_citation,
            create_harvard_reference,
            validate_all_references,
            generate_reference_list_tool,
            fact_check_claim,
            check_academic_integrity
        ]
    
    writer = Agent(
        role="Content Writer",
        goal="Create well-structured, engaging content based on research and analysis",
        backstory="""You are a professional content writer with expertise in creating clear, 
        compelling, and well-structured content. You excel at taking complex information and 
        presenting it in an accessible, engaging way. You have a strong understanding of 
        different content formats and can adapt your writing style to suit various audiences 
        and purposes. You have access to document analysis tools to incorporate data insights 
        into your writing.""",
        verbose=True,
        allow_delegation=False,
        llm=llm,
        max_iter=3,
        max_rpm=5,
        max_execution_time=300,
        memory=False,
        tools=writer_tools
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
