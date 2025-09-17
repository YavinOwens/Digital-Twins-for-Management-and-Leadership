#!/usr/bin/env python3
"""
Test the updated function calling support
"""
import os
from dotenv import load_dotenv
from crewai import LLM

# Load environment variables
load_dotenv()

def test_function_calling_support(llm, model_name):
    """Test if the LLM is working and responsive"""
    try:
        # Simple test message
        test_message = "Hello, can you respond with just 'Hi'?"
        
        # Test basic LLM call
        response = llm.call(test_message)
        
        if response and len(response) > 0:
            return True, f"✅ {model_name} is working and responsive (Response: {response[:50]}...)"
        else:
            return False, f"❌ {model_name} returned empty response"
            
    except Exception as e:
        return False, f"❌ {model_name} failed: {str(e)}"

def main():
    print("🧪 Testing Function Calling Support...")
    print("=" * 60)
    
    # Test local LLM
    print("🔍 Testing Local llama3.1...")
    try:
        local_llm = LLM(
            model="ollama/llama3.1",
            base_url="http://localhost:11434",
            temperature=0.7,
            max_tokens=100
        )
        success, message = test_function_calling_support(local_llm, 'llama3.1')
        print(f"Local: {message}")
    except Exception as e:
        print(f"Local failed: {e}")
    
    # Test cloud LLM
    print("\n🔍 Testing Cloud gpt-oss:20b...")
    try:
        api_key = os.getenv('OLLAMA_API_KEY')
        cloud_llm = LLM(
            model="ollama/gpt-oss:20b",
            base_url="https://ollama.com",
            headers={'Authorization': f'Bearer {api_key}'},
            temperature=0.7,
            max_tokens=100
        )
        success, message = test_function_calling_support(cloud_llm, 'gpt-oss:20b (Turbo)')
        print(f"Cloud: {message}")
    except Exception as e:
        print(f"Cloud failed: {e}")

if __name__ == "__main__":
    main()
