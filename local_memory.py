"""
Local ChromaDB Memory Management

This module provides a local ChromaDB setup that works with Ollama
without requiring external API keys.
"""

import chromadb
from chromadb.config import Settings
import os
from typing import List, Dict, Any
import json


class LocalMemoryManager:
    """
    Local memory manager using ChromaDB with local embeddings
    """
    
    def __init__(self, persist_directory: str = "./memory_db"):
        """
        Initialize local ChromaDB client
        
        Args:
            persist_directory: Directory to store the ChromaDB database
        """
        self.persist_directory = persist_directory
        
        # Create directory if it doesn't exist
        os.makedirs(persist_directory, exist_ok=True)
        
        # Initialize ChromaDB client with local settings
        self.client = chromadb.PersistentClient(
            path=persist_directory,
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
        
        # Get or create the conversation collection
        self.collection = self.client.get_or_create_collection(
            name="conversation_memory",
            metadata={"description": "Stores conversation history and context"}
        )
    
    def add_conversation(self, query: str, response: str, metadata: Dict[str, Any] = None):
        """
        Add a conversation to memory
        
        Args:
            query: The user's query
            response: The AI's response
            metadata: Additional metadata to store
        """
        if metadata is None:
            metadata = {}
        
        # Create a unique ID for this conversation
        conversation_id = f"conv_{len(self.collection.get()['ids'])}"
        
        # Store the conversation
        self.collection.add(
            documents=[f"Query: {query}\nResponse: {response}"],
            metadatas=[{
                "query": query,
                "response": response,
                "timestamp": metadata.get("timestamp", ""),
                "type": "conversation"
            }],
            ids=[conversation_id]
        )
        
        return conversation_id
    
    def search_similar(self, query: str, n_results: int = 3) -> List[Dict[str, Any]]:
        """
        Search for similar past conversations
        
        Args:
            query: The search query
            n_results: Number of results to return
            
        Returns:
            List of similar conversations
        """
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        
        similar_conversations = []
        for i, doc in enumerate(results['documents'][0]):
            similar_conversations.append({
                "content": doc,
                "metadata": results['metadatas'][0][i],
                "distance": results['distances'][0][i] if 'distances' in results else None
            })
        
        return similar_conversations
    
    def get_all_conversations(self) -> List[Dict[str, Any]]:
        """
        Get all stored conversations
        
        Returns:
            List of all conversations
        """
        results = self.collection.get()
        
        conversations = []
        for i, doc in enumerate(results['documents']):
            conversations.append({
                "id": results['ids'][i],
                "content": doc,
                "metadata": results['metadatas'][i]
            })
        
        return conversations
    
    def clear_memory(self):
        """
        Clear all stored conversations
        """
        # Delete the collection
        self.client.delete_collection("conversation_memory")
        
        # Recreate the collection
        self.collection = self.client.get_or_create_collection(
            name="conversation_memory",
            metadata={"description": "Stores conversation history and context"}
        )
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the memory database
        
        Returns:
            Dictionary with memory statistics
        """
        count = self.collection.count()
        
        return {
            "total_conversations": count,
            "persist_directory": self.persist_directory,
            "collection_name": "conversation_memory"
        }


# Global memory manager instance
memory_manager = LocalMemoryManager()


def add_to_memory(query: str, response: str, metadata: Dict[str, Any] = None):
    """Add a conversation to memory"""
    return memory_manager.add_conversation(query, response, metadata)


def search_memory(query: str, n_results: int = 3) -> List[Dict[str, Any]]:
    """Search for similar past conversations"""
    return memory_manager.search_similar(query, n_results)


def get_memory_stats() -> Dict[str, Any]:
    """Get memory statistics"""
    return memory_manager.get_memory_stats()


def clear_memory():
    """Clear all memory"""
    memory_manager.clear_memory()
