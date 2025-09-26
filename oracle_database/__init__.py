"""
Oracle Database Package for Web Knowledge System

This package provides database connectivity and management utilities for Oracle Database 23ai.
"""

from .database_config import config, DatabaseConfig
from .database_manager import DatabaseManager, get_db_manager
from .database_utils import DatabaseUtils, test_connection, get_connection_info

__all__ = [
    'config',
    'DatabaseConfig', 
    'DatabaseManager',
    'get_db_manager',
    'DatabaseUtils',
    'test_connection',
    'get_connection_info'
]
