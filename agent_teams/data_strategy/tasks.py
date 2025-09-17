"""
Data Strategy Team Tasks

This module contains the task definitions for the Data Strategy team.
"""

from crewai import Task
from typing import List, Optional, Any


def create_data_strategy_tasks(
    data_governance_specialist,
    dcam_template_specialist,
    tranch_guidance_specialist,
    query: str,
    previous_team_data: str,
    conversation_history: Optional[List[Any]] = None
) -> List[Task]:
    """
    Create Data Strategy team tasks.
    
    Args:
        data_governance_specialist: The data governance specialist agent
        dcam_template_specialist: The DCAM template specialist agent
        tranch_guidance_specialist: The tranch guidance specialist agent
        query: The user's query
        previous_team_data: Output from the previous team
        conversation_history: Previous conversation context
        
    Returns:
        List of tasks for the Data Strategy team
    """
    
    # Data Governance Task
    data_governance_task = Task(
        description=f"""
        Based on the research and analysis findings, create comprehensive DAMA-DMBOK frameworks 
        and data governance structures for the digital twin implementation.
        
        **Context from Previous Team:**
        {previous_team_data}
        
        **Original Query:** {query}
        
        **Your Task:**
        1. Analyze the research findings to identify data governance requirements
        2. Create DAMA-DMBOK aligned data governance frameworks
        3. Design data policies, procedures, and standards
        4. Establish data quality and compliance frameworks
        5. Define roles, responsibilities, and accountability structures
        
        **Deliverables:**
        - Data governance framework document
        - Data policies and procedures
        - Data quality standards
        - Compliance frameworks
        - Role and responsibility matrix
        """,
        expected_output="""
        Comprehensive data governance framework including:
        1. DAMA-DMBOK aligned governance structure
        2. Data policies and procedures
        3. Data quality standards and metrics
        4. Compliance and regulatory frameworks
        5. Role and responsibility definitions
        """,
        agent=data_governance_specialist
    )
    
    # DCAM Template Task
    dcam_template_task = Task(
        description=f"""
        Based on the data governance framework, develop Data Capability Assessment Model 
        templates and maturity frameworks for digital twin implementation.
        
        **Context from Previous Team:**
        {previous_team_data}
        
        **Original Query:** {query}
        
        **Your Task:**
        1. Create DCAM assessment templates
        2. Develop maturity models for data capabilities
        3. Design capability assessment frameworks
        4. Create evaluation criteria and scoring methods
        5. Develop improvement roadmaps based on assessments
        
        **Deliverables:**
        - DCAM assessment templates
        - Maturity model frameworks
        - Capability evaluation criteria
        - Scoring and rating systems
        - Improvement roadmap templates
        """,
        expected_output="""
        Complete DCAM framework including:
        1. Assessment templates and questionnaires
        2. Maturity model definitions
        3. Capability evaluation criteria
        4. Scoring and rating methodologies
        5. Improvement roadmap templates
        """,
        agent=dcam_template_specialist
    )
    
    # Tranch Guidance Task
    tranch_guidance_task = Task(
        description=f"""
        Based on the data governance and DCAM frameworks, design phased implementation 
        roadmaps and delivery tranches for digital twin implementation.
        
        **Context from Previous Team:**
        {previous_team_data}
        
        **Original Query:** {query}
        
        **Your Task:**
        1. Create phased implementation roadmap
        2. Design delivery tranches with clear milestones
        3. Develop project timelines and dependencies
        4. Identify risks and mitigation strategies
        5. Create stakeholder engagement plans
        
        **Deliverables:**
        - Phased implementation roadmap
        - Delivery tranche definitions
        - Project timeline and dependencies
        - Risk assessment and mitigation plans
        - Stakeholder engagement strategy
        """,
        expected_output="""
        Comprehensive implementation guidance including:
        1. Phased implementation roadmap
        2. Delivery tranche definitions and milestones
        3. Project timeline with dependencies
        4. Risk assessment and mitigation strategies
        5. Stakeholder engagement and change management plans
        """,
        agent=tranch_guidance_specialist
    )
    
    return [data_governance_task, dcam_template_task, tranch_guidance_task]


def create_data_strategy_tasks_with_data(
    data_governance_specialist,
    dcam_template_specialist,
    tranch_guidance_specialist,
    query: str,
    previous_team_data: str,
    conversation_history: Optional[List[Any]] = None
) -> List[Task]:
    """
    Create Data Strategy team tasks with data from previous team.
    
    Args:
        data_governance_specialist: The data governance specialist agent
        dcam_template_specialist: The DCAM template specialist agent
        tranch_guidance_specialist: The tranch guidance specialist agent
        query: The user's query
        previous_team_data: Output from the previous team
        conversation_history: Previous conversation context
        
    Returns:
        List of tasks for the Data Strategy team
    """
    
    return create_data_strategy_tasks(
        data_governance_specialist, dcam_template_specialist, tranch_guidance_specialist, 
        query, previous_team_data, conversation_history
    )
