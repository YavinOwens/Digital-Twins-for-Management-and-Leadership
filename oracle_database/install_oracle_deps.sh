#!/bin/bash

# Install Oracle Database dependencies for Web Knowledge System
# This script installs the required Python packages for Oracle Database connectivity

echo "Installing Oracle Database dependencies..."
echo "=========================================="

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed or not in PATH"
    exit 1
fi

# Check if pip is available
if ! command -v pip3 &> /dev/null; then
    echo "Error: pip3 is not installed or not in PATH"
    exit 1
fi

# Install Oracle Instant Client (macOS)
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Detected macOS - installing Oracle Instant Client..."
    
    # Check if Homebrew is installed
    if ! command -v brew &> /dev/null; then
        echo "Installing Homebrew..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    fi
    
    # Install Oracle Instant Client
    echo "Installing Oracle Instant Client via Homebrew..."
    brew install instantclient-basic instantclient-sdk
    
    # Set environment variables
    echo "Setting up environment variables..."
    export ORACLE_HOME=/opt/homebrew/lib/instantclient_21_8
    export DYLD_LIBRARY_PATH=$ORACLE_HOME:$DYLD_LIBRARY_PATH
    export PATH=$ORACLE_HOME:$PATH
    
    # Add to shell profile
    echo "" >> ~/.zshrc
    echo "# Oracle Instant Client" >> ~/.zshrc
    echo "export ORACLE_HOME=/opt/homebrew/lib/instantclient_21_8" >> ~/.zshrc
    echo "export DYLD_LIBRARY_PATH=\$ORACLE_HOME:\$DYLD_LIBRARY_PATH" >> ~/.zshrc
    echo "export PATH=\$ORACLE_HOME:\$PATH" >> ~/.zshrc
    
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "Detected Linux - installing Oracle Instant Client..."
    
    # Download and install Oracle Instant Client
    cd /tmp
    wget https://download.oracle.com/otn_software/linux/instantclient/2118000/instantclient-basic-linux.x64-21.18.0.0.0dbru.zip
    wget https://download.oracle.com/otn_software/linux/instantclient/2118000/instantclient-sdk-linux.x64-21.18.0.0.0dbru.zip
    
    # Unzip and install
    unzip instantclient-basic-linux.x64-21.18.0.0.0dbru.zip
    unzip instantclient-sdk-linux.x64-21.18.0.0.0dbru.zip
    
    sudo mkdir -p /opt/oracle
    sudo mv instantclient_21_8 /opt/oracle/
    
    # Set environment variables
    echo "Setting up environment variables..."
    export ORACLE_HOME=/opt/oracle/instantclient_21_8
    export LD_LIBRARY_PATH=$ORACLE_HOME:$LD_LIBRARY_PATH
    export PATH=$ORACLE_HOME:$PATH
    
    # Add to shell profile
    echo "" >> ~/.bashrc
    echo "# Oracle Instant Client" >> ~/.bashrc
    echo "export ORACLE_HOME=/opt/oracle/instantclient_21_8" >> ~/.bashrc
    echo "export LD_LIBRARY_PATH=\$ORACLE_HOME:\$LD_LIBRARY_PATH" >> ~/.bashrc
    echo "export PATH=\$ORACLE_HOME:\$PATH" >> ~/.bashrc
    
    # Update ldconfig
    echo "/opt/oracle/instantclient_21_8" | sudo tee /etc/ld.so.conf.d/oracle-instantclient.conf
    sudo ldconfig
    
else
    echo "Unsupported operating system: $OSTYPE"
    echo "Please install Oracle Instant Client manually"
    exit 1
fi

# Install Python packages
echo "Installing Python packages..."
pip3 install cx_Oracle==8.3.0
pip3 install oracledb==2.3.0

# Verify installation
echo "Verifying installation..."
python3 -c "import cx_Oracle; print('cx_Oracle version:', cx_Oracle.version)"
python3 -c "import oracledb; print('oracledb version:', oracledb.__version__)"

echo ""
echo "✅ Oracle Database dependencies installed successfully!"
echo ""
echo "Next steps:"
echo "1. Run ./setup_oracle_db.sh to set up the Oracle Database container"
echo "2. Run python init_database.py to initialize the database schema"
echo "3. Start using the database with your Web Knowledge System"
echo ""
echo "Note: You may need to restart your terminal or run 'source ~/.zshrc' (macOS) or 'source ~/.bashrc' (Linux) to load the environment variables."
