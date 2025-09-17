#!/usr/bin/env python3
"""
Debug script to test LLM response handling
"""
import os
from dotenv import load_dotenv
from crewai import LLM

# Load environment variables
load_dotenv()

def debug_llm_response():
    """Debug LLM response handling"""
    print("🔍 Debugging LLM Response...")
    print("=" * 60)
    
    # Get configuration
    api_key = os.getenv('OLLAMA_API_KEY')
    base_url = os.getenv('OLLAMA_CLOUD_BASE_URL', 'https://ollama.com')
    model = os.getenv('OLLAMA_CLOUD_MODEL', 'gpt-oss:20b')
    
    try:
        # Initialize LLM
        print("🔧 Initializing LLM...")
        llm = LLM(
            model=f"ollama/{model}",
            base_url=base_url,
            headers={'Authorization': f'Bearer {api_key}'},
            temperature=0.7,
            max_tokens=100
        )
        
        # Test different types of calls
        test_messages = [
            "Hello",
            "Can you respond with just 'Hi'?",
            "What is 2+2?",
            "Say 'test' if you can hear me"
        ]
        
        for i, message in enumerate(test_messages, 1):
            print(f"\n📞 Test {i}: '{message}'")
            try:
                response = llm.call(message)
                print(f"Response type: {type(response)}")
                print(f"Response length: {len(response) if response else 'None'}")
                print(f"Response content: {repr(response)}")
                
                if response and len(response) > 0:
                    print("✅ Success!")
                else:
                    print("❌ Empty or None response")
                    
            except Exception as e:
                print(f"❌ Error: {str(e)}")
        
        # Test with different parameters
        print(f"\n🔧 Testing with different parameters...")
        try:
            # Test with streaming
            print("Testing streaming...")
            response = llm.call("Hello", stream=True)
            print(f"Streaming response: {response}")
            
        except Exception as e:
            print(f"Streaming error: {str(e)}")
            
    except Exception as e:
        print(f"❌ Initialization error: {str(e)}")

if __name__ == "__main__":
    debug_llm_response()
