# CLAUDE.MD - AI Chef Agent Project Guide

## Project Overview

This is a **Recipe Multi-Agent System** built with Google's Agent Development Kit (ADK). It's an AI-powered application that analyzes food ingredients (from text or images) and generates authentic regional recipes.

**Core Functionality:**
1. User uploads ingredient photo or lists ingredients
2. Gemini Vision analyzes and identifies ingredients
3. Multi-agent system generates 3-5 authentic recipes based on selected cuisine
4. Modern Streamlit UI displays results with detailed cooking instructions

## Technology Stack

- **Backend:** Google Vertex AI Agent Engine, ADK (Agent Development Kit)
- **Frontend:** Streamlit on Cloud Run
- **AI Models:** Gemini 2.0 Flash (vision & text generation)
- **Infrastructure:** Google Cloud Platform (Cloud Run, Cloud Storage, Vertex AI)
- **Language:** Python 3.9+
- **Deployment:** Docker containers, automated deployment scripts

## Architecture

### Multi-Agent System (ADK)

The system uses a hierarchical agent structure:

```
root_agent (recipe_coordinator)
├── food_analyzer (validates & structures ingredients)
│   ├── food_analyzer_google_search_agent
│   └── food_analyzer_url_context_agent
└── recipe_generator (creates authentic regional recipes)
    ├── recipe_generator_google_search_agent
    └── recipe_generator_url_context_agent
```

**Agent Flow:**
1. **recipe_coordinator** (root) - Orchestrates the entire conversation
2. **food_analyzer** - Validates ingredient lists, structures data
3. **recipe_generator** - Creates authentic recipes for specified cuisines

### File Structure

```
ai-chef-agent/
├── agents.py                    # ADK agent definitions (CORE LOGIC)
├── requirements.txt             # Backend dependencies
├── .env                        # Backend configuration
├── deploy_agent.py             # Agent deployment script
├── deploy_agent.sh             # Bash deployment script
├── test_agent.py               # Agent testing utility
├── README.md                   # User-facing documentation
├── CLAUDE.MD                   # This file - AI assistant guide
│
├── streamlit_app/              # Frontend UI
│   ├── app.py                  # Main Streamlit application
│   ├── config.py               # UI configuration
│   ├── requirements.txt        # UI dependencies
│   ├── .env                   # UI configuration
│   ├── Dockerfile             # Container definition
│   ├── deploy_cloudrun.py     # UI deployment script
│   ├── deploy_cloudrun.sh     # Bash UI deployment
│   └── run_local.sh           # Local testing script
│
├── cloud_function/            # Optional extensions
└── config/
    └── openapi.yaml          # API specifications
```

## Key Files

### `agents.py` (Most Important)

This file defines the entire multi-agent system:

- **food_analyzer**: Takes ingredient lists (text or image URIs) and validates/structures them
- **recipe_generator**: Creates 3-5 authentic regional recipes with detailed instructions
- **recipe_coordinator** (root): Orchestrates conversation flow and delegates to sub-agents

**Important Notes:**
- The system does NOT have native image analysis in agents (uses Gemini Vision separately)
- Agents use GoogleSearchTool and url_context for web research
- All agents use Gemini 2.0 Flash model

### `streamlit_app/app.py`

The user-facing web interface:
- Image upload functionality
- Cuisine selection (15+ cuisines)
- Ingredient analysis display
- Recipe generation and display
- Recipe download feature

### Configuration Files

**Two separate `.env` files:**
1. **Root `.env`** - Backend (Vertex AI Agent) configuration
2. **`streamlit_app/.env`** - Frontend (Cloud Run) configuration

Both need: `PROJECT_ID`, `REGION`, `MODEL_NAME`, `BUCKET_NAME`

## Common Development Tasks

### Making Changes to Agent Logic

**File to edit:** `agents.py`

When modifying agent behavior:
1. Edit the agent's `instruction` field in `agents.py`
2. Test locally: `python test_agent.py`
3. Deploy: `python deploy_agent.py` (works on Windows)
4. Verify: Check agent in Vertex AI console

**Example modification locations:**
- Change ingredient analysis format → Edit `food_analyzer.instruction`
- Modify recipe output → Edit `recipe_generator.instruction`
- Adjust conversation flow → Edit `root_agent.instruction`

### Making Changes to UI

**File to edit:** `streamlit_app/app.py`

For UI changes:
1. Edit `app.py` for functionality or layout
2. Edit `config.py` for cuisine list or constants
3. Test locally: `cd streamlit_app && streamlit run app.py`
4. Deploy: `cd streamlit_app && python deploy_cloudrun.py`

### Adding New Cuisines

**File:** `streamlit_app/config.py`

Add to the `CUISINES` list:
```python
CUISINES = [
    "Italian",
    "Mexican",
    # Add new cuisine here
    "Korean",
]
```

No deployment to Vertex AI needed - just redeploy Cloud Run UI.

### Debugging Issues

**Common issues:**

1. **"Agent not found"**
   - Run: `gcloud ai agents list --region=us-central1`
   - If empty, deploy: `python deploy_agent.py`

2. **"Permission denied" on image upload**
   - Check service account has `roles/storage.admin`
   - Verify bucket exists and is accessible

3. **"Model error" or "Quota exceeded"**
   - Check Vertex AI quotas in GCP console
   - Verify MODEL_NAME in .env matches available models

4. **UI not loading recipes**
   - Check Cloud Run logs: `gcloud run services logs read recipe-ai-app`
   - Verify .env has correct PROJECT_ID and AGENT_ID
   - Test agent directly: `python test_agent.py`

### Testing

**Local Backend Test:**
```bash
python test_agent.py
```

**Local Frontend Test:**
```bash
cd streamlit_app
streamlit run app.py
```

**End-to-End Test:**
1. Start local UI
2. Upload test image of ingredients
3. Verify ingredient analysis works
4. Select cuisine and generate recipes
5. Verify recipe output format

## Deployment

### Backend (Vertex AI Agent)
```bash
python deploy_agent.py
```
This deploys agents to Vertex AI Agent Engine (~2-3 minutes)

### Frontend (Cloud Run)
```bash
cd streamlit_app
python deploy_cloudrun.py
```
This containerizes and deploys UI to Cloud Run (~5-10 minutes)

**Note:** Both Python scripts work on Windows, Linux, and Mac. Bash scripts (.sh) are alternatives for Unix systems.

## Important Constraints

1. **Image Analysis**: Agents don't directly analyze images. The Streamlit app uses Gemini Vision API separately, then passes text results to agents.

2. **GCS URIs Only**: If using image URIs with agents, they must be `gs://` URIs (Google Cloud Storage), not local paths.

3. **Model Availability**: Uses `gemini-3-flash-preview` - verify this model is available in your region.

4. **Quota Limits**: Gemini API has rate limits. For production, consider implementing caching or rate limiting.

5. **Cost Awareness**: Each recipe generation involves multiple API calls (vision analysis + agent calls). See README.md for cost estimates.

## Environment Variables

### Backend `.env`
```bash
PROJECT_ID=your-gcp-project-id
REGION=us-central1
MODEL_NAME=gemini-3-flash-preview
AGENT_ENGINE_ID=        # Auto-populated after deployment
```

### Frontend `streamlit_app/.env`
```bash
PROJECT_ID=your-gcp-project-id              # Must match backend
REGION=us-central1                          # Must match backend
BUCKET_NAME=your-project-id-recipe-images   # For image storage
MODEL_NAME=gemini-3-flash-preview             # Must match backend
AGENT_ID=                                   # Optional - for deployed agent
DEBUG_MODE=false
```

## Extending the System

### Adding New Agent Capabilities

To add a new sub-agent:
1. Define new `LlmAgent` in `agents.py`
2. Add to parent agent's `sub_agents` list
3. Update parent's `instruction` to explain when to use new sub-agent
4. Redeploy: `python deploy_agent.py`

### Adding New Tools

Agents can use:
- `GoogleSearchTool()` - Already integrated
- `url_context` - Already integrated
- Custom tools - Define with `@agent_tool` decorator

### Adding Dietary Filters

**Files to modify:**
1. `streamlit_app/app.py` - Add UI controls
2. Pass dietary preferences in prompt to recipe_generator
3. Optionally update `recipe_generator.instruction` to emphasize dietary requirements

## Security Considerations

1. **Service Accounts**: Use least-privilege IAM roles
2. **API Keys**: Never commit `.env` files (in `.gitignore`)
3. **Image Storage**: Implement lifecycle policies to auto-delete old images
4. **Rate Limiting**: Consider implementing request limits per user
5. **Input Validation**: Streamlit app validates file types and sizes

## Performance Optimization

1. **Caching**: Use `@st.cache_data` for frequently requested recipes
2. **Image Compression**: Reduce image size before upload
3. **Min Instances**: Set to 0 for cost savings (cold starts acceptable)
4. **Max Instances**: Limit concurrent Cloud Run instances to control costs
5. **Timeouts**: Increase Cloud Run timeout if generation takes too long

## Monitoring

**View Logs:**
```bash
# Cloud Run logs (UI)
gcloud run services logs read recipe-ai-app --region=us-central1

# Filter errors
gcloud run services logs read recipe-ai-app --log-filter='severity>=ERROR'

# Real-time
gcloud run services logs tail recipe-ai-app --region=us-central1
```

**Check Status:**
```bash
# List agents
gcloud ai agents list --region=us-central1

# List services
gcloud run services list --region=us-central1

# Describe service
gcloud run services describe recipe-ai-app --region=us-central1
```

## Quick Reference for AI Assistants

When helping with this project:

1. **Agent Logic Changes** → Edit `agents.py`, redeploy with `deploy_agent.py`
2. **UI Changes** → Edit `streamlit_app/app.py`, redeploy with `deploy_cloudrun.py`
3. **Configuration** → Two separate `.env` files (root and streamlit_app)
4. **Testing** → `test_agent.py` for backend, `streamlit run app.py` for frontend
5. **Deployment** → Python scripts work everywhere, bash scripts for Unix only

**Always consider:**
- Cost implications of API calls
- Image analysis is separate from agents (Gemini Vision API)
- Changes to agents require redeployment
- UI changes require Cloud Run redeployment
- Test locally before deploying

## Resources

- **Google ADK Documentation**: Agent Development Kit reference
- **Vertex AI Agent Engine**: Managed agent deployment platform
- **Gemini API**: Vision and text generation models
- **Streamlit**: UI framework documentation
- **Cloud Run**: Serverless container platform

## Project Status

**Current State:** Production-ready multi-agent recipe system with web UI

**Future Improvements** (see README.md):
- Dietary filters (vegan, gluten-free, etc.)
- Save favorite recipes
- Multi-language support
- Nutritional information
- Shopping list generation

---

**For Users:** See `README.md`
**For AI Assistants:** This file (CLAUDE.MD)
**For Developers:** Both files + inline code comments
