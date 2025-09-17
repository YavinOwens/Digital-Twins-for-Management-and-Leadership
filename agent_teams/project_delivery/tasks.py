"""
Project Delivery Team Tasks
Technical implementation tasks for digital twin solutions
"""

from crewai import Task
from typing import List, Optional, Any

def create_data_engineering_task(data_engineer, previous_team_data: str, query: str, conversation_history: Optional[List[Any]] = None) -> Task:
    """
    Create data engineering task for implementing data infrastructure
    """
    context_instruction = ""
    if conversation_history:
        context_instruction = f"\n\nPrevious conversation context: {conversation_history[-3:] if len(conversation_history) >= 3 else conversation_history}"
    
    task_description = f"""Design and implement comprehensive data engineering solutions for: "{query}"
    {context_instruction}
    
    Based on the comprehensive digital twin strategy and tender response provided, develop detailed data engineering specifications that include:
    
    1. **Data Architecture Design**: Design scalable data lake and warehouse architecture for digital twin data
    2. **ETL Pipeline Development**: Create robust data ingestion, transformation, and loading pipelines
    3. **Real-time Data Processing**: Implement streaming data processing for real-time digital twin updates
    4. **Data Quality Framework**: Establish data quality monitoring, validation, and cleansing processes
    5. **API Development**: Design and implement APIs for data access and integration
    6. **Data Security**: Implement comprehensive data security and access control measures
    7. **Performance Optimization**: Optimize data processing for high-volume, high-velocity data
    8. **Monitoring and Alerting**: Set up comprehensive monitoring and alerting systems
    9. **Documentation**: Create detailed technical documentation and operational procedures
    10. **Testing Strategy**: Develop comprehensive testing framework for data pipelines
    
    Requirements:
    - Design cloud-native, scalable data architecture
    - Implement modern data engineering best practices
    - Ensure high availability and fault tolerance
    - Include comprehensive security measures
    - Provide detailed technical specifications
    - Include performance optimization strategies
    - Reference the comprehensive strategy and technical frameworks
    - Include specific technology recommendations and implementation details
    - Provide clear deployment and operational procedures"""
    
    expected_output = """A comprehensive data engineering specification document (3500-4500 words) including:
    - Executive summary of data architecture and approach
    - Detailed data lake and warehouse architecture design
    - ETL pipeline specifications and implementation details
    - Real-time data processing architecture and streaming solutions
    - Data quality framework and monitoring systems
    - API design and integration specifications
    - Security architecture and access control measures
    - Performance optimization strategies and tuning
    - Monitoring, alerting, and operational procedures
    - Technical documentation and maintenance procedures
    - Testing strategy and quality assurance framework
    - Deployment guide and operational runbooks"""
    
    return Task(
        description=task_description,
        expected_output=expected_output,
        agent=data_engineer,
        timeout=200,  # 3.3 minute timeout
    )

def create_data_science_task(data_scientist, previous_team_data: str, query: str, conversation_history: Optional[List[Any]] = None) -> Task:
    """
    Create data science task for developing analytics and ML models
    """
    context_instruction = ""
    if conversation_history:
        context_instruction = f"\n\nPrevious conversation context: {conversation_history[-3:] if len(conversation_history) >= 3 else conversation_history}"
    
    task_description = f"""Develop advanced analytics and machine learning solutions for: "{query}"
    {context_instruction}
    
    Based on the comprehensive digital twin strategy and data engineering specifications provided, develop detailed data science specifications that include:
    
    1. **Analytics Framework**: Design comprehensive analytics framework for digital twin insights
    2. **Machine Learning Models**: Develop predictive models for various digital twin use cases
    3. **Real-time Analytics**: Implement real-time analytics and streaming analytics capabilities
    4. **Data Visualization**: Create interactive dashboards and visualization solutions
    5. **Model Management**: Establish MLOps practices for model development and deployment
    6. **Feature Engineering**: Design feature engineering pipelines for model inputs
    7. **Model Validation**: Implement comprehensive model validation and testing frameworks
    8. **Performance Monitoring**: Set up model performance monitoring and drift detection
    9. **A/B Testing**: Design experimentation framework for model and feature testing
    10. **Documentation**: Create detailed model documentation and usage guidelines
    
    Requirements:
    - Develop production-ready machine learning models
    - Implement modern MLOps practices and workflows
    - Ensure model interpretability and explainability
    - Include comprehensive model validation and testing
    - Provide detailed technical specifications and code examples
    - Include performance optimization and scaling strategies
    - Reference the comprehensive strategy and data engineering frameworks
    - Include specific algorithm recommendations and implementation details
    - Provide clear deployment and operational procedures"""
    
    expected_output = """A comprehensive data science specification document (3500-4500 words) including:
    - Executive summary of analytics approach and capabilities
    - Detailed analytics framework and methodology
    - Machine learning model specifications and algorithms
    - Real-time analytics architecture and streaming solutions
    - Data visualization and dashboard specifications
    - MLOps framework and model management processes
    - Feature engineering pipelines and data preparation
    - Model validation and testing frameworks
    - Performance monitoring and drift detection systems
    - A/B testing and experimentation framework
    - Technical documentation and model usage guidelines
    - Deployment guide and operational procedures"""
    
    return Task(
        description=task_description,
        expected_output=expected_output,
        agent=data_scientist,
        timeout=200,  # 3.3 minute timeout
    )

def create_data_architecture_task(data_architect, previous_team_data: str, query: str, conversation_history: Optional[List[Any]] = None) -> Task:
    """
    Create data architecture task for designing system architecture
    """
    context_instruction = ""
    if conversation_history:
        context_instruction = f"\n\nPrevious conversation context: {conversation_history[-3:] if len(conversation_history) >= 3 else conversation_history}"
    
    task_description = f"""Design comprehensive data architecture for: "{query}"
    {context_instruction}
    
    Based on the comprehensive digital twin strategy and technical specifications provided, develop detailed data architecture that includes:
    
    1. **System Architecture**: Design overall system architecture and component relationships
    2. **Data Models**: Create comprehensive data models and schemas for digital twin data
    3. **Integration Architecture**: Design integration patterns and API specifications
    4. **Security Architecture**: Implement comprehensive security and access control design
    5. **Scalability Design**: Design for horizontal and vertical scaling requirements
    6. **Disaster Recovery**: Implement disaster recovery and business continuity planning
    7. **Data Governance**: Establish data governance and metadata management frameworks
    8. **Technology Stack**: Define technology stack and platform requirements
    9. **Performance Architecture**: Design for high-performance and low-latency requirements
    10. **Documentation**: Create comprehensive architecture documentation and diagrams
    
    Requirements:
    - Design enterprise-grade, scalable architecture
    - Implement modern architectural patterns and best practices
    - Ensure high availability and fault tolerance
    - Include comprehensive security and compliance measures
    - Provide detailed technical specifications and diagrams
    - Include scalability and performance optimization strategies
    - Reference the comprehensive strategy and technical frameworks
    - Include specific technology recommendations and implementation details
    - Provide clear deployment and operational procedures"""
    
    expected_output = """A comprehensive data architecture specification document (4000-5000 words) including:
    - Executive summary of architecture approach and design principles
    - Detailed system architecture and component design
    - Comprehensive data models and schema specifications
    - Integration architecture and API design patterns
    - Security architecture and access control design
    - Scalability design and performance optimization
    - Disaster recovery and business continuity planning
    - Data governance and metadata management framework
    - Technology stack and platform requirements
    - Performance architecture and optimization strategies
    - Comprehensive documentation and architectural diagrams
    - Deployment guide and operational procedures"""
    
    return Task(
        description=task_description,
        expected_output=expected_output,
        agent=data_architect,
        timeout=200,  # 3.3 minute timeout
    )

def create_devops_task(devops_engineer, previous_team_data: str, query: str, conversation_history: Optional[List[Any]] = None) -> Task:
    """
    Create DevOps task for implementing infrastructure and deployment
    """
    context_instruction = ""
    if conversation_history:
        context_instruction = f"\n\nPrevious conversation context: {conversation_history[-3:] if len(conversation_history) >= 3 else conversation_history}"
    
    task_description = f"""Implement comprehensive DevOps and infrastructure solutions for: "{query}"
    {context_instruction}
    
    Based on the comprehensive digital twin strategy and technical specifications provided, develop detailed DevOps specifications that include:
    
    1. **Infrastructure as Code**: Implement infrastructure automation and configuration management
    2. **CI/CD Pipelines**: Design and implement continuous integration and deployment pipelines
    3. **Containerization**: Implement containerization strategy using Docker and Kubernetes
    4. **Monitoring and Observability**: Set up comprehensive monitoring, logging, and alerting
    5. **Security Operations**: Implement security monitoring and incident response procedures
    6. **Backup and Recovery**: Design backup and disaster recovery procedures
    7. **Performance Monitoring**: Implement application and infrastructure performance monitoring
    8. **Automation**: Automate operational tasks and deployment procedures
    9. **Documentation**: Create operational documentation and runbooks
    10. **Testing**: Implement infrastructure and deployment testing procedures
    
    Requirements:
    - Implement modern DevOps practices and automation
    - Ensure high availability and fault tolerance
    - Include comprehensive security and compliance measures
    - Provide detailed technical specifications and code examples
    - Include performance optimization and scaling strategies
    - Reference the comprehensive strategy and technical frameworks
    - Include specific technology recommendations and implementation details
    - Provide clear deployment and operational procedures"""
    
    expected_output = """A comprehensive DevOps specification document (3000-4000 words) including:
    - Executive summary of DevOps approach and automation strategy
    - Detailed infrastructure as code specifications
    - CI/CD pipeline design and implementation details
    - Containerization strategy and Kubernetes deployment
    - Monitoring and observability framework
    - Security operations and incident response procedures
    - Backup and disaster recovery planning
    - Performance monitoring and optimization strategies
    - Automation framework and operational procedures
    - Technical documentation and operational runbooks
    - Testing strategy and quality assurance framework
    - Deployment guide and operational procedures"""
    
    return Task(
        description=task_description,
        expected_output=expected_output,
        agent=devops_engineer,
        timeout=200,  # 3.3 minute timeout
    )

def create_project_management_task(project_manager, previous_team_data: str, query: str, conversation_history: Optional[List[Any]] = None) -> Task:
    """
    Create project management task for coordinating technical delivery
    """
    context_instruction = ""
    if conversation_history:
        context_instruction = f"\n\nPrevious conversation context: {conversation_history[-3:] if len(conversation_history) >= 3 else conversation_history}"
    
    task_description = f"""Develop comprehensive project management framework for: "{query}"
    {context_instruction}
    
    Based on the comprehensive digital twin strategy and technical specifications provided, develop detailed project management specifications that include:
    
    1. **Project Governance**: Establish project governance structure and decision-making processes
    2. **Resource Management**: Define resource allocation, team structure, and skill requirements
    3. **Timeline and Milestones**: Create detailed project timeline with key milestones and deliverables
    4. **Risk Management**: Implement comprehensive risk management and mitigation strategies
    5. **Quality Assurance**: Establish quality assurance processes and testing frameworks
    6. **Communication Plan**: Design stakeholder communication and reporting procedures
    7. **Change Management**: Implement change management and configuration control processes
    8. **Budget Management**: Establish budget tracking and cost control procedures
    9. **Stakeholder Management**: Define stakeholder engagement and expectation management
    10. **Documentation**: Create project documentation and knowledge management procedures
    
    Requirements:
    - Implement agile project management methodologies
    - Ensure clear governance and decision-making processes
    - Include comprehensive risk management and mitigation
    - Provide detailed project specifications and procedures
    - Include stakeholder engagement and communication strategies
    - Reference the comprehensive strategy and technical frameworks
    - Include specific project management tools and techniques
    - Provide clear project delivery and operational procedures"""
    
    expected_output = """A comprehensive project management specification document (3000-4000 words) including:
    - Executive summary of project management approach and governance
    - Detailed project governance structure and processes
    - Resource management and team allocation strategy
    - Project timeline with milestones and deliverables
    - Risk management framework and mitigation strategies
    - Quality assurance processes and testing frameworks
    - Communication plan and stakeholder engagement strategy
    - Change management and configuration control procedures
    - Budget management and cost control framework
    - Stakeholder management and expectation setting
    - Project documentation and knowledge management
    - Project delivery guide and operational procedures"""
    
    return Task(
        description=task_description,
        expected_output=expected_output,
        agent=project_manager,
        timeout=200,  # 3.3 minute timeout
    )

def create_project_delivery_tasks(data_engineer, data_scientist, data_architect, devops_engineer, project_manager, previous_team_data: str, query: str, conversation_history: Optional[List[Any]] = None) -> List[Task]:
    """
    Create all project delivery tasks
    """
    return [
        create_data_engineering_task(data_engineer, previous_team_data, query, conversation_history),
        create_data_science_task(data_scientist, previous_team_data, query, conversation_history),
        create_data_architecture_task(data_architect, previous_team_data, query, conversation_history),
        create_devops_task(devops_engineer, previous_team_data, query, conversation_history),
        create_project_management_task(project_manager, previous_team_data, query, conversation_history)
    ]


def create_project_delivery_tasks_with_data(data_engineer, data_scientist, data_architect, devops_engineer, project_manager, previous_team_data: str, query: str, conversation_history: Optional[List[Any]] = None) -> List[Task]:
    """
    Create project delivery tasks with data from previous team.
    
    Args:
        data_engineer: The data engineer agent
        data_scientist: The data scientist agent
        data_architect: The data architect agent
        devops_engineer: The DevOps engineer agent
        project_manager: The project manager agent
        previous_team_data: Data from the previous team
        query: The user's query
        conversation_history: Previous conversation context
        
    Returns:
        List of tasks for the project delivery team
    """
    
    return create_project_delivery_tasks(data_engineer, data_scientist, data_architect, devops_engineer, project_manager, previous_team_data, query, conversation_history)
