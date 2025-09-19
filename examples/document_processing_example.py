"""
Document Processing Example for Digital Twins Management System

This example demonstrates how agents can work with uploaded documents
in the Digital Twins system.
"""

import streamlit as st
import pandas as pd
from pathlib import Path
import json

# Import document processing tools
from agent_tools.document_processor import DocumentProcessor
from agent_tools.data_analysis_tool import DataAnalysisTool
from agent_tools.document_access_tool import (
    access_uploaded_documents,
    analyze_document_data,
    query_document_data,
    get_document_summary
)

def demonstrate_document_processing():
    """
    Demonstrate document processing capabilities
    """
    st.title("📁 Document Processing Demo")
    st.write("This demo shows how the Digital Twins system can process various document types.")
    
    # Initialize tools
    processor = DocumentProcessor()
    analyzer = DataAnalysisTool()
    
    # Create sample data for demonstration
    st.subheader("📊 Sample Data Processing")
    
    # Create sample CSV data
    sample_data = {
        'Employee_ID': [1, 2, 3, 4, 5],
        'Name': ['John Doe', 'Jane Smith', 'Bob Johnson', 'Alice Brown', 'Charlie Wilson'],
        'Department': ['IT', 'HR', 'Finance', 'IT', 'Marketing'],
        'Salary': [75000, 65000, 80000, 70000, 60000],
        'Years_Experience': [5, 3, 8, 4, 2]
    }
    
    df = pd.DataFrame(sample_data)
    st.write("**Sample Employee Data:**")
    st.dataframe(df)
    
    # Demonstrate analysis
    st.subheader("🔍 Data Analysis")
    
    # Basic statistics
    st.write("**Basic Statistics:**")
    st.write(df.describe())
    
    # Department analysis
    st.write("**Department Analysis:**")
    dept_analysis = df.groupby('Department').agg({
        'Salary': ['mean', 'count'],
        'Years_Experience': 'mean'
    }).round(2)
    st.write(dept_analysis)
    
    # Salary distribution
    st.write("**Salary Distribution:**")
    salary_stats = {
        'Mean Salary': f"${df['Salary'].mean():,.2f}",
        'Median Salary': f"${df['Salary'].median():,.2f}",
        'Min Salary': f"${df['Salary'].min():,.2f}",
        'Max Salary': f"${df['Salary'].max():,.2f}",
        'Standard Deviation': f"${df['Salary'].std():,.2f}"
    }
    
    for key, value in salary_stats.items():
        st.metric(key, value)
    
    # Correlation analysis
    st.write("**Correlation Analysis:**")
    correlation_matrix = df[['Salary', 'Years_Experience']].corr()
    st.write(correlation_matrix)
    
    # Insights
    st.subheader("💡 Key Insights")
    
    insights = [
        "IT department has the highest average salary",
        "Strong positive correlation between years of experience and salary",
        "Marketing department has the lowest average salary",
        "Salary range shows good distribution across departments"
    ]
    
    for i, insight in enumerate(insights, 1):
        st.write(f"{i}. {insight}")
    
    # Document processing simulation
    st.subheader("📄 Document Processing Simulation")
    
    # Simulate processing different document types
    document_types = [
        {"type": "CSV", "description": "Structured data files", "use_case": "Employee records, financial data"},
        {"type": "Excel", "description": "Spreadsheet files", "use_case": "Reports, budgets, project plans"},
        {"type": "PDF", "description": "Document files", "use_case": "Policies, procedures, reports"},
        {"type": "JSON", "description": "Semi-structured data", "use_case": "API responses, configuration files"},
        {"type": "SQLite", "description": "Database files", "use_case": "Application databases, data storage"}
    ]
    
    for doc_type in document_types:
        with st.expander(f"📋 {doc_type['type']} Processing"):
            st.write(f"**Description:** {doc_type['description']}")
            st.write(f"**Use Case:** {doc_type['use_case']}")
            st.write("**Processing Capabilities:**")
            st.write("- Data extraction and parsing")
            st.write("- Structure analysis")
            st.write("- Content indexing")
            st.write("- Query and search functionality")
    
    # Agent integration example
    st.subheader("🤖 Agent Integration Example")
    
    st.write("**How Agents Use Document Data:**")
    
    agent_examples = [
        {
            "agent": "Research Specialist",
            "use_case": "Analyze uploaded research papers and reports",
            "tools": ["search_document_content", "analyze_document_data"]
        },
        {
            "agent": "Data Analyst", 
            "use_case": "Process uploaded datasets and spreadsheets",
            "tools": ["query_document_data", "extract_document_insights"]
        },
        {
            "agent": "Compliance Specialist",
            "use_case": "Review uploaded policy documents and regulations",
            "tools": ["search_document_content", "compare_documents"]
        },
        {
            "agent": "Technical Writer",
            "use_case": "Reference uploaded technical documentation",
            "tools": ["get_document_summary", "search_document_content"]
        }
    ]
    
    for example in agent_examples:
        with st.expander(f"👤 {example['agent']}"):
            st.write(f"**Use Case:** {example['use_case']}")
            st.write("**Available Tools:**")
            for tool in example['tools']:
                st.write(f"- {tool}")
    
    # Digital Twin context
    st.subheader("🏢 Digital Twin Integration")
    
    st.write("**How Document Processing Enhances Digital Twins:**")
    
    benefits = [
        "**Real Data Integration:** Upload actual organizational data for accurate modeling",
        "**Historical Analysis:** Process past reports and data for trend analysis", 
        "**Compliance Monitoring:** Upload regulatory documents for compliance checking",
        "**Performance Tracking:** Analyze uploaded performance metrics and KPIs",
        "**Decision Support:** Use uploaded data to inform strategic recommendations",
        "**Scenario Planning:** Process uploaded scenarios and what-if analyses"
    ]
    
    for benefit in benefits:
        st.write(f"✅ {benefit}")
    
    # Implementation steps
    st.subheader("🚀 Implementation Steps")
    
    steps = [
        "1. **Upload Documents:** Use the file upload interface to add your documents",
        "2. **Automatic Processing:** The system automatically processes and indexes your data",
        "3. **Agent Access:** Agents can immediately access and analyze your documents",
        "4. **Enhanced Analysis:** Get more accurate insights based on your real data",
        "5. **Continuous Learning:** The system learns from your data patterns over time"
    ]
    
    for step in steps:
        st.write(step)

if __name__ == "__main__":
    demonstrate_document_processing()
