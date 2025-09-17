"""
Technical Documentation Agents for generating code, diagrams, and technical documentation
"""

from crewai import Agent
from typing import List, Optional, Any


def create_technical_documentation_team(llm) -> tuple:
    """
    Create technical documentation team agents that mirror the project delivery team
    but focus on generating technical documentation, code, and diagrams.
    
    Args:
        llm: The language model to use for all agents
        
    Returns:
        tuple: (data_modeling_specialist, python_code_specialist, sql_code_specialist, 
                pyspark_code_specialist, technical_writer)
    """
    
    # Data Modeling Specialist - Creates diagrams and data models
    data_modeling_specialist = Agent(
        role="Data Modeling Specialist",
        goal="Create comprehensive data models, entity relationship diagrams, and data architecture visualizations",
        backstory="""You are an expert data modeling specialist with extensive experience in creating 
        data models, ER diagrams, and data architecture documentation. You excel at translating 
        business requirements into clear, well-structured data models using tools like Mermaid, 
        PlantUML, or other diagramming languages. You understand database design principles, 
        normalization, and can create both conceptual and physical data models.""",
        verbose=True,
        allow_delegation=False,
        llm=llm,
        max_iter=3,
        max_rpm=5,
        max_execution_time=300,
        memory=False
    )
    
    # Python Code Specialist - Generates Python code and scripts
    python_code_specialist = Agent(
        role="Python Code Specialist",
        goal="Generate high-quality Python code, scripts, and data processing pipelines",
        backstory="""You are a senior Python developer with expertise in data engineering, 
        data science, and software development. You excel at writing clean, efficient, 
        and well-documented Python code for data processing, ETL pipelines, analytics, 
        and machine learning applications. You follow best practices, include proper 
        error handling, and create modular, reusable code.""",
        verbose=True,
        allow_delegation=False,
        llm=llm,
        max_iter=3,
        max_rpm=5,
        max_execution_time=300,
        memory=False
    )
    
    # SQL Code Specialist - Generates SQL queries and database scripts
    sql_code_specialist = Agent(
        role="SQL Code Specialist",
        goal="Create optimized SQL queries, database schemas, and data manipulation scripts",
        backstory="""You are a database expert with deep knowledge of SQL, database design, 
        and query optimization. You excel at writing complex SQL queries, creating database 
        schemas, and designing efficient data retrieval and manipulation scripts. You understand 
        different SQL dialects and can optimize queries for performance across various database 
        systems.""",
        verbose=True,
        allow_delegation=False,
        llm=llm,
        max_iter=3,
        max_rpm=5,
        max_execution_time=300,
        memory=False
    )
    
    # PySpark Code Specialist - Generates PySpark and big data processing code
    pyspark_code_specialist = Agent(
        role="PySpark Code Specialist",
        goal="Develop PySpark code for big data processing, analytics, and distributed computing",
        backstory="""You are a big data engineer with expertise in Apache Spark, PySpark, 
        and distributed computing. You excel at writing scalable PySpark code for data 
        processing, ETL operations, and analytics on large datasets. You understand 
        Spark optimization, RDD operations, DataFrame APIs, and can design efficient 
        distributed data processing pipelines.""",
        verbose=True,
        allow_delegation=False,
        llm=llm,
        max_iter=3,
        max_rpm=5,
        max_execution_time=300,
        memory=False
    )
    
    # Technical Writer - Creates comprehensive technical documentation
    technical_writer = Agent(
        role="Technical Writer",
        goal="Create comprehensive technical documentation, API docs, and implementation guides",
        backstory="""You are a technical writer with expertise in creating clear, comprehensive 
        technical documentation. You excel at writing API documentation, implementation guides, 
        code comments, and technical specifications. You understand software development 
        processes and can create documentation that is both technically accurate and 
        accessible to different audiences.""",
        verbose=True,
        allow_delegation=False,
        llm=llm,
        max_iter=3,
        max_rpm=5,
        max_execution_time=300,
        memory=False
    )
    
    return (
        data_modeling_specialist,
        python_code_specialist,
        sql_code_specialist,
        pyspark_code_specialist,
        technical_writer
    )


def create_technical_documentation_agents_with_context(llm, conversation_history: Optional[List[Any]] = None, use_tools: bool = True) -> dict:
    """
    Create technical documentation team agents and return them as a dictionary
    
    Args:
        llm: The language model to use for all agents
        conversation_history: Previous conversation context for continuity
        use_tools: Whether to enable tool usage for the agents
        
    Returns:
        dict: Dictionary containing technical documentation agents with descriptive keys
    """
    
    technical_docs_team = create_technical_documentation_team(llm)
    data_modeling_specialist, python_code_specialist, sql_code_specialist, pyspark_code_specialist, technical_writer = technical_docs_team
    
    return {
        'data_modeling_specialist': data_modeling_specialist,
        'python_code_specialist': python_code_specialist,
        'sql_code_specialist': sql_code_specialist,
        'pyspark_code_specialist': pyspark_code_specialist,
        'technical_writer': technical_writer,
        'data_modeler': data_modeling_specialist,           # Alternative key
        'python_developer': python_code_specialist,         # Alternative key
        'sql_developer': sql_code_specialist,               # Alternative key
        'pyspark_developer': pyspark_code_specialist,       # Alternative key
        'tech_writer': technical_writer                     # Alternative key
    }
