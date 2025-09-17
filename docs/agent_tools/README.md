# Agent Tools Documentation

This directory contains detailed documentation for all tools and utilities used by the CrewAI Multi-Agent Workflow System.

## Overview

The agent tools module provides essential utilities and integrations that support the multi-agent workflows. These tools handle LLM communication, web search, PDF generation, and other critical functions.

## Tool Categories

### 1. LLM Wrappers
**Purpose**: Robust LLM communication with error handling and retry logic
**Files**: `robust_llm_v2.py`, `retry_llm.py`
**Key Features**:
- Exponential backoff retry logic
- Rate limiting and timeout handling
- Message processing and optimization
- Error recovery and fallback mechanisms

### 2. Search Tools
**Purpose**: Web search and information gathering
**Files**: `search_web.py`
**Key Features**:
- DuckDuckGo integration
- Search result processing and formatting
- Error handling and retry logic
- Result validation and quality checks

### 3. PDF Generation
**Purpose**: Professional PDF report generation
**Files**: `pdf_writer.py`
**Key Features**:
- Multiple template layouts
- Academic and professional formatting
- Table and chart generation
- Download link creation

### 4. Memory Management
**Purpose**: Conversation memory and context retrieval
**Files**: `local_memory.py`
**Key Features**:
- ChromaDB integration
- Vector similarity search
- Context retrieval and formatting
- Memory persistence and management

## LLM Wrappers

### RobustLLM (robust_llm_v2.py)

The `RobustLLM` class provides advanced LLM communication with comprehensive error handling:

```python
class RobustLLM(LLM):
    def __init__(self, *args, max_retries: int = 5, base_delay: float = 2.0, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_retries = max_retries
        self.base_delay = base_delay
    
    def call(self, messages, tools=None, callbacks=None, available_functions=None, from_task=None, from_agent=None, **kwargs):
        # Advanced retry logic with exponential backoff
        # Message processing and optimization
        # Error handling and recovery
```

#### Key Features

- **Exponential Backoff**: Intelligent retry delays with jitter
- **Message Processing**: Optimizes messages for better performance
- **Error Recovery**: Comprehensive error handling and recovery
- **CrewAI Integration**: Full compatibility with CrewAI parameters
- **Logging**: Detailed logging for debugging and monitoring

#### Configuration

```python
llm = RobustLLM(
    model="ollama/gpt-oss:20b",
    base_url="https://ollama.com",
    headers={'Authorization': f'Bearer {api_key}'},
    temperature=0.5,
    max_tokens=8000,
    max_retries=5,
    base_delay=2.0,
    system_message="You are an expert business consultant..."
)
```

### RetryLLM (retry_llm.py)

The `RetryLLM` class provides basic retry functionality:

```python
class RetryLLM(LLM):
    def __init__(self, *args, max_retries: int = 5, base_delay: float = 2.0, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_retries = max_retries
        self.base_delay = base_delay
    
    def call(self, messages, tools=None, callbacks=None, available_functions=None, from_task=None, from_agent=None, **kwargs):
        # Basic retry logic with exponential backoff
        # Error handling and recovery
```

#### Key Features

- **Simple Retry Logic**: Basic exponential backoff
- **Error Handling**: Graceful error handling
- **CrewAI Compatibility**: Full CrewAI parameter support
- **Lightweight**: Minimal overhead and complexity

## Search Tools

### Web Search (search_web.py)

The web search tool provides DuckDuckGo integration:

```python
@tool("search_web")
def search_web(query: str, max_results: int = 5) -> str:
    """
    Search the web for information using DuckDuckGo
    """
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
            return format_search_results(results)
    except Exception as e:
        return f"Search error: {e}"
```

#### Key Features

- **DuckDuckGo Integration**: Reliable web search
- **Result Formatting**: Structured search results
- **Error Handling**: Graceful error handling
- **Rate Limiting**: Built-in rate limiting
- **Result Validation**: Quality checks for results

#### Configuration

```python
# Environment variables
DUCKDUCKGO_MAX_RESULTS=5
SEARCH_RETRY_ATTEMPTS=3
SEARCH_DELAY_SECONDS=1
```

## PDF Generation

### PDF Writer (pdf_writer.py)

The PDF writer creates professional reports:

```python
class PDFWriter:
    def __init__(self):
        self.templates = {
            "academic": AcademicTemplate(),
            "professional": ProfessionalTemplate(),
            "hybrid": HybridTemplate()
        }
    
    def create_pdf(self, content: str, template_type: str = "hybrid") -> str:
        """
        Create PDF from markdown content
        """
        template = self.templates[template_type]
        return template.generate_pdf(content)
```

#### Key Features

- **Multiple Templates**: Academic, professional, and hybrid layouts
- **Markdown Support**: Converts markdown to PDF
- **Table Generation**: Creates formatted tables
- **Chart Support**: Generates charts and visualizations
- **Download Links**: Creates download links for Streamlit

#### Templates

1. **Academic Template**: University-style formatting
2. **Professional Template**: Business report formatting
3. **Hybrid Template**: Combination of academic and professional

#### Usage

```python
from agent_tools.pdf_writer import PDFWriter

writer = PDFWriter()
pdf_path = writer.create_pdf(content, template_type="hybrid")
```

## Memory Management

### Local Memory (local_memory.py)

The local memory manager handles conversation memory:

```python
class LocalMemoryManager:
    def __init__(self, db_path: str = "./memory_db"):
        self.client = chromadb.PersistentClient(path=db_path)
        self.collection = self.client.get_or_create_collection("conversations")
    
    def add_conversation(self, query: str, response: str, metadata: Dict[str, Any]):
        """
        Add conversation to memory
        """
        self.collection.add(
            documents=[f"{query}\n\n{response}"],
            metadatas=[metadata],
            ids=[str(uuid.uuid4())]
        )
    
    def search_memory(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """
        Search conversation memory
        """
        results = self.collection.query(
            query_texts=[query],
            n_results=max_results
        )
        return results
```

#### Key Features

- **ChromaDB Integration**: Vector database for semantic search
- **Local Embeddings**: ONNXMiniLM_L6_V2 model (no external API keys)
- **Semantic Search**: Vector similarity search
- **Metadata Support**: Rich metadata for conversations
- **Persistence**: Persistent storage across sessions

#### Configuration

```python
# Environment variables
MEMORY_DB_PATH="./memory_db"
MAX_MEMORY_RESULTS=5
EMBEDDING_MODEL="ONNXMiniLM_L6_V2"
```

## Error Handling

All tools include comprehensive error handling:

```python
try:
    result = tool_function()
    if result and result.strip():
        return result
    else:
        raise Exception("Empty result from tool")
except Exception as e:
    logger.error(f"Tool error: {e}")
    # Implement fallback or retry logic
    raise
```

## Performance Optimization

Tools are optimized for performance:

- **Caching**: Intelligent caching for repeated requests
- **Rate Limiting**: Built-in rate limiting
- **Timeout Handling**: Proper timeout management
- **Memory Management**: Efficient memory usage
- **Connection Pooling**: Reuse connections where possible

## Testing

Tools can be tested independently:

```python
# Test LLM wrapper
from agent_tools.robust_llm_v2 import create_robust_llm

# Test search tool
from agent_tools.search_web import search_web

# Test PDF writer
from agent_tools.pdf_writer import PDFWriter

# Test memory manager
from agent_tools.local_memory import LocalMemoryManager
```

## Configuration

Tool behavior can be configured through environment variables:

- `MAX_RETRIES`: Maximum retry attempts
- `BASE_DELAY`: Base delay for retries
- `MAX_RPM`: Rate limiting
- `TIMEOUT`: Request timeout
- `CACHE_SIZE`: Cache size for caching

## Monitoring

Tools include comprehensive monitoring:

- **Performance Metrics**: Execution time and resource usage
- **Error Tracking**: Error rates and types
- **Usage Statistics**: Tool usage patterns
- **Health Checks**: Tool availability and status

## Troubleshooting

Common tool issues and solutions:

1. **LLM Errors**: Check API keys and model availability
2. **Search Failures**: Verify internet connection and DuckDuckGo access
3. **PDF Generation**: Check dependencies and file permissions
4. **Memory Issues**: Verify ChromaDB installation and permissions
5. **Performance Issues**: Check rate limiting and caching

## Best Practices

1. **Error Handling**: Include comprehensive error handling
2. **Logging**: Provide detailed logging for debugging
3. **Performance**: Optimize for performance and reliability
4. **Testing**: Test thoroughly with different scenarios
5. **Documentation**: Keep documentation up to date
6. **Monitoring**: Include comprehensive monitoring
7. **Security**: Follow security best practices

## Extending Tools

To add new tools:

1. Create new file in `agent_tools/` directory
2. Follow existing patterns for tool creation
3. Include comprehensive error handling
4. Add proper logging and monitoring
5. Test thoroughly with different scenarios
6. Update documentation

## Support

For issues with specific tools:
1. Check the tool-specific documentation
2. Review error logs and messages
3. Test with simplified scenarios
4. Verify configuration and dependencies
5. Check system requirements and resources
