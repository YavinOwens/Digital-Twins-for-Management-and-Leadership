#!/bin/bash

# Oracle Database 23ai Docker Setup Script
# This script sets up Oracle Database 23ai using Docker for the Web Knowledge System

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
CONTAINER_NAME="oracle-23ai"
IMAGE_NAME="container-registry.oracle.com/database/free:latest"
DB_PORT=1521
EM_PORT=5500
VOLUME_NAME="oracle_data"
DEFAULT_PASSWORD="WebKnowledge2024!"

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if Docker is running
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker and try again."
        exit 1
    fi
    print_success "Docker is running"
}

# Function to check if container already exists
check_existing_container() {
    if docker ps -a --format "table {{.Names}}" | grep -q "^${CONTAINER_NAME}$"; then
        print_warning "Container '${CONTAINER_NAME}' already exists"
        echo "Do you want to remove the existing container and create a new one? (y/N)"
        read -r response
        if [[ "$response" =~ ^[Yy]$ ]]; then
            print_status "Stopping and removing existing container..."
            docker stop "${CONTAINER_NAME}" 2>/dev/null || true
            docker rm "${CONTAINER_NAME}" 2>/dev/null || true
            print_success "Existing container removed"
        else
            print_status "Using existing container"
            return 0
        fi
    fi
    return 1
}

# Function to pull Oracle image
pull_oracle_image() {
    print_status "Pulling Oracle Database 23ai image..."
    if docker pull "${IMAGE_NAME}"; then
        print_success "Oracle image pulled successfully"
    else
        print_error "Failed to pull Oracle image"
        exit 1
    fi
}

# Function to create and start container
create_container() {
    local password="$1"
    
    print_status "Creating Oracle Database 23ai container..."
    print_status "Container name: ${CONTAINER_NAME}"
    print_status "Database port: ${DB_PORT}"
    print_status "Enterprise Manager port: ${EM_PORT}"
    print_status "Volume: ${VOLUME_NAME}"
    
    # Create the container
    docker run -d \
        --name "${CONTAINER_NAME}" \
        -p "${DB_PORT}:${DB_PORT}" \
        -p "${EM_PORT}:${EM_PORT}" \
        -e ORACLE_PWD="${password}" \
        -e ORACLE_CHARACTERSET=AL32UTF8 \
        -v "${VOLUME_NAME}:/opt/oracle/oradata" \
        "${IMAGE_NAME}"
    
    if [ $? -eq 0 ]; then
        print_success "Container created and started successfully"
    else
        print_error "Failed to create container"
        exit 1
    fi
}

# Function to wait for database to be ready
wait_for_database() {
    print_status "Waiting for Oracle Database to be ready..."
    print_status "This may take several minutes on first startup..."
    
    local max_attempts=60
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        if docker exec "${CONTAINER_NAME}" sqlplus -s / as sysdba <<< "SELECT 1 FROM DUAL;" > /dev/null 2>&1; then
            print_success "Database is ready!"
            return 0
        fi
        
        echo -n "."
        sleep 10
        ((attempt++))
    done
    
    print_error "Database did not become ready within expected time"
    print_status "You can check the container logs with: docker logs ${CONTAINER_NAME}"
    exit 1
}

# Function to show connection information
show_connection_info() {
    local password="$1"
    
    echo ""
    echo "=========================================="
    echo "Oracle Database 23ai Setup Complete!"
    echo "=========================================="
    echo ""
    echo "Container Information:"
    echo "  Name: ${CONTAINER_NAME}"
    echo "  Status: $(docker ps --format "table {{.Status}}" --filter "name=${CONTAINER_NAME}")"
    echo ""
    echo "Connection Information:"
    echo "  Host: localhost"
    echo "  Port: ${DB_PORT}"
    echo "  Service Name: FREE"
    echo "  PDB Name: FREEPDB1"
    echo ""
    echo "Default Accounts:"
    echo "  SYS: sys/${password}@FREE as sysdba"
    echo "  SYSTEM: system/${password}@FREE"
    echo "  PDBADMIN: pdbadmin/${password}@FREEPDB1"
    echo ""
    echo "Enterprise Manager Express:"
    echo "  URL: http://localhost:${EM_PORT}/em"
    echo "  Username: sys"
    echo "  Password: ${password}"
    echo ""
    echo "Useful Commands:"
    echo "  Connect to database: docker exec -it ${CONTAINER_NAME} sqlplus sys/${password}@FREE as sysdba"
    echo "  Connect to PDB: docker exec -it ${CONTAINER_NAME} sqlplus pdbadmin/${password}@FREEPDB1"
    echo "  View logs: docker logs ${CONTAINER_NAME}"
    echo "  Stop container: docker stop ${CONTAINER_NAME}"
    echo "  Start container: docker start ${CONTAINER_NAME}"
    echo "  Remove container: docker rm ${CONTAINER_NAME}"
    echo ""
}

# Function to create application user
create_app_user() {
    local password="$1"
    
    print_status "Creating application user..."
    
    docker exec "${CONTAINER_NAME}" sqlplus -s sys/"${password}"@FREE as sysdba <<EOF
-- Create application user
CREATE USER web_knowledge IDENTIFIED BY WebKnowledge2024!
DEFAULT TABLESPACE users
TEMPORARY TABLESPACE temp
QUOTA 500M ON users;

-- Grant necessary privileges
GRANT CONNECT, RESOURCE TO web_knowledge;
GRANT CREATE SESSION TO web_knowledge;
GRANT CREATE TABLE TO web_knowledge;
GRANT CREATE SEQUENCE TO web_knowledge;
GRANT CREATE PROCEDURE TO web_knowledge;
GRANT CREATE TRIGGER TO web_knowledge;
GRANT CREATE VIEW TO web_knowledge;

-- Grant privileges on PDB
ALTER SESSION SET CONTAINER=FREEPDB1;

CREATE USER web_knowledge IDENTIFIED BY WebKnowledge2024!
DEFAULT TABLESPACE users
TEMPORARY TABLESPACE temp
QUOTA 500M ON users;

GRANT CONNECT, RESOURCE TO web_knowledge;
GRANT CREATE SESSION TO web_knowledge;
GRANT CREATE TABLE TO web_knowledge;
GRANT CREATE SEQUENCE TO web_knowledge;
GRANT CREATE PROCEDURE TO web_knowledge;
GRANT CREATE TRIGGER TO web_knowledge;
GRANT CREATE VIEW TO web_knowledge;

EXIT;
EOF

    if [ $? -eq 0 ]; then
        print_success "Application user 'web_knowledge' created successfully"
    else
        print_warning "Failed to create application user. You can create it manually later."
    fi
}

# Main execution
main() {
    echo "Oracle Database 23ai Setup for Web Knowledge System"
    echo "=================================================="
    echo ""
    
    # Get password from user
    echo "Enter password for Oracle Database (default: ${DEFAULT_PASSWORD}):"
    read -r password
    password=${password:-$DEFAULT_PASSWORD}
    
    # Validate password
    if [ ${#password} -lt 8 ]; then
        print_error "Password must be at least 8 characters long"
        exit 1
    fi
    
    # Check Docker
    check_docker
    
    # Check for existing container
    if check_existing_container; then
        print_status "Container already exists and is ready"
        show_connection_info "$password"
        exit 0
    fi
    
    # Pull image
    pull_oracle_image
    
    # Create container
    create_container "$password"
    
    # Wait for database
    wait_for_database
    
    # Create application user
    create_app_user "$password"
    
    # Show connection information
    show_connection_info "$password"
    
    print_success "Oracle Database 23ai setup completed successfully!"
}

# Run main function
main "$@"
