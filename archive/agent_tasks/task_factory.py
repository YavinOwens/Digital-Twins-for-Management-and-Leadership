"""
Task Factory for CrewAI Multi-Agent Workflow

This module provides factory functions to create and configure all tasks
for the CrewAI workflow with proper conversation context and data handling.
"""

from typing import List, Optional, Any
from .research_task import create_research_task, create_research_task_with_data
from .analysis_task import create_analysis_task
from .writing_task import create_writing_task
from .data_strategy_tasks import create_data_strategy_tasks
from .compliance_risk_tasks import create_compliance_risk_tasks
from .information_management_tasks import create_information_management_tasks
from .tender_response_tasks import create_tender_response_tasks
from .project_delivery_tasks import create_project_delivery_tasks
from .technical_documentation_tasks import create_technical_documentation_tasks


def create_crew_tasks(researcher_agent, analyst_agent, writer_agent, query: str, conversation_history: Optional[List[Any]] = None, use_tools: bool = True) -> List[Any]:
    """
    Create all CrewAI tasks for the workflow with conversation context
    
    Args:
        researcher_agent: The Research Specialist agent
        analyst_agent: The Data Analyst agent
        writer_agent: The Content Writer agent
        query: The main query/topic for the workflow
        conversation_history: Previous conversation context for continuity
        use_tools: Whether to enable tool usage for the agents
        
    Returns:
        List[Task]: List of configured tasks in execution order
    """
    
    # Create individual tasks
    research_task = create_research_task(researcher_agent, query, conversation_history, use_tools)
    analysis_task = create_analysis_task(analyst_agent, query, conversation_history, use_tools)
    writing_task = create_writing_task(writer_agent, query, conversation_history)
    
    return [research_task, analysis_task, writing_task]


def create_crew_tasks_with_data(researcher_agent, analyst_agent, writer_agent, query: str, search_data: str, conversation_history: Optional[List[Any]] = None) -> List[Any]:
    """
    Create all CrewAI tasks for the workflow with pre-searched data and dependencies
    
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
    
    # Create analysis task (will depend on research output through CrewAI's sequential process)
    analysis_task = create_analysis_task(analyst_agent, query, conversation_history, use_tools=False)
    
    # Create writing task (will depend on both research and analysis outputs)
    writing_task = create_writing_task(writer_agent, query, conversation_history, search_data)
    
    return [research_task, analysis_task, writing_task]


def create_tasks_by_type(task_type: str, agent, query: str, conversation_history: Optional[List[Any]] = None, **kwargs) -> Any:
    """
    Create a specific task by type
    
    Args:
        task_type: The type of task ('research', 'analysis', 'writing')
        agent: The agent to assign the task to
        query: The main query/topic
        conversation_history: Previous conversation context for continuity
        **kwargs: Additional arguments (search_data, use_tools, etc.)
        
    Returns:
        Task: The requested task
        
    Raises:
        ValueError: If task_type is not recognized
    """
    
    task_mapping = {
        'research': create_research_task,
        'analysis': create_analysis_task,
        'writing': create_writing_task
    }
    
    if task_type.lower() not in task_mapping:
        raise ValueError(f"Unknown task type: {task_type}. Available types: {list(task_mapping.keys())}")
    
    # Handle special case for research task with data
    if task_type.lower() == 'research' and 'search_data' in kwargs:
        return create_research_task_with_data(agent, query, kwargs['search_data'], conversation_history)
    
    # Extract use_tools parameter
    use_tools = kwargs.get('use_tools', True)
    
    return task_mapping[task_type.lower()](agent, query, conversation_history, use_tools)


def create_data_strategy_tasks_with_data(governance_agent, dcam_agent, tranch_agent, query: str, research_data: str, conversation_history: Optional[List[Any]] = None) -> List[Any]:
    """
    Create all data strategy tasks for the second team workflow
    
    Args:
        governance_agent: The Data Governance Specialist agent
        dcam_agent: The DCAM Template Specialist agent
        tranch_agent: The Tranch Guidance Specialist agent
        query: The main query/topic for the workflow
        research_data: Research data from the first team
        conversation_history: Previous conversation context for continuity
        
    Returns:
        List[Task]: List of configured data strategy tasks
    """
    
    return create_data_strategy_tasks(governance_agent, dcam_agent, tranch_agent, research_data, query, conversation_history)


def create_tasks_dictionary(researcher_agent, analyst_agent, writer_agent, query: str, conversation_history: Optional[List[Any]] = None, use_tools: bool = True) -> dict:
    """
    Create all tasks and return them as a dictionary for easy access
    
    Args:
        researcher_agent: The Research Specialist agent
        analyst_agent: The Data Analyst agent
        writer_agent: The Content Writer agent
        query: The main query/topic for the workflow
        conversation_history: Previous conversation context for continuity
        use_tools: Whether to enable tool usage for the agents
        
    Returns:
        dict: Dictionary containing all tasks with descriptive keys
    """
    
    research_task, analysis_task, writing_task = create_crew_tasks(
        researcher_agent, analyst_agent, writer_agent, query, conversation_history, use_tools
    )
    
    return {
        'research': research_task,
        'analysis': analysis_task,
        'writing': writing_task,
        'research_task': research_task,    # Alternative key
        'analysis_task': analysis_task,    # Alternative key
        'writing_task': writing_task,      # Alternative key
        'all_tasks': [research_task, analysis_task, writing_task]
    }


def create_data_strategy_tasks_dictionary(governance_agent, dcam_agent, tranch_agent, query: str, research_data: str, conversation_history: Optional[List[Any]] = None) -> dict:
    """
    Create all data strategy tasks and return them as a dictionary for easy access
    
    Args:
        governance_agent: The Data Governance Specialist agent
        dcam_agent: The DCAM Template Specialist agent
        tranch_agent: The Tranch Guidance Specialist agent
        query: The main query/topic for the workflow
        research_data: Research data from the first team
        conversation_history: Previous conversation context for continuity
        
    Returns:
        dict: Dictionary containing all data strategy tasks with descriptive keys
    """
    
    governance_task, dcam_task, tranch_task = create_data_strategy_tasks(
        governance_agent, dcam_agent, tranch_agent, research_data, query, conversation_history
    )
    
    return {
        'governance': governance_task,
        'dcam': dcam_task,
        'tranch': tranch_task,
        'governance_task': governance_task,    # Alternative key
        'dcam_task': dcam_task,               # Alternative key
        'tranch_task': tranch_task,           # Alternative key
        'all_data_strategy_tasks': [governance_task, dcam_task, tranch_task]
    }


def create_compliance_risk_tasks_with_data(compliance_agent, risk_agent, audit_agent, query: str, data_strategy_data: str, conversation_history: Optional[List[Any]] = None) -> List[Any]:
    """
    Create all compliance and risk management tasks for the third team workflow
    
    Args:
        compliance_agent: The Compliance Specialist agent
        risk_agent: The Risk Management Specialist agent
        audit_agent: The Audit & Governance Specialist agent
        query: The main query/topic for the workflow
        data_strategy_data: Data strategy data from the second team
        conversation_history: Previous conversation context for continuity
        
    Returns:
        List[Task]: List of configured compliance and risk management tasks
    """
    
    return create_compliance_risk_tasks(compliance_agent, risk_agent, audit_agent, data_strategy_data, query, conversation_history)


def create_compliance_risk_tasks_dictionary(compliance_agent, risk_agent, audit_agent, query: str, data_strategy_data: str, conversation_history: Optional[List[Any]] = None) -> dict:
    """
    Create all compliance and risk management tasks and return them as a dictionary for easy access
    
    Args:
        compliance_agent: The Compliance Specialist agent
        risk_agent: The Risk Management Specialist agent
        audit_agent: The Audit & Governance Specialist agent
        query: The main query/topic for the workflow
        data_strategy_data: Data strategy data from the second team
        conversation_history: Previous conversation context for continuity
        
    Returns:
        dict: Dictionary containing all compliance and risk management tasks with descriptive keys
    """
    
    compliance_task, risk_task, audit_task = create_compliance_risk_tasks(
        compliance_agent, risk_agent, audit_agent, data_strategy_data, query, conversation_history
    )
    
    return {
        'compliance': compliance_task,
        'risk': risk_task,
        'audit': audit_task,
        'compliance_task': compliance_task,    # Alternative key
        'risk_task': risk_task,               # Alternative key
        'audit_task': audit_task,             # Alternative key
        'all_compliance_risk_tasks': [compliance_task, risk_task, audit_task]
    }


def create_information_management_tasks_with_data(info_governance_agent, metadata_agent, data_quality_agent, query: str, compliance_risk_data: str, conversation_history: Optional[List[Any]] = None) -> List[Any]:
    """
    Create all information management tasks for the fourth team workflow
    
    Args:
        info_governance_agent: The Information Governance Specialist agent
        metadata_agent: The Metadata Management Specialist agent
        data_quality_agent: The Data Quality Specialist agent
        query: The main query/topic for the workflow
        compliance_risk_data: Compliance and risk data from the third team
        conversation_history: Previous conversation context for continuity
        
    Returns:
        List[Task]: List of configured information management tasks
    """
    
    return create_information_management_tasks(info_governance_agent, metadata_agent, data_quality_agent, compliance_risk_data, query, conversation_history)


def create_information_management_tasks_dictionary(info_governance_agent, metadata_agent, data_quality_agent, query: str, compliance_risk_data: str, conversation_history: Optional[List[Any]] = None) -> dict:
    """
    Create all information management tasks and return them as a dictionary for easy access
    
    Args:
        info_governance_agent: The Information Governance Specialist agent
        metadata_agent: The Metadata Management Specialist agent
        data_quality_agent: The Data Quality Specialist agent
        query: The main query/topic for the workflow
        compliance_risk_data: Compliance and risk data from the third team
        conversation_history: Previous conversation context for continuity
        
    Returns:
        dict: Dictionary containing all information management tasks with descriptive keys
    """
    
    info_governance_task, metadata_task, data_quality_task = create_information_management_tasks(
        info_governance_agent, metadata_agent, data_quality_agent, compliance_risk_data, query, conversation_history
    )
    
    return {
        'information_governance': info_governance_task,
        'metadata_management': metadata_task,
        'data_quality': data_quality_task,
        'info_governance_task': info_governance_task,    # Alternative key
        'metadata_task': metadata_task,                 # Alternative key
        'data_quality_task': data_quality_task,         # Alternative key
        'all_information_management_tasks': [info_governance_task, metadata_task, data_quality_task]
    }


def create_tender_response_tasks_with_data(tender_specialist, proposal_writer, compliance_expert, information_management_data: str, query: str, conversation_history: Optional[List[Any]] = None) -> List[Any]:
    """
    Create tender response team tasks with data from previous team
    
    Args:
        tender_specialist: Tender response specialist agent
        proposal_writer: Proposal writer agent
        compliance_expert: Compliance expert agent
        information_management_data: Data from information management team
        query: User query
        conversation_history: Previous conversation context for continuity
        
    Returns:
        List[Task]: List of tender response tasks
    """
    
    tender_analysis_task, proposal_writing_task, compliance_verification_task = create_tender_response_tasks(
        tender_specialist, proposal_writer, compliance_expert, information_management_data, query, conversation_history
    )
    
    return [tender_analysis_task, proposal_writing_task, compliance_verification_task]


def create_project_delivery_tasks_with_data(data_engineer, data_scientist, data_architect, devops_engineer, project_manager, tender_response_data: str, query: str, conversation_history: Optional[List[Any]] = None) -> List[Any]:
    """
    Create project delivery team tasks with data from previous team
    
    Args:
        data_engineer: Data engineer agent
        data_scientist: Data scientist agent
        data_architect: Data architect agent
        devops_engineer: DevOps engineer agent
        project_manager: Project manager agent
        tender_response_data: Data from tender response team
        query: User query
        conversation_history: Previous conversation context for continuity
        
    Returns:
        List[Task]: List of project delivery tasks
    """
    
    data_engineering_task, data_science_task, data_architecture_task, devops_task, project_management_task = create_project_delivery_tasks(
        data_engineer, data_scientist, data_architect, devops_engineer, project_manager, tender_response_data, query, conversation_history
    )
    
    return [data_engineering_task, data_science_task, data_architecture_task, devops_task, project_management_task]


def create_technical_documentation_tasks_with_data(
    data_modeling_specialist,
    python_code_specialist,
    sql_code_specialist,
    pyspark_code_specialist,
    technical_writer,
    project_delivery_data: str,
    query: str,
    conversation_history: Optional[List[Any]] = None
) -> List[Any]:
    """
    Create technical documentation team tasks with data from previous team
    
    Args:
        data_modeling_specialist: Agent for creating data models and diagrams
        python_code_specialist: Agent for generating Python code
        sql_code_specialist: Agent for creating SQL queries and schemas
        pyspark_code_specialist: Agent for developing PySpark code
        technical_writer: Agent for creating technical documentation
        project_delivery_data: Output from the project delivery team
        query: Original user query
        conversation_history: Previous conversation context
        
    Returns:
        List[Task]: List of technical documentation tasks
    """
    
    data_modeling_task, python_code_task, sql_code_task, pyspark_code_task, technical_writing_task = create_technical_documentation_tasks(
        data_modeling_specialist, python_code_specialist, sql_code_specialist, 
        pyspark_code_specialist, technical_writer, project_delivery_data, query, conversation_history
    )
    
    return [data_modeling_task, python_code_task, sql_code_task, pyspark_code_task, technical_writing_task]
