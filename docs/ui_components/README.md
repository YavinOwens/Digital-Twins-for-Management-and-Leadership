# UI Components Documentation

This directory contains detailed documentation for all Streamlit UI components in the CrewAI Multi-Agent Workflow System.

## Overview

The UI components module provides reusable Streamlit components that create a clean, modular, and maintainable user interface. Components are organized by functionality and can be easily customized and extended.

## Component Structure

```
ui_components/
├── __init__.py              # Module initialization and exports
├── sidebar.py               # Sidebar navigation and controls
├── model_selection.py       # Model selection components
├── workflow_selection.py    # Workflow selection components
└── chat_interface.py        # Chat interface components
```

## Component Categories

### 1. Sidebar Components
**File**: `sidebar.py`
**Purpose**: Navigation, controls, and system information
**Key Components**:
- `create_sidebar()`: Main sidebar with navigation and controls
- `create_model_selection_ui()`: Model selection interface
- `create_workflow_selection_ui()`: Workflow selection interface
- `create_chat_interface()`: Chat interface components

### 2. Model Selection
**File**: `model_selection.py`
**Purpose**: Model configuration and selection
**Key Components**:
- `create_model_selection_ui()`: Model selection interface
- `create_workflow_mode_ui()`: Workflow mode selection
- `create_api_key_input()`: API key input component

### 3. Workflow Selection
**File**: `workflow_selection.py`
**Purpose**: Workflow type selection and configuration
**Key Components**:
- `create_workflow_selection_ui()`: Workflow selection interface
- `create_workflow_info()`: Workflow information display
- `create_workflow_config()`: Workflow configuration options

### 4. Chat Interface
**File**: `chat_interface.py`
**Purpose**: Chat interface and message handling
**Key Components**:
- `create_chat_interface()`: Main chat interface
- `create_message_display()`: Message display components
- `create_input_components()`: Input components

## Sidebar Components

### Main Sidebar (sidebar.py)

The main sidebar provides navigation and system controls:

```python
def create_sidebar():
    """
    Create the main sidebar with navigation and controls
    """
    with st.sidebar:
        st.title("🤖 CrewAI Workflow Assistant")
        
        # Model selection
        model_type = create_model_selection_ui()
        
        # Workflow selection
        workflow_type = create_workflow_selection_ui()
        
        # System information
        create_system_info()
        
        # Configuration
        create_configuration_panel()
```

#### Key Features

- **Navigation**: Easy navigation between different sections
- **Model Selection**: Choose between local and cloud models
- **Workflow Selection**: Select from 1-7 team workflows
- **System Info**: Display system status and information
- **Configuration**: Access to configuration options

### Model Selection (model_selection.py)

The model selection component handles model configuration:

```python
def create_model_selection_ui():
    """
    Create model selection interface
    """
    st.subheader("🔧 Model Configuration")
    
    # Model type selection
    model_type = st.radio(
        "Select Model Type:",
        ["Local Ollama", "Ollama Cloud (Turbo)"],
        help="Choose between local or cloud model"
    )
    
    # API key input for cloud
    if model_type == "Ollama Cloud (Turbo)":
        api_key = st.text_input(
            "API Key:",
            type="password",
            help="Enter your Ollama Cloud API key"
        )
    else:
        api_key = None
    
    return model_type, api_key
```

#### Key Features

- **Model Type Selection**: Choose between local and cloud models
- **API Key Input**: Secure API key input for cloud models
- **Help Text**: Contextual help and guidance
- **Validation**: Input validation and error handling

### Workflow Selection (workflow_selection.py)

The workflow selection component handles workflow configuration:

```python
def create_workflow_selection_ui():
    """
    Create workflow selection interface
    """
    st.subheader("🔄 Workflow Selection")
    
    # Workflow type selection
    workflow_type = st.selectbox(
        "Select Workflow:",
        [
            "Single Team (Research & Analysis)",
            "Two Teams (Research → Data Strategy)",
            "Three Teams (Research → Data Strategy → Compliance & Risk)",
            "Four Teams (Research → Data Strategy → Compliance & Risk → Information Management)",
            "Five Teams (+ Tender Response)",
            "Six Teams (+ Project Delivery)",
            "Seven Teams (+ Technical Documentation)"
        ],
        help="Choose the number of teams for your workflow"
    )
    
    # Workflow information
    create_workflow_info(workflow_type)
    
    return workflow_type
```

#### Key Features

- **Workflow Types**: 1-7 team workflow options
- **Workflow Information**: Detailed information about each workflow
- **Help Text**: Contextual help and guidance
- **Validation**: Workflow validation and error handling

### Chat Interface (chat_interface.py)

The chat interface component handles user interaction:

```python
def create_chat_interface():
    """
    Create chat interface components
    """
    # Chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask me anything..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Process message
        process_message(prompt)
```

#### Key Features

- **Chat History**: Persistent chat history
- **Message Display**: Rich message display with formatting
- **Input Handling**: User input processing
- **Real-time Updates**: Real-time chat updates

## Component Configuration

### Environment Variables

Components can be configured through environment variables:

```python
# UI Configuration
STREAMLIT_PORT=8501
STREAMLIT_ADDRESS=localhost
STREAMLIT_THEME=light

# Model Configuration
DEFAULT_MODEL_TYPE=local
DEFAULT_WORKFLOW_TYPE=single_team

# Display Configuration
MAX_MESSAGE_LENGTH=10000
ENABLE_MARKDOWN=True
ENABLE_CODE_HIGHLIGHTING=True
```

### Styling

Components use consistent styling:

```python
# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    
    .workflow-card {
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    
    .status-indicator {
        display: inline-block;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        margin-right: 0.5rem;
    }
    
    .status-success { background-color: #4caf50; }
    .status-error { background-color: #f44336; }
    .status-warning { background-color: #ff9800; }
</style>
""", unsafe_allow_html=True)
```

## Error Handling

All components include comprehensive error handling:

```python
try:
    result = component_function()
    if result:
        return result
    else:
        st.error("Component error: Empty result")
        return None
except Exception as e:
    st.error(f"Component error: {e}")
    logger.error(f"Component error: {e}")
    return None
```

## Performance Optimization

Components are optimized for performance:

- **Lazy Loading**: Load components only when needed
- **Caching**: Cache expensive operations
- **State Management**: Efficient state management
- **Memory Management**: Efficient memory usage
- **Rendering Optimization**: Optimize rendering performance

## Testing

Components can be tested independently:

```python
# Test sidebar component
from ui_components.sidebar import create_sidebar

# Test model selection
from ui_components.model_selection import create_model_selection_ui

# Test workflow selection
from ui_components.workflow_selection import create_workflow_selection_ui

# Test chat interface
from ui_components.chat_interface import create_chat_interface
```

## Customization

Components can be easily customized:

### Custom Styling

```python
def create_custom_component():
    """
    Create a custom component with custom styling
    """
    st.markdown("""
    <style>
        .custom-component {
            background-color: #f0f0f0;
            padding: 1rem;
            border-radius: 8px;
        }
    </style>
    """, unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="custom-component">', unsafe_allow_html=True)
        # Component content
        st.markdown('</div>', unsafe_allow_html=True)
```

### Custom Configuration

```python
def create_configurable_component(config: Dict[str, Any]):
    """
    Create a component with custom configuration
    """
    # Use configuration to customize component behavior
    if config.get("show_help", True):
        st.help("This is a configurable component")
    
    if config.get("enable_validation", True):
        # Add validation logic
        pass
```

## Accessibility

Components are designed with accessibility in mind:

- **Keyboard Navigation**: Full keyboard navigation support
- **Screen Reader Support**: Proper ARIA labels and descriptions
- **Color Contrast**: High contrast color schemes
- **Font Sizing**: Scalable font sizes
- **Focus Management**: Proper focus management

## Responsive Design

Components are responsive and work on different screen sizes:

- **Mobile Support**: Mobile-responsive design
- **Tablet Support**: Tablet-optimized layout
- **Desktop Support**: Full desktop functionality
- **Adaptive Layout**: Layout adapts to screen size

## Internationalization

Components support internationalization:

- **Multi-language Support**: Support for multiple languages
- **Localization**: Date, time, and number formatting
- **RTL Support**: Right-to-left language support
- **Unicode Support**: Full Unicode character support

## Troubleshooting

Common component issues and solutions:

1. **Rendering Issues**: Check Streamlit version and dependencies
2. **State Issues**: Verify session state management
3. **Styling Issues**: Check CSS and HTML formatting
4. **Performance Issues**: Optimize rendering and state management
5. **Accessibility Issues**: Verify ARIA labels and keyboard navigation

## Best Practices

1. **Modularity**: Keep components modular and reusable
2. **Error Handling**: Include comprehensive error handling
3. **Performance**: Optimize for performance and responsiveness
4. **Accessibility**: Follow accessibility best practices
5. **Testing**: Test thoroughly with different scenarios
6. **Documentation**: Keep documentation up to date
7. **Styling**: Use consistent styling and theming

## Extending Components

To add new components:

1. Create new file in `ui_components/` directory
2. Follow existing patterns for component creation
3. Include comprehensive error handling
4. Add proper styling and theming
5. Test thoroughly with different scenarios
6. Update documentation

## Support

For issues with specific components:
1. Check the component-specific documentation
2. Review error logs and messages
3. Test with simplified scenarios
4. Verify configuration and dependencies
5. Check Streamlit version and compatibility
