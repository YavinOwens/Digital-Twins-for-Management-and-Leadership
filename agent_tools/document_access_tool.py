"""
Document Access Tool for Digital Twins Management System

This module provides agents with tools to access and work with uploaded documents.
"""

from crewai.tools import tool
from typing import Dict, List, Any, Optional
import pandas as pd
import json
import logging
import streamlit as st
from agent_tools.data_analysis_tool import DataAnalysisTool
from agent_tools.document_memory_manager import (
    search_documents_in_memory,
    get_document_from_memory,
    list_documents_in_memory
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize data analysis tool
data_analyzer = DataAnalysisTool()

def get_uploaded_documents() -> Dict[str, Any]:
    """
    Get uploaded documents from Streamlit session state
    """
    try:
        if hasattr(st, 'session_state') and 'uploaded_documents' in st.session_state:
            return st.session_state.uploaded_documents
        return {}
    except Exception as e:
        logger.error(f"Error accessing session state: {e}")
        return {}

@tool("access_uploaded_documents")
def access_uploaded_documents() -> str:
    """
    Access information about all uploaded documents in the Digital Twin system.
    Returns a summary of available documents and their characteristics.
    """
    try:
        documents = get_uploaded_documents()
        
        if not documents:
            return "No documents have been uploaded to the Digital Twin system yet."
        
        result_parts = ["**Available Documents in Digital Twin System:**\n"]
        
        for doc_name, doc_data in documents.items():
            if 'error' in doc_data:
                result_parts.append(f"- **{doc_name}**: ❌ Error - {doc_data['error']}")
                continue
            
            # Get document summary
            doc_type = doc_data.get('type', 'unknown')
            data_type = doc_data.get('data_type', 'unknown')
            
            result_parts.append(f"- **{doc_name}**: {doc_type} ({data_type})")
            
            # Add specific details based on document type
            if doc_type == 'structured':
                if 'shape' in doc_data:
                    result_parts.append(f"  - Data points: {doc_data['shape'][0]:,} rows, {doc_data['shape'][1]} columns")
                if 'columns' in doc_data:
                    result_parts.append(f"  - Columns: {', '.join(doc_data['columns'][:5])}{'...' if len(doc_data['columns']) > 5 else ''}")
            
            elif doc_type == 'semi_structured':
                if 'line_count' in doc_data:
                    result_parts.append(f"  - Lines: {doc_data['line_count']:,}")
                if 'word_count' in doc_data:
                    result_parts.append(f"  - Words: {doc_data['word_count']:,}")
            
            elif doc_type == 'unstructured':
                if 'word_count' in doc_data:
                    result_parts.append(f"  - Words: {doc_data['word_count']:,}")
                if 'page_count' in doc_data:
                    result_parts.append(f"  - Pages: {doc_data['page_count']}")
            
            # Add metadata
            metadata = doc_data.get('metadata', {})
            if 'file_size' in metadata:
                result_parts.append(f"  - Size: {metadata['file_size']:,} bytes")
        
        result_parts.append("\n**Available Operations:**")
        result_parts.append("- analyze_document_data: Analyze specific document data")
        result_parts.append("- query_document_data: Query document data with natural language")
        result_parts.append("- get_document_summary: Get summary of document contents")
        result_parts.append("- search_document_content: Search for specific content in documents")
        
        return "\n".join(result_parts)
        
    except Exception as e:
        logger.error(f"Error accessing uploaded documents: {e}")
        return f"Error accessing documents: {e}"

@tool("analyze_document_data")
def analyze_document_data(document_name: str, analysis_type: str = "comprehensive") -> str:
    """
    Analyze uploaded document data to extract insights and patterns.
    
    Args:
        document_name: Name of the document to analyze
        analysis_type: Type of analysis (comprehensive, statistical, text, temporal, categorical)
    
    Returns:
        Analysis results and insights
    """
    try:
        documents = get_uploaded_documents()
        
        if document_name not in documents:
            return f"Document '{document_name}' not found. Available documents: {list(documents.keys())}"
        
        doc_data = documents[document_name]
        
        if 'error' in doc_data:
            return f"Error in document '{document_name}': {doc_data['error']}"
        
        analysis_types = {
            "comprehensive": "Complete analysis including data quality, patterns, and insights",
            "statistical": "Statistical analysis of numeric data",
            "text": "Text analysis for unstructured content",
            "temporal": "Time-series analysis for temporal data",
            "categorical": "Analysis of categorical variables"
        }
        
        result_parts = [f"**Document Analysis Results for: {document_name}**\n"]
        result_parts.append(f"Analysis Type: {analysis_type}")
        result_parts.append(f"Description: {analysis_types.get(analysis_type, 'Custom analysis')}\n")
        
        # Get document type and basic info
        doc_type = doc_data.get('type', 'unknown')
        data_type = doc_data.get('data_type', 'unknown')
        result_parts.append(f"Document Type: {doc_type} ({data_type})")
        
        # Perform analysis based on document type
        if doc_type == 'structured':
            result_parts.append("\n**Structured Data Analysis:**")
            
            if 'shape' in doc_data:
                rows, cols = doc_data['shape']
                result_parts.append(f"- Dataset size: {rows:,} rows × {cols} columns")
            
            if 'columns' in doc_data:
                result_parts.append(f"- Columns: {', '.join(doc_data['columns'])}")
            
            if 'sample_data' in doc_data and doc_data['sample_data']:
                sample_df = pd.DataFrame(doc_data['sample_data'])
                result_parts.append(f"- Sample data preview: {len(sample_df)} rows shown")
                
                # Basic statistics for numeric columns
                numeric_cols = sample_df.select_dtypes(include=['number']).columns
                if len(numeric_cols) > 0:
                    result_parts.append(f"- Numeric columns: {', '.join(numeric_cols)}")
                    for col in numeric_cols[:3]:  # Show stats for first 3 numeric columns
                        stats = sample_df[col].describe()
                        result_parts.append(f"  - {col}: mean={stats['mean']:.2f}, std={stats['std']:.2f}, min={stats['min']:.2f}, max={stats['max']:.2f}")
        
        elif doc_type == 'semi_structured':
            result_parts.append("\n**Semi-structured Data Analysis:**")
            
            if 'line_count' in doc_data:
                result_parts.append(f"- Total lines: {doc_data['line_count']:,}")
            
            if 'word_count' in doc_data:
                result_parts.append(f"- Total words: {doc_data['word_count']:,}")
            
            if 'headers' in doc_data:
                result_parts.append(f"- Headers found: {len(doc_data['headers'])}")
                result_parts.append(f"- Header names: {', '.join(doc_data['headers'][:5])}{'...' if len(doc_data['headers']) > 5 else ''}")
        
        elif doc_type == 'unstructured':
            result_parts.append("\n**Unstructured Data Analysis:**")
            
            if 'word_count' in doc_data:
                result_parts.append(f"- Total words: {doc_data['word_count']:,}")
            
            if 'page_count' in doc_data:
                result_parts.append(f"- Total pages: {doc_data['page_count']}")
            
            if 'sample_text' in doc_data:
                sample_text = doc_data['sample_text']
                result_parts.append(f"- Sample text length: {len(sample_text)} characters")
                result_parts.append(f"- Sample preview: {sample_text[:200]}...")
        
        # Add metadata
        metadata = doc_data.get('metadata', {})
        if metadata:
            result_parts.append("\n**Document Metadata:**")
            if 'file_size' in metadata:
                result_parts.append(f"- File size: {metadata['file_size']:,} bytes")
            if 'file_type' in metadata:
                result_parts.append(f"- File type: {metadata['file_type']}")
        
        result_parts.append("\n**Analysis Complete:**")
        result_parts.append("- Document successfully analyzed")
        result_parts.append("- Data structure and content examined")
        result_parts.append("- Ready for further processing and querying")
        
        return "\n".join(result_parts)
        
    except Exception as e:
        logger.error(f"Error analyzing document {document_name}: {e}")
        return f"Error analyzing document: {e}"

@tool("query_document_data")
def query_document_data(document_name: str, query: str) -> str:
    """
    Query uploaded document data using natural language questions.
    
    Args:
        document_name: Name of the document to query
        query: Natural language query about the document
    
    Returns:
        Query results and answers
    """
    try:
        documents = get_uploaded_documents()
        
        if document_name not in documents:
            return f"Document '{document_name}' not found. Available documents: {list(documents.keys())}"
        
        doc_data = documents[document_name]
        
        if 'error' in doc_data:
            return f"Error in document '{document_name}': {doc_data['error']}"
        
        result_parts = [f"**Query Results for: {document_name}**\n"]
        result_parts.append(f"Query: \"{query}\"\n")
        
        doc_type = doc_data.get('type', 'unknown')
        
        # Process query based on document type
        if doc_type == 'structured':
            result_parts.append("**Structured Data Query Results:**")
            
            if 'sample_data' in doc_data and doc_data['sample_data']:
                sample_df = pd.DataFrame(doc_data['sample_data'])
                
                # Basic query processing for structured data
                query_lower = query.lower()
                
                if 'column' in query_lower or 'field' in query_lower:
                    if 'columns' in doc_data:
                        result_parts.append(f"- Available columns: {', '.join(doc_data['columns'])}")
                
                if 'row' in query_lower or 'record' in query_lower:
                    if 'shape' in doc_data:
                        rows, cols = doc_data['shape']
                        result_parts.append(f"- Total rows: {rows:,}")
                
                if 'statistic' in query_lower or 'average' in query_lower or 'mean' in query_lower:
                    numeric_cols = sample_df.select_dtypes(include=['number']).columns
                    if len(numeric_cols) > 0:
                        result_parts.append("- Numeric column statistics:")
                        for col in numeric_cols[:3]:
                            stats = sample_df[col].describe()
                            result_parts.append(f"  - {col}: mean={stats['mean']:.2f}, min={stats['min']:.2f}, max={stats['max']:.2f}")
                
                if 'sample' in query_lower or 'preview' in query_lower:
                    result_parts.append(f"- Sample data ({len(sample_df)} rows):")
                    result_parts.append(sample_df.head().to_string())
        
        elif doc_type == 'semi_structured':
            result_parts.append("**Semi-structured Data Query Results:**")
            
            query_lower = query.lower()
            
            if 'line' in query_lower:
                if 'line_count' in doc_data:
                    result_parts.append(f"- Total lines: {doc_data['line_count']:,}")
            
            if 'word' in query_lower:
                if 'word_count' in doc_data:
                    result_parts.append(f"- Total words: {doc_data['word_count']:,}")
            
            if 'header' in query_lower:
                if 'headers' in doc_data:
                    result_parts.append(f"- Headers: {', '.join(doc_data['headers'])}")
            
            if 'content' in query_lower or 'text' in query_lower:
                if 'sample_lines' in doc_data:
                    result_parts.append("- Sample content:")
                    for line in doc_data['sample_lines'][:5]:
                        result_parts.append(f"  {line}")
        
        elif doc_type == 'unstructured':
            result_parts.append("**Unstructured Data Query Results:**")
            
            query_lower = query.lower()
            
            if 'word' in query_lower:
                if 'word_count' in doc_data:
                    result_parts.append(f"- Total words: {doc_data['word_count']:,}")
            
            if 'page' in query_lower:
                if 'page_count' in doc_data:
                    result_parts.append(f"- Total pages: {doc_data['page_count']}")
            
            if 'content' in query_lower or 'text' in query_lower:
                if 'sample_text' in doc_data:
                    sample_text = doc_data['sample_text']
                    result_parts.append("- Sample content:")
                    result_parts.append(f"  {sample_text[:300]}...")
        
        result_parts.append("\n**Query Processing Complete:**")
        result_parts.append("- Document queried successfully")
        result_parts.append("- Results based on available data")
        result_parts.append("- Use analyze_document_data for deeper analysis")
        
        return "\n".join(result_parts)
        
    except Exception as e:
        logger.error(f"Error querying document {document_name}: {e}")
        return f"Error querying document: {e}"

@tool("get_document_summary")
def get_document_summary(document_name: str) -> str:
    """
    Get a comprehensive summary of an uploaded document.
    
    Args:
        document_name: Name of the document to summarize
    
    Returns:
        Document summary with key information
    """
    try:
        documents = get_uploaded_documents()
        
        if document_name not in documents:
            return f"Document '{document_name}' not found. Available documents: {list(documents.keys())}"
        
        doc_data = documents[document_name]
        
        if 'error' in doc_data:
            return f"Error in document '{document_name}': {doc_data['error']}"
        
        result_parts = [f"**Document Summary for: {document_name}**\n"]
        
        # Basic document information
        doc_type = doc_data.get('type', 'unknown')
        data_type = doc_data.get('data_type', 'unknown')
        result_parts.append(f"**Document Type:** {doc_type} ({data_type})")
        
        # Document-specific summary
        if doc_type == 'structured':
            result_parts.append("\n**Structured Data Summary:**")
            
            if 'shape' in doc_data:
                rows, cols = doc_data['shape']
                result_parts.append(f"- Dataset dimensions: {rows:,} rows × {cols} columns")
            
            if 'columns' in doc_data:
                result_parts.append(f"- Column names: {', '.join(doc_data['columns'])}")
            
            if 'sample_data' in doc_data and doc_data['sample_data']:
                sample_df = pd.DataFrame(doc_data['sample_data'])
                result_parts.append(f"- Sample data available: {len(sample_df)} rows")
                
                # Data types summary
                dtypes = sample_df.dtypes.value_counts()
                result_parts.append(f"- Data types: {dict(dtypes)}")
        
        elif doc_type == 'semi_structured':
            result_parts.append("\n**Semi-structured Data Summary:**")
            
            if 'line_count' in doc_data:
                result_parts.append(f"- Total lines: {doc_data['line_count']:,}")
            
            if 'word_count' in doc_data:
                result_parts.append(f"- Total words: {doc_data['word_count']:,}")
            
            if 'headers' in doc_data:
                result_parts.append(f"- Headers: {', '.join(doc_data['headers'])}")
            
            if 'sample_lines' in doc_data:
                result_parts.append(f"- Sample lines available: {len(doc_data['sample_lines'])}")
        
        elif doc_type == 'unstructured':
            result_parts.append("\n**Unstructured Data Summary:**")
            
            if 'word_count' in doc_data:
                result_parts.append(f"- Total words: {doc_data['word_count']:,}")
            
            if 'page_count' in doc_data:
                result_parts.append(f"- Total pages: {doc_data['page_count']}")
            
            if 'sample_text' in doc_data:
                sample_text = doc_data['sample_text']
                result_parts.append(f"- Sample text length: {len(sample_text)} characters")
        
        # Metadata summary
        metadata = doc_data.get('metadata', {})
        if metadata:
            result_parts.append("\n**File Metadata:**")
            if 'file_size' in metadata:
                result_parts.append(f"- File size: {metadata['file_size']:,} bytes")
            if 'file_type' in metadata:
                result_parts.append(f"- File type: {metadata['file_type']}")
        
        # Usage information
        result_parts.append("\n**Available Operations:**")
        result_parts.append("- analyze_document_data: Detailed analysis and insights")
        result_parts.append("- query_document_data: Natural language querying")
        result_parts.append("- search_document_content: Content search and filtering")
        
        result_parts.append("\n**Digital Twin Integration:**")
        result_parts.append("- Document is accessible to all agent teams")
        result_parts.append("- Can be used for enhanced analysis and recommendations")
        result_parts.append("- Supports data-driven decision making")
        
        return "\n".join(result_parts)
        
    except Exception as e:
        logger.error(f"Error getting document summary for {document_name}: {e}")
        return f"Error getting document summary: {e}"

@tool("search_document_content")
def search_document_content(document_name: str, search_terms: str) -> str:
    """
    Search for specific content within an uploaded document.
    
    Args:
        document_name: Name of the document to search
        search_terms: Terms to search for in the document
    
    Returns:
        Search results with context
    """
    try:
        documents = get_uploaded_documents()
        
        if document_name not in documents:
            return f"Document '{document_name}' not found. Available documents: {list(documents.keys())}"
        
        doc_data = documents[document_name]
        
        if 'error' in doc_data:
            return f"Error in document '{document_name}': {doc_data['error']}"
        
        result_parts = [f"**Search Results for: {document_name}**\n"]
        result_parts.append(f"Search Terms: \"{search_terms}\"\n")
        
        doc_type = doc_data.get('type', 'unknown')
        search_terms_lower = search_terms.lower()
        
        # Perform search based on document type
        if doc_type == 'structured':
            result_parts.append("**Structured Data Search Results:**")
            
            if 'sample_data' in doc_data and doc_data['sample_data']:
                sample_df = pd.DataFrame(doc_data['sample_data'])
                
                # Search in column names
                matching_cols = [col for col in sample_df.columns if search_terms_lower in col.lower()]
                if matching_cols:
                    result_parts.append(f"- Matching columns: {', '.join(matching_cols)}")
                
                # Search in data values
                matches = []
                for col in sample_df.columns:
                    col_matches = sample_df[col].astype(str).str.contains(search_terms_lower, case=False, na=False)
                    if col_matches.any():
                        matching_values = sample_df[col_matches][col].unique()[:3]
                        matches.extend([f"{col}: {', '.join(map(str, matching_values))}"])
                
                if matches:
                    result_parts.append("- Matching data values:")
                    for match in matches[:5]:  # Limit to 5 matches
                        result_parts.append(f"  - {match}")
        
        elif doc_type == 'semi_structured':
            result_parts.append("**Semi-structured Data Search Results:**")
            
            if 'sample_lines' in doc_data:
                matching_lines = []
                for i, line in enumerate(doc_data['sample_lines']):
                    if search_terms_lower in line.lower():
                        matching_lines.append(f"Line {i+1}: {line[:100]}...")
                
                if matching_lines:
                    result_parts.append(f"- Found {len(matching_lines)} matching lines:")
                    for line in matching_lines[:5]:  # Limit to 5 matches
                        result_parts.append(f"  - {line}")
                else:
                    result_parts.append("- No matching lines found in sample data")
        
        elif doc_type == 'unstructured':
            result_parts.append("**Unstructured Data Search Results:**")
            
            if 'sample_text' in doc_data:
                sample_text = doc_data['sample_text']
                text_lower = sample_text.lower()
                
                # Count occurrences
                count = text_lower.count(search_terms_lower)
                result_parts.append(f"- Found {count} occurrences of '{search_terms}'")
                
                # Find context around matches
                if count > 0:
                    result_parts.append("- Context around matches:")
                    start = 0
                    for i in range(min(3, count)):  # Show first 3 matches
                        pos = text_lower.find(search_terms_lower, start)
                        if pos != -1:
                            context_start = max(0, pos - 50)
                            context_end = min(len(sample_text), pos + len(search_terms) + 50)
                            context = sample_text[context_start:context_end]
                            result_parts.append(f"  - ...{context}...")
                            start = pos + 1
        
        result_parts.append("\n**Search Complete:**")
        result_parts.append("- Search performed successfully")
        result_parts.append("- Results based on available sample data")
        result_parts.append("- Use analyze_document_data for comprehensive analysis")
        
        return "\n".join(result_parts)
        
    except Exception as e:
        logger.error(f"Error searching document {document_name}: {e}")
        return f"Error searching document: {e}"

@tool("get_document_metadata")
def get_document_metadata(document_name: str) -> str:
    """
    Get metadata information about an uploaded document.
    
    Args:
        document_name: Name of the document to get metadata for
    
    Returns:
        Document metadata including file info, data characteristics, etc.
    """
    try:
        documents = get_uploaded_documents()
        
        if document_name not in documents:
            return f"Document '{document_name}' not found. Available documents: {list(documents.keys())}"
        
        doc_data = documents[document_name]
        
        if 'error' in doc_data:
            return f"Error in document '{document_name}': {doc_data['error']}"
        
        result_parts = [f"**Document Metadata for: {document_name}**\n"]
        
        # File information
        result_parts.append("**File Information:**")
        result_parts.append(f"- Filename: {document_name}")
        result_parts.append("- Upload Status: Successfully uploaded")
        result_parts.append("- Processing Status: Ready for analysis")
        
        # Document characteristics
        doc_type = doc_data.get('type', 'unknown')
        data_type = doc_data.get('data_type', 'unknown')
        result_parts.append(f"- Document Type: {doc_type}")
        result_parts.append(f"- Data Type: {data_type}")
        
        # Technical details
        result_parts.append("\n**Technical Details:**")
        
        metadata = doc_data.get('metadata', {})
        if 'file_size' in metadata:
            result_parts.append(f"- File Size: {metadata['file_size']:,} bytes")
        if 'file_type' in metadata:
            result_parts.append(f"- File Format: {metadata['file_type']}")
        
        # Data-specific metadata
        if doc_type == 'structured':
            if 'shape' in doc_data:
                rows, cols = doc_data['shape']
                result_parts.append(f"- Data Dimensions: {rows:,} rows × {cols} columns")
            if 'columns' in doc_data:
                result_parts.append(f"- Column Count: {len(doc_data['columns'])}")
        
        elif doc_type == 'semi_structured':
            if 'line_count' in doc_data:
                result_parts.append(f"- Line Count: {doc_data['line_count']:,}")
            if 'word_count' in doc_data:
                result_parts.append(f"- Word Count: {doc_data['word_count']:,}")
        
        elif doc_type == 'unstructured':
            if 'word_count' in doc_data:
                result_parts.append(f"- Word Count: {doc_data['word_count']:,}")
            if 'page_count' in doc_data:
                result_parts.append(f"- Page Count: {doc_data['page_count']}")
        
        # Access information
        result_parts.append("\n**Access Information:**")
        result_parts.append("- Available to: All agent teams")
        result_parts.append("- Access level: Full read access")
        result_parts.append("- Operations: Analysis, querying, searching")
        
        return "\n".join(result_parts)
        
    except Exception as e:
        logger.error(f"Error getting metadata for {document_name}: {e}")
        return f"Error getting metadata: {e}"

@tool("compare_documents")
def compare_documents(document1_name: str, document2_name: str, comparison_type: str = "basic") -> str:
    """
    Compare two uploaded documents to identify similarities and differences.
    
    Args:
        document1_name: Name of the first document to compare
        document2_name: Name of the second document to compare
        comparison_type: Type of comparison (basic, detailed, structural)
    
    Returns:
        Comparison results and analysis
    """
    try:
        documents = get_uploaded_documents()
        
        if document1_name not in documents:
            return f"Document '{document1_name}' not found. Available documents: {list(documents.keys())}"
        
        if document2_name not in documents:
            return f"Document '{document2_name}' not found. Available documents: {list(documents.keys())}"
        
        doc1_data = documents[document1_name]
        doc2_data = documents[document2_name]
        
        if 'error' in doc1_data:
            return f"Error in document '{document1_name}': {doc1_data['error']}"
        
        if 'error' in doc2_data:
            return f"Error in document '{document2_name}': {doc2_data['error']}"
        
        result_parts = ["**Document Comparison Results**\n"]
        result_parts.append(f"**Documents Compared:**")
        result_parts.append(f"- Document 1: {document1_name}")
        result_parts.append(f"- Document 2: {document2_name}")
        result_parts.append(f"- Comparison Type: {comparison_type}\n")
        
        # Basic comparison
        doc1_type = doc1_data.get('type', 'unknown')
        doc2_type = doc2_data.get('type', 'unknown')
        
        result_parts.append("**Document Types:**")
        result_parts.append(f"- {document1_name}: {doc1_type}")
        result_parts.append(f"- {document2_name}: {doc2_type}")
        result_parts.append(f"- Type Match: {'Yes' if doc1_type == doc2_type else 'No'}\n")
        
        # Size comparison
        result_parts.append("**Size Comparison:**")
        
        if doc1_type == 'structured' and 'shape' in doc1_data:
            rows1, cols1 = doc1_data['shape']
            result_parts.append(f"- {document1_name}: {rows1:,} rows × {cols1} columns")
        
        if doc2_type == 'structured' and 'shape' in doc2_data:
            rows2, cols2 = doc2_data['shape']
            result_parts.append(f"- {document2_name}: {rows2:,} rows × {cols2} columns")
        
        if doc1_type == 'semi_structured' and 'line_count' in doc1_data:
            result_parts.append(f"- {document1_name}: {doc1_data['line_count']:,} lines")
        
        if doc2_type == 'semi_structured' and 'line_count' in doc2_data:
            result_parts.append(f"- {document2_name}: {doc2_data['line_count']:,} lines")
        
        if doc1_type == 'unstructured' and 'word_count' in doc1_data:
            result_parts.append(f"- {document1_name}: {doc1_data['word_count']:,} words")
        
        if doc2_type == 'unstructured' and 'word_count' in doc2_data:
            result_parts.append(f"- {document2_name}: {doc2_data['word_count']:,} words")
        
        # Column comparison for structured data
        if doc1_type == 'structured' and doc2_type == 'structured':
            result_parts.append("\n**Column Comparison:**")
            
            cols1 = set(doc1_data.get('columns', []))
            cols2 = set(doc2_data.get('columns', []))
            
            common_cols = cols1.intersection(cols2)
            unique_to_doc1 = cols1 - cols2
            unique_to_doc2 = cols2 - cols1
            
            result_parts.append(f"- Common columns: {len(common_cols)}")
            if common_cols:
                result_parts.append(f"  - {', '.join(list(common_cols)[:5])}{'...' if len(common_cols) > 5 else ''}")
            
            result_parts.append(f"- Unique to {document1_name}: {len(unique_to_doc1)}")
            if unique_to_doc1:
                result_parts.append(f"  - {', '.join(list(unique_to_doc1)[:3])}{'...' if len(unique_to_doc1) > 3 else ''}")
            
            result_parts.append(f"- Unique to {document2_name}: {len(unique_to_doc2)}")
            if unique_to_doc2:
                result_parts.append(f"  - {', '.join(list(unique_to_doc2)[:3])}{'...' if len(unique_to_doc2) > 3 else ''}")
        
        result_parts.append("\n**Comparison Complete:**")
        result_parts.append("- Documents successfully compared")
        result_parts.append("- Analysis based on available metadata")
        result_parts.append("- Use analyze_document_data for detailed analysis")
        
        return "\n".join(result_parts)
        
    except Exception as e:
        logger.error(f"Error comparing documents {document1_name} and {document2_name}: {e}")
        return f"Error comparing documents: {e}"

@tool("extract_document_insights")
def extract_document_insights(document_name: str, insight_type: str = "general") -> str:
    """
    Extract specific insights from an uploaded document.
    
    Args:
        document_name: Name of the document to extract insights from
        insight_type: Type of insights to extract (general, trends, patterns, anomalies)
    
    Returns:
        Extracted insights and recommendations
    """
    try:
        documents = get_uploaded_documents()
        
        if document_name not in documents:
            return f"Document '{document_name}' not found. Available documents: {list(documents.keys())}"
        
        doc_data = documents[document_name]
        
        if 'error' in doc_data:
            return f"Error in document '{document_name}': {doc_data['error']}"
        
        result_parts = [f"**Document Insights for: {document_name}**\n"]
        
        insight_types = {
            "general": "General insights and observations",
            "trends": "Trend analysis and patterns",
            "patterns": "Pattern recognition and analysis",
            "anomalies": "Anomaly detection and outliers"
        }
        
        result_parts.append(f"**Insight Type: {insight_type}**")
        result_parts.append(f"Description: {insight_types.get(insight_type, 'Custom insights')}\n")
        
        doc_type = doc_data.get('type', 'unknown')
        
        # Extract insights based on document type and insight type
        if doc_type == 'structured':
            result_parts.append("**Structured Data Insights:**")
            
            if 'sample_data' in doc_data and doc_data['sample_data']:
                sample_df = pd.DataFrame(doc_data['sample_data'])
                
                if insight_type in ['general', 'patterns']:
                    # Data quality insights
                    null_counts = sample_df.isnull().sum()
                    if null_counts.any():
                        result_parts.append(f"- Missing values detected in {null_counts.sum()} cells")
                        for col, count in null_counts[null_counts > 0].items():
                            result_parts.append(f"  - {col}: {count} missing values")
                    else:
                        result_parts.append("- No missing values detected")
                
                if insight_type in ['trends', 'patterns']:
                    # Numeric column insights
                    numeric_cols = sample_df.select_dtypes(include=['number']).columns
                    if len(numeric_cols) > 0:
                        result_parts.append(f"- Numeric columns analyzed: {', '.join(numeric_cols)}")
                        for col in numeric_cols[:3]:
                            stats = sample_df[col].describe()
                            result_parts.append(f"  - {col}: range {stats['min']:.2f} to {stats['max']:.2f}, mean {stats['mean']:.2f}")
                
                if insight_type == 'anomalies':
                    # Anomaly detection
                    numeric_cols = sample_df.select_dtypes(include=['number']).columns
                    if len(numeric_cols) > 0:
                        result_parts.append("- Potential anomalies detected:")
                        for col in numeric_cols[:2]:
                            Q1 = sample_df[col].quantile(0.25)
                            Q3 = sample_df[col].quantile(0.75)
                            IQR = Q3 - Q1
                            outliers = sample_df[(sample_df[col] < Q1 - 1.5*IQR) | (sample_df[col] > Q3 + 1.5*IQR)]
                            if len(outliers) > 0:
                                result_parts.append(f"  - {col}: {len(outliers)} potential outliers")
        
        elif doc_type == 'semi_structured':
            result_parts.append("**Semi-structured Data Insights:**")
            
            if insight_type in ['general', 'patterns']:
                if 'line_count' in doc_data:
                    result_parts.append(f"- Document contains {doc_data['line_count']:,} lines")
                
                if 'headers' in doc_data:
                    result_parts.append(f"- Found {len(doc_data['headers'])} headers")
                    result_parts.append(f"- Header structure: {', '.join(doc_data['headers'][:3])}{'...' if len(doc_data['headers']) > 3 else ''}")
        
        elif doc_type == 'unstructured':
            result_parts.append("**Unstructured Data Insights:**")
            
            if insight_type in ['general', 'patterns']:
                if 'word_count' in doc_data:
                    result_parts.append(f"- Document contains {doc_data['word_count']:,} words")
                
                if 'page_count' in doc_data:
                    result_parts.append(f"- Document spans {doc_data['page_count']} pages")
                
                if 'sample_text' in doc_data:
                    sample_text = doc_data['sample_text']
                    # Basic text analysis
                    sentences = sample_text.count('.') + sample_text.count('!') + sample_text.count('?')
                    result_parts.append(f"- Estimated sentences: {sentences}")
                    
                    # Word frequency analysis
                    words = sample_text.lower().split()
                    word_freq = {}
                    for word in words:
                        word = word.strip('.,!?;:"()[]{}')
                        if len(word) > 3:  # Only count words longer than 3 characters
                            word_freq[word] = word_freq.get(word, 0) + 1
                    
                    if word_freq:
                        top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:5]
                        result_parts.append("- Most frequent words:")
                        for word, count in top_words:
                            result_parts.append(f"  - {word}: {count} times")
        
        result_parts.append("\n**Insights Summary:**")
        result_parts.append("- Document successfully analyzed")
        result_parts.append("- Insights extracted based on available data")
        result_parts.append("- Ready for decision-making support")
        
        result_parts.append("\n**Recommendations:**")
        result_parts.append("- Use these insights to inform analysis")
        result_parts.append("- Combine with other document analyses")
        result_parts.append("- Apply to Digital Twin recommendations")
        
        return "\n".join(result_parts)
        
    except Exception as e:
        logger.error(f"Error extracting insights from {document_name}: {e}")
        return f"Error extracting insights: {e}"

@tool("search_documents_semantically")
def search_documents_semantically(query: str, n_results: int = 5, file_types: Optional[List[str]] = None) -> str:
    """
    Search through all uploaded documents using semantic similarity.
    This tool uses vector embeddings to find relevant content even when exact keywords don't match.
    
    Args:
        query: Natural language query to search for
        n_results: Number of results to return (default: 5)
        file_types: Optional filter by file types (e.g., ['csv', 'pdf', 'docx'])
    
    Returns:
        Semantic search results with relevant document chunks
    """
    try:
        result_parts = [f"**Semantic Search Results**\n"]
        result_parts.append(f"Query: \"{query}\"\n")
        
        # Perform semantic search
        search_results = search_documents_in_memory(query, n_results, file_types)
        
        if not search_results:
            return "No relevant documents found for your query. Try different search terms or check if documents have been uploaded."
        
        result_parts.append(f"Found {len(search_results)} relevant document chunks:\n")
        
        for i, result in enumerate(search_results, 1):
            metadata = result['metadata']
            content = result['content']
            distance = result.get('distance', 0)
            
            # Calculate relevance score (lower distance = higher relevance)
            relevance_score = max(0, 100 - (distance * 100)) if distance else 100
            
            result_parts.append(f"**Result {i}** (Relevance: {relevance_score:.1f}%)")
            result_parts.append(f"- Document: {metadata.get('filename', 'Unknown')}")
            result_parts.append(f"- File Type: {metadata.get('file_type', 'Unknown')}")
            result_parts.append(f"- Chunk: {metadata.get('chunk_index', 0) + 1}/{metadata.get('total_chunks', 1)}")
            result_parts.append(f"- Content Preview: {content[:200]}...")
            result_parts.append("")
        
        result_parts.append("**Search Tips:**")
        result_parts.append("- Use natural language queries (e.g., 'financial data', 'customer information')")
        result_parts.append("- Try different keywords if results are not relevant")
        result_parts.append("- Use file_types parameter to filter by document type")
        result_parts.append("- Higher relevance scores indicate better matches")
        
        return "\n".join(result_parts)
        
    except Exception as e:
        logger.error(f"Error performing semantic search: {e}")
        return f"Error performing semantic search: {e}"

@tool("get_document_from_memory")
def get_document_from_memory_tool(document_id: str) -> str:
    """
    Retrieve a complete document from memory using its document ID.
    
    Args:
        document_id: The document ID to retrieve
    
    Returns:
        Complete document content with all chunks
    """
    try:
        result_parts = [f"**Document Retrieval: {document_id}**\n"]
        
        # Get document chunks
        chunks = get_document_from_memory(document_id)
        
        if not chunks:
            return f"Document with ID '{document_id}' not found in memory."
        
        # Get metadata from first chunk
        metadata = chunks[0]['metadata']
        result_parts.append(f"**Document Information:**")
        result_parts.append(f"- Filename: {metadata.get('filename', 'Unknown')}")
        result_parts.append(f"- File Type: {metadata.get('file_type', 'Unknown')}")
        result_parts.append(f"- Total Chunks: {len(chunks)}")
        result_parts.append("")
        
        # Combine all chunks
        full_content = " ".join([chunk['content'] for chunk in chunks])
        result_parts.append(f"**Complete Document Content:**\n{full_content}")
        
        return "\n".join(result_parts)
        
    except Exception as e:
        logger.error(f"Error retrieving document {document_id}: {e}")
        return f"Error retrieving document: {e}"

@tool("list_documents_in_memory")
def list_documents_in_memory_tool() -> str:
    """
    List all documents stored in semantic memory.
    
    Returns:
        List of all documents with their metadata
    """
    try:
        result_parts = ["**Documents in Semantic Memory**\n"]
        
        # Get all documents
        documents = list_documents_in_memory()
        
        if not documents:
            return "No documents are currently stored in semantic memory."
        
        result_parts.append(f"Total documents: {len(documents)}\n")
        
        for i, doc in enumerate(documents, 1):
            result_parts.append(f"**Document {i}:**")
            result_parts.append(f"- ID: {doc['document_id']}")
            result_parts.append(f"- Filename: {doc['filename']}")
            result_parts.append(f"- File Type: {doc['file_type']}")
            result_parts.append(f"- Chunks: {doc['total_chunks']}")
            result_parts.append("")
        
        result_parts.append("**Memory Usage:**")
        result_parts.append("- Documents are stored in ChromaDB for semantic search")
        result_parts.append("- Each document is split into chunks for better search")
        result_parts.append("- Use search_documents_semantically to find relevant content")
        
        return "\n".join(result_parts)
        
    except Exception as e:
        logger.error(f"Error listing documents in memory: {e}")
        return f"Error listing documents: {e}"
