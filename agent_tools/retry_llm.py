"""
Retry LLM Wrapper

This module provides a retry wrapper for LLM calls to handle rate limiting and API failures.
"""

import time
import random
from typing import Any, Dict, List, Optional
from crewai import LLM


class RetryLLM(LLM):
    """
    LLM wrapper with exponential backoff retry logic for rate limiting
    """
    
    def __init__(self, *args, max_retries: int = 5, base_delay: float = 2.0, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_retries = max_retries
        self.base_delay = base_delay
    
    def call(self, messages: List[Dict[str, Any]], tools=None, callbacks=None, available_functions=None, from_task=None, from_agent=None, **kwargs) -> Optional[str]:
        """
        Make LLM call with exponential backoff retry logic
        Handles CrewAI-specific parameters properly
        """
        last_exception = None
        
        for attempt in range(self.max_retries):
            try:
                print(f"🔄 LLM call attempt {attempt + 1}/{self.max_retries}")
                result = super().call(
                    messages, 
                    tools=tools,
                    callbacks=callbacks,
                    available_functions=available_functions,
                    from_task=from_task,
                    from_agent=from_agent,
                    **kwargs
                )
                
                if result and result.strip():
                    print(f"✅ LLM call successful on attempt {attempt + 1}")
                    return result
                else:
                    print(f"⚠️ Empty response on attempt {attempt + 1}")
                    if attempt < self.max_retries - 1:
                        delay = self._calculate_delay(attempt)
                        print(f"⏳ Waiting {delay:.1f} seconds before retry...")
                        time.sleep(delay)
                    continue
                    
            except Exception as e:
                last_exception = e
                error_str = str(e).lower()
                print(f"❌ LLM call failed on attempt {attempt + 1}: {str(e)}")
                
                # Check if it's a retryable error
                if any(keyword in error_str for keyword in ['rate', 'limit', 'timeout', 'connection', '502', '503', '429']):
                    if attempt < self.max_retries - 1:
                        delay = self._calculate_delay(attempt)
                        print(f"⏳ Rate limiting detected, waiting {delay:.1f} seconds before retry...")
                        time.sleep(delay)
                        continue
                else:
                    # Non-retryable error, fail immediately
                    print(f"💥 Non-retryable error: {str(e)}")
                    raise e
        
        # All retries exhausted
        error_msg = f"All {self.max_retries} retry attempts failed"
        if last_exception:
            error_msg += f" - Last error: {str(last_exception)}"
        print(f"💥 {error_msg}")
        raise Exception(error_msg)
    
    def _calculate_delay(self, attempt: int) -> float:
        """
        Calculate exponential backoff delay with jitter
        """
        delay = self.base_delay * (2 ** attempt)
        # Add jitter (random variation) to prevent thundering herd
        jitter = random.uniform(0.1, 0.5)
        return delay + jitter


def create_retry_llm(use_cloud: bool = False, api_key: Optional[str] = None) -> RetryLLM:
    """
    Create RetryLLM instance with retry logic
    """
    import os
    
    if use_cloud and api_key:
        return RetryLLM(
            model="ollama/gpt-oss:20b",
            base_url="https://ollama.com",
            headers={'Authorization': f'Bearer {api_key}'},
            temperature=0.5,
            max_tokens=8000,
            max_retries=5,
            base_delay=2.0,
            system_message="You are an expert business consultant and writer. When asked to write reports, you must provide complete, detailed content - never summaries or placeholders. Write comprehensive, actionable content that executives can use immediately for decision-making. NEVER use ellipsis (...), continuation phrases, or placeholders like '[Insert content here]' or '[The actual content would continue here]'. Always write the complete, final content for every section. ONLY use references from the actual research data provided - NEVER make up citations, author names, or publication details."
        )
    else:
        return RetryLLM(
            model="ollama/llama3.1:latest",
            base_url="http://localhost:11434",
            temperature=0.5,
            max_tokens=8000,
            max_retries=3,  # Fewer retries for local
            base_delay=1.0,  # Shorter delay for local
            system_message="You are an expert business consultant and writer. When asked to write reports, you must provide complete, detailed content - never summaries or placeholders. Write comprehensive, actionable content that executives can use immediately for decision-making. NEVER use ellipsis (...), continuation phrases, or placeholders like '[Insert content here]' or '[The actual content would continue here]'. Always write the complete, final content for every section. ONLY use references from the actual research data provided - NEVER make up citations, author names, or publication details."
        )
