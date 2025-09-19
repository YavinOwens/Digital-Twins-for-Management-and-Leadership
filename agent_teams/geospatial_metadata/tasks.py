"""
Geospatial Metadata Tasks

This module contains task definitions for the Geospatial Metadata team.
"""

from crewai import Task
from typing import List, Optional, Any


def create_geospatial_metadata_tasks_with_data(
    geospatial_agent,
    query: str,
    geospatial_data: str,
    conversation_history: Optional[List[Any]] = None,
    document_context: Optional[str] = None
) -> List[Task]:
    """
    Create geospatial metadata tasks with geospatial data
    
    Args:
        geospatial_agent: Geospatial metadata specialist agent
        query: Original user query
        geospatial_data: Geospatial data to create metadata for
        conversation_history: Previous conversation context
        document_context: Document context from uploaded files
        
    Returns:
        List of geospatial metadata tasks
    """
    
    # Task 1: Geospatial Data Analysis and Metadata Extraction
    data_analysis_task = Task(
        description=f"""
        **TASK: Geospatial Data Analysis and Metadata Extraction**
        
        **Objective:** Analyze geospatial data to extract metadata information and identify spatial characteristics.
        
        **Geospatial Data to Analyze:**
        {geospatial_data}
        
        **Document Context:**
        {document_context if document_context else "No additional document context available"}
        
        **Instructions:**
        1. **Analyze the geospatial data** to identify spatial characteristics
        2. **Extract spatial extent information** (bounding box coordinates)
        3. **Identify temporal coverage** if available
        4. **Determine data type and format** (vector, raster, point cloud, etc.)
        5. **Extract thematic information** and keywords
        6. **Identify coordinate reference system** requirements
        7. **Assess spatial resolution** and scale
        8. **Extract data lineage information** and sources
        
        **Analysis Requirements:**
        - Identify spatial extent (west, east, south, north coordinates)
        - Determine temporal coverage (start and end dates)
        - Extract thematic keywords and categories
        - Identify coordinate reference system (CRS)
        - Assess spatial resolution and accuracy
        - Determine data quality and completeness
        - Extract data lineage and processing history
        
        **Output Requirements:**
        - Comprehensive geospatial data analysis report
        - Extracted metadata elements and values
        - Spatial extent definition with coordinates
        - Temporal coverage information
        - Thematic classification and keywords
        - Coordinate reference system specification
        - Data quality assessment
        - Recommendations for metadata creation
        
        **Quality Standards:**
        - Ensure accurate spatial extent calculation
        - Verify coordinate reference system identification
        - Validate temporal coverage information
        - Ensure comprehensive thematic classification
        - Maintain high standards of spatial data analysis
        """,
        expected_output="""A comprehensive geospatial data analysis report including:
        1. Spatial extent definition with coordinates
        2. Temporal coverage information
        3. Thematic classification and keywords
        4. Coordinate reference system specification
        5. Data quality assessment
        6. Recommendations for ISO 19115 metadata creation""",
        agent=geospatial_agent,
        context=[],
        output_file="geospatial_data_analysis.md"
    )
    
    # Task 2: ISO 19115 Metadata Creation
    metadata_creation_task = Task(
        description=f"""
        **TASK: ISO 19115 Metadata Creation**
        
        **Objective:** Create comprehensive ISO 19115 metadata records for the geospatial data.
        
        **Geospatial Data Analysis Results:**
        {geospatial_data}
        
        **Instructions:**
        1. **Create ISO 19115 metadata record** based on analysis results
        2. **Include all required elements** according to ISO 19115 standard
        3. **Add spatial extent information** with proper coordinate formatting
        4. **Include temporal coverage** if applicable
        5. **Add thematic keywords** and classification
        6. **Specify coordinate reference system** and projection
        7. **Include data quality information** and lineage
        8. **Add contact information** and data provider details
        
        **ISO 19115 Requirements:**
        - File identifier and language specification
        - Character set and hierarchy level
        - Contact information and date stamp
        - Metadata standard name and version
        - Identification information (title, abstract, keywords)
        - Spatial extent (geographic bounding box)
        - Temporal extent (if applicable)
        - Distribution information
        - Data quality information
        - Resource constraints and limitations
        
        **Output Requirements:**
        - Complete ISO 19115 XML metadata record
        - Validation report for the metadata
        - Metadata element documentation
        - Compliance assessment
        - Recommendations for metadata improvement
        
        **Quality Standards:**
        - Ensure full ISO 19115 compliance
        - Validate all required elements are present
        - Verify coordinate and temporal formatting
        - Ensure proper XML structure and namespaces
        - Maintain high standards of metadata quality
        """,
        expected_output="""A complete ISO 19115 metadata package including:
        1. XML metadata record
        2. Validation report
        3. Element documentation
        4. Compliance assessment
        5. Quality assurance summary""",
        agent=geospatial_agent,
        context=[data_analysis_task],
        output_file="iso19115_metadata.xml"
    )
    
    # Task 3: Metadata Validation and Quality Assurance
    validation_task = Task(
        description=f"""
        **TASK: Metadata Validation and Quality Assurance**
        
        **Objective:** Validate ISO 19115 metadata records and ensure quality and compliance.
        
        **ISO 19115 Metadata Record:**
        {geospatial_data}
        
        **Instructions:**
        1. **Validate ISO 19115 metadata** against standard requirements
        2. **Check XML structure** and namespace compliance
        3. **Verify required elements** are present and properly formatted
        4. **Validate coordinate information** and spatial extent
        5. **Check temporal information** formatting and validity
        6. **Verify keyword classification** and thematic accuracy
        7. **Assess data quality information** completeness
        8. **Generate validation report** with recommendations
        
        **Validation Criteria:**
        - XML structure and namespace compliance
        - Required elements presence and formatting
        - Coordinate reference system validity
        - Spatial extent coordinate accuracy
        - Temporal coverage format compliance
        - Keyword classification appropriateness
        - Data quality information completeness
        - Contact information validity
        
        **Output Requirements:**
        - Comprehensive validation report
        - Issue identification and resolution
        - Compliance assessment
        - Quality improvement recommendations
        - Final metadata certification
        
        **Quality Standards:**
        - Ensure 100% ISO 19115 compliance
        - Validate all coordinate and temporal information
        - Verify proper XML structure and formatting
        - Ensure comprehensive data quality information
        - Maintain highest standards of metadata quality
        """,
        expected_output="""A comprehensive validation report including:
        1. Validation status and compliance assessment
        2. Issue identification and resolution
        3. Quality improvement recommendations
        4. Final metadata certification
        5. Quality assurance summary""",
        agent=geospatial_agent,
        context=[data_analysis_task, metadata_creation_task],
        output_file="metadata_validation_report.md"
    )
    
    # Task 4: Geospatial Data Catalog Integration
    catalog_integration_task = Task(
        description=f"""
        **TASK: Geospatial Data Catalog Integration**
        
        **Objective:** Prepare geospatial metadata for integration into data catalogs and discovery systems.
        
        **Validated ISO 19115 Metadata:**
        {geospatial_data}
        
        **Instructions:**
        1. **Prepare metadata for catalog integration** and discovery
        2. **Create catalog-specific metadata** formats if needed
        3. **Generate discovery keywords** and search terms
        4. **Create data access information** and links
        5. **Prepare visualization metadata** for mapping services
        6. **Generate data service information** for web services
        7. **Create metadata summary** for quick reference
        8. **Prepare integration documentation** for system administrators
        
        **Catalog Integration Requirements:**
        - Discovery metadata optimization
        - Search keyword generation
        - Data access information
        - Visualization metadata
        - Web service information
        - Metadata summary creation
        - Integration documentation
        
        **Output Requirements:**
        - Catalog-ready metadata package
        - Discovery optimization report
        - Data access information
        - Integration documentation
        - System administrator guide
        
        **Quality Standards:**
        - Ensure optimal discoverability
        - Verify data access information accuracy
        - Ensure proper visualization metadata
        - Maintain comprehensive documentation
        - Ensure seamless catalog integration
        """,
        expected_output="""A complete catalog integration package including:
        1. Catalog-ready metadata
        2. Discovery optimization report
        3. Data access information
        4. Integration documentation
        5. System administrator guide""",
        agent=geospatial_agent,
        context=[data_analysis_task, metadata_creation_task, validation_task],
        output_file="catalog_integration_package.md"
    )
    
    return [
        data_analysis_task,
        metadata_creation_task,
        validation_task,
        catalog_integration_task
    ]


def create_geospatial_metadata_tasks(
    geospatial_agent,
    query: str,
    conversation_history: Optional[List[Any]] = None
) -> List[Task]:
    """
    Create geospatial metadata tasks without specific geospatial data
    
    Args:
        geospatial_agent: Geospatial metadata specialist agent
        query: Original user query
        conversation_history: Previous conversation context
        
    Returns:
        List of geospatial metadata tasks
    """
    
    # Task 1: Geospatial Metadata Framework Setup
    framework_task = Task(
        description=f"""
        **TASK: Geospatial Metadata Framework Setup**
        
        **Objective:** Establish geospatial metadata framework and standards for the Digital Twin system.
        
        **Query to Address:**
        {query}
        
        **Instructions:**
        1. **Analyze geospatial metadata requirements** for the Digital Twin system
        2. **Establish ISO 19115 compliance standards** and guidelines
        3. **Create metadata templates** for common geospatial data types
        4. **Define spatial data quality standards** and assessment criteria
        5. **Establish coordinate reference system** management procedures
        6. **Create metadata validation workflows** and quality assurance processes
        7. **Define data catalog integration** requirements and procedures
        
        **Framework Components:**
        - ISO 19115 compliance standards
        - Metadata templates and schemas
        - Spatial data quality criteria
        - Coordinate reference system management
        - Validation workflows and processes
        - Data catalog integration procedures
        - Quality assurance guidelines
        
        **Output Requirements:**
        - Geospatial metadata framework document
        - ISO 19115 compliance guidelines
        - Metadata templates and schemas
        - Quality assurance procedures
        - Integration documentation
        
        **Quality Standards:**
        - Ensure comprehensive framework coverage
        - Maintain ISO 19115 compliance
        - Provide clear guidelines and procedures
        - Ensure practical applicability
        - Maintain high standards of documentation
        """,
        expected_output="A comprehensive geospatial metadata framework and implementation guide",
        agent=geospatial_agent,
        context=[],
        output_file="geospatial_metadata_framework.md"
    )
    
    return [framework_task]
