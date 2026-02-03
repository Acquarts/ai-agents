#!/bin/bash

# ============================================================================
# Deploy Recipe AI Streamlit App to Cloud Run
# ============================================================================

set -e  # Exit on error

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# ============================================================================
# Configuration
# ============================================================================

PROJECT_ID=${1:-$(gcloud config get-value project)}
REGION=${2:-us-central1}

SERVICE_NAME="recipe-ai-app"
IMAGE_NAME="recipe-ai-streamlit"
BUCKET_NAME="${PROJECT_ID}-recipe-images"

if [ -z "$PROJECT_ID" ]; then
    echo -e "${RED}Error: No project ID provided${NC}"
    echo "Usage: ./deploy_cloudrun.sh YOUR_PROJECT_ID [REGION]"
    exit 1
fi

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Deploying Recipe AI to Cloud Run${NC}"
echo -e "${GREEN}========================================${NC}"
echo "Project: $PROJECT_ID"
echo "Region: $REGION"
echo "Service: $SERVICE_NAME"
echo ""

# ============================================================================
# Check prerequisites
# ============================================================================

echo -e "${YELLOW}Checking prerequisites...${NC}"

# Check Docker
if ! command -v docker &> /dev/null; then
    echo -e "${RED}Error: Docker not installed${NC}"
    exit 1
fi

# Check gcloud
if ! command -v gcloud &> /dev/null; then
    echo -e "${RED}Error: gcloud CLI not installed${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Prerequisites OK${NC}"
echo ""

# ============================================================================
# Enable APIs
# ============================================================================

echo -e "${YELLOW}Enabling required APIs...${NC}"

gcloud services enable \
    run.googleapis.com \
    cloudbuild.googleapis.com \
    artifactregistry.googleapis.com \
    storage.googleapis.com \
    aiplatform.googleapis.com \
    --project=$PROJECT_ID \
    --quiet

echo -e "${GREEN}✓ APIs enabled${NC}"
echo ""

# ============================================================================
# Create GCS bucket for images
# ============================================================================

echo -e "${YELLOW}Creating/verifying GCS bucket...${NC}"

if gsutil ls -b gs://$BUCKET_NAME 2>/dev/null; then
    echo "Bucket $BUCKET_NAME already exists"
else
    echo "Creating bucket $BUCKET_NAME"
    gsutil mb -p $PROJECT_ID -l $REGION gs://$BUCKET_NAME
    
    # Set CORS for bucket
    cat > /tmp/cors.json << 'EOF'
[
  {
    "origin": ["*"],
    "method": ["GET", "PUT", "POST"],
    "responseHeader": ["Content-Type"],
    "maxAgeSeconds": 3600
  }
]
EOF
    gsutil cors set /tmp/cors.json gs://$BUCKET_NAME
    rm /tmp/cors.json
fi

echo -e "${GREEN}✓ Bucket ready${NC}"
echo ""

# ============================================================================
# Build container
# ============================================================================

echo -e "${YELLOW}Building container image...${NC}"

# Set image URL
IMAGE_URL="gcr.io/${PROJECT_ID}/${IMAGE_NAME}:latest"

echo "Building image: $IMAGE_URL"

docker build -t $IMAGE_URL .

if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Docker build failed${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Container built${NC}"
echo ""

# ============================================================================
# Push to Container Registry
# ============================================================================

echo -e "${YELLOW}Pushing image to Container Registry...${NC}"

# Configure Docker auth
gcloud auth configure-docker --quiet

# Push image
docker push $IMAGE_URL

if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Docker push failed${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Image pushed${NC}"
echo ""

# ============================================================================
# Deploy to Cloud Run
# ============================================================================

echo -e "${YELLOW}Deploying to Cloud Run...${NC}"

gcloud run deploy $SERVICE_NAME \
    --image=$IMAGE_URL \
    --platform=managed \
    --region=$REGION \
    --allow-unauthenticated \
    --memory=2Gi \
    --cpu=2 \
    --timeout=300 \
    --max-instances=10 \
    --set-env-vars="PROJECT_ID=${PROJECT_ID},REGION=${REGION},BUCKET_NAME=${BUCKET_NAME}" \
    --project=$PROJECT_ID

if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Cloud Run deployment failed${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Deployment Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# ============================================================================
# Get service URL
# ============================================================================

SERVICE_URL=$(gcloud run services describe $SERVICE_NAME \
    --platform=managed \
    --region=$REGION \
    --project=$PROJECT_ID \
    --format='value(status.url)')

echo -e "${GREEN}Service URL:${NC}"
echo "$SERVICE_URL"
echo ""

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Next Steps:${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo "1. Open your app:"
echo "   $SERVICE_URL"
echo ""
echo "2. Test by uploading a food image"
echo ""
echo "3. (Optional) Set up custom domain:"
echo "   https://console.cloud.google.com/run/domains"
echo ""
echo "4. Monitor logs:"
echo "   gcloud run services logs read $SERVICE_NAME --region=$REGION --project=$PROJECT_ID --limit=50"
echo ""
echo "5. View metrics:"
echo "   https://console.cloud.google.com/run/detail/$REGION/$SERVICE_NAME/metrics?project=$PROJECT_ID"
echo ""
echo -e "${GREEN}Done! 🎉${NC}"
