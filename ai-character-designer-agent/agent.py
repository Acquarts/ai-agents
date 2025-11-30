from google.adk.agents import LlmAgent
from google.adk.tools import google_search
from google.adk.tools.agent_tool import AgentTool
import os

MODEL="gemini-2.5-flash"

idea_agent = LlmAgent(
    model=MODEL,
    name="IdeaAgent",
    description="An agent that generates innovative fantasy characters ideas based on user preferences or requests.",
    instruction="You are a creative assistant that generates unique and imaginative fantasy character ideas based on the user's request.",
    tools=[google_search],
    disallow_transfer_to_peers=True,
)

refiner_agent = LlmAgent(
    model=MODEL,
    name="RefinerAgent",
    description="Reviews provided fantasy character ideas to make them more detailed and engaging selecting the best one",
    instruction="Use your tools to review the provided fantasy character ideas. Respond ONLY with the improved and detailed idea.",
    tools=[google_search],
    disallow_transfer_to_peers=True,
)

root_agent = LlmAgent(
    model=MODEL,
    name="CharacterDesignerAgent",
    instruction=f"""You are a Character Designer, coordinating specialist agents.
    Your goal is to provide super awesome fantasy character ideas. For each user request, follow the below instructions:
    1. First, use "{idea_agent}" to brainstorm ideas based on the user's request.
    2. Then, use "{refiner_agent}" to take those ideas to filter them selecting the coolest.
    3. Present the final, refined list to the user.
    Always use the agents in the specified order to ensure high-quality results.
    """,
    tools=[AgentTool(agent=idea_agent), AgentTool(agent=refiner_agent)],
)

# Streamlit UI
import streamlit as st
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
import asyncio
import uuid

# Initialize session service
APP_NAME = "character_designer"
USER_ID = "user_001"

async def initialize_session():
    """Initialize session asynchronously"""
    session_service = InMemorySessionService()
    session_id = str(uuid.uuid4())
    await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=session_id
    )
    return session_service, session_id

if "session_service" not in st.session_state:
    # Run async initialization
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    st.session_state.session_service, st.session_state.session_id = loop.run_until_complete(initialize_session())
    loop.close()

# Create runner
if "runner" not in st.session_state:
    st.session_state.runner = Runner(
        agent=root_agent,
        app_name=APP_NAME,
        session_service=st.session_state.session_service
    )

st.title("🎭 Fantasy Character Designer")
st.write("Generate unique and detailed fantasy character ideas powered by AI agents.")

# API Key input in sidebar
with st.sidebar:
    st.header("About")
    st.markdown("""
    **Fantasy Character Designer** is a multi-agent AI system that creates unique and detailed fantasy character concepts.

    This app uses three specialized AI agents:
    - **IdeaAgent**: Generates creative character ideas
    - **RefinerAgent**: Enhances and polishes the concepts
    - **CharacterDesignerAgent**: Coordinates the workflow

    Powered by Google's Gemini 2.5 Flash and the Agent Development Kit (ADK).
    """)

    st.divider()

    st.header("Configuration")
    api_key_input = st.text_input(
        "Google API Key",
        type="password",
        value="",
        placeholder="Enter your Google API key",
        help="Enter your Google AI API key. Get one at https://aistudio.google.com/app/apikey"
    )

    if api_key_input:
        # Update API key if provided
        os.environ["GOOGLE_API_KEY"] = api_key_input
        st.success("API key set for this session!")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Describe the character you want to create..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Creating your character..."):
            content = types.Content(
                role="user",
                parts=[types.Part(text=prompt)]
            )

            response_text = ""
            for event in st.session_state.runner.run(
                user_id=USER_ID,
                session_id=st.session_state.session_id,
                new_message=content
            ):
                if event.is_final_response():
                    if event.content and event.content.parts:
                        response_text = event.content.parts[0].text
                        break

            st.markdown(response_text)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response_text})

    st.divider()
    st.header("Example Prompts")
    st.markdown("""
    - "Create a mysterious elven rogue with a dark past"
    - "I need a powerful wizard character for D&D"
    - "Design a noble knight with a tragic backstory"
    - "Generate a chaotic villain for a fantasy campaign"
    """)

    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()