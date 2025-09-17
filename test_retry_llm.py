#!/usr/bin/env python3
"""
Test RetryLLM to ensure it works correctly
"""
import os
from dotenv import load_dotenv
from agent_tools.retry_llm import create_retry_llm

# Load environment variables
load_dotenv()

def test_retry_llm():
    """Test RetryLLM with simple call"""
    print("🔍 Testing RetryLLM...")
    print("=" * 60)
    
    # Get configuration
    api_key = os.getenv('OLLAMA_API_KEY')
    
    if not api_key:
        print("❌ No API key found. Please set OLLAMA_API_KEY in .env file")
        return False
    
    try:
        # Create RetryLLM
        print("🔧 Creating RetryLLM...")
        llm = create_retry_llm(use_cloud=True, api_key=api_key)
        print(f"✅ RetryLLM created: {type(llm)}")
        print(f"🔍 Max retries: {llm.max_retries}")
        print(f"🔍 Base delay: {llm.base_delay}")
        
        # Test simple call
        print("\n🔧 Testing RetryLLM call...")
        messages = [{"role": "user", "content": "What are 3 benefits of digital twins? Be concise."}]
        
        # Make the call (with retry logic)
        response = llm.call(messages)
        
        if response:
            print(f"✅ RetryLLM response successful: {response[:200]}...")
            return True
        else:
            print("❌ RetryLLM returned empty response")
            return False
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        import traceback
        print(f"❌ Full traceback: {traceback.format_exc()}")
        return False

if __name__ == "__main__":
    success = test_retry_llm()
    if success:
        print("\n🎉 RetryLLM test completed successfully!")
    else:
        print("\n💥 RetryLLM test failed!")
