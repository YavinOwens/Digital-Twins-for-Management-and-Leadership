"""
Geospatial Metadata Specialist Agent

This module contains the geospatial metadata specialist agent that handles
ISO 19115 metadata creation, validation, and management for geospatial data.
"""

from crewai import Agent
from typing import List, Optional, Any, Tuple, Dict
from agent_tools.iso19115_metadata_tool import (
    create_iso19115_metadata,
    validate_iso19115_metadata,
    extract_geospatial_metadata
)
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_geospatial_metadata_agent(llm, conversation_history: Optional[List[Any]] = None, use_tools: bool = True) -> Agent:
    """
    Create Geospatial Metadata Specialist Agent
    
    Args:
        llm: Language model instance
        conversation_history: Previous conversation context
        use_tools: Whether to include tools
        
    Returns:
        Geospatial Metadata Specialist Agent
    """
    
    # Define tools for geospatial metadata agent
    geospatial_tools = []
    if use_tools:
        geospatial_tools = [
            create_iso19115_metadata,
            validate_iso19115_metadata,
            extract_geospatial_metadata
        ]
    
    geospatial_agent = Agent(
        role="Geospatial Metadata Specialist",
        goal="Create, validate, and manage ISO 19115 metadata for geospatial data in the Digital Twin system",
        backstory="""You are an expert geospatial metadata specialist with extensive experience in 
        ISO 19115 metadata standards, geospatial data management, and spatial data interoperability. 
        You have deep knowledge of geographic information systems (GIS), spatial data formats, 
        coordinate reference systems, and metadata best practices.
        
        Your expertise includes:
        - ISO 19115 metadata standard implementation and validation
        - Geospatial data discovery and cataloging
        - Spatial data quality assessment and lineage tracking
        - Coordinate reference system (CRS) management
        - Spatial and temporal extent definition
        - Geospatial data interoperability and standards compliance
        - Spatial data infrastructure (SDI) development
        - Geographic information metadata modeling
        
        You understand the critical importance of proper metadata for geospatial data discovery, 
        access, and interoperability. You ensure that all geospatial data in the Digital Twin 
        system is properly documented, discoverable, and compliant with international standards.
        
        You work closely with data providers, GIS professionals, and system administrators to 
        ensure that geospatial metadata meets the highest standards of quality, completeness, 
        and compliance with ISO 19115 and related standards.""",
        verbose=True,
        allow_delegation=False,
        max_iter=3,
        memory=False,
        tools=geospatial_tools
    )
    
    return geospatial_agent


def create_geospatial_metadata_agents_with_context(llm, conversation_history: Optional[List[Any]] = None, use_tools: bool = True) -> Dict[str, Agent]:
    """
    Create Geospatial Metadata agents with conversation context
    
    Args:
        llm: Language model instance
        conversation_history: Previous conversation context
        use_tools: Whether to include tools
        
    Returns:
        Dictionary of geospatial metadata agents
    """
    
    # Create geospatial metadata agent
    geospatial_agent = create_geospatial_metadata_agent(llm, conversation_history, use_tools)
    
    # Add conversation context to agent's backstory
    if conversation_history:
        context_summary = f"""
        
        **Previous Conversation Context:**
        {conversation_history[-3:] if len(conversation_history) > 3 else conversation_history}
        
        Use this context to understand the geospatial metadata requirements and ensure consistency 
        with previous discussions about spatial data management and ISO 19115 compliance.
        """
        
        geospatial_agent.backstory += context_summary
    
    return {
        "geospatial_metadata_specialist": geospatial_agent
    }
