"""
Project Delivery Team Agents
Technical specialists for implementing digital twin solutions
"""

from crewai import Agent
from typing import Optional, List, Any

def create_project_delivery_team(llm, conversation_history: Optional[List[Any]] = None, use_tools: bool = True) -> tuple:
    """
    Create project delivery team agents
    
    Args:
        llm: The language model to use for all agents
        conversation_history: Previous conversation context for continuity
        use_tools: Whether to enable tool usage for the agents
        
    Returns:
        tuple: (data_engineer, data_scientist, data_architect, devops_engineer, project_manager)
    """
    
    # Data Engineer
    data_engineer = Agent(
        role="Senior Data Engineer",
        goal="Design and implement robust data pipelines, ETL processes, and data infrastructure for digital twin systems",
        backstory="""You are a senior data engineer with 12+ years of experience in building scalable data platforms 
        for enterprise applications. You specialize in cloud-based data architectures, real-time streaming, and 
        batch processing systems. Your expertise includes Apache Spark, Kafka, Azure Data Factory, and modern 
        data lake architectures. You have successfully delivered complex data projects for educational institutions, 
        including student information systems, learning analytics platforms, and IoT data processing. You excel at 
        creating maintainable, scalable, and efficient data pipelines that can handle the high-volume, high-velocity 
        data requirements of digital twin systems.""",
        verbose=True,
        allow_delegation=False,
        llm=llm,
        max_iter=3,
        max_rpm=5,
        max_execution_time=300,
        memory=False
    )
    
    # Data Scientist
    data_scientist = Agent(
        role="Lead Data Scientist",
        goal="Develop advanced analytics models, machine learning algorithms, and predictive analytics for digital twin insights",
        backstory="""You are a lead data scientist with 10+ years of experience in applied machine learning and 
        statistical modeling. You specialize in time series analysis, predictive modeling, and real-time analytics 
        for complex systems. Your expertise includes Python, R, TensorFlow, PyTorch, and cloud ML platforms like 
        Azure ML and AWS SageMaker. You have extensive experience in educational analytics, including student 
        performance prediction, resource optimization, and behavioral analysis. You excel at translating business 
        requirements into sophisticated analytical models that provide actionable insights for digital twin systems.""",
        verbose=True,
        allow_delegation=False,
        llm=llm,
        max_iter=3,
        max_rpm=5,
        max_execution_time=300,
        memory=False
    )
    
    # Data Architect
    data_architect = Agent(
        role="Principal Data Architect",
        goal="Design comprehensive data architectures, data models, and integration strategies for digital twin ecosystems",
        backstory="""You are a principal data architect with 15+ years of experience in designing enterprise-scale 
        data architectures. You specialize in data modeling, API design, microservices architecture, and cloud 
        data platforms. Your expertise includes designing data lakes, data warehouses, and real-time analytics 
        platforms for complex organizations. You have extensive experience in education sector data architectures, 
        including student data management, learning analytics, and institutional reporting systems. You excel at 
        creating scalable, secure, and maintainable data architectures that support both current needs and future 
        growth of digital twin implementations.""",
        verbose=True,
        allow_delegation=False,
        llm=llm,
        max_iter=3,
        max_rpm=5,
        max_execution_time=300,
        memory=False
    )
    
    # DevOps Engineer
    devops_engineer = Agent(
        role="Senior DevOps Engineer",
        goal="Implement CI/CD pipelines, infrastructure as code, and operational monitoring for digital twin systems",
        backstory="""You are a senior DevOps engineer with 10+ years of experience in cloud infrastructure, 
        automation, and operational excellence. You specialize in containerization, Kubernetes, infrastructure 
        as code, and monitoring systems. Your expertise includes Azure DevOps, GitHub Actions, Terraform, and 
        comprehensive monitoring solutions. You have extensive experience in educational technology deployments, 
        including high-availability systems, disaster recovery, and security compliance. You excel at creating 
        robust, automated, and scalable infrastructure that supports digital twin systems with high reliability 
        and performance.""",
        verbose=True,
        allow_delegation=False,
        llm=llm,
        max_iter=3,
        max_rpm=5,
        max_execution_time=300,
        memory=False
    )
    
    # Project Manager
    project_manager = Agent(
        role="Technical Project Manager",
        goal="Coordinate technical delivery, manage resources, and ensure successful implementation of digital twin projects",
        backstory="""You are a technical project manager with 12+ years of experience in managing complex technology 
        implementations, particularly in the education sector. You specialize in agile methodologies, stakeholder 
        management, and technical project delivery. Your expertise includes managing cross-functional teams, 
        risk management, and delivery excellence. You have extensive experience in digital transformation projects, 
        including data platform implementations, analytics projects, and system integrations. You excel at 
        coordinating technical teams, managing project timelines, and ensuring successful delivery of complex 
        digital twin implementations.""",
        verbose=True,
        allow_delegation=False,
        llm=llm,
        max_iter=3,
        max_rpm=5,
        max_execution_time=300,
        memory=False
    )
    
    return data_engineer, data_scientist, data_architect, devops_engineer, project_manager


def create_project_delivery_agents_with_context(llm, conversation_history: Optional[List[Any]] = None, use_tools: bool = True) -> dict:
    """
    Create project delivery team agents and return them as a dictionary
    
    Args:
        llm: The language model to use for all agents
        conversation_history: Previous conversation context for continuity
        use_tools: Whether to enable tool usage for the agents
        
    Returns:
        dict: Dictionary containing project delivery agents with descriptive keys
    """
    
    project_delivery_team = create_project_delivery_team(llm)
    data_engineer, data_scientist, data_architect, devops_engineer, project_manager = project_delivery_team
    
    return {
        'data_engineer': data_engineer,
        'data_scientist': data_scientist,
        'data_architect': data_architect,
        'devops_engineer': devops_engineer,
        'project_manager': project_manager,
        'senior_data_engineer': data_engineer,      # Alternative key
        'lead_data_scientist': data_scientist,      # Alternative key
        'principal_data_architect': data_architect, # Alternative key
        'senior_devops_engineer': devops_engineer,  # Alternative key
        'technical_project_manager': project_manager # Alternative key
    }
