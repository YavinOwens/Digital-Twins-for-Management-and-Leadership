"""
Robust LLM wrapper with retry logic for Ollama Cloud
"""

import time
import requests
from crewai import LLM
from typing import Optional, Dict, Any
import logging

class RobustLLM:
    """
    A wrapper around CrewAI's LLM that adds retry logic and better error handling
    for Ollama Cloud service issues.
    """
    
    def __init__(self, base_llm: LLM, max_retries: int = 3, retry_delay: float = 2.0):
        self.base_llm = base_llm
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.logger = logging.getLogger(__name__)
        
        # Copy all attributes from base_llm to make this a proper LLM replacement
        for attr in dir(base_llm):
            if not attr.startswith('_') and not callable(getattr(base_llm, attr)):
                setattr(self, attr, getattr(base_llm, attr))
    
    def call(self, messages, **kwargs):
        """
        Call the LLM with retry logic
        """
        last_exception = None
        
        for attempt in range(self.max_retries):
            try:
                self.logger.info(f"🔄 RobustLLM call attempt {attempt + 1}/{self.max_retries}")
                print(f"🔄 RobustLLM call attempt {attempt + 1}/{self.max_retries}")
                result = self.base_llm.call(messages, **kwargs)
                self.logger.info(f"✅ RobustLLM call successful on attempt {attempt + 1}")
                print(f"✅ RobustLLM call successful on attempt {attempt + 1}")
                return result
                
            except Exception as e:
                last_exception = e
                error_msg = str(e).lower()
                
                self.logger.error(f"❌ RobustLLM error on attempt {attempt + 1}: {e}")
                print(f"❌ RobustLLM error on attempt {attempt + 1}: {e}")
                
                # Check if it's a retryable error
                if any(keyword in error_msg for keyword in [
                    '502', 'bad gateway', 'upstream error', 'connection error', 
                    'timeout', 'network', 'service unavailable', 'unauthorized'
                ]):
                    if attempt < self.max_retries - 1:
                        delay = self.retry_delay * (2 ** attempt)  # Exponential backoff
                        self.logger.warning(f"🔄 Retryable error on attempt {attempt + 1}: {e}")
                        self.logger.info(f"⏳ Retrying in {delay} seconds...")
                        print(f"🔄 Retryable error on attempt {attempt + 1}: {e}")
                        print(f"⏳ Retrying in {delay} seconds...")
                        time.sleep(delay)
                        continue
                    else:
                        self.logger.error(f"❌ All {self.max_retries} attempts failed. Last error: {e}")
                        print(f"❌ All {self.max_retries} attempts failed. Last error: {e}")
                        break
                else:
                    # Non-retryable error, fail immediately
                    self.logger.error(f"❌ Non-retryable error: {e}")
                    print(f"❌ Non-retryable error: {e}")
                    break
        
        # If we get here, all retries failed
        raise last_exception
    
    def invoke(self, *args, **kwargs):
        """Delegate to call method"""
        return self.call(*args, **kwargs)
    
    def __getattr__(self, name):
        """Delegate all other attributes to the base LLM"""
        try:
            return getattr(self.base_llm, name)
        except AttributeError:
            # If the attribute doesn't exist, raise a proper error
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
    
    def __setattr__(self, name, value):
        """Handle attribute setting"""
        if name in ['base_llm', 'max_retries', 'retry_delay', 'logger']:
            super().__setattr__(name, value)
        else:
            # Delegate to base_llm for other attributes
            setattr(self.base_llm, name, value)

def create_robust_llm(use_cloud: bool = True, api_key: Optional[str] = None) -> RobustLLM:
    """
    Create a robust LLM instance with retry logic
    """
    import os
    
    if use_cloud and api_key:
        # Create base LLM for Ollama Cloud
        base_llm = LLM(
            model=f"ollama/{os.getenv('OLLAMA_CLOUD_MODEL', 'gpt-oss:20b')}",
            base_url=os.getenv('OLLAMA_CLOUD_BASE_URL', 'https://ollama.com'),
            headers={'Authorization': f'Bearer {api_key}'},
            temperature=float(os.getenv('DEFAULT_TEMPERATURE', '0.5')),
            max_tokens=int(os.getenv('DEFAULT_MAX_TOKENS', '8000')),
            system_message="You are an expert business consultant and writer. When asked to write reports, you must provide complete, detailed content - never summaries or placeholders. Write comprehensive, actionable content that executives can use immediately for decision-making. NEVER use ellipsis (...), continuation phrases, or placeholders like '[Insert content here]' or '[The actual content would continue here]'. Always write the complete, final content for every section. ONLY use references from the actual research data provided - NEVER make up citations, author names, or publication details."
        )
    else:
        # Create base LLM for local Ollama
        import ollama
        ollama.list()
        base_llm = LLM(
            model=f"ollama/{os.getenv('OLLAMA_LOCAL_MODEL', 'llama3.1:latest')}",
            base_url=os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434'),
            temperature=float(os.getenv('DEFAULT_TEMPERATURE', '0.5')),
            max_tokens=int(os.getenv('DEFAULT_MAX_TOKENS', '8000')),
            system_message="You are an expert business consultant and writer. When asked to write reports, you must provide complete, detailed content - never summaries or placeholders. Write comprehensive, actionable content that executives can use immediately for decision-making. NEVER use ellipsis (...), continuation phrases, or placeholders like '[Insert content here]' or '[The actual content would continue here]'. Always write the complete, final content for every section. ONLY use references from the actual research data provided - NEVER make up citations, author names, or publication details."
        )
    
    # Wrap with retry logic
    return RobustLLM(base_llm, max_retries=3, retry_delay=2.0)
