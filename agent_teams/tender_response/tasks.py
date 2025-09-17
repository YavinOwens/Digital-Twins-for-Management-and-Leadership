"""
Tender Response Team Tasks
Specialized tasks for creating professional tender responses and proposals
"""

from crewai import Task
from typing import List, Optional, Any

def create_tender_analysis_task(tender_specialist, previous_team_data: str, query: str, conversation_history: Optional[List[Any]] = None) -> Task:
    """
    Create tender analysis task focused on understanding requirements and creating response strategy
    """
    context_instruction = ""
    if conversation_history:
        context_instruction = f"\n\nPrevious conversation context: {conversation_history[-3:] if len(conversation_history) >= 3 else conversation_history}"
    
    task_description = f"""Conduct a comprehensive tender analysis for: "{query}"
    {context_instruction}
    
    Based on the comprehensive digital twin strategy and implementation framework provided, develop a detailed tender analysis that includes:
    
    1. **Tender Requirements Analysis**: Break down the tender specification into key requirements, evaluation criteria, and scoring methodology
    2. **Competitive Positioning**: Analyze our strengths and unique value propositions compared to likely competitors
    3. **Compliance Mapping**: Map all technical and business requirements to our proposed solution components
    4. **Risk Assessment**: Identify potential risks and mitigation strategies for the tender response
    5. **Resource Requirements**: Define the team, timeline, and budget requirements for successful delivery
    6. **Value Proposition Development**: Create compelling value propositions that align with the client's strategic objectives
    7. **Technical Solution Mapping**: Map our digital twin capabilities to the specific tender requirements
    8. **Implementation Roadmap**: Develop a detailed implementation plan that addresses all tender requirements
    9. **Success Metrics**: Define measurable outcomes and KPIs that demonstrate value delivery
    10. **Partnership Strategy**: Identify key partnerships and subcontractors needed for successful delivery
    
    Requirements:
    - Address all tender requirements comprehensively
    - Highlight our competitive advantages and differentiators
    - Ensure alignment with the comprehensive strategy provided
    - Include specific technical and business capabilities
    - Provide clear implementation timelines and milestones
    - Include risk mitigation strategies
    - Reference the data strategy, compliance, and technical frameworks for context
    - Include measurable success criteria and value propositions"""
    
    expected_output = """A comprehensive tender analysis document (3000-4000 words) including:
    - Executive summary of tender requirements and our approach
    - Detailed requirements analysis with compliance mapping
    - Competitive positioning and unique value propositions
    - Technical solution architecture and capabilities mapping
    - Implementation roadmap with timelines and milestones
    - Resource requirements and team structure
    - Risk assessment and mitigation strategies
    - Success metrics and value delivery framework
    - Partnership strategy and key relationships
    - Budget estimates and cost breakdown
    - References to the comprehensive digital twin strategy framework"""
    
    return Task(
        description=task_description,
        expected_output=expected_output,
        agent=tender_specialist,
        timeout=200,  # 3.3 minute timeout
    )

def create_proposal_writing_task(proposal_writer, previous_team_data: str, query: str, conversation_history: Optional[List[Any]] = None) -> Task:
    """
    Create proposal writing task for creating compelling tender responses
    """
    context_instruction = ""
    if conversation_history:
        context_instruction = f"\n\nPrevious conversation context: {conversation_history[-3:] if len(conversation_history) >= 3 else conversation_history}"
    
    task_description = f"""Create a compelling tender response proposal for: "{query}"
    {context_instruction}
    
    Based on the comprehensive digital twin strategy and tender analysis provided, develop a professional tender response that includes:
    
    1. **Executive Summary**: Compelling overview of our solution and value proposition
    2. **Technical Approach**: Detailed technical methodology and implementation approach
    3. **Solution Architecture**: Comprehensive system design and integration strategy
    4. **Implementation Plan**: Phased delivery approach with clear milestones and deliverables
    5. **Project Management**: Detailed project governance, risk management, and quality assurance
    6. **Team Structure**: Key personnel, roles, responsibilities, and expertise
    7. **Innovation and Value**: Unique differentiators and innovative approaches
    8. **Compliance and Security**: Detailed compliance framework and security measures
    9. **Support and Maintenance**: Ongoing support strategy and service level agreements
    10. **Cost and Pricing**: Transparent pricing model and value for money proposition
    
    Requirements:
    - Write in a professional, compelling tone that resonates with procurement evaluators
    - Clearly articulate technical capabilities and business value
    - Address all tender requirements systematically
    - Include specific examples and case studies where relevant
    - Ensure compliance with procurement regulations and standards
    - Highlight competitive advantages and unique selling points
    - Provide clear timelines, deliverables, and success metrics
    - Reference the comprehensive strategy and technical frameworks
    - Include visual elements and structured formatting for clarity"""
    
    expected_output = """A comprehensive tender response proposal (4000-5000 words) including:
    - Executive summary with key value propositions
    - Detailed technical approach and methodology
    - Comprehensive solution architecture and integration strategy
    - Phased implementation plan with clear milestones
    - Project management framework and governance structure
    - Team structure with key personnel and expertise
    - Innovation highlights and competitive differentiators
    - Compliance framework and security measures
    - Support and maintenance strategy
    - Transparent pricing and value proposition
    - Appendices with technical specifications and references"""
    
    return Task(
        description=task_description,
        expected_output=expected_output,
        agent=proposal_writer,
        timeout=200,  # 3.3 minute timeout
    )

def create_compliance_verification_task(compliance_expert, previous_team_data: str, query: str, conversation_history: Optional[List[Any]] = None) -> Task:
    """
    Create compliance verification task for ensuring tender response meets all requirements
    """
    context_instruction = ""
    if conversation_history:
        context_instruction = f"\n\nPrevious conversation context: {conversation_history[-3:] if len(conversation_history) >= 3 else conversation_history}"
    
    task_description = f"""Conduct comprehensive compliance verification for: "{query}"
    {context_instruction}
    
    Based on the comprehensive digital twin strategy and tender response provided, perform detailed compliance verification that includes:
    
    1. **Regulatory Compliance Check**: Verify compliance with UK procurement regulations, GDPR, and sector-specific requirements
    2. **Technical Requirements Mapping**: Ensure all technical specifications meet tender requirements
    3. **Evaluation Criteria Alignment**: Map response content to evaluation criteria and scoring methodology
    4. **Documentation Completeness**: Verify all required documents, certifications, and evidence are included
    5. **Accessibility Standards**: Ensure compliance with accessibility requirements and inclusive design
    6. **Security Standards**: Verify adherence to security frameworks and data protection requirements
    7. **Quality Assurance**: Review response quality, consistency, and professional standards
    8. **Risk Assessment**: Identify compliance risks and mitigation strategies
    9. **Certification Requirements**: Verify all necessary certifications and accreditations are addressed
    10. **Submission Readiness**: Final checklist to ensure response is ready for submission
    
    Requirements:
    - Conduct thorough compliance verification against all tender requirements
    - Identify any gaps or non-compliance issues
    - Provide specific recommendations for improvement
    - Ensure alignment with procurement regulations and standards
    - Verify technical and business capability claims
    - Check documentation completeness and accuracy
    - Assess risk levels and mitigation strategies
    - Provide clear action items for final response preparation
    - Reference the comprehensive strategy and technical frameworks
    - Include compliance scoring and readiness assessment"""
    
    expected_output = """A comprehensive compliance verification report (2500-3000 words) including:
    - Executive summary of compliance status and readiness
    - Detailed regulatory compliance assessment
    - Technical requirements mapping and verification
    - Evaluation criteria alignment analysis
    - Documentation completeness review
    - Accessibility and security standards verification
    - Quality assurance assessment and recommendations
    - Risk assessment and mitigation strategies
    - Certification requirements verification
    - Final submission readiness checklist
    - Action items and improvement recommendations
    - Compliance scoring and overall assessment"""
    
    return Task(
        description=task_description,
        expected_output=expected_output,
        agent=compliance_expert,
        timeout=200,  # 3.3 minute timeout
    )

def create_tender_response_tasks(tender_specialist, proposal_writer, compliance_expert, previous_team_data: str, query: str, conversation_history: Optional[List[Any]] = None) -> List[Task]:
    """
    Create all tender response tasks
    """
    return [
        create_tender_analysis_task(tender_specialist, previous_team_data, query, conversation_history),
        create_proposal_writing_task(proposal_writer, previous_team_data, query, conversation_history),
        create_compliance_verification_task(compliance_expert, previous_team_data, query, conversation_history)
    ]


def create_tender_response_tasks_with_data(tender_specialist, proposal_writer, compliance_expert, previous_team_data: str, query: str, conversation_history: Optional[List[Any]] = None) -> List[Task]:
    """
    Create tender response tasks with data from previous team.
    
    Args:
        tender_specialist: The tender response specialist agent
        proposal_writer: The proposal writer agent
        compliance_expert: The compliance expert agent
        previous_team_data: Data from the previous team
        query: The user's query
        conversation_history: Previous conversation context
        
    Returns:
        List of tasks for the tender response team
    """
    
    return create_tender_response_tasks(tender_specialist, proposal_writer, compliance_expert, previous_team_data, query, conversation_history)
