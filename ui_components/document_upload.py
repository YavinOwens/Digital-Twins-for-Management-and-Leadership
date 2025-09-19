"""
Document Upload UI Component for Digital Twins Management System

This module provides Streamlit UI components for file upload and document management.
"""

import streamlit as st
import pandas as pd
from typing import Dict, List, Any, Optional
from pathlib import Path
import json
from agent_tools.document_processor import DocumentProcessor
from agent_tools.document_memory_manager import store_document_in_memory, get_document_memory_stats

class DocumentUploadUI:
    """
    UI component for document upload and management
    """
    
    def __init__(self, upload_dir: str = "./uploads"):
        self.processor = DocumentProcessor(upload_dir)
        self.upload_dir = Path(upload_dir)
        self.upload_dir.mkdir(exist_ok=True)
        self._key_counter = 0  # Counter for unique key generation
    
    def _generate_unique_key(self, prefix: str, doc_name: str = None) -> str:
        """
        Generate a unique key for Streamlit elements
        """
        self._key_counter += 1
        if doc_name:
            # Use doc_name and counter for uniqueness
            safe_name = doc_name.replace(' ', '_').replace('.', '_').replace('/', '_')
            return f"{prefix}_{safe_name}_{self._key_counter}"
        else:
            return f"{prefix}_{self._key_counter}"
    
    def create_file_upload_section(self) -> Dict[str, Any]:
        """
        Create the file upload section UI
        """
        st.subheader("📁 Document Upload & Processing")
        
        # File upload options
        upload_option = st.radio(
            "Choose upload method:",
            ["Upload Files", "Upload Directory", "Connect to Database"],
            help="Select how you want to provide data to the Digital Twin system"
        )
        
        uploaded_data = {}
        
        if upload_option == "Upload Files":
            uploaded_data = self._handle_file_upload()
        elif upload_option == "Upload Directory":
            uploaded_data = self._handle_directory_upload()
        elif upload_option == "Connect to Database":
            uploaded_data = self._handle_database_connection()
        
        return uploaded_data
    
    def _handle_file_upload(self) -> Dict[str, Any]:
        """
        Handle individual file uploads
        """
        st.write("**Upload multiple files:**")
        
        # Supported file types
        supported_types = [
            "csv", "xlsx", "xls", "json", "xml", "yaml", "yml",
            "txt", "md", "log", "tsv", "pdf", "docx", "doc", "rtf",
            "sqlite", "db", "zip", "tar", "gz"
        ]
        
        uploaded_files = st.file_uploader(
            "Choose files to upload",
            type=supported_types,
            accept_multiple_files=True,
            help="Upload various document types including databases, spreadsheets, text files, and archives"
        )
        
        if uploaded_files:
            st.write(f"**Uploaded {len(uploaded_files)} files:**")
            
            # Process files
            processed_files = {}
            progress_bar = st.progress(0)
            
            for i, uploaded_file in enumerate(uploaded_files):
                with st.expander(f"📄 {uploaded_file.name}"):
                    try:
                        # Process file
                        result = self.processor.process_uploaded_file(uploaded_file)
                        processed_files[uploaded_file.name] = result
                        
                        # Display file info
                        self._display_file_info(result)
                        
                        # Display preview
                        self._display_file_preview(result)
                        
                    except Exception as e:
                        st.error(f"Error processing {uploaded_file.name}: {e}")
                        processed_files[uploaded_file.name] = {'error': str(e)}
                
                progress_bar.progress((i + 1) / len(uploaded_files))
            
            st.success(f"Successfully processed {len(processed_files)} files!")
            return processed_files
        
        return {}
    
    def _handle_directory_upload(self) -> Dict[str, Any]:
        """
        Handle directory upload
        """
        st.write("**Upload a directory:**")
        
        # Directory path input
        directory_path = st.text_input(
            "Enter directory path:",
            placeholder="/path/to/your/documents",
            help="Enter the full path to a directory containing documents"
        )
        
        if directory_path and Path(directory_path).exists():
            if st.button("Process Directory"):
                with st.spinner("Processing directory..."):
                    try:
                        processed_files = self.processor.process_directory(directory_path)
                        
                        st.write(f"**Processed {len(processed_files)} files from directory:**")
                        
                        # Display summary
                        self._display_directory_summary(processed_files)
                        
                        return processed_files
                        
                    except Exception as e:
                        st.error(f"Error processing directory: {e}")
                        return {'error': str(e)}
        elif directory_path and not Path(directory_path).exists():
            st.error("Directory does not exist. Please check the path.")
        
        return {}
    
    def _handle_database_connection(self) -> Dict[str, Any]:
        """
        Handle database connection
        """
        st.write("**Connect to a database:**")
        
        # Database type selection
        db_type = st.selectbox(
            "Database type:",
            ["SQLite", "PostgreSQL", "MySQL", "SQL Server", "Oracle"],
            help="Select the type of database you want to connect to"
        )
        
        if db_type == "SQLite":
            return self._handle_sqlite_connection()
        else:
            st.info(f"Database connection for {db_type} will be implemented in future versions.")
            return {}
    
    def _handle_sqlite_connection(self) -> Dict[str, Any]:
        """
        Handle SQLite database connection
        """
        st.write("**SQLite Database Connection:**")
        
        # Database file upload
        db_file = st.file_uploader(
            "Upload SQLite database file:",
            type=["sqlite", "db"],
            help="Upload a SQLite database file (.sqlite or .db)"
        )
        
        if db_file:
            try:
                # Save and process database
                db_path = self.upload_dir / db_file.name
                with open(db_path, "wb") as f:
                    f.write(db_file.getbuffer())
                
                result = self.processor._process_sqlite(db_path)
                
                # Display database info
                self._display_database_info(result)
                
                return {db_file.name: result}
                
            except Exception as e:
                st.error(f"Error processing database: {e}")
                return {'error': str(e)}
        
        return {}
    
    def _display_file_info(self, result: Dict[str, Any]) -> None:
        """
        Display file information
        """
        if 'error' in result:
            st.error(f"Error: {result['error']}")
            return
        
        metadata = result.get('metadata', {})
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("File Size", f"{metadata.get('file_size', 0):,} bytes")
        
        with col2:
            st.metric("File Type", metadata.get('file_type', 'Unknown'))
        
        with col3:
            st.metric("Data Type", result.get('data_type', 'Unknown'))
        
        # Additional info based on data type
        if result.get('type') == 'structured':
            if 'shape' in result:
                st.info(f"Dimensions: {result['shape']}")
            if 'columns' in result:
                st.info(f"Columns: {', '.join(result['columns'])}")
        
        elif result.get('type') == 'semi_structured':
            if 'line_count' in result:
                st.info(f"Lines: {result['line_count']}")
            if 'word_count' in result:
                st.info(f"Words: {result['word_count']}")
        
        elif result.get('type') == 'unstructured':
            if 'word_count' in result:
                st.info(f"Words: {result['word_count']}")
            if 'page_count' in result:
                st.info(f"Pages: {result['page_count']}")
    
    def _display_file_preview(self, result: Dict[str, Any]) -> None:
        """
        Display file preview
        """
        if 'error' in result:
            return
        
        # Show preview based on data type
        if result.get('type') == 'structured':
            if 'sample_data' in result and result['sample_data']:
                st.write("**Data Preview:**")
                df = pd.DataFrame(result['sample_data'])
                # Generate unique key for dataframe
                doc_name = result.get('metadata', {}).get('filename', 'unknown')
                unique_key = self._generate_unique_key("dataframe", doc_name)
                st.dataframe(df, use_container_width=True, key=unique_key)
            
            elif 'sheets' in result:
                st.write("**Sheets Preview:**")
                # Get doc_name for unique key generation
                doc_name = result.get('metadata', {}).get('filename', 'unknown')
                for sheet_name, sheet_data in result['sheets'].items():
                    with st.expander(f"Sheet: {sheet_name}"):
                        if 'sample_data' in sheet_data and sheet_data['sample_data']:
                            df = pd.DataFrame(sheet_data['sample_data'])
                            # Generate unique key for sheet dataframe
                            sheet_key = self._generate_unique_key(f"sheet_{sheet_name}", doc_name)
                            st.dataframe(df, use_container_width=True, key=sheet_key)
        
        elif result.get('type') == 'semi_structured':
            if 'sample_lines' in result:
                st.write("**Content Preview:**")
                for line in result['sample_lines'][:10]:  # First 10 lines
                    st.text(line)
        
        elif result.get('type') == 'unstructured':
            if 'sample_text' in result:
                st.write("**Content Preview:**")
                # Generate unique key based on document metadata
                doc_name = result.get('metadata', {}).get('filename', 'unknown')
                unique_key = self._generate_unique_key("preview_text", doc_name)
                st.text_area("", result['sample_text'], height=200, disabled=True, key=unique_key)
    
    def _display_database_info(self, result: Dict[str, Any]) -> None:
        """
        Display database information
        """
        if 'error' in result:
            st.error(f"Error: {result['error']}")
            return
        
        st.write("**Database Information:**")
        
        if 'tables' in result:
            st.write(f"**Tables: {len(result['tables'])}**")
            
            for table_name, table_data in result['tables'].items():
                with st.expander(f"Table: {table_name}"):
                    st.write(f"Rows: {table_data.get('row_count', 0):,}")
                    st.write(f"Columns: {len(table_data.get('columns', []))}")
                    
                    # Show column info
                    if 'columns' in table_data:
                        col_df = pd.DataFrame(table_data['columns'])
                        # Generate unique key for column dataframe
                        col_key = self._generate_unique_key(f"table_cols_{table_name}")
                        st.dataframe(col_df, use_container_width=True, key=col_key)
                    
                    # Show sample data
                    if 'sample_data' in table_data and table_data['sample_data']:
                        st.write("**Sample Data:**")
                        df = pd.DataFrame(table_data['sample_data'])
                        # Generate unique key for sample data dataframe
                        sample_key = self._generate_unique_key(f"table_sample_{table_name}")
                        st.dataframe(df, use_container_width=True, key=sample_key)
    
    def _display_directory_summary(self, processed_files: Dict[str, Any]) -> None:
        """
        Display directory processing summary
        """
        if not processed_files:
            return
        
        # Count by type
        type_counts = {}
        error_count = 0
        
        for file_path, result in processed_files.items():
            if 'error' in result:
                error_count += 1
            else:
                data_type = result.get('data_type', 'unknown')
                type_counts[data_type] = type_counts.get(data_type, 0) + 1
        
        # Display summary
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Files", len(processed_files))
        
        with col2:
            st.metric("Successful", len(processed_files) - error_count)
        
        with col3:
            st.metric("Errors", error_count)
        
        # File type breakdown
        if type_counts:
            st.write("**File Types:**")
            type_df = pd.DataFrame(list(type_counts.items()), columns=['Type', 'Count'])
            st.dataframe(type_df, use_container_width=True, key="file_type_breakdown")
    
    def create_document_management_section(self) -> None:
        """
        Create document management section
        """
        st.subheader("📚 Document Management")
        
        # Show uploaded documents
        if 'uploaded_documents' in st.session_state:
            documents = st.session_state.uploaded_documents
            
            st.write(f"**Available Documents: {len(documents)}**")
            
            # Document list
            for doc_name, doc_data in documents.items():
                with st.expander(f"📄 {doc_name}"):
                    self._display_file_info(doc_data)
                    
                    # Action buttons
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        if st.button(f"View Details", key=f"view_{doc_name}"):
                            st.session_state[f"show_details_{doc_name}"] = True
                    
                    with col2:
                        if st.button(f"Download", key=f"download_{doc_name}"):
                            # Implement download functionality
                            st.info("Download functionality will be implemented")
                    
                    with col3:
                        if st.button(f"Remove", key=f"remove_{doc_name}"):
                            del st.session_state.uploaded_documents[doc_name]
                            st.rerun()
                    
                    # Show details if requested
                    if st.session_state.get(f"show_details_{doc_name}", False):
                        self._display_file_preview(doc_data)
                        if st.button(f"Hide Details", key=f"hide_{doc_name}"):
                            st.session_state[f"show_details_{doc_name}"] = False
                            st.rerun()
        else:
            st.info("No documents uploaded yet. Use the upload section above to add documents.")
    
    def get_agent_context(self, documents: Dict[str, Any]) -> str:
        """
        Generate context for agents from uploaded documents
        """
        if not documents:
            return "No documents available for analysis."
        
        context_parts = ["**Available Documents for Analysis:**\n"]
        
        for doc_name, doc_data in documents.items():
            if 'error' in doc_data:
                context_parts.append(f"- {doc_name}: Error - {doc_data['error']}")
                continue
            
            summary = self.processor.get_processed_data_summary(doc_data)
            context_parts.append(f"- {doc_name}: {summary}")
            
            # Add specific data insights
            if doc_data.get('type') == 'structured':
                if 'columns' in doc_data:
                    context_parts.append(f"  - Columns: {', '.join(doc_data['columns'])}")
                if 'shape' in doc_data:
                    context_parts.append(f"  - Data points: {doc_data['shape'][0]:,} rows, {doc_data['shape'][1]} columns")
            
            elif doc_data.get('type') == 'semi_structured':
                if 'line_count' in doc_data:
                    context_parts.append(f"  - Lines: {doc_data['line_count']:,}")
                if 'headers' in doc_data:
                    context_parts.append(f"  - Headers: {len(doc_data['headers'])}")
            
            elif doc_data.get('type') == 'unstructured':
                if 'word_count' in doc_data:
                    context_parts.append(f"  - Words: {doc_data['word_count']:,}")
                if 'page_count' in doc_data:
                    context_parts.append(f"  - Pages: {doc_data['page_count']}")
        
        return "\n".join(context_parts)
    
    def save_documents_to_session(self, documents: Dict[str, Any]) -> None:
        """
        Save documents to session state and store in memory for semantic search
        """
        if 'uploaded_documents' not in st.session_state:
            st.session_state.uploaded_documents = {}
        
        # Store in session state
        st.session_state.uploaded_documents.update(documents)
        
        # Store in memory for semantic search
        self._store_documents_in_memory(documents)
    
    def _store_documents_in_memory(self, documents: Dict[str, Any]) -> None:
        """
        Store documents in ChromaDB memory for semantic search
        """
        try:
            stored_count = 0
            for doc_name, doc_data in documents.items():
                if 'error' not in doc_data:
                    try:
                        # Store document in memory
                        doc_id = store_document_in_memory(doc_data)
                        st.session_state[f"doc_memory_id_{doc_name}"] = doc_id
                        stored_count += 1
                    except Exception as e:
                        st.warning(f"Could not store {doc_name} in memory: {e}")
            
            if stored_count > 0:
                st.success(f"✅ Stored {stored_count} documents in semantic memory!")
                
                # Show memory stats
                stats = get_document_memory_stats()
                if 'error' not in stats:
                    st.info(f"📊 Memory contains {stats.get('total_documents', 0)} documents with {stats.get('total_chunks', 0)} chunks")
                
        except Exception as e:
            st.error(f"Error storing documents in memory: {e}")
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """
        Get document memory statistics
        """
        return get_document_memory_stats()
