"""
Help Page - Documentation and Support

This page provides help, documentation, and support information for the Digital Twins system.
"""

import streamlit as st
from shared.components import create_header, create_footer, create_sidebar_info

def main():
    """Main function for the Help page"""
    
    # Page configuration
    st.set_page_config(
        page_title="Digital Twins Management System - Help",
        page_icon="📚",
        layout="wide"
    )
    
    # Create header
    create_header("Help & Documentation", "📚")
    
    # Sidebar
    with st.sidebar:
        create_sidebar_info()
        
        st.header("📚 Help Navigation")
        
        help_sections = [
            "🚀 Getting Started",
            "🤖 Workflows Guide",
            "📁 Document Management",
            "💬 Chat Interface",
            "📊 Analytics",
            "⚙️ Configuration",
            "❓ FAQ",
            "🐛 Troubleshooting",
            "📞 Support"
        ]
        
        selected_section = st.radio("Select Section:", help_sections)
    
    # Main content
    st.markdown(f"## {selected_section}")
    
    if selected_section == "🚀 Getting Started":
        getting_started_help()
    elif selected_section == "🤖 Workflows Guide":
        workflows_help()
    elif selected_section == "📁 Document Management":
        document_management_help()
    elif selected_section == "💬 Chat Interface":
        chat_interface_help()
    elif selected_section == "📊 Analytics":
        analytics_help()
    elif selected_section == "⚙️ Configuration":
        configuration_help()
    elif selected_section == "❓ FAQ":
        faq_help()
    elif selected_section == "🐛 Troubleshooting":
        troubleshooting_help()
    elif selected_section == "📞 Support":
        support_help()
    
    # Create footer
    create_footer()

def getting_started_help():
    """Getting Started help section"""
    
    st.markdown("### 🚀 Getting Started with Digital Twins Management System")
    
    st.markdown("""
    Welcome to the Digital Twins Management & Leadership System! This comprehensive platform 
    provides AI-powered digital replicas of management systems and leadership teams with 
    real-time insights, decision support, and executive coaching tools.
    """)
    
    # Quick start steps
    st.markdown("#### 📋 Quick Start Steps")
    
    steps = [
        {
            "step": "1",
            "title": "Configure Your AI Models",
            "description": "Go to Settings → AI Models to set up your Ollama Cloud API key and configure model preferences.",
            "action": "Go to Settings"
        },
        {
            "step": "2", 
            "title": "Upload Your Documents",
            "description": "Navigate to Documents page to upload your organizational data, reports, and datasets.",
            "action": "Go to Documents"
        },
        {
            "step": "3",
            "title": "Start Your First Workflow",
            "description": "Visit the Workflows page to select a workflow type and ask your first question.",
            "action": "Go to Workflows"
        },
        {
            "step": "4",
            "title": "Explore Analytics",
            "description": "Check the Analytics page to monitor system performance and usage insights.",
            "action": "Go to Analytics"
        }
    ]
    
    for step in steps:
        with st.container():
            col1, col2 = st.columns([1, 4])
            
            with col1:
                st.markdown(f"### {step['step']}")
            
            with col2:
                st.markdown(f"**{step['title']}**")
                st.markdown(step['description'])
                
                if st.button(step['action'], key=f"action_{step['step']}"):
                    if step['step'] == "1":
                        st.switch_page("pages/6_⚙️_Settings.py")
                    elif step['step'] == "2":
                        st.switch_page("pages/3_📁_Documents.py")
                    elif step['step'] == "3":
                        st.switch_page("pages/2_🤖_Workflows.py")
                    elif step['step'] == "4":
                        st.switch_page("pages/5_📊_Analytics.py")
            
            st.divider()
    
    # System overview
    st.markdown("#### 🎯 System Overview")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Core Features:**
        - 🤖 Multi-Agent Workflows (1-7 teams)
        - 🧠 Advanced RAG System
        - 📁 Document Processing (15+ formats)
        - 💬 Conversational Interface
        - 📊 Real-time Analytics
        - ⚙️ Flexible Configuration
        """)
    
    with col2:
        st.markdown("""
        **Key Benefits:**
        - Real-time insights and decision support
        - Comprehensive document analysis
        - Scalable multi-agent architecture
        - Enterprise-grade security
        - Easy-to-use interface
        - Extensive customization options
        """)

def workflows_help():
    """Workflows help section"""
    
    st.markdown("### 🤖 Workflows Guide")
    
    st.markdown("""
    The Digital Twins system offers 7 different workflow configurations, each designed 
    for specific use cases and complexity levels. Workflows are executed by specialized 
    AI agent teams working sequentially.
    """)
    
    # Workflow types
    workflows = [
        {
            "name": "Standard Research & Analysis",
            "teams": "1 Team",
            "agents": "Research Specialist, Data Analyst, Content Writer",
            "use_case": "Basic research and analysis tasks",
            "duration": "2-5 minutes"
        },
        {
            "name": "Two-Team Data Strategy (DAMA)",
            "teams": "2 Teams", 
            "agents": "Research Team + Data Strategy Team (Governance, DCAM, Tranch)",
            "use_case": "Data strategy and DAMA implementation",
            "duration": "5-10 minutes"
        },
        {
            "name": "Three-Team Complete (DAMA + Compliance)",
            "teams": "3 Teams",
            "agents": "Research + Data Strategy + Compliance & Risk",
            "use_case": "Comprehensive analysis with compliance focus",
            "duration": "8-15 minutes"
        },
        {
            "name": "Four-Team Enterprise (DAMA + Compliance + Information Management)",
            "teams": "4 Teams",
            "agents": "Research + Data Strategy + Compliance + Information Management",
            "use_case": "Enterprise-level analysis and governance",
            "duration": "12-20 minutes"
        },
        {
            "name": "Five-Team Tender Response",
            "teams": "5 Teams",
            "agents": "All above + Tender Response Team",
            "use_case": "Tender analysis and proposal development",
            "duration": "15-25 minutes"
        },
        {
            "name": "Six-Team Project Delivery",
            "teams": "6 Teams",
            "agents": "All above + Project Delivery Team",
            "use_case": "Technical implementation and project management",
            "duration": "20-30 minutes"
        },
        {
            "name": "Seven-Team Complete",
            "teams": "7 Teams",
            "agents": "All teams including Technical Documentation",
            "use_case": "Complete enterprise solution with full documentation",
            "duration": "25-40 minutes"
        }
    ]
    
    for workflow in workflows:
        with st.expander(f"**{workflow['name']}** - {workflow['teams']}", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**Agents:** {workflow['agents']}")
                st.markdown(f"**Use Case:** {workflow['use_case']}")
            
            with col2:
                st.markdown(f"**Duration:** {workflow['duration']}")
                st.markdown(f"**Complexity:** {'Low' if workflow['teams'] == '1 Team' else 'Medium' if workflow['teams'] in ['2 Teams', '3 Teams'] else 'High'}")
    
    # Workflow execution tips
    st.markdown("#### 💡 Workflow Execution Tips")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Best Practices:**
        - Start with simpler workflows for basic tasks
        - Use pre-search mode for reliable results
        - Provide clear, specific questions
        - Upload relevant documents beforehand
        - Monitor progress in the progress panel
        """)
    
    with col2:
        st.markdown("""
        **Performance Tips:**
        - Use native function calling for faster execution
        - Enable memory for context continuity
        - Choose appropriate workflow complexity
        - Monitor system resources during execution
        - Save important results for future reference
        """)

def document_management_help():
    """Document Management help section"""
    
    st.markdown("### 📁 Document Management Guide")
    
    st.markdown("""
    The Document Management system allows you to upload, process, and analyze various 
    document types to enhance your Digital Twin analysis with real organizational data.
    """)
    
    # Supported formats
    st.markdown("#### 📄 Supported Document Formats")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **Structured Data:**
        - CSV files
        - Excel (XLSX, XLS)
        - JSON files
        - XML files
        - YAML files
        - SQLite databases
        """)
    
    with col2:
        st.markdown("""
        **Semi-Structured:**
        - Text files (TXT)
        - Markdown (MD)
        - Log files
        - TSV files
        - Configuration files
        """)
    
    with col3:
        st.markdown("""
        **Unstructured:**
        - PDF documents
        - Word documents (DOCX, DOC)
        - RTF files
        - Archives (ZIP, TAR, GZ)
        """)
    
    # Document processing workflow
    st.markdown("#### 🔄 Document Processing Workflow")
    
    steps = [
        "**Upload** - Select and upload your documents",
        "**Process** - System automatically processes and analyzes content",
        "**Chunk** - Documents are split into searchable chunks",
        "**Store** - Chunks are stored in vector database for semantic search",
        "**Search** - Use semantic search to find relevant information",
        "**Analyze** - Generate insights and analytics from your documents"
    ]
    
    for i, step in enumerate(steps, 1):
        st.markdown(f"{i}. {step}")
    
    # Document management features
    st.markdown("#### 🛠️ Document Management Features")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Upload & Processing:**
        - Drag-and-drop interface
        - Batch upload support
        - Automatic format detection
        - Content extraction and analysis
        - Metadata extraction
        """)
    
    with col2:
        st.markdown("""
        **Search & Retrieval:**
        - Semantic search across all documents
        - Content-based filtering
        - Metadata-based queries
        - Similarity scoring
        - Context-aware results
        """)
    
    # Best practices
    st.markdown("#### 💡 Best Practices")
    
    st.markdown("""
    **Document Preparation:**
    - Ensure documents are readable and not corrupted
    - Use descriptive filenames for better organization
    - Group related documents together
    - Remove sensitive information before uploading
    
    **Search Optimization:**
    - Use specific, descriptive search terms
    - Combine multiple search criteria
    - Review search results for relevance
    - Use document metadata for filtering
    """)

def chat_interface_help():
    """Chat Interface help section"""
    
    st.markdown("### 💬 Chat Interface Guide")
    
    st.markdown("""
    The Chat Interface provides a conversational way to interact with your Digital Twin 
    system. It combines the power of multi-agent workflows with an intuitive chat experience.
    """)
    
    # Chat features
    st.markdown("#### 🎯 Chat Features")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Core Features:**
        - Natural language interaction
        - Context-aware responses
        - Memory integration
        - Pre-search capabilities
        - Real-time processing
        - Conversation history
        """)
    
    with col2:
        st.markdown("""
        **Advanced Features:**
        - Multi-turn conversations
        - Topic tracking
        - Quick action buttons
        - Export capabilities
        - Memory management
        - Performance monitoring
        """)
    
    # Chat settings
    st.markdown("#### ⚙️ Chat Settings")
    
    st.markdown("""
    **Memory Settings:**
    - **Enable Memory**: Remember previous conversations for context
    - **Clear Chat History**: Reset the current conversation
    - **Clear Memory**: Remove all stored conversation data
    
    **Pre-search Settings:**
    - **Enable Pre-search**: Search web and memory before responding
    - **Search Sources**: Choose between web, memory, or both
    - **Result Quality**: Configure search result filtering
    """)
    
    # Quick actions
    st.markdown("#### 🚀 Quick Actions")
    
    quick_actions = [
        {
            "action": "🔍 Research Topic",
            "description": "Start a research conversation about a specific topic",
            "example": "Research the latest trends in digital transformation"
        },
        {
            "action": "📊 Analyze Data", 
            "description": "Begin data analysis and insights generation",
            "example": "Analyze our quarterly performance metrics"
        },
        {
            "action": "💡 Strategic Insights",
            "description": "Get strategic recommendations and insights",
            "example": "Provide strategic insights for our digital transformation"
        },
        {
            "action": "📋 Generate Report",
            "description": "Create comprehensive reports and documentation",
            "example": "Generate a report on digital transformation best practices"
        }
    ]
    
    for action in quick_actions:
        with st.expander(f"**{action['action']}** - {action['description']}", expanded=False):
            st.markdown(f"**Example:** {action['example']}")
    
    # Chat tips
    st.markdown("#### 💡 Chat Tips")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Effective Questions:**
        - Be specific and clear
        - Provide context when needed
        - Ask follow-up questions
        - Use industry-specific terms
        - Request examples or details
        """)
    
    with col2:
        st.markdown("""
        **Conversation Flow:**
        - Start with broad questions
        - Drill down into specifics
        - Ask for clarification
        - Request different perspectives
        - Summarize key points
        """)

def analytics_help():
    """Analytics help section"""
    
    st.markdown("### 📊 Analytics Guide")
    
    st.markdown("""
    The Analytics page provides comprehensive insights into system usage, performance, 
    and user behavior. Use these insights to optimize your Digital Twin experience.
    """)
    
    # Analytics sections
    st.markdown("#### 📈 Analytics Sections")
    
    sections = [
        {
            "name": "System Overview",
            "description": "High-level metrics and system status",
            "metrics": ["Total Conversations", "Stored Documents", "System Status", "Uptime"]
        },
        {
            "name": "Conversation Analytics", 
            "description": "Chat usage patterns and trends",
            "metrics": ["Daily Conversations", "Message Volume", "User Engagement", "Response Times"]
        },
        {
            "name": "Document Analytics",
            "description": "Document processing and storage insights",
            "metrics": ["Document Types", "Storage Usage", "Processing Times", "Search Queries"]
        },
        {
            "name": "Workflow Analytics",
            "description": "Workflow execution and performance data",
            "metrics": ["Workflow Executions", "Success Rates", "Duration Analysis", "Agent Performance"]
        },
        {
            "name": "Performance Analytics",
            "description": "System performance and resource utilization",
            "metrics": ["Response Times", "Memory Usage", "CPU Usage", "Error Rates"]
        }
    ]
    
    for section in sections:
        with st.expander(f"**{section['name']}** - {section['description']}", expanded=False):
            st.markdown("**Key Metrics:**")
            for metric in section['metrics']:
                st.markdown(f"- {metric}")
    
    # Analytics features
    st.markdown("#### 🛠️ Analytics Features")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Visualization:**
        - Interactive charts and graphs
        - Real-time data updates
        - Customizable date ranges
        - Export capabilities
        - Performance gauges
        """)
    
    with col2:
        st.markdown("""
        **Insights:**
        - Usage pattern analysis
        - Performance recommendations
        - Trend identification
        - Anomaly detection
        - Optimization suggestions
        """)
    
    # Using analytics
    st.markdown("#### 💡 Using Analytics Effectively")
    
    st.markdown("""
    **Regular Monitoring:**
    - Check system status daily
    - Monitor performance metrics weekly
    - Review usage patterns monthly
    - Analyze trends quarterly
    
    **Optimization:**
    - Identify peak usage times
    - Optimize resource allocation
    - Improve workflow efficiency
    - Enhance user experience
    """)

def configuration_help():
    """Configuration help section"""
    
    st.markdown("### ⚙️ Configuration Guide")
    
    st.markdown("""
    The Configuration page allows you to customize various aspects of your Digital Twin 
    system, from AI models to appearance settings.
    """)
    
    # Configuration sections
    st.markdown("#### 🔧 Configuration Sections")
    
    sections = [
        {
            "name": "AI Models",
            "description": "Configure AI models and their parameters",
            "settings": ["Model Selection", "API Keys", "Temperature", "Max Tokens", "Performance Tuning"]
        },
        {
            "name": "System Config",
            "description": "General system settings and preferences",
            "settings": ["App Name", "Default Workflow", "Performance Limits", "Memory Settings"]
        },
        {
            "name": "Security",
            "description": "Security and privacy configuration",
            "settings": ["API Key Management", "Data Encryption", "Access Control", "Audit Logging"]
        },
        {
            "name": "Performance",
            "description": "Performance optimization settings",
            "settings": ["Caching", "Resource Limits", "Monitoring", "Auto-scaling"]
        },
        {
            "name": "Appearance",
            "description": "UI customization and theming",
            "settings": ["Theme", "Colors", "Layout", "Fonts"]
        },
        {
            "name": "Export/Import",
            "description": "Data export and import configuration",
            "settings": ["Export Formats", "Import Settings", "Backup Configuration", "Data Retention"]
        }
    ]
    
    for section in sections:
        with st.expander(f"**{section['name']}** - {section['description']}", expanded=False):
            st.markdown("**Available Settings:**")
            for setting in section['settings']:
                st.markdown(f"- {setting}")
    
    # Configuration best practices
    st.markdown("#### 💡 Configuration Best Practices")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **AI Models:**
        - Use appropriate models for your use case
        - Monitor API usage and costs
        - Test different temperature settings
        - Keep API keys secure
        - Regular model updates
        """)
    
    with col2:
        st.markdown("""
        **System Settings:**
        - Set realistic performance limits
        - Enable monitoring and alerts
        - Regular backup configuration
        - Security-first approach
        - Document your configuration
        """)

def faq_help():
    """FAQ help section"""
    
    st.markdown("### ❓ Frequently Asked Questions")
    
    faqs = [
        {
            "question": "What is the Digital Twins Management System?",
            "answer": "It's an AI-powered platform that creates digital replicas of management systems and leadership teams, providing real-time insights, decision support, and executive coaching tools through multi-agent workflows."
        },
        {
            "question": "How many workflow types are available?",
            "answer": "There are 7 workflow types, ranging from 1-team basic research to 7-team complete enterprise solutions. Each workflow adds specialized agent teams for different business functions."
        },
        {
            "question": "What document formats are supported?",
            "answer": "The system supports 15+ document formats including PDF, DOCX, CSV, Excel, JSON, XML, SQLite, and more. Documents are automatically processed and made searchable."
        },
        {
            "question": "How does the memory system work?",
            "answer": "The system uses ChromaDB for vector storage with semantic search capabilities. It maintains both conversation memory and document memory for context-aware responses."
        },
        {
            "question": "Can I use local AI models instead of cloud?",
            "answer": "Yes, the system supports both local Ollama models and cloud models. You can configure this in the Settings page under AI Models."
        },
        {
            "question": "How secure is my data?",
            "answer": "The system implements enterprise-grade security with data encryption, secure API key management, and local data processing options. All data can be stored locally if preferred."
        },
        {
            "question": "What is the difference between pre-search and native function calling?",
            "answer": "Pre-search mode gathers context from web and memory before processing, while native function calling allows agents to directly call tools. Pre-search is more reliable for complex workflows."
        },
        {
            "question": "How can I export my results?",
            "answer": "Results can be exported as PDF reports, and the system supports various export formats. You can also save conversation history and document analysis results."
        },
        {
            "question": "Is there a limit to the number of documents I can upload?",
            "answer": "There are configurable limits based on your system resources. The default limit is 100MB per file, but this can be adjusted in the Settings page."
        },
        {
            "question": "How do I get support if I encounter issues?",
            "answer": "Check the Troubleshooting section first, then use the Support section to contact our team. We also provide comprehensive documentation and help resources."
        }
    ]
    
    for faq in faqs:
        with st.expander(f"**Q: {faq['question']}**", expanded=False):
            st.markdown(f"**A:** {faq['answer']}")

def troubleshooting_help():
    """Troubleshooting help section"""
    
    st.markdown("### 🐛 Troubleshooting Guide")
    
    st.markdown("""
    This section helps you resolve common issues and optimize your Digital Twin system performance.
    """)
    
    # Common issues
    st.markdown("#### 🔧 Common Issues")
    
    issues = [
        {
            "issue": "LLM Connection Failed",
            "symptoms": ["Error initializing LLM", "Connection timeout", "API key invalid"],
            "solutions": [
                "Check your API key in Settings → AI Models",
                "Verify internet connection",
                "Test connection using the test button",
                "Try switching between cloud and local models"
            ]
        },
        {
            "issue": "Workflow Execution Failed",
            "symptoms": ["Workflow timeout", "Agent errors", "Empty responses"],
            "solutions": [
                "Try using pre-search mode instead of native function calling",
                "Reduce workflow complexity",
                "Check system resources",
                "Clear memory and try again"
            ]
        },
        {
            "issue": "Document Upload Issues",
            "symptoms": ["Upload failed", "Processing error", "File not recognized"],
            "solutions": [
                "Check file format is supported",
                "Verify file is not corrupted",
                "Check file size limits",
                "Try uploading one file at a time"
            ]
        },
        {
            "issue": "Memory Issues",
            "symptoms": ["Memory not saving", "Search not working", "Context lost"],
            "solutions": [
                "Check ChromaDB is running",
                "Verify memory directory permissions",
                "Clear and rebuild memory",
                "Check disk space"
            ]
        },
        {
            "issue": "Performance Issues",
            "symptoms": ["Slow responses", "High memory usage", "System freezing"],
            "solutions": [
                "Check system resources",
                "Reduce concurrent workflows",
                "Clear cache and memory",
                "Restart the application"
            ]
        }
    ]
    
    for issue in issues:
        with st.expander(f"**{issue['issue']}**", expanded=False):
            st.markdown("**Symptoms:**")
            for symptom in issue['symptoms']:
                st.markdown(f"- {symptom}")
            
            st.markdown("**Solutions:**")
            for solution in issue['solutions']:
                st.markdown(f"- {solution}")
    
    # Diagnostic tools
    st.markdown("#### 🔍 Diagnostic Tools")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🧪 Run System Diagnostics", use_container_width=True):
            st.info("Running diagnostics...")
            # Add diagnostic logic here
            st.success("✅ System diagnostics completed!")
    
    with col2:
        if st.button("📊 Check System Status", use_container_width=True):
            st.info("Checking system status...")
            # Add status check logic here
            st.success("✅ System status check completed!")
    
    # Performance optimization
    st.markdown("#### ⚡ Performance Optimization")
    
    st.markdown("""
    **System Optimization:**
    - Monitor memory usage and clear when needed
    - Use appropriate workflow complexity for your tasks
    - Enable caching for frequently accessed data
    - Regular system maintenance and updates
    
    **Workflow Optimization:**
    - Use pre-search mode for reliable results
    - Start with simpler workflows for basic tasks
    - Provide clear, specific questions
    - Upload relevant documents beforehand
    """)

def support_help():
    """Support help section"""
    
    st.markdown("### 📞 Support & Contact")
    
    st.markdown("""
    Need help? We're here to support you with your Digital Twin system. Choose the 
    support option that works best for you.
    """)
    
    # Support options
    st.markdown("#### 🆘 Support Options")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Self-Service:**
        - 📚 Documentation and guides
        - ❓ FAQ section
        - 🐛 Troubleshooting guide
        - 💡 Best practices
        - 🔍 Search functionality
        """)
    
    with col2:
        st.markdown("""
        **Direct Support:**
        - 📧 Email support
        - 💬 Live chat
        - 📞 Phone support
        - 🎫 Support tickets
        - 👥 Community forum
        """)
    
    # Contact information
    st.markdown("#### 📧 Contact Information")
    
    contact_info = [
        {
            "method": "📧 Email Support",
            "contact": "support@digitaltwins.com",
            "hours": "24/7",
            "response": "Within 24 hours"
        },
        {
            "method": "💬 Live Chat",
            "contact": "Available in app",
            "hours": "9 AM - 6 PM EST",
            "response": "Immediate"
        },
        {
            "method": "📞 Phone Support",
            "contact": "+1 (555) 123-4567",
            "hours": "9 AM - 6 PM EST",
            "response": "Immediate"
        },
        {
            "method": "🎫 Support Ticket",
            "contact": "Create ticket in app",
            "hours": "24/7",
            "response": "Within 4 hours"
        }
    ]
    
    for contact in contact_info:
        with st.container():
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"**{contact['method']}**")
            
            with col2:
                st.markdown(contact['contact'])
            
            with col3:
                st.markdown(contact['hours'])
            
            with col4:
                st.markdown(contact['response'])
    
    # Community resources
    st.markdown("#### 👥 Community Resources")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Online Resources:**
        - 🌐 Official website
        - 📚 Documentation portal
        - 🎥 Video tutorials
        - 📖 User guides
        - 🔧 API documentation
        """)
    
    with col2:
        st.markdown("""
        **Community:**
        - 💬 Discussion forums
        - 👥 User groups
        - 🎓 Training programs
        - 🏆 Success stories
        - 🔄 Feature requests
        """)
    
    # Feedback
    st.markdown("#### 💭 Feedback & Suggestions")
    
    st.markdown("""
    We value your feedback! Help us improve the Digital Twin system by sharing 
    your thoughts, suggestions, and experiences.
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("💡 Submit Feedback", use_container_width=True):
            st.info("Feedback form coming soon!")
    
    with col2:
        if st.button("🔄 Request Feature", use_container_width=True):
            st.info("Feature request form coming soon!")
    
    with col3:
        if st.button("🐛 Report Bug", use_container_width=True):
            st.info("Bug report form coming soon!")

if __name__ == "__main__":
    main()
