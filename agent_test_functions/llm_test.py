"""
LLM Test Functions

This module provides test functions to validate LLM connectivity,
response quality, and performance in the CrewAI workflow.
"""

from typing import Tuple, Any, Optional, List
import time
import re


def test_llm_connectivity(llm, model_name: str) -> Tuple[bool, str]:
    """
    Test basic LLM connectivity and responsiveness
    
    Args:
        llm: The language model to test
        model_name: Name of the model for reporting
        
    Returns:
        Tuple[bool, str]: (success, message) indicating test result
    """
    try:
        # Simple connectivity test
        test_message = "Hello"
        response = llm.call(test_message)
        
        if response and len(response) > 0:
            return True, f"✅ {model_name}: Connected and responsive"
        else:
            return False, f"❌ {model_name}: No response received"
            
    except Exception as e:
        return False, f"❌ {model_name}: Connection failed: {str(e)}"


def test_llm_response_quality(llm, model_name: str) -> Tuple[bool, str]:
    """
    Test LLM response quality and coherence
    
    Args:
        llm: The language model to test
        model_name: Name of the model for reporting
        
    Returns:
        Tuple[bool, str]: (success, message) indicating test result
    """
    try:
        # Test with a more complex query
        test_message = "Explain artificial intelligence in one sentence."
        response = llm.call(test_message)
        
        if not response:
            return False, f"❌ {model_name}: No response"
        
        # Basic quality checks
        response_length = len(response)
        word_count = len(response.split())
        
        # Check for coherent response
        has_ai_keywords = any(keyword in response.lower() for keyword in 
                             ['artificial', 'intelligence', 'ai', 'machine', 'learning', 'computer'])
        
        if response_length < 10:
            return False, f"❌ {model_name}: Response too short ({response_length} chars)"
        
        if word_count < 5:
            return False, f"❌ {model_name}: Response too brief ({word_count} words)"
        
        if not has_ai_keywords:
            return False, f"❌ {model_name}: Response doesn't address the topic"
        
        return True, f"✅ {model_name}: Quality response ({word_count} words, {response_length} chars)"
        
    except Exception as e:
        return False, f"❌ {model_name}: Quality test failed: {str(e)}"


def test_llm_consistency(llm, model_name: str, iterations: int = 3) -> Tuple[bool, str]:
    """
    Test LLM response consistency across multiple calls
    
    Args:
        llm: The language model to test
        model_name: Name of the model for reporting
        iterations: Number of test iterations
        
    Returns:
        Tuple[bool, str]: (success, message) indicating test result
    """
    try:
        test_message = "What is 2+2?"
        responses = []
        
        for i in range(iterations):
            response = llm.call(test_message)
            if response:
                responses.append(response.strip().lower())
            else:
                return False, f"❌ {model_name}: Failed on iteration {i+1}"
        
        # Check for consistency (all responses should contain "4")
        consistent_responses = sum(1 for resp in responses if "4" in resp)
        consistency_rate = consistent_responses / len(responses)
        
        if consistency_rate >= 0.8:  # 80% consistency threshold
            return True, f"✅ {model_name}: {consistency_rate:.1%} consistency ({consistent_responses}/{len(responses)})"
        else:
            return False, f"❌ {model_name}: Low consistency {consistency_rate:.1%} ({consistent_responses}/{len(responses)})"
        
    except Exception as e:
        return False, f"❌ {model_name}: Consistency test failed: {str(e)}"


def test_llm_performance(llm, model_name: str, test_queries: List[str] = None) -> Tuple[bool, str]:
    """
    Test LLM performance with various query types
    
    Args:
        llm: The language model to test
        model_name: Name of the model for reporting
        test_queries: List of test queries to use
        
    Returns:
        Tuple[bool, str]: (success, message) with performance metrics
    """
    try:
        if not test_queries:
            test_queries = [
                "Hello",
                "What is machine learning?",
                "Explain quantum computing briefly",
                "List 3 benefits of AI"
            ]
        
        total_time = 0
        successful_responses = 0
        
        for i, query in enumerate(test_queries):
            start_time = time.time()
            response = llm.call(query)
            end_time = time.time()
            
            query_time = end_time - start_time
            total_time += query_time
            
            if response and len(response) > 0:
                successful_responses += 1
            
            # Add small delay between requests
            time.sleep(0.1)
        
        avg_time = total_time / len(test_queries)
        success_rate = successful_responses / len(test_queries)
        
        if success_rate >= 0.8:  # 80% success threshold
            return True, f"✅ {model_name}: {success_rate:.1%} success, avg {avg_time:.2f}s per query"
        else:
            return False, f"❌ {model_name}: Low success rate {success_rate:.1%}, avg {avg_time:.2f}s per query"
        
    except Exception as e:
        return False, f"❌ {model_name}: Performance test failed: {str(e)}"


def validate_llm_configuration(llm, model_name: str) -> Tuple[bool, str]:
    """
    Validate LLM configuration and settings
    
    Args:
        llm: The language model to test
        model_name: Name of the model for reporting
        
    Returns:
        Tuple[bool, str]: (success, message) indicating configuration status
    """
    try:
        # Check if LLM has required attributes
        required_attrs = ['model', 'temperature', 'max_tokens']
        missing_attrs = []
        
        for attr in required_attrs:
            if not hasattr(llm, attr):
                missing_attrs.append(attr)
        
        if missing_attrs:
            return False, f"❌ {model_name}: Missing attributes: {', '.join(missing_attrs)}"
        
        # Check configuration values
        config_issues = []
        
        if hasattr(llm, 'temperature') and (llm.temperature < 0 or llm.temperature > 2):
            config_issues.append(f"temperature={llm.temperature}")
        
        if hasattr(llm, 'max_tokens') and llm.max_tokens <= 0:
            config_issues.append(f"max_tokens={llm.max_tokens}")
        
        if config_issues:
            return False, f"❌ {model_name}: Configuration issues: {', '.join(config_issues)}"
        
        return True, f"✅ {model_name}: Configuration valid (temp={llm.temperature}, tokens={llm.max_tokens})"
        
    except Exception as e:
        return False, f"❌ {model_name}: Configuration validation failed: {str(e)}"
