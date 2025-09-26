"""
Database Management Page - Oracle Database Interface

This page provides a web-based interface for managing and querying the Oracle database.
"""

import streamlit as st
import pandas as pd
import oracledb
from oracle_database.database_config import config
from oracle_database.database_manager import get_db_manager
from oracle_database.database_utils import DatabaseUtils, test_connection, get_connection_info
from shared.components import create_header, create_footer, create_sidebar_info
import json
from datetime import datetime

def main():
    """Main function for the Database Management page"""
    
    # Page configuration
    st.set_page_config(
        page_title="Digital Twins Management System - Database",
        page_icon="🗄️",
        layout="wide"
    )
    
    # Create header
    create_header("Oracle Database Management", "🗄️")
    
    # Sidebar
    with st.sidebar:
        create_sidebar_info()
        
        st.header("🗄️ Database Tools")
        st.markdown("""
        **Available Tools:**
        - SQL Query Interface
        - Schema Browser
        - Table Data Viewer
        - Database Statistics
        - Connection Status
        """)
        
        # Connection status
        if test_connection():
            st.success("✅ Database Connected")
            conn_info = get_connection_info()
            st.info(f"**Host:** {conn_info['host']}:{conn_info['port']}")
            st.info(f"**Service:** {conn_info['service_name']}")
            st.info(f"**User:** {conn_info['username']}")
        else:
            st.error("❌ Database Disconnected")
    
    # Main content
    tab1, tab2, tab3, tab4 = st.tabs(["🔍 SQL Query", "📊 Schema Browser", "📋 Table Data", "📈 Statistics"])
    
    with tab1:
        sql_query_interface()
    
    with tab2:
        schema_browser()
    
    with tab3:
        table_data_viewer()
    
    with tab4:
        database_statistics()


def sql_query_interface():
    """SQL Query Interface"""
    st.markdown("### 🔍 SQL Query Interface")
    st.markdown("Execute SQL queries against your Oracle database.")
    
    # Query input
    query = st.text_area(
        "Enter your SQL query:",
        height=200,
        placeholder="SELECT * FROM documents LIMIT 10;"
    )
    
    col1, col2, col3 = st.columns([1, 1, 4])
    
    with col1:
        execute_button = st.button("▶️ Execute", type="primary")
    
    with col2:
        clear_button = st.button("🗑️ Clear")
    
    if clear_button:
        st.rerun()
    
    if execute_button and query.strip():
        execute_sql_query(query)
    
    # Query history
    if "query_history" not in st.session_state:
        st.session_state.query_history = []
    
    if st.session_state.query_history:
        with st.expander("📜 Query History", expanded=False):
            for i, (timestamp, q) in enumerate(reversed(st.session_state.query_history[-10:])):
                if st.button(f"{timestamp}: {q[:50]}...", key=f"history_{i}"):
                    st.session_state.current_query = q
                    st.rerun()

def execute_sql_query(query):
    """Execute SQL query and display results"""
    utils = DatabaseUtils()
    
    # Check if it's a SELECT query
    if query.strip().upper().startswith('SELECT'):
        df = utils.execute_query(query)
        
        if not df.empty:
            st.success(f"✅ Query executed successfully! Found {len(df)} rows.")
            st.dataframe(df, use_container_width=True)
            
            # Download option
            csv = df.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name=f"query_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        else:
            st.info("Query executed successfully but returned no results.")
    else:
        # Non-SELECT query
        success = utils.execute_non_query(query)
        if success:
            st.success("✅ Query executed successfully!")
    
    # Add to history
    utils.save_query_to_history(query)

def schema_browser():
    """Schema Browser"""
    st.markdown("### 📊 Schema Browser")
    st.markdown("Browse database schema and objects.")
    
    try:
        conn_config = config.get_app_connection_config()
        dsn = f"{conn_config['host']}:{conn_config['port']}/{conn_config['service_name']}"
        
        with oracledb.connect(
            user=conn_config['username'],
            password=conn_config['password'],
            dsn=dsn
        ) as conn:
            cursor = conn.cursor()
            
            # Get tables
            cursor.execute("""
                SELECT table_name, num_rows, last_analyzed
                FROM user_tables
                ORDER BY table_name
            """)
            tables = cursor.fetchall()
            
            if tables:
                st.markdown("#### 📋 Tables")
                table_df = pd.DataFrame(tables, columns=['Table Name', 'Rows', 'Last Analyzed'])
                st.dataframe(table_df, use_container_width=True)
                
                # Table details
                selected_table = st.selectbox("Select a table to view details:", [t[0] for t in tables])
                
                if selected_table:
                    # Get table columns
                    cursor.execute(f"""
                        SELECT column_name, data_type, data_length, nullable
                        FROM user_tab_columns
                        WHERE table_name = '{selected_table}'
                        ORDER BY column_id
                    """)
                    columns = cursor.fetchall()
                    
                    if columns:
                        st.markdown(f"#### 🔍 Columns in {selected_table}")
                        col_df = pd.DataFrame(columns, columns=['Column Name', 'Data Type', 'Length', 'Nullable'])
                        st.dataframe(col_df, use_container_width=True)
            
            # Get indexes
            cursor.execute("""
                SELECT index_name, table_name, uniqueness, status
                FROM user_indexes
                ORDER BY table_name, index_name
            """)
            indexes = cursor.fetchall()
            
            if indexes:
                st.markdown("#### 🔗 Indexes")
                idx_df = pd.DataFrame(indexes, columns=['Index Name', 'Table', 'Uniqueness', 'Status'])
                st.dataframe(idx_df, use_container_width=True)
            
            cursor.close()
            
    except Exception as e:
        st.error(f"❌ Schema browsing failed: {str(e)}")

def table_data_viewer():
    """Table Data Viewer"""
    st.markdown("### 📋 Table Data Viewer")
    st.markdown("View and explore table data.")
    
    try:
        conn_config = config.get_app_connection_config()
        dsn = f"{conn_config['host']}:{conn_config['port']}/{conn_config['service_name']}"
        
        with oracledb.connect(
            user=conn_config['username'],
            password=conn_config['password'],
            dsn=dsn
        ) as conn:
            cursor = conn.cursor()
            
            # Get available tables
            cursor.execute("SELECT table_name FROM user_tables ORDER BY table_name")
            tables = [row[0] for row in cursor.fetchall()]
            
            if tables:
                selected_table = st.selectbox("Select a table:", tables)
                
                if selected_table:
                    # Get row count
                    cursor.execute(f"SELECT COUNT(*) FROM {selected_table}")
                    row_count = cursor.fetchone()[0]
                    
                    st.info(f"Table **{selected_table}** has **{row_count:,}** rows.")
                    
                    # Pagination
                    page_size = st.selectbox("Rows per page:", [10, 25, 50, 100], index=1)
                    page = st.number_input("Page:", min_value=1, value=1)
                    
                    offset = (page - 1) * page_size
                    
                    # Fetch data
                    query = f"SELECT * FROM {selected_table} ORDER BY ROWNUM OFFSET {offset} ROWS FETCH NEXT {page_size} ROWS ONLY"
                    cursor.execute(query)
                    
                    results = cursor.fetchall()
                    columns = [desc[0] for desc in cursor.description]
                    
                    if results:
                        df = pd.DataFrame(results, columns=columns)
                        st.dataframe(df, use_container_width=True)
                        
                        # Pagination info
                        total_pages = (row_count + page_size - 1) // page_size
                        st.info(f"Showing page {page} of {total_pages} (rows {offset + 1} to {min(offset + page_size, row_count)})")
                    else:
                        st.info("No data found.")
            
            cursor.close()
            
    except Exception as e:
        st.error(f"❌ Table data viewing failed: {str(e)}")

def database_statistics():
    """Database Statistics"""
    st.markdown("### 📈 Database Statistics")
    st.markdown("View database performance and usage statistics.")
    
    try:
        conn_config = config.get_app_connection_config()
        dsn = f"{conn_config['host']}:{conn_config['port']}/{conn_config['service_name']}"
        
        with oracledb.connect(
            user=conn_config['username'],
            password=conn_config['password'],
            dsn=dsn
        ) as conn:
            cursor = conn.cursor()
            
            # Database info
            cursor.execute("SELECT * FROM v$version WHERE banner LIKE '%Oracle%'")
            version = cursor.fetchone()[0]
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 🗄️ Database Information")
                st.info(f"**Version:** {version}")
                st.info(f"**Host:** {conn_config['host']}")
                st.info(f"**Port:** {conn_config['port']}")
                st.info(f"**Service:** {conn_config['service_name']}")
                st.info(f"**User:** {conn_config['username']}")
            
            with col2:
                st.markdown("#### 📊 Object Statistics")
                
                # Table counts
                cursor.execute("SELECT COUNT(*) FROM user_tables")
                table_count = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM user_views")
                view_count = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM user_indexes")
                index_count = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM user_sequences")
                sequence_count = cursor.fetchone()[0]
                
                # Get total row count across all tables
                cursor.execute("""
                    SELECT SUM(num_rows) 
                    FROM user_tables 
                    WHERE num_rows IS NOT NULL
                """)
                total_rows = cursor.fetchone()[0] or 0
                
                st.metric("Tables", table_count)
                st.metric("Views", view_count)
                st.metric("Indexes", index_count)
                st.metric("Sequences", sequence_count)
                st.metric("Total Rows", f"{total_rows:,}")
            
            # Space usage
            st.markdown("#### 💾 Space Usage")
            try:
                cursor.execute("""
                    SELECT 
                        tablespace_name,
                        ROUND(bytes/1024/1024, 2) as used_mb,
                        CASE 
                            WHEN max_bytes = -1 THEN 'UNLIMITED'
                            ELSE ROUND(max_bytes/1024/1024, 2) || ' MB'
                        END as max_size
                    FROM user_ts_quotas
                    WHERE bytes > 0
                """)
                space_usage = cursor.fetchall()
                
                if space_usage:
                    space_df = pd.DataFrame(space_usage, columns=['Tablespace', 'Used (MB)', 'Max Size'])
                    st.dataframe(space_df, use_container_width=True)
                else:
                    st.info("No tablespace quota information available.")
            except Exception as space_error:
                # Fallback to simpler query if max_bytes column doesn't exist
                cursor.execute("""
                    SELECT 
                        tablespace_name,
                        ROUND(bytes/1024/1024, 2) as used_mb
                    FROM user_ts_quotas
                    WHERE bytes > 0
                """)
                space_usage = cursor.fetchall()
                
                if space_usage:
                    space_df = pd.DataFrame(space_usage, columns=['Tablespace', 'Used (MB)'])
                    st.dataframe(space_df, use_container_width=True)
                else:
                    st.info("No tablespace quota information available.")
            
            # Top tables by row count
            st.markdown("#### 📋 Largest Tables")
            try:
                cursor.execute("""
                    SELECT table_name, num_rows
                    FROM user_tables
                    WHERE num_rows IS NOT NULL AND num_rows > 0
                    ORDER BY num_rows DESC
                    FETCH FIRST 10 ROWS ONLY
                """)
                top_tables = cursor.fetchall()
                
                if top_tables:
                    tables_df = pd.DataFrame(top_tables, columns=['Table Name', 'Row Count'])
                    st.dataframe(tables_df, use_container_width=True)
                else:
                    st.info("No table statistics available.")
            except Exception as table_error:
                st.info("Table statistics not available.")
            
            cursor.close()
            
    except Exception as e:
        st.error(f"❌ Statistics retrieval failed: {str(e)}")
    
    # Create footer
    create_footer()

if __name__ == "__main__":
    main()
