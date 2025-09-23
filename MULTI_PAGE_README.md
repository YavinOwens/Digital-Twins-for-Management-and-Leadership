# Digital Twins Management System - Multi-Page Application

This document explains how to convert your single-page Streamlit RAG application into a multi-page application.

## 🚀 Quick Start

### Option 1: Use the New Multi-Page App
```bash
streamlit run streamlit_app_multi_page.py
```

### Option 2: Convert Existing App
1. Backup your current `streamlit_app.py`
2. Rename `streamlit_app_multi_page.py` to `streamlit_app.py`
3. Run: `streamlit run streamlit_app.py`

## 📁 New File Structure

```
web_knowledge/
├── streamlit_app_multi_page.py    # Main multi-page app
├── pages/                         # Page directory (auto-detected by Streamlit)
│   ├── 1_🏠_Home.py              # Landing page
│   ├── 2_🤖_Workflows.py         # Workflow execution
│   ├── 3_📁_Documents.py         # Document management
│   ├── 4_💬_Chat.py              # Chat interface
│   ├── 5_📊_Analytics.py         # Analytics dashboard
│   ├── 6_⚙️_Settings.py          # Configuration
│   └── 7_📚_Help.py              # Help & documentation
├── shared/                        # Shared components
│   ├── __init__.py
│   ├── components.py              # Reusable UI components
│   ├── utils.py                   # Utility functions
│   └── config.py                  # Configuration management
└── ... (existing structure)
```

## 🎯 Key Features

### **Multi-Page Navigation**
- **Automatic Sidebar**: Streamlit automatically creates navigation
- **Page Routing**: Seamless navigation between pages
- **Consistent UI**: Shared components across all pages
- **State Management**: Session state preserved across pages

### **Page Structure**
1. **🏠 Home**: Landing page with system overview
2. **🤖 Workflows**: Multi-agent workflow execution
3. **📁 Documents**: Document upload and management
4. **💬 Chat**: Conversational interface
5. **📊 Analytics**: System analytics and insights
6. **⚙️ Settings**: Configuration and preferences
7. **📚 Help**: Documentation and support

### **Shared Components**
- **Header/Footer**: Consistent branding
- **Sidebar Info**: System status and navigation
- **UI Components**: Reusable cards, metrics, and forms
- **Utilities**: Common functions and helpers

## 🔧 Implementation Details

### **Streamlit Pages Convention**
Streamlit automatically detects pages in the `pages/` directory. Page order is determined by:
1. **Number prefix**: `1_`, `2_`, etc.
2. **Icon prefix**: `🏠`, `🤖`, etc.
3. **Alphabetical order**: If no prefix

### **Page Naming Convention**
```
{number}_{icon}_{name}.py
```
Examples:
- `1_🏠_Home.py`
- `2_🤖_Workflows.py`
- `3_📁_Documents.py`

### **Navigation Between Pages**
```python
# Switch to another page
st.switch_page("pages/2_🤖_Workflows.py")

# Or use button navigation
if st.button("Go to Workflows"):
    st.switch_page("pages/2_🤖_Workflows.py")
```

### **Shared State Management**
```python
# Access shared utilities
from shared.utils import get_memory_stats, initialize_llm
from shared.components import create_header, create_footer

# Use shared configuration
from shared.config import get_config, set_config
```

## 📋 Migration Steps

### **Step 1: Create Pages Directory**
```bash
mkdir pages
```

### **Step 2: Move Existing Code**
1. Extract workflow logic → `pages/2_🤖_Workflows.py`
2. Extract document logic → `pages/3_📁_Documents.py`
3. Extract chat logic → `pages/4_💬_Chat.py`
4. Create new pages for analytics, settings, help

### **Step 3: Create Shared Components**
1. Extract common UI components → `shared/components.py`
2. Extract utility functions → `shared/utils.py`
3. Create configuration management → `shared/config.py`

### **Step 4: Update Imports**
```python
# Old imports
from agent_tools import search_web
from local_memory import add_to_memory

# New imports (in pages)
from shared.utils import get_memory_stats
from shared.components import create_header
```

## 🎨 Customization

### **Adding New Pages**
1. Create new file in `pages/` directory
2. Follow naming convention: `{number}_{icon}_{name}.py`
3. Import shared components
4. Add navigation in sidebar

### **Modifying Shared Components**
- Edit `shared/components.py` for UI changes
- Edit `shared/utils.py` for utility functions
- Edit `shared/config.py` for configuration

### **Styling and Theming**
- Modify `create_header()` and `create_footer()` in `shared/components.py`
- Use Streamlit's theming capabilities
- Custom CSS in `shared/components.py`

## 🔍 Testing

### **Test Navigation**
1. Start the app: `streamlit run streamlit_app_multi_page.py`
2. Click through all pages
3. Verify state persistence
4. Test shared components

### **Test Functionality**
1. Upload documents
2. Run workflows
3. Use chat interface
4. Check analytics
5. Modify settings

## 🚨 Troubleshooting

### **Common Issues**

**Pages not showing in sidebar:**
- Check file naming convention
- Ensure files are in `pages/` directory
- Verify Python syntax

**Import errors:**
- Check `shared/` directory structure
- Verify `__init__.py` files
- Update import paths

**State not persisting:**
- Use `st.session_state` for persistent data
- Initialize state in main app
- Check state initialization

**Navigation not working:**
- Use `st.switch_page()` for navigation
- Check page file paths
- Verify page exists

### **Debug Mode**
```python
# Add to any page for debugging
st.write("Session State:", st.session_state)
st.write("Current Page:", st.get_option("server.headless"))
```

## 📚 Additional Resources

### **Streamlit Pages Documentation**
- [Streamlit Pages Guide](https://docs.streamlit.io/library/advanced-features/pages)
- [Multi-Page Apps Tutorial](https://docs.streamlit.io/library/advanced-features/pages)

### **Best Practices**
- Keep pages focused and single-purpose
- Use shared components for consistency
- Implement proper error handling
- Test navigation thoroughly

### **Performance Tips**
- Use `@st.cache_data` for expensive operations
- Minimize imports in page files
- Use shared utilities efficiently
- Monitor memory usage

## 🎉 Benefits of Multi-Page Architecture

### **User Experience**
- **Better Organization**: Clear separation of functionality
- **Faster Navigation**: Quick access to specific features
- **Reduced Complexity**: Simpler, focused interfaces
- **Better Performance**: Load only what's needed

### **Development**
- **Modular Code**: Easier to maintain and extend
- **Reusable Components**: Shared UI elements
- **Team Collaboration**: Multiple developers can work on different pages
- **Testing**: Easier to test individual pages

### **Scalability**
- **Easy Extension**: Add new pages without affecting existing ones
- **Feature Isolation**: Changes to one page don't affect others
- **Resource Optimization**: Load components on demand
- **Future-Proof**: Easy to add new features

## 🔄 Migration Checklist

- [ ] Create `pages/` directory
- [ ] Create `shared/` directory with components
- [ ] Move workflow logic to `pages/2_🤖_Workflows.py`
- [ ] Move document logic to `pages/3_📁_Documents.py`
- [ ] Move chat logic to `pages/4_💬_Chat.py`
- [ ] Create analytics page `pages/5_📊_Analytics.py`
- [ ] Create settings page `pages/6_⚙️_Settings.py`
- [ ] Create help page `pages/7_📚_Help.py`
- [ ] Create home page `pages/1_🏠_Home.py`
- [ ] Update all import statements
- [ ] Test navigation between pages
- [ ] Test shared state management
- [ ] Test all functionality
- [ ] Update documentation

## 🎯 Next Steps

1. **Test the multi-page app** with your existing data
2. **Customize pages** to match your specific needs
3. **Add new features** using the modular architecture
4. **Optimize performance** based on usage patterns
5. **Deploy** the multi-page application

---

**Need Help?** Check the Help page in the application or refer to the troubleshooting section above.
