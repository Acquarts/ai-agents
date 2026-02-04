# 🍳 Recipe Multi-Agent System

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Google Cloud](https://img.shields.io/badge/Google%20Cloud-Vertex%20AI-4285F4?logo=google-cloud)](https://cloud.google.com/vertex-ai)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-FF4B4B?logo=streamlit)](https://streamlit.io)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker)](https://www.docker.com/)
[![Gemini](https://img.shields.io/badge/Gemini%203%20Flash-8E75B2)](https://deepmind.google/technologies/gemini/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**Frameworks & Libraries:**
- 🤖 **Google ADK** - Agent Development Kit
- 🧠 **Vertex AI** - Agent Engine & Gemini Models
- 🎨 **Streamlit** - Web UI Framework
- ☁️ **Cloud Run** - Serverless Deployment
- 📦 **Cloud Storage** - Image Storage
- 🐳 **Docker** - Containerization

---

Complete AI-powered multi-agent system with web UI where users upload ingredient photos and instantly get personalized recipe recommendations.

---

DEMO LIVE: https://recipe-ai-app-562289298058.us-central1.run.app/

## 📋 Table of Contents

- [What is this](#-what-is-this)
- [Features](#-features)
- [Architecture](#️-architecture)
- [Project Structure](#-project-structure)
- [Prerequisites](#-prerequisites)
- [Quick Start](#-quick-start-5-minutes)
- [Configuration](#️-configuration)
- [Deployment](#-deployment)
- [Usage](#-usage)
- [Testing](#-testing)
- [Costs](#-costs)
- [Troubleshooting](#-troubleshooting)
- [Customization](#-customization)
- [Quick Commands](#-quick-reference-commands)

---

## 🎯 What is this

An AI system that:
1. **User uploads photo** of ingredients
2. **Gemini Vision analyzes** and identifies ingredients
3. **Vertex AI Agent generates** 3-5 authentic recipes
4. **Modern UI displays** recipes with detailed steps

**Complete with professional web interface on Streamlit + Cloud Run.**

---

## ✨ Features

### For End Users:
- 📸 **Direct photo upload** (no URIs, no complications)
- 🌍 **15+ international cuisines** (Italian, Mexican, Thai, etc.)
- ⚡ **Instant results** with AI
- 📱 **Responsive** - works on mobile and desktop
- 📥 **Download recipes** as text file
- 🎨 **Modern, clean UI**

### Technical:
- 🤖 **Multi-agent ADK** (3 coordinated agents)
- 👁️ **Gemini Vision** for image analysis
- ☁️ **Cloud Run** with auto-scaling
- 🔄 **CI/CD ready** with automated scripts
- 🔒 **Secure** with IAM and service accounts

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────┐
│         User (Web Browser)                  │
└────────────────┬────────────────────────────┘
                 │
                 ▼
    ┌────────────────────────┐
    │   Streamlit UI         │
    │   (Cloud Run)          │
    │   - Upload image       │
    │   - Select cuisine     │
    │   - Display recipes    │
    └────────┬───────────────┘
             │
             ├──────────────┐
             │              │
             ▼              ▼
┌────────────────┐  ┌──────────────┐
│ Cloud Storage  │  │ Gemini Vision│
│ (Images)       │  │ (Analysis)   │
└────────────────┘  └──────┬───────┘
                           │
                           ▼
              ┌────────────────────────┐
              │   Vertex AI Agent      │
              │   (Recipe Generator)   │
              │   - Food Analyzer      │
              │   - Recipe Generator   │
              └────────────────────────┘
```

### Components:

**Frontend (Streamlit):**
- User interface
- Image upload
- Results display
- Deployed on Cloud Run

**Backend (Vertex AI):**
- Root Agent: Recipe Coordinator
- Sub-Agent 1: Food Analyzer
- Sub-Agent 2: Recipe Generator
- Deployed on Vertex AI Agent Engine

**Storage:**
- Cloud Storage for temporary images

**AI Models:**
- Gemini 2.0 Flash for vision analysis
- Gemini 3 Flash for Agent Engine (recipe generation)

---

## 📁 Project Structure

```
recipe-multi-agent/
│
├── README.md                    # ⭐ EVERYTHING HERE (only .md file)
│
├── agents.py                    # ADK agents definition
├── requirements.txt             # Backend dependencies
├── .env.example                # Backend config (copy to .env)
├── .gitignore                  
│
├── deploy_agent.py             # 🚀 Deploy agent (Python - works on Windows)
├── deploy_agent.sh             # 🚀 Deploy agent (Bash - Linux/Mac)
├── test_agent.py               # 🧪 Test agent locally
│
├── streamlit_app/              # ⭐ COMPLETE WEB UI
│   ├── app.py                  # Streamlit application
│   ├── config.py               # Configuration
│   ├── requirements.txt        # UI dependencies
│   ├── .env.example           # UI config (copy to .env)
│   ├── Dockerfile             # Container
│   ├── .dockerignore          # Docker optimization
│   ├── deploy_cloudrun.py     # 🚀 Deploy UI (Python - works on Windows)
│   ├── deploy_cloudrun.sh     # 🚀 Deploy UI (Bash - Linux/Mac)
│   └── run_local.sh           # 🧪 Test locally
│
├── cloud_function/            # (Optional - advanced analysis)
│   ├── main.py               # Cloud Function
│   ├── requirements.txt      
│   └── deploy.sh             
│
└── config/
    └── openapi.yaml          # API spec for extensions
```

**Key files:**
- `agents.py` → The 3 agents (root + 2 sub-agents)
- `streamlit_app/app.py` → Complete UI
- `deploy_agent.py` → Deploy backend (Python - **works on Windows**)
- `streamlit_app/deploy_cloudrun.py` → Deploy frontend (Python - **works on Windows**)

**Total: 26 files**

---

## 📦 Prerequisites

### Required:
- ✅ **Google Cloud Project** with billing enabled
- ✅ **Python 3.9+**
- ✅ **gcloud CLI** installed and configured
- ✅ **Docker** installed

### Verify:
```bash
# Python
python3 --version  # Should be 3.9+

# gcloud
gcloud --version
gcloud auth list

# Docker
docker --version

# Project configured
gcloud config get-value project
```

### Install missing components:
```bash
# gcloud CLI
# https://cloud.google.com/sdk/docs/install

# Login and setup
gcloud auth login
gcloud auth application-default login
gcloud config set project YOUR_PROJECT_ID

# Docker
# https://docs.docker.com/get-docker/
```

---

## ⚡ Quick Start (5 minutes)

### 1. Configure
```bash
# Backend
cp .env.example .env
nano .env  # Change: PROJECT_ID=your-real-project

# Frontend
cp streamlit_app/.env.example streamlit_app/.env
nano streamlit_app/.env  # Change: PROJECT_ID=your-real-project
```

### 2. Install Dependencies
```bash
# Backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Frontend
cd streamlit_app
pip install -r requirements.txt
cd ..
```

### 3. Deploy Backend
```bash
# Option A: Python script (works on Windows/Linux/Mac)
python deploy_agent.py
# Wait 2-3 minutes... ✅

# Option B: Bash script (Linux/Mac only)
chmod +x deploy_agent.sh
./deploy_agent.sh YOUR_PROJECT_ID us-central1
```

### 4. Deploy Frontend
```bash
cd streamlit_app

# Option A: Python script (works on Windows/Linux/Mac)
python deploy_cloudrun.py
# Wait 5-10 minutes... ✅

# Option B: Bash script (Linux/Mac only)
chmod +x deploy_cloudrun.sh
./deploy_cloudrun.sh YOUR_PROJECT_ID us-central1
```

### 5. Use! 🎉
```
Open: https://recipe-ai-app-xxxxx.run.app
Upload ingredient photo
Select cuisine
Get recipes!
```

---

## ⚙️ Configuration

### Two `.env` files?

**Yes, they're different:**
- **Root** (`/.env`) → For backend (Vertex AI Agent)
- **Streamlit** (`/streamlit_app/.env`) → For frontend (Cloud Run)

### Backend `.env` (root)

```bash
# ============== MINIMUM REQUIRED ==============
PROJECT_ID=your-project-id
REGION=us-central1
MODEL_NAME=gemini-3-flash-preview

# ============== OPTIONAL (filled after deploy) ==============
AGENT_ENGINE_ID=         # Auto-filled
IMAGE_BUCKET=            # For configs
CONFIG_BUCKET=           # For specs
```

### Frontend `.env` (streamlit_app/)

```bash
# ============== MINIMUM REQUIRED ==============
PROJECT_ID=your-project-id                    # Same as above
REGION=us-central1                            # Same as above
BUCKET_NAME=your-project-id-recipe-images     # Bucket for photos
MODEL_NAME=gemini-3-flash-preview               # Same as above

# ============== OPTIONAL ==============
AGENT_ID=               # If using deployed agent
DEBUG_MODE=false        # Debug logs
```

### Values that MUST match:
```bash
PROJECT_ID    → Same in both
REGION        → Same in both
MODEL_NAME    → Same in both
```

### Local Authentication (for testing):
```bash
# Option 1: Service account
gcloud iam service-accounts keys create key.json \
  --iam-account=SA_NAME@PROJECT.iam.gserviceaccount.com

export GOOGLE_APPLICATION_CREDENTIALS=/path/to/key.json

# Option 2: User credentials (easier)
gcloud auth application-default login
```

---

## 🚀 Deployment

### Complete Deployment

```bash
# 1. Backend (Vertex AI Agent)
./deploy_agent.sh YOUR_PROJECT_ID us-central1
# ⏱️ 2-3 minutes

# 2. Frontend (Streamlit + Cloud Run)
cd streamlit_app
./deploy_cloudrun.sh YOUR_PROJECT_ID us-central1
# ⏱️ 5-10 minutes

# 3. Done!
# URL: https://recipe-ai-app-xxxxx.run.app
```

### Backend Only
```bash
./deploy_agent.sh YOUR_PROJECT_ID us-central1
```

### Frontend Only
```bash
cd streamlit_app
./deploy_cloudrun.sh YOUR_PROJECT_ID us-central1
```

### Verify Deployment

```bash
# Backend
gcloud ai agents list --region=us-central1

# Frontend
gcloud run services list --region=us-central1

# Get URL
gcloud run services describe recipe-ai-app \
  --region=us-central1 \
  --format='value(status.url)'
```

### Update

```bash
# Make changes to code...

# Update backend
./deploy_agent.sh YOUR_PROJECT_ID

# Update frontend
cd streamlit_app
./deploy_cloudrun.sh YOUR_PROJECT_ID
# Cloud Run does rolling update automatically
```

### View Logs

```bash
# Cloud Run logs
gcloud run services logs read recipe-ai-app \
  --region=us-central1 \
  --limit=50

# Real-time logs
gcloud run services logs tail recipe-ai-app \
  --region=us-central1

# Filter errors
gcloud run services logs read recipe-ai-app \
  --region=us-central1 \
  --log-filter='severity>=ERROR'
```

---

## 💻 Usage

### Web UI (End Users)

**1. Open app:**
```
https://recipe-ai-app-xxxxx.run.app
```

**2. Upload photo:**
- Click "Upload Your Ingredients"
- Select JPG, PNG or WebP
- Max 10MB

**3. Select cuisine:**
- Sidebar → "Choose cuisine style"
- 15+ options available

**4. Analyze:**
- Click "🔍 Analyze Ingredients"
- Wait 5-10 seconds
- See ingredient list

**5. Generate recipes:**
- Click "👨‍🍳 Generate Recipes"
- Wait 10-15 seconds
- Get 3-5 complete recipes

**6. Download:**
- Click "📥 Download Recipes"
- Download .txt file

### API (Programmatic)

```python
import vertexai
from vertexai.generative_models import GenerativeModel, Part

# Initialize
vertexai.init(project="YOUR_PROJECT", location="us-central1")
model = GenerativeModel("gemini-2.0-flash")  # Use 2.0-flash for direct API calls

# Analyze image
image = Part.from_uri("gs://bucket/food.jpg", mime_type="image/jpeg")
response = model.generate_content([
    "List all ingredients in this food image",
    image
])
ingredients = response.text

# Generate recipes
recipes = model.generate_content(f"""
Generate 3 Italian recipes using: {ingredients}
Include full ingredients list and step-by-step instructions.
""")
print(recipes.text)
```

---

## 🧪 Testing

### Test Backend Locally

```bash
python test_agent.py

# Validates:
# ✓ Agent structure
# ✓ .env configuration
# ✓ Instructions
# ✓ Available tools
# ✓ Interactive mode
```

### Test Frontend Locally

```bash
cd streamlit_app
./run_local.sh

# Or manually:
streamlit run app.py --server.port=8501

# Open: http://localhost:8501
```

### Test Docker Locally

```bash
cd streamlit_app

# Build
docker build -t recipe-test .

# Run
docker run -p 8080:8080 \
  -e PROJECT_ID=your-project \
  -e BUCKET_NAME=your-bucket \
  recipe-test

# Test: http://localhost:8080
```

### Complete End-to-End Test

1. Backend working: `python test_agent.py`
2. Frontend working: `cd streamlit_app && ./run_local.sh`
3. Upload test image
4. Verify correct analysis
5. Generate recipes
6. Download result

---

## 💰 Costs

### Monthly Estimate (1000 active users)

| Service | Usage | Cost |
|---------|-------|------|
| **Cloud Run** | 50K requests | $10-15 |
| **Cloud Storage** | 10GB + transfer | $2-5 |
| **Gemini Vision** | 5K analyses | $10-15 |
| **Gemini Text** | 50K requests | $5-10 |
| **Agent Engine** | Hosting | $5-10 |
| **TOTAL** | | **$32-55/month** |

### Per User:
- **~$0.03-0.05** per active user/month
- **~$0.001-0.002** per recipe generated

### Reduce Costs:

**1. Cloud Run - Min instances to 0:**
```bash
gcloud run services update recipe-ai-app \
  --min-instances=0 \
  --max-instances=10 \
  --region=us-central1
```

**2. Storage - Lifecycle policy:**
```bash
# lifecycle.json
{
  "lifecycle": {
    "rule": [{
      "action": {"type": "Delete"},
      "condition": {"age": 7}
    }]
  }
}

gsutil lifecycle set lifecycle.json gs://BUCKET_NAME
```

**3. Rate limiting:**
```python
# In app.py
MAX_REQUESTS_PER_USER = 20
```

**4. Caching:**
```python
@st.cache_data(ttl=3600)
def generate_recipes(ingredients, cuisine):
    ...
```

---

## 🔧 Troubleshooting

### "Permission Denied" on image upload

**Solution:**
```bash
gcloud projects add-iam-policy-binding PROJECT_ID \
  --member=serviceAccount:SA@PROJECT.iam.gserviceaccount.com \
  --role=roles/storage.admin
```

### "Agent not found"

**Solution:**
```bash
# Verify
gcloud ai agents list --region=us-central1

# If doesn't exist, deploy
./deploy_agent.sh PROJECT_ID
```

### "Cloud Run timeout"

**Solution:**
```bash
gcloud run services update recipe-ai-app \
  --timeout=300 \
  --region=us-central1
```

### "Out of memory"

**Solution:**
```bash
gcloud run services update recipe-ai-app \
  --memory=4Gi \
  --cpu=4 \
  --region=us-central1
```

### "Image too large"

**Solution:**
```python
# In app.py, add compression
from PIL import Image

def compress_image(img_file):
    img = Image.open(img_file)
    img.thumbnail((1920, 1920))
    # Save compressed version
```

### View detailed logs:

```bash
# Last 100 logs
gcloud run services logs read recipe-ai-app --limit=100

# Errors only
gcloud run services logs read recipe-ai-app \
  --log-filter='severity>=ERROR'

# Real-time logs
gcloud run services logs tail recipe-ai-app
```

---

## 🎨 Customization

### Change available cuisines

**Edit:** `streamlit_app/config.py`
```python
CUISINES = [
    "Italian",
    "Mexican",
    "Thai",
    # Add:
    "Peruvian",
    "Ethiopian",
    "Cuban",
]
```

### Change UI colors

**Edit:** `streamlit_app/app.py`
```python
st.markdown("""
<style>
    .main-header {
        color: #FF6B6B;  # ← Change here
    }
    .stButton>button {
        background-color: #FF6B6B;  # ← And here
    }
</style>
""", unsafe_allow_html=True)
```

### Change AI model

**Edit:** `.env` files and `agents.py`
```bash
# Options:
MODEL_NAME=gemini-3-flash-preview    # Latest, best performance (recommended)
MODEL_NAME=gemini-2.0-flash          # Stable, good balance
MODEL_NAME=gemini-1.5-pro            # More capable, expensive
```
**Note:** After changing the model in `agents.py`, run `python deploy_agent.py` to update the Agent Engine.

### Add dietary filters

**Edit:** `streamlit_app/app.py`
```python
# Add in sidebar
dietary = st.multiselect(
    "Dietary restrictions:",
    ["Vegetarian", "Vegan", "Gluten-free", "Dairy-free"]
)

# Pass to prompt
prompt = f"""
Generate {cuisine} recipes with:
- Ingredients: {ingredients}
- Dietary restrictions: {', '.join(dietary)}
"""
```

### Custom domain

```bash
gcloud run domain-mappings create \
  --service=recipe-ai-app \
  --domain=recipes.yourdomain.com \
  --region=us-central1

# Follow instructions to update DNS
```

---

## 📚 Quick Reference Commands

```bash
# =================== SETUP ===================
cp .env.example .env
cp streamlit_app/.env.example streamlit_app/.env
pip install -r requirements.txt

# ================ LOCAL TESTING ===============
python test_agent.py                    # Backend
cd streamlit_app && ./run_local.sh     # Frontend

# ================ DEPLOYMENT ==================
./deploy_agent.sh PROJECT_ID           # Backend
cd streamlit_app
./deploy_cloudrun.sh PROJECT_ID        # Frontend

# ================ MONITORING ==================
# Logs
gcloud run services logs read recipe-ai-app --limit=50

# Metrics
gcloud run services describe recipe-ai-app --region=us-central1

# List
gcloud run services list
gcloud ai agents list --region=us-central1

# ================== UPDATES ===================
# Make changes, then:
./deploy_agent.sh PROJECT_ID
cd streamlit_app && ./deploy_cloudrun.sh PROJECT_ID

# ================== ROLLBACK ==================
gcloud run revisions list --service=recipe-ai-app
gcloud run services update-traffic recipe-ai-app \
  --to-revisions=REVISION_NAME=100

# ================== CLEANUP ===================
# Delete service
gcloud run services delete recipe-ai-app --region=us-central1

# Delete agent
gcloud ai agents delete AGENT_ID --region=us-central1

# Delete bucket
gsutil rm -r gs://PROJECT_ID-recipe-images
```

---

## 🤝 Support

### Report Bugs:
1. View logs: `gcloud run services logs read recipe-ai-app`
2. Verify `.env` configured correctly
3. Test locally: `./run_local.sh`
4. Create issue with logs and reproduction steps

### Future Improvements:
- [ ] Dietary filters (vegan, gluten-free)
- [ ] Save favorite recipes
- [ ] Social media sharing
- [ ] Multi-language support
- [ ] Auto shopping list
- [ ] Nutritional information
- [ ] Video tutorials

---

## 📄 License

MIT License

---

## 🙏 Credits

- **Google Cloud Platform** - Infrastructure
- **Vertex AI** - Agents and models
- **Gemini** - Vision and generation
- **Streamlit** - UI framework

---

## 🎉 TL;DR - Super Quick Start

```bash
# 1. Config
cp .env.example .env && nano .env
cp streamlit_app/.env.example streamlit_app/.env && nano streamlit_app/.env

# 2. Deploy (Python scripts work on Windows!)
python deploy_agent.py
cd streamlit_app && python deploy_cloudrun.py

# 3. Use
open https://recipe-ai-app-xxxxx.run.app
```

---

**Questions? Read this README or create an issue.**

**Happy Cooking! 🍳👨‍🍳**
