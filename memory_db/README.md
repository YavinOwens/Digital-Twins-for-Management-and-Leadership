# Memory Database Module

This module handles the persistent memory storage and retrieval system for the CrewAI multi-agent workflow application. It uses ChromaDB for vector-based semantic search and conversation storage.

## Structure

```
memory_db/
├── [ChromaDB files]              # ChromaDB database files
│   ├── [collection data]         # Conversation collection data
│   ├── [embeddings]              # Vector embeddings
│   └── [metadata]                # Database metadata
└── README.md                     # This documentation
```

## Key Components

### ChromaDB Integration
- **Vector Database**: ChromaDB for semantic search
- **Embeddings**: ONNXMiniLM_L6_V2 model for local embeddings
- **Collections**: Organized conversation storage
- **Metadata**: Rich metadata for each conversation

### Memory Management
- **Conversation Storage**: Save and retrieve conversations
- **Semantic Search**: Find similar past conversations
- **Context Retrieval**: Get relevant context for new queries
- **Memory Statistics**: Track memory usage and performance

## Pseudocode Examples

### Memory Manager Class
```python
class MemoryManager:
    """
    Pseudocode for memory management
    """
    def __init__(self, db_path: str = "./memory_db"):
        self.db_path = db_path
        self.client = chromadb.PersistentClient(path=db_path)
        self.collection = self.client.get_or_create_collection(
            name="conversation_memory",
            embedding_function=embedding_functions.ONNXMiniLM_L6_V2()
        )
    
    def save_conversation(self, query: str, response: str, metadata: Dict[str, Any] = None) -> str:
        """
        Pseudocode for saving conversation
        """
        # 1. Generate unique ID
        conversation_id = str(uuid.uuid4())
        
        # 2. Prepare conversation data
        conversation_data = {
            'query': query,
            'response': response,
            'timestamp': datetime.now().isoformat(),
            'metadata': metadata or {}
        }
        
        # 3. Create document for embedding
        document = f"Query: {query}\nResponse: {response}"
        
        # 4. Save to ChromaDB
        self.collection.add(
            documents=[document],
            metadatas=[conversation_data],
            ids=[conversation_id]
        )
        
        return conversation_id
    
    def search_similar_conversations(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Pseudocode for semantic search
        """
        # 1. Search for similar conversations
        results = self.collection.query(
            query_texts=[query],
            n_results=limit
        )
        
        # 2. Format results
        similar_conversations = []
        for i, result in enumerate(results['metadatas'][0]):
            similar_conversations.append({
                'id': results['ids'][0][i],
                'query': result['query'],
                'response': result['response'],
                'timestamp': result['timestamp'],
                'similarity_score': results['distances'][0][i],
                'metadata': result.get('metadata', {})
            })
        
        return similar_conversations
```

### Memory Statistics
```python
def get_memory_stats(self) -> Dict[str, Any]:
    """
    Pseudocode for memory statistics
    """
    # 1. Get collection count
    total_conversations = self.collection.count()
    
    # 2. Get database size
    db_size = self._calculate_db_size()
    
    # 3. Get recent activity
    recent_conversations = self._get_recent_conversations(limit=5)
    
    # 4. Calculate statistics
    stats = {
        'total_conversations': total_conversations,
        'database_size_mb': db_size,
        'recent_conversations': recent_conversations,
        'last_updated': datetime.now().isoformat()
    }
    
    return stats

def _calculate_db_size(self) -> float:
    """
    Pseudocode for calculating database size
    """
    total_size = 0
    for file_path in Path(self.db_path).rglob('*'):
        if file_path.is_file():
            total_size += file_path.stat().st_size
    
    return round(total_size / (1024 * 1024), 2)  # Convert to MB
```

### Context Retrieval
```python
def get_context_for_query(self, query: str, max_context: int = 3) -> str:
    """
    Pseudocode for context retrieval
    """
    # 1. Search for similar conversations
    similar_conversations = self.search_similar_conversations(query, limit=max_context)
    
    if not similar_conversations:
        return ""
    
    # 2. Format context
    context_parts = []
    for conv in similar_conversations:
        context_part = f"Previous Query: {conv['query']}\nPrevious Response: {conv['response'][:500]}...\n"
        context_parts.append(context_part)
    
    # 3. Combine context
    combined_context = "\n".join(context_parts)
    
    return combined_context
```

### Memory Operations
```python
def clear_memory(self) -> bool:
    """
    Pseudocode for clearing memory
    """
    try:
        # 1. Delete collection
        self.client.delete_collection("conversation_memory")
        
        # 2. Recreate collection
        self.collection = self.client.create_collection(
            name="conversation_memory",
            embedding_function=embedding_functions.ONNXMiniLM_L6_V2()
        )
        
        return True
        
    except Exception as e:
        logging.error(f"Failed to clear memory: {e}")
        return False

def get_all_conversations(self) -> List[Dict[str, Any]]:
    """
    Pseudocode for getting all conversations
    """
    # 1. Get all documents
    results = self.collection.get()
    
    # 2. Format conversations
    conversations = []
    for i, metadata in enumerate(results['metadatas']):
        conversations.append({
            'id': results['ids'][i],
            'query': metadata['query'],
            'response': metadata['response'],
            'timestamp': metadata['timestamp'],
            'metadata': metadata.get('metadata', {})
        })
    
    return conversations
```

## Usage Examples

### Basic Memory Operations
```python
from local_memory import MemoryManager

# Initialize memory manager
memory_manager = MemoryManager()

# Save conversation
conversation_id = memory_manager.save_conversation(
    query="What are digital twins?",
    response="Digital twins are virtual representations...",
    metadata={"workflow_type": "single_team", "timestamp": "2024-01-01T12:00:00"}
)

# Search similar conversations
similar = memory_manager.search_similar_conversations("AI in education", limit=3)

# Get context for query
context = memory_manager.get_context_for_query("digital transformation", max_context=2)
```

### Memory Statistics
```python
# Get memory statistics
stats = memory_manager.get_memory_stats()
print(f"Total conversations: {stats['total_conversations']}")
print(f"Database size: {stats['database_size_mb']} MB")

# Get all conversations
all_conversations = memory_manager.get_all_conversations()
print(f"Found {len(all_conversations)} conversations")
```

### Memory Integration
```python
def integrate_memory_with_workflow(query: str, workflow_type: str) -> str:
    """
    Pseudocode for memory integration
    """
    # 1. Search for similar past conversations
    similar_conversations = memory_manager.search_similar_conversations(query, limit=3)
    
    # 2. Build context from similar conversations
    context_parts = []
    for conv in similar_conversations:
        context_parts.append(f"Previous: {conv['query']} -> {conv['response'][:200]}...")
    
    # 3. Combine with current query
    enhanced_query = f"{query}\n\nContext from similar past conversations:\n" + "\n".join(context_parts)
    
    # 4. Execute workflow with enhanced context
    result = execute_workflow(enhanced_query, workflow_type)
    
    # 5. Save new conversation
    memory_manager.save_conversation(
        query=query,
        response=result,
        metadata={"workflow_type": workflow_type, "timestamp": datetime.now().isoformat()}
    )
    
    return result
```

## Database Schema

### Collection Structure
```python
COLLECTION_SCHEMA = {
    'name': 'conversation_memory',
    'embedding_function': 'ONNXMiniLM_L6_V2',
    'metadata': {
        'description': 'Stores conversation history and context',
        'created': '2024-01-01T00:00:00Z',
        'version': '1.0'
    }
}
```

### Document Format
```python
DOCUMENT_FORMAT = {
    'id': 'uuid4_string',
    'document': 'Query: {query}\nResponse: {response}',
    'metadata': {
        'query': 'Original user query',
        'response': 'Agent response',
        'timestamp': 'ISO timestamp',
        'workflow_type': 'Workflow type used',
        'team_count': 'Number of teams',
        'execution_time': 'Execution time in seconds',
        'status': 'Success/failure status'
    }
}
```

## Performance Optimization

### Batch Operations
```python
def batch_save_conversations(self, conversations: List[Dict[str, Any]]) -> List[str]:
    """
    Pseudocode for batch saving
    """
    # 1. Prepare batch data
    documents = []
    metadatas = []
    ids = []
    
    for conv in conversations:
        documents.append(f"Query: {conv['query']}\nResponse: {conv['response']}")
        metadatas.append(conv['metadata'])
        ids.append(str(uuid.uuid4()))
    
    # 2. Batch add to collection
    self.collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )
    
    return ids
```

### Caching
```python
from functools import lru_cache

@lru_cache(maxsize=100)
def cached_search(self, query: str, limit: int) -> List[Dict[str, Any]]:
    """
    Cached search to avoid duplicate queries
    """
    return self.search_similar_conversations(query, limit)
```

## Error Handling

### Database Error Recovery
```python
def safe_memory_operation(self, operation_func, *args, **kwargs):
    """
    Pseudocode for safe memory operations
    """
    try:
        return operation_func(*args, **kwargs)
    except Exception as e:
        logging.error(f"Memory operation failed: {e}")
        return None

def handle_database_errors(self, error: Exception) -> str:
    """
    Pseudocode for database error handling
    """
    if "collection not found" in str(error).lower():
        return "Memory database not initialized. Please restart the application."
    elif "embedding" in str(error).lower():
        return "Embedding model error. Please check model availability."
    elif "disk space" in str(error).lower():
        return "Insufficient disk space for memory database."
    else:
        return f"Database error: {error}"
```

## Testing

### Memory Tests
```python
def test_memory_operations():
    """Test memory operations"""
    memory_manager = MemoryManager("test_memory_db")
    
    # Test saving conversation
    conv_id = memory_manager.save_conversation("Test query", "Test response")
    assert conv_id is not None
    
    # Test searching
    similar = memory_manager.search_similar_conversations("Test query", limit=1)
    assert len(similar) > 0
    
    # Test statistics
    stats = memory_manager.get_memory_stats()
    assert stats['total_conversations'] > 0
```
