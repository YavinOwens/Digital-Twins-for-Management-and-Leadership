#!/usr/bin/env python3
"""
Setup script for CrewAI + Streamlit Workflow
Helps verify installation and setup requirements
"""

import subprocess
import sys
import requests
from pathlib import Path

def check_ollama_installation():
    """Check if Ollama is installed and running"""
    print("🔍 Checking Ollama installation...")
    
    try:
        # Check if ollama command exists
        subprocess.run(["ollama", "--version"], capture_output=True, check=True)
        print("✅ Ollama is installed")
        
        # Check if Ollama server is running
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            print("✅ Ollama server is running")
            
            # Check if phi3 model is available
            models = response.json()
            phi3_available = any("phi3" in model["name"] for model in models.get("models", []))
            
            if phi3_available:
                print("✅ phi3 model is available")
                return True
            else:
                print("❌ phi3 model not found")
                print("Run: ollama pull phi3")
                return False
        else:
            print("❌ Ollama server not responding")
            return False
            
    except subprocess.CalledProcessError:
        print("❌ Ollama not installed")
        print("Install with: brew install ollama")
        return False
    except requests.RequestException:
        print("❌ Cannot connect to Ollama server")
        print("Start with: ollama serve")
        return False

def install_requirements():
    """Install Python requirements"""
    print("📦 Installing Python requirements...")
    
    requirements_file = Path("local_requirements.txt")
    if requirements_file.exists():
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", str(requirements_file)], 
                         check=True)
            print("✅ Python requirements installed")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install requirements: {e}")
            return False
    else:
        print("❌ local_requirements.txt not found")
        return False

def main():
    """Main setup function"""
    print("🚀 CrewAI + Streamlit Workflow Setup")
    print("=" * 40)
    
    success = True
    
    # Check Ollama
    if not check_ollama_installation():
        success = False
    
    print()
    
    # Install requirements
    if not install_requirements():
        success = False
    
    print()
    
    if success:
        print("🎉 Setup complete!")
        print("\nTo run the application:")
        print("streamlit run streamlit_app.py")
    else:
        print("❌ Setup incomplete. Please resolve the issues above.")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
