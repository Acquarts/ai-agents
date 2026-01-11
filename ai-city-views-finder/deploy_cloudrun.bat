@echo off
REM ============================================================================
REM Cloud Run Deployment Script for City Views Finder (Windows)
REM
REM This script automates the deployment of the Streamlit app to Cloud Run
REM with monitoring and logging enabled.
REM
REM Author: Adri
REM Date: 2026-01-11
REM ============================================================================

REM ============================================================================
REM CONFIGURATION - Update these values
REM ============================================================================

set PROJECT_ID=gen-lang-client-0495395701
set REGION=us-central1
set SERVICE_NAME=city-views-finder
set IMAGE_NAME=gcr.io/%PROJECT_ID%/%SERVICE_NAME%

REM Cloud Run configuration
set MEMORY=2Gi
set CPU=2
set MAX_INSTANCES=10
set MIN_INSTANCES=0
set TIMEOUT=300s
set CONCURRENCY=80

REM ============================================================================
REM Main deployment
REM ============================================================================

echo.
echo ========================================================================
echo Cloud Run Deployment for City Views Finder
echo ========================================================================
echo.

REM Check if gcloud is installed
where gcloud >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] gcloud CLI is not installed. Please install it first.
    echo Visit: https://cloud.google.com/sdk/docs/install
    exit /b 1
)

REM Set project
echo [+] Setting project to: %PROJECT_ID%
gcloud config set project %PROJECT_ID%

REM Enable required APIs
echo.
echo ========================================================================
echo Enabling Required APIs
echo ========================================================================
echo.

echo [+] Enabling Cloud Run API...
gcloud services enable run.googleapis.com --quiet

echo [+] Enabling Cloud Build API...
gcloud services enable cloudbuild.googleapis.com --quiet

echo [+] Enabling Container Registry API...
gcloud services enable containerregistry.googleapis.com --quiet

echo [+] Enabling Cloud Logging API...
gcloud services enable logging.googleapis.com --quiet

echo [+] Enabling Cloud Monitoring API...
gcloud services enable monitoring.googleapis.com --quiet

echo [OK] All APIs enabled

REM Build the Docker image
echo.
echo ========================================================================
echo Building Docker Image
echo ========================================================================
echo.

echo [+] Building image: %IMAGE_NAME%
gcloud builds submit --tag %IMAGE_NAME% .

if %errorlevel% neq 0 (
    echo [ERROR] Failed to build Docker image
    exit /b 1
)

echo [OK] Docker image built successfully

REM Read agent resource name
if exist agent_resource_name.txt (
    set /p AGENT_RESOURCE_NAME=<agent_resource_name.txt
    echo [+] Agent resource name found
) else (
    echo [ERROR] agent_resource_name.txt not found. You will need to set AGENT_RESOURCE_NAME manually.
    set AGENT_RESOURCE_NAME=
)

REM Deploy to Cloud Run
echo.
echo ========================================================================
echo Deploying to Cloud Run
echo ========================================================================
echo.

echo [+] Deploying service: %SERVICE_NAME%

gcloud run deploy %SERVICE_NAME% ^
    --image %IMAGE_NAME% ^
    --platform managed ^
    --region %REGION% ^
    --memory %MEMORY% ^
    --cpu %CPU% ^
    --timeout %TIMEOUT% ^
    --concurrency %CONCURRENCY% ^
    --max-instances %MAX_INSTANCES% ^
    --min-instances %MIN_INSTANCES% ^
    --allow-unauthenticated ^
    --set-env-vars "PROJECT_ID=%PROJECT_ID%,LOCATION=%REGION%,AGENT_RESOURCE_NAME=%AGENT_RESOURCE_NAME%" ^
    --quiet

if %errorlevel% neq 0 (
    echo [ERROR] Failed to deploy to Cloud Run
    exit /b 1
)

echo [OK] Service deployed successfully

REM Get service URL
for /f "delims=" %%i in ('gcloud run services describe %SERVICE_NAME% --region %REGION% --format="value(status.url)"') do set SERVICE_URL=%%i

echo.
echo ========================================================================
echo Deployment Complete!
echo ========================================================================
echo.

echo Your app is live at:
echo %SERVICE_URL%
echo.

REM Show monitoring links
echo.
echo ========================================================================
echo Monitoring and Logs
echo ========================================================================
echo.

echo Cloud Run Service:
echo https://console.cloud.google.com/run/detail/%REGION%/%SERVICE_NAME%?project=%PROJECT_ID%
echo.

echo Logs:
echo https://console.cloud.google.com/logs/query?project=%PROJECT_ID%
echo.

echo Metrics:
echo https://console.cloud.google.com/monitoring?project=%PROJECT_ID%
echo.

REM Show next steps
echo.
echo ========================================================================
echo Next Steps
echo ========================================================================
echo.

echo 1. Test your app: %SERVICE_URL%
echo 2. View logs: gcloud run logs read %SERVICE_NAME% --region %REGION% --limit 50
echo 3. Monitor metrics in Cloud Console
echo 4. Set up custom alerts using monitoring_config.yaml
echo.

echo [+] To update the app, run this script again
echo [+] To delete the service: gcloud run services delete %SERVICE_NAME% --region %REGION%

echo.
echo [OK] Deployment script completed!
echo.
