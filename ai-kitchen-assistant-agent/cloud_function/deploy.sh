#!/bin/bash

# ============================================================================
# Deploy Food Image Analyzer Cloud Function
# ============================================================================

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# ============================================================================
# Configuration
# ============================================================================

# Get project ID from gcloud config or use provided argument
if [ -z "$1" ]; then
    PROJECT_ID=$(gcloud config get-value project)
    if [ -z "$PROJECT_ID" ]; then
        echo -e "${RED}Error: No project ID provided and no default project set${NC}"
        echo "Usage: ./deploy.sh YOUR_PROJECT_ID [REGION]"
        exit 1
    fi
else
    PROJECT_ID=$1
fi

# Region (default: us-central1)
REGION=${2:-us-central1}

# Function name
FUNCTION_NAME="analyze-food-image"
ENTRY_POINT="analyze_food_image"
RUNTIME="python311"
MEMORY="512MB"
TIMEOUT="60s"

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Deploying Food Image Analyzer${NC}"
echo -e "${GREEN}========================================${NC}"
echo "Project ID: $PROJECT_ID"
echo "Region: $REGION"
echo "Function: $FUNCTION_NAME"
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

# Check if logged in
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
    echo -e "${RED}Error: Not logged in to gcloud${NC}"
    echo "Run: gcloud auth login"
    exit 1
fi

echo -e "${GREEN}✓ Prerequisites OK${NC}"
echo ""

# ============================================================================
# Enable required APIs
# ============================================================================

echo -e "${YELLOW}Enabling required APIs...${NC}"

gcloud services enable \
    cloudfunctions.googleapis.com \
    cloudbuild.googleapis.com \
    aiplatform.googleapis.com \
    --project=$PROJECT_ID

echo -e "${GREEN}✓ APIs enabled${NC}"
echo ""

# ============================================================================
# Deploy function
# ============================================================================

echo -e "${YELLOW}Deploying Cloud Function...${NC}"

gcloud functions deploy $FUNCTION_NAME \
    --gen2 \
    --runtime=$RUNTIME \
    --region=$REGION \
    --source=. \
    --entry-point=$ENTRY_POINT \
    --trigger-http \
    --allow-unauthenticated \
    --memory=$MEMORY \
    --timeout=$TIMEOUT \
    --set-env-vars PROJECT_ID=$PROJECT_ID,LOCATION=$REGION,MODEL_NAME=gemini-3-flash-preview \
    --project=$PROJECT_ID

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Deployment Complete!${NC}"
echo -e "${GREEN}========================================${NC}"

# ============================================================================
# Get function URL
# ============================================================================

echo ""
echo -e "${YELLOW}Getting function URL...${NC}"

FUNCTION_URL=$(gcloud functions describe $FUNCTION_NAME \
    --region=$REGION \
    --project=$PROJECT_ID \
    --gen2 \
    --format="value(serviceConfig.uri)")

echo ""
echo -e "${GREEN}Function URL:${NC}"
echo "$FUNCTION_URL"

# ============================================================================
# Test the function
# ============================================================================

echo ""
echo -e "${YELLOW}Testing function...${NC}"
echo ""

# Create test payload
TEST_PAYLOAD='{"image_uri":"gs://cloud-samples-data/generative-ai/image/scones.jpg"}'

curl -X POST \
    -H "Content-Type: application/json" \
    -d "$TEST_PAYLOAD" \
    "$FUNCTION_URL" \
    2>/dev/null | python3 -m json.tool || echo "Test request sent (formatting failed)"

echo ""
echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Next Steps:${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "1. Save your function URL:"
echo "   $FUNCTION_URL"
echo ""
echo "2. Create OpenAPI spec (see ../config/openapi.yaml)"
echo "   Update the server URL with your function URL"
echo ""
echo "3. Register as Vertex AI Extension:"
echo "   cd ../config"
echo "   gcloud ai extensions create food-image-analyzer \\"
echo "     --region=$REGION \\"
echo "     --openapi-spec-uri=gs://YOUR_BUCKET/openapi.yaml \\"
echo "     --display-name='Food Image Analyzer'"
echo ""
echo "4. Add extension to your ADK agent in Agent Builder UI"
echo ""
echo -e "${GREEN}Done!${NC}"
