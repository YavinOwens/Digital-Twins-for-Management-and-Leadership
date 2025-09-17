"""
Agent Tools Package

This package contains all the tools used by the CrewAI agents in the multi-agent workflow.
Each tool is organized in its own module for better maintainability and reusability.
"""

from .search_tool import search_web
from .analysis_tool import AnalysisTool
from .pdf_writer import create_pdf_report, AcademicPDFWriter

__all__ = ['search_web', 'AnalysisTool', 'create_pdf_report', 'AcademicPDFWriter']
