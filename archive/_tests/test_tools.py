#!/usr/bin/env python3
"""
Test script for agent_tools package

This script tests that all tools can be imported and basic functionality works.
"""

def test_imports():
    """Test that all tools can be imported successfully"""
    try:
        from agent_tools import search_web, AnalysisTool
        from agent_tools.search_tool import parse_search_results, get_source_quality
        print("✅ All imports successful!")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def test_analysis_tool():
    """Test the AnalysisTool functionality"""
    try:
        from agent_tools import AnalysisTool
        
        # Create an instance
        analysis_tool = AnalysisTool()
        
        # Test with sample data
        sample_data = """
        This is a sample research report about artificial intelligence in healthcare.
        The market is growing at 25% annually with $50 billion in revenue.
        Key challenges include data privacy and regulatory compliance.
        Opportunities include improved patient outcomes and cost reduction.
        """
        
        result = analysis_tool._run(sample_data)
        print("✅ AnalysisTool test successful!")
        print(f"Result length: {len(result)} characters")
        return True
    except Exception as e:
        print(f"❌ AnalysisTool test failed: {e}")
        return False

def test_search_tool_functions():
    """Test the search tool helper functions"""
    try:
        from agent_tools.search_tool import parse_search_results, get_source_quality
        
        # Test quality scoring
        quality_score = get_source_quality("harvard.edu", "This is a research study with academic content and peer-reviewed data.")
        print(f"✅ Quality scoring test successful! Score: {quality_score}")
        
        # Test parsing (with mock data)
        mock_search_text = """
        # Research Results for: AI in Healthcare
        
        ## Source 1: AI Healthcare Study
        **URL:** https://example.com/study
        **Content:** This study shows significant improvements in patient outcomes.
        **Reference:** (Example, 2024)
        
        ## References (Harvard Style):
        1. Example (2024). AI Healthcare Study. Available at: https://example.com/study
        """
        
        parsed = parse_search_results(mock_search_text)
        print(f"✅ Parsing test successful! Found {parsed['total_sources']} sources")
        return True
    except Exception as e:
        print(f"❌ Search tool functions test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing agent_tools package...")
    print("=" * 40)
    
    tests = [
        ("Import Test", test_imports),
        ("AnalysisTool Test", test_analysis_tool),
        ("Search Tool Functions Test", test_search_tool_functions)
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
        print("🎉 All tests passed! The agent_tools package is working correctly.")
        return 0
    else:
        print("⚠️ Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    exit(main())
