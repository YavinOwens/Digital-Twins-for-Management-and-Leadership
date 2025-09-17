#!/usr/bin/env python3
"""
Test script for Ollama Cloud API connection
"""
import os
from dotenv import load_dotenv
from crewai import LLM

# Load environment variables
load_dotenv()

def test_ollama_cloud():
    """Test Ollama Cloud connection"""
    print("🧪 Testing Ollama Cloud Connection...")
    print("=" * 60)
    
    # Get API key from environment
    api_key = os.getenv('OLLAMA_API_KEY')
    base_url = os.getenv('OLLAMA_CLOUD_BASE_URL', 'https://ollama.com')
    model = os.getenv('OLLAMA_CLOUD_MODEL', 'gpt-oss:20b')
    
    print(f"📋 Configuration:")
    print(f"  Base URL: {base_url}")
    print(f"  Model: {model}")
    print(f"  API Key: {'Set' if api_key else 'Not set'}")
    
    if not api_key:
        print("❌ No API key found in environment variables")
        print("💡 Please set OLLAMA_API_KEY in your .env file")
        print("💡 Get your API key from: https://ollama.com/settings/keys")
        return False
    
    if api_key == "your_api_key_here":
        print("❌ API key is still set to placeholder value")
        print("💡 Please replace 'your_api_key_here' with your actual API key")
        return False
    
    try:
        # Initialize LLM
        print("\n🔧 Initializing LLM...")
        llm = LLM(
            model=f"ollama/{model}",
            base_url=base_url,
            headers={'Authorization': f'Bearer {api_key}'},
            temperature=0.7,
            max_tokens=100
        )
        
        # Test simple call
        print("📞 Testing API call...")
        response = llm.call("Hello, can you respond with just 'Hi'?")
        
        if response and len(response) > 0:
            print(f"✅ Success! Response: {response[:100]}...")
            return True
        else:
            print("❌ Empty response received")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("\n💡 Troubleshooting:")
        print("  1. Check if your API key is correct")
        print("  2. Verify you have an active Ollama Cloud subscription")
        print("  3. Ensure the model name is correct")
        print("  4. Check your internet connection")
        return False

if __name__ == "__main__":
    success = test_ollama_cloud()
    if success:
        print("\n🎉 Ollama Cloud is working correctly!")
    else:
        print("\n🔧 Please fix the issues above and try again")
