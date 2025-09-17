"""
Agent Factory for CrewAI Multi-Agent Workflow

This module provides factory functions to create and configure all agents
for the CrewAI workflow with proper conversation context and tool configuration.
"""

from typing import List, Optional, Any, Tuple
from .researcher_agent import create_researcher_agent
from .analyst_agent import create_analyst_agent
from .writer_agent import create_writer_agent
from .data_strategy_agents import create_data_strategy_team
from .compliance_risk_agents import create_compliance_risk_team
from .information_management_agents import create_information_management_team
from .tender_response_agents import create_tender_response_team
from .project_delivery_agents import create_project_delivery_team
from .technical_documentation_agents import create_technical_documentation_team


def create_crew_agents(llm, conversation_history: Optional[List[Any]] = None, use_tools: bool = True) -> Tuple[Any, Any, Any]:
    """
    Create all CrewAI agents for the workflow with conversation context
    
    Args:
        llm: The language model to use for all agents
        conversation_history: Previous conversation context for continuity
        use_tools: Whether to enable tool usage for the agents
        
    Returns:
        Tuple[Agent, Agent, Agent]: Tuple of (researcher, analyst, writer) agents
    """
    
    # Create individual agents
    researcher = create_researcher_agent(llm, conversation_history, use_tools)
    analyst = create_analyst_agent(llm, conversation_history, use_tools)
    writer = create_writer_agent(llm, conversation_history, use_tools)
    
    return researcher, analyst, writer


def create_agents_with_context(llm, conversation_history: Optional[List[Any]] = None, use_tools: bool = True) -> dict:
    """
    Create all agents and return them as a dictionary for easy access
    
    Args:
        llm: The language model to use for all agents
        conversation_history: Previous conversation context for continuity
        use_tools: Whether to enable tool usage for the agents
        
    Returns:
        dict: Dictionary containing all agents with descriptive keys
    """
    
    researcher, analyst, writer = create_crew_agents(llm, conversation_history, use_tools)
    
    return {
        'researcher': researcher,
        'analyst': analyst,
        'writer': writer,
        'research_specialist': researcher,  # Alternative key
        'data_analyst': analyst,           # Alternative key
        'content_writer': writer           # Alternative key
    }


def create_data_strategy_agents_with_context(llm, conversation_history: Optional[List[Any]] = None, use_tools: bool = True) -> dict:
    """
    Create data strategy team agents and return them as a dictionary
    
    Args:
        llm: The language model to use for all agents
        conversation_history: Previous conversation context for continuity
        use_tools: Whether to enable tool usage for the agents
        
    Returns:
        dict: Dictionary containing data strategy agents with descriptive keys
    """
    
    data_strategy_team = create_data_strategy_team(llm)
    governance_agent, dcam_agent, tranch_agent = data_strategy_team
    
    return {
        'data_governance_specialist': governance_agent,
        'dcam_template_specialist': dcam_agent,
        'tranch_guidance_specialist': tranch_agent,
        'governance_agent': governance_agent,  # Alternative key
        'dcam_agent': dcam_agent,             # Alternative key
        'tranch_agent': tranch_agent          # Alternative key
    }


def create_compliance_risk_agents_with_context(llm, conversation_history: Optional[List[Any]] = None, use_tools: bool = True) -> dict:
    """
    Create compliance and risk management team agents and return them as a dictionary
    
    Args:
        llm: The language model to use for all agents
        conversation_history: Previous conversation context for continuity
        use_tools: Whether to enable tool usage for the agents
        
    Returns:
        dict: Dictionary containing compliance and risk agents with descriptive keys
    """
    
    compliance_risk_team = create_compliance_risk_team(llm)
    compliance_agent, risk_agent, audit_agent = compliance_risk_team
    
    return {
        'compliance_specialist': compliance_agent,
        'risk_management_specialist': risk_agent,
        'audit_governance_specialist': audit_agent,
        'compliance_agent': compliance_agent,  # Alternative key
        'risk_agent': risk_agent,             # Alternative key
        'audit_agent': audit_agent            # Alternative key
    }


def create_information_management_agents_with_context(llm, conversation_history: Optional[List[Any]] = None, use_tools: bool = True) -> dict:
    """
    Create information management team agents and return them as a dictionary
    
    Args:
        llm: The language model to use for all agents
        conversation_history: Previous conversation context for continuity
        use_tools: Whether to enable tool usage for the agents
        
    Returns:
        dict: Dictionary containing information management agents with descriptive keys
    """
    
    information_management_team = create_information_management_team(llm)
    info_governance_agent, metadata_agent, data_quality_agent = information_management_team
    
    return {
        'information_governance_specialist': info_governance_agent,
        'metadata_management_specialist': metadata_agent,
        'data_quality_specialist': data_quality_agent,
        'info_governance_agent': info_governance_agent,  # Alternative key
        'metadata_agent': metadata_agent,               # Alternative key
        'data_quality_agent': data_quality_agent        # Alternative key
    }


def get_agent_by_role(role: str, llm, conversation_history: Optional[List[Any]] = None, use_tools: bool = True) -> Any:
    """
    Get a specific agent by role name
    
    Args:
        role: The role name ('researcher', 'analyst', 'writer')
        llm: The language model to use for the agent
        conversation_history: Previous conversation context for continuity
        use_tools: Whether to enable tool usage for the agent
        
    Returns:
        Agent: The requested agent
        
    Raises:
        ValueError: If role is not recognized
    """
    
    role_mapping = {
        'researcher': create_researcher_agent,
        'research_specialist': create_researcher_agent,
        'analyst': create_analyst_agent,
        'data_analyst': create_analyst_agent,
        'writer': create_writer_agent,
        'content_writer': create_writer_agent
    }
    
    if role.lower() not in role_mapping:
        raise ValueError(f"Unknown role: {role}. Available roles: {list(role_mapping.keys())}")
    
    return role_mapping[role.lower()](llm, conversation_history, use_tools)


def create_tender_response_agents_with_context(llm, conversation_history: Optional[List[Any]] = None, use_tools: bool = True) -> dict:
    """
    Create tender response team agents and return them as a dictionary
    
    Args:
        llm: The language model to use for all agents
        conversation_history: Previous conversation context for continuity
        use_tools: Whether to enable tool usage for the agents
        
    Returns:
        dict: Dictionary containing tender response agents with descriptive keys
    """
    
    tender_response_team = create_tender_response_team(llm)
    tender_specialist, proposal_writer, compliance_expert = tender_response_team
    
    return {
        'tender_specialist': tender_specialist,
        'proposal_writer': proposal_writer,
        'compliance_expert': compliance_expert,
        'tender_response_specialist': tender_specialist,  # Alternative key
        'proposal_writer_agent': proposal_writer,         # Alternative key
        'compliance_expert_agent': compliance_expert      # Alternative key
    }


def create_project_delivery_agents_with_context(llm, conversation_history: Optional[List[Any]] = None, use_tools: bool = True) -> dict:
    """
    Create project delivery team agents and return them as a dictionary
    
    Args:
        llm: The language model to use for all agents
        conversation_history: Previous conversation context for continuity
        use_tools: Whether to enable tool usage for the agents
        
    Returns:
        dict: Dictionary containing project delivery agents with descriptive keys
    """
    
    project_delivery_team = create_project_delivery_team(llm)
    data_engineer, data_scientist, data_architect, devops_engineer, project_manager = project_delivery_team
    
    return {
        'data_engineer': data_engineer,
        'data_scientist': data_scientist,
        'data_architect': data_architect,
        'devops_engineer': devops_engineer,
        'project_manager': project_manager,
        'senior_data_engineer': data_engineer,      # Alternative key
        'lead_data_scientist': data_scientist,      # Alternative key
        'principal_data_architect': data_architect, # Alternative key
        'senior_devops_engineer': devops_engineer,  # Alternative key
        'technical_project_manager': project_manager # Alternative key
    }


def create_technical_documentation_agents_with_context(llm, conversation_history: Optional[List[Any]] = None, use_tools: bool = True) -> dict:
    """
    Create technical documentation team agents and return them as a dictionary
    
    Args:
        llm: The language model to use for all agents
        conversation_history: Previous conversation context for continuity
        use_tools: Whether to enable tool usage for the agents
        
    Returns:
        dict: Dictionary containing technical documentation agents with descriptive keys
    """
    
    technical_docs_team = create_technical_documentation_team(llm)
    data_modeling_specialist, python_code_specialist, sql_code_specialist, pyspark_code_specialist, technical_writer = technical_docs_team
    
    return {
        'data_modeling_specialist': data_modeling_specialist,
        'python_code_specialist': python_code_specialist,
        'sql_code_specialist': sql_code_specialist,
        'pyspark_code_specialist': pyspark_code_specialist,
        'technical_writer': technical_writer,
        'data_modeler': data_modeling_specialist,           # Alternative key
        'python_developer': python_code_specialist,         # Alternative key
        'sql_developer': sql_code_specialist,               # Alternative key
        'pyspark_developer': pyspark_code_specialist,       # Alternative key
        'tech_writer': technical_writer                     # Alternative key
    }
