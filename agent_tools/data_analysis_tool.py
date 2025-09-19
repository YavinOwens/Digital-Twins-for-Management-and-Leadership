"""
Data Analysis Tool for Digital Twins Management System

This module provides comprehensive data analysis capabilities for agents to work with
uploaded documents and datasets.
"""

import pandas as pd
import numpy as np
import json
from typing import Dict, List, Any, Optional, Union
import logging
from pathlib import Path
import sqlite3
from datetime import datetime, timedelta
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataAnalysisTool:
    """
    Comprehensive data analysis tool for agents
    """
    
    def __init__(self):
        self.analysis_cache = {}
    
    def analyze_document_data(self, document_data: Dict[str, Any], analysis_type: str = "comprehensive") -> Dict[str, Any]:
        """
        Analyze document data and return insights
        """
        try:
            if 'error' in document_data:
                return {'error': f"Document has errors: {document_data['error']}"}
            
            data_type = document_data.get('data_type', 'unknown')
            doc_type = document_data.get('type', 'unknown')
            
            if analysis_type == "comprehensive":
                return self._comprehensive_analysis(document_data)
            elif analysis_type == "statistical":
                return self._statistical_analysis(document_data)
            elif analysis_type == "text":
                return self._text_analysis(document_data)
            elif analysis_type == "temporal":
                return self._temporal_analysis(document_data)
            elif analysis_type == "categorical":
                return self._categorical_analysis(document_data)
            else:
                return self._basic_analysis(document_data)
                
        except Exception as e:
            logger.error(f"Error analyzing document data: {e}")
            return {'error': str(e)}
    
    def _comprehensive_analysis(self, document_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform comprehensive analysis on document data
        """
        analysis = {
            'document_type': document_data.get('type', 'unknown'),
            'data_type': document_data.get('data_type', 'unknown'),
            'analysis_timestamp': datetime.now().isoformat(),
            'insights': []
        }
        
        # Basic analysis
        basic_analysis = self._basic_analysis(document_data)
        analysis.update(basic_analysis)
        
        # Type-specific analysis
        if document_data.get('type') == 'structured':
            structured_analysis = self._structured_data_analysis(document_data)
            analysis.update(structured_analysis)
        
        elif document_data.get('type') == 'semi_structured':
            semi_structured_analysis = self._semi_structured_data_analysis(document_data)
            analysis.update(semi_structured_analysis)
        
        elif document_data.get('type') == 'unstructured':
            unstructured_analysis = self._unstructured_data_analysis(document_data)
            analysis.update(unstructured_analysis)
        
        # Generate insights
        analysis['insights'] = self._generate_insights(analysis)
        
        return analysis
    
    def _basic_analysis(self, document_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform basic analysis on document data
        """
        analysis = {
            'file_info': {
                'filename': document_data.get('metadata', {}).get('filename', 'Unknown'),
                'file_size': document_data.get('metadata', {}).get('file_size', 0),
                'file_type': document_data.get('metadata', {}).get('file_type', 'Unknown'),
                'upload_timestamp': document_data.get('metadata', {}).get('upload_timestamp', 'Unknown')
            },
            'data_characteristics': {
                'type': document_data.get('type', 'unknown'),
                'data_type': document_data.get('data_type', 'unknown')
            }
        }
        
        # Add size information
        if 'shape' in document_data:
            analysis['data_characteristics']['dimensions'] = document_data['shape']
            analysis['data_characteristics']['row_count'] = document_data['shape'][0]
            analysis['data_characteristics']['column_count'] = document_data['shape'][1]
        
        if 'word_count' in document_data:
            analysis['data_characteristics']['word_count'] = document_data['word_count']
        
        if 'line_count' in document_data:
            analysis['data_characteristics']['line_count'] = document_data['line_count']
        
        if 'page_count' in document_data:
            analysis['data_characteristics']['page_count'] = document_data['page_count']
        
        return analysis
    
    def _structured_data_analysis(self, document_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze structured data (CSV, Excel, JSON, etc.)
        """
        analysis = {
            'structured_analysis': {
                'columns': document_data.get('columns', []),
                'data_types': document_data.get('dtypes', {}),
                'null_analysis': document_data.get('null_counts', {}),
                'summary_statistics': document_data.get('summary', {})
            }
        }
        
        # Analyze data quality
        if 'null_counts' in document_data:
            total_rows = document_data.get('shape', [0, 0])[0]
            if total_rows > 0:
                null_percentages = {
                    col: (count / total_rows) * 100 
                    for col, count in document_data['null_counts'].items()
                }
                analysis['structured_analysis']['data_quality'] = {
                    'null_percentages': null_percentages,
                    'completeness_score': 100 - np.mean(list(null_percentages.values())),
                    'columns_with_nulls': [col for col, pct in null_percentages.items() if pct > 0]
                }
        
        # Analyze data distribution
        if 'summary' in document_data and document_data['summary']:
            analysis['structured_analysis']['distribution_analysis'] = self._analyze_distribution(document_data['summary'])
        
        # Analyze column relationships
        if 'data' in document_data and document_data['data']:
            df = pd.DataFrame(document_data['data'])
            analysis['structured_analysis']['correlation_analysis'] = self._analyze_correlations(df)
        
        return analysis
    
    def _semi_structured_data_analysis(self, document_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze semi-structured data (JSON, XML, YAML, etc.)
        """
        analysis = {
            'semi_structured_analysis': {
                'structure_type': document_data.get('data_type', 'unknown'),
                'content_metrics': {
                    'line_count': document_data.get('line_count', 0),
                    'word_count': document_data.get('word_count', 0),
                    'char_count': document_data.get('char_count', 0)
                }
            }
        }
        
        # Analyze structure
        if 'structure' in document_data:
            analysis['semi_structured_analysis']['structure_analysis'] = self._analyze_structure(document_data['structure'])
        
        # Analyze content patterns
        if 'content' in document_data:
            content_analysis = self._analyze_content_patterns(document_data['content'])
            analysis['semi_structured_analysis']['content_patterns'] = content_analysis
        
        return analysis
    
    def _unstructured_data_analysis(self, document_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze unstructured data (PDF, DOCX, TXT, etc.)
        """
        analysis = {
            'unstructured_analysis': {
                'content_type': document_data.get('data_type', 'unknown'),
                'content_metrics': {
                    'word_count': document_data.get('word_count', 0),
                    'char_count': document_data.get('char_count', 0),
                    'page_count': document_data.get('page_count', 0),
                    'paragraph_count': document_data.get('paragraph_count', 0)
                }
            }
        }
        
        # Analyze text content
        if 'content' in document_data:
            text_analysis = self._analyze_text_content(document_data['content'])
            analysis['unstructured_analysis']['text_analysis'] = text_analysis
        
        return analysis
    
    def _analyze_distribution(self, summary_stats: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze data distribution from summary statistics
        """
        distribution_analysis = {}
        
        for column, stats in summary_stats.items():
            if isinstance(stats, dict) and 'mean' in stats:
                # Calculate distribution characteristics
                mean = stats.get('mean', 0)
                std = stats.get('std', 0)
                min_val = stats.get('min', 0)
                max_val = stats.get('max', 0)
                
                # Coefficient of variation
                cv = (std / mean) * 100 if mean != 0 else 0
                
                # Range
                range_val = max_val - min_val
                
                distribution_analysis[column] = {
                    'mean': mean,
                    'std': std,
                    'cv': cv,
                    'range': range_val,
                    'distribution_type': self._classify_distribution(cv, mean, std)
                }
        
        return distribution_analysis
    
    def _classify_distribution(self, cv: float, mean: float, std: float) -> str:
        """
        Classify distribution type based on statistics
        """
        if cv < 15:
            return "Low variability"
        elif cv < 35:
            return "Moderate variability"
        elif cv < 70:
            return "High variability"
        else:
            return "Very high variability"
    
    def _analyze_correlations(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze correlations between numeric columns
        """
        try:
            # Select only numeric columns
            numeric_df = df.select_dtypes(include=[np.number])
            
            if numeric_df.empty:
                return {'message': 'No numeric columns found for correlation analysis'}
            
            # Calculate correlation matrix
            corr_matrix = numeric_df.corr()
            
            # Find strong correlations
            strong_correlations = []
            for i in range(len(corr_matrix.columns)):
                for j in range(i+1, len(corr_matrix.columns)):
                    corr_value = corr_matrix.iloc[i, j]
                    if abs(corr_value) > 0.7:  # Strong correlation threshold
                        strong_correlations.append({
                            'column1': corr_matrix.columns[i],
                            'column2': corr_matrix.columns[j],
                            'correlation': corr_value
                        })
            
            return {
                'correlation_matrix': corr_matrix.to_dict(),
                'strong_correlations': strong_correlations,
                'correlation_summary': {
                    'total_pairs': len(strong_correlations),
                    'strong_positive': len([c for c in strong_correlations if c['correlation'] > 0.7]),
                    'strong_negative': len([c for c in strong_correlations if c['correlation'] < -0.7])
                }
            }
        except Exception as e:
            return {'error': f"Correlation analysis failed: {e}"}
    
    def _analyze_structure(self, structure: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze data structure for semi-structured data
        """
        structure_analysis = {
            'depth': self._calculate_structure_depth(structure),
            'complexity': self._calculate_structure_complexity(structure),
            'key_insights': []
        }
        
        # Analyze structure patterns
        if structure.get('type') == 'object':
            keys = structure.get('keys', [])
            structure_analysis['key_insights'].append(f"Object with {len(keys)} keys")
            
            # Check for nested structures
            children = structure.get('children', {})
            nested_objects = [k for k, v in children.items() if v.get('type') == 'object']
            if nested_objects:
                structure_analysis['key_insights'].append(f"Nested objects: {', '.join(nested_objects)}")
        
        elif structure.get('type') == 'array':
            length = structure.get('length', 0)
            structure_analysis['key_insights'].append(f"Array with {length} elements")
        
        return structure_analysis
    
    def _calculate_structure_depth(self, structure: Dict[str, Any], current_depth: int = 0) -> int:
        """
        Calculate the maximum depth of nested structures
        """
        if structure.get('type') in ['object', 'array']:
            children = structure.get('children', {})
            if isinstance(children, dict):
                max_child_depth = max([
                    self._calculate_structure_depth(child, current_depth + 1)
                    for child in children.values()
                ], default=current_depth)
                return max_child_depth
            elif isinstance(children, list):
                max_child_depth = max([
                    self._calculate_structure_depth(child, current_depth + 1)
                    for child in children
                ], default=current_depth)
                return max_child_depth
        
        return current_depth
    
    def _calculate_structure_complexity(self, structure: Dict[str, Any]) -> str:
        """
        Calculate structure complexity
        """
        depth = self._calculate_structure_depth(structure)
        
        if depth <= 2:
            return "Simple"
        elif depth <= 4:
            return "Moderate"
        else:
            return "Complex"
    
    def _analyze_content_patterns(self, content: str) -> Dict[str, Any]:
        """
        Analyze content patterns in semi-structured data
        """
        patterns = {
            'line_patterns': {},
            'content_insights': []
        }
        
        lines = content.split('\n')
        
        # Analyze line patterns
        line_lengths = [len(line) for line in lines if line.strip()]
        if line_lengths:
            patterns['line_patterns'] = {
                'avg_length': np.mean(line_lengths),
                'max_length': max(line_lengths),
                'min_length': min(line_lengths),
                'empty_lines': len([line for line in lines if not line.strip()])
            }
        
        # Look for common patterns
        if any('http' in line for line in lines):
            patterns['content_insights'].append("Contains URLs")
        
        if any('@' in line for line in lines):
            patterns['content_insights'].append("Contains email addresses")
        
        if any(re.match(r'\d{4}-\d{2}-\d{2}', line) for line in lines):
            patterns['content_insights'].append("Contains date patterns")
        
        return patterns
    
    def _analyze_text_content(self, content: str) -> Dict[str, Any]:
        """
        Analyze text content in unstructured data
        """
        text_analysis = {
            'basic_metrics': {
                'word_count': len(content.split()),
                'char_count': len(content),
                'sentence_count': len(re.split(r'[.!?]+', content)),
                'paragraph_count': len([p for p in content.split('\n\n') if p.strip()])
            },
            'readability': {},
            'content_insights': []
        }
        
        # Basic readability metrics
        words = content.split()
        sentences = re.split(r'[.!?]+', content)
        
        if words and sentences:
            avg_words_per_sentence = len(words) / len(sentences)
            avg_chars_per_word = len(content) / len(words)
            
            text_analysis['readability'] = {
                'avg_words_per_sentence': avg_words_per_sentence,
                'avg_chars_per_word': avg_chars_per_word,
                'readability_level': self._assess_readability(avg_words_per_sentence, avg_chars_per_word)
            }
        
        # Content analysis
        if 'http' in content:
            text_analysis['content_insights'].append("Contains URLs")
        
        if '@' in content:
            text_analysis['content_insights'].append("Contains email addresses")
        
        if re.search(r'\d{4}-\d{2}-\d{2}', content):
            text_analysis['content_insights'].append("Contains date patterns")
        
        # Keyword analysis
        common_words = self._extract_common_words(content)
        if common_words:
            text_analysis['common_words'] = common_words[:10]  # Top 10
        
        return text_analysis
    
    def _assess_readability(self, avg_words_per_sentence: float, avg_chars_per_word: float) -> str:
        """
        Assess readability level
        """
        if avg_words_per_sentence < 15 and avg_chars_per_word < 5:
            return "Easy"
        elif avg_words_per_sentence < 20 and avg_chars_per_word < 6:
            return "Moderate"
        else:
            return "Complex"
    
    def _extract_common_words(self, content: str, min_length: int = 4) -> List[tuple]:
        """
        Extract most common words from content
        """
        # Clean and tokenize
        words = re.findall(r'\b[a-zA-Z]+\b', content.lower())
        words = [word for word in words if len(word) >= min_length]
        
        # Count frequencies
        word_counts = {}
        for word in words:
            word_counts[word] = word_counts.get(word, 0) + 1
        
        # Sort by frequency
        return sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
    
    def _generate_insights(self, analysis: Dict[str, Any]) -> List[str]:
        """
        Generate insights from analysis results
        """
        insights = []
        
        # Data quality insights
        if 'structured_analysis' in analysis:
            structured = analysis['structured_analysis']
            if 'data_quality' in structured:
                completeness = structured['data_quality'].get('completeness_score', 100)
                if completeness < 80:
                    insights.append(f"Data completeness is {completeness:.1f}% - consider data cleaning")
                elif completeness > 95:
                    insights.append("Excellent data completeness")
        
        # Distribution insights
        if 'structured_analysis' in analysis and 'distribution_analysis' in analysis['structured_analysis']:
            dist_analysis = analysis['structured_analysis']['distribution_analysis']
            high_var_cols = [col for col, stats in dist_analysis.items() if stats.get('distribution_type') == 'Very high variability']
            if high_var_cols:
                insights.append(f"High variability detected in columns: {', '.join(high_var_cols)}")
        
        # Correlation insights
        if 'structured_analysis' in analysis and 'correlation_analysis' in analysis['structured_analysis']:
            corr_analysis = analysis['structured_analysis']['correlation_analysis']
            if 'strong_correlations' in corr_analysis and corr_analysis['strong_correlations']:
                insights.append(f"Found {len(corr_analysis['strong_correlations'])} strong correlations between variables")
        
        # Content insights
        if 'unstructured_analysis' in analysis and 'text_analysis' in analysis['unstructured_analysis']:
            text_analysis = analysis['unstructured_analysis']['text_analysis']
            if 'readability' in text_analysis:
                readability = text_analysis['readability'].get('readability_level', 'Unknown')
                insights.append(f"Content readability level: {readability}")
        
        # Structure insights
        if 'semi_structured_analysis' in analysis and 'structure_analysis' in analysis['semi_structured_analysis']:
            structure = analysis['semi_structured_analysis']['structure_analysis']
            complexity = structure.get('complexity', 'Unknown')
            insights.append(f"Data structure complexity: {complexity}")
        
        return insights
    
    def query_document_data(self, document_data: Dict[str, Any], query: str) -> Dict[str, Any]:
        """
        Query document data based on natural language query
        """
        try:
            if 'error' in document_data:
                return {'error': f"Document has errors: {document_data['error']}"}
            
            # Parse query
            query_lower = query.lower()
            
            # Handle different query types
            if 'count' in query_lower or 'how many' in query_lower:
                return self._handle_count_query(document_data, query)
            elif 'find' in query_lower or 'search' in query_lower:
                return self._handle_search_query(document_data, query)
            elif 'summary' in query_lower or 'overview' in query_lower:
                return self._handle_summary_query(document_data, query)
            elif 'columns' in query_lower or 'fields' in query_lower:
                return self._handle_columns_query(document_data, query)
            else:
                return self._handle_general_query(document_data, query)
                
        except Exception as e:
            logger.error(f"Error querying document data: {e}")
            return {'error': str(e)}
    
    def _handle_count_query(self, document_data: Dict[str, Any], query: str) -> Dict[str, Any]:
        """
        Handle count-related queries
        """
        result = {'query_type': 'count', 'query': query}
        
        if document_data.get('type') == 'structured':
            if 'shape' in document_data:
                result['row_count'] = document_data['shape'][0]
                result['column_count'] = document_data['shape'][1]
            
            if 'sheets' in document_data:
                result['sheet_count'] = len(document_data['sheets'])
        
        elif document_data.get('type') == 'semi_structured':
            if 'line_count' in document_data:
                result['line_count'] = document_data['line_count']
        
        elif document_data.get('type') == 'unstructured':
            if 'word_count' in document_data:
                result['word_count'] = document_data['word_count']
            if 'page_count' in document_data:
                result['page_count'] = document_data['page_count']
        
        return result
    
    def _handle_search_query(self, document_data: Dict[str, Any], query: str) -> Dict[str, Any]:
        """
        Handle search-related queries
        """
        result = {'query_type': 'search', 'query': query}
        
        # Extract search terms from query
        search_terms = re.findall(r'"([^"]*)"', query) or re.findall(r'\b(\w+)\b', query)
        
        if 'content' in document_data:
            content = document_data['content']
            matches = []
            
            for term in search_terms:
                if term.lower() in content.lower():
                    # Find context around matches
                    lines = content.split('\n')
                    for i, line in enumerate(lines):
                        if term.lower() in line.lower():
                            matches.append({
                                'term': term,
                                'line': i + 1,
                                'context': line.strip()
                            })
            
            result['matches'] = matches
            result['match_count'] = len(matches)
        
        return result
    
    def _handle_summary_query(self, document_data: Dict[str, Any], query: str) -> Dict[str, Any]:
        """
        Handle summary-related queries
        """
        result = {'query_type': 'summary', 'query': query}
        
        # Use existing analysis if available
        if 'analysis' in document_data:
            result['summary'] = document_data['analysis']
        else:
            # Perform basic analysis
            analysis = self._basic_analysis(document_data)
            result['summary'] = analysis
        
        return result
    
    def _handle_columns_query(self, document_data: Dict[str, Any], query: str) -> Dict[str, Any]:
        """
        Handle columns/fields-related queries
        """
        result = {'query_type': 'columns', 'query': query}
        
        if document_data.get('type') == 'structured':
            if 'columns' in document_data:
                result['columns'] = document_data['columns']
                result['column_count'] = len(document_data['columns'])
            
            if 'dtypes' in document_data:
                result['data_types'] = document_data['dtypes']
            
            if 'sheets' in document_data:
                result['sheets'] = {}
                for sheet_name, sheet_data in document_data['sheets'].items():
                    result['sheets'][sheet_name] = {
                        'columns': sheet_data.get('columns', []),
                        'column_count': len(sheet_data.get('columns', []))
                    }
        
        return result
    
    def _handle_general_query(self, document_data: Dict[str, Any], query: str) -> Dict[str, Any]:
        """
        Handle general queries
        """
        result = {'query_type': 'general', 'query': query}
        
        # Provide basic information about the document
        result['document_info'] = {
            'type': document_data.get('type', 'unknown'),
            'data_type': document_data.get('data_type', 'unknown'),
            'filename': document_data.get('metadata', {}).get('filename', 'Unknown')
        }
        
        # Add relevant data based on document type
        if document_data.get('type') == 'structured':
            if 'shape' in document_data:
                result['data_info'] = {
                    'rows': document_data['shape'][0],
                    'columns': document_data['shape'][1]
                }
        
        elif document_data.get('type') == 'unstructured':
            if 'word_count' in document_data:
                result['content_info'] = {
                    'word_count': document_data['word_count'],
                    'char_count': document_data.get('char_count', 0)
                }
        
        return result
