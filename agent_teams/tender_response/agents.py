"""
Tender Response Team Agents
Specialized agents for creating professional tender responses and proposals
"""

from crewai import Agent
from typing import Optional, List, Any

def create_tender_response_team(llm, conversation_history: Optional[List[Any]] = None, use_tools: bool = True) -> tuple:
    """
    Create tender response team agents
    
    Args:
        llm: The language model to use for all agents
        conversation_history: Previous conversation context for continuity
        use_tools: Whether to enable tool usage for the agents
        
    Returns:
        tuple: (tender_specialist, proposal_writer, compliance_expert)
    """
    
    # Tender Response Specialist
    tender_specialist = Agent(
        role="Tender Response Specialist",
        goal="Analyze tender requirements and create comprehensive response strategies that maximize win probability",
        backstory="""You are an expert tender response specialist with 15+ years of experience in the UK public sector, 
        particularly in education and technology procurement. You have successfully led responses to multi-million pound 
        tenders for digital transformation projects, data management systems, and educational technology initiatives. 
        Your expertise includes understanding complex procurement frameworks, scoring methodologies, and compliance 
        requirements. You excel at translating technical capabilities into compelling business value propositions 
        that resonate with procurement teams and decision-makers.""",
        verbose=True,
        allow_delegation=False,
        llm=llm,
        max_iter=3,
        max_rpm=5,
        max_execution_time=300,
        memory=False
    )
    
    # Proposal Writer
    proposal_writer = Agent(
        role="Proposal Writer",
        goal="Create compelling, well-structured tender responses that clearly articulate value propositions and technical solutions",
        backstory="""You are a senior proposal writer with extensive experience in technology and education sector 
        tenders. You have a unique ability to translate complex technical concepts into clear, persuasive language 
        that procurement evaluators can easily understand. Your writing style is professional, concise, and 
        compelling, with a focus on demonstrating clear value and competitive advantage. You excel at creating 
        executive summaries, technical specifications, and implementation plans that align with tender requirements 
        while highlighting unique differentiators.""",
        verbose=True,
        allow_delegation=False,
        llm=llm,
        max_iter=3,
        max_rpm=5,
        max_execution_time=300,
        memory=False
    )
    
    # Compliance Expert
    compliance_expert = Agent(
        role="Tender Compliance Expert",
        goal="Ensure all tender responses meet regulatory requirements, procurement standards, and evaluation criteria",
        backstory="""You are a compliance expert specializing in UK public sector procurement, particularly in 
        education and technology sectors. You have deep knowledge of Crown Commercial Service frameworks, 
        Public Contracts Regulations 2015, and sector-specific compliance requirements. Your expertise includes 
        GDPR compliance, accessibility standards, security requirements, and social value obligations. You ensure 
        that all tender responses are fully compliant with procurement regulations while maximizing scoring potential 
        through strategic compliance positioning.""",
        verbose=True,
        allow_delegation=False,
        llm=llm,
        max_iter=3,
        max_rpm=5,
        max_execution_time=300,
        memory=False
    )
    
    return tender_specialist, proposal_writer, compliance_expert


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
