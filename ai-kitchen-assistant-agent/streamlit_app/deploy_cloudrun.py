"""
STREAMLIT UI DEPLOYMENT TO CLOUD RUN
=====================================

Simple Python deployment script for Windows/Linux/Mac

Instructions:
1. Configure your PROJECT_ID below
2. Run from streamlit_app folder: python deploy_cloudrun.py

Author: Adapted for Recipe Multi-Agent
Date: 2025-01-18
"""

import subprocess
import os
import sys

# ============================================================================
# ⚙️ CONFIGURATION - UPDATE THESE VALUES
# ============================================================================

PROJECT_ID = "gen-lang-client-0495395701"        # Your Google Cloud Project ID
REGION = "us-central1"                           # Region (us-central1, europe-west1, etc.)

SERVICE_NAME = "recipe-ai-app"
IMAGE_NAME = "recipe-ai-streamlit"
BUCKET_NAME = f"{PROJECT_ID}-recipe-images"

# ============================================================================
# 🚀 DEPLOYMENT
# ============================================================================

def run_command(cmd, description):
    """Run a command and handle errors"""
    print(f"\n{'='*70}")
    print(f"📌 {description}")
    print(f"{'='*70}")
    
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        if e.stderr:
            print(e.stderr)
        return False


def main():
    print("=" * 70)
    print("🍳 STREAMLIT UI DEPLOYMENT TO CLOUD RUN")
    print("=" * 70)
    
    # Verify we're in streamlit_app folder
    if not os.path.exists("app.py") or not os.path.exists("Dockerfile"):
        print("\n❌ Error: app.py or Dockerfile not found!")
        print("Make sure you're running this from the streamlit_app directory")
        print("\nRun: cd streamlit_app")
        print("Then: python deploy_cloudrun.py")
        return
    
    print(f"\n📍 Project: {PROJECT_ID}")
    print(f"📍 Region: {REGION}")
    print(f"📍 Service: {SERVICE_NAME}")
    print(f"📍 Bucket: {BUCKET_NAME}")
    
    # Step 1: Enable APIs
    print("\n" + "="*70)
    print("🔧 STEP 1: Enabling required APIs")
    print("="*70)
    
    apis = [
        "run.googleapis.com",
        "cloudbuild.googleapis.com",
        "artifactregistry.googleapis.com",
        "storage.googleapis.com",
        "aiplatform.googleapis.com"
    ]
    
    for api in apis:
        cmd = f"gcloud services enable {api} --project={PROJECT_ID}"
        if not run_command(cmd, f"Enabling {api}"):
            print(f"⚠️  Warning: Failed to enable {api}, continuing...")
    
    print("\n✅ APIs enabled")
    
    # Step 2: Create/verify GCS bucket
    print("\n" + "="*70)
    print("🔧 STEP 2: Creating/verifying GCS bucket")
    print("="*70)
    
    check_bucket = f"gsutil ls -b gs://{BUCKET_NAME}"
    result = subprocess.run(check_bucket, shell=True, capture_output=True)
    
    if result.returncode == 0:
        print(f"✅ Bucket gs://{BUCKET_NAME} already exists")
    else:
        print(f"📦 Creating bucket gs://{BUCKET_NAME}")
        cmd = f"gsutil mb -p {PROJECT_ID} -l {REGION} gs://{BUCKET_NAME}"
        if run_command(cmd, "Creating bucket"):
            print("✅ Bucket created")
        else:
            print("⚠️  Warning: Could not create bucket, continuing...")
    
    # Step 3: Build container
    print("\n" + "="*70)
    print("🔧 STEP 3: Building container image")
    print("="*70)
    
    image_url = f"gcr.io/{PROJECT_ID}/{IMAGE_NAME}:latest"
    print(f"📦 Building: {image_url}")
    
    cmd = f"docker build -t {image_url} ."
    if not run_command(cmd, "Building Docker image"):
        print("❌ Build failed")
        return
    
    print("✅ Container built")
    
    # Step 4: Configure Docker auth
    print("\n" + "="*70)
    print("🔧 STEP 4: Configuring Docker authentication")
    print("="*70)
    
    cmd = "gcloud auth configure-docker --quiet"
    run_command(cmd, "Configuring Docker")
    
    # Step 5: Push to registry
    print("\n" + "="*70)
    print("🔧 STEP 5: Pushing image to Container Registry")
    print("="*70)
    
    cmd = f"docker push {image_url}"
    if not run_command(cmd, "Pushing image"):
        print("❌ Push failed")
        return
    
    print("✅ Image pushed")
    
    # Step 6: Deploy to Cloud Run
    print("\n" + "="*70)
    print("🔧 STEP 6: Deploying to Cloud Run")
    print("="*70)
    
    cmd = f"""gcloud run deploy {SERVICE_NAME} \
        --image={image_url} \
        --platform=managed \
        --region={REGION} \
        --allow-unauthenticated \
        --memory=2Gi \
        --cpu=2 \
        --timeout=300 \
        --max-instances=10 \
        --set-env-vars=PROJECT_ID={PROJECT_ID},REGION={REGION},BUCKET_NAME={BUCKET_NAME} \
        --project={PROJECT_ID}"""
    
    if not run_command(cmd, "Deploying to Cloud Run"):
        print("❌ Deployment failed")
        return
    
    # Step 7: Get service URL
    print("\n" + "="*70)
    print("✅ DEPLOYMENT SUCCESSFUL!")
    print("="*70)
    
    cmd = f"""gcloud run services describe {SERVICE_NAME} \
        --platform=managed \
        --region={REGION} \
        --project={PROJECT_ID} \
        --format='value(status.url)'"""
    
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0 and result.stdout:
        service_url = result.stdout.strip()
        
        print(f"\n🌐 Your app is live at:")
        print(f"   {service_url}")
        
        print(f"\n📋 Next steps:")
        print(f"   1. Open the URL above in your browser")
        print(f"   2. Upload a food image")
        print(f"   3. Generate recipes!")
        
        print(f"\n📊 View logs:")
        print(f"   gcloud run services logs read {SERVICE_NAME} --region={REGION} --limit=50")
        
        print(f"\n🔧 View in Console:")
        print(f"   https://console.cloud.google.com/run/detail/{REGION}/{SERVICE_NAME}?project={PROJECT_ID}")
        
        # Save URL
        with open("service_url.txt", "w") as f:
            f.write(service_url)
        print(f"\n💾 Service URL saved to: service_url.txt")
    else:
        print("\n⚠️  Could not retrieve service URL")
        print("Check Cloud Console for the URL")
    
    print("\n" + "="*70)
    print("🎉 DONE!")
    print("="*70)


if __name__ == "__main__":
    main()
