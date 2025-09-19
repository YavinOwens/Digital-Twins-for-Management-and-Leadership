#!/bin/bash

# Digital Twins for Management and Leadership - Installation Script
# This script installs all required dependencies for the CrewAI Multi-Agent Workflow System

echo "🚀 Installing Digital Twins Management System Dependencies..."
echo "=========================================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip3."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install core requirements
echo "📚 Installing core requirements..."
pip install -r local_requirements.txt

# Install additional document processing packages if not already installed
echo "📄 Installing document processing packages..."
pip install python-docx PyPDF2 chardet

# Verify installation
echo "✅ Verifying installation..."
python3 -c "
import streamlit
import crewai
import pandas
import openpyxl
import docx
import PyPDF2
import chardet
print('✅ All core packages installed successfully!')
"

echo ""
echo "🎉 Installation completed successfully!"
echo ""
echo "To run the application:"
echo "1. Activate the virtual environment: source venv/bin/activate"
echo "2. Run the Streamlit app: streamlit run streamlit_app.py"
echo ""
echo "For more information, see the README.md file."
