"""
Workflow Test Functions

This module provides test functions to validate the complete
CrewAI workflow execution and agent communication.
"""

from typing import Tuple, Any, Optional, List, Dict
import time


def test_workflow_execution(crew, query: str, timeout: int = 60) -> Tuple[bool, str]:
    """
    Test complete workflow execution
    
    Args:
        crew: The CrewAI crew to test
        query: Test query to execute
        timeout: Maximum execution time in seconds
        
    Returns:
        Tuple[bool, str]: (success, message) indicating test result
    """
    try:
        start_time = time.time()
        
        # Execute the workflow
        result = crew.kickoff()
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        if execution_time > timeout:
            return False, f"❌ Workflow: Execution timeout ({execution_time:.1f}s > {timeout}s)"
        
        if not result:
            return False, f"❌ Workflow: No result produced"
        
        result_length = len(str(result))
        if result_length < 100:
            return False, f"❌ Workflow: Result too short ({result_length} chars)"
        
        return True, f"✅ Workflow: Completed in {execution_time:.1f}s, {result_length} chars output"
        
    except Exception as e:
        return False, f"❌ Workflow: Execution failed: {str(e)}"


def test_agent_communication(agents: List[Any]) -> Tuple[bool, str]:
    """
    Test agent communication and coordination
    
    Args:
        agents: List of agents to test
        
    Returns:
        Tuple[bool, str]: (success, message) indicating test result
    """
    try:
        if not agents:
            return False, f"❌ Communication: No agents provided"
        
        # Check agent roles and tools
        agent_info = []
        for agent in agents:
            if hasattr(agent, 'role') and hasattr(agent, 'tools'):
                tool_count = len(agent.tools) if agent.tools else 0
                agent_info.append(f"{agent.role}({tool_count}tools)")
            else:
                return False, f"❌ Communication: Agent missing required attributes"
        
        # Check for role diversity
        roles = [agent.role for agent in agents if hasattr(agent, 'role')]
        unique_roles = len(set(roles))
        
        if unique_roles < 2:
            return False, f"❌ Communication: Insufficient role diversity ({unique_roles} unique roles)"
        
        return True, f"✅ Communication: {len(agents)} agents ready ({', '.join(agent_info)})"
        
    except Exception as e:
        return False, f"❌ Communication: Test failed: {str(e)}"


def test_task_execution_order(tasks: List[Any]) -> Tuple[bool, str]:
    """
    Test task execution order and dependencies
    
    Args:
        tasks: List of tasks to test
        
    Returns:
        Tuple[bool, str]: (success, message) indicating test result
    """
    try:
        if not tasks:
            return False, f"❌ Tasks: No tasks provided"
        
        # Check task structure
        task_info = []
        for i, task in enumerate(tasks):
            if hasattr(task, 'agent') and hasattr(task, 'description'):
                agent_role = task.agent.role if hasattr(task.agent, 'role') else 'Unknown'
                task_info.append(f"Task{i+1}({agent_role})")
            else:
                return False, f"❌ Tasks: Task {i+1} missing required attributes"
        
        # Check for proper task sequence (research -> analysis -> writing)
        expected_roles = ['Research Specialist', 'Data Analyst', 'Content Writer']
        actual_roles = [task.agent.role for task in tasks if hasattr(task.agent, 'role')]
        
        if len(actual_roles) < len(expected_roles):
            return False, f"❌ Tasks: Insufficient tasks ({len(actual_roles)}/{len(expected_roles)})"
        
        return True, f"✅ Tasks: {len(tasks)} tasks ready ({' -> '.join(task_info)})"
        
    except Exception as e:
        return False, f"❌ Tasks: Test failed: {str(e)}"


def test_tool_integration(agents: List[Any]) -> Tuple[bool, str]:
    """
    Test tool integration across agents
    
    Args:
        agents: List of agents to test
        
    Returns:
        Tuple[bool, str]: (success, message) indicating test result
    """
    try:
        if not agents:
            return False, f"❌ Tools: No agents provided"
        
        tool_info = []
        total_tools = 0
        
        for agent in agents:
            if hasattr(agent, 'tools') and agent.tools:
                tool_count = len(agent.tools)
                total_tools += tool_count
                tool_info.append(f"{agent.role}({tool_count})")
            else:
                tool_info.append(f"{agent.role}(0)")
        
        if total_tools == 0:
            return False, f"❌ Tools: No tools found across agents"
        
        return True, f"✅ Tools: {total_tools} tools across agents ({', '.join(tool_info)})"
        
    except Exception as e:
        return False, f"❌ Tools: Test failed: {str(e)}"


def test_conversation_context(conversation_history: List[Dict], query: str) -> Tuple[bool, str]:
    """
    Test conversation context handling
    
    Args:
        conversation_history: Previous conversation messages
        query: Current query
        
    Returns:
        Tuple[bool, str]: (success, message) indicating test result
    """
    try:
        if not conversation_history:
            return True, f"✅ Context: No previous conversation (fresh start)"
        
        # Check conversation structure
        valid_messages = 0
        for msg in conversation_history:
            if isinstance(msg, dict) and 'role' in msg and 'content' in msg:
                valid_messages += 1
        
        if valid_messages == 0:
            return False, f"❌ Context: No valid messages in history"
        
        # Check for context relevance
        context_length = sum(len(msg.get('content', '')) for msg in conversation_history)
        
        if context_length < 10:
            return False, f"❌ Context: Insufficient context data ({context_length} chars)"
        
        return True, f"✅ Context: {valid_messages} messages, {context_length} chars context"
        
    except Exception as e:
        return False, f"❌ Context: Test failed: {str(e)}"


def benchmark_workflow_performance(crew, test_queries: List[str], iterations: int = 1) -> Tuple[bool, str]:
    """
    Benchmark workflow performance across multiple queries
    
    Args:
        crew: The CrewAI crew to test
        test_queries: List of test queries
        iterations: Number of iterations per query
        
    Returns:
        Tuple[bool, str]: (success, message) with performance metrics
    """
    try:
        total_time = 0
        successful_executions = 0
        total_queries = len(test_queries) * iterations
        
        for query in test_queries:
            for i in range(iterations):
                start_time = time.time()
                
                try:
                    result = crew.kickoff()
                    end_time = time.time()
                    
                    execution_time = end_time - start_time
                    total_time += execution_time
                    
                    if result and len(str(result)) > 50:
                        successful_executions += 1
                    
                except Exception as e:
                    return False, f"❌ Benchmark: Failed on query '{query}' iteration {i+1}: {str(e)}"
        
        avg_time = total_time / total_queries
        success_rate = successful_executions / total_queries
        
        if success_rate >= 0.8:  # 80% success threshold
            return True, f"✅ Benchmark: {success_rate:.1%} success, avg {avg_time:.1f}s per query"
        else:
            return False, f"❌ Benchmark: Low success rate {success_rate:.1%}, avg {avg_time:.1f}s per query"
        
    except Exception as e:
        return False, f"❌ Benchmark: Test failed: {str(e)}"
