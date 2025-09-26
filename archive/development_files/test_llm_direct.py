#!/usr/bin/env python3
"""
Test LLM directly to see what's happening
"""
import os
from dotenv import load_dotenv
from crewai import LLM

# Load environment variables
load_dotenv()

def test_llm_direct():
    """Test LLM directly with simple call"""
    print("🔍 Testing LLM directly...")
    print("=" * 60)
    
    # Get configuration
    api_key = os.getenv('OLLAMA_API_KEY')
    
    if not api_key:
        print("❌ No API key found. Please set OLLAMA_API_KEY in .env file")
        return False
    
    try:
        # Create LLM exactly like llm_manager does
        print("🔧 Creating LLM exactly like llm_manager...")
        llm = LLM(
            model="ollama/gpt-oss:20b",
            base_url="https://ollama.com",
            headers={'Authorization': f'Bearer {api_key}'},
            temperature=0.5,
            max_tokens=8000,
            system_message="You are an expert business consultant and writer. When asked to write reports, you must provide complete, detailed content - never summaries or placeholders. Write comprehensive, actionable content that executives can use immediately for decision-making. NEVER use ellipsis (...), continuation phrases, or placeholders like '[Insert content here]' or '[The actual content would continue here]'. Always write the complete, final content for every section. ONLY use references from the actual research data provided - NEVER make up citations, author names, or publication details."
        )
        print(f"✅ LLM created: {type(llm)}")
        print(f"🔍 LLM model: {llm.model}")
        print(f"🔍 LLM base_url: {llm.base_url}")
        
        # Test simple call
        print("\n🔧 Testing simple LLM call...")
        messages = [{"role": "user", "content": "What are the main benefits of digital twins? Give me 3 key benefits in 2 sentences each."}]
        
        print(f"🔍 Input messages: {messages}")
        
        # Make the call
        response = llm.call(messages)
        
        print(f"🔍 Raw response type: {type(response)}")
        print(f"🔍 Raw response: {repr(response)}")
        
        if response:
            print(f"✅ LLM response successful: {response[:200]}...")
            return True
        else:
            print("❌ LLM returned empty response")
            return False
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        import traceback
        print(f"❌ Full traceback: {traceback.format_exc()}")
        return False

if __name__ == "__main__":
    success = test_llm_direct()
    if success:
        print("\n🎉 Direct LLM test completed successfully!")
    else:
        print("\n💥 Direct LLM test failed!")
