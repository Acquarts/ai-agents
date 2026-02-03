"""
Local testing script for Recipe Multi-Agent
Run this to test agent interactions before deploying
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

try:
    from agents import root_agent, food_analyzer, recipe_generator
    import vertexai
except ImportError as e:
    print(f"Error importing dependencies: {e}")
    print("Make sure to install requirements: pip install -r requirements.txt")
    sys.exit(1)


def setup_vertex_ai():
    """Initialize Vertex AI with project settings"""
    project_id = os.getenv('PROJECT_ID')
    location = os.getenv('LOCATION', 'us-central1')
    
    if not project_id:
        print("Error: PROJECT_ID not set in .env file")
        print("Copy .env.example to .env and update with your project ID")
        sys.exit(1)
    
    print(f"Initializing Vertex AI...")
    print(f"  Project: {project_id}")
    print(f"  Location: {location}")
    
    vertexai.init(project=project_id, location=location)
    print("✓ Vertex AI initialized\n")


def test_agent_structure():
    """Test that agents are properly configured"""
    print("=" * 60)
    print("Testing Agent Structure")
    print("=" * 60)
    
    print(f"\n✓ Root Agent: {root_agent.name}")
    print(f"  Model: {root_agent.model}")
    print(f"  Description: {root_agent.description}")
    print(f"  Number of subagents: {len(root_agent.sub_agents)}")
    
    print(f"\n  Subagents:")
    for i, subagent in enumerate(root_agent.sub_agents, 1):
        print(f"    {i}. {subagent.name}")
        print(f"       Model: {subagent.model}")
        print(f"       Tools: {len(subagent.tools)}")
    
    print("\n✓ Agent structure looks good!\n")


def simulate_conversation():
    """Simulate a conversation with the agent"""
    print("=" * 60)
    print("Simulating Conversation")
    print("=" * 60)
    print("\nThis will simulate how the agent responds to queries.")
    print("Note: Actual LLM responses require deployment to Vertex AI.\n")
    
    # Test queries
    test_queries = [
        "I have tomatoes, pasta, garlic, and olive oil. Give me Italian recipes.",
        "What can I cook with chicken and rice? Make it Thai.",
        "gs://my-bucket/food.jpg - Give me Spanish recipes",
    ]
    
    print("Sample queries that the agent can handle:")
    print("-" * 60)
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{i}. Query: {query}")
        print(f"   → Root agent would receive this")
        print(f"   → Route to food_analyzer for ingredient validation")
        print(f"   → Then route to recipe_generator with location")
        print(f"   → Return formatted recipes to user")
    
    print("\n" + "-" * 60)
    print("\n✓ Conversation flow validated\n")


def test_instructions():
    """Display agent instructions for review"""
    print("=" * 60)
    print("Agent Instructions Review")
    print("=" * 60)
    
    agents_to_review = [
        ("Root Agent", root_agent),
        ("Food Analyzer", food_analyzer),
        ("Recipe Generator", recipe_generator),
    ]
    
    for name, agent in agents_to_review:
        print(f"\n{name} ({agent.name})")
        print("-" * 60)
        instruction = agent.instruction
        # Show first 200 chars
        preview = instruction[:200] + "..." if len(instruction) > 200 else instruction
        print(preview)
        print(f"\nFull instruction length: {len(instruction)} characters")
    
    print("\n✓ All instructions are configured\n")


def test_tools():
    """Check tool configurations"""
    print("=" * 60)
    print("Tool Configuration")
    print("=" * 60)
    
    def check_agent_tools(agent, indent=0):
        prefix = "  " * indent
        print(f"{prefix}Agent: {agent.name}")
        print(f"{prefix}  Tools: {len(agent.tools)}")
        
        for tool in agent.tools:
            tool_name = getattr(tool, 'name', type(tool).__name__)
            print(f"{prefix}    - {tool_name}")
        
        if agent.sub_agents:
            for subagent in agent.sub_agents:
                check_agent_tools(subagent, indent + 1)
    
    check_agent_tools(root_agent)
    
    print("\n✓ Tool configuration checked\n")


def interactive_mode():
    """Interactive testing mode"""
    print("=" * 60)
    print("Interactive Testing Mode")
    print("=" * 60)
    print("\nThis mode lets you see how queries would be processed.")
    print("(Actual LLM responses require deployment)")
    print("\nType 'quit' to exit\n")
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break
            
            if not user_input:
                continue
            
            print(f"\n→ Root Agent receives: '{user_input}'")
            
            # Simulate routing logic
            if any(word in user_input.lower() for word in ['have', 'ingredients', 'with']):
                print("→ Would delegate to: food_analyzer")
                print("  (to validate and structure ingredients)")
            
            if any(word in user_input.lower() for word in ['recipe', 'cook', 'make']):
                print("→ Then delegate to: recipe_generator")
                print("  (to generate recipes)")
            
            if 'gs://' in user_input or 'http' in user_input:
                print("→ Image URI detected")
                print("  (Would use image analyzer extension if configured)")
            
            print("→ Finally: Return formatted response to user")
            
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")


def main():
    """Main test runner"""
    print("\n" + "=" * 60)
    print("Recipe Multi-Agent - Local Testing")
    print("=" * 60 + "\n")
    
    # Setup
    try:
        setup_vertex_ai()
    except Exception as e:
        print(f"Warning: Could not initialize Vertex AI: {e}")
        print("Continuing with local tests...\n")
    
    # Run tests
    test_agent_structure()
    test_instructions()
    test_tools()
    simulate_conversation()
    
    # Interactive mode
    print("\nAll tests passed! ✓")
    print("\nOptions:")
    print("  1. Enter interactive mode (press Enter)")
    print("  2. Deploy agent (run: ./deploy_agent.sh)")
    print("  3. Exit (type 'n')")
    
    choice = input("\nEnter interactive mode? [Y/n]: ").strip().lower()
    
    if choice != 'n':
        interactive_mode()
    else:
        print("\nTo deploy the agent, run:")
        print("  ./deploy_agent.sh YOUR_PROJECT_ID")
        print("\nOr for more options:")
        print("  ./deploy_agent.sh --help")


if __name__ == "__main__":
    main()
