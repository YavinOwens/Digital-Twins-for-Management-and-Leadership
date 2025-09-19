"""
Research Validation Tool

This module provides tools for research validation and Harvard referencing
that can be used by all agents in the Digital Twin system.
"""

from crewai.tools import tool
from typing import Dict, List, Any, Optional
import logging
import re
import requests
from agent_tools.reference_manager import (
    create_reference,
    add_citation,
    validate_reference,
    format_harvard_reference,
    generate_reference_list,
    get_citation_stats,
    remove_invalid_references
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@tool("validate_research_source")
def validate_research_source(url: str, title: str = None, authors: str = None, year: str = None) -> str:
    """
    Validate a research source by checking URL accessibility and extracting metadata.
    
    Args:
        url: URL of the source to validate
        title: Optional title of the source
        authors: Optional authors of the source
        year: Optional publication year
        
    Returns:
        Validation result with source information
    """
    try:
        # Validate URL
        from agent_tools.reference_manager import reference_manager
        validation_result = reference_manager.validate_url(url)
        
        if not validation_result['valid']:
            return f"❌ Source validation failed: {validation_result['error']}"
        
        # Extract metadata if not provided
        if not title and validation_result.get('title'):
            title = validation_result['title']
        
        if not authors:
            authors = "Unknown Author"
        
        if not year:
            year = "2024"  # Default year
        
        # Create reference
        ref_id = create_reference(
            title=title or "Untitled",
            authors=authors,
            year=year,
            url=url
        )
        
        # Validate the reference
        ref_validation = validate_reference(ref_id)
        
        if ref_validation['valid']:
            return f"✅ Source validated successfully!\n\n**Reference ID:** {ref_id}\n**Title:** {title}\n**Authors:** {authors}\n**Year:** {year}\n**URL:** {url}\n**Status:** Accessible and verified"
        else:
            return f"⚠️ Source accessible but validation incomplete: {ref_validation['error']}"
            
    except Exception as e:
        logger.error(f"Error validating research source: {e}")
        return f"❌ Error validating source: {e}"


@tool("add_harvard_citation")
def add_harvard_citation(text: str, ref_id: str, page: str = None) -> str:
    """
    Add Harvard-style inline citation to text.
    
    Args:
        text: Text to add citation to
        ref_id: Reference ID for citation
        page: Optional page number
        
    Returns:
        Text with Harvard citation added
    """
    try:
        cited_text = add_citation(text, ref_id, page)
        return f"✅ Citation added successfully!\n\n**Original text:** {text}\n**With citation:** {cited_text}"
        
    except Exception as e:
        logger.error(f"Error adding citation: {e}")
        return f"❌ Error adding citation: {e}"


@tool("create_harvard_reference")
def create_harvard_reference(title: str, authors: str, year: str, url: str = None, publisher: str = None, journal: str = None) -> str:
    """
    Create a Harvard-style reference entry.
    
    Args:
        title: Title of the source
        authors: Author names (comma-separated)
        year: Publication year
        url: Optional URL for web sources
        publisher: Optional publisher name
        journal: Optional journal name
        
    Returns:
        Reference ID and formatted reference
    """
    try:
        ref_id = create_reference(
            title=title,
            authors=authors,
            year=year,
            url=url,
            publisher=publisher,
            journal=journal
        )
        
        if ref_id:
            formatted_ref = format_harvard_reference(ref_id)
            return f"✅ Reference created successfully!\n\n**Reference ID:** {ref_id}\n**Formatted Reference:** {formatted_ref}"
        else:
            return "❌ Error creating reference"
            
    except Exception as e:
        logger.error(f"Error creating reference: {e}")
        return f"❌ Error creating reference: {e}"


@tool("validate_all_references")
def validate_all_references() -> str:
    """
    Validate all references in the system and remove invalid ones.
    
    Returns:
        Validation report with statistics
    """
    try:
        # Get citation stats before validation
        stats_before = get_citation_stats()
        
        # Remove invalid references
        removed_refs = remove_invalid_references()
        
        # Get citation stats after validation
        stats_after = get_citation_stats()
        
        report = f"📊 **Reference Validation Report**\n\n"
        report += f"**Before Validation:**\n"
        report += f"- Total references: {stats_before['total_references']}\n"
        report += f"- Validated references: {stats_before['validated_references']}\n"
        report += f"- Validation rate: {stats_before['validation_rate']:.1f}%\n\n"
        
        report += f"**After Validation:**\n"
        report += f"- Total references: {stats_after['total_references']}\n"
        report += f"- Validated references: {stats_after['validated_references']}\n"
        report += f"- Validation rate: {stats_after['validation_rate']:.1f}%\n\n"
        
        report += f"**Removed References:** {len(removed_refs)}\n"
        if removed_refs:
            report += f"Removed reference IDs: {', '.join(removed_refs)}\n"
        
        return report
        
    except Exception as e:
        logger.error(f"Error validating references: {e}")
        return f"❌ Error validating references: {e}"


@tool("generate_reference_list")
def generate_reference_list_tool() -> str:
    """
    Generate a complete reference list in Harvard style.
    
    Returns:
        Formatted reference list
    """
    try:
        reference_list = generate_reference_list()
        stats = get_citation_stats()
        
        report = f"📚 **Reference List**\n\n"
        report += f"**Statistics:**\n"
        report += f"- Total references: {stats['total_references']}\n"
        report += f"- Validated references: {stats['validated_references']}\n"
        report += f"- Web references: {stats['web_references']}\n"
        report += f"- Inline citations: {stats['inline_citations']}\n\n"
        report += f"**References:**\n{reference_list}"
        
        return report
        
    except Exception as e:
        logger.error(f"Error generating reference list: {e}")
        return f"❌ Error generating reference list: {e}"


@tool("fact_check_claim")
def fact_check_claim(claim: str, context: str = None) -> str:
    """
    Fact-check a specific claim against reliable sources.
    
    Args:
        claim: The claim to fact-check
        context: Optional context for the claim
        
    Returns:
        Fact-checking result with verification status
    """
    try:
        # This is a simplified fact-checking tool
        # In a real implementation, this would use multiple reliable sources
        
        report = f"🔍 **Fact-Checking Report**\n\n"
        report += f"**Claim to verify:** {claim}\n\n"
        
        if context:
            report += f"**Context:** {context}\n\n"
        
        # Basic validation logic (simplified)
        if any(keyword in claim.lower() for keyword in ['always', 'never', 'all', 'none', 'every']):
            report += "⚠️ **Warning:** Absolute statements detected. These are often difficult to verify and may be inaccurate.\n\n"
        
        if any(keyword in claim.lower() for keyword in ['recent', 'latest', 'new', 'current']):
            report += "ℹ️ **Note:** Time-sensitive claims detected. Ensure information is current and up-to-date.\n\n"
        
        # Check for statistical claims
        if re.search(r'\d+%|\d+\.\d+%', claim):
            report += "📊 **Statistical claim detected:** Verify statistics against authoritative sources.\n\n"
        
        # Check for source requirements
        if not any(keyword in claim.lower() for keyword in ['according to', 'source:', 'study shows', 'research indicates']):
            report += "❌ **No source attribution:** This claim lacks proper source attribution.\n\n"
        
        report += "**Recommendations:**\n"
        report += "1. Verify against multiple reliable sources\n"
        report += "2. Check for recent updates or corrections\n"
        report += "3. Ensure proper source attribution\n"
        report += "4. Avoid absolute statements without qualification\n"
        report += "5. Use peer-reviewed sources when possible\n"
        
        return report
        
    except Exception as e:
        logger.error(f"Error fact-checking claim: {e}")
        return f"❌ Error fact-checking claim: {e}"


@tool("check_academic_integrity")
def check_academic_integrity(content: str) -> str:
    """
    Check content for academic integrity issues.
    
    Args:
        content: Content to check for integrity issues
        
    Returns:
        Academic integrity assessment
    """
    try:
        report = f"🎓 **Academic Integrity Assessment**\n\n"
        
        issues = []
        recommendations = []
        
        # Check for proper citations
        if not re.search(r'\([^)]+\d{4}\)', content):
            issues.append("Missing inline citations")
            recommendations.append("Add proper Harvard-style inline citations")
        
        # Check for reference list
        if 'references' not in content.lower() and 'bibliography' not in content.lower():
            issues.append("Missing reference list")
            recommendations.append("Include a comprehensive reference list")
        
        # Check for source diversity
        if content.count('(') < 3:  # Basic check for citation frequency
            issues.append("Insufficient source citations")
            recommendations.append("Increase the number of source citations")
        
        # Check for proper attribution
        if re.search(r'\b(according to|source:|study shows|research indicates)\b', content, re.IGNORECASE):
            report += "✅ **Good:** Proper source attribution detected\n\n"
        else:
            issues.append("Lack of source attribution")
            recommendations.append("Add clear source attributions")
        
        # Check for plagiarism indicators
        if content.count('"') > 0 and not re.search(r'"[^"]*"\s*\([^)]+\d{4}\)', content):
            issues.append("Unattributed quotations")
            recommendations.append("Properly cite all quotations")
        
        # Generate report
        if issues:
            report += "❌ **Issues Found:**\n"
            for issue in issues:
                report += f"- {issue}\n"
            report += "\n"
        else:
            report += "✅ **No major issues detected**\n\n"
        
        if recommendations:
            report += "📝 **Recommendations:**\n"
            for rec in recommendations:
                report += f"- {rec}\n"
            report += "\n"
        
        report += "**Academic Integrity Score:** "
        if len(issues) == 0:
            report += "Excellent (A)\n"
        elif len(issues) <= 2:
            report += "Good (B)\n"
        elif len(issues) <= 4:
            report += "Fair (C)\n"
        else:
            report += "Needs Improvement (D)\n"
        
        return report
        
    except Exception as e:
        logger.error(f"Error checking academic integrity: {e}")
        return f"❌ Error checking academic integrity: {e}"
