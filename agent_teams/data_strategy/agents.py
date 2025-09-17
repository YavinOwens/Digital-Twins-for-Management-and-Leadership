"""
Data Strategy Team Agents

This module contains the agent definitions for the Data Strategy team.
"""

from crewai import Agent
from typing import List, Optional, Any, Tuple


def create_data_strategy_agents(llm, conversation_history: Optional[List[Any]] = None, use_tools: bool = True) -> Tuple[Agent, Agent, Agent]:
    """
    Create Data Strategy team agents.
    
    Args:
        llm: The language model to use for all agents
        conversation_history: Previous conversation context for continuity
        use_tools: Whether to enable tool usage for the agents
        
    Returns:
        Tuple of (data_governance_specialist, dcam_template_specialist, tranch_guidance_specialist) agents
    """
    
    # Data Governance Specialist Agent
    data_governance_specialist = Agent(
        role="Data Governance Specialist",
        goal="Create comprehensive DAMA-DMBOK frameworks and data governance structures",
        backstory="""You are an expert in data governance with deep knowledge of DAMA-DMBOK 
        (Data Management Body of Knowledge) frameworks. You excel at designing data governance 
        structures, policies, and procedures that align with industry best practices. You have 
        extensive experience in data management, data quality, and regulatory compliance.""",
        verbose=True,
        allow_delegation=False,
        llm=llm,
        max_iter=3,
        max_rpm=5,
        max_execution_time=300,
        memory=False
    )
    
    # DCAM Template Specialist Agent
    dcam_template_specialist = Agent(
        role="DCAM Template Specialist",
        goal="Develop Data Capability Assessment Model templates and maturity frameworks",
        backstory="""You are a specialist in Data Capability Assessment Model (DCAM) frameworks. 
        You excel at creating assessment templates, maturity models, and capability frameworks 
        that help organizations evaluate and improve their data management capabilities. You have 
        extensive experience in data architecture, data modeling, and organizational assessment.""",
        verbose=True,
        allow_delegation=False,
        llm=llm,
        max_iter=3,
        max_rpm=5,
        max_execution_time=300,
        memory=False
    )
    
    # Tranch Guidance Specialist Agent
    tranch_guidance_specialist = Agent(
        role="Tranch Guidance Specialist",
        goal="Design phased implementation roadmaps and delivery tranches",
        backstory="""You are an expert in project management and implementation planning. You excel 
        at creating phased implementation roadmaps, delivery tranches, and project timelines that 
        ensure successful data strategy implementation. You have extensive experience in change 
        management, risk assessment, and stakeholder engagement.""",
        verbose=True,
        allow_delegation=False,
        llm=llm,
        max_iter=3,
        max_rpm=5,
        max_execution_time=300,
        memory=False
    )
    
    return data_governance_specialist, dcam_template_specialist, tranch_guidance_specialist


def create_data_strategy_agents_with_context(llm, conversation_history: Optional[List[Any]] = None, use_tools: bool = True) -> dict:
    """
    Create Data Strategy team agents and return them as a dictionary.
    
    Args:
        llm: The language model to use for all agents
        conversation_history: Previous conversation context for continuity
        use_tools: Whether to enable tool usage for the agents
        
    Returns:
        dict: Dictionary containing data strategy agents with descriptive keys
    """
    
    data_governance_specialist, dcam_template_specialist, tranch_guidance_specialist = create_data_strategy_agents(llm, conversation_history, use_tools)
    
    return {
        'data_governance_specialist': data_governance_specialist,
        'dcam_template_specialist': dcam_template_specialist,
        'tranch_guidance_specialist': tranch_guidance_specialist,
        'governance_agent': data_governance_specialist,  # Alternative key
        'dcam_agent': dcam_template_specialist,         # Alternative key
        'tranch_agent': tranch_guidance_specialist      # Alternative key
    }
