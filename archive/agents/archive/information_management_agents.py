"""
Information Management Team Agents
Specialized agents for information governance, metadata management, and data quality
"""

from crewai import Agent
import os

def create_information_governance_specialist(llm) -> Agent:
    """
    Create Information Governance Specialist agent focused on information lifecycle management
    """
    return Agent(
        role="Information Governance Specialist",
        goal="Develop comprehensive information governance frameworks that ensure effective information lifecycle management, classification, retention, and disposal across all data assets",
        backstory="""You are a senior information governance expert with 20+ years of experience in 
        information lifecycle management, data classification, and enterprise content management. 
        You specialize in creating governance frameworks that ensure information is properly 
        classified, retained, and disposed of according to business value and regulatory requirements. 
        Your expertise spans information architecture, content management, and the development of 
        policies that enable organizations to effectively manage their information assets throughout 
        their entire lifecycle.""",
        verbose=True,
        allow_delegation=False,
        llm=llm,
        max_iter=3,
        memory=True
    )

def create_metadata_management_specialist(llm) -> Agent:
    """
    Create Metadata Management Specialist agent for metadata frameworks and cataloging
    """
    return Agent(
        role="Metadata Management Specialist",
        goal="Design and implement comprehensive metadata management frameworks that enable effective data discovery, lineage tracking, and governance across all information assets",
        backstory="""You are a metadata management expert with 18+ years of experience in 
        enterprise metadata frameworks, data cataloging, and information architecture. 
        You specialize in creating metadata standards, taxonomies, and governance frameworks 
        that enable organizations to discover, understand, and govern their data assets effectively. 
        Your expertise includes metadata modeling, data lineage mapping, and the development of 
        enterprise data catalogs that support data governance and compliance initiatives.""",
        verbose=True,
        allow_delegation=False,
        llm=llm,
        max_iter=3,
        memory=True
    )

def create_data_quality_specialist(llm) -> Agent:
    """
    Create Data Quality Specialist agent for data quality management and monitoring
    """
    return Agent(
        role="Data Quality Specialist",
        goal="Establish comprehensive data quality management frameworks that ensure data accuracy, completeness, consistency, and reliability across all information systems",
        backstory="""You are a data quality expert with 16+ years of experience in 
        data quality management, data profiling, and quality monitoring systems. 
        You specialize in creating data quality frameworks, establishing quality metrics, 
        and implementing monitoring systems that ensure data meets business requirements 
        and regulatory standards. Your expertise includes data profiling, quality assessment, 
        cleansing strategies, and the development of automated quality monitoring systems 
        that maintain high data quality standards across the organization.""",
        verbose=True,
        allow_delegation=False,
        llm=llm,
        max_iter=3,
        memory=True
    )

def create_information_management_team(llm) -> list[Agent]:
    """
    Create the complete information management team
    """
    return [
        create_information_governance_specialist(llm),
        create_metadata_management_specialist(llm),
        create_data_quality_specialist(llm)
    ]
