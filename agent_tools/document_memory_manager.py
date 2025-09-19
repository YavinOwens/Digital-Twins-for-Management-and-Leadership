"""
Document Memory Manager

This module provides functionality to store uploaded documents in ChromaDB
for semantic search and retrieval by agents.
"""

import chromadb
from chromadb.config import Settings
import os
from typing import List, Dict, Any, Optional
import json
import hashlib
from pathlib import Path
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DocumentMemoryManager:
    """
    Manages document storage and retrieval in ChromaDB for semantic search
    """
    
    def __init__(self, persist_directory: str = "./memory_db"):
        """
        Initialize document memory manager
        
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
        
        # Get or create the document collection
        self.document_collection = self.client.get_or_create_collection(
            name="document_memory",
            metadata={"description": "Stores uploaded documents for semantic search"}
        )
    
    def chunk_document(self, content: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
        """
        Split document content into overlapping chunks for better semantic search
        
        Args:
            content: The document content to chunk
            chunk_size: Maximum size of each chunk
            overlap: Number of characters to overlap between chunks
            
        Returns:
            List of document chunks
        """
        if len(content) <= chunk_size:
            return [content]
        
        chunks = []
        start = 0
        
        while start < len(content):
            end = start + chunk_size
            
            # Try to break at sentence boundary
            if end < len(content):
                # Look for sentence endings within the last 100 characters
                sentence_end = content.rfind('.', start, end)
                if sentence_end > start + chunk_size - 100:
                    end = sentence_end + 1
            
            chunk = content[start:end].strip()
            if chunk:
                chunks.append(chunk)
            
            # Move start position with overlap
            start = end - overlap
            if start >= len(content):
                break
        
        return chunks
    
    def store_document(self, document_data: Dict[str, Any]) -> str:
        """
        Store a document in memory for semantic search
        
        Args:
            document_data: Dictionary containing document information
            
        Returns:
            Document ID for reference
        """
        try:
            # Extract document information
            filename = document_data.get('metadata', {}).get('filename', 'unknown')
            file_type = document_data.get('type', 'unknown')
            content = document_data.get('sample_text', '')
            
            # Generate unique document ID
            doc_id = f"doc_{hashlib.md5(filename.encode()).hexdigest()[:12]}"
            
            # Chunk the document content
            chunks = self.chunk_document(content)
            
            # Store each chunk
            chunk_ids = []
            for i, chunk in enumerate(chunks):
                chunk_id = f"{doc_id}_chunk_{i}"
                chunk_ids.append(chunk_id)
                
                self.document_collection.add(
                    documents=[chunk],
                    metadatas=[{
                        "document_id": doc_id,
                        "filename": filename,
                        "file_type": file_type,
                        "chunk_index": i,
                        "total_chunks": len(chunks),
                        "type": "document_chunk"
                    }],
                    ids=[chunk_id]
                )
            
            logger.info(f"Stored document '{filename}' with {len(chunks)} chunks")
            return doc_id
            
        except Exception as e:
            logger.error(f"Error storing document: {e}")
            raise
    
    def search_documents(self, query: str, n_results: int = 5, file_types: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """
        Search for relevant document chunks using semantic similarity
        
        Args:
            query: The search query
            n_results: Number of results to return
            file_types: Optional filter by file types
            
        Returns:
            List of relevant document chunks with metadata
        """
        try:
            # Build where clause for filtering
            where_clause = {"type": "document_chunk"}
            if file_types:
                where_clause["file_type"] = {"$in": file_types}
            
            results = self.document_collection.query(
                query_texts=[query],
                n_results=n_results,
                where=where_clause if where_clause else None
            )
            
            document_chunks = []
            for i, doc in enumerate(results['documents'][0]):
                document_chunks.append({
                    "content": doc,
                    "metadata": results['metadatas'][0][i],
                    "distance": results['distances'][0][i] if 'distances' in results else None
                })
            
            return document_chunks
            
        except Exception as e:
            logger.error(f"Error searching documents: {e}")
            return []
    
    def get_document_by_id(self, document_id: str) -> List[Dict[str, Any]]:
        """
        Retrieve all chunks of a specific document
        
        Args:
            document_id: The document ID to retrieve
            
        Returns:
            List of document chunks
        """
        try:
            results = self.document_collection.query(
                query_texts=[""],  # Empty query to get all
                where={"document_id": document_id},
                n_results=1000  # Large number to get all chunks
            )
            
            chunks = []
            for i, doc in enumerate(results['documents'][0]):
                chunks.append({
                    "content": doc,
                    "metadata": results['metadatas'][0][i]
                })
            
            # Sort by chunk index
            chunks.sort(key=lambda x: x['metadata'].get('chunk_index', 0))
            return chunks
            
        except Exception as e:
            logger.error(f"Error retrieving document {document_id}: {e}")
            return []
    
    def get_document_summary(self, document_id: str) -> Dict[str, Any]:
        """
        Get summary information about a document
        
        Args:
            document_id: The document ID
            
        Returns:
            Document summary information
        """
        try:
            chunks = self.get_document_by_id(document_id)
            if not chunks:
                return {"error": "Document not found"}
            
            # Get metadata from first chunk
            metadata = chunks[0]['metadata']
            
            # Combine all chunks for full content
            full_content = " ".join([chunk['content'] for chunk in chunks])
            
            return {
                "document_id": document_id,
                "filename": metadata.get('filename', 'unknown'),
                "file_type": metadata.get('file_type', 'unknown'),
                "total_chunks": len(chunks),
                "content_length": len(full_content),
                "first_chunk_preview": chunks[0]['content'][:200] + "..." if len(chunks[0]['content']) > 200 else chunks[0]['content']
            }
            
        except Exception as e:
            logger.error(f"Error getting document summary: {e}")
            return {"error": str(e)}
    
    def list_documents(self) -> List[Dict[str, Any]]:
        """
        List all stored documents
        
        Returns:
            List of document summaries
        """
        try:
            # Get all document chunks
            results = self.document_collection.get()
            
            # Group by document_id
            documents = {}
            for i, metadata in enumerate(results['metadatas']):
                doc_id = metadata.get('document_id')
                if doc_id and doc_id not in documents:
                    documents[doc_id] = {
                        "document_id": doc_id,
                        "filename": metadata.get('filename', 'unknown'),
                        "file_type": metadata.get('file_type', 'unknown'),
                        "total_chunks": metadata.get('total_chunks', 0)
                    }
            
            return list(documents.values())
            
        except Exception as e:
            logger.error(f"Error listing documents: {e}")
            return []
    
    def delete_document(self, document_id: str) -> bool:
        """
        Delete a document and all its chunks
        
        Args:
            document_id: The document ID to delete
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Get all chunks for this document
            chunks = self.get_document_by_id(document_id)
            chunk_ids = [chunk['metadata'].get('id') for chunk in chunks if chunk['metadata'].get('id')]
            
            if chunk_ids:
                self.document_collection.delete(ids=chunk_ids)
                logger.info(f"Deleted document {document_id} with {len(chunk_ids)} chunks")
                return True
            else:
                logger.warning(f"No chunks found for document {document_id}")
                return False
                
        except Exception as e:
            logger.error(f"Error deleting document {document_id}: {e}")
            return False
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the document memory
        
        Returns:
            Dictionary with memory statistics
        """
        try:
            count = self.document_collection.count()
            documents = self.list_documents()
            
            return {
                "total_chunks": count,
                "total_documents": len(documents),
                "persist_directory": self.persist_directory,
                "collection_name": "document_memory"
            }
            
        except Exception as e:
            logger.error(f"Error getting memory stats: {e}")
            return {"error": str(e)}


# Global document memory manager instance
document_memory_manager = DocumentMemoryManager()


def store_document_in_memory(document_data: Dict[str, Any]) -> str:
    """Store a document in memory for semantic search"""
    return document_memory_manager.store_document(document_data)


def search_documents_in_memory(query: str, n_results: int = 5, file_types: Optional[List[str]] = None) -> List[Dict[str, Any]]:
    """Search for relevant documents using semantic similarity"""
    return document_memory_manager.search_documents(query, n_results, file_types)


def get_document_from_memory(document_id: str) -> List[Dict[str, Any]]:
    """Retrieve a document from memory"""
    return document_memory_manager.get_document_by_id(document_id)


def list_documents_in_memory() -> List[Dict[str, Any]]:
    """List all documents in memory"""
    return document_memory_manager.list_documents()


def delete_document_from_memory(document_id: str) -> bool:
    """Delete a document from memory"""
    return document_memory_manager.delete_document(document_id)


def get_document_memory_stats() -> Dict[str, Any]:
    """Get document memory statistics"""
    return document_memory_manager.get_memory_stats()
