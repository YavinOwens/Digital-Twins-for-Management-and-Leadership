#!/usr/bin/env python3
"""
Quick start script for CrewAI + Streamlit Workflow
"""

import subprocess
import sys
import time
from pathlib import Path

def main():
    """Run the Streamlit application"""
    print("🚀 Starting CrewAI + Streamlit Workflow...")
    print("=" * 40)
    
    # Check if streamlit_app.py exists
    app_file = Path("streamlit_app.py")
    if not app_file.exists():
        print("❌ streamlit_app.py not found")
        return 1
    
    print("📱 Launching Streamlit application...")
    print("🌐 Application will open in your default browser")
    print("🛑 Press Ctrl+C to stop the application")
    print()
    
    try:
        # Run streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            str(app_file),
            "--server.address", "localhost",
            "--server.port", "8501",
            "--browser.gatherUsageStats", "false"
        ], check=True)
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start application: {e}")
        return 1
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
        return 0
    
    return 0

if __name__ == "__main__":
    exit(main())
