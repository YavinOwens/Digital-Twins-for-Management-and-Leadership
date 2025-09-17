# Agent Tools Module

This module contains all the tools and utilities used by the CrewAI agents to perform their tasks. It includes search tools, PDF generation, LLM wrappers, and analysis tools.

## Structure

```
agent_tools/
├── __init__.py                    # Module initialization
├── search_tool.py                 # Web search functionality using DuckDuckGo
├── analysis_tool.py               # Data analysis and insight extraction
├── pdf_writer.py                  # Academic PDF report generation
├── pdf_templates.py               # Professional PDF templates
├── mockup_pdf_template.py         # Exact mockup PDF replication
├── xhtml2pdf_template.py          # xhtml2pdf-based templates
├── robust_llm.py                  # Basic LLM wrapper with retry logic
├── robust_llm_v2.py               # Advanced LLM wrapper with intelligent handling
└── retry_llm.py                   # Retry wrapper for LLM calls
```

## Key Components

### Search Tools
- **DuckDuckGo Integration**: Web search without API keys
- **Result Parsing**: Structured extraction of search results
- **Quality Assessment**: Source credibility evaluation

### PDF Generation
- **Multiple Templates**: Academic, professional, and mockup styles
- **ReportLab Integration**: Native Python PDF generation
- **xhtml2pdf Support**: HTML-to-PDF conversion
- **Custom Styling**: Professional layouts and formatting

### LLM Wrappers
- **Retry Logic**: Exponential backoff for failed requests
- **Error Handling**: Graceful degradation and recovery
- **Rate Limiting**: Built-in request throttling
- **Message Processing**: Intelligent content optimization

## Pseudocode Examples

### Search Tool Usage
```python
@tool
def search_web(search_query: str) -> str:
    """
    Pseudocode for web search functionality
    """
    # 1. Initialize DuckDuckGo search
    with DDGS() as ddgs:
        # 2. Perform search with query
        results = ddgs.text(search_query, max_results=5)
        
        # 3. Parse and format results
        formatted_results = []
        for result in results:
            formatted_results.append({
                'title': result.get('title', ''),
                'body': result.get('body', ''),
                'href': result.get('href', ''),
                'quality_score': assess_source_quality(result)
            })
        
        # 4. Return structured results
        return format_search_output(formatted_results)
```

### PDF Generation Pattern
```python
class PDFTemplate:
    """
    Pseudocode for PDF template system
    """
    def __init__(self, template_type: str):
        self.template_type = template_type
        self.styles = self.setup_styles()
    
    def generate_pdf(self, content_data: Dict[str, Any]) -> str:
        """
        Generate PDF from content data
        """
        # 1. Create document with page setup
        doc = SimpleDocTemplate(filename, pagesize=A4)
        
        # 2. Build content elements
        story = []
        story.append(self.create_cover_page(content_data['title']))
        story.append(self.create_table_of_contents(content_data['sections']))
        
        # 3. Add main content sections
        for section in content_data['sections']:
            story.append(self.create_section(section))
        
        # 4. Build PDF with custom header/footer
        doc.build(story, onFirstPage=self.create_header_footer)
        
        return filename
```

### LLM Wrapper Pattern
```python
class RobustLLM(LLM):
    """
    Pseudocode for robust LLM wrapper
    """
    def __init__(self, max_retries: int = 3, retry_delay: float = 2.0):
        self.max_retries = max_retries
        self.retry_delay = retry_delay
    
    def call(self, messages, **kwargs) -> str:
        """
        Make LLM call with retry logic
        """
        for attempt in range(self.max_retries):
            try:
                # 1. Process messages for optimization
                processed_messages = self._process_messages(messages)
                
                # 2. Make the actual LLM call
                result = super().call(processed_messages, **kwargs)
                
                # 3. Validate response
                if result and result.strip():
                    return result
                else:
                    raise EmptyResponseError("Empty response received")
                    
            except Exception as e:
                if attempt < self.max_retries - 1:
                    # 4. Wait before retry with exponential backoff
                    time.sleep(self.retry_delay * (2 ** attempt))
                    continue
                else:
                    raise MaxRetriesExceededError(f"All retries failed: {e}")
```

### Analysis Tool Pattern
```python
class AnalysisTool(BaseTool):
    """
    Pseudocode for data analysis tool
    """
    def _run(self, data: str) -> str:
        """
        Analyze data and extract insights
        """
        # 1. Parse input data
        parsed_data = self._parse_input(data)
        
        # 2. Extract key themes
        themes = self._extract_themes(parsed_data)
        
        # 3. Identify statistics and metrics
        statistics = self._extract_statistics(parsed_data)
        
        # 4. Find challenges and opportunities
        challenges = self._identify_challenges(parsed_data)
        opportunities = self._identify_opportunities(parsed_data)
        
        # 5. Generate structured analysis
        analysis = {
            'themes': themes,
            'statistics': statistics,
            'challenges': challenges,
            'opportunities': opportunities,
            'summary': self._generate_summary(themes, statistics)
        }
        
        return self._format_analysis(analysis)
```

## Usage Examples

### Basic Search
```python
from agent_tools.search_tool import search_web

# Search for information
results = search_web("digital twins in education")
print(results)
```

### PDF Generation
```python
from agent_tools.pdf_writer import create_pdf_report

# Generate academic PDF
pdf_path = create_pdf_report(
    content="Your report content here",
    filename="report.pdf",
    template="academic"
)
```

### LLM with Retry Logic
```python
from agent_tools.robust_llm_v2 import create_robust_llm

# Create robust LLM instance
llm = create_robust_llm(use_cloud=True, api_key="your_key")

# Use in CrewAI agents
agent = Agent(
    role="Researcher",
    goal="Research topics",
    llm=llm,
    tools=[search_web]
)
```

## Tool Integration

### With CrewAI Agents
```python
from crewai import Agent, Task, Crew
from agent_tools.search_tool import search_web
from agent_tools.analysis_tool import AnalysisTool

# Create agent with tools
researcher = Agent(
    role="Research Specialist",
    goal="Conduct research",
    tools=[search_web, AnalysisTool()],
    llm=llm
)

# Create task that uses tools
research_task = Task(
    description="Research digital twins and analyze findings",
    agent=researcher
)
```

## Error Handling

### Retry Logic
```python
def retry_with_backoff(func, max_retries=3, base_delay=1.0):
    """
    Pseudocode for retry with exponential backoff
    """
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt < max_retries - 1:
                delay = base_delay * (2 ** attempt)
                time.sleep(delay)
                continue
            else:
                raise e
```

### Graceful Degradation
```python
def safe_tool_execution(tool_func, fallback_value=""):
    """
    Pseudocode for safe tool execution
    """
    try:
        return tool_func()
    except Exception as e:
        logger.warning(f"Tool execution failed: {e}")
        return fallback_value
```

## Performance Optimization

### Caching
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def cached_search(query: str) -> str:
    """
    Cached search to avoid duplicate requests
    """
    return search_web(query)
```

### Rate Limiting
```python
import time
from threading import Lock

class RateLimiter:
    def __init__(self, max_requests: int, time_window: int):
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = []
        self.lock = Lock()
    
    def wait_if_needed(self):
        with self.lock:
            now = time.time()
            # Remove old requests outside time window
            self.requests = [req_time for req_time in self.requests 
                           if now - req_time < self.time_window]
            
            if len(self.requests) >= self.max_requests:
                sleep_time = self.time_window - (now - self.requests[0])
                time.sleep(sleep_time)
            
            self.requests.append(now)
```

## Testing

### Unit Tests
```python
def test_search_tool():
    """Test search tool functionality"""
    result = search_web("test query")
    assert isinstance(result, str)
    assert len(result) > 0

def test_pdf_generation():
    """Test PDF generation"""
    content = "Test content for PDF"
    pdf_path = create_pdf_report(content, "test.pdf")
    assert os.path.exists(pdf_path)
```

### Integration Tests
```python
def test_llm_wrapper():
    """Test LLM wrapper with retry logic"""
    llm = create_robust_llm(use_cloud=False)
    response = llm.call([{"role": "user", "content": "Hello"}])
    assert response is not None
```
