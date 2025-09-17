# UI Components Module

This module contains reusable Streamlit UI components for the CrewAI multi-agent workflow application. It provides modular UI elements for model selection, workflow selection, chat interface, and sidebar functionality.

## Structure

```
ui_components/
├── __init__.py                    # Module initialization
├── sidebar.py                     # Sidebar component
├── model_selection.py             # Model selection UI
├── workflow_selection.py          # Workflow selection UI
└── chat_interface.py              # Chat interface components
```

## Key Components

### Sidebar Component
- **Navigation**: Main navigation and controls
- **Status Display**: System status and information
- **Settings**: Configuration options
- **Memory Management**: Memory database controls

### Model Selection
- **Model Choice**: Local vs Cloud model selection
- **API Key Input**: Secure API key handling
- **Configuration**: Model parameters and settings
- **Status Indicators**: Connection status display

### Workflow Selection
- **Workflow Types**: 1-7 team workflow options
- **Mode Selection**: Native function calling vs pre-search
- **Information Display**: Workflow descriptions and details
- **Validation**: Input validation and error handling

### Chat Interface
- **Message Display**: Conversation history display
- **Input Handling**: User input and submission
- **Result Display**: Workflow results and outputs
- **Topic Extraction**: Conversation topic analysis

## Pseudocode Examples

### Sidebar Component
```python
def create_sidebar():
    """
    Pseudocode for sidebar component
    """
    with st.sidebar:
        # 1. Header
        st.title("🤖 CrewAI Workflow")
        
        # 2. Memory status
        if st.button("📊 Memory Status"):
            show_memory_stats()
        
        # 3. Clear memory
        if st.button("🗑️ Clear Memory"):
            clear_memory()
        
        # 4. Settings
        with st.expander("⚙️ Settings"):
            show_settings()
        
        # 5. Workflow info
        with st.expander("ℹ️ Workflow Info"):
            show_workflow_info()
```

### Model Selection UI
```python
def create_model_selection_ui():
    """
    Pseudocode for model selection UI
    """
    # 1. Model type selection
    model_type = st.radio(
        "Select Model Type:",
        ["Local Ollama", "Ollama Cloud"],
        help="Choose between local or cloud-based model"
    )
    
    # 2. API key input for cloud
    api_key = None
    if model_type == "Ollama Cloud":
        api_key = st.text_input(
            "API Key:",
            type="password",
            help="Enter your Ollama Cloud API key"
        )
    
    # 3. Model configuration
    with st.expander("🔧 Model Configuration"):
        temperature = st.slider("Temperature", 0.0, 2.0, 0.5)
        max_tokens = st.number_input("Max Tokens", 1000, 16000, 8000)
    
    # 4. Test connection
    if st.button("🔍 Test Connection"):
        test_model_connection(model_type, api_key)
    
    return model_type, api_key

def create_workflow_mode_ui():
    """
    Pseudocode for workflow mode selection
    """
    # 1. Mode selection
    use_native = st.checkbox(
        "Use Native Function Calling",
        value=False,
        help="Enable native function calling for better tool integration"
    )
    
    # 2. Mode description
    if use_native:
        st.info("✅ Native function calling enabled - agents can use tools directly")
    else:
        st.info("ℹ️ Pre-search mode - web search performed before workflow")
    
    return use_native
```

### Workflow Selection UI
```python
def create_workflow_selection_ui():
    """
    Pseudocode for workflow selection UI
    """
    # 1. Workflow options
    workflow_options = {
        "Single Team": "research_analysis",
        "Two Teams": "two_team",
        "Three Teams": "three_team",
        "Four Teams": "four_team",
        "Five Teams": "five_team",
        "Six Teams": "six_team",
        "Seven Teams": "seven_team"
    }
    
    # 2. Workflow selection
    selected_workflow = st.selectbox(
        "Select Workflow:",
        list(workflow_options.keys()),
        help="Choose the number of teams for your workflow"
    )
    
    # 3. Workflow description
    workflow_descriptions = {
        "Single Team": "Research → Analysis → Writing",
        "Two Teams": "Research → Data Strategy",
        "Three Teams": "Research → Data Strategy → Compliance & Risk",
        "Four Teams": "Research → Data Strategy → Compliance & Risk → Information Management",
        "Five Teams": "Research → Data Strategy → Compliance & Risk → Information Management → Tender Response",
        "Six Teams": "Research → Data Strategy → Compliance & Risk → Information Management → Tender Response → Project Delivery",
        "Seven Teams": "Research → Data Strategy → Compliance & Risk → Information Management → Tender Response → Project Delivery → Technical Documentation"
    }
    
    st.info(f"**Workflow:** {workflow_descriptions[selected_workflow]}")
    
    return workflow_options[selected_workflow]

def create_workflow_info_sidebar():
    """
    Pseudocode for workflow information sidebar
    """
    with st.expander("📋 Workflow Information"):
        # 1. Team descriptions
        team_info = {
            "Research & Analysis": "Conducts research and analysis",
            "Data Strategy": "Creates DAMA frameworks and strategies",
            "Compliance & Risk": "Handles regulatory compliance",
            "Information Management": "Manages data governance",
            "Tender Response": "Creates professional proposals",
            "Project Delivery": "Technical implementation",
            "Technical Documentation": "Generates code and documentation"
        }
        
        for team, description in team_info.items():
            st.write(f"**{team}:** {description}")
```

### Chat Interface Components
```python
def create_chat_interface():
    """
    Pseudocode for chat interface
    """
    # 1. Chat history display
    if 'conversation_history' in st.session_state:
        display_chat_history()
    
    # 2. Input area
    user_input = create_chat_input()
    
    # 3. Submit button
    if st.button("🚀 Run Workflow", type="primary"):
        if user_input:
            run_workflow(user_input)
        else:
            st.warning("Please enter a query")
    
    return user_input

def create_chat_input():
    """
    Pseudocode for chat input component
    """
    # 1. Text area for input
    user_input = st.text_area(
        "Enter your query:",
        height=100,
        placeholder="Ask about digital twins in education, AI implementation, data strategy, etc.",
        help="Enter a detailed query for the multi-agent workflow"
    )
    
    # 2. Character count
    if user_input:
        char_count = len(user_input)
        if char_count > 1000:
            st.warning(f"Query is {char_count} characters. Consider shortening for better performance.")
        else:
            st.success(f"Query length: {char_count} characters")
    
    return user_input

def display_workflow_results(result: str, workflow_type: str):
    """
    Pseudocode for displaying workflow results
    """
    # 1. Results header
    st.subheader(f"🤖 {workflow_type.replace('_', ' ').title()} Results")
    
    # 2. Results content
    with st.expander("📄 View Results", expanded=True):
        st.markdown(result)
    
    # 3. Download options
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📥 Download as PDF"):
            download_pdf(result, workflow_type)
    
    with col2:
        if st.button("💾 Save to Memory"):
            save_to_memory(result, workflow_type)
```

### Conversation Topics
```python
def create_conversation_topics_sidebar():
    """
    Pseudocode for conversation topics sidebar
    """
    with st.expander("💬 Conversation Topics"):
        # 1. Extract topics from conversation history
        if 'conversation_history' in st.session_state:
            topics = extract_conversation_topics(st.session_state.conversation_history)
            
            if topics:
                st.write("**Recent Topics:**")
                for topic in topics:
                    st.write(f"• {topic}")
            else:
                st.write("No topics identified yet")
        else:
            st.write("Start a conversation to see topics")

def extract_conversation_topics(conversation_history: List[Dict]) -> List[str]:
    """
    Pseudocode for extracting conversation topics
    """
    # 1. Extract text from conversations
    all_text = []
    for conv in conversation_history[-5:]:  # Last 5 conversations
        if isinstance(conv, dict):
            all_text.append(conv.get('query', ''))
            all_text.append(conv.get('response', ''))
        else:
            all_text.append(str(conv))
    
    # 2. Simple keyword extraction
    text = ' '.join(all_text).lower()
    keywords = ['digital twin', 'AI', 'education', 'data', 'strategy', 'compliance', 'risk']
    
    # 3. Find mentioned keywords
    topics = [keyword for keyword in keywords if keyword in text]
    
    return topics[:5]  # Return top 5 topics
```

## Usage Examples

### Basic UI Setup
```python
from ui_components import create_sidebar, create_model_selection_ui

# Create sidebar
create_sidebar()

# Create model selection
model_type, api_key = create_model_selection_ui()
```

### Workflow Selection
```python
from ui_components import create_workflow_selection_ui, create_workflow_mode_ui

# Select workflow
workflow_type = create_workflow_selection_ui()

# Select mode
use_native = create_workflow_mode_ui()
```

### Chat Interface
```python
from ui_components import create_chat_interface, display_workflow_results

# Create chat interface
user_input = create_chat_interface()

# Display results
if workflow_result:
    display_workflow_results(workflow_result, workflow_type)
```

## Component Integration

### Main Application Integration
```python
def main():
    """
    Pseudocode for main application with UI components
    """
    # 1. Configure page
    st.set_page_config(page_title="CrewAI Workflow", layout="wide")
    
    # 2. Create sidebar
    create_sidebar()
    
    # 3. Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Model and workflow selection
        model_type, api_key = create_model_selection_ui()
        workflow_type = create_workflow_selection_ui()
        use_native = create_workflow_mode_ui()
        
        # Chat interface
        user_input = create_chat_interface()
    
    with col2:
        # Workflow information
        create_workflow_info_sidebar()
        create_conversation_topics_sidebar()
```

## Error Handling

### Input Validation
```python
def validate_user_input(user_input: str) -> Tuple[bool, str]:
    """
    Pseudocode for input validation
    """
    if not user_input or not user_input.strip():
        return False, "Please enter a query"
    
    if len(user_input) < 10:
        return False, "Query too short. Please provide more details."
    
    if len(user_input) > 5000:
        return False, "Query too long. Please shorten your query."
    
    return True, "Valid input"

def handle_ui_errors(error: Exception) -> None:
    """
    Pseudocode for UI error handling
    """
    if "connection" in str(error).lower():
        st.error("Connection error. Please check your internet connection.")
    elif "api" in str(error).lower():
        st.error("API error. Please check your API key.")
    else:
        st.error(f"An error occurred: {error}")
```

## Testing

### Component Tests
```python
def test_sidebar_creation():
    """Test sidebar component creation"""
    sidebar = create_sidebar()
    assert sidebar is not None

def test_model_selection():
    """Test model selection UI"""
    model_type, api_key = create_model_selection_ui()
    assert model_type in ["Local Ollama", "Ollama Cloud"]

def test_workflow_selection():
    """Test workflow selection UI"""
    workflow_type = create_workflow_selection_ui()
    assert workflow_type in ["research_analysis", "two_team", "three_team", "four_team", "five_team", "six_team", "seven_team"]
```
