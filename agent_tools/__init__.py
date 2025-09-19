"""
Agent Tools Package

This package contains all the tools used by the CrewAI agents in the multi-agent workflow.
Each tool is organized in its own module for better maintainability and reusability.
"""

from .search_tool import search_web
from .analysis_tool import AnalysisTool
from .pdf_writer import create_pdf_report, AcademicPDFWriter
from .document_processor import DocumentProcessor
from .data_analysis_tool import DataAnalysisTool
from .document_access_tool import (
    access_uploaded_documents,
    analyze_document_data,
    query_document_data,
    get_document_summary,
    search_document_content,
    get_document_metadata,
    compare_documents,
    extract_document_insights,
    search_documents_semantically,
    get_document_from_memory_tool,
    list_documents_in_memory_tool
)
from .research_validation_tool import (
    validate_research_source,
    add_harvard_citation,
    create_harvard_reference,
    validate_all_references,
    generate_reference_list_tool,
    fact_check_claim,
    check_academic_integrity
)
from .iso19115_metadata_tool import (
    create_iso19115_metadata,
    validate_iso19115_metadata,
    extract_geospatial_metadata
)

__all__ = [
    'search_web',
    'AnalysisTool',
    'create_pdf_report',
    'AcademicPDFWriter',
    'DocumentProcessor',
    'DataAnalysisTool',
    'access_uploaded_documents',
    'analyze_document_data',
    'query_document_data',
    'get_document_summary',
    'search_document_content',
    'get_document_metadata',
    'compare_documents',
    'extract_document_insights',
    'search_documents_semantically',
    'get_document_from_memory_tool',
    'list_documents_in_memory_tool',
    'validate_research_source',
    'add_harvard_citation',
    'create_harvard_reference',
    'validate_all_references',
    'generate_reference_list_tool',
    'fact_check_claim',
    'check_academic_integrity',
    'create_iso19115_metadata',
    'validate_iso19115_metadata',
    'extract_geospatial_metadata'
]
