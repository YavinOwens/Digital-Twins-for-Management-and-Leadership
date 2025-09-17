"""
Technical Documentation Tasks for generating code, diagrams, and technical documentation
"""

from crewai import Task
from typing import List, Optional, Any


def create_technical_documentation_tasks(
    data_modeling_specialist,
    python_code_specialist,
    sql_code_specialist,
    pyspark_code_specialist,
    technical_writer,
    project_delivery_data: str,
    query: str,
    conversation_history: Optional[List[Any]] = None
) -> tuple:
    """
    Create technical documentation team tasks that generate code, diagrams, and documentation
    based on project delivery team outputs.
    
    Args:
        data_modeling_specialist: Agent for creating data models and diagrams
        python_code_specialist: Agent for generating Python code
        sql_code_specialist: Agent for creating SQL queries and schemas
        pyspark_code_specialist: Agent for developing PySpark code
        technical_writer: Agent for creating technical documentation
        project_delivery_data: Output from the project delivery team
        query: Original user query
        conversation_history: Previous conversation context
        
    Returns:
        tuple: (data_modeling_task, python_code_task, sql_code_task, pyspark_code_task, technical_writing_task)
    """
    
    # Data Modeling Task
    data_modeling_task = Task(
        description=f"""
        Based on the project delivery team's technical specifications and architecture decisions, 
        create comprehensive data models and diagrams for the digital twin system.
        
        **Context from Project Delivery Team:**
        {project_delivery_data}
        
        **Original Query:** {query}
        
        **Your Task:**
        1. Analyze the technical architecture and data requirements from the project delivery team
        2. Create entity relationship diagrams (ERD) for the digital twin data model
        3. Design data flow diagrams showing how data moves through the system
        4. Create system architecture diagrams using Mermaid syntax
        5. Define data schemas and relationships between different data entities
        6. Include both conceptual and physical data models
        7. Ensure diagrams are clear, well-labeled, and follow standard notation
        
        **Deliverables:**
        - ERD diagrams in Mermaid format
        - Data flow diagrams
        - System architecture diagrams
        - Data schema definitions
        - Data model documentation
        
        **Format:** Provide all diagrams in Mermaid syntax and include detailed explanations.
        """,
        expected_output="""
        Comprehensive data modeling documentation including:
        1. Entity Relationship Diagrams (ERD) in Mermaid format
        2. Data flow diagrams showing system data movement
        3. System architecture diagrams
        4. Detailed data schema definitions
        5. Data model documentation with relationships and constraints
        6. Clear explanations of each diagram and its purpose
        """,
        agent=data_modeling_specialist
    )
    
    # Python Code Generation Task
    python_code_task = Task(
        description=f"""
        Based on the project delivery team's technical specifications, generate comprehensive 
        Python code for the digital twin system implementation.
        
        **Context from Project Delivery Team:**
        {project_delivery_data}
        
        **Original Query:** {query}
        
        **Your Task:**
        1. Analyze the technical requirements and architecture from the project delivery team
        2. Generate Python code for data processing pipelines and ETL operations
        3. Create Python scripts for data analytics and machine learning components
        4. Develop API endpoints and service classes for the digital twin system
        5. Include proper error handling, logging, and documentation
        6. Follow Python best practices and PEP 8 standards
        7. Create modular, reusable code with clear separation of concerns
        
        **Deliverables:**
        - Data processing pipeline scripts (.py files)
        - Analytics and ML model code
        - API service implementations
        - Configuration and utility modules
        - Unit tests and documentation
        
        **Format:** Provide complete Python files with proper imports, docstrings, and comments.
        """,
        expected_output="""
        Complete Python codebase including:
        1. Data processing pipeline scripts
        2. Analytics and machine learning modules
        3. API service implementations
        4. Configuration and utility modules
        5. Unit tests for critical functions
        6. Comprehensive docstrings and inline comments
        7. Requirements.txt with all dependencies
        """,
        agent=python_code_specialist
    )
    
    # SQL Code Generation Task
    sql_code_task = Task(
        description=f"""
        Based on the project delivery team's data architecture decisions, create comprehensive 
        SQL code for database operations and data management.
        
        **Context from Project Delivery Team:**
        {project_delivery_data}
        
        **Original Query:** {query}
        
        **Your Task:**
        1. Analyze the data requirements and architecture from the project delivery team
        2. Create database schema definitions (DDL) for all tables and relationships
        3. Generate SQL queries for data retrieval, analysis, and reporting
        4. Develop stored procedures and functions for complex data operations
        5. Create data migration scripts and version control procedures
        6. Include performance optimization and indexing strategies
        7. Ensure SQL code is compatible with multiple database systems
        
        **Deliverables:**
        - Database schema creation scripts (.sql files)
        - Data retrieval and analysis queries
        - Stored procedures and functions
        - Data migration scripts
        - Performance optimization recommendations
        
        **Format:** Provide complete SQL files with proper formatting and comments.
        """,
        expected_output="""
        Comprehensive SQL codebase including:
        1. Complete database schema definitions (DDL)
        2. Data retrieval and analysis queries
        3. Stored procedures and functions
        4. Data migration and version control scripts
        5. Performance optimization recommendations
        6. Indexing strategies and query optimization
        7. Database documentation and usage examples
        """,
        agent=sql_code_specialist
    )
    
    # PySpark Code Generation Task
    pyspark_code_task = Task(
        description=f"""
        Based on the project delivery team's big data requirements, generate comprehensive 
        PySpark code for distributed data processing and analytics.
        
        **Context from Project Delivery Team:**
        {project_delivery_data}
        
        **Original Query:** {query}
        
        **Your Task:**
        1. Analyze the big data processing requirements from the project delivery team
        2. Generate PySpark code for distributed data processing and ETL operations
        3. Create Spark applications for real-time and batch data processing
        4. Develop machine learning pipelines using Spark MLlib
        5. Implement data streaming and real-time analytics solutions
        6. Include proper error handling, monitoring, and performance optimization
        7. Follow Spark best practices and optimization techniques
        
        **Deliverables:**
        - PySpark ETL pipeline scripts (.py files)
        - Spark MLlib machine learning applications
        - Real-time streaming data processing code
        - Batch processing and analytics applications
        - Configuration and deployment scripts
        
        **Format:** Provide complete PySpark files with proper imports, documentation, and comments.
        """,
        expected_output="""
        Complete PySpark codebase including:
        1. Distributed ETL pipeline implementations
        2. Spark MLlib machine learning applications
        3. Real-time streaming data processing code
        4. Batch processing and analytics applications
        5. Configuration and deployment scripts
        6. Performance optimization and monitoring code
        7. Comprehensive documentation and usage examples
        """,
        agent=pyspark_code_specialist
    )
    
    # Technical Writing Task
    technical_writing_task = Task(
        description=f"""
        Based on all the technical outputs from previous teams, create comprehensive 
        technical documentation for the digital twin system.
        
        **Context from Project Delivery Team:**
        {project_delivery_data}
        
        **Original Query:** {query}
        
        **Your Task:**
        1. Synthesize all technical information from previous teams
        2. Create comprehensive technical documentation and implementation guides
        3. Develop API documentation with examples and usage instructions
        4. Write deployment and configuration guides
        5. Create troubleshooting and maintenance documentation
        6. Include code examples, diagrams, and step-by-step instructions
        7. Ensure documentation is clear, comprehensive, and accessible to different audiences
        
        **Deliverables:**
        - Technical implementation guide
        - API documentation
        - Deployment and configuration guide
        - Troubleshooting and maintenance manual
        - Code examples and usage instructions
        - Architecture overview documentation
        
        **Format:** Provide well-structured documentation in markdown format with clear sections and examples.
        """,
        expected_output="""
        Comprehensive technical documentation including:
        1. Complete technical implementation guide
        2. Detailed API documentation with examples
        3. Step-by-step deployment and configuration instructions
        4. Troubleshooting guide and common issues
        5. Maintenance and monitoring procedures
        6. Code examples and usage instructions
        7. Architecture overview and system design documentation
        """,
        agent=technical_writer
    )
    
    return (
        data_modeling_task,
        python_code_task,
        sql_code_task,
        pyspark_code_task,
        technical_writing_task
    )


def create_technical_documentation_tasks_with_data(
    data_modeling_specialist,
    python_code_specialist,
    sql_code_specialist,
    pyspark_code_specialist,
    technical_writer,
    project_delivery_data: str,
    query: str,
    conversation_history: Optional[List[Any]] = None
) -> List[Any]:
    """
    Create technical documentation team tasks with data from previous team
    
    Args:
        data_modeling_specialist: Agent for creating data models and diagrams
        python_code_specialist: Agent for generating Python code
        sql_code_specialist: Agent for creating SQL queries and schemas
        pyspark_code_specialist: Agent for developing PySpark code
        technical_writer: Agent for creating technical documentation
        project_delivery_data: Output from the project delivery team
        query: Original user query
        conversation_history: Previous conversation context
        
    Returns:
        List[Task]: List of technical documentation tasks
    """
    
    data_modeling_task, python_code_task, sql_code_task, pyspark_code_task, technical_writing_task = create_technical_documentation_tasks(
        data_modeling_specialist, python_code_specialist, sql_code_specialist, 
        pyspark_code_specialist, technical_writer, project_delivery_data, query, conversation_history
    )
    
    return [data_modeling_task, python_code_task, sql_code_task, pyspark_code_task, technical_writing_task]
