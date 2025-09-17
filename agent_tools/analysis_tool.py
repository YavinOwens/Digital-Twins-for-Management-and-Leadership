"""
Analysis Tool for CrewAI Agents

This module provides the AnalysisTool that enables agents to process
and analyze research data to extract meaningful insights and patterns.
"""

from crewai.tools import BaseTool
from typing import Dict, Any, List
import re
import json


class AnalysisTool(BaseTool):
    """
    Tool to analyze research data and extract key insights
    
    This tool processes research data to identify patterns, themes,
    and strategic insights that can inform decision-making.
    """
    
    name: str = "analysis_tool"
    description: str = "Tool to analyze research data and extract meaningful insights, patterns, and strategic recommendations"
    
    def _run(self, data: str) -> str:
        """
        Analyze the provided data and return insights
        
        Args:
            data (str): The research data to analyze
            
        Returns:
            str: Analysis results with key insights and patterns
        """
        try:
            # Basic analysis of the data
            analysis_result = self._perform_analysis(data)
            return analysis_result
            
        except Exception as e:
            return f"Analysis failed: {str(e)}. Data preview: {data[:100]}..."
    
    def _perform_analysis(self, data: str) -> str:
        """
        Perform streamlined analysis on the research data for faster processing
        
        Args:
            data (str): The research data to analyze
            
        Returns:
            str: Concise analysis results
        """
        # Extract key metrics
        word_count = len(data.split())
        char_count = len(data)
        
        # Identify key themes and topics (limited to top 5)
        themes = self._extract_themes(data)[:5]
        
        # Extract key statistics (limited to top 3)
        statistics = self._extract_statistics(data)[:3]
        
        # Identify top challenges and opportunities (limited to top 3 each)
        challenges = self._identify_challenges(data)[:3]
        opportunities = self._identify_opportunities(data)[:3]
        
        # Create streamlined analysis
        analysis = f"""# Strategic Analysis Summary

## Key Insights
- **Data Scope**: {word_count:,} words analyzed
- **Primary Themes**: {len(themes)} key themes identified
- **Critical Challenges**: {len(challenges)} main obstacles
- **Key Opportunities**: {len(opportunities)} strategic advantages

## Top Themes
{self._format_list(themes)}

## Key Statistics
{self._format_list(statistics)}

## Main Challenges
{self._format_list(challenges)}

## Strategic Opportunities
{self._format_list(opportunities)}

## Executive Summary
Based on the analysis, the data reveals significant potential with clear implementation pathways. The identified opportunities align with current market trends, while the challenges require focused strategic planning and resource allocation.

## Immediate Recommendations
1. **Priority Focus**: Address the most critical challenges first
2. **Quick Wins**: Leverage the top opportunities for immediate impact
3. **Strategic Planning**: Develop implementation roadmap based on key themes
4. **Risk Management**: Proactively address identified challenges

**Data Quality**: {'High' if char_count > 1000 else 'Medium' if char_count > 500 else 'Low'} completeness, {'High' if len(themes) > 3 else 'Medium' if len(themes) > 1 else 'Low'} relevance
"""
        
        return analysis
    
    def _extract_themes(self, data: str) -> List[str]:
        """Extract key themes from the data"""
        # Common business and technology themes
        theme_keywords = {
            'Technology': ['technology', 'digital', 'innovation', 'AI', 'automation', 'software', 'platform'],
            'Market': ['market', 'industry', 'sector', 'competition', 'growth', 'trends'],
            'Business': ['business', 'strategy', 'operations', 'management', 'leadership'],
            'Financial': ['revenue', 'profit', 'cost', 'investment', 'ROI', 'financial'],
            'Customer': ['customer', 'user', 'client', 'experience', 'satisfaction'],
            'Process': ['process', 'workflow', 'efficiency', 'optimization', 'improvement'],
            'Risk': ['risk', 'challenge', 'threat', 'vulnerability', 'concern'],
            'Opportunity': ['opportunity', 'potential', 'advantage', 'benefit', 'value']
        }
        
        themes = []
        data_lower = data.lower()
        
        for theme, keywords in theme_keywords.items():
            if any(keyword in data_lower for keyword in keywords):
                themes.append(theme)
        
        return themes
    
    def _extract_statistics(self, data: str) -> List[str]:
        """Extract statistical information from the data"""
        statistics = []
        
        # Look for percentage patterns
        percentage_pattern = r'(\d+(?:\.\d+)?%)'
        percentages = re.findall(percentage_pattern, data)
        statistics.extend([f"{p} mentioned" for p in percentages[:5]])  # Limit to 5
        
        # Look for number patterns
        number_pattern = r'(\d+(?:,\d{3})*(?:\.\d+)?)'
        numbers = re.findall(number_pattern, data)
        
        # Filter for meaningful numbers (not years or small counts)
        meaningful_numbers = [n for n in numbers if len(n) > 2 and not (1900 <= int(n.replace(',', '')) <= 2030)]
        statistics.extend([f"Key metric: {n}" for n in meaningful_numbers[:3]])  # Limit to 3
        
        return statistics
    
    def _identify_challenges(self, data: str) -> List[str]:
        """Identify challenges and pain points in the data"""
        challenge_keywords = [
            'challenge', 'difficulty', 'problem', 'issue', 'barrier', 'obstacle',
            'risk', 'threat', 'concern', 'limitation', 'constraint', 'bottleneck',
            'struggle', 'pain point', 'gap', 'shortage', 'deficiency'
        ]
        
        challenges = []
        data_lower = data.lower()
        
        for keyword in challenge_keywords:
            if keyword in data_lower:
                # Extract sentence containing the keyword
                sentences = data.split('.')
                for sentence in sentences:
                    if keyword in sentence.lower():
                        challenges.append(sentence.strip()[:100] + "...")
                        break
        
        return challenges[:5]  # Limit to 5 challenges
    
    def _identify_opportunities(self, data: str) -> List[str]:
        """Identify opportunities and advantages in the data"""
        opportunity_keywords = [
            'opportunity', 'potential', 'advantage', 'benefit', 'value',
            'growth', 'expansion', 'improvement', 'enhancement', 'innovation',
            'breakthrough', 'success', 'win', 'gain', 'profit'
        ]
        
        opportunities = []
        data_lower = data.lower()
        
        for keyword in opportunity_keywords:
            if keyword in data_lower:
                # Extract sentence containing the keyword
                sentences = data.split('.')
                for sentence in sentences:
                    if keyword in sentence.lower():
                        opportunities.append(sentence.strip()[:100] + "...")
                        break
        
        return opportunities[:5]  # Limit to 5 opportunities
    
    def _format_list(self, items: List[str]) -> str:
        """Format a list of items for display"""
        if not items:
            return "- No items identified"
        
        return '\n'.join([f"- {item}" for item in items])
