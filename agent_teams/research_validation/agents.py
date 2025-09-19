"""
Research Validation Agent

This module contains the research validation agent that verifies sources,
checks links, and ensures factual accuracy of information.
"""

from crewai import Agent
from typing import List, Optional, Any, Tuple, Dict
from agent_tools.reference_manager import (
    create_reference,
    add_citation,
    validate_reference,
    format_harvard_reference,
    generate_reference_list,
    get_citation_stats,
    remove_invalid_references
)
from agent_tools.search_tool import search_web
import re
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_research_validation_agent(llm, conversation_history: Optional[List[Any]] = None, use_tools: bool = True) -> Agent:
    """
    Create Research Validation Agent
    
    Args:
        llm: Language model instance
        conversation_history: Previous conversation context
        use_tools: Whether to include tools
        
    Returns:
        Research Validation Agent
    """
    
    # Define tools for validation agent
    validation_tools = []
    if use_tools:
        validation_tools = [
            search_web,
            create_reference,
            add_citation,
            validate_reference,
            format_harvard_reference,
            generate_reference_list,
            get_citation_stats,
            remove_invalid_references
        ]
    
    validation_agent = Agent(
        role="Research Validation Specialist",
        goal="Verify the accuracy, credibility, and validity of all research sources and information used in Digital Twin outputs",
        backstory="""You are an expert research validation specialist with extensive experience in fact-checking, 
        source verification, and academic integrity. You have a keen eye for identifying credible sources, 
        detecting misinformation, and ensuring that all information presented is accurate and properly referenced. 
        You understand the importance of academic integrity and the potential consequences of including 
        unverified or false information in professional reports.
        
        Your expertise includes:
        - Verifying web sources and checking link accessibility
        - Validating academic references and citations
        - Fact-checking claims against multiple reliable sources
        - Identifying potential misinformation or biased sources
        - Ensuring proper Harvard referencing format
        - Maintaining high standards of academic integrity
        
        You are meticulous, thorough, and never compromise on accuracy. You understand that trust and credibility 
        are essential in professional reporting, and you take your role as a quality gatekeeper very seriously.""",
        verbose=True,
        allow_delegation=False,
        max_iter=3,
        memory=False,
        tools=validation_tools
    )
    
    return validation_agent


def create_research_validation_agents_with_context(llm, conversation_history: Optional[List[Any]] = None, use_tools: bool = True) -> Dict[str, Agent]:
    """
    Create Research Validation agents with conversation context
    
    Args:
        llm: Language model instance
        conversation_history: Previous conversation context
        use_tools: Whether to include tools
        
    Returns:
        Dictionary of validation agents
    """
    
    # Create validation agent
    validation_agent = create_research_validation_agent(llm, conversation_history, use_tools)
    
    # Add conversation context to agent's backstory
    if conversation_history:
        context_summary = f"""
        
        **Previous Conversation Context:**
        {conversation_history[-3:] if len(conversation_history) > 3 else conversation_history}
        
        Use this context to understand the research validation requirements and ensure consistency 
        with previous discussions about source verification and academic standards.
        """
        
        validation_agent.backstory += context_summary
    
    return {
        "research_validation_specialist": validation_agent
    }
