"""
DEPLOYMENT TEMPLATE FOR ADK AGENTS
===================================

Instructions:
1. Copy this file to the root of your project
2. Update the variables in the CONFIGURATION section
3. Run: python deploy_agent.py

Author: Adri
Date: 2026-01-03
"""

import vertexai
from vertexai.agent_engines import AdkApp

# ============================================================================
# ⚙️ CONFIGURATION - UPDATE THESE VALUES ⚙️
# ============================================================================

PROJECT_ID = "gen-lang-client-0495395701"                  # Your Google Cloud Project ID
LOCATION = "us-central1"                        # Region (us-central1, europe-west1, etc.)
STAGING_BUCKET = "gs://adribucket2"             # Your GCS bucket (gs://bucket-name)

AGENT_FOLDER = "my_agent"              # Name of your agent folder
AGENT_DISPLAY_NAME = "City Views Finder"                 # Display name in UI
AGENT_DESCRIPTION = "AI agent that finds the best views, viewpoints, routes, paradores, and beautiful natural enclaves for a given city."   # Agent description

# Additional requirements (optional)
EXTRA_REQUIREMENTS = [
    # "langchain",
    # "pandas",
    # "requests",
]

# ============================================================================
# 🚀 DEPLOYMENT - DO NOT MODIFY THIS SECTION
# ============================================================================

def main():
    print("=" * 70)
    print("🚀 ADK AGENT DEPLOYMENT")
    print("=" * 70)
    
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
    print(f"\n📦 Importing agent from: {AGENT_FOLDER}")
    try:
        # Dynamic import
        import importlib
        agent_module = importlib.import_module(f"{AGENT_FOLDER}.agent")
        root_agent = agent_module.root_agent
        
        print(f"✅ Agent imported: {root_agent.name}")
        print(f"🔧 Model: {root_agent.model}")
        if hasattr(root_agent, 'tools') and root_agent.tools:
            print(f"🛠️  Tools: {len(root_agent.tools)} tools")
    except Exception as e:
        print(f"❌ Error importing agent: {e}")
        print(f"\nVerify that:")
        print(f"1. The folder '{AGENT_FOLDER}' exists")
        print(f"2. The file '{AGENT_FOLDER}/agent.py' exists")
        print(f"3. The file '{AGENT_FOLDER}/__init__.py' exports 'root_agent'")
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
            extra_packages=[f"./{AGENT_FOLDER}"],  # ⭐ IMPORTANT
            display_name=AGENT_DISPLAY_NAME,
            description=AGENT_DESCRIPTION,
        )
        
        print("\n" + "=" * 70)
        print("✅ DEPLOYMENT SUCCESSFUL!")
        print("=" * 70)
        
        print(f"\n📍 Resource Name:")
        print(f"   {remote_app.resource_name}")
        
        # Extract resource ID for URL
        resource_id = remote_app.resource_name.split('/')[-1]
        console_url = (
            f"https://console.cloud.google.com/vertex-ai/agents/"
            f"locations/{LOCATION}/agent-engines/{resource_id}"
            f"?project={PROJECT_ID}"
        )
        
        print(f"\n🔗 View in Google Cloud Console:")
        print(f"   {console_url}")
        
        print(f"\n🔧 To use in another script:")
        print(f"   from vertexai import agent_engines")
        print(f"   remote_app = agent_engines.get('{remote_app.resource_name}')")
        
        print(f"\n💡 Next step:")
        print(f"   1. Go to the URL above to test the agent in the UI")
        print(f"   2. Or use the test_agent.py script for programmatic testing")
        
        print("\n" + "=" * 70)
        
        # Save resource name for testing
        with open("agent_resource_name.txt", "w") as f:
            f.write(remote_app.resource_name)
        print(f"\n📝 Resource name saved to: agent_resource_name.txt")
        
    except Exception as e:
        print(f"\n❌ Deployment failed: {e}")
        print("\n🔍 Troubleshooting:")
        print("1. Verify bucket exists: gsutil ls " + STAGING_BUCKET)
        print("2. Verify credentials: gcloud auth application-default login")
        print("3. Check logs in Cloud Console")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
