"""
Test script for the modular agent teams structure
"""

def test_imports():
    """Test that all team modules can be imported correctly"""
    print("🧪 Testing modular structure imports...")
    
    try:
        # Test research analysis team
        from .research_analysis import create_research_analysis_agents_with_context, create_research_analysis_tasks_with_data
        print("✅ Research Analysis team imported successfully")
        
        # Test data strategy team
        from .data_strategy import create_data_strategy_agents_with_context, create_data_strategy_tasks_with_data
        print("✅ Data Strategy team imported successfully")
        
        # Test compliance risk team
        from .compliance_risk import create_compliance_risk_agents_with_context, create_compliance_risk_tasks_with_data
        print("✅ Compliance Risk team imported successfully")
        
        # Test information management team
        from .information_management import create_information_management_agents_with_context, create_information_management_tasks_with_data
        print("✅ Information Management team imported successfully")
        
        # Test tender response team
        from .tender_response import create_tender_response_agents_with_context, create_tender_response_tasks_with_data
        print("✅ Tender Response team imported successfully")
        
        # Test project delivery team
        from .project_delivery import create_project_delivery_agents_with_context, create_project_delivery_tasks_with_data
        print("✅ Project Delivery team imported successfully")
        
        # Test technical documentation team
        from .technical_documentation import create_technical_documentation_agents_with_context, create_technical_documentation_tasks_with_data
        print("✅ Technical Documentation team imported successfully")
        
        print("\n✅ All team modules imported successfully!")
        return True
        
    except Exception as e:
        print(f"\n❌ Import failed: {e}")
        import traceback
        print(f"❌ Full traceback: {traceback.format_exc()}")
        return False


def test_team_structure():
    """Test the team structure and organization"""
    print("\n🧪 Testing team structure...")
    
    import os
    from pathlib import Path
    
    # Check if all team directories exist
    agent_teams_dir = Path("agent_teams")
    expected_teams = [
        "research_analysis",
        "data_strategy", 
        "compliance_risk",
        "information_management",
        "tender_response",
        "project_delivery",
        "technical_documentation"
    ]
    
    for team in expected_teams:
        team_dir = agent_teams_dir / team
        if team_dir.exists():
            print(f"✅ {team} directory exists")
            
            # Check for required files
            agents_file = team_dir / "agents.py"
            tasks_file = team_dir / "tasks.py"
            init_file = team_dir / "__init__.py"
            
            if agents_file.exists():
                print(f"  ✅ {team}/agents.py exists")
            else:
                print(f"  ❌ {team}/agents.py missing")
                
            if tasks_file.exists():
                print(f"  ✅ {team}/tasks.py exists")
            else:
                print(f"  ❌ {team}/tasks.py missing")
                
            if init_file.exists():
                print(f"  ✅ {team}/__init__.py exists")
            else:
                print(f"  ❌ {team}/__init__.py missing")
        else:
            print(f"❌ {team} directory missing")
    
    print("\n✅ Team structure test completed!")


if __name__ == "__main__":
    print("🚀 Starting modular structure tests...")
    
    try:
        # Test imports
        import_success = test_imports()
        
        # Test structure
        test_team_structure()
        
        if import_success:
            print("\n✅ All tests completed successfully!")
        else:
            print("\n❌ Some tests failed!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        print(f"❌ Full traceback: {traceback.format_exc()}")
