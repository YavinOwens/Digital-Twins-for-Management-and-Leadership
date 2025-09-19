"""
Reference Management System

This module provides Harvard referencing functionality and reference management
for all agents in the Digital Twin system.
"""

import re
import requests
import time
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import logging
from urllib.parse import urlparse
import hashlib

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ReferenceManager:
    """
    Manages Harvard referencing and citation tracking for all agents
    """
    
    def __init__(self):
        self.references = {}  # Store all references by ID
        self.inline_citations = {}  # Track inline citations
        self.reference_counter = 1
        self.validated_sources = {}  # Cache for validated sources
        
    def create_reference(self, 
                        title: str, 
                        authors: str, 
                        year: str, 
                        url: str = None, 
                        publisher: str = None, 
                        journal: str = None, 
                        doi: str = None,
                        access_date: str = None) -> str:
        """
        Create a Harvard reference entry
        
        Args:
            title: Title of the source
            authors: Author names (comma-separated)
            year: Publication year
            url: URL if web source
            publisher: Publisher name
            journal: Journal name if applicable
            doi: DOI if available
            access_date: Date accessed (if web source)
            
        Returns:
            Reference ID for inline citation
        """
        try:
            # Generate unique reference ID
            ref_id = f"ref_{self.reference_counter}"
            self.reference_counter += 1
            
            # Format access date
            if not access_date:
                access_date = datetime.now().strftime("%d %B %Y")
            
            # Create reference entry
            reference = {
                "id": ref_id,
                "title": title,
                "authors": authors,
                "year": year,
                "url": url,
                "publisher": publisher,
                "journal": journal,
                "doi": doi,
                "access_date": access_date,
                "created_at": datetime.now().isoformat(),
                "validated": False
            }
            
            # Store reference
            self.references[ref_id] = reference
            
            logger.info(f"Created reference: {ref_id} - {title}")
            return ref_id
            
        except Exception as e:
            logger.error(f"Error creating reference: {e}")
            return None
    
    def add_inline_citation(self, text: str, ref_id: str, page: str = None) -> str:
        """
        Add inline citation to text
        
        Args:
            text: The text to add citation to
            ref_id: Reference ID
            page: Page number if applicable
            
        Returns:
            Text with inline citation added
        """
        try:
            if ref_id not in self.references:
                logger.warning(f"Reference {ref_id} not found")
                return text
            
            # Create citation text
            citation_text = f"({self.references[ref_id]['authors'].split(',')[0].strip()} et al., {self.references[ref_id]['year']}"
            if page:
                citation_text += f", p. {page}"
            citation_text += ")"
            
            # Add citation to text
            cited_text = f"{text} {citation_text}"
            
            # Track inline citation
            if ref_id not in self.inline_citations:
                self.inline_citations[ref_id] = []
            self.inline_citations[ref_id].append({
                "text": text,
                "page": page,
                "timestamp": datetime.now().isoformat()
            })
            
            return cited_text
            
        except Exception as e:
            logger.error(f"Error adding inline citation: {e}")
            return text
    
    def validate_url(self, url: str, timeout: int = 10) -> Dict[str, Any]:
        """
        Validate if a URL is accessible and get basic information
        
        Args:
            url: URL to validate
            timeout: Request timeout in seconds
            
        Returns:
            Validation result with status and metadata
        """
        try:
            # Check if already validated recently
            url_hash = hashlib.md5(url.encode()).hexdigest()
            if url_hash in self.validated_sources:
                cached_result = self.validated_sources[url_hash]
                if time.time() - cached_result['timestamp'] < 3600:  # 1 hour cache
                    return cached_result['result']
            
            # Parse URL
            parsed_url = urlparse(url)
            if not parsed_url.scheme or not parsed_url.netloc:
                return {
                    "valid": False,
                    "error": "Invalid URL format",
                    "status_code": None,
                    "title": None,
                    "accessible": False
                }
            
            # Make request with proper headers
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=timeout, allow_redirects=True)
            
            # Extract title if possible
            title = None
            if response.status_code == 200:
                try:
                    # Simple title extraction
                    title_match = re.search(r'<title[^>]*>([^<]+)</title>', response.text, re.IGNORECASE)
                    if title_match:
                        title = title_match.group(1).strip()
                except:
                    pass
            
            result = {
                "valid": response.status_code == 200,
                "error": None if response.status_code == 200 else f"HTTP {response.status_code}",
                "status_code": response.status_code,
                "title": title,
                "accessible": response.status_code == 200,
                "url": response.url  # Final URL after redirects
            }
            
            # Cache result
            self.validated_sources[url_hash] = {
                "result": result,
                "timestamp": time.time()
            }
            
            return result
            
        except requests.exceptions.Timeout:
            return {
                "valid": False,
                "error": "Request timeout",
                "status_code": None,
                "title": None,
                "accessible": False
            }
        except requests.exceptions.RequestException as e:
            return {
                "valid": False,
                "error": str(e),
                "status_code": None,
                "title": None,
                "accessible": False
            }
        except Exception as e:
            logger.error(f"Error validating URL {url}: {e}")
            return {
                "valid": False,
                "error": str(e),
                "status_code": None,
                "title": None,
                "accessible": False
            }
    
    def validate_reference(self, ref_id: str) -> Dict[str, Any]:
        """
        Validate a reference by checking its URL and extracting metadata
        
        Args:
            ref_id: Reference ID to validate
            
        Returns:
            Validation result
        """
        try:
            if ref_id not in self.references:
                return {
                    "valid": False,
                    "error": "Reference not found",
                    "metadata": None
                }
            
            reference = self.references[ref_id]
            
            # If no URL, mark as validated (book, journal, etc.)
            if not reference.get('url'):
                reference['validated'] = True
                return {
                    "valid": True,
                    "error": None,
                    "metadata": reference
                }
            
            # Validate URL
            url_validation = self.validate_url(reference['url'])
            
            if url_validation['valid']:
                # Update reference with validated information
                if url_validation.get('title') and not reference.get('title'):
                    reference['title'] = url_validation['title']
                reference['validated'] = True
                reference['validation_date'] = datetime.now().isoformat()
                
                return {
                    "valid": True,
                    "error": None,
                    "metadata": reference
                }
            else:
                reference['validated'] = False
                reference['validation_error'] = url_validation['error']
                
                return {
                    "valid": False,
                    "error": url_validation['error'],
                    "metadata": reference
                }
                
        except Exception as e:
            logger.error(f"Error validating reference {ref_id}: {e}")
            return {
                "valid": False,
                "error": str(e),
                "metadata": None
            }
    
    def format_harvard_reference(self, ref_id: str) -> str:
        """
        Format a reference in Harvard style
        
        Args:
            ref_id: Reference ID
            
        Returns:
            Formatted Harvard reference
        """
        try:
            if ref_id not in self.references:
                return f"[Reference {ref_id} not found]"
            
            ref = self.references[ref_id]
            
            # Format authors
            authors = ref['authors']
            if ',' in authors:
                # Multiple authors
                author_list = [author.strip() for author in authors.split(',')]
                if len(author_list) == 2:
                    formatted_authors = f"{author_list[0]} and {author_list[1]}"
                else:
                    formatted_authors = f"{author_list[0]} et al."
            else:
                formatted_authors = authors
            
            # Format based on source type
            if ref.get('url'):
                # Web source
                reference_text = f"{formatted_authors} ({ref['year']}) {ref['title']}. "
                if ref.get('journal'):
                    reference_text += f"{ref['journal']}. "
                if ref.get('publisher'):
                    reference_text += f"{ref['publisher']}. "
                reference_text += f"Available at: {ref['url']} (Accessed: {ref['access_date']})"
            elif ref.get('journal'):
                # Journal article
                reference_text = f"{formatted_authors} ({ref['year']}) {ref['title']}. {ref['journal']}"
                if ref.get('publisher'):
                    reference_text += f", {ref['publisher']}"
            else:
                # Book or other source
                reference_text = f"{formatted_authors} ({ref['year']}) {ref['title']}"
                if ref.get('publisher'):
                    reference_text += f". {ref['publisher']}"
            
            return reference_text
            
        except Exception as e:
            logger.error(f"Error formatting reference {ref_id}: {e}")
            return f"[Error formatting reference {ref_id}]"
    
    def generate_reference_list(self) -> str:
        """
        Generate a complete reference list in Harvard style
        
        Returns:
            Formatted reference list
        """
        try:
            if not self.references:
                return "No references available."
            
            reference_list = ["## References\n"]
            
            # Sort references by author name
            sorted_refs = sorted(self.references.values(), key=lambda x: x['authors'].split(',')[0].strip())
            
            for i, ref in enumerate(sorted_refs, 1):
                reference_text = self.format_harvard_reference(ref['id'])
                validation_status = "✓" if ref.get('validated') else "✗"
                reference_list.append(f"{i}. {reference_text} {validation_status}")
            
            return "\n".join(reference_list)
            
        except Exception as e:
            logger.error(f"Error generating reference list: {e}")
            return "Error generating reference list."
    
    def get_citation_stats(self) -> Dict[str, Any]:
        """
        Get statistics about citations and references
        
        Returns:
            Citation statistics
        """
        try:
            total_refs = len(self.references)
            validated_refs = sum(1 for ref in self.references.values() if ref.get('validated'))
            web_refs = sum(1 for ref in self.references.values() if ref.get('url'))
            inline_citations = sum(len(citations) for citations in self.inline_citations.values())
            
            return {
                "total_references": total_refs,
                "validated_references": validated_refs,
                "web_references": web_refs,
                "inline_citations": inline_citations,
                "validation_rate": (validated_refs / total_refs * 100) if total_refs > 0 else 0
            }
            
        except Exception as e:
            logger.error(f"Error getting citation stats: {e}")
            return {"error": str(e)}
    
    def remove_invalid_references(self) -> List[str]:
        """
        Remove references that failed validation
        
        Returns:
            List of removed reference IDs
        """
        try:
            removed_refs = []
            refs_to_remove = []
            
            for ref_id, ref in self.references.items():
                if not ref.get('validated') and ref.get('validation_error'):
                    refs_to_remove.append(ref_id)
                    removed_refs.append(ref_id)
            
            # Remove invalid references
            for ref_id in refs_to_remove:
                del self.references[ref_id]
                if ref_id in self.inline_citations:
                    del self.inline_citations[ref_id]
            
            logger.info(f"Removed {len(removed_refs)} invalid references")
            return removed_refs
            
        except Exception as e:
            logger.error(f"Error removing invalid references: {e}")
            return []


# Global reference manager instance
reference_manager = ReferenceManager()


def create_reference(title: str, authors: str, year: str, **kwargs) -> str:
    """Create a new reference"""
    return reference_manager.create_reference(title, authors, year, **kwargs)


def add_citation(text: str, ref_id: str, page: str = None) -> str:
    """Add inline citation to text"""
    return reference_manager.add_inline_citation(text, ref_id, page)


def validate_reference(ref_id: str) -> Dict[str, Any]:
    """Validate a reference"""
    return reference_manager.validate_reference(ref_id)


def format_harvard_reference(ref_id: str) -> str:
    """Format a reference in Harvard style"""
    return reference_manager.format_harvard_reference(ref_id)


def generate_reference_list() -> str:
    """Generate complete reference list"""
    return reference_manager.generate_reference_list()


def get_citation_stats() -> Dict[str, Any]:
    """Get citation statistics"""
    return reference_manager.get_citation_stats()


def remove_invalid_references() -> List[str]:
    """Remove invalid references"""
    return reference_manager.remove_invalid_references()
