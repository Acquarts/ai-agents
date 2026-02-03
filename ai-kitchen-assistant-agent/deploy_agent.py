"""
RECIPE MULTI-AGENT DEPLOYMENT
==============================

Simple Python deployment script for Windows/Linux/Mac

Instructions:
1. Configure your PROJECT_ID below
2. Run: python deploy_agent.py

Author: Adapted for Recipe Multi-Agent
Date: 2025-01-18
"""

import vertexai
from vertexai.agent_engines import AdkApp
import os

# ============================================================================
# ⚙️ CONFIGURATION - UPDATE THESE VALUES
# ============================================================================

PROJECT_ID = "gen-lang-client-0495395701"        # Your Google Cloud Project ID
LOCATION = "us-central1"                         # Region (us-central1, europe-west1, etc.)
STAGING_BUCKET = "gs://adribucket2"              # Your GCS bucket (gs://bucket-name)

AGENT_DISPLAY_NAME = "Recipe Coordinator Multi-Agent"
AGENT_DESCRIPTION = "AI multi-agent system that analyzes food images and generates authentic regional recipes"

# Additional requirements (optional)
EXTRA_REQUIREMENTS = [
    # Add any extra packages if needed
]

# ============================================================================
# 🚀 DEPLOYMENT - DO NOT MODIFY BELOW
# ============================================================================

def main():
    print("=" * 70)
    print("🍳 RECIPE MULTI-AGENT DEPLOYMENT")
    print("=" * 70)
    
    # Verify agents.py exists
    if not os.path.exists("agents.py"):
        print("\n❌ Error: agents.py not found!")
        print("Make sure you're running this script from the project root directory")
        return
    
    # Initialize Vertex AI
    print(f"\n📍 Project: {PROJECT_ID}")
    print(f"📍 Region: {LOCATION}")
    print(f"📍 Bucket: {STAGING_BUCKET}")
    
    vertexai.init(
        project=PROJECT_ID,
        location=LOCATION,
        staging_bucket=STAGING_BUCKET
    )
    
    # Import the agent
    print(f"\n📦 Importing agents from agents.py...")
    try:
        from agents import root_agent, food_analyzer, recipe_generator
        
        print(f"✅ Root Agent: {root_agent.name}")
        print(f"   Model: {root_agent.model}")
        print(f"   Subagents: {len(root_agent.sub_agents)}")
        for subagent in root_agent.sub_agents:
            print(f"      • {subagent.name}")
        
    except Exception as e:
        print(f"❌ Error importing agents: {e}")
        print(f"\nVerify that:")
        print(f"1. agents.py exists in current directory")
        print(f"2. agents.py defines root_agent, food_analyzer, recipe_generator")
        return
    
    # Create AdkApp wrapper
    print(f"\n🔨 Creating AdkApp...")
    app = AdkApp(agent=root_agent)
    
    # Prepare requirements
    requirements = [
        "google-cloud-aiplatform[adk,agent_engines]>=1.132.0",
    ] + EXTRA_REQUIREMENTS
    
    print(f"\n📚 Requirements:")
    for req in requirements:
        print(f"   - {req}")
    
    # Deploy to Agent Engine
    print(f"\n🚀 Deploying to Agent Engine...")
    print("⏳ This may take 2-5 minutes...")
    
    try:
        from vertexai import agent_engines
        
        remote_app = agent_engines.create(
            app,
            requirements=requirements,
            display_name=AGENT_DISPLAY_NAME,
            description=AGENT_DESCRIPTION,
        )
        
        print("\n" + "=" * 70)
        print("✅ DEPLOYMENT SUCCESSFUL!")
        print("=" * 70)
        
        print(f"\n🔗 Resource Name:")
        print(f"   {remote_app.resource_name}")
        
        # Extract resource ID for URL
        resource_id = remote_app.resource_name.split('/')[-1]
        console_url = (
            f"https://console.cloud.google.com/vertex-ai/agents/"
            f"locations/{LOCATION}/agent-engines/{resource_id}"
            f"?project={PROJECT_ID}"
        )
        
        print(f"\n🌐 View in Google Cloud Console:")
        print(f"   {console_url}")
        
        print(f"\n💻 To use in another script:")
        print(f"   from vertexai import agent_engines")
        print(f"   remote_app = agent_engines.get('{remote_app.resource_name}')")
        
        print(f"\n📋 Next steps:")
        print(f"   1. Test the agent at the URL above")
        print(f"   2. Deploy the Streamlit UI:")
        print(f"      cd streamlit_app")
        print(f"      python deploy_cloudrun.py")
        
        print("\n" + "=" * 70)
        
        # Save resource name for later use
        with open("agent_resource_name.txt", "w") as f:
            f.write(remote_app.resource_name)
        print(f"\n💾 Resource name saved to: agent_resource_name.txt")
        
        # Save AGENT_ID for Streamlit config
        agent_id = resource_id
        print(f"\n⚙️  Add this to streamlit_app/.env:")
        print(f"   AGENT_ID={agent_id}")
        
    except Exception as e:
        print(f"\n❌ Deployment failed: {e}")
        print("\n🔍 Troubleshooting:")
        print(f"1. Verify bucket exists:")
        print(f"   gsutil ls {STAGING_BUCKET}")
        print(f"2. Verify credentials:")
        print(f"   gcloud auth application-default login")
        print(f"3. Check if APIs are enabled:")
        print(f"   gcloud services enable aiplatform.googleapis.com --project={PROJECT_ID}")
        print(f"4. Check logs in Cloud Console")
        
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
