"""
TESTING TEMPLATE FOR DEPLOYED ADK AGENTS
=========================================

Instructions:
1. Copy this file to the root of your project
2. Update PROJECT_ID and LOCATION
3. AGENT_RESOURCE_NAME will be read automatically from agent_resource_name.txt
   (or update it manually)
4. Run: python test_agent.py

Author: Adri
Date: 2026-01-03
"""

import asyncio
import vertexai
from pathlib import Path

# ============================================================================
# ⚙️ CONFIGURATION - UPDATE THESE VALUES ⚙️
# ============================================================================

PROJECT_ID = "gen-lang-client-0495395701"
LOCATION = "us-central1"

# Will attempt to read from agent_resource_name.txt, or use this value:
AGENT_RESOURCE_NAME = "projects/.../locations/.../reasoningEngines/..."

# Test messages
TEST_MESSAGES = [
    "Hello! What can you help me with?",
    "Tell me about yourself",
    # Add more test messages here
]

# ============================================================================
# 🧪 TESTING - DO NOT MODIFY THIS SECTION
# ============================================================================

async def test_agent():
    """Main testing function"""
    
    print("=" * 70)
    print("🧪 TESTING ADK AGENT")
    print("=" * 70)
    
    # Try to read resource name from file
    global AGENT_RESOURCE_NAME
    resource_file = Path("agent_resource_name.txt")
    if resource_file.exists():
        AGENT_RESOURCE_NAME = resource_file.read_text().strip()
        print(f"\n📄 Resource name read from: agent_resource_name.txt")
    
    print(f"\n📍 Project: {PROJECT_ID}")
    print(f"📍 Region: {LOCATION}")
    print(f"📍 Agent: {AGENT_RESOURCE_NAME}")
    
    # Initialize Vertex AI
    vertexai.init(project=PROJECT_ID, location=LOCATION)
    
    # Get deployed agent
    print(f"\n🔍 Getting deployed agent...")
    try:
        from vertexai import agent_engines
        remote_app = agent_engines.get(AGENT_RESOURCE_NAME)
        print(f"✅ Agent found!")
    except Exception as e:
        print(f"❌ Error getting agent: {e}")
        print(f"\nVerify:")
        print(f"1. The resource name is correct")
        print(f"2. The agent exists at: https://console.cloud.google.com/vertex-ai/agents")
        return
    
    # Create a session
    print(f"\n📝 Creating test session...")
    try:
        session = await remote_app.async_create_session(user_id="test_user")
        session_id = session["id"]
        print(f"✅ Session created: {session_id}")
    except Exception as e:
        print(f"❌ Error creating session: {e}")
        return
    
    # Run tests
    print(f"\n" + "=" * 70)
    print(f"🧪 RUNNING {len(TEST_MESSAGES)} TESTS")
    print("=" * 70)
    
    for i, message in enumerate(TEST_MESSAGES, 1):
        print(f"\n{'─' * 70}")
        print(f"Test {i}/{len(TEST_MESSAGES)}")
        print(f"{'─' * 70}")
        print(f"👤 User: {message}")
        print(f"🤖 Agent: ", end="", flush=True)
        
        try:
            response_text = ""
            async for event in remote_app.async_stream_query(
                user_id="test_user",
                session_id=session_id,
                message=message,
            ):
                # Extract text from event
                if hasattr(event, 'content'):
                    if hasattr(event.content, 'parts'):
                        for part in event.content.parts:
                            if hasattr(part, 'text'):
                                text = part.text
                                print(text, end="", flush=True)
                                response_text += text
                    elif hasattr(event.content, 'text'):
                        text = event.content.text
                        print(text, end="", flush=True)
                        response_text += text
            
            print()  # New line
            
            if not response_text:
                print("⚠️  No text response received")
                print(f"Full event: {event}")
                
        except Exception as e:
            print(f"\n❌ Test error: {e}")
            import traceback
            traceback.print_exc()
    
    # Summary
    print(f"\n" + "=" * 70)
    print(f"✅ TESTS COMPLETED")
    print("=" * 70)
    print(f"\n💡 For more testing, go to:")
    resource_id = AGENT_RESOURCE_NAME.split('/')[-1]
    console_url = (
        f"https://console.cloud.google.com/vertex-ai/agents/"
        f"locations/{LOCATION}/agent-engines/{resource_id}"
        f"?project={PROJECT_ID}"
    )
    print(f"   {console_url}")


async def list_sessions():
    """Helper function to list existing sessions"""
    
    vertexai.init(project=PROJECT_ID, location=LOCATION)
    
    from vertexai import agent_engines
    remote_app = agent_engines.get(AGENT_RESOURCE_NAME)
    
    print("\n📋 Listing existing sessions...")
    sessions = await remote_app.async_list_sessions(user_id="test_user")
    
    if sessions:
        print(f"Found {len(sessions)} sessions:")
        for session in sessions:
            print(f"  - {session['id']}")
    else:
        print("No existing sessions")


def main():
    """Main entry point"""
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--list-sessions":
        asyncio.run(list_sessions())
    else:
        asyncio.run(test_agent())


if __name__ == "__main__":
    main()
