#!/bin/bash

################################################################################
# Cloud Run Deployment Script for City Views Finder
#
# This script automates the deployment of the Streamlit app to Cloud Run
# with monitoring and logging enabled.
#
# Author: Adri
# Date: 2026-01-11
################################################################################

set -e  # Exit on error

# ============================================================================
# CONFIGURATION - Update these values
# ============================================================================

PROJECT_ID="gen-lang-client-0495395701"
REGION="us-central1"
SERVICE_NAME="city-views-finder"
IMAGE_NAME="gcr.io/${PROJECT_ID}/${SERVICE_NAME}"

# Cloud Run configuration
MEMORY="2Gi"
CPU="2"
MAX_INSTANCES="10"
MIN_INSTANCES="0"
TIMEOUT="300s"
CONCURRENCY="80"

# ============================================================================
# Colors for output
# ============================================================================

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ============================================================================
# Helper functions
# ============================================================================

print_header() {
    echo ""
    echo -e "${BLUE}========================================================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================================================${NC}"
    echo ""
}

print_step() {
    echo -e "${GREEN}➜${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

# ============================================================================
# Main deployment
# ============================================================================

print_header "🚀 Cloud Run Deployment for City Views Finder"

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    print_error "gcloud CLI is not installed. Please install it first."
    echo "Visit: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Set project
print_step "Setting project to: $PROJECT_ID"
gcloud config set project "$PROJECT_ID"

# Enable required APIs
print_header "📡 Enabling Required APIs"

print_step "Enabling Cloud Run API..."
gcloud services enable run.googleapis.com --quiet

print_step "Enabling Cloud Build API..."
gcloud services enable cloudbuild.googleapis.com --quiet

print_step "Enabling Container Registry API..."
gcloud services enable containerregistry.googleapis.com --quiet

print_step "Enabling Cloud Logging API..."
gcloud services enable logging.googleapis.com --quiet

print_step "Enabling Cloud Monitoring API..."
gcloud services enable monitoring.googleapis.com --quiet

print_success "All APIs enabled"

# Build the Docker image
print_header "🔨 Building Docker Image"

print_step "Building image: $IMAGE_NAME"
gcloud builds submit --tag "$IMAGE_NAME" .

print_success "Docker image built successfully"

# Deploy to Cloud Run
print_header "🚀 Deploying to Cloud Run"

print_step "Deploying service: $SERVICE_NAME"

# Read agent resource name
if [ -f "agent_resource_name.txt" ]; then
    AGENT_RESOURCE_NAME=$(cat agent_resource_name.txt)
    print_step "Agent resource name found: ${AGENT_RESOURCE_NAME:0:50}..."
else
    print_warning "agent_resource_name.txt not found. You'll need to set AGENT_RESOURCE_NAME manually."
    AGENT_RESOURCE_NAME=""
fi

gcloud run deploy "$SERVICE_NAME" \
    --image "$IMAGE_NAME" \
    --platform managed \
    --region "$REGION" \
    --memory "$MEMORY" \
    --cpu "$CPU" \
    --timeout "$TIMEOUT" \
    --concurrency "$CONCURRENCY" \
    --max-instances "$MAX_INSTANCES" \
    --min-instances "$MIN_INSTANCES" \
    --allow-unauthenticated \
    --set-env-vars "PROJECT_ID=$PROJECT_ID,LOCATION=$REGION,AGENT_RESOURCE_NAME=$AGENT_RESOURCE_NAME" \
    --quiet

print_success "Service deployed successfully"

# Get service URL
SERVICE_URL=$(gcloud run services describe "$SERVICE_NAME" --region "$REGION" --format="value(status.url)")

print_header "✅ Deployment Complete!"

echo ""
echo -e "${GREEN}Your app is live at:${NC}"
echo -e "${BLUE}$SERVICE_URL${NC}"
echo ""

# Show monitoring links
print_header "📊 Monitoring & Logs"

echo -e "${GREEN}Cloud Run Service:${NC}"
echo "https://console.cloud.google.com/run/detail/${REGION}/${SERVICE_NAME}?project=${PROJECT_ID}"
echo ""

echo -e "${GREEN}Logs:${NC}"
echo "https://console.cloud.google.com/logs/query?project=${PROJECT_ID}"
echo ""

echo -e "${GREEN}Metrics:${NC}"
echo "https://console.cloud.google.com/monitoring?project=${PROJECT_ID}"
echo ""

# Show next steps
print_header "🎯 Next Steps"

echo "1. Test your app: $SERVICE_URL"
echo "2. View logs: gcloud run logs read $SERVICE_NAME --region $REGION --limit 50"
echo "3. Monitor metrics in Cloud Console"
echo "4. Set up custom alerts using monitoring_config.yaml"
echo ""

print_step "To update the app, run this script again"
print_step "To delete the service: gcloud run services delete $SERVICE_NAME --region $REGION"

echo ""
print_success "Deployment script completed!"
echo ""
