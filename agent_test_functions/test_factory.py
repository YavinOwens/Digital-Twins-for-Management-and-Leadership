"""
Test Factory for CrewAI Multi-Agent Workflow

This module provides factory functions to create and run comprehensive
test suites for the CrewAI workflow components.
"""

from typing import List, Dict, Any, Optional, Tuple
from .function_calling_test import (
    test_function_calling_support, 
    test_tool_calling_capability,
    test_agent_function_calling,
    benchmark_function_calling_performance
)
from .llm_test import (
    test_llm_connectivity,
    test_llm_response_quality,
    test_llm_consistency,
    test_llm_performance,
    validate_llm_configuration
)
from .workflow_test import (
    test_workflow_execution,
    test_agent_communication,
    test_task_execution_order,
    test_tool_integration,
    test_conversation_context,
    benchmark_workflow_performance
)


def create_test_suite() -> Dict[str, List[callable]]:
    """
    Create a comprehensive test suite organized by category
    
    Returns:
        Dict[str, List[callable]]: Organized test functions by category
    """
    return {
        'llm_tests': [
            test_llm_connectivity,
            test_llm_response_quality,
            test_llm_consistency,
            test_llm_performance,
            validate_llm_configuration
        ],
        'function_calling_tests': [
            test_function_calling_support,
            test_tool_calling_capability,
            test_agent_function_calling,
            benchmark_function_calling_performance
        ],
        'workflow_tests': [
            test_workflow_execution,
            test_agent_communication,
            test_task_execution_order,
            test_tool_integration,
            test_conversation_context,
            benchmark_workflow_performance
        ]
    }


def run_llm_tests(llm, model_name: str) -> Dict[str, Tuple[bool, str]]:
    """
    Run all LLM-related tests
    
    Args:
        llm: The language model to test
        model_name: Name of the model for reporting
        
    Returns:
        Dict[str, Tuple[bool, str]]: Test results by test name
    """
    results = {}
    
    # Basic connectivity
    results['connectivity'] = test_llm_connectivity(llm, model_name)
    
    # Response quality
    results['quality'] = test_llm_response_quality(llm, model_name)
    
    # Consistency
    results['consistency'] = test_llm_consistency(llm, model_name)
    
    # Performance
    results['performance'] = test_llm_performance(llm, model_name)
    
    # Configuration
    results['configuration'] = validate_llm_configuration(llm, model_name)
    
    return results


def run_function_calling_tests(llm, model_name: str, agents: List[Any] = None, test_tool=None) -> Dict[str, Tuple[bool, str]]:
    """
    Run all function calling tests
    
    Args:
        llm: The language model to test
        model_name: Name of the model for reporting
        agents: Optional list of agents to test
        test_tool: Optional tool to test with
        
    Returns:
        Dict[str, Tuple[bool, str]]: Test results by test name
    """
    results = {}
    
    # Basic function calling
    results['basic_calling'] = test_function_calling_support(llm, model_name)
    
    # Tool calling capability
    results['tool_calling'] = test_tool_calling_capability(llm, model_name, test_tool)
    
    # Performance benchmark
    results['performance'] = benchmark_function_calling_performance(llm, model_name)
    
    # Agent function calling (if agents provided)
    if agents:
        for i, agent in enumerate(agents):
            results[f'agent_{i}_calling'] = test_agent_function_calling(agent, f"Test query for {agent.role}")
    
    return results


def run_workflow_tests(crew, agents: List[Any], tasks: List[Any], query: str, conversation_history: List[Dict] = None) -> Dict[str, Tuple[bool, str]]:
    """
    Run all workflow-related tests
    
    Args:
        crew: The CrewAI crew to test
        agents: List of agents in the workflow
        tasks: List of tasks in the workflow
        query: Test query to use
        conversation_history: Optional conversation history
        
    Returns:
        Dict[str, Tuple[bool, str]]: Test results by test name
    """
    results = {}
    
    # Agent communication
    results['agent_communication'] = test_agent_communication(agents)
    
    # Task execution order
    results['task_order'] = test_task_execution_order(tasks)
    
    # Tool integration
    results['tool_integration'] = test_tool_integration(agents)
    
    # Conversation context
    results['conversation_context'] = test_conversation_context(conversation_history or [], query)
    
    # Workflow execution (if crew provided)
    if crew:
        results['workflow_execution'] = test_workflow_execution(crew, query)
    
    return results


def run_all_tests(llm, model_name: str, crew=None, agents: List[Any] = None, tasks: List[Any] = None, 
                 query: str = "Test query", conversation_history: List[Dict] = None) -> Dict[str, Dict[str, Tuple[bool, str]]]:
    """
    Run all available tests
    
    Args:
        llm: The language model to test
        model_name: Name of the model for reporting
        crew: Optional CrewAI crew to test
        agents: Optional list of agents to test
        tasks: Optional list of tasks to test
        query: Test query to use
        conversation_history: Optional conversation history
        
    Returns:
        Dict[str, Dict[str, Tuple[bool, str]]]: Complete test results organized by category
    """
    results = {}
    
    # Run LLM tests
    results['llm_tests'] = run_llm_tests(llm, model_name)
    
    # Run function calling tests
    results['function_calling_tests'] = run_function_calling_tests(llm, model_name, agents)
    
    # Run workflow tests (if components provided)
    if agents or tasks or crew:
        results['workflow_tests'] = run_workflow_tests(crew, agents or [], tasks or [], query, conversation_history)
    
    return results


def generate_test_report(results: Dict[str, Dict[str, Tuple[bool, str]]]) -> str:
    """
    Generate a comprehensive test report
    
    Args:
        results: Test results from run_all_tests
        
    Returns:
        str: Formatted test report
    """
    report = ["🧪 CrewAI Workflow Test Report", "=" * 50, ""]
    
    total_tests = 0
    passed_tests = 0
    
    for category, tests in results.items():
        report.append(f"📋 {category.replace('_', ' ').title()}")
        report.append("-" * 30)
        
        category_passed = 0
        category_total = len(tests)
        
        for test_name, (success, message) in tests.items():
            status = "✅" if success else "❌"
            report.append(f"{status} {test_name}: {message}")
            if success:
                category_passed += 1
        
        report.append(f"Category Results: {category_passed}/{category_total} passed")
        report.append("")
        
        total_tests += category_total
        passed_tests += category_passed
    
    # Overall summary
    success_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
    report.append("📊 Overall Summary")
    report.append("-" * 20)
    report.append(f"Total Tests: {total_tests}")
    report.append(f"Passed: {passed_tests}")
    report.append(f"Failed: {total_tests - passed_tests}")
    report.append(f"Success Rate: {success_rate:.1f}%")
    
    if success_rate >= 80:
        report.append("🎉 Overall Status: EXCELLENT")
    elif success_rate >= 60:
        report.append("✅ Overall Status: GOOD")
    elif success_rate >= 40:
        report.append("⚠️ Overall Status: NEEDS IMPROVEMENT")
    else:
        report.append("❌ Overall Status: CRITICAL ISSUES")
    
    return "\n".join(report)


def quick_test(llm, model_name: str) -> Tuple[bool, str]:
    """
    Run a quick test to verify basic functionality
    
    Args:
        llm: The language model to test
        model_name: Name of the model for reporting
        
    Returns:
        Tuple[bool, str]: (success, message) indicating overall status
    """
    try:
        # Run basic connectivity test
        connectivity_success, connectivity_msg = test_llm_connectivity(llm, model_name)
        
        if not connectivity_success:
            return False, f"❌ Quick Test Failed: {connectivity_msg}"
        
        # Run function calling test
        fc_success, fc_msg = test_function_calling_support(llm, model_name)
        
        if not fc_success:
            return False, f"❌ Quick Test Failed: {fc_msg}"
        
        return True, f"✅ Quick Test Passed: {model_name} is ready for use"
        
    except Exception as e:
        return False, f"❌ Quick Test Failed: {str(e)}"
