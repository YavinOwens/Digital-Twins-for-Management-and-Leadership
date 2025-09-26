"""
Database Connection Utilities for Web Knowledge System
Provides connection management and utility functions for Oracle Database 23ai
"""

import oracledb
import logging
import json
from typing import Dict, Any, List, Optional, Union
from contextlib import contextmanager
from .database_config import config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseConnection:
    """Manages Oracle Database connections with connection pooling"""
    
    def __init__(self, connection_config: Dict[str, Any] = None):
        self.config = connection_config or config.get_app_connection_config()
        self.pool = None
        self._initialize_pool()
    
    def _initialize_pool(self):
        """Initialize connection pool"""
        try:
            dsn = f"{self.config['host']}:{self.config['port']}/{self.config['service_name']}"
            
            self.pool = oracledb.create_pool(
                user=self.config['username'],
                password=self.config['password'],
                dsn=dsn,
                min=1,
                max=10,
                increment=1
            )
            logger.info("Database connection pool initialized successfully")
        except oracledb.Error as e:
            logger.error(f"Failed to initialize connection pool: {e}")
            self.pool = None
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        connection = None
        try:
            if self.pool:
                connection = self.pool.acquire()
            else:
                # Fallback to direct connection
                dsn = cx_Oracle.makedsn(
                    self.config['host'],
                    self.config['port'],
                    service_name=self.config['service_name']
                )
                connection = cx_Oracle.connect(
                    self.config['username'],
                    self.config['password'],
                    dsn
                )
            yield connection
        except cx_Oracle.Error as e:
            logger.error(f"Database connection error: {e}")
            if connection:
                connection.rollback()
            raise
        finally:
            if connection and self.pool:
                self.pool.release(connection)
            elif connection:
                connection.close()
    
    def execute_query(self, sql: str, params: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Execute SELECT query and return results as list of dictionaries"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(sql, params or {})
                
                # Get column names
                columns = [desc[0] for desc in cursor.description]
                
                # Fetch all results
                results = []
                for row in cursor.fetchall():
                    results.append(dict(zip(columns, row)))
                
                cursor.close()
                return results
        except cx_Oracle.Error as e:
            logger.error(f"Query execution failed: {e}")
            logger.error(f"SQL: {sql}")
            raise
    
    def execute_update(self, sql: str, params: Dict[str, Any] = None) -> int:
        """Execute INSERT/UPDATE/DELETE and return number of affected rows"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(sql, params or {})
                conn.commit()
                rowcount = cursor.rowcount
                cursor.close()
                return rowcount
        except cx_Oracle.Error as e:
            logger.error(f"Update execution failed: {e}")
            logger.error(f"SQL: {sql}")
            raise
    
    def execute_batch(self, sql: str, params_list: List[Dict[str, Any]]) -> int:
        """Execute batch operations"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.executemany(sql, params_list)
                conn.commit()
                rowcount = cursor.rowcount
                cursor.close()
                return rowcount
        except cx_Oracle.Error as e:
            logger.error(f"Batch execution failed: {e}")
            logger.error(f"SQL: {sql}")
            raise
    
    def get_sequence_nextval(self, sequence_name: str) -> int:
        """Get next value from sequence"""
        sql = f"SELECT {sequence_name}.NEXTVAL FROM DUAL"
        result = self.execute_query(sql)
        return result[0]['NEXTVAL']
    
    def close_pool(self):
        """Close the connection pool"""
        if self.pool:
            self.pool.close()
            logger.info("Connection pool closed")

class DatabaseManager:
    """High-level database operations for the Web Knowledge System"""
    
    def __init__(self, connection_config: Dict[str, Any] = None):
        self.db = DatabaseConnection(connection_config)
    
    # Document operations
    def save_document(self, filename: str, file_path: str, file_type: str, 
                     file_size: int, metadata: Dict[str, Any] = None, 
                     content_hash: str = None, created_by: str = None) -> int:
        """Save document metadata to database"""
        sql = """
        INSERT INTO documents (filename, file_path, file_type, file_size, 
                              metadata, content_hash, created_by)
        VALUES (:filename, :file_path, :file_type, :file_size, 
                :metadata, :content_hash, :created_by)
        RETURNING document_id INTO :doc_id
        """
        
        params = {
            'filename': filename,
            'file_path': file_path,
            'file_type': file_type,
            'file_size': file_size,
            'metadata': json.dumps(metadata) if metadata else None,
            'content_hash': content_hash,
            'created_by': created_by
        }
        
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            doc_id = cursor.var(cx_Oracle.NUMBER)
            params['doc_id'] = doc_id
            cursor.execute(sql, params)
            conn.commit()
            return int(doc_id.getvalue()[0])
    
    def get_document(self, document_id: int) -> Optional[Dict[str, Any]]:
        """Get document by ID"""
        sql = "SELECT * FROM documents WHERE document_id = :doc_id"
        results = self.db.execute_query(sql, {'doc_id': document_id})
        return results[0] if results else None
    
    def update_document_status(self, document_id: int, status: str) -> bool:
        """Update document processing status"""
        sql = """
        UPDATE documents 
        SET status = :status, processed_date = CURRENT_TIMESTAMP 
        WHERE document_id = :doc_id
        """
        try:
            self.db.execute_update(sql, {'doc_id': document_id, 'status': status})
            return True
        except Exception as e:
            logger.error(f"Failed to update document status: {e}")
            return False
    
    def save_document_chunk(self, document_id: int, chunk_text: str, 
                           chunk_index: int, embedding_vector: str = None,
                           metadata: Dict[str, Any] = None) -> int:
        """Save document chunk"""
        sql = """
        INSERT INTO document_chunks (document_id, chunk_text, chunk_index, 
                                    chunk_size, embedding_vector, metadata)
        VALUES (:doc_id, :chunk_text, :chunk_index, :chunk_size, 
                :embedding_vector, :metadata)
        RETURNING chunk_id INTO :chunk_id
        """
        
        params = {
            'doc_id': document_id,
            'chunk_text': chunk_text,
            'chunk_index': chunk_index,
            'chunk_size': len(chunk_text),
            'embedding_vector': embedding_vector,
            'metadata': json.dumps(metadata) if metadata else None
        }
        
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            chunk_id = cursor.var(cx_Oracle.NUMBER)
            params['chunk_id'] = chunk_id
            cursor.execute(sql, params)
            conn.commit()
            return int(chunk_id.getvalue()[0])
    
    # Agent task operations
    def create_task(self, task_name: str, task_type: str, description: str = None,
                   priority: int = 5, assigned_agent: str = None) -> int:
        """Create new agent task"""
        sql = """
        INSERT INTO agent_tasks (task_name, task_type, description, 
                               priority, assigned_agent)
        VALUES (:task_name, :task_type, :description, :priority, :assigned_agent)
        RETURNING task_id INTO :task_id
        """
        
        params = {
            'task_name': task_name,
            'task_type': task_type,
            'description': description,
            'priority': priority,
            'assigned_agent': assigned_agent
        }
        
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            task_id = cursor.var(cx_Oracle.NUMBER)
            params['task_id'] = task_id
            cursor.execute(sql, params)
            conn.commit()
            return int(task_id.getvalue()[0])
    
    def update_task_status(self, task_id: int, status: str, 
                          result_data: Dict[str, Any] = None,
                          error_message: str = None) -> bool:
        """Update task status"""
        sql = """
        UPDATE agent_tasks 
        SET status = :status, 
            result_data = :result_data,
            error_message = :error_message,
            completed_date = CASE WHEN :status = 'COMPLETED' THEN CURRENT_TIMESTAMP ELSE completed_date END
        WHERE task_id = :task_id
        """
        
        params = {
            'task_id': task_id,
            'status': status,
            'result_data': json.dumps(result_data) if result_data else None,
            'error_message': error_message
        }
        
        try:
            self.db.execute_update(sql, params)
            return True
        except Exception as e:
            logger.error(f"Failed to update task status: {e}")
            return False
    
    # Memory operations
    def save_memory(self, agent_name: str, memory_type: str, memory_key: str,
                   memory_value: Any, expires_date: str = None) -> bool:
        """Save agent memory"""
        sql = """
        MERGE INTO agent_memory m
        USING (SELECT :agent_name as agent_name, :memory_type as memory_type, 
                      :memory_key as memory_key FROM DUAL) s
        ON (m.agent_name = s.agent_name AND m.memory_type = s.memory_type 
            AND m.memory_key = s.memory_key)
        WHEN MATCHED THEN
            UPDATE SET memory_value = :memory_value,
                      last_accessed = CURRENT_TIMESTAMP,
                      access_count = access_count + 1,
                      expires_date = :expires_date
        WHEN NOT MATCHED THEN
            INSERT (agent_name, memory_type, memory_key, memory_value, expires_date)
            VALUES (:agent_name, :memory_type, :memory_key, :memory_value, :expires_date)
        """
        
        params = {
            'agent_name': agent_name,
            'memory_type': memory_type,
            'memory_key': memory_key,
            'memory_value': json.dumps(memory_value),
            'expires_date': expires_date
        }
        
        try:
            self.db.execute_update(sql, params)
            return True
        except Exception as e:
            logger.error(f"Failed to save memory: {e}")
            return False
    
    def get_memory(self, agent_name: str, memory_type: str, memory_key: str) -> Optional[Any]:
        """Get agent memory"""
        sql = """
        SELECT memory_value FROM agent_memory 
        WHERE agent_name = :agent_name 
        AND memory_type = :memory_type 
        AND memory_key = :memory_key
        AND (expires_date IS NULL OR expires_date > CURRENT_TIMESTAMP)
        """
        
        params = {
            'agent_name': agent_name,
            'memory_type': memory_type,
            'memory_key': memory_key
        }
        
        try:
            results = self.db.execute_query(sql, params)
            if results:
                # Update access count
                update_sql = """
                UPDATE agent_memory 
                SET last_accessed = CURRENT_TIMESTAMP, access_count = access_count + 1
                WHERE agent_name = :agent_name 
                AND memory_type = :memory_type 
                AND memory_key = :memory_key
                """
                self.db.execute_update(update_sql, params)
                return json.loads(results[0]['memory_value'])
            return None
        except Exception as e:
            logger.error(f"Failed to get memory: {e}")
            return None
    
    # Configuration operations
    def get_config(self, config_key: str) -> Optional[str]:
        """Get system configuration value"""
        sql = "SELECT config_value FROM system_config WHERE config_key = :key AND is_active = 'Y'"
        results = self.db.execute_query(sql, {'key': config_key})
        return results[0]['config_value'] if results else None
    
    def set_config(self, config_key: str, config_value: str, 
                   config_type: str = 'STRING', description: str = None) -> bool:
        """Set system configuration value"""
        sql = """
        MERGE INTO system_config s
        USING (SELECT :config_key as config_key FROM DUAL) k
        ON (s.config_key = k.config_key)
        WHEN MATCHED THEN
            UPDATE SET config_value = :config_value,
                      config_type = :config_type,
                      description = :description,
                      updated_date = CURRENT_TIMESTAMP
        WHEN NOT MATCHED THEN
            INSERT (config_key, config_value, config_type, description)
            VALUES (:config_key, :config_value, :config_type, :description)
        """
        
        params = {
            'config_key': config_key,
            'config_value': config_value,
            'config_type': config_type,
            'description': description
        }
        
        try:
            self.db.execute_update(sql, params)
            return True
        except Exception as e:
            logger.error(f"Failed to set config: {e}")
            return False
    
    def close(self):
        """Close database connections"""
        self.db.close_pool()

# Global database manager instance
db_manager = DatabaseManager()

def get_db_manager() -> DatabaseManager:
    """Get the global database manager instance"""
    return db_manager
