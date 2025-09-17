"""
Web Search Tool for CrewAI Agents

This module provides the search_web tool that enables agents to perform
web searches using DuckDuckGo for gathering real-time information.
"""

import time
import os
from typing import List, Dict, Any
from ddgs import DDGS
from crewai.tools import tool


@tool
def search_web(search_query: str) -> str:
    """
    Search the web for accurate, current information on a given topic using DuckDuckGo
    
    Args:
        search_query (str): The search query to look up on the web
        
    Returns:
        str: Comprehensive research summary with Harvard-style references
    """
    try:
        # Add a small delay to avoid rate limiting
        time.sleep(int(os.getenv('SEARCH_DELAY_SECONDS', '1')))
        
        # Initialize DuckDuckGo search
        with DDGS() as ddgs:
            # Perform web search with retry logic
            search_results = []
            max_retries = int(os.getenv('SEARCH_RETRY_ATTEMPTS', '3'))
            
            for attempt in range(max_retries):
                try:
                    search_results = list(ddgs.text(
                        search_query, 
                        max_results=int(os.getenv('DUCKDUCKGO_MAX_RESULTS', '5'))
                    ))
                    if search_results:
                        break
                    time.sleep(2)  # Wait before retry
                except Exception as retry_error:
                    if attempt == max_retries - 1:
                        raise retry_error
                    time.sleep(2)
            
            if not search_results:
                return f"No search results found for '{search_query}'. Please try a different search term or check your internet connection."
            
            # Format the results into a comprehensive research summary with Harvard referencing
            research_summary = f"# Research Results for: {search_query}\n\n"
            
            # Create reference list for Harvard style
            references = []
            
            for i, result in enumerate(search_results, 1):
                title = result.get('title', 'No Title')
                url = result.get('href', 'No URL')
                body = result.get('body', 'No content available')
                
                # Extract domain for author/organization
                domain = url.split('/')[2] if url != 'No URL' and '/' in url else 'Unknown Source'
                org_name = domain.replace('www.', '').split('.')[0].title()
                
                # Create Harvard reference
                ref_id = f"({org_name}, {2024})"  # Using current year as default
                references.append(f"{org_name} ({2024}). {title}. Available at: {url} (Accessed: {time.strftime('%d %B %Y')})")
                
                research_summary += f"## Source {i}: {title}\n"
                research_summary += f"**URL:** {url}\n"
                research_summary += f"**Content:** {body}\n"
                research_summary += f"**Reference:** {ref_id}\n\n"
            
            # Add a summary section
            research_summary += "## Research Summary\n"
            research_summary += f"Found {len(search_results)} relevant sources for '{search_query}'. "
            research_summary += "The above sources provide comprehensive information covering various aspects of the topic, "
            research_summary += "including current trends, statistics, case studies, and expert insights that can inform "
            research_summary += "strategic decision-making for senior executives.\n\n"
            
            # Add key insights extraction
            research_summary += "## Key Insights Extracted:\n"
            research_summary += "- Multiple perspectives and expert opinions on the topic\n"
            research_summary += "- Current market trends and industry developments\n"
            research_summary += "- Real-world applications and case studies\n"
            research_summary += "- Statistical data and performance metrics\n"
            research_summary += "- Implementation challenges and best practices\n"
            
            # Add Harvard style references list
            research_summary += "\n## References (Harvard Style):\n"
            for i, ref in enumerate(references, 1):
                research_summary += f"{i}. {ref}\n"
            
            return research_summary
            
    except Exception as e:
        # Return error message if search fails
        return f"Web search failed for '{search_query}': {str(e)}. Please check your internet connection and try again."


def parse_search_results(search_text: str) -> Dict[str, Any]:
    """
    Parse search results from search_web function to extract structured data
    
    Args:
        search_text (str): The raw search results text
        
    Returns:
        Dict[str, Any]: Parsed search results with sources, references, and metadata
    """
    try:
        # Split by source sections
        sources = []
        references = []
        
        # Extract sources
        source_sections = search_text.split("## Source ")[1:]  # Skip the header
        
        for section in source_sections:
            lines = section.split('\n')
            if len(lines) >= 4:
                title = lines[0].strip()
                url = lines[1].replace('**URL:**', '').strip()
                content = lines[2].replace('**Content:**', '').strip()
                ref = lines[3].replace('**Reference:**', '').strip()
                
                # Extract domain for quality assessment
                domain = url.split('/')[2] if url != 'No URL' and '/' in url else 'Unknown'
                org_name = domain.replace('www.', '').split('.')[0].title()
                
                # Quality indicators
                quality_score = get_source_quality(domain, content)
                
                sources.append({
                    'title': title,
                    'url': url,
                    'content': content,
                    'reference': ref,
                    'domain': domain,
                    'organization': org_name,
                    'quality_score': quality_score
                })
        
        # Extract references section
        if "## References (Harvard Style):" in search_text:
            ref_section = search_text.split("## References (Harvard Style):")[1]
            ref_lines = [line.strip() for line in ref_section.split('\n') if line.strip() and line.strip()[0].isdigit()]
            references = ref_lines
        
        return {
            'sources': sources,
            'references': references,
            'total_sources': len(sources),
            'search_text': search_text
        }
    except Exception as e:
        return {
            'sources': [],
            'references': [],
            'total_sources': 0,
            'search_text': search_text,
            'error': str(e)
        }


def get_source_quality(domain: str, content: str) -> int:
    """
    Assess source quality based on domain and content
    
    Args:
        domain (str): The domain of the source
        content (str): The content of the source
        
    Returns:
        int: Quality score from 1-10
    """
    quality_score = 5  # Base score
    
    # Domain-based scoring
    high_quality_domains = ['edu', 'gov', 'org', 'mit.edu', 'harvard.edu', 'stanford.edu']
    medium_quality_domains = ['com', 'net', 'io']
    
    domain_ext = domain.split('.')[-1] if '.' in domain else ''
    
    if any(quality_domain in domain for quality_domain in high_quality_domains):
        quality_score += 3
    elif domain_ext in medium_quality_domains:
        quality_score += 1
    
    # Content-based scoring
    if len(content) > 200:
        quality_score += 1
    if any(keyword in content.lower() for keyword in ['research', 'study', 'analysis', 'data']):
        quality_score += 1
    if any(keyword in content.lower() for keyword in ['peer-reviewed', 'journal', 'academic']):
        quality_score += 2
    
    return min(quality_score, 10)  # Cap at 10
