"""
Compliance & Risk Management Team Agents
Specialized agents for regulatory compliance, risk management, and audit governance
"""

from crewai import Agent
import os

def create_compliance_specialist(llm) -> Agent:
    """
    Create Compliance Specialist agent focused on regulatory compliance
    """
    return Agent(
        role="Compliance Specialist",
        goal="Ensure comprehensive regulatory compliance across all data initiatives and create detailed compliance frameworks for GDPR, CCPA, SOX, HIPAA, and other relevant regulations",
        backstory="""You are a senior compliance expert with 20+ years of experience in regulatory 
        compliance across multiple industries including healthcare, finance, education, and technology. 
        You specialize in GDPR, CCPA, SOX, HIPAA, FERPA, and other data protection regulations. 
        You excel at creating comprehensive compliance frameworks, conducting compliance assessments, 
        and developing implementation roadmaps that ensure organizations meet all regulatory 
        requirements while maintaining operational efficiency.""",
        verbose=True,
        allow_delegation=False,
        llm=llm,
        max_iter=3,
        max_rpm=5,
        max_execution_time=300,
        memory=False
    )

def create_risk_management_specialist(llm) -> Agent:
    """
    Create Risk Management Specialist agent for risk assessment and mitigation
    """
    return Agent(
        role="Risk Management Specialist",
        goal="Conduct comprehensive risk assessments and develop detailed risk mitigation strategies for data initiatives, including operational, technical, financial, and reputational risks",
        backstory="""You are a certified risk management professional (CRMP) with extensive experience 
        in enterprise risk management, cybersecurity risk assessment, and business continuity planning. 
        You specialize in identifying, analyzing, and mitigating risks across data governance, 
        technology implementation, and organizational change. Your expertise spans quantitative 
        risk analysis, scenario planning, and the development of robust risk management frameworks 
        that protect organizations while enabling innovation.""",
        verbose=True,
        allow_delegation=False,
        llm=llm,
        max_iter=3,
        max_rpm=5,
        max_execution_time=300,
        memory=False
    )

def create_audit_governance_specialist(llm) -> Agent:
    """
    Create Audit & Governance Specialist agent for audit frameworks and governance oversight
    """
    return Agent(
        role="Audit & Governance Specialist",
        goal="Design comprehensive audit frameworks and governance oversight mechanisms to ensure ongoing compliance monitoring, internal controls, and continuous improvement",
        backstory="""You are a certified internal auditor (CIA) and governance expert with 18+ years 
        of experience in internal auditing, compliance monitoring, and governance frameworks. 
        You specialize in designing audit programs, establishing internal controls, and creating 
        governance oversight mechanisms. Your expertise includes SOX compliance, internal audit 
        standards, and the development of continuous monitoring systems that ensure ongoing 
        compliance and risk mitigation across complex data initiatives.""",
        verbose=True,
        allow_delegation=False,
        llm=llm,
        max_iter=3,
        max_rpm=5,
        max_execution_time=300,
        memory=False
    )

def create_compliance_risk_team(llm) -> list[Agent]:
    """
    Create the complete compliance and risk management team
    """
    return [
        create_compliance_specialist(llm),
        create_risk_management_specialist(llm),
        create_audit_governance_specialist(llm)
    ]


def create_compliance_risk_agents_with_context(llm, conversation_history=None, use_tools: bool = True) -> dict:
    """
    Create Compliance & Risk team agents and return them as a dictionary.
    
    Args:
        llm: The language model to use for all agents
        conversation_history: Previous conversation context for continuity
        use_tools: Whether to enable tool usage for the agents
        
    Returns:
        dict: Dictionary containing compliance risk agents with descriptive keys
    """
    
    compliance_agent = create_compliance_specialist(llm)
    risk_agent = create_risk_management_specialist(llm)
    audit_agent = create_audit_governance_specialist(llm)
    
    return {
        'compliance_specialist': compliance_agent,
        'risk_management_specialist': risk_agent,
        'audit_governance_specialist': audit_agent,
        'compliance_agent': compliance_agent,  # Alternative key
        'risk_agent': risk_agent,              # Alternative key
        'audit_agent': audit_agent             # Alternative key
    }
