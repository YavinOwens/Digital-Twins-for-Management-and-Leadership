#!/usr/bin/env python3
"""
Test script for agents package

This script tests that all agents can be imported and created successfully.
"""

def test_agent_imports():
    """Test that all agents can be imported successfully"""
    try:
        from agents import create_crew_agents
        from agents.researcher_agent import create_researcher_agent
        from agents.analyst_agent import create_analyst_agent
        from agents.writer_agent import create_writer_agent
        from agents.agent_factory import create_agents_with_context, get_agent_by_role
        print("✅ All agent imports successful!")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def test_agent_creation():
    """Test that agents can be created successfully"""
    try:
        from agents import create_crew_agents
        
        # Mock LLM for testing
        class MockLLM:
            def __init__(self):
                self.model = "test-model"
        
        mock_llm = MockLLM()
        
        # Test creating all agents
        researcher, analyst, writer = create_crew_agents(mock_llm, use_tools=False)
        
        print(f"✅ Agent creation successful!")
        print(f"   - Researcher role: {researcher.role}")
        print(f"   - Analyst role: {analyst.role}")
        print(f"   - Writer role: {writer.role}")
        return True
    except Exception as e:
        print(f"❌ Agent creation failed: {e}")
        return False

def test_agent_factory():
    """Test the agent factory functions"""
    try:
        from agents.agent_factory import create_agents_with_context, get_agent_by_role
        
        # Mock LLM for testing
        class MockLLM:
            def __init__(self):
                self.model = "test-model"
        
        mock_llm = MockLLM()
        
        # Test dictionary creation
        agents_dict = create_agents_with_context(mock_llm, use_tools=False)
        print(f"✅ Agent factory dictionary creation successful!")
        print(f"   - Available agents: {list(agents_dict.keys())}")
        
        # Test individual agent creation
        researcher = get_agent_by_role('researcher', mock_llm, use_tools=False)
        analyst = get_agent_by_role('data_analyst', mock_llm, use_tools=False)
        writer = get_agent_by_role('content_writer', mock_llm, use_tools=False)
        
        print(f"✅ Individual agent creation successful!")
        print(f"   - Researcher: {researcher.role}")
        print(f"   - Analyst: {analyst.role}")
        print(f"   - Writer: {writer.role}")
        
        return True
    except Exception as e:
        print(f"❌ Agent factory test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing agents package...")
    print("=" * 40)
    
    tests = [
        ("Import Test", test_agent_imports),
        ("Agent Creation Test", test_agent_creation),
        ("Agent Factory Test", test_agent_factory)
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
        print("🎉 All tests passed! The agents package is working correctly.")
        return 0
    else:
        print("⚠️ Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    exit(main())
