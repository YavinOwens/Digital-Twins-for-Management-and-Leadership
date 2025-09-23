# CrewAI Multi-Agent Workflow System - Technical Documentation Index

This is the comprehensive technical documentation index for the CrewAI Multi-Agent Workflow System. Use this index to navigate to specific documentation sections.

## Quick Navigation

- [System Overview](#system-overview)
- [Architecture Documentation](#architecture-documentation)
- [Module Documentation](#module-documentation)
- [Deployment Guides](#deployment-guides)
- [API Reference](#api-reference)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

## System Overview

### High-Level Architecture
- [Main README](../README.md) - Project overview and quick start
- [Architecture Diagram](../ARCHITECTURE.md) - Interactive system architecture
- [System Overview](README.md) - Detailed system overview

### Core Concepts
- **Multi-Agent Workflows**: 1-7 team sequential workflows
- **Memory System**: ChromaDB with local embeddings
- **LLM Integration**: Local Ollama + Ollama Cloud support
- **Modular Architecture**: Organized, maintainable codebase

## Architecture Documentation

### System Design
- [Architecture Overview](../ARCHITECTURE.md) - Interactive Mermaid diagram
- [Component Details](../ARCHITECTURE.md#component-details) - Detailed component descriptions
- [Data Flow](../ARCHITECTURE.md#data-flow) - System data flow patterns
- [Workflow Types](../ARCHITECTURE.md#workflow-types) - All 7 workflow configurations

### Technical Specifications
- [Memory System](memory_system/README.md) - ChromaDB and embedding details
- [Configuration Management](configuration/README.md) - Environment and security config
- [Deployment Architecture](deployment/README.md) - Deployment patterns and options

## Module Documentation

### Agent Teams
- [Agent Teams Overview](agent_teams/README.md) - All 7 agent teams
- [Framework Mapping](agent_teams/AGENT_TEAMS_FRAMEWORK_MAPPING.md) - Team frameworks and standards
- [Framework Diagrams](agent_teams/FRAMEWORK_MAPPING_DIAGRAMS.md) - Visual framework mappings
- [Research & Analysis](agent_teams/research_analysis.md) - Team 1 documentation
- [Data Strategy](agent_teams/data_strategy.md) - Team 2 documentation
- [Compliance & Risk](agent_teams/compliance_risk.md) - Team 3 documentation
- [Information Management](agent_teams/information_management.md) - Team 4 documentation
- [Tender Response](agent_teams/tender_response.md) - Team 5 documentation
- [Project Delivery](agent_teams/project_delivery.md) - Team 6 documentation
- [Technical Documentation](agent_teams/technical_documentation.md) - Team 7 documentation

### Workflows
- [Workflows Overview](workflows/README.md) - All workflow execution functions
- [Single Team Workflow](workflows/single_team_workflow.md) - Basic research workflow
- [Multi-Team Workflows](workflows/multi_team_workflow.md) - 2-7 team workflows
- [Execution Patterns](workflows/execution_patterns.md) - Workflow execution patterns

### Agent Tools
- [Agent Tools Overview](agent_tools/README.md) - All tools and utilities
- [LLM Wrappers](agent_tools/llm_wrappers.md) - RobustLLM and RetryLLM
- [Search Tools](agent_tools/search_tools.md) - Web search and DuckDuckGo
- [PDF Generation](agent_tools/pdf_generation.md) - PDF report generation

### UI Components
- [UI Components Overview](ui_components/README.md) - All Streamlit components
- [Component Details](ui_components/components.md) - Individual component documentation
- [Styling Guide](ui_components/styling.md) - UI styling and theming

## Deployment Guides

### Local Deployment
- [Local Setup](deployment/local_deployment.md) - Local development setup
- [Prerequisites](deployment/local_deployment.md#prerequisites) - System requirements
- [Installation](deployment/local_deployment.md#installation-steps) - Step-by-step installation
- [Configuration](deployment/local_deployment.md#configuration) - Local configuration

### Cloud Deployment
- [Cloud Setup](deployment/cloud_deployment.md) - Cloud deployment options
- [AWS Deployment](deployment/cloud_deployment.md#aws-deployment) - AWS-specific deployment
- [Docker Deployment](deployment/cloud_deployment.md#docker-deployment) - Containerized deployment
- [Kubernetes](deployment/cloud_deployment.md#kubernetes-deployment) - K8s deployment

### Monitoring & Observability
- [Monitoring Guide](deployment/monitoring.md) - Application monitoring
- [Health Checks](deployment/monitoring.md#health-checks) - System health monitoring
- [Performance Metrics](deployment/monitoring.md#performance-metrics) - Performance tracking
- [Logging](deployment/monitoring.md#logging) - Logging configuration

## API Reference

### Core APIs
- **Agent Teams**: [Agent Teams API](agent_teams/README.md#api-reference)
- **Workflows**: [Workflow API](workflows/README.md#api-reference)
- **Tools**: [Tools API](agent_tools/README.md#api-reference)
- **UI Components**: [UI API](ui_components/README.md#api-reference)

### Configuration APIs
- **Environment**: [Environment API](configuration/README.md#environment-variables)
- **Security**: [Security API](configuration/README.md#security-configuration)
- **Database**: [Database API](memory_system/README.md#database-configuration)

## Troubleshooting

### Common Issues
- [General Troubleshooting](../README.md#troubleshooting) - Common issues and solutions
- [Deployment Issues](deployment/README.md#troubleshooting) - Deployment-specific issues
- [Configuration Issues](configuration/README.md#troubleshooting) - Configuration problems
- [Memory Issues](memory_system/README.md#troubleshooting) - Memory system problems

### Debugging
- [Debug Scripts](deployment/README.md#debugging) - Debugging tools and scripts
- [Log Analysis](deployment/monitoring.md#log-analysis) - Log analysis techniques
- [Performance Debugging](deployment/monitoring.md#performance-debugging) - Performance issues

## Development

### Getting Started
- [Development Setup](README.md#development) - Development environment setup
- [Code Structure](README.md#architecture) - Codebase organization
- [Contributing Guidelines](README.md#contributing) - How to contribute

### Adding Features
- [New Agent Teams](agent_teams/README.md#extending-teams) - Adding new agent teams
- [New Workflows](workflows/README.md#extending-workflows) - Adding new workflows
- [New Tools](agent_tools/README.md#extending-tools) - Adding new tools
- [New UI Components](ui_components/README.md#extending-components) - Adding new UI components

### Testing
- [Testing Guide](README.md#testing) - Testing strategies
- [Unit Tests](agent_test_functions/README.md) - Unit testing
- [Integration Tests](workflows/README.md#testing) - Integration testing
- [End-to-End Tests](deployment/README.md#testing) - E2E testing

## Security

### Security Overview
- [Security Configuration](configuration/security.md) - Security settings
- [API Key Management](configuration/README.md#api-key-management) - Secure API key handling
- [Data Privacy](memory_system/README.md#data-privacy) - Data privacy considerations
- [Access Control](configuration/README.md#access-control) - User access control

### Best Practices
- [Security Best Practices](configuration/README.md#security-best-practices) - Security guidelines
- [Data Protection](memory_system/README.md#security-considerations) - Data protection
- [Secure Deployment](deployment/README.md#security) - Secure deployment practices

## Performance

### Optimization
- [Performance Tuning](deployment/README.md#performance-optimization) - Performance optimization
- [Caching Strategies](agent_tools/README.md#caching) - Caching implementation
- [Memory Management](memory_system/README.md#performance-optimization) - Memory optimization
- [Load Balancing](deployment/README.md#load-balancing) - Load balancing setup

### Monitoring
- [Performance Metrics](deployment/monitoring.md#performance-metrics) - Performance monitoring
- [Resource Usage](deployment/monitoring.md#resource-monitoring) - Resource monitoring
- [Alerting](deployment/monitoring.md#alerting) - Alert configuration

## Maintenance

### Updates
- [Version Updates](README.md#updates) - System updates
- [Dependency Updates](README.md#dependencies) - Dependency management
- [Security Updates](configuration/README.md#security-updates) - Security patches

### Backup & Recovery
- [Data Backup](memory_system/README.md#backup) - Data backup strategies
- [Configuration Backup](configuration/README.md#backup) - Configuration backup
- [Disaster Recovery](deployment/README.md#disaster-recovery) - Recovery procedures

## Support

### Getting Help
- [Documentation Issues](README.md#support) - Documentation problems
- [Technical Issues](README.md#troubleshooting) - Technical problems
- [Feature Requests](README.md#contributing) - Feature requests
- [Bug Reports](README.md#contributing) - Bug reporting

### Community
- [Contributing](README.md#contributing) - How to contribute
- [Code of Conduct](README.md#code-of-conduct) - Community guidelines
- [License](README.md#license) - License information

## Quick Reference

### Common Commands
```bash
# Start application
streamlit run streamlit_app.py

# Install dependencies
pip install -r local_requirements.txt

# Start Ollama
ollama serve

# Pull models
ollama pull llama3.1

# Check status
ollama list
```

### Key Files
- `streamlit_app.py` - Main application
- `.env` - Environment configuration
- `local_requirements.txt` - Dependencies
- `memory_db/` - ChromaDB storage
- `team_outputs/` - Generated outputs

### Important URLs
- Local Application: http://localhost:8501
- Ollama API: http://localhost:11434
- Ollama Cloud: https://api.ollama.ai

---

**Note**: This documentation is continuously updated. For the latest information, always refer to the main repository and the specific module documentation.
