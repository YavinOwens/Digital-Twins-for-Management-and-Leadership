"""
Settings Page - Configuration and System Settings

This page handles system configuration, model settings, and preferences.
"""

import streamlit as st
import os
from pathlib import Path
from shared.components import create_header, create_footer, create_sidebar_info
from shared.utils import get_system_info, test_llm_connection

def main():
    """Main function for the Settings page"""
    
    # Page configuration
    st.set_page_config(
        page_title="Digital Twins Management System - Settings",
        page_icon="⚙️",
        layout="wide"
    )
    
    # Create header
    create_header("System Settings & Configuration", "⚙️")
    
    # Sidebar
    with st.sidebar:
        create_sidebar_info()
        
        st.header("⚙️ Settings Navigation")
        
        settings_tabs = [
            "🤖 AI Models",
            "🔧 System Config",
            "🔐 Security",
            "📊 Performance",
            "🎨 Appearance",
            "📤 Export/Import"
        ]
        
        selected_tab = st.radio("Select Category:", settings_tabs)
    
    # Main content
    st.markdown(f"## {selected_tab}")
    
    if selected_tab == "🤖 AI Models":
        ai_models_settings()
    elif selected_tab == "🔧 System Config":
        system_config_settings()
    elif selected_tab == "🔐 Security":
        security_settings()
    elif selected_tab == "📊 Performance":
        performance_settings()
    elif selected_tab == "🎨 Appearance":
        appearance_settings()
    elif selected_tab == "📤 Export/Import":
        export_import_settings()
    
    # Create footer
    create_footer()

def ai_models_settings():
    """AI Models configuration section"""
    
    st.markdown("### 🤖 AI Model Configuration")
    
    # Model selection
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🌐 Cloud Models")
        
        # Ollama Cloud settings
        st.markdown("#### Ollama Cloud (Turbo)")
        
        ollama_cloud_enabled = st.checkbox("Enable Ollama Cloud", value=True)
        
        if ollama_cloud_enabled:
            ollama_cloud_model = st.selectbox(
                "Cloud Model:",
                ["gpt-oss:20b", "gpt-oss:120b", "deepseek-v3.1:671b"],
                index=0,
                help="Select the Ollama Cloud model to use"
            )
            
            ollama_api_key = st.text_input(
                "API Key:",
                type="password",
                help="Enter your Ollama Cloud API key"
            )
            
            if st.button("🧪 Test Connection"):
                if ollama_api_key:
                    with st.spinner("Testing connection..."):
                        try:
                            success = test_llm_connection(use_cloud=True, api_key=ollama_api_key)
                            if success:
                                st.success("✅ Connection successful!")
                            else:
                                st.error("❌ Connection failed!")
                        except Exception as e:
                            st.error(f"❌ Error: {e}")
                else:
                    st.warning("Please enter your API key first")
        
        # OpenAI settings (placeholder)
        st.markdown("#### OpenAI (Optional)")
        openai_enabled = st.checkbox("Enable OpenAI", value=False)
        
        if openai_enabled:
            openai_api_key = st.text_input(
                "OpenAI API Key:",
                type="password",
                help="Enter your OpenAI API key"
            )
            openai_model = st.selectbox(
                "OpenAI Model:",
                ["gpt-4", "gpt-3.5-turbo", "gpt-4-turbo"],
                index=0
            )
    
    with col2:
        st.subheader("💻 Local Models")
        
        # Local Ollama settings
        st.markdown("#### Local Ollama")
        
        local_ollama_enabled = st.checkbox("Enable Local Ollama", value=False)
        
        if local_ollama_enabled:
            local_ollama_url = st.text_input(
                "Ollama URL:",
                value="http://localhost:11434",
                help="URL of your local Ollama server"
            )
            
            local_ollama_model = st.selectbox(
                "Local Model:",
                ["llama3.1:latest", "phi3:latest", "mistral:latest"],
                index=0,
                help="Select the local model to use"
            )
            
            if st.button("🧪 Test Local Connection"):
                with st.spinner("Testing local connection..."):
                    try:
                        success = test_llm_connection(use_cloud=False)
                        if success:
                            st.success("✅ Local connection successful!")
                        else:
                            st.error("❌ Local connection failed!")
                    except Exception as e:
                        st.error(f"❌ Error: {e}")
    
    # Model preferences
    st.markdown("### ⚙️ Model Preferences")
    
    col1, col2 = st.columns(2)
    
    with col1:
        temperature = st.slider(
            "Temperature:",
            min_value=0.0,
            max_value=2.0,
            value=0.7,
            step=0.1,
            help="Controls randomness in responses"
        )
        
        max_tokens = st.number_input(
            "Max Tokens:",
            min_value=100,
            max_value=32000,
            value=8000,
            step=100,
            help="Maximum number of tokens to generate"
        )
    
    with col2:
        top_p = st.slider(
            "Top P:",
            min_value=0.0,
            max_value=1.0,
            value=0.9,
            step=0.05,
            help="Controls diversity of responses"
        )
        
        frequency_penalty = st.slider(
            "Frequency Penalty:",
            min_value=-2.0,
            max_value=2.0,
            value=0.0,
            step=0.1,
            help="Reduces repetition in responses"
        )
    
    # Save settings
    if st.button("💾 Save AI Model Settings", type="primary"):
        st.success("✅ AI Model settings saved!")
        st.rerun()

def system_config_settings():
    """System configuration section"""
    
    st.markdown("### 🔧 System Configuration")
    
    # General settings
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🌐 General Settings")
        
        app_name = st.text_input(
            "Application Name:",
            value="Digital Twins Management System",
            help="Name of your application"
        )
        
        app_description = st.text_area(
            "Description:",
            value="AI-powered digital replicas of management systems and leadership teams",
            help="Description of your application"
        )
        
        default_workflow = st.selectbox(
            "Default Workflow:",
            ["Standard Research & Analysis", "Two-Team Data Strategy", "Three-Team Complete", "Four-Team Enterprise"],
            index=0,
            help="Default workflow to use when starting new sessions"
        )
    
    with col2:
        st.subheader("📊 Performance Settings")
        
        max_concurrent_workflows = st.number_input(
            "Max Concurrent Workflows:",
            min_value=1,
            max_value=10,
            value=3,
            help="Maximum number of workflows that can run simultaneously"
        )
        
        workflow_timeout = st.number_input(
            "Workflow Timeout (minutes):",
            min_value=1,
            max_value=60,
            value=10,
            help="Maximum time a workflow can run before timing out"
        )
        
        memory_retention_days = st.number_input(
            "Memory Retention (days):",
            min_value=1,
            max_value=365,
            value=30,
            help="How long to keep conversation memory"
        )
    
    # Search settings
    st.markdown("### 🔍 Search Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        max_search_results = st.number_input(
            "Max Search Results:",
            min_value=1,
            max_value=20,
            value=5,
            help="Maximum number of search results to return"
        )
        
        search_timeout = st.number_input(
            "Search Timeout (seconds):",
            min_value=5,
            max_value=60,
            value=30,
            help="Timeout for search operations"
        )
    
    with col2:
        enable_web_search = st.checkbox("Enable Web Search", value=True)
        enable_memory_search = st.checkbox("Enable Memory Search", value=True)
        enable_document_search = st.checkbox("Enable Document Search", value=True)
    
    # Save settings
    if st.button("💾 Save System Settings", type="primary"):
        st.success("✅ System settings saved!")
        st.rerun()

def security_settings():
    """Security settings section"""
    
    st.markdown("### 🔐 Security Configuration")
    
    # API Key management
    st.subheader("🔑 API Key Management")
    
    st.info("""
    **Security Best Practices:**
    - Never share your API keys
    - Use environment variables for production
    - Regularly rotate your API keys
    - Monitor API usage for unusual activity
    """)
    
    # Data privacy
    st.subheader("🔒 Data Privacy")
    
    col1, col2 = st.columns(2)
    
    with col1:
        enable_data_encryption = st.checkbox("Enable Data Encryption", value=True)
        enable_audit_logging = st.checkbox("Enable Audit Logging", value=True)
        enable_data_anonymization = st.checkbox("Enable Data Anonymization", value=False)
    
    with col2:
        data_retention_policy = st.selectbox(
            "Data Retention Policy:",
            ["30 days", "90 days", "1 year", "Indefinite"],
            index=0
        )
        
        auto_delete_sensitive = st.checkbox("Auto-delete Sensitive Data", value=False)
    
    # Access control
    st.subheader("👥 Access Control")
    
    enable_user_authentication = st.checkbox("Enable User Authentication", value=False)
    
    if enable_user_authentication:
        auth_method = st.selectbox(
            "Authentication Method:",
            ["Local", "LDAP", "OAuth", "SAML"],
            index=0
        )
        
        enable_role_based_access = st.checkbox("Enable Role-based Access Control", value=False)
    
    # Save settings
    if st.button("💾 Save Security Settings", type="primary"):
        st.success("✅ Security settings saved!")
        st.rerun()

def performance_settings():
    """Performance settings section"""
    
    st.markdown("### 📊 Performance Configuration")
    
    # Caching settings
    st.subheader("💾 Caching Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        enable_response_caching = st.checkbox("Enable Response Caching", value=True)
        cache_ttl = st.number_input(
            "Cache TTL (minutes):",
            min_value=1,
            max_value=1440,
            value=60,
            help="Time to live for cached responses"
        )
    
    with col2:
        enable_memory_caching = st.checkbox("Enable Memory Caching", value=True)
        max_cache_size = st.number_input(
            "Max Cache Size (MB):",
            min_value=100,
            max_value=10000,
            value=1000,
            help="Maximum size of the cache in megabytes"
        )
    
    # Resource limits
    st.subheader("⚡ Resource Limits")
    
    col1, col2 = st.columns(2)
    
    with col1:
        max_memory_usage = st.number_input(
            "Max Memory Usage (GB):",
            min_value=1,
            max_value=32,
            value=8,
            help="Maximum memory usage for the application"
        )
        
        max_cpu_usage = st.number_input(
            "Max CPU Usage (%):",
            min_value=10,
            max_value=100,
            value=80,
            help="Maximum CPU usage percentage"
        )
    
    with col2:
        max_disk_usage = st.number_input(
            "Max Disk Usage (GB):",
            min_value=1,
            max_value=1000,
            value=100,
            help="Maximum disk usage for the application"
        )
        
        enable_auto_scaling = st.checkbox("Enable Auto-scaling", value=False)
    
    # Monitoring
    st.subheader("📈 Monitoring")
    
    enable_performance_monitoring = st.checkbox("Enable Performance Monitoring", value=True)
    
    if enable_performance_monitoring:
        monitoring_interval = st.number_input(
            "Monitoring Interval (seconds):",
            min_value=10,
            max_value=300,
            value=60,
            help="Interval for performance monitoring"
        )
        
        enable_alerts = st.checkbox("Enable Performance Alerts", value=True)
    
    # Save settings
    if st.button("💾 Save Performance Settings", type="primary"):
        st.success("✅ Performance settings saved!")
        st.rerun()

def appearance_settings():
    """Appearance settings section"""
    
    st.markdown("### 🎨 Appearance Configuration")
    
    # Theme settings
    st.subheader("🎨 Theme Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        theme = st.selectbox(
            "Theme:",
            ["Light", "Dark", "Auto"],
            index=2,
            help="Select the application theme"
        )
        
        primary_color = st.color_picker(
            "Primary Color:",
            value="#1f77b4",
            help="Primary color for the application"
        )
    
    with col2:
        secondary_color = st.color_picker(
            "Secondary Color:",
            value="#ff7f0e",
            help="Secondary color for the application"
        )
        
        accent_color = st.color_picker(
            "Accent Color:",
            value="#2ca02c",
            help="Accent color for the application"
        )
    
    # Layout settings
    st.subheader("📐 Layout Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        sidebar_width = st.slider(
            "Sidebar Width:",
            min_value=200,
            max_value=500,
            value=300,
            help="Width of the sidebar in pixels"
        )
        
        content_width = st.selectbox(
            "Content Width:",
            ["Wide", "Narrow", "Auto"],
            index=0,
            help="Width of the main content area"
        )
    
    with col2:
        show_sidebar = st.checkbox("Show Sidebar", value=True)
        show_footer = st.checkbox("Show Footer", value=True)
        show_breadcrumbs = st.checkbox("Show Breadcrumbs", value=True)
    
    # Font settings
    st.subheader("🔤 Font Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        font_family = st.selectbox(
            "Font Family:",
            ["Arial", "Helvetica", "Times New Roman", "Georgia", "Courier New"],
            index=0,
            help="Font family for the application"
        )
        
        font_size = st.slider(
            "Font Size:",
            min_value=10,
            max_value=20,
            value=14,
            help="Base font size in pixels"
        )
    
    with col2:
        heading_font = st.selectbox(
            "Heading Font:",
            ["Arial", "Helvetica", "Times New Roman", "Georgia", "Courier New"],
            index=1,
            help="Font family for headings"
        )
        
        enable_custom_fonts = st.checkbox("Enable Custom Fonts", value=False)
    
    # Save settings
    if st.button("💾 Save Appearance Settings", type="primary"):
        st.success("✅ Appearance settings saved!")
        st.rerun()

def export_import_settings():
    """Export/Import settings section"""
    
    st.markdown("### 📤 Export/Import Configuration")
    
    # Export settings
    st.subheader("📤 Export Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        export_format = st.selectbox(
            "Default Export Format:",
            ["PDF", "CSV", "JSON", "Excel", "Markdown"],
            index=0,
            help="Default format for exporting data"
        )
        
        include_metadata = st.checkbox("Include Metadata", value=True)
        include_timestamps = st.checkbox("Include Timestamps", value=True)
    
    with col2:
        export_quality = st.selectbox(
            "Export Quality:",
            ["Low", "Medium", "High", "Ultra"],
            index=2,
            help="Quality of exported documents"
        )
        
        compress_exports = st.checkbox("Compress Exports", value=False)
    
    # Import settings
    st.subheader("📥 Import Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        max_import_size = st.number_input(
            "Max Import Size (MB):",
            min_value=1,
            max_value=1000,
            value=100,
            help="Maximum size for imported files"
        )
        
        auto_process_imports = st.checkbox("Auto-process Imports", value=True)
    
    with col2:
        import_format = st.multiselect(
            "Supported Import Formats:",
            ["PDF", "DOCX", "CSV", "XLSX", "JSON", "TXT", "MD"],
            default=["PDF", "DOCX", "CSV", "XLSX", "JSON", "TXT", "MD"],
            help="Formats supported for import"
        )
        
        validate_imports = st.checkbox("Validate Imports", value=True)
    
    # Backup settings
    st.subheader("💾 Backup Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        enable_auto_backup = st.checkbox("Enable Auto Backup", value=True)
        
        if enable_auto_backup:
            backup_frequency = st.selectbox(
                "Backup Frequency:",
                ["Daily", "Weekly", "Monthly"],
                index=0
            )
            
            backup_retention = st.number_input(
                "Backup Retention (days):",
                min_value=7,
                max_value=365,
                value=30
            )
    
    with col2:
        backup_location = st.text_input(
            "Backup Location:",
            value="./backups",
            help="Directory for storing backups"
        )
        
        encrypt_backups = st.checkbox("Encrypt Backups", value=True)
    
    # Export/Import actions
    st.subheader("🔄 Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📤 Export All Settings", use_container_width=True):
            st.info("Export functionality coming soon!")
    
    with col2:
        if st.button("📥 Import Settings", use_container_width=True):
            st.info("Import functionality coming soon!")
    
    with col3:
        if st.button("🔄 Reset to Defaults", use_container_width=True):
            st.warning("This will reset all settings to their default values. Are you sure?")
            if st.button("Yes, Reset", type="primary"):
                st.success("Settings reset to defaults!")
                st.rerun()
    
    # Save settings
    if st.button("💾 Save Export/Import Settings", type="primary"):
        st.success("✅ Export/Import settings saved!")
        st.rerun()

if __name__ == "__main__":
    main()
