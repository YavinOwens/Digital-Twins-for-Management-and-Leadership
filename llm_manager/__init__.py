"""
LLM Manager Module

This module handles LLM initialization, configuration, and management for the CrewAI system.
"""

from .llm_initializer import initialize_llm, check_ollama_cloud_status

__all__ = ['initialize_llm', 'check_ollama_cloud_status']
