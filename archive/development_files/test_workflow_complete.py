#!/usr/bin/env python3
"""
Test complete workflow execution to ensure everything is working
"""
import os
from dotenv import load_dotenv
from agent_tools.robust_llm_v2 import create_robust_llm
from workflows import run_crew_workflow, run_two_team_workflow, run_three_team_workflow

# Load environment variables
load_dotenv()

def test_workflow_execution():
    """Test actual workflow execution"""
    print("🔍 Testing Complete Workflow Execution...")
    print("=" * 60)
    
    # Get configuration
    api_key = os.getenv('OLLAMA_API_KEY')
    
    if not api_key:
        print("❌ No API key found. Please set OLLAMA_API_KEY in .env file")
        return False
    
    try:
        # Create RobustLLM v2
        print("🔧 Creating RobustLLM v2...")
        llm = create_robust_llm(use_cloud=True, api_key=api_key)
        print(f"✅ RobustLLM v2 created: {type(llm)}")
        
        # Test query
        test_query = "What are the main benefits of digital twins in education? Provide 3 key benefits with brief explanations."
        
        print(f"\n🔧 Testing with query: {test_query}")
        print("=" * 60)
        
        # Test single team workflow
        print("\n🚀 Testing Single Team Workflow...")
        result = run_crew_workflow(
            query=test_query,
            llm=llm,
            conversation_history=None,
            use_native_function_calling=False
        )
        
        if result and len(str(result)) > 100:
            print(f"✅ Single team workflow completed successfully!")
            print(f"📊 Result length: {len(str(result))} characters")
            print(f"📝 Result preview: {str(result)[:200]}...")
            return True
        else:
            print(f"❌ Single team workflow failed or returned empty result")
            print(f"📊 Result: {repr(result)}")
            return False
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        import traceback
        print(f"❌ Full traceback: {traceback.format_exc()}")
        return False

if __name__ == "__main__":
    success = test_workflow_execution()
    if success:
        print("\n🎉 Workflow test completed successfully!")
    else:
        print("\n💥 Workflow test failed!")
