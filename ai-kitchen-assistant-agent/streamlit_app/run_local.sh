#!/bin/bash

# ============================================================================
# Local Testing Script for Streamlit App
# ============================================================================

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Recipe AI - Local Testing${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# Check if in correct directory
if [ ! -f "app.py" ]; then
    echo -e "${RED}Error: app.py not found${NC}"
    echo "Please run this script from the streamlit_app directory"
    exit 1
fi

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 not installed${NC}"
    exit 1
fi

echo -e "${YELLOW}Setting up environment...${NC}"

# Create venv if doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate venv
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt

echo -e "${GREEN}✓ Environment ready${NC}"
echo ""

# Check for .env file
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}Warning: .env file not found${NC}"
    echo "Creating from template..."
    cp .env.example .env
    echo ""
    echo -e "${RED}IMPORTANT: Edit .env file and set your PROJECT_ID${NC}"
    echo ""
    read -p "Press Enter to continue or Ctrl+C to cancel..."
fi

# Check for Google credentials
if [ -z "$GOOGLE_APPLICATION_CREDENTIALS" ]; then
    echo -e "${YELLOW}Warning: GOOGLE_APPLICATION_CREDENTIALS not set${NC}"
    echo ""
    echo "For local testing, you need a service account key:"
    echo "1. Go to: https://console.cloud.google.com/iam-admin/serviceaccounts"
    echo "2. Create or select a service account"
    echo "3. Create and download a JSON key"
    echo "4. Set environment variable:"
    echo "   export GOOGLE_APPLICATION_CREDENTIALS=/path/to/key.json"
    echo ""
    read -p "Do you have credentials configured? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Please configure credentials and try again"
        exit 1
    fi
fi

# Run configuration test
echo -e "${YELLOW}Testing configuration...${NC}"
python3 config.py

if [ $? -ne 0 ]; then
    echo -e "${RED}Configuration test failed${NC}"
    echo "Please fix errors in .env file"
    exit 1
fi

echo ""
echo -e "${GREEN}✓ Configuration valid${NC}"
echo ""

# Start Streamlit
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Starting Streamlit App${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "The app will open in your browser at:"
echo "http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

streamlit run app.py
