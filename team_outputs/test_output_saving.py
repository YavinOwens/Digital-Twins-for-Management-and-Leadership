"""
Test script for team output saving functionality
"""

from output_manager import TeamOutputManager, save_team_outputs


def test_output_manager():
    """Test the TeamOutputManager functionality"""
    print("🧪 Testing TeamOutputManager...")
    
    # Initialize manager
    manager = TeamOutputManager()
    
    # Test data
    query = "Test query for digital twin technology"
    team_outputs = {
        "Team 1 - Research & Analysis": "This is a test research output with findings about digital twins.",
        "Team 2 - Data Strategy": "This is a test data strategy output with DAMA frameworks.",
        "Team 3 - Compliance": "This is a test compliance output with regulatory requirements."
    }
    metadata = {
        "timestamp": "2024-01-01 12:00:00",
        "workflow_type": "test_workflow",
        "execution_time": "120.5 seconds"
    }
    
    # Test saving workflow outputs
    output_path = manager.save_workflow_outputs(
        "test_workflow", 
        query, 
        team_outputs, 
        metadata
    )
    
    print(f"✅ Workflow outputs saved to: {output_path}")
    
    # Test saving individual team output
    individual_path = manager.save_individual_team_output(
        "test_workflow",
        "Test Team",
        "This is a test individual team output.",
        query,
        metadata
    )
    
    print(f"✅ Individual team output saved to: {individual_path}")
    
    # Test listing outputs
    outputs = manager.list_workflow_outputs()
    print(f"✅ Found {len(outputs)} workflow outputs")
    
    # Test output summary
    summary = manager.get_output_summary()
    print(f"✅ Output summary: {summary}")
    
    return output_path


def test_convenience_function():
    """Test the convenience function"""
    print("\n🧪 Testing convenience function...")
    
    query = "Another test query"
    team_outputs = {
        "Team A": "Output from Team A",
        "Team B": "Output from Team B"
    }
    metadata = {"test": True}
    
    output_path = save_team_outputs(
        "convenience_test_workflow",
        query,
        team_outputs,
        metadata
    )
    
    print(f"✅ Convenience function output saved to: {output_path}")
    return output_path


if __name__ == "__main__":
    print("🚀 Starting team output saving tests...")
    
    try:
        # Test manager
        test_output_manager()
        
        # Test convenience function
        test_convenience_function()
        
        print("\n✅ All tests completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        print(f"❌ Full traceback: {traceback.format_exc()}")
