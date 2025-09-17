"""
Pre-search Manager for CrewAI Multi-Agent Workflow

This module handles pre-searching data before agent teams process it.
It combines web search results with conversation memory for comprehensive context.
"""

import time
from typing import List, Any, Optional, Dict
from agent_tools import search_web
from local_memory import search_memory


class PreSearchManager:
    """
    Manages pre-search functionality for gathering context before agent processing.
    """
    
    def __init__(self, memory_enabled: bool = True, max_memory_results: int = 3):
        """
        Initialize the PreSearchManager.
        
        Args:
            memory_enabled: Whether to search conversation memory
            max_memory_results: Maximum number of memory results to retrieve
        """
        self.memory_enabled = memory_enabled
        self.max_memory_results = max_memory_results
    
    def search_and_combine_context(
        self, 
        query: str, 
        conversation_history: Optional[List[Any]] = None
    ) -> Dict[str, Any]:
        """
        Perform comprehensive pre-search and combine all context sources.
        
        Args:
            query: The user's query
            conversation_history: Previous conversation context
            
        Returns:
            Dict containing search results, memory results, and combined context
        """
        start_time = time.time()
        
        print(f"🔍 Pre-searching data for query: {query}")
        
        # Search conversation memory
        memory_results = None
        if self.memory_enabled:
            try:
                memory_results = search_memory(query, n_results=self.max_memory_results)
                if memory_results:
                    print(f"🧠 Found {len(memory_results)} similar past conversations")
                else:
                    print("🧠 No similar past conversations found")
            except Exception as e:
                print(f"⚠️ Memory search failed: {e}")
                memory_results = None
        
        # Search web for current information
        web_results = None
        try:
            web_results = search_web.run(query)
            if web_results:
                print(f"🔍 Found {len(web_results)} web search results")
            else:
                print("🔍 No web search results found")
        except Exception as e:
            print(f"⚠️ Web search failed: {e}")
            web_results = None
        
        # Combine all context sources
        combined_context = self._combine_context_sources(
            query, memory_results, web_results, conversation_history
        )
        
        # Log performance metrics
        elapsed_time = time.time() - start_time
        print(f"⏱️ Pre-search completed in {elapsed_time:.2f} seconds")
        
        return {
            'query': query,
            'memory_results': memory_results,
            'web_results': web_results,
            'combined_context': combined_context,
            'search_time': elapsed_time,
            'conversation_history': conversation_history
        }
    
    def _combine_context_sources(
        self, 
        query: str, 
        memory_results: Optional[str], 
        web_results: Optional[str], 
        conversation_history: Optional[List[Any]] = None
    ) -> str:
        """
        Combine all context sources into a single string.
        
        Args:
            query: The user's query
            memory_results: Results from conversation memory search
            web_results: Results from web search
            conversation_history: Previous conversation context
            
        Returns:
            Combined context string
        """
        combined_context = f"Query: {query}\n\n"
        
        # Add memory results if available
        if memory_results:
            combined_context += f"Similar past conversations:\n{memory_results}\n\n"
        
        # Add web search results if available
        if web_results:
            combined_context += f"Current search results:\n{web_results}\n\n"
        
        # Add conversation history if available
        if conversation_history:
            combined_context += f"Current conversation context:\n{len(conversation_history)} previous messages\n\n"
        
        return combined_context
    
    def get_search_results_only(self, query: str) -> Optional[str]:
        """
        Get only web search results without memory or context combination.
        
        Args:
            query: The user's query
            
        Returns:
            Web search results or None
        """
        try:
            return search_web.run(query)
        except Exception as e:
            print(f"⚠️ Web search failed: {e}")
            return None
    
    def get_memory_results_only(self, query: str) -> Optional[str]:
        """
        Get only memory search results without web search.
        
        Args:
            query: The user's query
            
        Returns:
            Memory search results or None
        """
        if not self.memory_enabled:
            return None
            
        try:
            return search_memory(query, n_results=self.max_memory_results)
        except Exception as e:
            print(f"⚠️ Memory search failed: {e}")
            return None


# Convenience function for backward compatibility
def perform_presearch(query: str, conversation_history: Optional[List[Any]] = None) -> Dict[str, Any]:
    """
    Convenience function to perform pre-search with default settings.
    
    Args:
        query: The user's query
        conversation_history: Previous conversation context
        
    Returns:
        Dict containing search results and combined context
    """
    manager = PreSearchManager()
    return manager.search_and_combine_context(query, conversation_history)
