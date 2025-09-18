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
- [System Overview](README.md) - Detailed system overview {todo}

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
- [Research & Analysis](agent_teams/research_analysis.md) - Team 1 documentation {todo}
- [Data Strategy](agent_teams/data_strategy.md) - Team 2 documentation {todo}
- [Compliance & Risk](agent_teams/compliance_risk.md) - Team 3 documentation {todo}
- [Information Management](agent_teams/information_management.md) - Team 4 documentation {todo}
- [Tender Response](agent_teams/tender_response.md) - Team 5 documentation {todo}
- [Project Delivery](agent_teams/project_delivery.md) - Team 6 documentation {todo}
- [Technical Documentation](agent_teams/technical_documentation.md) - Team 7 documentation {todo}

### Workflows
- [Workflows Overview](workflows/README.md) - All workflow execution functions
- [Single Team Workflow](workflows/single_team.md) - Basic research workflow {todo}
- [Multi-Team Workflows](workflows/multi_team.md) - 2-7 team workflows {todo}
- [Execution Patterns](workflows/execution_patterns.md) - Workflow execution patterns {todo}

### Agent Tools
- [Agent Tools Overview](agent_tools/README.md) - All tools and utilities
- [LLM Wrappers](agent_tools/llm_wrappers.md) - RobustLLM and RetryLLM {todo}
- [Search Tools](agent_tools/search_tools.md) - Web search and DuckDuckGo {todo}
- [PDF Generation](agent_tools/pdf_generation.md) - PDF report generation {todo}

### UI Components
- [UI Components Overview](ui_components/README.md) - All Streamlit components
- [Component Details](ui_components/components.md) - Individual component documentation {todo}
- [Styling Guide](ui_components/styling.md) - UI styling and theming {todo}

## Deployment Guides

### Local Deployment
- [Local Setup](deployment/local_deployment.md) - Local development setup {todo}
- [Prerequisites](deployment/local_deployment.md#prerequisites) - System requirements {todo}
- [Installation](deployment/local_deployment.md#installation-steps) - Step-by-step installation {todo}
- [Configuration](deployment/local_deployment.md#configuration) - Local configuration {todo}

### Cloud Deployment
- [Cloud Setup](deployment/cloud_deployment.md) - Cloud deployment options {todo}
- [AWS Deployment](deployment/cloud_deployment.md#aws-deployment) - AWS-specific deployment {todo}
- [Docker Deployment](deployment/cloud_deployment.md#docker-deployment) - Containerized deployment {todo}
- [Kubernetes](deployment/cloud_deployment.md#kubernetes-deployment) - K8s deployment {todo}

### Monitoring & Observability
- [Monitoring Guide](deployment/monitoring.md) - Application monitoring {todo}
- [Health Checks](deployment/monitoring.md#health-checks) - System health monitoring {todo}
- [Performance Metrics](deployment/monitoring.md#performance-metrics) - Performance tracking {todo}
- [Logging](deployment/monitoring.md#logging) - Logging configuration {todo}

## API Reference

### Core APIs
- **Agent Teams**: [Agent Teams API](agent_teams/README.md#api-reference) {todo}
- **Workflows**: [Workflow API](workflows/README.md#api-reference) {todo}
- **Tools**: [Tools API](agent_tools/README.md#api-reference) {todo}
- **UI Components**: [UI API](ui_components/README.md#api-reference) {todo}

### Configuration APIs
- **Environment**: [Environment API](configuration/README.md#environment-variables) {todo}
- **Security**: [Security API](configuration/README.md#security-configuration) {todo}
- **Database**: [Database API](memory_system/README.md#database-configuration) {todo}

## Troubleshooting

### Common Issues
- [General Troubleshooting](../README.md#troubleshooting) - Common issues and solutions
- [Deployment Issues](deployment/README.md#troubleshooting) - Deployment-specific issues {todo}
- [Configuration Issues](configuration/README.md#troubleshooting) - Configuration problems {todo}
- [Memory Issues](memory_system/README.md#troubleshooting) - Memory system problems {todo}

### Debugging
- [Debug Scripts](deployment/README.md#debugging) - Debugging tools and scripts {todo}
- [Log Analysis](deployment/monitoring.md#log-analysis) - Log analysis techniques {todo}
- [Performance Debugging](deployment/monitoring.md#performance-debugging) - Performance issues {todo}

## Development

### Getting Started
- [Development Setup](README.md#development) - Development environment setup {todo}
- [Code Structure](README.md#architecture) - Codebase organization {todo}
- [Contributing Guidelines](README.md#contributing) - How to contribute {todo}

### Adding Features
- [New Agent Teams](agent_teams/README.md#extending-teams) - Adding new agent teams {todo}
- [New Workflows](workflows/README.md#extending-workflows) - Adding new workflows {todo}
- [New Tools](agent_tools/README.md#extending-tools) - Adding new tools {todo}
- [New UI Components](ui_components/README.md#extending-components) - Adding new UI components {todo}

### Testing
- [Testing Guide](README.md#testing) - Testing strategies {todo}
- [Unit Tests](agent_test_functions/README.md) - Unit testing
- [Integration Tests](workflows/README.md#testing) - Integration testing {todo}
- [End-to-End Tests](deployment/README.md#testing) - E2E testing {todo}

## Security

### Security Overview
- [Security Configuration](configuration/security.md) - Security settings {todo}
- [API Key Management](configuration/README.md#api-key-management) - Secure API key handling {todo}
- [Data Privacy](memory_system/README.md#data-privacy) - Data privacy considerations {todo}
- [Access Control](configuration/README.md#access-control) - User access control {todo}

### Best Practices
- [Security Best Practices](configuration/README.md#security-best-practices) - Security guidelines {todo}
- [Data Protection](memory_system/README.md#security-considerations) - Data protection {todo}
- [Secure Deployment](deployment/README.md#security) - Secure deployment practices {todo}

## Performance

### Optimization
- [Performance Tuning](deployment/README.md#performance-optimization) - Performance optimization {todo}
- [Caching Strategies](agent_tools/README.md#caching) - Caching implementation {todo}
- [Memory Management](memory_system/README.md#performance-optimization) - Memory optimization {todo}
- [Load Balancing](deployment/README.md#load-balancing) - Load balancing setup {todo}

### Monitoring
- [Performance Metrics](deployment/monitoring.md#performance-metrics) - Performance monitoring {todo}
- [Resource Usage](deployment/monitoring.md#resource-monitoring) - Resource monitoring {todo}
- [Alerting](deployment/monitoring.md#alerting) - Alert configuration {todo}

## Maintenance

### Updates
- [Version Updates](README.md#updates) - System updates {todo}
- [Dependency Updates](README.md#dependencies) - Dependency management {todo}
- [Security Updates](configuration/README.md#security-updates) - Security patches {todo}

### Backup & Recovery
- [Data Backup](memory_system/README.md#backup) - Data backup strategies {todo}
- [Configuration Backup](configuration/README.md#backup) - Configuration backup {todo}
- [Disaster Recovery](deployment/README.md#disaster-recovery) - Recovery procedures {todo}

## Support

### Getting Help
- [Documentation Issues](README.md#support) - Documentation problems {todo}
- [Technical Issues](README.md#troubleshooting) - Technical problems
- [Feature Requests](README.md#contributing) - Feature requests {todo}
- [Bug Reports](README.md#contributing) - Bug reporting {todo}

### Community
- [Contributing](README.md#contributing) - How to contribute
- [Code of Conduct](README.md#code-of-conduct) - Community guidelines {todo}
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
