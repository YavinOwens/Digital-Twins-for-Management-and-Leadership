# 🚀 Quick Start Guide - Multi-Page Application

## ✅ Application Status
Your **Digital Twins Management & Leadership System** multi-page application is now running successfully!

### 🌐 Access Your Application
**URL**: `http://localhost:8502`

### 🔧 What I Fixed
1. **✅ Installed Missing Dependencies**
   - `plotly` - For interactive charts in Analytics page
   - `psutil` - For system monitoring and performance metrics

2. **✅ Created Streamlit Configuration**
   - `.streamlit/secrets.toml` - API keys and sensitive configuration
   - `.streamlit/config.toml` - Streamlit app configuration

3. **✅ Fixed Secrets Access**
   - Updated pages to handle missing secrets gracefully
   - Added proper error handling for API key access

### 📱 Available Pages
Navigate through these pages using the sidebar:

1. **🏠 Home** - System overview and quick start
2. **🤖 Workflows** - Multi-agent workflow execution (1-7 teams)
3. **📁 Documents** - Document upload and management
4. **💬 Chat** - Conversational interface
5. **📊 Analytics** - System analytics with interactive charts
6. **⚙️ Settings** - Configuration and preferences
7. **📚 Help** - Documentation and support

### 🔑 API Configuration
To use the AI features, you'll need to:

1. **Get an Ollama Cloud API Key**:
   - Visit: https://ollama.ai/settings
   - Sign up/login and get your API key

2. **Add API Key to Secrets**:
   - Edit `.streamlit/secrets.toml`
   - Replace `your_ollama_api_key_here` with your actual API key
   - Or enter it directly in the Settings page

### 🎯 Next Steps
1. **Open the application**: Go to `http://localhost:8502`
2. **Configure API keys**: Go to Settings → AI Models
3. **Upload documents**: Go to Documents page
4. **Run workflows**: Go to Workflows page
5. **Explore features**: Navigate through all pages

### 🛠️ Management Commands

**Stop the application**:
```bash
pkill -f streamlit
```

**Start the application**:
```bash
cd /Users/yavin/python_projects/web_knowledge
source venv/bin/activate
streamlit run streamlit_app_multi_page.py
```

**Check if running**:
```bash
ps aux | grep streamlit
```

### 🎉 Features Available
- **Multi-Page Navigation**: Clean, organized interface
- **Multi-Agent Workflows**: 1-7 team configurations
- **Document Processing**: 15+ file formats supported
- **Memory System**: Conversation and document memory
- **Web Search**: Real-time DuckDuckGo integration
- **Analytics Dashboard**: Interactive charts and metrics
- **Settings Management**: Comprehensive configuration
- **Help System**: Complete documentation

### 🔍 Troubleshooting
If you encounter any issues:

1. **Check dependencies**: `pip list | grep -E "(plotly|psutil|streamlit)"`
2. **Check secrets**: Verify `.streamlit/secrets.toml` exists
3. **Check logs**: Look at terminal output for errors
4. **Restart app**: Stop and start the application

### 📚 Documentation
- **Complete Guide**: See `MULTI_PAGE_README.md`
- **Architecture**: See `ARCHITECTURE.md`
- **Installation**: See `INSTALLATION_GUIDE.md`

---

**🎉 Your multi-page RAG application is ready to use!**
