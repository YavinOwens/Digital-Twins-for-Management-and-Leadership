"""
Compliance & Risk Management Team Tasks
Specialized tasks for regulatory compliance, risk management, and audit governance
"""

from crewai import Task
from typing import List, Optional, Any

def create_compliance_assessment_task(compliance_agent, data_strategy_data: str, query: str, conversation_history: Optional[List[Any]] = None) -> Task:
    """
    Create compliance assessment task focused on regulatory requirements
    """
    context_instruction = ""
    if conversation_history:
        context_instruction = f"\n\nPrevious conversation context: {conversation_history[-3:] if len(conversation_history) >= 3 else conversation_history}"
    
    task_description = f"""Conduct a comprehensive compliance assessment for: "{query}"
    {context_instruction}
    
    Based on the data strategy framework provided, develop a complete compliance assessment that includes:
    
    1. **Regulatory Mapping**: Map all data initiatives to relevant regulations (GDPR, CCPA, SOX, HIPAA, FERPA, etc.)
    2. **Compliance Gap Analysis**: Identify gaps between current state and regulatory requirements
    3. **Data Protection Impact Assessment (DPIA)**: Evaluate privacy risks and mitigation strategies
    4. **Consent Management Framework**: Design comprehensive consent collection and management processes
    5. **Data Subject Rights**: Implement frameworks for data access, rectification, erasure, and portability
    6. **Cross-Border Data Transfer**: Ensure compliance with international data transfer regulations
    7. **Breach Notification Procedures**: Develop incident response and notification protocols
    8. **Compliance Monitoring**: Create ongoing monitoring and reporting mechanisms
    9. **Training and Awareness**: Design compliance training programs for all stakeholders
    10. **Vendor Management**: Ensure third-party vendors meet compliance requirements
    
    Requirements:
    - Address all relevant regulations based on the data strategy scope
    - Include specific compliance checklists and assessment criteria
    - Provide implementation timelines and resource requirements
    - Include risk-based prioritization of compliance activities
    - Reference the data strategy framework for context and alignment
    - Include measurable compliance metrics and KPIs"""
    
    expected_output = """A comprehensive compliance assessment document (2500-3500 words) including:
    - Executive summary of compliance requirements and gaps
    - Detailed regulatory mapping with specific requirements
    - Comprehensive gap analysis with risk ratings
    - Data Protection Impact Assessment (DPIA) results
    - Consent management framework and procedures
    - Data subject rights implementation guide
    - Cross-border data transfer compliance procedures
    - Breach notification and incident response protocols
    - Compliance monitoring and reporting framework
    - Training and awareness program design
    - Vendor compliance management procedures
    - Implementation roadmap with timelines and resources
    - Compliance metrics and KPI framework
    - References to relevant regulations and standards"""
    
    return Task(
        description=task_description,
        expected_output=expected_output,
        agent=compliance_agent,
        timeout=200,  # 3.3 minute timeout
    )

def create_risk_assessment_task(risk_agent, data_strategy_data: str, query: str, conversation_history: Optional[List[Any]] = None) -> Task:
    """
    Create risk assessment task for comprehensive risk analysis
    """
    context_instruction = ""
    if conversation_history:
        context_instruction = f"\n\nPrevious conversation context: {conversation_history[-3:] if len(conversation_history) >= 3 else conversation_history}"
    
    task_description = f"""Conduct a comprehensive risk assessment for: "{query}"
    {context_instruction}
    
    Based on the data strategy framework provided, develop a complete risk assessment that includes:
    
    1. **Risk Identification**: Identify all potential risks across operational, technical, financial, and reputational domains
    2. **Risk Analysis**: Analyze probability, impact, and velocity of identified risks
    3. **Risk Evaluation**: Prioritize risks based on severity and likelihood
    4. **Risk Treatment Strategies**: Develop specific mitigation, transfer, acceptance, or avoidance strategies
    5. **Business Continuity Planning**: Design continuity plans for critical data operations
    6. **Cybersecurity Risk Assessment**: Evaluate and address cybersecurity threats and vulnerabilities
    7. **Operational Risk Management**: Address risks related to process failures and human error
    8. **Financial Risk Analysis**: Assess budget overruns, cost escalation, and ROI risks
    9. **Reputational Risk Management**: Address brand damage and stakeholder trust risks
    10. **Risk Monitoring and Reporting**: Establish ongoing risk monitoring and escalation procedures
    
    Requirements:
    - Use quantitative and qualitative risk assessment methodologies
    - Include specific risk mitigation strategies with implementation timelines
    - Address both internal and external risk factors
    - Provide risk appetite and tolerance guidelines
    - Include scenario planning and stress testing
    - Reference the data strategy framework for context and alignment
    - Include measurable risk metrics and monitoring procedures"""
    
    expected_output = """A comprehensive risk assessment document (2500-3500 words) including:
    - Executive summary of risk landscape and key findings
    - Detailed risk register with probability and impact assessments
    - Risk heat map and prioritization matrix
    - Specific risk treatment strategies and implementation plans
    - Business continuity and disaster recovery procedures
    - Cybersecurity risk assessment and mitigation strategies
    - Operational risk management framework
    - Financial risk analysis and budget contingency planning
    - Reputational risk management strategies
    - Risk monitoring and reporting framework
    - Risk appetite and tolerance guidelines
    - Scenario planning and stress testing results
    - Implementation roadmap with timelines and resources
    - Risk metrics and KPI framework
    - References to risk management standards and best practices"""
    
    return Task(
        description=task_description,
        expected_output=expected_output,
        agent=risk_agent,
        timeout=200,  # 3.3 minute timeout
    )

def create_audit_governance_task(audit_agent, data_strategy_data: str, query: str, conversation_history: Optional[List[Any]] = None) -> Task:
    """
    Create audit and governance task for oversight frameworks
    """
    context_instruction = ""
    if conversation_history:
        context_instruction = f"\n\nPrevious conversation context: {conversation_history[-3:] if len(conversation_history) >= 3 else conversation_history}"
    
    task_description = f"""Design comprehensive audit and governance frameworks for: "{query}"
    {context_instruction}
    
    Based on the data strategy framework provided, develop complete audit and governance oversight that includes:
    
    1. **Internal Audit Framework**: Design comprehensive internal audit programs and procedures
    2. **Governance Structure**: Establish governance committees and oversight mechanisms
    3. **Internal Controls**: Design and implement robust internal control systems
    4. **Compliance Monitoring**: Create ongoing compliance monitoring and testing procedures
    5. **Audit Trail Management**: Establish comprehensive audit trail and documentation requirements
    6. **Whistleblower Protection**: Implement confidential reporting and protection mechanisms
    7. **Third-Party Audits**: Design vendor and partner audit procedures
    8. **Regulatory Reporting**: Create regulatory reporting and disclosure frameworks
    9. **Continuous Improvement**: Establish feedback loops and continuous improvement processes
    10. **Board and Executive Reporting**: Design executive and board-level reporting mechanisms
    
    Requirements:
    - Align with internal audit standards and best practices
    - Include specific audit procedures and testing methodologies
    - Address both preventive and detective controls
    - Provide clear governance roles and responsibilities
    - Include audit scheduling and resource planning
    - Reference the data strategy framework for context and alignment
    - Include measurable audit metrics and success criteria"""
    
    expected_output = """A comprehensive audit and governance framework document (2500-3500 words) including:
    - Executive summary of audit and governance approach
    - Detailed internal audit framework and procedures
    - Governance structure with roles and responsibilities
    - Comprehensive internal controls design and implementation
    - Compliance monitoring and testing procedures
    - Audit trail management and documentation requirements
    - Whistleblower protection and reporting mechanisms
    - Third-party audit procedures and vendor management
    - Regulatory reporting and disclosure frameworks
    - Continuous improvement and feedback mechanisms
    - Board and executive reporting procedures
    - Audit scheduling and resource planning
    - Implementation roadmap with timelines and resources
    - Audit metrics and success criteria framework
    - References to audit standards and governance best practices"""
    
    return Task(
        description=task_description,
        expected_output=expected_output,
        agent=audit_agent,
        timeout=200,  # 3.3 minute timeout
    )

def create_compliance_risk_tasks(compliance_agent, risk_agent, audit_agent, data_strategy_data: str, query: str, conversation_history: Optional[List[Any]] = None) -> List[Task]:
    """
    Create all compliance and risk management tasks
    """
    return [
        create_compliance_assessment_task(compliance_agent, data_strategy_data, query, conversation_history),
        create_risk_assessment_task(risk_agent, data_strategy_data, query, conversation_history),
        create_audit_governance_task(audit_agent, data_strategy_data, query, conversation_history)
    ]


def create_compliance_risk_tasks_with_data(compliance_agent, risk_agent, audit_agent, data_strategy_data: str, query: str, conversation_history: Optional[List[Any]] = None) -> List[Task]:
    """
    Create compliance and risk management tasks with data from previous team.
    
    Args:
        compliance_agent: The compliance specialist agent
        risk_agent: The risk management specialist agent
        audit_agent: The audit & governance specialist agent
        data_strategy_data: Data from the data strategy team
        query: The user's query
        conversation_history: Previous conversation context
        
    Returns:
        List of tasks for the compliance and risk management team
    """
    
    return create_compliance_risk_tasks(compliance_agent, risk_agent, audit_agent, data_strategy_data, query, conversation_history)
