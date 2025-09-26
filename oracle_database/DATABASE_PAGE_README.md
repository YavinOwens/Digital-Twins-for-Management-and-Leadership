# Database Management Page

This page provides a comprehensive web-based interface for managing and interacting with your Oracle Database 23ai.

## Features

### 🔍 SQL Query Interface
- Execute SQL queries directly in the browser
- View results in an interactive data table
- Download query results as CSV files
- Query history tracking
- Support for both SELECT and non-SELECT queries

### 📊 Schema Browser
- Browse all database tables and their structure
- View table columns, data types, and constraints
- Examine indexes and their properties
- Navigate database objects easily

### 📋 Table Data Viewer
- View table data with pagination
- Selectable page sizes (10, 25, 50, 100 rows)
- Navigate through large datasets efficiently
- Real-time row count display

### 📈 Database Statistics
- Database version and connection information
- Table, view, index, and sequence counts
- Tablespace usage information
- Performance metrics

## Connection Details

The page automatically connects to your Oracle database using these settings:
- **Host**: localhost
- **Port**: 1521
- **Service Name**: FREEPDB1
- **Username**: web_knowledge
- **Password**: WebKnowledge2024!

## Usage Examples

### Basic Queries
```sql
-- View all tables
SELECT table_name FROM user_tables;

-- Check document count
SELECT COUNT(*) FROM documents;

-- View recent uploads
SELECT filename, upload_date FROM documents 
ORDER BY upload_date DESC 
FETCH FIRST 10 ROWS ONLY;
```

### Schema Exploration
```sql
-- Get table structure
SELECT column_name, data_type, nullable 
FROM user_tab_columns 
WHERE table_name = 'DOCUMENTS';

-- Check constraints
SELECT constraint_name, constraint_type 
FROM user_constraints 
WHERE table_name = 'DOCUMENTS';
```

## Security Features

- **Connection Security**: All passwords are securely stored
- **Query Validation**: Basic SQL injection protection
- **Session Management**: Automatic connection handling
- **Error Handling**: Graceful error display without exposing sensitive information

## Integration

This page integrates seamlessly with:
- Your existing Oracle Database 23ai setup
- The Web Knowledge System application
- Streamlit's session state management
- The database configuration system

## Troubleshooting

### Connection Issues
If you see "Database Disconnected":
1. Ensure Docker containers are running: `docker-compose ps`
2. Check database health: `docker-compose logs oracle-db`
3. Verify port 1521 is accessible: `netstat -an | grep 1521`

### Query Errors
- Check SQL syntax
- Ensure table names are correct (case-sensitive)
- Verify user permissions for the operation
- Check for typos in column names

### Performance
- Use LIMIT/FETCH for large result sets
- Add appropriate WHERE clauses
- Consider using indexes for frequently queried columns
- Monitor query execution time for complex operations
