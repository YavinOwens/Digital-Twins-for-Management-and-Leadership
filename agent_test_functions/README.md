# Agent Test Functions Module

This module provides comprehensive testing utilities for validating and debugging the CrewAI multi-agent workflow system. It includes LLM connectivity tests, function calling validation, workflow execution tests, and performance benchmarking.

## Structure

```
agent_test_functions/
├── __init__.py                    # Module initialization and exports
├── function_calling_test.py       # Function calling capability tests
├── llm_test.py                    # LLM connectivity and performance tests
├── workflow_test.py               # Workflow execution and integration tests
└── test_factory.py                # Test suite factory and orchestration
```

## Key Components

### LLM Testing
- **Connectivity Tests**: Verify LLM connection and basic functionality
- **Response Quality**: Assess response quality and consistency
- **Performance Benchmarking**: Measure response times and throughput
- **Configuration Validation**: Ensure proper LLM setup

### Function Calling Tests
- **Capability Detection**: Test if model supports function calling
- **Tool Integration**: Validate tool usage with agents
- **Performance Metrics**: Measure function calling efficiency
- **Error Handling**: Test failure scenarios and recovery

### Workflow Testing
- **Execution Validation**: Test complete workflow runs
- **Agent Communication**: Verify inter-agent communication
- **Task Sequencing**: Validate task execution order
- **Integration Testing**: End-to-end workflow validation

## Pseudocode Examples

### LLM Connectivity Test
```python
def test_llm_connectivity(llm, model_name: str) -> Tuple[bool, str]:
    """
    Pseudocode for testing LLM connectivity
    """
    try:
        # 1. Prepare test message
        test_message = [{"role": "user", "content": "Hello, respond with 'OK'"}]
        
        # 2. Make LLM call with timeout
        start_time = time.time()
        response = llm.call(test_message)
        response_time = time.time() - start_time
        
        # 3. Validate response
        if response and "OK" in response.upper():
            return True, f"✅ LLM connected successfully in {response_time:.2f}s"
        else:
            return False, f"❌ Invalid response: {response}"
            
    except Exception as e:
        return False, f"❌ Connection failed: {str(e)}"
```

### Function Calling Test
```python
def test_function_calling_support(llm, model_name: str) -> Tuple[bool, str]:
    """
    Pseudocode for testing function calling capabilities
    """
    try:
        # 1. Define test function
        test_function = {
            "name": "test_function",
            "description": "A simple test function",
            "parameters": {
                "type": "object",
                "properties": {
                    "input": {"type": "string", "description": "Test input"}
                }
            }
        }
        
        # 2. Create test message with function
        test_message = [{
            "role": "user", 
            "content": "Call the test function with input 'hello'"
        }]
        
        # 3. Make call with function available
        response = llm.call(
            test_message, 
            tools=[test_function],
            available_functions={"test_function": test_function}
        )
        
        # 4. Check if function was called
        if "function_call" in str(response) or "test_function" in str(response):
            return True, "✅ Function calling supported"
        else:
            return False, "❌ Function calling not supported"
            
    except Exception as e:
        return False, f"❌ Function calling test failed: {str(e)}"
```

### Workflow Execution Test
```python
def test_workflow_execution(crew, query: str, timeout: int = 60) -> Tuple[bool, str]:
    """
    Pseudocode for testing workflow execution
    """
    try:
        # 1. Start workflow execution
        start_time = time.time()
        
        # 2. Execute crew with timeout
        result = crew.kickoff()
        
        execution_time = time.time() - start_time
        
        # 3. Validate result
        if result and len(str(result).strip()) > 10:
            return True, f"✅ Workflow completed in {execution_time:.2f}s"
        else:
            return False, f"❌ Workflow produced empty result"
            
    except TimeoutError:
        return False, f"❌ Workflow timed out after {timeout}s"
    except Exception as e:
        return False, f"❌ Workflow execution failed: {str(e)}"
```

### Agent Communication Test
```python
def test_agent_communication(agents: List[Any]) -> Tuple[bool, str]:
    """
    Pseudocode for testing agent communication
    """
    try:
        # 1. Create simple communication test
        test_tasks = []
        for i, agent in enumerate(agents):
            task = Task(
                description=f"Agent {i+1} task: Pass message to next agent",
                agent=agent,
                expected_output=f"Message from agent {i+1}"
            )
            test_tasks.append(task)
        
        # 2. Create test crew
        test_crew = Crew(
            agents=agents,
            tasks=test_tasks,
            process=Process.sequential
        )
        
        # 3. Execute communication test
        result = test_crew.kickoff()
        
        # 4. Validate communication
        if result and len(str(result)) > 0:
            return True, "✅ Agent communication working"
        else:
            return False, "❌ Agent communication failed"
            
    except Exception as e:
        return False, f"❌ Communication test failed: {str(e)}"
```

### Test Suite Factory
```python
def create_test_suite() -> Dict[str, List[callable]]:
    """
    Pseudocode for creating comprehensive test suite
    """
    return {
        "llm_tests": [
            test_llm_connectivity,
            test_llm_response_quality,
            test_llm_consistency,
            test_llm_performance
        ],
        "function_calling_tests": [
            test_function_calling_support,
            test_tool_calling_capability,
            test_agent_function_calling,
            benchmark_function_calling_performance
        ],
        "workflow_tests": [
            test_workflow_execution,
            test_agent_communication,
            test_task_execution_order,
            test_tool_integration
        ]
    }

def run_all_tests(llm, model_name: str, **kwargs) -> Dict[str, Dict[str, Tuple[bool, str]]]:
    """
    Pseudocode for running all tests
    """
    test_suite = create_test_suite()
    results = {}
    
    # 1. Run LLM tests
    results["llm_tests"] = {}
    for test_func in test_suite["llm_tests"]:
        test_name = test_func.__name__
        success, message = test_func(llm, model_name)
        results["llm_tests"][test_name] = (success, message)
    
    # 2. Run function calling tests
    results["function_calling_tests"] = {}
    for test_func in test_suite["function_calling_tests"]:
        test_name = test_func.__name__
        success, message = test_func(llm, model_name, **kwargs)
        results["function_calling_tests"][test_name] = (success, message)
    
    # 3. Run workflow tests
    if "crew" in kwargs:
        results["workflow_tests"] = {}
        for test_func in test_suite["workflow_tests"]:
            test_name = test_func.__name__
            success, message = test_func(**kwargs)
            results["workflow_tests"][test_name] = (success, message)
    
    return results
```

### Performance Benchmarking
```python
def benchmark_workflow_performance(crew, test_queries: List[str], iterations: int = 1) -> Tuple[bool, str]:
    """
    Pseudocode for workflow performance benchmarking
    """
    try:
        results = []
        
        # 1. Run multiple iterations
        for iteration in range(iterations):
            for query in test_queries:
                start_time = time.time()
                
                # 2. Execute workflow
                result = crew.kickoff()
                
                execution_time = time.time() - start_time
                results.append({
                    'query': query,
                    'time': execution_time,
                    'success': result is not None
                })
        
        # 3. Calculate statistics
        avg_time = sum(r['time'] for r in results) / len(results)
        success_rate = sum(r['success'] for r in results) / len(results)
        
        # 4. Generate report
        report = f"""
        Performance Benchmark Results:
        - Average execution time: {avg_time:.2f}s
        - Success rate: {success_rate:.1%}
        - Total tests: {len(results)}
        """
        
        return True, report
        
    except Exception as e:
        return False, f"❌ Benchmark failed: {str(e)}"
```

## Usage Examples

### Quick Test
```python
from agent_test_functions import quick_test

# Quick connectivity test
success, message = quick_test(llm, "ollama/llama3.1:latest")
print(message)
```

### Comprehensive Testing
```python
from agent_test_functions import run_all_tests

# Run all tests
results = run_all_tests(
    llm=llm,
    model_name="ollama/llama3.1:latest",
    crew=crew,
    agents=agents,
    tasks=tasks,
    query="Test query"
)

# Print results
for category, tests in results.items():
    print(f"\n{category.upper()}:")
    for test_name, (success, message) in tests.items():
        print(f"  {test_name}: {message}")
```

### Individual Test Categories
```python
from agent_test_functions import run_llm_tests, run_function_calling_tests

# Test only LLM functionality
llm_results = run_llm_tests(llm, "ollama/llama3.1:latest")

# Test only function calling
fc_results = run_function_calling_tests(llm, "ollama/llama3.1:latest", agents=agents)
```

## Test Configuration

### Custom Test Parameters
```python
def configure_test_parameters():
    """
    Pseudocode for configuring test parameters
    """
    return {
        "timeout": 60,              # Workflow timeout in seconds
        "iterations": 3,            # Number of test iterations
        "max_retries": 3,           # Maximum retry attempts
        "response_threshold": 10,   # Minimum response length
        "performance_threshold": 30 # Maximum acceptable execution time
    }
```

### Test Data Generation
```python
def generate_test_queries() -> List[str]:
    """
    Pseudocode for generating test queries
    """
    return [
        "What is artificial intelligence?",
        "Explain machine learning concepts",
        "Describe data science methodologies",
        "What are digital twins?",
        "How does cloud computing work?"
    ]
```

## Error Handling and Reporting

### Test Result Formatting
```python
def format_test_results(results: Dict[str, Dict[str, Tuple[bool, str]]]) -> str:
    """
    Pseudocode for formatting test results
    """
    report = "🧪 TEST RESULTS SUMMARY\n" + "="*50 + "\n"
    
    for category, tests in results.items():
        report += f"\n📋 {category.upper()}:\n"
        
        passed = sum(1 for success, _ in tests.values() if success)
        total = len(tests)
        
        report += f"  Passed: {passed}/{total} tests\n"
        
        for test_name, (success, message) in tests.items():
            status = "✅" if success else "❌"
            report += f"  {status} {test_name}: {message}\n"
    
    return report
```

### Continuous Integration Support
```python
def ci_test_runner(llm, model_name: str) -> bool:
    """
    Pseudocode for CI/CD test runner
    """
    try:
        # 1. Run critical tests only
        critical_tests = [
            test_llm_connectivity,
            test_function_calling_support,
            test_workflow_execution
        ]
        
        # 2. Execute tests
        all_passed = True
        for test_func in critical_tests:
            success, _ = test_func(llm, model_name)
            if not success:
                all_passed = False
        
        # 3. Return CI status
        return all_passed
        
    except Exception as e:
        print(f"CI test runner failed: {e}")
        return False
```
