# Memory System Documentation

This directory contains detailed documentation for the memory system in the CrewAI Multi-Agent Workflow System.

## Overview

The memory system provides persistent conversation storage and context retrieval using ChromaDB with local embeddings. It enables the system to maintain context across sessions and provide relevant information from past conversations.

## System Architecture

```
memory_system/
├── README.md                    # This overview
├── chromadb_integration.md      # ChromaDB integration details
└── embedding_models.md          # Embedding model documentation
```

## Core Components

### 1. ChromaDB Integration
**Purpose**: Vector database for conversation storage
**Key Features**:
- Persistent storage across sessions
- Vector similarity search
- Metadata support
- Local storage (no external API keys)

### 2. Embedding Models
**Purpose**: Convert text to vector embeddings
**Model**: ONNXMiniLM_L6_V2 (all-MiniLM-L6-v2)
**Key Features**:
- Local model (no external API keys)
- 384-dimensional embeddings
- Fast inference
- High quality semantic representations

### 3. Memory Management
**Purpose**: Conversation memory and context retrieval
**Key Features**:
- Conversation storage
- Context retrieval
- Semantic search
- Metadata management

## ChromaDB Integration

### Database Structure

The memory system uses ChromaDB with the following structure:

```python
# Collection structure
collection = {
    "name": "conversations",
    "metadata": {
        "description": "Conversation memory storage",
        "embedding_model": "ONNXMiniLM_L6_V2",
        "embedding_dimension": 384
    },
    "documents": [
        {
            "id": "uuid4",
            "content": "conversation_text",
            "metadata": {
                "timestamp": "2024-01-01T00:00:00Z",
                "workflow_type": "seven_team",
                "query": "user_query",
                "response": "agent_response",
                "team_outputs": {...}
            }
        }
    ]
}
```

### Collection Management

```python
class MemoryManager:
    def __init__(self, db_path: str = "./memory_db"):
        self.client = chromadb.PersistentClient(path=db_path)
        self.collection = self.client.get_or_create_collection(
            name="conversations",
            embedding_function=embedding_function
        )
    
    def add_conversation(self, query: str, response: str, metadata: Dict[str, Any]):
        """
        Add conversation to memory
        """
        conversation_id = str(uuid.uuid4())
        conversation_text = f"{query}\n\n{response}"
        
        self.collection.add(
            documents=[conversation_text],
            metadatas=[metadata],
            ids=[conversation_id]
        )
    
    def search_memory(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """
        Search conversation memory using semantic similarity
        """
        results = self.collection.query(
            query_texts=[query],
            n_results=max_results,
            include=["documents", "metadatas", "distances"]
        )
        
        return self._format_search_results(results)
```

### Data Storage

Conversations are stored with rich metadata:

```python
metadata = {
    "timestamp": datetime.utcnow().isoformat(),
    "workflow_type": "seven_team",
    "query": user_query,
    "response": agent_response,
    "team_outputs": {
        "team1": team1_output,
        "team2": team2_output,
        # ... other teams
    },
    "execution_time": execution_time,
    "model_used": model_name,
    "api_key_used": api_key_hash
}
```

## Embedding Models

### ONNXMiniLM_L6_V2

The system uses the ONNXMiniLM_L6_V2 model for embeddings:

```python
from chromadb.utils import embedding_functions

# Create embedding function
embedding_function = embedding_functions.ONNXMiniLM_L6_V2()

# Model specifications
model_specs = {
    "name": "ONNXMiniLM_L6_V2",
    "dimension": 384,
    "model_type": "sentence-transformers",
    "base_model": "all-MiniLM-L6-v2",
    "max_sequence_length": 256,
    "vocab_size": 30522
}
```

#### Key Features

- **Local Model**: No external API keys required
- **Fast Inference**: Optimized for speed
- **High Quality**: Good semantic representations
- **Small Size**: ~80MB model size
- **ONNX Runtime**: Optimized inference engine

#### Performance Characteristics

- **Embedding Dimension**: 384
- **Max Sequence Length**: 256 tokens
- **Inference Speed**: ~1000 embeddings/second
- **Memory Usage**: ~200MB RAM
- **Model Size**: ~80MB disk space

### Embedding Process

```python
def create_embeddings(text: str) -> List[float]:
    """
    Create embeddings for text using ONNXMiniLM_L6_V2
    """
    # Preprocess text
    processed_text = preprocess_text(text)
    
    # Create embeddings
    embeddings = embedding_function([processed_text])
    
    return embeddings[0]
```

## Memory Management

### Conversation Storage

```python
def store_conversation(
    query: str,
    response: str,
    workflow_type: str,
    team_outputs: Dict[str, Any],
    metadata: Dict[str, Any]
):
    """
    Store conversation in memory
    """
    # Create conversation text
    conversation_text = f"Query: {query}\n\nResponse: {response}"
    
    # Create metadata
    conversation_metadata = {
        "timestamp": datetime.utcnow().isoformat(),
        "workflow_type": workflow_type,
        "query": query,
        "response": response,
        "team_outputs": team_outputs,
        **metadata
    }
    
    # Store in ChromaDB
    memory_manager.add_conversation(
        query=query,
        response=response,
        metadata=conversation_metadata
    )
```

### Context Retrieval

```python
def retrieve_context(
    query: str,
    max_results: int = 5,
    similarity_threshold: float = 0.7
) -> List[Dict[str, Any]]:
    """
    Retrieve relevant context from memory
    """
    # Search memory
    search_results = memory_manager.search_memory(
        query=query,
        max_results=max_results
    )
    
    # Filter by similarity threshold
    filtered_results = [
        result for result in search_results
        if result["similarity"] >= similarity_threshold
    ]
    
    return filtered_results
```

### Semantic Search

```python
def semantic_search(
    query: str,
    max_results: int = 5,
    include_metadata: bool = True
) -> List[Dict[str, Any]]:
    """
    Perform semantic search on conversation memory
    """
    results = memory_manager.collection.query(
        query_texts=[query],
        n_results=max_results,
        include=["documents", "metadatas", "distances"] if include_metadata else ["documents"]
    )
    
    return self._format_search_results(results)
```

## Configuration

### Environment Variables

```python
# Memory Configuration
MEMORY_DB_PATH="./memory_db"
MAX_MEMORY_RESULTS=5
MEMORY_SIMILARITY_THRESHOLD=0.7
EMBEDDING_MODEL="ONNXMiniLM_L6_V2"
EMBEDDING_DIMENSION=384

# ChromaDB Configuration
CHROMADB_PERSIST_DIRECTORY="./memory_db"
CHROMADB_COLLECTION_NAME="conversations"
CHROMADB_DISTANCE_FUNCTION="cosine"

# Performance Configuration
MEMORY_CACHE_SIZE=1000
MEMORY_CACHE_TTL=3600
MEMORY_BATCH_SIZE=100
```

### Database Configuration

```python
# ChromaDB client configuration
client = chromadb.PersistentClient(
    path="./memory_db",
    settings=Settings(
        anonymized_telemetry=False,
        allow_reset=True
    )
)

# Collection configuration
collection = client.get_or_create_collection(
    name="conversations",
    embedding_function=embedding_function,
    metadata={"description": "Conversation memory storage"}
)
```

## Performance Optimization

### Caching

```python
class CachedMemoryManager:
    def __init__(self, cache_size: int = 1000, cache_ttl: int = 3600):
        self.cache = {}
        self.cache_size = cache_size
        self.cache_ttl = cache_ttl
    
    def get_cached_result(self, query: str) -> Optional[List[Dict[str, Any]]]:
        """
        Get cached search result
        """
        if query in self.cache:
            result, timestamp = self.cache[query]
            if time.time() - timestamp < self.cache_ttl:
                return result
            else:
                del self.cache[query]
        return None
    
    def cache_result(self, query: str, result: List[Dict[str, Any]]):
        """
        Cache search result
        """
        if len(self.cache) >= self.cache_size:
            # Remove oldest entry
            oldest_key = min(self.cache.keys(), key=lambda k: self.cache[k][1])
            del self.cache[oldest_key]
        
        self.cache[query] = (result, time.time())
```

### Batch Processing

```python
def batch_store_conversations(conversations: List[Dict[str, Any]]):
    """
    Store multiple conversations in batch
    """
    documents = []
    metadatas = []
    ids = []
    
    for conversation in conversations:
        documents.append(conversation["text"])
        metadatas.append(conversation["metadata"])
        ids.append(conversation["id"])
    
    # Batch add to ChromaDB
    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )
```

## Error Handling

### Database Errors

```python
try:
    result = collection.query(query_texts=[query])
    return result
except Exception as e:
    logger.error(f"ChromaDB query error: {e}")
    # Fallback to empty result
    return {"documents": [[]], "metadatas": [[]], "distances": [[]]}
```

### Embedding Errors

```python
try:
    embeddings = embedding_function([text])
    return embeddings[0]
except Exception as e:
    logger.error(f"Embedding error: {e}")
    # Fallback to zero vector
    return [0.0] * 384
```

## Monitoring

### Performance Metrics

```python
class MemoryMetrics:
    def __init__(self):
        self.query_count = 0
        self.query_time = 0
        self.cache_hits = 0
        self.cache_misses = 0
    
    def record_query(self, query_time: float, cache_hit: bool):
        """
        Record query metrics
        """
        self.query_count += 1
        self.query_time += query_time
        if cache_hit:
            self.cache_hits += 1
        else:
            self.cache_misses += 1
    
    def get_metrics(self) -> Dict[str, Any]:
        """
        Get performance metrics
        """
        return {
            "query_count": self.query_count,
            "average_query_time": self.query_time / max(self.query_count, 1),
            "cache_hit_rate": self.cache_hits / max(self.query_count, 1),
            "cache_miss_rate": self.cache_misses / max(self.query_count, 1)
        }
```

### Health Checks

```python
def check_memory_health() -> Dict[str, Any]:
    """
    Check memory system health
    """
    try:
        # Test database connection
        collection.count()
        
        # Test embedding function
        test_embedding = embedding_function(["test"])
        
        return {
            "status": "healthy",
            "database_connected": True,
            "embedding_function_working": True,
            "collection_count": collection.count()
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "database_connected": False,
            "embedding_function_working": False
        }
```

## Troubleshooting

### Common Issues

1. **Database Connection Errors**
   - Check ChromaDB installation
   - Verify database path permissions
   - Check disk space

2. **Embedding Errors**
   - Verify ONNXMiniLM_L6_V2 model
   - Check model file integrity
   - Verify ONNX Runtime installation

3. **Performance Issues**
   - Check cache configuration
   - Monitor memory usage
   - Optimize batch sizes

4. **Search Quality Issues**
   - Adjust similarity threshold
   - Check embedding quality
   - Verify text preprocessing

### Debugging

```python
def debug_memory_system():
    """
    Debug memory system issues
    """
    # Check database
    print(f"Database path: {MEMORY_DB_PATH}")
    print(f"Collection count: {collection.count()}")
    
    # Check embedding function
    test_text = "This is a test query"
    test_embedding = embedding_function([test_text])
    print(f"Embedding dimension: {len(test_embedding[0])}")
    
    # Test search
    search_results = collection.query(query_texts=[test_text])
    print(f"Search results: {len(search_results['documents'][0])}")
```

## Best Practices

1. **Data Management**: Regular cleanup of old conversations
2. **Performance**: Use caching and batch processing
3. **Error Handling**: Comprehensive error handling and fallbacks
4. **Monitoring**: Regular health checks and performance monitoring
5. **Security**: Secure storage of sensitive information
6. **Backup**: Regular backup of conversation data
7. **Testing**: Thorough testing of memory operations

## Security Considerations

### Data Privacy

- **Local Storage**: All data stored locally
- **No External API**: No external API calls for embeddings
- **Encryption**: Consider encryption for sensitive data
- **Access Control**: Implement proper access controls

### Data Retention

```python
def cleanup_old_conversations(days_old: int = 30):
    """
    Clean up conversations older than specified days
    """
    cutoff_date = datetime.utcnow() - timedelta(days=days_old)
    
    # Get old conversations
    old_conversations = collection.get(
        where={"timestamp": {"$lt": cutoff_date.isoformat()}}
    )
    
    # Delete old conversations
    if old_conversations["ids"]:
        collection.delete(ids=old_conversations["ids"])
```

## Support

For issues with the memory system:
1. Check the ChromaDB documentation
2. Verify ONNXMiniLM_L6_V2 model installation
3. Check database permissions and disk space
4. Review error logs and debug information
5. Test with simplified scenarios
