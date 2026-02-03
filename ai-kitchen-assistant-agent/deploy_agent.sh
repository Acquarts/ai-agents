#!/bin/bash

# ============================================================================
# Deploy Recipe Multi-Agent to Vertex AI Agent Engine
# ============================================================================

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ============================================================================
# Load environment variables
# ============================================================================

if [ -f .env ]; then
    echo -e "${YELLOW}Loading .env file...${NC}"
    export $(cat .env | grep -v '^#' | xargs)
fi

# ============================================================================
# Configuration
# ============================================================================

# Get project ID from environment or gcloud config or command line
PROJECT_ID=${PROJECT_ID:-$(gcloud config get-value project)}
PROJECT_ID=${1:-$PROJECT_ID}

if [ -z "$PROJECT_ID" ]; then
    echo -e "${RED}Error: No project ID provided${NC}"
    echo "Usage: ./deploy_agent.sh YOUR_PROJECT_ID [REGION]"
    echo "Or set PROJECT_ID in .env file"
    exit 1
fi

# Region (default: us-central1)
REGION=${2:-${REGION:-us-central1}}

# Agent configuration
AGENT_NAME=${AGENT_NAME:-recipe_coordinator}
DISPLAY_NAME="Recipe Coordinator Multi-Agent"

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Deploying Recipe Multi-Agent${NC}"
echo -e "${GREEN}========================================${NC}"
echo "Project ID: $PROJECT_ID"
echo "Region: $REGION"
echo "Agent Name: $AGENT_NAME"
echo ""

# ============================================================================
# Check prerequisites
# ============================================================================

echo -e "${YELLOW}Checking prerequisites...${NC}"

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo -e "${RED}Error: gcloud CLI not installed${NC}"
    echo "Install from: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 not installed${NC}"
    exit 1
fi

# Check if agents.py exists
if [ ! -f "agents.py" ]; then
    echo -e "${RED}Error: agents.py not found${NC}"
    echo "Make sure you're in the project root directory"
    exit 1
fi

echo -e "${GREEN}✓ Prerequisites OK${NC}"
echo ""

# ============================================================================
# Setup Python environment
# ============================================================================

echo -e "${YELLOW}Setting up Python environment...${NC}"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt

echo -e "${GREEN}✓ Python environment ready${NC}"
echo ""

# ============================================================================
# Enable required APIs
# ============================================================================

echo -e "${YELLOW}Enabling required APIs...${NC}"

gcloud services enable \
    aiplatform.googleapis.com \
    cloudfunctions.googleapis.com \
    cloudbuild.googleapis.com \
    --project=$PROJECT_ID \
    --quiet

echo -e "${GREEN}✓ APIs enabled${NC}"
echo ""

# ============================================================================
# Validate agent configuration
# ============================================================================

echo -e "${YELLOW}Validating agent configuration...${NC}"

python3 << 'END_PYTHON'
import sys
try:
    from agents import root_agent, food_analyzer, recipe_generator
    
    print(f"✓ Root agent loaded: {root_agent.name}")
    print(f"  - Model: {root_agent.model}")
    print(f"  - Subagents: {len(root_agent.sub_agents)}")
    
    for subagent in root_agent.sub_agents:
        print(f"    • {subagent.name}")
    
    print("\n✓ Agent configuration valid")
except Exception as e:
    print(f"✗ Error validating agents: {e}", file=sys.stderr)
    sys.exit(1)
END_PYTHON

if [ $? -ne 0 ]; then
    echo -e "${RED}Agent validation failed${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Agent configuration valid${NC}"
echo ""

# ============================================================================
# Deploy to Vertex AI Agent Engine
# ============================================================================

echo -e "${YELLOW}Deploying agent to Vertex AI...${NC}"
echo ""
echo -e "${BLUE}Note: This uses the ADK CLI (google-adk deploy)${NC}"
echo -e "${BLUE}Make sure ADK is properly configured${NC}"
echo ""

# Check if ADK is installed
if ! python3 -c "import google.adk" 2>/dev/null; then
    echo -e "${RED}Error: Google ADK not installed${NC}"
    echo "Install with: pip install google-adk"
    exit 1
fi

# Deploy using ADK
echo -e "${YELLOW}Running: google-adk deploy${NC}"

google-adk deploy \
    --project=$PROJECT_ID \
    --location=$REGION \
    --agent-file=agents.py \
    --agent-name=$AGENT_NAME \
    --display-name="$DISPLAY_NAME"

if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}Deployment Successful!${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo ""
    
    # Try to get agent URL
    echo -e "${YELLOW}Agent deployed to Vertex AI Agent Builder${NC}"
    echo ""
    echo "Access your agent at:"
    echo "https://console.cloud.google.com/gen-app-builder/engines?project=$PROJECT_ID"
    echo ""
    
else
    echo ""
    echo -e "${RED}========================================${NC}"
    echo -e "${RED}Deployment Failed${NC}"
    echo -e "${RED}========================================${NC}"
    echo ""
    echo "Check the error messages above for details."
    echo ""
    echo "Common issues:"
    echo "1. ADK not properly configured"
    echo "2. Missing permissions in GCP project"
    echo "3. APIs not enabled"
    echo ""
    exit 1
fi

# ============================================================================
# Post-deployment instructions
# ============================================================================

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Next Steps${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "1. Go to Agent Builder console:"
echo "   https://console.cloud.google.com/gen-app-builder/engines?project=$PROJECT_ID"
echo ""
echo "2. Find your agent: '$DISPLAY_NAME'"
echo ""
echo "3. Test the agent in the UI:"
echo "   • Try: 'I have tomatoes, pasta, garlic. Give me Italian recipes'"
echo "   • Or: 'What can I cook with chicken and rice? Make it Thai'"
echo ""
echo "4. (Optional) To enable image analysis:"
echo "   a. Deploy the Cloud Function:"
echo "      cd cloud_function && ./deploy.sh $PROJECT_ID"
echo ""
echo "   b. Register as Vertex AI Extension using config/openapi.yaml"
echo ""
echo "   c. Add the extension to your Food Analyzer agent in the UI"
echo ""
echo "5. Share the agent URL with users or integrate via API"
echo ""
echo -e "${GREEN}Done! 🎉${NC}"
echo ""
