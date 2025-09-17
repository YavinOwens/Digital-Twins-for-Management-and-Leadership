"""
Data Strategy Team Tasks
Specialized tasks for data governance, DCAM templates, and tranch guidance
"""

from crewai import Task
from typing import List, Optional, Any

def create_data_governance_task(governance_agent, research_data: str, query: str, conversation_history: Optional[List[Any]] = None) -> Task:
    """
    Create data governance task focused on DAMA principles
    """
    context_instruction = ""
    if conversation_history:
        context_instruction = f"\n\nPrevious conversation context: {conversation_history[-3:] if len(conversation_history) >= 3 else conversation_history}"
    
    task_description = f"""Create a comprehensive data governance framework for: "{query}"
    {context_instruction}
    
    Based on the research data provided, develop a complete data governance strategy that includes:
    
    1. **DAMA-DMBOK Alignment**: Map all governance activities to DAMA-DMBOK knowledge areas
    2. **Data Governance Charter**: Define governance structure, roles, and responsibilities
    3. **Data Policies & Standards**: Create specific policies for data quality, security, privacy, and lifecycle
    4. **Regulatory Compliance**: Ensure alignment with GDPR, CCPA, SOX, and other relevant regulations
    5. **Data Stewardship Framework**: Define data steward roles and accountability models
    6. **Data Quality Management**: Establish data quality standards, metrics, and monitoring processes
    7. **Data Security & Privacy**: Create security controls and privacy protection measures
    8. **Change Management**: Design governance change processes and approval workflows
    
    Requirements:
    - Align with DAMA-DMBOK 2.0 principles and knowledge areas
    - Include specific templates and frameworks for implementation
    - Address regulatory compliance requirements
    - Provide clear role definitions and accountability structures
    - Include measurable success metrics and KPIs
    - Reference the research data provided for context and industry best practices"""
    
    expected_output = """A comprehensive data governance framework document (2000-3000 words) including:
    - Executive summary of governance approach
    - DAMA-DMBOK knowledge area mapping
    - Detailed governance charter with roles and responsibilities
    - Specific data policies and standards
    - Regulatory compliance checklist and requirements
    - Data stewardship framework and accountability model
    - Data quality management processes and metrics
    - Security and privacy controls
    - Change management procedures
    - Implementation roadmap with timelines
    - Success metrics and monitoring framework
    - References to DAMA-DMBOK and regulatory sources"""
    
    return Task(
        description=task_description,
        expected_output=expected_output,
        agent=governance_agent,
        timeout=180,  # 3 minute timeout
    )

def create_dcam_template_task(dcam_agent, research_data: str, query: str, conversation_history: Optional[List[Any]] = None) -> Task:
    """
    Create DCAM template development task
    """
    context_instruction = ""
    if conversation_history:
        context_instruction = f"\n\nPrevious conversation context: {conversation_history[-3:] if len(conversation_history) >= 3 else conversation_history}"
    
    task_description = f"""Develop comprehensive DCAM (Data Capability Assessment Model) templates for: "{query}"
    {context_instruction}
    
    Based on the research data provided, create detailed DCAM templates that include:
    
    1. **Data Capability Assessment Framework**: Complete assessment model with scoring criteria
    2. **Maturity Level Definitions**: Clear definitions for each maturity level (0-5 scale)
    3. **Capability Gap Analysis**: Templates for identifying and prioritizing capability gaps
    4. **Data Architecture Templates**: Blueprints for data architecture components
    5. **Data Quality Templates**: Assessment and improvement templates for data quality
    6. **Data Security Templates**: Security assessment and implementation templates
    7. **Data Lifecycle Templates**: Management templates for data lifecycle stages
    8. **Implementation Roadmaps**: Detailed roadmaps for capability development
    9. **Success Metrics**: KPIs and measurement frameworks for each capability
    10. **Training Materials**: Templates for capability development training programs
    
    Requirements:
    - Align with DCAM framework and industry best practices
    - Include practical, implementable templates
    - Provide clear assessment criteria and scoring methods
    - Address both technical and organizational capabilities
    - Include change management and training components
    - Reference the research data for industry context and examples"""
    
    expected_output = """A comprehensive DCAM template package (2500-3500 words) including:
    - Executive summary of DCAM approach
    - Complete capability assessment framework with scoring matrix
    - Detailed maturity level definitions and criteria
    - Capability gap analysis templates and methodologies
    - Data architecture blueprint templates
    - Data quality assessment and improvement templates
    - Data security framework and assessment templates
    - Data lifecycle management templates
    - Implementation roadmap templates with timelines
    - Success metrics and KPI frameworks
    - Training and development templates
    - References to DCAM framework and industry standards"""
    
    return Task(
        description=task_description,
        expected_output=expected_output,
        agent=dcam_agent,
        timeout=180,  # 3 minute timeout
    )

def create_tranch_guidance_task(tranch_agent, research_data: str, query: str, conversation_history: Optional[List[Any]] = None) -> Task:
    """
    Create tranch guidance and implementation planning task
    """
    context_instruction = ""
    if conversation_history:
        context_instruction = f"\n\nPrevious conversation context: {conversation_history[-3:] if len(conversation_history) >= 3 else conversation_history}"
    
    task_description = f"""Design detailed implementation tranches for: "{query}"
    {context_instruction}
    
    Based on the research data provided, create comprehensive tranch guidance that includes:
    
    1. **Tranch Structure**: Define 3-5 implementation tranches with clear boundaries
    2. **Deliverable Specifications**: Detailed deliverables for each tranch
    3. **Timeline Planning**: Realistic timelines and dependencies for each tranch
    4. **Resource Requirements**: Human, technical, and financial resource needs
    5. **Risk Management**: Risk identification and mitigation strategies per tranch
    6. **Success Criteria**: Clear success metrics and acceptance criteria
    7. **Governance Framework**: Decision-making and approval processes
    8. **Change Management**: Organizational change and adoption strategies
    9. **Quality Assurance**: Testing and validation procedures
    10. **Monitoring & Reporting**: Progress tracking and reporting mechanisms
    
    Requirements:
    - Align with DAMA principles and best practices
    - Include specific, measurable deliverables
    - Address dependencies and critical path items
    - Provide realistic resource and timeline estimates
    - Include risk mitigation strategies
    - Reference the research data for industry context and lessons learned"""
    
    expected_output = """A comprehensive tranch guidance document (2000-3000 words) including:
    - Executive summary of tranch approach
    - Detailed tranch structure with boundaries and objectives
    - Specific deliverables and acceptance criteria for each tranch
    - Realistic timeline with dependencies and critical path
    - Resource requirements and allocation strategies
    - Risk management framework and mitigation plans
    - Success criteria and measurement frameworks
    - Governance and decision-making processes
    - Change management and adoption strategies
    - Quality assurance and testing procedures
    - Monitoring, reporting, and feedback mechanisms
    - References to DAMA principles and industry best practices"""
    
    return Task(
        description=task_description,
        expected_output=expected_output,
        agent=tranch_agent,
        timeout=180,  # 3 minute timeout
    )

def create_data_strategy_tasks(governance_agent, dcam_agent, tranch_agent, research_data: str, query: str, conversation_history: Optional[List[Any]] = None) -> List[Task]:
    """
    Create all data strategy tasks
    """
    return [
        create_data_governance_task(governance_agent, research_data, query, conversation_history),
        create_dcam_template_task(dcam_agent, research_data, query, conversation_history),
        create_tranch_guidance_task(tranch_agent, research_data, query, conversation_history)
    ]
