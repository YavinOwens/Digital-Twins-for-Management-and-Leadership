"""
Data Strategy Team Agents
Specialized agents for data strategy, DAMA principles, DCAM templates, and tranch guidance
"""

from crewai import Agent
import os

def create_data_governance_specialist(llm) -> Agent:
    """
    Create Data Governance Specialist agent focused on DAMA principles
    """
    return Agent(
        role="Data Governance Specialist",
        goal="Create comprehensive data governance frameworks aligned with DAMA-DMBOK principles and ensure regulatory compliance",
        backstory="""You are a senior data governance expert with 15+ years of experience implementing 
        DAMA-DMBOK frameworks across various industries. You specialize in creating data governance 
        charters, policies, and procedures that ensure data quality, security, and compliance. 
        You have deep expertise in GDPR, CCPA, SOX, and other regulatory frameworks, and excel at 
        translating complex governance requirements into actionable implementation plans.""",
        verbose=True,
        allow_delegation=False,
        llm=llm,
        max_iter=3,
        memory=True
    )

def create_dcam_template_specialist(llm) -> Agent:
    """
    Create DCAM Template Specialist agent for data capability templates
    """
    return Agent(
        role="DCAM Template Specialist", 
        goal="Develop comprehensive Data Capability Assessment Model (DCAM) templates and maturity frameworks for data strategy implementation",
        backstory="""You are a data architecture and capability modeling expert with extensive experience 
        in DCAM frameworks, data maturity assessments, and capability gap analysis. You excel at creating 
        detailed templates for data capabilities, assessing organizational readiness, and designing 
        implementation roadmaps. Your expertise spans data architecture, data quality management, 
        data security, and data lifecycle management across enterprise environments.""",
        verbose=True,
        allow_delegation=False,
        llm=llm,
        max_iter=3,
        memory=True
    )

def create_tranch_guidance_specialist(llm) -> Agent:
    """
    Create Tranch Guidance Specialist agent for implementation phases
    """
    return Agent(
        role="Tranch Guidance Specialist",
        goal="Design detailed implementation tranches with specific deliverables, timelines, and success metrics aligned with DAMA principles",
        backstory="""You are a program management and implementation specialist with deep expertise in 
        data strategy execution and change management. You excel at breaking down complex data 
        initiatives into manageable tranches, creating detailed work breakdown structures, and 
        ensuring successful delivery through structured governance and monitoring. Your experience 
        spans enterprise data transformations, data platform implementations, and organizational 
        change management in data-driven environments.""",
        verbose=True,
        allow_delegation=False,
        llm=llm,
        max_iter=3,
        memory=True
    )

def create_data_strategy_team(llm) -> list[Agent]:
    """
    Create the complete data strategy team
    """
    return [
        create_data_governance_specialist(llm),
        create_dcam_template_specialist(llm),
        create_tranch_guidance_specialist(llm)
    ]
