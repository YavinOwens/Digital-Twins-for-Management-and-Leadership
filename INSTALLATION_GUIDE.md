# Installation Guide - Digital Twins Management System

## Overview

This guide provides step-by-step instructions for installing and setting up the Digital Twins for Management and Leadership - CrewAI Multi-Agent Workflow System with comprehensive document processing capabilities.

## Prerequisites

- **Python 3.8 or higher** (Python 3.13 recommended)
- **pip3** package manager
- **Git** (for cloning the repository)
- **8GB RAM minimum** (16GB recommended for optimal performance)
- **2GB free disk space** (for dependencies and uploaded documents)

## Quick Installation

### Option 1: Automated Installation (Recommended)

```bash
# Clone the repository
git clone https://github.com/YavinOwens/Digital-Twins-for-Management-and-Leadership.git
cd Digital-Twins-for-Management-and-Leadership

# Run the installation script
./install_requirements.sh
```

### Option 2: Manual Installation

```bash
# Clone the repository
git clone https://github.com/YavinOwens/Digital-Twins-for-Management-and-Leadership.git
cd Digital-Twins-for-Management-and-Leadership

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

## Document Processing Dependencies

The system includes comprehensive document processing capabilities with the following key packages:

### Core Document Processing
- **pandas==2.3.2** - Data manipulation and analysis
- **numpy==2.3.3** - Numerical computing
- **openpyxl==3.1.5** - Excel file processing
- **python-docx==1.2.0** - Word document processing
- **PyPDF2==3.0.1** - PDF processing
- **chardet==5.2.0** - Character encoding detection
- **lxml==6.0.1** - XML processing
- **PyYAML==6.0.2** - YAML processing

### Additional PDF Processing
- **pypdf==6.0.0** - Advanced PDF processing
- **pdfminer.six==20250506** - PDF text extraction
- **pdfplumber==0.11.7** - PDF table extraction
- **pypdfium2==4.30.0** - High-performance PDF processing

### Data Analysis and Visualization
- **altair==5.5.0** - Statistical visualization
- **matplotlib-inline==0.1.7** - Plotting
- **pydeck==0.9.1** - 3D visualization

## Supported Document Types

### Structured Data
- **CSV Files** (.csv) - Comma-separated values
- **Excel Files** (.xlsx, .xls) - Spreadsheet data
- **JSON Files** (.json) - JavaScript Object Notation
- **XML Files** (.xml) - Extensible Markup Language
- **YAML Files** (.yaml, .yml) - YAML Ain't Markup Language
- **SQLite Databases** (.sqlite, .db) - SQLite database files

### Semi-Structured Data
- **Text Files** (.txt) - Plain text documents
- **Markdown Files** (.md) - Markdown formatted text
- **Log Files** (.log) - System and application logs
- **TSV Files** (.tsv) - Tab-separated values

### Unstructured Data
- **PDF Files** (.pdf) - Portable Document Format
- **Word Documents** (.docx, .doc) - Microsoft Word documents
- **RTF Files** (.rtf) - Rich Text Format

### Archives
- **ZIP Files** (.zip) - Compressed archives
- **TAR Files** (.tar) - Tape archives
- **GZ Files** (.gz) - Compressed files

## Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
# Ollama Cloud API Key (required for cloud models)
OLLAMA_API_KEY=your_ollama_api_key_here

# Optional: Local Ollama configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:latest
```

### API Keys

1. **Ollama Cloud API Key** (Required for cloud models):
   - Visit [https://ollama.ai/settings](https://ollama.ai/settings)
   - Create an account and generate an API key
   - Add the key to your `.env` file

2. **Local Ollama** (Optional for local models):
   - Install Ollama from [https://ollama.ai](https://ollama.ai)
   - Pull the model: `ollama pull llama3.1:latest`

## Running the Application

### Start the Streamlit Application

```bash
# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Run the application
streamlit run streamlit_app.py
```

The application will be available at `http://localhost:8501`

### Using Document Processing

1. **Upload Documents**: Use the "Document Upload & Data Integration" section
2. **Choose Upload Method**: Individual files, directory, or database connection
3. **Automatic Processing**: Documents are processed and indexed automatically
4. **Agent Access**: All 7 agent teams can access and analyze your documents

## Troubleshooting

### Common Issues

1. **Import Errors**:
   ```bash
   # Reinstall packages
   pip install --upgrade -r requirements.txt
   ```

2. **Memory Issues**:
   - Reduce the number of concurrent document processing
   - Use smaller document files
   - Increase system RAM

3. **Permission Errors**:
   ```bash
   # Fix file permissions
   chmod +x install_requirements.sh
   ```

4. **Virtual Environment Issues**:
   ```bash
   # Recreate virtual environment
   rm -rf venv
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

### Performance Optimization

1. **Document Size**: Keep individual documents under 100MB
2. **Batch Processing**: Process multiple small files rather than one large file
3. **Memory Management**: Monitor memory usage during processing
4. **Storage**: Ensure adequate disk space for uploaded documents

## Development Setup

### For Contributors

```bash
# Clone repository
git clone https://github.com/YavinOwens/Digital-Twins-for-Management-and-Leadership.git
cd Digital-Twins-for-Management-and-Leadership

# Create development environment
python3 -m venv venv
source venv/bin/activate

# Install development dependencies
pip install -r requirements.txt
pip install pytest black flake8 mypy

# Run tests
pytest tests/

# Format code
black .

# Lint code
flake8 .
```

## Support

### Getting Help

1. **Documentation**: Check the `docs/` directory for detailed guides
2. **Issues**: Report issues on GitHub
3. **Discussions**: Use GitHub Discussions for questions
4. **Examples**: See `examples/` directory for usage examples

### System Requirements

- **Operating System**: macOS, Linux, or Windows
- **Python**: 3.8+ (3.13 recommended)
- **RAM**: 8GB minimum, 16GB recommended
- **Storage**: 2GB free space minimum
- **Network**: Internet connection for Ollama Cloud

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contributing

We welcome contributions! Please see CONTRIBUTING.md for guidelines.

---

**Note**: This system processes sensitive organizational data. Ensure proper security measures and compliance with your organization's data policies.
