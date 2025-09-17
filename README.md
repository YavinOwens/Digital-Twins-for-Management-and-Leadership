# Digital Twins for Management and Leadership - CrewAI Multi-Agent Workflow System

A comprehensive Streamlit application that orchestrates multiple AI agent teams using CrewAI with Ollama (local and cloud) for enterprise-level research, analysis, and document generation. This system implements the Digital Twin concept for management and leadership teams, providing AI-powered digital replicas of management systems and leadership teams with real-time insights, decision support, simulations, and executive coaching tools.

## 🚀 Features

### **Multi-Team Workflows (1-7 Teams)**
- **Single Team**: Research → Analysis → Writing
- **Two Teams**: Research → Data Strategy (DAMA)
- **Three Teams**: Research → Data Strategy → Compliance & Risk
- **Four Teams**: Research → Data Strategy → Compliance & Risk → Information Management
- **Five Teams**: + Tender Response
- **Six Teams**: + Project Delivery
- **Seven Teams**: + Technical Documentation

### **Advanced Capabilities**
- **Hybrid Model Support**: Local Ollama (llama3.1) and Ollama Cloud (Turbo)
- **Real-time Web Search**: DuckDuckGo integration with enhanced visualization
- **Conversation Memory**: ChromaDB with local embeddings (no external API keys)
- **PDF Report Generation**: Professional templated reports with multiple layouts
- **Team Output Management**: Structured saving of all team outputs
- **Pre-search Functionality**: Web + memory search for comprehensive context
- **Modular Architecture**: Organized agent teams, workflows, and UI components
- **Function Calling Testing**: Test model capabilities before use
- **Environment Configuration**: Secure API key management

## Setup

### 1. Install Dependencies

```bash
pip install -r local_requirements.txt
```

### 2. Environment Configuration

Copy the example environment file and configure your settings:

```bash
cp .env.example .env
```

Edit `.env` with your configuration:

```env
# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_LOCAL_MODEL=llama3.1

# Ollama Cloud (Turbo) settings
OLLAMA_CLOUD_BASE_URL=https://api.ollama.ai
OLLAMA_CLOUD_MODEL=gpt-oss:20b
OLLAMA_API_KEY=your_api_key_here

# Application settings
STREAMLIT_PORT=8501
STREAMLIT_ADDRESS=localhost

# Search settings
DUCKDUCKGO_MAX_RESULTS=5
SEARCH_RETRY_ATTEMPTS=3
SEARCH_DELAY_SECONDS=1

# Model settings
DEFAULT_TEMPERATURE=0.7
DEFAULT_MAX_TOKENS=20000
DEFAULT_TOP_P=0.9
```

### 3. Start Ollama (Local)

```bash
ollama serve
```

### 4. Pull Required Models

```bash
ollama pull llama3.1
```

### 5. Run the Application

```bash
streamlit run streamlit_app.py
```

## Usage

### **Basic Workflow**
1. **Choose Model**: Select between Local Ollama (llama3.1) or Ollama Cloud (Turbo)
2. **Enter API Key**: If using cloud, enter your Ollama API key
3. **Select Workflow**: Choose from 1-7 team workflows
4. **Test Function Calling**: Click the test button to verify capabilities
5. **Ask Questions**: The app will orchestrate multiple agent teams

### **Advanced Features**
- **Memory Search**: Past conversations are automatically searched for context
- **PDF Generation**: Download professional reports in multiple formats
- **Team Outputs**: All team outputs are saved to structured folders
- **Pre-search**: Web and memory search provides comprehensive context
- **Modular Teams**: Each team specializes in different aspects (research, data strategy, compliance, etc.)

### **Workflow Selection Guide**
- **1 Team**: Basic research and analysis
- **2 Teams**: Add data strategy and DAMA implementation
- **3 Teams**: Add compliance and risk management
- **4 Teams**: Add information management
- **5 Teams**: Add tender response capabilities
- **6 Teams**: Add project delivery teams
- **7 Teams**: Add technical documentation (complete solution)

## Models

### Local Models
- **llama3.1**: 8B parameters, ~8GB RAM required
- **phi3**: 3.8B parameters, ~4GB RAM required (legacy)

### Cloud Models (Ollama Turbo)
- **gpt-oss:20b**: 20B parameters, $20/month
- **gpt-oss:120b**: 120B parameters, $20/month
- **deepseek-v3.1:671b**: 671B parameters, $20/month

## Architecture

### **Modular Structure**
```
web_knowledge/
├── agent_teams/           # Specialized agent teams
│   ├── research_analysis/
│   ├── data_strategy/
│   ├── compliance_risk/
│   ├── information_management/
│   ├── tender_response/
│   ├── project_delivery/
│   └── technical_documentation/
├── workflows/             # Workflow execution functions
├── agent_tools/           # Tools and utilities
├── ui_components/         # Streamlit UI components
├── team_outputs/          # Generated outputs
├── memory_db/             # ChromaDB conversation memory
└── presearch/             # Search and context management
```

### **Agent Teams**
- **Research & Analysis**: Web search, data gathering, analysis
- **Data Strategy**: DAMA implementation, data governance
- **Compliance & Risk**: Regulatory compliance, risk management
- **Information Management**: Data lifecycle, metadata management
- **Tender Response**: Proposal writing, compliance checking
- **Project Delivery**: Technical implementation, project management
- **Technical Documentation**: Code generation, documentation

## Configuration

All settings can be configured via environment variables in the `.env` file:

- `OLLAMA_BASE_URL`: Local Ollama server URL
- `OLLAMA_LOCAL_MODEL`: Local model to use
- `OLLAMA_CLOUD_BASE_URL`: Ollama Cloud API URL
- `OLLAMA_CLOUD_MODEL`: Cloud model to use
- `OLLAMA_API_KEY`: Your Ollama Cloud API key
- `DEFAULT_TEMPERATURE`: Model temperature (0.0-1.0)
- `DEFAULT_MAX_TOKENS`: Maximum tokens per response
- `DUCKDUCKGO_MAX_RESULTS`: Number of search results to fetch
- `MAX_MEMORY_RESULTS`: Number of memory search results

## Memory & Storage

### **Conversation Memory**
- **ChromaDB**: Local vector database with 384-dimensional embeddings
- **Model**: ONNXMiniLM_L6_V2 (all-MiniLM-L6-v2) - no external API keys needed
- **Storage**: `./memory_db/` directory with SQLite backend
- **Search**: Semantic similarity search across past conversations
- **Privacy**: All data stored locally, no external API calls

### **Team Outputs**
- **Location**: `./team_outputs/` directory
- **Format**: Markdown files with metadata
- **Structure**: Organized by workflow type and timestamp
- **Content**: Individual team outputs and combined results

### **PDF Generation**
- **Templates**: Professional report layouts
- **Formats**: Multiple template options available
- **Content**: Structured reports with tables, charts, and formatting
- **Download**: Direct download links in Streamlit interface

## Security

- The `.env` file is gitignored to protect your API keys
- Never commit API keys to version control
- Use `.env.example` as a template for configuration
- **Local Memory**: No external API calls for embeddings
- **Data Privacy**: All conversations stored locally

## Troubleshooting

1. **Local Ollama not working**: Ensure Ollama is running (`ollama serve`)
2. **Model not found**: Pull the required model (`ollama pull llama3.1`)
3. **API key issues**: Check your Ollama Cloud subscription and API key
4. **Function calling fails**: Use pre-search mode as fallback
5. **Memory issues**: Check `./memory_db/` directory permissions
6. **PDF generation fails**: Ensure all dependencies are installed
7. **Team outputs not saving**: Check `./team_outputs/` directory permissions


## 📚 Documentation

### **Comprehensive Technical Documentation**
- **[Technical Documentation Index](docs/INDEX.md)** - Complete documentation navigation
- **[System Architecture](ARCHITECTURE.md)** - Interactive architecture diagram and design
- **[Agent Teams](docs/agent_teams/README.md)** - Detailed agent team documentation
- **[Workflows](docs/workflows/README.md)** - Workflow execution documentation
- **[Agent Tools](docs/agent_tools/README.md)** - Tools and utilities documentation
- **[UI Components](docs/ui_components/README.md)** - Streamlit UI components
- **[Memory System](docs/memory_system/README.md)** - ChromaDB and embedding system
- **[Configuration](docs/configuration/README.md)** - Environment and security configuration
- **[Deployment](docs/deployment/README.md)** - Local and cloud deployment guides

### **Quick Reference**
- **[API Reference](docs/INDEX.md#api-reference)** - Complete API documentation
- **[Troubleshooting Guide](docs/INDEX.md#troubleshooting)** - Common issues and solutions
- **[Development Guide](docs/INDEX.md#development)** - Development and contribution guidelines

## Development

### **Adding New Agent Teams**
1. Create new directory in `agent_teams/`
2. Add `agents.py` and `tasks.py` files
3. Follow existing patterns for agent and task creation
4. Import in main application
5. See [Agent Teams Documentation](docs/agent_teams/README.md#extending-teams) for detailed guide

### **Adding New Workflows**
1. Create new file in `workflows/` directory
2. Follow existing function signature pattern
3. Import required agent and task creation functions
4. Add to `__init__.py` exports
5. See [Workflows Documentation](docs/workflows/README.md#extending-workflows) for detailed guide

### **Testing**
- Use `agent_test_functions/` for testing individual components
- Test workflows with different queries
- Verify memory and output functionality
- See [Testing Guide](docs/INDEX.md#testing) for comprehensive testing strategies

## License

This project is open source and available under the MIT License.
=======
# Digital-Twins-for-Management-and-Leadership

<b> The hypothetical ask </b> ; "Digital Twin for Management and Leadership Teams: Create AI-powered digital replicas of management systems and leadership teams. Provides real-time insights, decision support, simulations, and executive coaching tools integrating live data, team dynamics, and personalised assistant features for leaders. "

This repository hosts an IMO digital twin platform designed to model, simulate, and analyse management processes in real time. The system creates a virtual representation of organisational, operational, and project management frameworks—mirroring real-world managerial entities, workflows, resources, and data. Its features enable advanced monitoring, decision support, and performance optimisation through dynamic feedback and analytics. Details of key features can be found in the Key Features markdown document [todo]

<b> Key Features </b>

- Virtual models for both entire management systems and specific leadership teams, reflecting roles, communication patterns, decision flows, and behavioral traits.
- Voice Recognition and NLP : proprietary 
- Machine Learning Integration : proprietary 
- Multi-Platform Integration:  Integration with organisational data, business intelligence, HR tools, and comms platforms to keep the digital twins up-to-date and contextually relevant.
- Organic Platform Integration: Integration of leadership attributes, individual leader profiles, and team dynamics for scenario simulation (e.g., restructuring, crisis response, succession planning).
- Assistant functionality for executives: personalized recommendations, strategic planning support, and continuous learning or coaching via AI-driven feedback loops.
Contextual “what-if” analysis for leadership scenarios—enabling evidence-based decisions and future-proofing strategies.

<b> Feature Considerations partially considered in this example  </b> ; 
Privacy, security, and ethical controls for handling leadership data.

<b> Abstract </b>
<i> Journal of Industrial Information Integration </i>

Recent events worldwide of climate and geological origins highlight the vulnerability of our infrastructures and stress the often dramatic consequences on our environment. Accurate digital models are needed to understand how climate change and associated risks affect buildings, while informing on ways of enhancing their adaptability and resilience. This requires a paradigm shift in design and engineering interventions as the potential for adaptation and resilience should be embedded into initial brief formulation, design, engineering, construction and facility maintenance methods. This paper argues the need for smarter and digital interventions for buildings and infrastructures and their underpinning data systems that factor in topology (including geometry), mereology, and behavioural (dynamic) considerations. Digital models can be used as a basis to understand the complex interplay between environmental variables and performance, and explore real-time response strategies (including control and actuation) to known and uncertain solicitations enabled by a new generation of technologies.

The paper proposes a digital twin model for the construction and industrial assets that paves the way to
a new generation of buildings and infrastructures that;

1. Address lifetime requirements.
2. Capable of performing optimally within the constraints of unknown future scenarios. 
3. Achieve acceptable levels of adaptability, efficiency and resilience.

<b> What Is a Digital Twin in Management? </b>

A digital twin is a virtual replica of a physical system, process, or organization, designed to simulate, monitor, and control real-world entities in real time. In management, this translates to mirroring business processes, leadership actions, and organizational resources in a dynamic, data-driven model. These twins use layers of technology—from data ingestion through analytics to visual interaction—enabling predictive modeling, scenario planning, and optimized decision-making.

<b> How Digital Twins Support Leadership </b>

Digital twins allow leaders and managers to:

Run 'what-if' scenario analyses, testing strategies before real-world execution.
Gain 360-degree, real-time visibility into operations and human resources.
Embed AI, optimization algorithms, and advanced analytics to simulate and automate leadership decision points (e.g., resource allocation, risk mitigation).
Foster organizational agility and resilience through continuous monitoring, feedback loops, and rapid adjustment.
Enhance communication and coordination across virtual teams and remote workforces, improving the organizational leadership model.

<b> Key Layers in Management Digital Twin Architectures </b>
Digital twins for management and leadership typically leverage a five-layered technology stack:

- Physical layer: Sensors and real-world data sources
- Data processing layer: Aggregation and transformation
- Data storage layer: Centralized or distributed data warehouses/lakes
- Analytics and computation layer: Predictive, prescriptive, and descriptive analytics
- Visualization and interaction layer: Dashboards, real-time feedback, and simulation environments.

<b> Strategic Management and Leadership Implications </b>

Digital twins can be used to model leadership teams, management structures, and corporate behaviors, automating tasks and interactions in virtual environments.

They support continuous organisational improvement, helping executives iterate strategies, monitor KPIs, and proactively adapt to changes.

Digital twins act as a “managerial revolution,” serving as real-time advisors, simulating potential team dynamics or market responses, and supporting culture and change management initiatives,

In complex or crisis situations, digital twins can provide leaders with faster, data-driven decision tools, enabling superior resource optimization and scenario planning compared to traditional approaches.

<b> Practical Examples </b>

- Modeling and optimizing entire business units, from supply chains to human resource allocations.
- Simulating leadership responses to hypothetical disruptions or organizational transformations.
- Enabling autonomous management agents or ‘leader avatars’ that take routine decisions or coordinate digital assets based on real-time data.

<b> Critical Success Factors </b>

Successful implementation requires robust big data infrastructure, clear organizational architecture, and investments in IoT, AI, and analytics platforms.

Leadership buy-in is essential, as is ongoing data governance and ethical oversight to avoid “algorithmic blindness” or bias in decisions.

[todo]

Timeline [Todo]

Digital Assitance vs Digital Twins 
[Insert slide deck slide(n2)] 

5 n Beyond (Incubator Challenge) 
[Insert slide deck slide(n1)] 

provide a product for the following 
Must Have
- Integration of leadership attributes 
- individual leader profiles
- team dynamics for scenario simulation
  - crisis response
  - succession planning
  - restructuring (Business Resllience best case, worst case) 

Assistant functionality for organisationl layers: 

## 🏢 Digital Twins for Management and Leadership

This system implements the Digital Twin concept for management and leadership teams, providing AI-powered digital replicas of management systems and leadership teams with real-time insights, decision support, simulations, and executive coaching tools.

### **Digital Twin Capabilities**

The system provides assistant functionality for all organizational layers:

**Layer 1: Governance**
- Strategic planning support
- Personalized recommendations
- Learning or coaching via AI-driven feedback loops

**Layer 2: Executive**
- Strategic planning support
- Personalized recommendations
- Learning or coaching via AI-driven feedback loops

**Layer 3: Senior Management**
- Strategic planning support
- Personalized recommendations
- Learning or coaching via AI-driven feedback loops

**Layer 4: Middle Management**
- Strategic planning support
- Personalized recommendations
- Learning or coaching via AI-driven feedback loops

**Layer 5: Supervisory**
- Strategic planning support
- Personalized recommendations
- Learning or coaching via AI-driven feedback loops

**Layer 6: Contributor**
- Strategic planning support
- Personalized recommendations
- Learning or coaching via AI-driven feedback loops

### **What-If Simulation**
Contextual analysis for leadership scenarios—enabling evidence-based decisions and future-proofing strategies.

### **Research Foundation**

This implementation is based on extensive research in Digital Twins for management and leadership:

1. **Petri, I., Rezgui, Y., Ghoroghi, A. & Alzahrani, A., 2023.** Digital twins for performance management in the built environment. Journal of Industrial Information Integration, 33, 100445.

2. **Sharma, A., Kosasih, E., Zhang, J., Brintrup, A., & Calinescu, A. (2022).** Digital Twins: State of the Art Theory and Practice, Challenges, and Open Research Questions. Journal of Industrial Information Integration, 30, 100383.

3. **Saunila, M., Ukko, J., Rantala, T., & Havukainen, J. (2022).** Characteristics of digital twins and theorizing their impact on organizational control.

4. **Tello, A., & Degeler, V. (2024).** Digital Twins – an enabler for digital transformation. Groningen Digital Business Centre, University of Groningen.

5. **"Digital twins of organization: implications for organization" (2024).** Journal of Organization Design, 13(3).

6. **Semeraro, C., et al. (2021).** Digital twin paradigm: A systematic literature review.

### **Additional Notable Studies**

1. **"Building an organizational digital twin" (2020).** Business Horizons, 63(6), 725–736.
2. **Strozzi, F., et al. (2019).** A state-of-the-art survey of Digital Twin: techniques, engineering product lifecycle management, and business innovation perspectives. Journal of Manufacturing Systems, 2020.

## Declaration of Competing Interest

I declare that I have no known competing financial interests or personal relationships that could have appeared to influence this proof of concept.
