#!/usr/bin/env python3
"""
Test RobustLLM v2 to ensure it works correctly
"""
import os
from dotenv import load_dotenv
from agent_tools.robust_llm_v2 import create_robust_llm

# Load environment variables
load_dotenv()

def test_robust_llm_v2():
    """Test RobustLLM v2 with simple call"""
    print("🔍 Testing RobustLLM v2...")
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
        print(f"🔍 Max retries: {llm.max_retries}")
        print(f"🔍 Retry delay: {llm.retry_delay}")
        
        # Test simple call
        print("\n🔧 Testing RobustLLM v2 call...")
        messages = [{"role": "user", "content": "What are 3 benefits of digital twins? Be concise."}]
        
        # Make the call (with retry logic)
        response = llm.call(messages)
        
        if response:
            print(f"✅ RobustLLM v2 response successful: {response[:200]}...")
            return True
        else:
            print("❌ RobustLLM v2 returned empty response")
            return False
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        import traceback
        print(f"❌ Full traceback: {traceback.format_exc()}")
        return False

if __name__ == "__main__":
    success = test_robust_llm_v2()
    if success:
        print("\n🎉 RobustLLM v2 test completed successfully!")
    else:
        print("\n💥 RobustLLM v2 test failed!")
