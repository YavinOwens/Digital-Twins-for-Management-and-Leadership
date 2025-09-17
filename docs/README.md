# CrewAI Multi-Agent Workflow System - Technical Documentation

This directory contains comprehensive technical documentation for the CrewAI Multi-Agent Workflow System. Each module has its own detailed documentation covering architecture, usage, and implementation details.

## Documentation Structure

```
docs/
├── README.md                           # This overview
├── agent_teams/                        # Agent team documentation
│   ├── README.md
│   ├── research_analysis.md
│   ├── data_strategy.md
│   ├── compliance_risk.md
│   ├── information_management.md
│   ├── tender_response.md
│   ├── project_delivery.md
│   └── technical_documentation.md
├── workflows/                          # Workflow documentation
│   ├── README.md
│   ├── single_team.md
│   ├── multi_team.md
│   └── execution_patterns.md
├── agent_tools/                        # Tool documentation
│   ├── README.md
│   ├── llm_wrappers.md
│   ├── search_tools.md
│   └── pdf_generation.md
├── ui_components/                      # UI documentation
│   ├── README.md
│   ├── components.md
│   └── styling.md
├── memory_system/                      # Memory documentation
│   ├── README.md
│   ├── chromadb_integration.md
│   └── embedding_models.md
├── configuration/                      # Configuration documentation
│   ├── README.md
│   ├── environment_setup.md
│   └── security.md
└── deployment/                         # Deployment documentation
    ├── README.md
    ├── local_deployment.md
    ├── cloud_deployment.md
    └── monitoring.md
```

## Quick Start

1. **System Overview**: Start with the main [README.md](../README.md) for a high-level understanding
2. **Architecture**: Review the [ARCHITECTURE.md](../ARCHITECTURE.md) for system design
3. **Module Details**: Dive into specific module documentation as needed
4. **Deployment**: Follow deployment guides for your environment

## Key Concepts

### Multi-Agent Workflows
The system supports 1-7 team workflows where each team specializes in specific aspects of business analysis and documentation. Teams work sequentially, passing context and results between them.

### Memory System
Uses ChromaDB with local embeddings (ONNXMiniLM_L6_V2) for persistent conversation memory and context retrieval. No external API keys required for embeddings.

### Modular Architecture
The system is organized into modular components:
- **Agent Teams**: Specialized teams with specific roles
- **Workflows**: Orchestration logic for multi-team execution
- **Tools**: Reusable utilities and integrations
- **UI Components**: Streamlit interface components
- **Memory System**: Persistent storage and retrieval

### LLM Integration
Supports both local Ollama (llama3.1) and Ollama Cloud (Turbo) with robust error handling and retry logic.

## Getting Help

- **Issues**: Check the troubleshooting section in each module's documentation
- **Development**: See the development guides for extending the system
- **Deployment**: Follow the deployment documentation for your environment
- **API Reference**: See individual module documentation for detailed API references

## Contributing

When contributing to the system:
1. Follow the existing modular structure
2. Update relevant documentation
3. Test thoroughly with different workflows
4. Ensure backward compatibility
5. Update this documentation index

## License

This project is open source and available under the MIT License.
