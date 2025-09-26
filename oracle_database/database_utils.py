"""
Database Utilities for Web Knowledge System

This module provides utility functions for database operations and management.
"""

import oracledb
import pandas as pd
import streamlit as st
from typing import List, Dict, Any, Optional
from oracle_database.database_config import config
from datetime import datetime
import json

class DatabaseUtils:
    """Utility class for database operations"""
    
    def __init__(self):
        self.config = config.get_app_connection_config()
        self.dsn = f"{self.config['host']}:{self.config['port']}/{self.config['service_name']}"
    
    def get_connection(self):
        """Get database connection"""
        return oracledb.connect(
            user=self.config['username'],
            password=self.config['password'],
            dsn=self.dsn
        )
    
    def execute_query(self, query: str, params: Dict = None) -> pd.DataFrame:
        """Execute SELECT query and return DataFrame"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                
                results = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]
                cursor.close()
                
                return pd.DataFrame(results, columns=columns)
        except Exception as e:
            st.error(f"Query execution failed: {e}")
            return pd.DataFrame()
    
    def execute_non_query(self, query: str, params: Dict = None) -> bool:
        """Execute non-SELECT query (INSERT, UPDATE, DELETE)"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                conn.commit()
                cursor.close()
                return True
        except Exception as e:
            st.error(f"Query execution failed: {e}")
            return False
    
    def get_table_info(self, table_name: str) -> Dict[str, Any]:
        """Get detailed information about a table"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Get column information
                cursor.execute(f"""
                    SELECT column_name, data_type, data_length, nullable, data_default
                    FROM user_tab_columns
                    WHERE table_name = '{table_name.upper()}'
                    ORDER BY column_id
                """)
                columns = cursor.fetchall()
                
                # Get row count
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                row_count = cursor.fetchone()[0]
                
                # Get constraints
                cursor.execute(f"""
                    SELECT constraint_name, constraint_type, status
                    FROM user_constraints
                    WHERE table_name = '{table_name.upper()}'
                """)
                constraints = cursor.fetchall()
                
                cursor.close()
                
                return {
                    'columns': columns,
                    'row_count': row_count,
                    'constraints': constraints
                }
        except Exception as e:
            st.error(f"Failed to get table info: {e}")
            return {}
    
    def get_database_stats(self) -> Dict[str, Any]:
        """Get database statistics"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                stats = {}
                
                # Table count
                cursor.execute("SELECT COUNT(*) FROM user_tables")
                stats['table_count'] = cursor.fetchone()[0]
                
                # View count
                cursor.execute("SELECT COUNT(*) FROM user_views")
                stats['view_count'] = cursor.fetchone()[0]
                
                # Index count
                cursor.execute("SELECT COUNT(*) FROM user_indexes")
                stats['index_count'] = cursor.fetchone()[0]
                
                # Sequence count
                cursor.execute("SELECT COUNT(*) FROM user_sequences")
                stats['sequence_count'] = cursor.fetchone()[0]
                
                # Database version
                cursor.execute("SELECT banner FROM v$version WHERE banner LIKE '%Oracle%'")
                stats['version'] = cursor.fetchone()[0]
                
                cursor.close()
                return stats
        except Exception as e:
            st.error(f"Failed to get database stats: {e}")
            return {}
    
    def get_recent_queries(self) -> List[Dict[str, Any]]:
        """Get recent query history from session state"""
        if "query_history" not in st.session_state:
            return []
        return st.session_state.query_history
    
    def save_query_to_history(self, query: str):
        """Save query to history"""
        if "query_history" not in st.session_state:
            st.session_state.query_history = []
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.query_history.append({
            'timestamp': timestamp,
            'query': query
        })
        
        # Keep only last 50 queries
        if len(st.session_state.query_history) > 50:
            st.session_state.query_history = st.session_state.query_history[-50:]

def get_database_utils() -> DatabaseUtils:
    """Get DatabaseUtils instance"""
    return DatabaseUtils()

def test_connection() -> bool:
    """Test database connection"""
    try:
        utils = DatabaseUtils()
        with utils.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM DUAL")
            cursor.fetchone()
            cursor.close()
        return True
    except Exception:
        return False

def get_connection_info() -> Dict[str, str]:
    """Get connection information"""
    config_obj = config.get_app_connection_config()
    return {
        'host': config_obj['host'],
        'port': str(config_obj['port']),
        'service_name': config_obj['service_name'],
        'username': config_obj['username'],
        'dsn': config_obj['dsn']
    }
