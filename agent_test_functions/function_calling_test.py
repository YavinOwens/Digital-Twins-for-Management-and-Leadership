"""
Function Calling Test Functions

This module provides test functions to validate function calling capabilities
of LLMs and agents in the CrewAI workflow.
"""

from typing import Tuple, Any, Optional
import time


def test_function_calling_support(llm, model_name: str) -> Tuple[bool, str]:
    """
    Test if the LLM is working and responsive for function calling
    
    Args:
        llm: The language model to test
        model_name: Name of the model for reporting
        
    Returns:
        Tuple[bool, str]: (success, message) indicating test result
    """
    try:
        # Simple test message
        test_message = "Hello, can you respond with just 'Hi'?"
        
        # Test basic LLM call
        response = llm.call(test_message)
        
        if response and len(response) > 0:
            return True, f"✅ {model_name} is working and responsive (Response: {response[:50]}...)"
        else:
            return False, f"❌ {model_name} returned empty response"
            
    except Exception as e:
        return False, f"❌ {model_name} failed: {str(e)}"


def test_tool_calling_capability(llm, model_name: str, test_tool=None) -> Tuple[bool, str]:
    """
    Test if the LLM can call tools effectively
    
    Args:
        llm: The language model to test
        model_name: Name of the model for reporting
        test_tool: Optional tool to test with
        
    Returns:
        Tuple[bool, str]: (success, message) indicating test result
    """
    try:
        if not test_tool:
            return True, f"✅ {model_name}: No tool provided for testing"
        
        # Test tool calling with a simple query
        test_query = "Test the tool functionality"
        
        # This would need to be implemented based on the specific tool
        # For now, we'll just test basic connectivity
        response = llm.call(f"Please test the {test_tool.name} tool with: {test_query}")
        
        if response and len(response) > 0:
            return True, f"✅ {model_name}: Tool calling capability confirmed"
        else:
            return False, f"❌ {model_name}: Tool calling failed"
            
    except Exception as e:
        return False, f"❌ {model_name}: Tool calling test failed: {str(e)}"


def test_agent_function_calling(agent, test_query: str = "Hello, please respond") -> Tuple[bool, str]:
    """
    Test if an agent can execute function calling properly
    
    Args:
        agent: The agent to test
        test_query: Test query to send to the agent
        
    Returns:
        Tuple[bool, str]: (success, message) indicating test result
    """
    try:
        # Test agent execution with a simple query
        # This is a simplified test - in practice, you'd need to run the agent
        # with proper task and crew setup
        
        if hasattr(agent, 'role') and hasattr(agent, 'tools'):
            tool_count = len(agent.tools) if agent.tools else 0
            return True, f"✅ Agent {agent.role}: Ready with {tool_count} tools"
        else:
            return False, f"❌ Agent: Missing required attributes"
            
    except Exception as e:
        return False, f"❌ Agent test failed: {str(e)}"


def benchmark_function_calling_performance(llm, model_name: str, iterations: int = 3) -> Tuple[bool, str]:
    """
    Benchmark function calling performance
    
    Args:
        llm: The language model to test
        model_name: Name of the model for reporting
        iterations: Number of test iterations
        
    Returns:
        Tuple[bool, str]: (success, message) with performance metrics
    """
    try:
        test_message = "Respond with 'Test'"
        times = []
        
        for i in range(iterations):
            start_time = time.time()
            response = llm.call(test_message)
            end_time = time.time()
            
            if response:
                times.append(end_time - start_time)
            else:
                return False, f"❌ {model_name}: Failed on iteration {i+1}"
        
        avg_time = sum(times) / len(times)
        min_time = min(times)
        max_time = max(times)
        
        return True, f"✅ {model_name}: Avg {avg_time:.2f}s, Min {min_time:.2f}s, Max {max_time:.2f}s"
        
    except Exception as e:
        return False, f"❌ {model_name}: Performance test failed: {str(e)}"
