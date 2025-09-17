#!/usr/bin/env python3
"""
Test script for agent_tasks package

This script tests that all tasks can be imported and created successfully.
"""

def test_task_imports():
    """Test that all tasks can be imported successfully"""
    try:
        from agent_tasks import create_crew_tasks, create_crew_tasks_with_data
        from agent_tasks.research_task import create_research_task, create_research_task_with_data
        from agent_tasks.analysis_task import create_analysis_task
        from agent_tasks.writing_task import create_writing_task
        from agent_tasks.task_factory import create_tasks_by_type, create_tasks_dictionary
        print("✅ All task imports successful!")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def test_task_creation():
    """Test that tasks can be created successfully"""
    try:
        from agent_tasks import create_crew_tasks
        from agents import create_crew_agents
        
        # Mock LLM and agents for testing
        class MockLLM:
            def __init__(self):
                self.model = "test-model"
        
        class MockAgent:
            def __init__(self, role):
                self.role = role
        
        mock_llm = MockLLM()
        researcher = MockAgent("Research Specialist")
        analyst = MockAgent("Data Analyst")
        writer = MockAgent("Content Writer")
        
        # Test creating all tasks
        tasks = create_crew_tasks(researcher, analyst, writer, "test query", use_tools=False)
        
        print(f"✅ Task creation successful!")
        print(f"   - Number of tasks: {len(tasks)}")
        print(f"   - Task types: {[task.agent.role for task in tasks]}")
        return True
    except Exception as e:
        print(f"❌ Task creation failed: {e}")
        return False

def test_task_factory():
    """Test the task factory functions"""
    try:
        from agent_tasks.task_factory import create_tasks_by_type, create_tasks_dictionary
        
        # Mock agent for testing
        class MockAgent:
            def __init__(self, role):
                self.role = role
        
        researcher = MockAgent("Research Specialist")
        analyst = MockAgent("Data Analyst")
        writer = MockAgent("Content Writer")
        
        # Test individual task creation
        research_task = create_tasks_by_type('research', researcher, "test query", use_tools=False)
        analysis_task = create_tasks_by_type('analysis', analyst, "test query", use_tools=False)
        writing_task = create_tasks_by_type('writing', writer, "test query")
        
        print(f"✅ Individual task creation successful!")
        print(f"   - Research task: {research_task.agent.role}")
        print(f"   - Analysis task: {analysis_task.agent.role}")
        print(f"   - Writing task: {writing_task.agent.role}")
        
        # Test dictionary creation
        tasks_dict = create_tasks_dictionary(researcher, analyst, writer, "test query", use_tools=False)
        print(f"✅ Task dictionary creation successful!")
        print(f"   - Available tasks: {list(tasks_dict.keys())}")
        
        return True
    except Exception as e:
        print(f"❌ Task factory test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing agent_tasks package...")
    print("=" * 40)
    
    tests = [
        ("Import Test", test_task_imports),
        ("Task Creation Test", test_task_creation),
        ("Task Factory Test", test_task_factory)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Running {test_name}...")
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} failed!")
    
    print("\n" + "=" * 40)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The agent_tasks package is working correctly.")
        return 0
    else:
        print("⚠️ Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    exit(main())
