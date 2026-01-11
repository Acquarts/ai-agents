# City Views Finder

An AI agent specialized in discovering and recommending the best viewpoints, panoramic routes, paradores, and natural enclaves around any city.

## Description

**City Views Finder** is an intelligent agent built with Google Agent Development Kit (ADK) and Vertex AI Agent Engine that helps explorers, photographers, and travelers discover the most scenic places and viewpoints around any city in the world.

The agent uses real-time web searches and content analysis to provide high-quality, personalized recommendations, prioritizing authentic locations with exceptional visual value.

## Key Features

### Agent Capabilities

- **Viewpoint Discovery**: Identifies the best urban and natural panoramic points
- **Scenic Routes**: Discovers panoramic roads, trails, and routes with exceptional views
- **Historic Paradores**: Recommends historic accommodations with stunning views
- **Natural Enclaves**: Finds cliffs, mountains, forests, coastlines, and nearby lakes
- **Authentic Places**: Prioritizes genuine experiences over generic tourist attractions

### Technology

- **Model**: Gemini 2.5 Flash
- **Architecture**: Multi-agent with specialization
  - Web search agent (Google Search)
  - Content analysis agent (URL Context)
- **Frontend**: Streamlit with responsive design
- **Deployment**: Google Cloud Run (serverless)
- **Monitoring**: Integrated Cloud Logging and Cloud Monitoring

## Architecture

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

## Installation and Setup

### Prerequisites

- Python 3.11 or higher
- Google Cloud account with billing enabled
- Google Cloud SDK ([Install](https://cloud.google.com/sdk/docs/install))
- Created Google Cloud project

### 1. Clone the Repository

```bash
git clone <repository-url>
cd ai-city-views-finder
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Google Cloud

```bash
# Authenticate with Google Cloud
gcloud auth login

# Set the project
gcloud config set project gen-lang-client-0495395701

# Configure application credentials
gcloud auth application-default login
```

### 5. Configure Environment Variables

Create a `.env` file in the project root:

```env
PROJECT_ID=gen-lang-client-0495395701
LOCATION=us-central1
```

## Usage

### Option 1: Local Usage (Development)

#### Deploy the Agent to Vertex AI

```bash
python deploy_agent.py
```

This command:
- Compiles the agent from `my_agent/agent.py`
- Deploys it to Vertex AI Agent Engine
- Saves the resource name to `agent_resource_name.txt`

#### Test the Agent Locally

```bash
python test_agent.py
```

Interactive mode:
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

#### Deploy Frontend to Cloud Run

**Windows:**
```bash
deploy_cloudrun.bat
```

**Linux/Mac:**
```bash
chmod +x deploy_cloudrun.sh
./deploy_cloudrun.sh
```

The script automatically:
1. Enables required Google Cloud APIs
2. Builds the Docker image
3. Deploys the service to Cloud Run
4. Configures environment variables
5. Displays the public service URL

#### Access the Application

Once deployed, access the provided URL:
```
https://city-views-finder-XXXXX.us-central1.run.app
```

## Project Structure

```
ai-city-views-finder/
├── my_agent/
│   ├── __init__.py
│   └── agent.py                 # Main agent definition
├── deploy_agent.py              # Vertex AI deployment script
├── test_agent.py                # Local testing script
├── streamlit_app.py             # Streamlit frontend for Cloud Run
├── requirements.txt             # Dependencies for local development
├── Dockerfile                   # Container configuration
├── .dockerignore               # Files excluded from build
├── deploy_cloudrun.bat         # Deployment script (Windows)
├── deploy_cloudrun.sh          # Deployment script (Linux/Mac)
├── monitoring_config.yaml      # Monitoring configuration
├── README.md                   # This file
```

## Agent Evaluation Criteria

The agent evaluates each recommendation using the following criteria:

1. **Visual Impact**: Panoramic quality and landscape composition
2. **Natural Beauty**: Natural environment and scenic elements
3. **Authenticity**: Avoids overly commercial places
4. **Accessibility**: Ease of access (car, walking, short routes)
5. **Proximity**: Distance from the city (clearly indicated)
6. **Purpose**: Suitability for photography, walks, or quiet exploration

## Usage Examples

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

## Monitoring and Logs

### View Real-Time Logs

```bash
# Cloud Run service logs
gcloud run services logs read city-views-finder --region us-central1 --limit 50

# Follow logs in real-time
gcloud run services logs tail city-views-finder --region us-central1
```

### Useful Cloud Logging Queries

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

### Available Metrics

- Total user queries
- Average response time
- Error rate
- Memory and CPU usage
- Number of active instances

## Service Updates

To update the application after making changes:

```bash
# Option 1: Re-run deployment script
deploy_cloudrun.bat  # Windows
./deploy_cloudrun.sh  # Linux/Mac

# Option 2: Manual commands
gcloud builds submit --tag gcr.io/gen-lang-client-0495395701/city-views-finder
gcloud run deploy city-views-finder \
  --image gcr.io/gen-lang-client-0495395701/city-views-finder \
  --region us-central1
```

## Troubleshooting

### Error: "Agent not found"

**Cause**: Agent not deployed or resource name is incorrect.

**Solution**:
```bash
# Verify agent_resource_name.txt exists
cat agent_resource_name.txt

# Re-deploy the agent if necessary
python deploy_agent.py
```

### Error: "Permission denied"

**Cause**: Missing permissions in the project.

**Solution**:
```bash
# Check current permissions
gcloud projects get-iam-policy gen-lang-client-0495395701

# Grant necessary permissions
gcloud projects add-iam-policy-binding gen-lang-client-0495395701 \
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

## Cost Estimates

### Monthly Estimate (moderate usage)

| Service | Description | Estimated Cost |
|---------|-------------|----------------|
| Cloud Run | Streamlit frontend | $10-50/month |
| Vertex AI Agent Engine | Agent processing | $20-100/month |
| Cloud Logging | Logs and monitoring | $0-10/month |
| **Total** | | **$30-160/month** |

### Cost Optimization

1. **Scale to zero**: Configure `min-instances=0`
2. **Limit instances**: Configure appropriate `max-instances`
3. **Reduce logs**: Minimize verbose logs in production
4. **Budgets**: Configure budget alerts in Google Cloud

## Technologies Used

- **Google Agent Development Kit (ADK)**: AI agent framework
- **Vertex AI Agent Engine**: Agent execution platform
- **Gemini 2.5 Flash**: Language model
- **Streamlit**: Python UI framework
- **Google Cloud Run**: Serverless platform
- **Cloud Logging**: Structured logging system
- **Cloud Monitoring**: Monitoring and alerts
- **Docker**: Containerization

## Technical Features

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

## Contributing

To contribute to the project:

1. Fork the repository
2. Create a branch for your feature (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## License

This project is licensed under the MIT License. See `LICENSE` file for details.

## Author

**Adri**
Date: 2026-01-11

## Additional Resources

- [Google Agent Development Kit Documentation](https://cloud.google.com/vertex-ai/docs/agent-builder)
- [Cloud Run Documentation](https://cloud.google.com/run/docs)
- [Streamlit Documentation](https://docs.streamlit.io)
- [Vertex AI Documentation](https://cloud.google.com/vertex-ai/docs)
- [Detailed Cloud Run Guide](README_CLOUDRUN.md)

## Support

For issues or questions:

1. Check the [Troubleshooting](#troubleshooting) section
2. Consult [README_CLOUDRUN.md](README_CLOUDRUN.md) for Cloud Run-specific details
3. Review logs: `gcloud run services logs read city-views-finder --region us-central1`
4. Create an issue in the repository

---

**Version**: 1.0
**Last updated**: 2026-01-11
