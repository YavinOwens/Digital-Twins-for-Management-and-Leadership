"""
Test script for presearch functionality
"""

from presearch_manager import PreSearchManager, perform_presearch


def test_presearch_manager():
    """Test the PreSearchManager functionality"""
    print("🧪 Testing PreSearchManager...")
    
    # Initialize manager
    manager = PreSearchManager(memory_enabled=True, max_memory_results=3)
    
    # Test search
    query = "digital twin technology"
    search_data = manager.search_and_combine_context(query)
    
    print(f"✅ Query: {search_data['query']}")
    print(f"✅ Search time: {search_data['search_time']:.2f} seconds")
    print(f"✅ Memory results: {'Found' if search_data['memory_results'] else 'None'}")
    print(f"✅ Web results: {'Found' if search_data['web_results'] else 'None'}")
    print(f"✅ Combined context length: {len(search_data['combined_context'])} characters")
    
    return search_data


def test_convenience_function():
    """Test the convenience function"""
    print("\n🧪 Testing convenience function...")
    
    query = "artificial intelligence"
    search_data = perform_presearch(query)
    
    print(f"✅ Query: {search_data['query']}")
    print(f"✅ Search time: {search_data['search_time']:.2f} seconds")
    
    return search_data


if __name__ == "__main__":
    print("🚀 Starting presearch tests...")
    
    try:
        # Test manager
        test_presearch_manager()
        
        # Test convenience function
        test_convenience_function()
        
        print("\n✅ All tests completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        print(f"❌ Full traceback: {traceback.format_exc()}")
