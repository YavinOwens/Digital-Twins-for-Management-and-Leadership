# PreSearch Module

This module handles pre-search functionality that combines web search and memory search to provide comprehensive context for the CrewAI multi-agent workflows. It intelligently searches both external sources and internal memory to gather relevant information before workflow execution.

## Structure

```
presearch/
├── __init__.py                    # Module initialization
├── presearch_manager.py           # Main pre-search functionality
└── test_presearch.py              # Pre-search testing utilities
```

## Key Components

### PreSearch Manager
- **Web Search Integration**: DuckDuckGo search for external information
- **Memory Search**: ChromaDB-based semantic search of past conversations
- **Context Combination**: Intelligent merging of search results
- **Query Optimization**: Enhanced search query generation

### Search Sources
- **Web Search**: Real-time information from the internet
- **Memory Database**: Past conversation history and insights
- **Conversation History**: Current session context
- **Combined Context**: Merged and ranked search results

## Pseudocode Examples

### PreSearch Manager Class
```python
class PreSearchManager:
    """
    Pseudocode for pre-search manager
    """
    def __init__(self, memory_enabled: bool = True, max_memory_results: int = 3):
        self.memory_enabled = memory_enabled
        self.max_memory_results = max_memory_results
        self.memory_manager = None
        
        if memory_enabled:
            self.memory_manager = initialize_memory_manager()
    
    def search_and_combine_context(
        self, 
        query: str, 
        conversation_history: Optional[List[Any]] = None
    ) -> Dict[str, Any]:
        """
        Main pre-search method
        """
        # 1. Perform web search
        web_results = self._perform_web_search(query)
        
        # 2. Perform memory search (if enabled)
        memory_results = None
        if self.memory_enabled and self.memory_manager:
            memory_results = self._perform_memory_search(query)
        
        # 3. Combine all context sources
        combined_context = self._combine_context_sources(
            query, memory_results, web_results, conversation_history
        )
        
        # 4. Return structured results
        return {
            'query': query,
            'web_results': web_results,
            'memory_results': memory_results,
            'combined_context': combined_context,
            'search_metadata': {
                'web_search_performed': web_results is not None,
                'memory_search_performed': memory_results is not None,
                'total_context_length': len(combined_context)
            }
        }
```

### Web Search Implementation
```python
def _perform_web_search(self, query: str) -> Optional[str]:
    """
    Pseudocode for web search functionality
    """
    try:
        # 1. Initialize DuckDuckGo search
        with DDGS() as ddgs:
            # 2. Perform search with enhanced query
            enhanced_query = self._enhance_search_query(query)
            search_results = ddgs.text(enhanced_query, max_results=5)
            
            # 3. Parse and format results
            formatted_results = []
            for result in search_results:
                formatted_results.append({
                    'title': result.get('title', ''),
                    'body': result.get('body', ''),
                    'url': result.get('href', ''),
                    'relevance_score': self._calculate_relevance_score(result, query)
                })
            
            # 4. Sort by relevance and format
            sorted_results = sorted(formatted_results, key=lambda x: x['relevance_score'], reverse=True)
            return self._format_web_results(sorted_results)
            
    except Exception as e:
        logging.error(f"Web search failed: {e}")
        return None

def _enhance_search_query(self, query: str) -> str:
    """
    Pseudocode for query enhancement
    """
    # 1. Add context-specific terms
    enhanced_terms = []
    
    # 2. Add domain-specific keywords
    if 'digital twin' in query.lower():
        enhanced_terms.extend(['technology', 'implementation', 'benefits'])
    
    if 'education' in query.lower():
        enhanced_terms.extend(['schools', 'learning', 'students', 'teachers'])
    
    # 3. Add time-based terms
    enhanced_terms.extend(['2024', 'latest', 'current', 'recent'])
    
    # 4. Combine original query with enhancements
    enhanced_query = f"{query} {' '.join(enhanced_terms)}"
    
    return enhanced_query
```

### Memory Search Implementation
```python
def _perform_memory_search(self, query: str) -> Optional[str]:
    """
    Pseudocode for memory search functionality
    """
    try:
        # 1. Search memory database
        memory_results = self.memory_manager.search_similar_conversations(
            query, 
            limit=self.max_memory_results
        )
        
        if not memory_results:
            return None
        
        # 2. Format memory results
        formatted_memory = []
        for result in memory_results:
            formatted_memory.append({
                'query': result.get('query', ''),
                'response': result.get('response', ''),
                'timestamp': result.get('timestamp', ''),
                'similarity_score': result.get('similarity_score', 0.0)
            })
        
        # 3. Sort by similarity and format
        sorted_memory = sorted(formatted_memory, key=lambda x: x['similarity_score'], reverse=True)
        return self._format_memory_results(sorted_memory)
        
    except Exception as e:
        logging.error(f"Memory search failed: {e}")
        return None
```

### Context Combination Logic
```python
def _combine_context_sources(
    self, 
    query: str, 
    memory_results: Optional[str], 
    web_results: Optional[str], 
    conversation_history: Optional[List[Any]] = None
) -> str:
    """
    Pseudocode for combining context sources
    """
    context_parts = []
    
    # 1. Add conversation history context
    if conversation_history:
        recent_context = self._extract_recent_context(conversation_history)
        if recent_context:
            context_parts.append(f"Recent conversation context:\n{recent_context}")
    
    # 2. Add memory search results
    if memory_results:
        context_parts.append(f"Relevant past conversations:\n{memory_results}")
    
    # 3. Add web search results
    if web_results:
        context_parts.append(f"Current web information:\n{web_results}")
    
    # 4. Combine all context parts
    combined_context = "\n\n".join(context_parts)
    
    # 5. Add query context
    final_context = f"Query: {query}\n\nContext Information:\n{combined_context}"
    
    return final_context

def _extract_recent_context(self, conversation_history: List[Any]) -> str:
    """
    Pseudocode for extracting recent conversation context
    """
    # 1. Get last 3 conversations
    recent_conversations = conversation_history[-3:] if len(conversation_history) >= 3 else conversation_history
    
    # 2. Format recent context
    formatted_context = []
    for i, conv in enumerate(recent_conversations, 1):
        if isinstance(conv, dict):
            query = conv.get('query', '')
            response = conv.get('response', '')
            formatted_context.append(f"Conversation {i}: Q: {query} A: {response[:200]}...")
        else:
            formatted_context.append(f"Conversation {i}: {str(conv)[:200]}...")
    
    return "\n".join(formatted_context)
```

### Relevance Scoring
```python
def _calculate_relevance_score(self, result: Dict[str, Any], query: str) -> float:
    """
    Pseudocode for calculating relevance scores
    """
    score = 0.0
    
    # 1. Title relevance
    title = result.get('title', '').lower()
    query_terms = query.lower().split()
    title_matches = sum(1 for term in query_terms if term in title)
    score += title_matches * 0.3
    
    # 2. Body relevance
    body = result.get('body', '').lower()
    body_matches = sum(1 for term in query_terms if term in body)
    score += body_matches * 0.2
    
    # 3. Domain authority
    url = result.get('href', '')
    domain_score = self._get_domain_authority_score(url)
    score += domain_score * 0.2
    
    # 4. Recency (if available)
    if 'date' in result:
        recency_score = self._calculate_recency_score(result['date'])
        score += recency_score * 0.1
    
    return min(score, 1.0)  # Cap at 1.0

def _get_domain_authority_score(self, url: str) -> float:
    """
    Pseudocode for domain authority scoring
    """
    high_authority_domains = [
        'gov.uk', 'ac.uk', 'edu', 'nature.com', 'ieee.org', 
        'acm.org', 'springer.com', 'wiley.com'
    ]
    
    medium_authority_domains = [
        'medium.com', 'linkedin.com', 'forbes.com', 'techcrunch.com'
    ]
    
    url_lower = url.lower()
    
    for domain in high_authority_domains:
        if domain in url_lower:
            return 0.8
    
    for domain in medium_authority_domains:
        if domain in url_lower:
            return 0.5
    
    return 0.3  # Default score
```

## Usage Examples

### Basic PreSearch
```python
from presearch import PreSearchManager

# Initialize pre-search manager
presearch_manager = PreSearchManager(memory_enabled=True)

# Perform pre-search
results = presearch_manager.search_and_combine_context(
    query="digital twins in education",
    conversation_history=conversation_history
)

# Access results
web_results = results['web_results']
memory_results = results['memory_results']
combined_context = results['combined_context']
```

### Convenience Function
```python
from presearch import perform_presearch

# Quick pre-search
results = perform_presearch(
    query="AI in schools",
    conversation_history=conversation_history
)
```

### Memory-Only Search
```python
# Search only memory database
memory_results = presearch_manager.get_memory_results_only("previous query")
```

### Web-Only Search
```python
# Search only web
web_results = presearch_manager.get_search_results_only("current query")
```

## Configuration Options

### PreSearch Settings
```python
PRESEARCH_CONFIG = {
    'memory_enabled': True,
    'max_memory_results': 3,
    'max_web_results': 5,
    'min_relevance_score': 0.3,
    'context_max_length': 10000,
    'enable_query_enhancement': True
}
```

### Search Enhancement Rules
```python
QUERY_ENHANCEMENT_RULES = {
    'digital twin': ['technology', 'implementation', 'benefits', 'use cases'],
    'education': ['schools', 'learning', 'students', 'teachers', 'curriculum'],
    'AI': ['artificial intelligence', 'machine learning', 'automation'],
    'data': ['analytics', 'management', 'governance', 'quality']
}
```

## Error Handling

### Search Error Recovery
```python
def safe_search_execution(self, search_func, fallback_value=None):
    """
    Pseudocode for safe search execution
    """
    try:
        return search_func()
    except Exception as e:
        logging.warning(f"Search failed: {e}")
        return fallback_value

def handle_search_errors(self, error: Exception) -> str:
    """
    Pseudocode for handling search errors
    """
    if "rate limit" in str(error).lower():
        return "Search rate limit exceeded. Using cached results."
    elif "network" in str(error).lower():
        return "Network error. Falling back to memory search only."
    elif "timeout" in str(error).lower():
        return "Search timeout. Using available results."
    else:
        return f"Search error: {error}"
```

## Performance Optimization

### Caching
```python
from functools import lru_cache

@lru_cache(maxsize=100)
def cached_web_search(query: str) -> Optional[str]:
    """
    Cached web search to avoid duplicate requests
    """
    return perform_web_search(query)

@lru_cache(maxsize=50)
def cached_memory_search(query: str) -> Optional[str]:
    """
    Cached memory search
    """
    return perform_memory_search(query)
```

### Result Filtering
```python
def filter_results_by_relevance(results: List[Dict], min_score: float = 0.3) -> List[Dict]:
    """
    Pseudocode for filtering results by relevance
    """
    return [result for result in results if result.get('relevance_score', 0) >= min_score]

def limit_context_length(context: str, max_length: int = 10000) -> str:
    """
    Pseudocode for limiting context length
    """
    if len(context) <= max_length:
        return context
    
    # Truncate and add ellipsis
    return context[:max_length-3] + "..."
```

## Testing

### PreSearch Tests
```python
def test_presearch_manager():
    """Test pre-search manager functionality"""
    manager = PreSearchManager(memory_enabled=True)
    
    results = manager.search_and_combine_context("test query")
    
    assert 'query' in results
    assert 'web_results' in results
    assert 'memory_results' in results
    assert 'combined_context' in results

def test_convenience_function():
    """Test convenience function"""
    results = perform_presearch("test query")
    assert isinstance(results, dict)
    assert 'combined_context' in results
```
