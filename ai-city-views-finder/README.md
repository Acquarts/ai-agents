# 🏔️ City Views Finder

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.40.0-FF4B4B?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Google Cloud](https://img.shields.io/badge/Google%20Cloud-Run-4285F4?style=flat&logo=googlecloud&logoColor=white)](https://cloud.google.com/run)
[![Vertex AI](https://img.shields.io/badge/Vertex%20AI-Agent%20Engine-4285F4?style=flat&logo=google&logoColor=white)](https://cloud.google.com/vertex-ai)
[![Gemini](https://img.shields.io/badge/Gemini-2.5%20Flash-8E75B2?style=flat&logo=google&logoColor=white)](https://deepmind.google/technologies/gemini/)
[![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An AI agent specialized in discovering and recommending the best viewpoints, panoramic routes, paradores, and natural enclaves around any city.

**🌐 Live Demo:** [https://city-views-finder-562289298058.us-central1.run.app](https://city-views-finder-562289298058.us-central1.run.app)

---

## 📖 Description

**City Views Finder** is an intelligent agent built with Google Agent Development Kit (ADK) and Vertex AI Agent Engine that helps explorers, photographers, and travelers discover the most scenic places and viewpoints around any city in the world.

The agent uses real-time web searches and content analysis to provide high-quality, personalized recommendations, prioritizing authentic locations with exceptional visual value.

## ✨ Key Features

### 🤖 Agent Capabilities

- **Viewpoint Discovery**: Identifies the best urban and natural panoramic points
- **Scenic Routes**: Discovers panoramic roads, trails, and routes with exceptional views
- **Historic Paradores**: Recommends historic accommodations with stunning views
- **Natural Enclaves**: Finds cliffs, mountains, forests, coastlines, and nearby lakes
- **Authentic Places**: Prioritizes genuine experiences over generic tourist attractions

### 🛠️ Technology Stack

- **Model**: Gemini 2.5 Flash
- **Architecture**: Multi-agent system with specialized sub-agents
  - Web search agent (Google Search Tool)
  - Content analysis agent (URL Context Tool)
- **Frontend**: Streamlit with responsive design
- **Deployment**: Google Cloud Run (serverless)
- **Monitoring**: Cloud Logging and Cloud Monitoring integration
- **Containerization**: Docker

## 🚢 Deployment Architecture

This project uses **two separate deployments** working together:

### 1. **Vertex AI Agent Engine** (Backend - AI Brain 🤖)
- **What**: The intelligent agent that processes queries
- **Where**: Vertex AI Agent Engine on Google Cloud
- **Deploy with**: `python deploy_agent.py`
- **Does**:
  - Processes user queries intelligently
  - Uses Google Search Tool for web searches
  - Uses URL Context Tool for content analysis
  - Generates personalized recommendations
- **Cost**: Pay-per-use based on model calls and tokens

### 2. **Cloud Run** (Frontend - Web Interface 🌐)
- **What**: The Streamlit web interface users interact with
- **Where**: Google Cloud Run (serverless container platform)
- **Deploy with**: `deploy_cloudrun.bat` or `deploy_cloudrun.sh`
- **Does**:
  - Displays conversational interface
  - Manages user sessions
  - Connects to the agent in Vertex AI
  - Streams responses in real-time
- **Public URL**: https://city-views-finder-562289298058.us-central1.run.app
- **Cost**: Pay-per-use based on CPU/memory usage

### Flow Diagram

```
User → Cloud Run (Streamlit) → Vertex AI (Agent) → Response
```

**Note**: This project does NOT use Streamlit Cloud. Instead, it uses Docker to containerize the Streamlit app and deploys it to Cloud Run for better control, scalability, and integration with Google Cloud services.

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     User (Web Browser)                       │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              Cloud Run (Streamlit Frontend)                  │
│  - Conversational interface                                  │
│  - Session management                                        │
│  - Response streaming                                        │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│           Vertex AI Agent Engine (ADK)                       │
│                                                              │
│  ┌────────────────────────────────────────────────┐         │
│  │  City Views Finder Agent (Root)                │         │
│  │  - Coordinates searches and analysis           │         │
│  │  - Filters and evaluates recommendations       │         │
│  └──────────────────┬─────────────────────────────┘         │
│                     │                                        │
│          ┌──────────┴──────────┐                            │
│          ▼                     ▼                             │
│  ┌──────────────┐      ┌──────────────────┐                │
│  │ Google       │      │ URL Context      │                │
│  │ Search Agent │      │ Agent            │                │
│  └──────────────┘      └──────────────────┘                │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│         Cloud Logging & Monitoring                           │
│  - Structured logs (JSON)                                    │
│  - Usage and performance metrics                             │
│  - Automatic alerts                                          │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- Google Cloud account with billing enabled
- [Google Cloud SDK](https://cloud.google.com/sdk/docs/install)
- Created Google Cloud project

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/Acquarts/ai-agents.git
cd ai-agents/ai-city-views-finder
```

2. **Create virtual environment**

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Configure Google Cloud**

```bash
# Authenticate with Google Cloud
gcloud auth login

# Set your project
gcloud config set project YOUR_PROJECT_ID

# Configure application credentials
gcloud auth application-default login
```

5. **Set environment variables**

Create a `.env` file:

```env
PROJECT_ID=your-project-id
LOCATION=us-central1
```

## 💻 Usage

### Option 1: Local Development

#### Deploy Agent to Vertex AI

```bash
python deploy_agent.py
```

This will:
- Compile the agent from `my_agent/agent.py`
- Deploy it to Vertex AI Agent Engine
- Save the resource name to `agent_resource_name.txt`

#### Test Locally

```bash
python test_agent.py
```

Interactive mode example:
```
Chat with the agent (type 'exit' to quit):

You: Find scenic viewpoints around Barcelona
Agent: Based on my research, here are the best viewpoints around Barcelona:

1. Bunkers del Carmel
   Type: Urban viewpoint
   Description: 360° panoramic views of Barcelona, coast, and Sagrada Familia
   Why special: Former anti-aircraft battery, authentic neighborhood vibe
   Distance: 4.5 km from city center
   Best time: Sunset
[...]
```

### Option 2: Cloud Run Deployment (Production)

#### Deploy to Cloud Run

**Windows:**
```bash
deploy_cloudrun.bat
```

**Linux/Mac:**
```bash
chmod +x deploy_cloudrun.sh
./deploy_cloudrun.sh
```

The script will:
1. ✅ Enable required Google Cloud APIs
2. 🐳 Build the Docker image
3. 🚀 Deploy to Cloud Run
4. ⚙️ Configure environment variables
5. 🌐 Display the public URL

#### Access Your Application

Visit the deployed app: **[https://city-views-finder-562289298058.us-central1.run.app](https://city-views-finder-562289298058.us-central1.run.app)**

## 📁 Project Structure

```
ai-city-views-finder/
├── my_agent/
│   ├── __init__.py
│   └── agent.py                 # Main agent definition
├── deploy_agent.py              # Vertex AI deployment script
├── test_agent.py                # Local testing script
├── streamlit_app.py             # Streamlit frontend for Cloud Run
├── requirements.txt             # Local development dependencies
├── requirements_cloudrun.txt    # Cloud Run dependencies
├── Dockerfile                   # Container configuration
├── .dockerignore               # Build exclusions
├── deploy_cloudrun.bat         # Windows deployment script
├── deploy_cloudrun.sh          # Linux/Mac deployment script
├── monitoring_config.yaml      # Monitoring configuration
├── .gitignore                  # Git exclusions
└── README.md                   # This file
```

## 🎯 Agent Evaluation Criteria

The agent evaluates each recommendation using:

1. **Visual Impact**: Panoramic quality and landscape composition
2. **Natural Beauty**: Natural environment and scenic elements
3. **Authenticity**: Avoids overly commercial places
4. **Accessibility**: Ease of access (car, walking, short routes)
5. **Proximity**: Distance from the city (clearly indicated)
6. **Purpose**: Suitability for photography, walks, or quiet exploration

## 💡 Usage Examples

### Example 1: Basic Search

**Input:**
```
Find viewpoints around Granada
```

**Output:**
```
Here are the best scenic viewpoints around Granada:

1. Mirador de San Nicolás
   Type: Urban viewpoint
   Description: Iconic views of the Alhambra with Sierra Nevada backdrop
   Why special: Classic Granada vista, popular at sunset
   Distance: In Albaicín neighborhood, 1.5 km from center
   Best time: Late afternoon for best light

2. Silla del Moro
   Type: Mountain lookout
   Description: Elevated viewpoint overlooking the Alhambra from above
   Why special: Less crowded, aerial perspective of the palace complex
   Distance: 3 km southeast, 30-minute hike
   Accessibility: Walking trail from Generalife
[...]
```

### Example 2: Specific Search

**Input:**
```
Show me panoramic driving routes near San Sebastian
```

**Output:**
```
Here are the best panoramic routes around San Sebastián:

1. Jaizkibel Coastal Road (GI-3440)
   Type: Scenic coastal drive
   Description: Dramatic coastal route between Pasajes and Hondarribia
   Why special: Spectacular Atlantic views, clifftop perspectives
   Distance: 15 km from San Sebastián
   Duration: 30-minute drive, multiple viewpoint stops
[...]
```

## 📊 Monitoring and Logs

This project has **two separate monitoring systems** for each deployment:

### 🌐 Cloud Run Monitoring (Frontend)

Monitors the **Streamlit application and infrastructure**.

#### What it tracks:
- **Container Performance**: CPU, memory usage, active instances, cold starts
- **Web Traffic**: Requests/second, HTTP status codes, response latency
- **Custom Application Logs**: User queries, response times, errors

#### View Logs:

```bash
# Cloud Run service logs
gcloud run services logs read city-views-finder --region us-central1 --limit 50

# Follow logs in real-time
gcloud run services logs tail city-views-finder --region us-central1

# Or in the console:
# https://console.cloud.google.com/run/detail/us-central1/city-views-finder
```

#### Useful Cloud Logging Queries

**View all user queries:**
```
resource.type="cloud_run_revision"
jsonPayload.event="user_query"
```

**View errors:**
```
resource.type="cloud_run_revision"
jsonPayload.event="error"
```

**View slow responses (>10 seconds):**
```
resource.type="cloud_run_revision"
jsonPayload.event="agent_response"
jsonPayload.response_time_seconds>10
```

#### Available Metrics:
- 📈 Total user queries
- ⏱️ Average response time
- ❌ Error rate
- 💾 Memory and CPU usage
- 🖥️ Number of active instances

#### Answers:
- ✅ Is the app running?
- ⚡ Is the interface responsive?
- 🔍 Are there Streamlit errors?
- 👥 How many users are connected?

---

### 🤖 Vertex AI Monitoring (Backend)

Monitors the **AI agent and its operations**.

#### What it tracks:
- **Model Usage**: Number of calls to Gemini, tokens consumed (input/output), cost per call
- **Agent Performance**: Inference latency, processing time, success/failure rate
- **Tool Usage**: Google Search calls, URL Context calls, tool failures
- **Agent Content**: Queries received, responses generated, reasoning errors

#### View Logs:

```bash
# Vertex AI console
# https://console.cloud.google.com/vertex-ai/reasoning-engines

# Or via API
gcloud ai reasoning-engines describe AGENT_ID --region=us-central1
```

#### Available Metrics:
- 💰 Tokens consumed per query
- 🔧 Tool usage frequency
- 🎯 Response quality
- 💸 Cost per interaction

#### Answers:
- 🧠 Is the agent reasoning correctly?
- 💵 How much does each query cost?
- 🛠️ Are the tools (Google Search, URL Context) working?
- ❌ Are there logic errors in the agent?

---

### 🔍 Monitoring Comparison

| Aspect | Cloud Run | Vertex AI |
|--------|-----------|-----------|
| **Monitors** | Frontend/Infrastructure | AI Agent/Model |
| **Key Metrics** | HTTP, CPU, memory | Tokens, calls, tools |
| **Logs** | Streamlit application | Agent reasoning |
| **Cost Driver** | Compute resources | Model tokens |
| **Key Question** | Is the app working? | Is the agent smart? |

**Example Investigation**: If users report "slow responses":
1. **Check Cloud Run**: See response times in logs → 15 seconds average
2. **Check Vertex AI**: Agent makes 10 Google searches per query, each takes 1.5s
3. **Solution**: Optimize agent to make fewer searches

## 🔄 Updating the Service

To update after making changes:

```bash
# Option 1: Re-run deployment script
deploy_cloudrun.bat  # Windows
./deploy_cloudrun.sh  # Linux/Mac

# Option 2: Manual commands
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/city-views-finder
gcloud run deploy city-views-finder \
  --image gcr.io/YOUR_PROJECT_ID/city-views-finder \
  --region us-central1
```

## 🐛 Troubleshooting

### Error: "Agent not found"

**Cause**: Agent not deployed or resource name is incorrect.

**Solution**:
```bash
# Verify agent_resource_name.txt exists
cat agent_resource_name.txt

# Re-deploy the agent
python deploy_agent.py
```

### Error: "Permission denied"

**Cause**: Missing permissions in the project.

**Solution**:
```bash
# Check current permissions
gcloud projects get-iam-policy YOUR_PROJECT_ID

# Grant necessary permissions
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
  --member="user:your-email@gmail.com" \
  --role="roles/run.admin"
```

### Performance Issues

If the service is slow:

```bash
# Increase resources
gcloud run services update city-views-finder \
  --region us-central1 \
  --memory 4Gi \
  --cpu 4

# Configure minimum instances (avoids cold starts)
gcloud run services update city-views-finder \
  --region us-central1 \
  --min-instances 1
```

## 💰 Cost Estimates

### Monthly Estimate (moderate usage)

| Service | Description | Estimated Cost |
|---------|-------------|----------------|
| Cloud Run | Streamlit frontend | $10-50/month |
| Vertex AI Agent Engine | Agent processing | $20-100/month |
| Cloud Logging | Logs and monitoring | $0-10/month |
| **Total** | | **$30-160/month** |

### Cost Optimization Tips

1. **Scale to zero**: Configure `min-instances=0`
2. **Limit instances**: Set appropriate `max-instances`
3. **Reduce logs**: Minimize verbose logs in production
4. **Budget alerts**: Configure budget alerts in Google Cloud Console

## 🔧 Technologies Used

- **[Google Agent Development Kit (ADK)](https://cloud.google.com/products/agent-builder)**: AI agent framework
- **[Vertex AI Agent Engine](https://cloud.google.com/vertex-ai/docs/generative-ai/agents/overview)**: Agent execution platform
- **[Gemini 2.5 Flash](https://deepmind.google/technologies/gemini/)**: Language model
- **[Streamlit](https://streamlit.io/)**: Python UI framework
- **[Google Cloud Run](https://cloud.google.com/run)**: Serverless platform
- **[Cloud Logging](https://cloud.google.com/logging/docs)**: Structured logging system
- **[Cloud Monitoring](https://cloud.google.com/monitoring/docs)**: Monitoring and alerts
- **[Docker](https://www.docker.com/)**: Containerization

## ⚙️ Technical Features

### Frontend (Streamlit)

- Real-time conversational interface
- Live response streaming with updates
- Persistent session management
- Conversation history
- Responsive and modern design
- Integrated structured logging

### Backend (Vertex AI Agent Engine)

- Multi-agent architecture
- Specialized tools:
  - Google Search for web searches
  - URL Context for content analysis
- Asynchronous processing
- Robust error handling

### Infrastructure

- Serverless deployment on Cloud Run
- Horizontal auto-scaling
- Native HTTPS
- Structured JSON logs
- Custom metrics
- Optimized resource configuration

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License. See `LICENSE` file for details.

## 👤 Author

**Adri**
Date: 2026-01-11

## 📚 Additional Resources

- [Google Agent Builder Documentation](https://cloud.google.com/products/agent-builder)
- [Vertex AI Generative AI Documentation](https://cloud.google.com/vertex-ai/docs/generative-ai/learn/overview)
- [Cloud Run Documentation](https://cloud.google.com/run/docs)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Gemini API Documentation](https://ai.google.dev/gemini-api/docs)

## 💬 Support

For issues or questions:

1. Check the [Troubleshooting](#-troubleshooting) section
2. Review logs: `gcloud run services logs read city-views-finder --region us-central1`
3. Create an issue in the [GitHub repository](https://github.com/Acquarts/ai-agents/issues)

---

**Version**: 1.0
**Last updated**: 2026-01-11
**Live Demo**: [https://city-views-finder-562289298058.us-central1.run.app](https://city-views-finder-562289298058.us-central1.run.app)
