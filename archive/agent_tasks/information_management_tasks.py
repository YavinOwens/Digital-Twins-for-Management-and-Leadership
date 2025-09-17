"""
Information Management Team Tasks
Specialized tasks for information governance, metadata management, and data quality
"""

from crewai import Task
from typing import List, Optional, Any

def create_information_governance_task(info_governance_agent, compliance_risk_data: str, query: str, conversation_history: Optional[List[Any]] = None) -> Task:
    """
    Create information governance task focused on information lifecycle management
    """
    context_instruction = ""
    if conversation_history:
        context_instruction = f"\n\nPrevious conversation context: {conversation_history[-3:] if len(conversation_history) >= 3 else conversation_history}"
    
    task_description = f"""Develop a comprehensive information governance framework for: "{query}"
    {context_instruction}
    
    Based on the compliance and risk management framework provided, create a complete information governance framework that includes:
    
    1. **Information Classification Framework**: Develop data classification schemes based on sensitivity, business value, and regulatory requirements
    2. **Information Lifecycle Management**: Design policies for creation, storage, access, retention, and disposal of information assets
    3. **Information Architecture**: Create enterprise information architecture that supports business processes and compliance requirements
    4. **Content Management Strategy**: Develop content management policies and procedures for structured and unstructured data
    5. **Information Security Controls**: Implement security controls based on information classification levels
    6. **Retention and Disposal Policies**: Create comprehensive retention schedules and secure disposal procedures
    7. **Information Access Management**: Design access control frameworks based on business roles and data sensitivity
    8. **Information Stewardship**: Establish information steward roles and responsibilities
    9. **Information Value Assessment**: Develop frameworks for assessing and maximizing information value
    10. **Information Governance Metrics**: Create KPIs and monitoring systems for information governance effectiveness
    
    Requirements:
    - Align with compliance and risk management frameworks
    - Address both structured and unstructured information
    - Include specific policies and procedures for implementation
    - Provide clear governance roles and responsibilities
    - Include information lifecycle workflows and decision trees
    - Reference the compliance and risk framework for context and alignment
    - Include measurable governance metrics and success criteria"""
    
    expected_output = """A comprehensive information governance framework document (2500-3500 words) including:
    - Executive summary of information governance approach and objectives
    - Detailed information classification framework with specific criteria
    - Comprehensive information lifecycle management policies and procedures
    - Enterprise information architecture design and principles
    - Content management strategy for structured and unstructured data
    - Information security controls based on classification levels
    - Retention and disposal policies with specific schedules
    - Information access management framework and procedures
    - Information stewardship roles and responsibilities
    - Information value assessment methodologies
    - Information governance metrics and KPI framework
    - Implementation roadmap with timelines and resources
    - Governance monitoring and reporting procedures
    - References to information governance standards and best practices"""
    
    return Task(
        description=task_description,
        expected_output=expected_output,
        agent=info_governance_agent,
        timeout=200,  # 3.3 minute timeout
    )

def create_metadata_management_task(metadata_agent, compliance_risk_data: str, query: str, conversation_history: Optional[List[Any]] = None) -> Task:
    """
    Create metadata management task for comprehensive metadata frameworks
    """
    context_instruction = ""
    if conversation_history:
        context_instruction = f"\n\nPrevious conversation context: {conversation_history[-3:] if len(conversation_history) >= 3 else conversation_history}"
    
    task_description = f"""Design and implement a comprehensive metadata management framework for: "{query}"
    {context_instruction}
    
    Based on the compliance and risk management framework provided, develop a complete metadata management system that includes:
    
    1. **Metadata Strategy**: Develop enterprise metadata strategy aligned with business objectives and compliance requirements
    2. **Metadata Standards**: Create metadata standards, schemas, and taxonomies for different data types
    3. **Data Catalog Design**: Design enterprise data catalog with search, discovery, and lineage capabilities
    4. **Metadata Governance**: Establish metadata governance policies and procedures
    5. **Data Lineage Management**: Implement data lineage tracking and impact analysis capabilities
    6. **Metadata Quality**: Ensure metadata accuracy, completeness, and consistency
    7. **Metadata Security**: Implement security controls for sensitive metadata
    8. **Metadata Integration**: Integrate metadata from various sources and systems
    9. **Metadata Analytics**: Develop metadata analytics and reporting capabilities
    10. **Metadata Tools and Technology**: Recommend metadata management tools and platforms
    
    Requirements:
    - Support both technical and business metadata
    - Enable data discovery and self-service analytics
    - Provide comprehensive data lineage tracking
    - Include metadata quality monitoring and validation
    - Address metadata security and access controls
    - Reference the compliance and risk framework for context and alignment
    - Include specific implementation guidelines and best practices"""
    
    expected_output = """A comprehensive metadata management framework document (2500-3500 words) including:
    - Executive summary of metadata management strategy and objectives
    - Detailed metadata standards and schemas for different data types
    - Enterprise data catalog design and architecture
    - Metadata governance policies and procedures
    - Data lineage management framework and procedures
    - Metadata quality management and validation processes
    - Metadata security controls and access management
    - Metadata integration strategies and procedures
    - Metadata analytics and reporting capabilities
    - Metadata management tools and technology recommendations
    - Implementation roadmap with timelines and resources
    - Metadata management metrics and KPI framework
    - References to metadata management standards and best practices"""
    
    return Task(
        description=task_description,
        expected_output=expected_output,
        agent=metadata_agent,
        timeout=200,  # 3.3 minute timeout
    )

def create_data_quality_task(data_quality_agent, compliance_risk_data: str, query: str, conversation_history: Optional[List[Any]] = None) -> Task:
    """
    Create data quality task for comprehensive data quality management
    """
    context_instruction = ""
    if conversation_history:
        context_instruction = f"\n\nPrevious conversation context: {conversation_history[-3:] if len(conversation_history) >= 3 else conversation_history}"
    
    task_description = f"""Establish a comprehensive data quality management framework for: "{query}"
    {context_instruction}
    
    Based on the compliance and risk management framework provided, develop a complete data quality management system that includes:
    
    1. **Data Quality Strategy**: Develop enterprise data quality strategy aligned with business objectives and compliance requirements
    2. **Data Quality Dimensions**: Define data quality dimensions (accuracy, completeness, consistency, timeliness, validity, uniqueness)
    3. **Data Quality Metrics**: Establish data quality metrics, thresholds, and measurement procedures
    4. **Data Profiling and Assessment**: Implement data profiling and quality assessment procedures
    5. **Data Quality Monitoring**: Create automated data quality monitoring and alerting systems
    6. **Data Cleansing and Remediation**: Develop data cleansing strategies and remediation procedures
    7. **Data Quality Governance**: Establish data quality governance policies and procedures
    8. **Data Quality Tools**: Recommend data quality tools and technology platforms
    9. **Data Quality Reporting**: Create data quality reporting and dashboard capabilities
    10. **Data Quality Training**: Develop data quality training and awareness programs
    
    Requirements:
    - Address all critical data quality dimensions
    - Include automated monitoring and alerting capabilities
    - Provide clear data quality standards and thresholds
    - Include data cleansing and remediation procedures
    - Address both technical and business data quality aspects
    - Reference the compliance and risk framework for context and alignment
    - Include specific implementation guidelines and success metrics"""
    
    expected_output = """A comprehensive data quality management framework document (2500-3500 words) including:
    - Executive summary of data quality strategy and objectives
    - Detailed data quality dimensions and measurement criteria
    - Data quality metrics framework with specific thresholds
    - Data profiling and assessment procedures and methodologies
    - Data quality monitoring and alerting system design
    - Data cleansing and remediation strategies and procedures
    - Data quality governance policies and procedures
    - Data quality tools and technology recommendations
    - Data quality reporting and dashboard capabilities
    - Data quality training and awareness program design
    - Implementation roadmap with timelines and resources
    - Data quality metrics and KPI framework
    - References to data quality management standards and best practices"""
    
    return Task(
        description=task_description,
        expected_output=expected_output,
        agent=data_quality_agent,
        timeout=200,  # 3.3 minute timeout
    )

def create_information_management_tasks(info_governance_agent, metadata_agent, data_quality_agent, compliance_risk_data: str, query: str, conversation_history: Optional[List[Any]] = None) -> List[Task]:
    """
    Create all information management tasks
    """
    return [
        create_information_governance_task(info_governance_agent, compliance_risk_data, query, conversation_history),
        create_metadata_management_task(metadata_agent, compliance_risk_data, query, conversation_history),
        create_data_quality_task(data_quality_agent, compliance_risk_data, query, conversation_history)
    ]
