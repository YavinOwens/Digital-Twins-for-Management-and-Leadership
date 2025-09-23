"""
Documents Page - Document Management and Analysis

This page handles document upload, processing, and management for the Digital Twins system.
"""

import streamlit as st
import os
from pathlib import Path
from shared.components import create_header, create_footer, create_sidebar_info
from shared.utils import get_document_memory_stats
from agent_tools.document_processor import DocumentProcessor
from agent_tools.document_memory_manager import (
    store_document_in_memory,
    search_documents_in_memory,
    list_documents_in_memory,
    delete_document_from_memory
)
from ui_components.document_upload import DocumentUploadUI

def main():
    """Main function for the Documents page"""
    
    # Page configuration
    st.set_page_config(
        page_title="Digital Twins Management System - Documents",
        page_icon="📁",
        layout="wide"
    )
    
    # Create header
    create_header("Document Management & Analysis", "📁")
    
    # Initialize document processor
    doc_processor = DocumentProcessor()
    
    # Sidebar
    with st.sidebar:
        create_sidebar_info()
        
        st.header("📊 Document Statistics")
        try:
            doc_stats = get_document_memory_stats()
            st.metric("Total Documents", doc_stats.get("total_documents", 0))
            st.metric("Total Chunks", doc_stats.get("total_chunks", 0))
        except Exception as e:
            st.warning(f"Unable to load document stats: {e}")
        
        st.header("🔍 Document Search")
        search_query = st.text_input("Search documents:", placeholder="Enter search terms...")
        if search_query:
            try:
                search_results = search_documents_in_memory(search_query, n_results=5)
                if search_results:
                    st.write("**Search Results:**")
                    for i, result in enumerate(search_results, 1):
                        with st.expander(f"Result {i}: {result['metadata'].get('filename', 'Unknown')}"):
                            st.write(f"**Content:** {result['content'][:200]}...")
                            st.write(f"**File Type:** {result['metadata'].get('file_type', 'Unknown')}")
                            st.write(f"**Chunk:** {result['metadata'].get('chunk_index', 0)}/{result['metadata'].get('total_chunks', 0)}")
                else:
                    st.info("No documents found matching your search.")
            except Exception as e:
                st.error(f"Search failed: {e}")
    
    # Main content
    st.markdown("## 📁 Document Management & Analysis")
    
    # Document upload section
    st.markdown("### 📤 Upload Documents")
    st.write("Upload documents and datasets to enhance the Digital Twin analysis with real organizational data.")
    
    # Initialize document upload UI
    doc_upload_ui = DocumentUploadUI()
    
    # Create document upload section
    uploaded_documents = doc_upload_ui.create_file_upload_section()
    
    # Process uploaded documents
    if uploaded_documents:
        st.success(f"✅ Successfully uploaded {len(uploaded_documents)} documents!")
        
        # Process each document
        for doc_name, doc_data in uploaded_documents.items():
            with st.expander(f"Processing: {doc_name}", expanded=True):
                try:
                    # Process the document
                    processed_data = doc_processor.process_uploaded_file(uploaded_documents[doc_name])
                    
                    if 'error' in processed_data:
                        st.error(f"❌ Error processing {doc_name}: {processed_data['error']}")
                        continue
                    
                    # Store in memory
                    doc_id = store_document_in_memory(processed_data)
                    st.success(f"✅ Document stored with ID: {doc_id}")
                    
                    # Show document summary
                    st.write("**Document Summary:**")
                    st.write(f"- Type: {processed_data.get('type', 'Unknown')}")
                    st.write(f"- Data Type: {processed_data.get('data_type', 'Unknown')}")
                    
                    if processed_data.get('type') == 'structured':
                        if 'shape' in processed_data:
                            st.write(f"- Dimensions: {processed_data['shape']}")
                        if 'columns' in processed_data:
                            st.write(f"- Columns: {', '.join(processed_data['columns'][:5])}{'...' if len(processed_data['columns']) > 5 else ''}")
                    
                    elif processed_data.get('type') == 'unstructured':
                        if 'word_count' in processed_data:
                            st.write(f"- Words: {processed_data['word_count']:,}")
                        if 'page_count' in processed_data:
                            st.write(f"- Pages: {processed_data['page_count']}")
                    
                except Exception as e:
                    st.error(f"❌ Error processing {doc_name}: {e}")
    
    # Document management section
    st.markdown("### 📋 Document Management")
    doc_upload_ui.create_document_management_section()
    
    # List stored documents
    st.markdown("### 📚 Stored Documents")
    
    try:
        stored_docs = list_documents_in_memory()
        
        if stored_docs:
            st.write(f"Found {len(stored_docs)} documents in memory:")
            
            for doc in stored_docs:
                with st.expander(f"📄 {doc['filename']} ({doc['file_type']})"):
                    col1, col2, col3 = st.columns([2, 1, 1])
                    
                    with col1:
                        st.write(f"**Document ID:** {doc['document_id']}")
                        st.write(f"**File Type:** {doc['file_type']}")
                        st.write(f"**Total Chunks:** {doc['total_chunks']}")
                    
                    with col2:
                        if st.button("🔍 Search", key=f"search_{doc['document_id']}"):
                            search_query = st.text_input("Search in this document:", key=f"search_input_{doc['document_id']}")
                            if search_query:
                                results = search_documents_in_memory(search_query, n_results=3)
                                for result in results:
                                    if result['metadata'].get('document_id') == doc['document_id']:
                                        st.write(f"**Chunk {result['metadata'].get('chunk_index', 0)}:** {result['content'][:100]}...")
                    
                    with col3:
                        if st.button("🗑️ Delete", key=f"delete_{doc['document_id']}"):
                            if delete_document_from_memory(doc['document_id']):
                                st.success("Document deleted successfully!")
                                st.rerun()
                            else:
                                st.error("Failed to delete document.")
        else:
            st.info("No documents stored in memory yet. Upload some documents to get started!")
    
    except Exception as e:
        st.error(f"Error loading stored documents: {e}")
    
    # Document analysis tools
    st.markdown("### 🔧 Document Analysis Tools")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Analyze All Documents", use_container_width=True):
            st.info("Document analysis feature coming soon!")
    
    with col2:
        if st.button("🔍 Semantic Search", use_container_width=True):
            st.info("Semantic search feature coming soon!")
    
    with col3:
        if st.button("📈 Generate Insights", use_container_width=True):
            st.info("Insights generation feature coming soon!")
    
    # Create footer
    create_footer()

if __name__ == "__main__":
    main()
