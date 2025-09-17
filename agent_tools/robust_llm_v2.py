"""
Robust LLM class with retry logic for Ollama Cloud
"""

import time
import requests
from crewai import LLM
from typing import Optional, Dict, Any, Union, List
import logging
import os


class RobustLLM(LLM):
    """
    A robust LLM class that inherits from CrewAI's LLM and adds retry logic
    for Ollama Cloud service issues. This class ensures full CrewAI compatibility.
    """
    
    def __init__(self, use_cloud: bool = True, api_key: Optional[str] = None, max_retries: int = 3, retry_delay: float = 2.0, **kwargs):
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.logger = logging.getLogger(__name__)
        
        # Set up the base LLM configuration
        if use_cloud and api_key:
            # Create base LLM for Ollama Cloud
            super().__init__(
                model=f"ollama/{os.getenv('OLLAMA_CLOUD_MODEL', 'gpt-oss:20b')}",
                base_url=os.getenv('OLLAMA_CLOUD_BASE_URL', 'https://ollama.com'),
                headers={'Authorization': f'Bearer {api_key}'},
                temperature=float(os.getenv('DEFAULT_TEMPERATURE', '0.5')),
                max_tokens=int(os.getenv('DEFAULT_MAX_TOKENS', '8000')),
                system_message="You are an expert business consultant and writer. When asked to write reports, you must provide complete, detailed content - never summaries or placeholders. Write comprehensive, actionable content that executives can use immediately for decision-making. NEVER use ellipsis (...), continuation phrases, or placeholders like '[Insert content here]' or '[The actual content would continue here]'. Always write the complete, final content for every section. ONLY use references from the actual research data provided - NEVER make up citations, author names, or publication details.",
                **kwargs
            )
        else:
            # Create base LLM for local Ollama
            import ollama
            ollama.list()
            super().__init__(
                model=f"ollama/{os.getenv('OLLAMA_LOCAL_MODEL', 'llama3.1:latest')}",
                base_url=os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434'),
                temperature=float(os.getenv('DEFAULT_TEMPERATURE', '0.5')),
                max_tokens=int(os.getenv('DEFAULT_MAX_TOKENS', '8000')),
                system_message="You are an expert business consultant and writer. When asked to write reports, you must provide complete, detailed content - never summaries or placeholders. Write comprehensive, actionable content that executives can use immediately for decision-making. NEVER use ellipsis (...), continuation phrases, or placeholders like '[Insert content here]' or '[The actual content would continue here]'. Always write the complete, final content for every section. ONLY use references from the actual research data provided - NEVER make up citations, author names, or publication details.",
                **kwargs
            )
    
    def call(self, messages, tools=None, callbacks=None, available_functions=None, from_task=None, from_agent=None, **kwargs):
        """
        Call the LLM with retry logic and intelligent message handling
        """
        last_exception = None
        
        # Process messages to handle length and complexity issues
        processed_messages = self._process_messages(messages)
        
        for attempt in range(self.max_retries):
            try:
                self.logger.info(f"🔄 RobustLLM call attempt {attempt + 1}/{self.max_retries}")
                print(f"🔄 RobustLLM call attempt {attempt + 1}/{self.max_retries}")
                
                # Call the parent class's call method
                print(f"🔍 Calling super().call with messages: {processed_messages}")
                result = super().call(
                    messages=processed_messages,
                    tools=tools,
                    callbacks=callbacks,
                    available_functions=available_functions,
                    from_task=from_task,
                    from_agent=from_agent,
                    **kwargs
                )
                print(f"🔍 Raw result from super().call: {repr(result)}")
                
                self.logger.info(f"✅ RobustLLM call successful on attempt {attempt + 1}")
                print(f"✅ RobustLLM call successful on attempt {attempt + 1}")
                print(f"🔍 Response type: {type(result)}")
                print(f"🔍 Response content: {result}")
                
                # Check if result is None or empty
                if result is None or (isinstance(result, str) and result.strip() == ""):
                    self.logger.warning(f"⚠️ Empty response received on attempt {attempt + 1}")
                    print(f"⚠️ Empty response received on attempt {attempt + 1}")
                    if attempt < self.max_retries - 1:
                        delay = self.retry_delay * (2 ** attempt)
                        self.logger.info(f"🔄 Retrying due to empty response in {delay} seconds...")
                        print(f"🔄 Retrying due to empty response in {delay} seconds...")
                        time.sleep(delay)
                        continue
                    else:
                        self.logger.error(f"❌ All {self.max_retries} attempts failed with empty responses")
                        print(f"❌ All {self.max_retries} attempts failed with empty responses")
                        # Set last_exception to a proper exception for empty responses
                        last_exception = Exception("All retry attempts failed with empty responses")
                        break
                
                return result
                
            except BaseException as e:
                # Debug: Print exception type and details
                print(f"🔍 Exception type: {type(e)}")
                print(f"🔍 Exception value: {repr(e)}")
                
                last_exception = e
                
                # Safely convert exception to string
                try:
                    error_msg = str(e).lower()
                    error_str = str(e)
                except Exception as str_error:
                    error_msg = "unknown error"
                    error_str = f"Error converting exception to string: {str(str_error)}"
                
                # Ensure error_str is always a string
                if not isinstance(error_str, str):
                    error_str = repr(error_str)
                
                # Safe logging and printing
                try:
                    self.logger.error(f"❌ RobustLLM error on attempt {attempt + 1}: {error_str}")
                    print(f"❌ RobustLLM error on attempt {attempt + 1}: {error_str}")
                except Exception as log_error:
                    print(f"❌ RobustLLM error on attempt {attempt + 1}: [Error logging failed: {str(log_error)}]")
                
                # Check if it's a retryable error
                if any(keyword in error_msg for keyword in [
                    '502', 'bad gateway', 'upstream error', 'connection error', 
                    'timeout', 'network', 'service unavailable', 'unauthorized'
                ]):
                    if attempt < self.max_retries - 1:
                        delay = self.retry_delay * (2 ** attempt)  # Exponential backoff
                        try:
                            self.logger.warning(f"🔄 Retryable error on attempt {attempt + 1}: {error_str}")
                            self.logger.info(f"⏳ Retrying in {delay} seconds...")
                            print(f"🔄 Retryable error on attempt {attempt + 1}: {error_str}")
                            print(f"⏳ Retrying in {delay} seconds...")
                        except Exception as log_error:
                            print(f"🔄 Retryable error on attempt {attempt + 1}: [Error logging failed: {str(log_error)}]")
                            print(f"⏳ Retrying in {delay} seconds...")
                        time.sleep(delay)
                        continue
                    else:
                        try:
                            self.logger.error(f"❌ All {self.max_retries} attempts failed. Last error: {error_str}")
                            print(f"❌ All {self.max_retries} attempts failed. Last error: {error_str}")
                        except Exception as log_error:
                            print(f"❌ All {self.max_retries} attempts failed. Last error: [Error logging failed: {str(log_error)}]")
                        break
                else:
                    # Non-retryable error, fail immediately
                    try:
                        self.logger.error(f"❌ Non-retryable error: {error_str}")
                        print(f"❌ Non-retryable error: {error_str}")
                    except Exception as log_error:
                        print(f"❌ Non-retryable error: [Error logging failed: {str(log_error)}]")
                    break
            except Exception as e:
                # Catch any other unexpected errors
                print(f"🔍 Unexpected error type: {type(e)}")
                print(f"🔍 Unexpected error value: {repr(e)}")
                last_exception = Exception(f"Unexpected error: {str(e)}")
                break
        
        # If we get here, all retries failed
        if last_exception is not None:
            raise last_exception
        else:
            # If no exception was captured, raise a generic one
            raise Exception("All retry attempts failed with empty responses")
    
    def _process_messages(self, messages):
        """
        Process messages to handle length and complexity issues
        """
        if isinstance(messages, str):
            return messages
        
        if not isinstance(messages, list):
            return messages
        
        processed = []
        max_user_content_length = 4000  # Reasonable limit for user content
        
        for message in messages:
            if isinstance(message, dict) and 'content' in message:
                content = message['content']
                
                # If it's a user message and too long, truncate intelligently
                if (message.get('role') == 'user' and 
                    isinstance(content, str) and 
                    len(content) > max_user_content_length):
                    
                    print(f"🔧 Truncating long user message from {len(content)} to {max_user_content_length} characters")
                    
                    # Try to find a good truncation point
                    truncated = content[:max_user_content_length]
                    
                    # Look for the last complete sentence or paragraph
                    last_period = truncated.rfind('.')
                    last_newline = truncated.rfind('\n')
                    
                    if last_period > max_user_content_length * 0.8:
                        truncated = truncated[:last_period + 1]
                    elif last_newline > max_user_content_length * 0.8:
                        truncated = truncated[:last_newline]
                    
                    # Add truncation notice
                    truncated += "\n\n[Content truncated for length - focusing on key information]"
                    
                    processed.append({
                        'role': message['role'],
                        'content': truncated
                    })
                else:
                    processed.append(message)
            else:
                processed.append(message)
        
        return processed
    
    def supports_function_calling(self) -> bool:
        """
        Check if the LLM supports function calling.
        Delegates to parent class implementation.
        """
        try:
            return super().supports_function_calling()
        except Exception as e:
            self.logger.warning(f"Failed to check function calling support: {e}")
            return False
    
    def supports_stop_words(self) -> bool:
        """
        Check if the LLM supports stop words.
        Delegates to parent class implementation.
        """
        try:
            return super().supports_stop_words()
        except Exception as e:
            self.logger.warning(f"Failed to check stop words support: {e}")
            return True  # Default to True for compatibility
    
    def get_context_window_size(self) -> int:
        """
        Get the context window size for the LLM.
        Delegates to parent class implementation.
        """
        try:
            return super().get_context_window_size()
        except Exception as e:
            self.logger.warning(f"Failed to get context window size: {e}")
            return 8000  # Default fallback
    
    def set_callbacks(self, callbacks: List[Any]):
        """
        Set callbacks for the LLM.
        Delegates to parent class implementation.
        """
        try:
            super().set_callbacks(callbacks)
        except Exception as e:
            self.logger.warning(f"Failed to set callbacks: {e}")
    
    def set_env_callbacks(self):
        """
        Set environment callbacks for the LLM.
        Delegates to parent class implementation.
        """
        try:
            super().set_env_callbacks()
        except Exception as e:
            self.logger.warning(f"Failed to set environment callbacks: {e}")


def create_robust_llm(use_cloud: bool = True, api_key: Optional[str] = None) -> RobustLLM:
    """
    Create a robust LLM instance with retry logic
    """
    return RobustLLM(use_cloud=use_cloud, api_key=api_key)
