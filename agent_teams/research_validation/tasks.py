"""
Research Validation Tasks

This module contains task definitions for the Research Validation team.
"""

from crewai import Task
from typing import List, Optional, Any
from agent_tools.reference_manager import reference_manager


def create_research_validation_tasks_with_data(
    validation_agent,
    query: str,
    research_data: str,
    conversation_history: Optional[List[Any]] = None,
    document_context: Optional[str] = None
) -> List[Task]:
    """
    Create research validation tasks with research data
    
    Args:
        validation_agent: Research validation agent
        query: Original user query
        research_data: Research data to validate
        conversation_history: Previous conversation context
        document_context: Document context from uploaded files
        
    Returns:
        List of validation tasks
    """
    
    # Task 1: Source Verification and Link Validation
    source_verification_task = Task(
        description=f"""
        **TASK: Source Verification and Link Validation**
        
        **Objective:** Verify all sources, links, and references mentioned in the research data for accuracy and accessibility.
        
        **Research Data to Validate:**
        {research_data}
        
        **Instructions:**
        1. **Extract all sources and links** from the research data
        2. **Verify each URL** by checking accessibility and content relevance
        3. **Validate academic references** and ensure they exist and are credible
        4. **Check for broken links** or inaccessible sources
        5. **Identify potentially unreliable sources** or suspicious domains
        6. **Create proper Harvard references** for all valid sources
        7. **Flag any sources that cannot be verified** for removal
        
        **Validation Criteria:**
        - URLs must be accessible and return valid content
        - Academic sources must be from credible institutions
        - News sources must be from reputable publications
        - Government sources must be from official domains
        - Commercial sources must be clearly identified
        
        **Output Requirements:**
        - List of all verified sources with Harvard references
        - List of invalid or inaccessible sources to be removed
        - Validation report with status of each source
        - Recommendations for source improvements
        
        **Quality Standards:**
        - Only include sources that can be independently verified
        - Ensure all Harvard references are properly formatted
        - Maintain high standards of academic integrity
        - Never include unverified or potentially false information
        """,
        expected_output="""A comprehensive source validation report including:
        1. Verified sources list with Harvard references
        2. Invalid sources list for removal
        3. Validation status for each source
        4. Recommendations for source quality improvement
        5. Academic integrity assessment""",
        agent=validation_agent,
        context=[],
        output_file="source_validation_report.md"
    )
    
    # Task 2: Fact-Checking and Accuracy Verification
    fact_checking_task = Task(
        description=f"""
        **TASK: Fact-Checking and Accuracy Verification**
        
        **Objective:** Verify the factual accuracy of all claims, statistics, and information presented in the research data.
        
        **Research Data to Fact-Check:**
        {research_data}
        
        **Instructions:**
        1. **Identify all factual claims** in the research data
        2. **Cross-reference each claim** with multiple reliable sources
        3. **Verify statistics and data points** against authoritative sources
        4. **Check for outdated information** and ensure currency
        5. **Validate technical information** against expert sources
        6. **Identify potential misinformation** or unsubstantiated claims
        7. **Flag any information that cannot be verified** for removal
        
        **Fact-Checking Sources:**
        - Academic databases and peer-reviewed journals
        - Government statistics and official reports
        - Reputable news organizations
        - Industry reports from credible institutions
        - Expert opinions from recognized authorities
        
        **Output Requirements:**
        - Fact-checking report with verification status
        - List of verified facts with source citations
        - List of unverified claims for removal
        - Recommendations for information accuracy improvements
        
        **Quality Standards:**
        - Only include information that can be independently verified
        - Use multiple sources to confirm each fact
        - Ensure all statistics are current and accurate
        - Maintain objectivity and avoid bias
        - Never include unverified or potentially false information
        """,
        expected_output="""A detailed fact-checking report including:
        1. Verified facts list with source citations
        2. Unverified claims list for removal
        3. Fact-checking methodology and sources used
        4. Accuracy assessment and recommendations
        5. Quality assurance summary""",
        agent=validation_agent,
        context=[source_verification_task],
        output_file="fact_checking_report.md"
    )
    
    # Task 3: Reference Formatting and Academic Integrity
    reference_formatting_task = Task(
        description=f"""
        **TASK: Reference Formatting and Academic Integrity**
        
        **Objective:** Ensure all references are properly formatted in Harvard style and maintain academic integrity standards.
        
        **Research Data to Format:**
        {research_data}
        
        **Instructions:**
        1. **Review all references** from previous validation tasks
        2. **Format references in Harvard style** according to academic standards
        3. **Add inline citations** throughout the research data
        4. **Create comprehensive reference list** with proper formatting
        5. **Ensure citation consistency** throughout the document
        6. **Add appendix with detailed source information**
        7. **Verify academic integrity** and proper attribution
        
        **Harvard Referencing Requirements:**
        - Author names: Surname, Initials
        - Publication year in parentheses
        - Title in italics for books, quotation marks for articles
        - Publisher and place of publication
        - URL and access date for web sources
        - DOI for academic articles when available
        
        **Inline Citation Format:**
        - (Author, Year) for single author
        - (Author et al., Year) for multiple authors
        - (Author, Year, p. X) for specific pages
        - Multiple citations: (Author1, Year; Author2, Year)
        
        **Output Requirements:**
        - Properly formatted Harvard reference list
        - Research data with inline citations added
        - Appendix with detailed source information
        - Academic integrity assessment
        - Citation quality report
        
        **Quality Standards:**
        - All references must be properly formatted
        - Inline citations must be accurate and consistent
        - Reference list must be complete and alphabetized
        - Academic integrity must be maintained throughout
        - No plagiarism or improper attribution
        """,
        expected_output="""A comprehensive reference formatting report including:
        1. Research data with inline citations added
        2. Properly formatted Harvard reference list
        3. Appendix with detailed source information
        4. Academic integrity assessment
        5. Citation quality and consistency report""",
        agent=validation_agent,
        context=[source_verification_task, fact_checking_task],
        output_file="reference_formatting_report.md"
    )
    
    # Task 4: Quality Assurance and Final Validation
    quality_assurance_task = Task(
        description=f"""
        **TASK: Quality Assurance and Final Validation**
        
        **Objective:** Perform final quality assurance check to ensure all information meets the highest standards of accuracy, credibility, and academic integrity.
        
        **Research Data to Validate:**
        {research_data}
        
        **Previous Validation Results:**
        - Source verification results
        - Fact-checking results
        - Reference formatting results
        
        **Instructions:**
        1. **Review all previous validation results** for completeness
        2. **Perform final accuracy check** on all remaining information
        3. **Verify all citations and references** are properly formatted
        4. **Check for any remaining unverified information** and remove it
        5. **Ensure academic integrity** throughout the document
        6. **Validate that all sources are credible** and accessible
        7. **Provide final quality assurance report** with recommendations
        
        **Quality Assurance Criteria:**
        - All information must be verifiable and accurate
        - All sources must be credible and accessible
        - All references must be properly formatted
        - No unverified or potentially false information
        - Academic integrity must be maintained
        - Professional standards must be met
        
        **Output Requirements:**
        - Final quality assurance report
        - Cleaned research data with only verified information
        - Complete reference list with all sources
        - Academic integrity certification
        - Recommendations for maintaining quality standards
        
        **Quality Standards:**
        - 100% accuracy for all included information
        - 100% accessibility for all sources
        - 100% proper formatting for all references
        - Zero tolerance for unverified information
        - Highest standards of academic integrity
        """,
        expected_output="""A final quality assurance report including:
        1. Cleaned research data with only verified information
        2. Complete and properly formatted reference list
        3. Academic integrity certification
        4. Quality assurance summary and recommendations
        5. Final validation status and approval""",
        agent=validation_agent,
        context=[source_verification_task, fact_checking_task, reference_formatting_task],
        output_file="quality_assurance_report.md"
    )
    
    return [
        source_verification_task,
        fact_checking_task,
        reference_formatting_task,
        quality_assurance_task
    ]


def create_research_validation_tasks(
    validation_agent,
    query: str,
    conversation_history: Optional[List[Any]] = None
) -> List[Task]:
    """
    Create research validation tasks without specific research data
    
    Args:
        validation_agent: Research validation agent
        query: Original user query
        conversation_history: Previous conversation context
        
    Returns:
        List of validation tasks
    """
    
    # Task 1: General Research Validation
    general_validation_task = Task(
        description=f"""
        **TASK: General Research Validation**
        
        **Objective:** Establish research validation standards and prepare for comprehensive source verification.
        
        **Query to Validate:**
        {query}
        
        **Instructions:**
        1. **Analyze the query** to identify research validation requirements
        2. **Establish validation standards** for the research topic
        3. **Identify potential sources** that will need verification
        4. **Prepare validation framework** for comprehensive checking
        5. **Set quality standards** for information accuracy
        6. **Create validation checklist** for systematic verification
        
        **Output Requirements:**
        - Research validation framework
        - Quality standards and criteria
        - Validation checklist and methodology
        - Recommendations for source verification
        """,
        expected_output="A comprehensive research validation framework and methodology",
        agent=validation_agent,
        context=[],
        output_file="validation_framework.md"
    )
    
    return [general_validation_task]
