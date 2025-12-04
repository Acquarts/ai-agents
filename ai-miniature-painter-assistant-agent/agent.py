from google.adk.agents import LlmAgent
from google.adk.tools import google_search
from google.adk.tools.agent_tool import AgentTool
import os

MODEL = "gemini-2.5-flash"

# Agent 1: Color Scheme Suggester
color_scheme_agent = LlmAgent(
    model=MODEL,
    name="ColorSchemeAgent",
    description="Analyzes unpainted miniatures and suggests creative color schemes based on the miniature type, theme, and painting trends.",
    instruction="""You are a miniature painting color expert. When you receive an image of an unpainted miniature:
    1. Analyze the miniature type (fantasy, sci-fi, historical, etc.)
    2. Identify key elements (armor, clothing, skin, weapons, accessories)
    3. Suggest 3 different color schemes with specific paint recommendations
    4. Use Google Search to find trending color schemes for similar miniatures
    5. Provide hex color codes and paint brand recommendations (Citadel, Vallejo, Army Painter)

    Format your response as:
    **Color Scheme 1: [Name]**
    - Element 1: [Color] ([Hex]) - [Paint Brand & Name]
    - Element 2: [Color] ([Hex]) - [Paint Brand & Name]
    ...

    **Color Scheme 2: [Name]**
    ...

    **Color Scheme 3: [Name]**
    ...
    """,
    tools=[google_search],
    disallow_transfer_to_peers=True,
)

# Agent 2: Painting Time and Budget Estimator
estimator_agent = LlmAgent(
    model=MODEL,
    name="EstimatorAgent",
    description="Calculates painting time and paint budget based on miniature complexity and chosen color scheme.",
    instruction="""You are a miniature painting estimator. Based on the miniature image and selected color scheme:
    1. Estimate painting time for different skill levels (Beginner, Intermediate, Advanced)
    2. Calculate paint budget including:
       - Base paints needed
       - Shades/washes
       - Highlights
       - Special effects (metallics, etc.)
    3. Consider miniature size (28mm, 32mm, 75mm, etc.) and detail level
    4. Use Google Search to verify current paint prices

    Format your response as:
    **Time Estimation:**
    - Beginner: X-Y hours
    - Intermediate: X-Y hours
    - Advanced: X-Y hours

    **Paint Budget:**
    - Base Paints: $X (list of paints)
    - Shades/Washes: $X (list)
    - Highlights: $X (list)
    - Special Effects: $X (list)
    - **Total Estimated Cost: $X-Y**

    **Notes:**
    - Include any special tools or materials needed
    - Mention difficulty level and special techniques required
    """,
    tools=[google_search],
    disallow_transfer_to_peers=True,
)

# Agent 3: Image Painter (Conceptual - Gemini will describe the painted version)
image_painter_agent = LlmAgent(
    model=MODEL,
    name="ImagePainterAgent",
    description="Creates a detailed description of how the miniature would look painted with the selected color scheme.",
    instruction="""You are a miniature painting visualization expert. Using the unpainted miniature image and the selected color scheme:
    1. Create a highly detailed description of how the painted miniature would look
    2. Describe each painted element in vivid detail
    3. Mention painting techniques used (layering, dry brushing, washing, highlighting, etc.)
    4. Describe the overall visual impact and finish quality
    5. Suggest photography/lighting tips for the finished piece

    IMPORTANT: Since you cannot actually generate images, provide such a detailed description that the user can visualize the painted miniature clearly. Use professional miniature painting terminology.

    Format your response as:
    **Painted Miniature Visualization:**

    [Extremely detailed description of the painted miniature, section by section]

    **Painting Techniques Used:**
    - Technique 1: [Description]
    - Technique 2: [Description]
    ...

    **Final Result:**
    [Overall impression and recommendations]

    **Photography Tips:**
    - [Lighting suggestions]
    - [Background recommendations]
    - [Angle suggestions]
    """,
    tools=[google_search],
    disallow_transfer_to_peers=True,
)

# Root Agent: Miniature Painter Coordinator
root_agent = LlmAgent(
    model=MODEL,
    name="MiniaturePainterAgent",
    instruction=f"""You are a Miniature Painting Assistant, coordinating specialized agents to help users paint their miniatures.

    When a user uploads an image of an unpainted miniature, follow these steps:

    1. First, use "{color_scheme_agent}" to analyze the miniature and suggest 3 color schemes
    2. Then, use "{estimator_agent}" to calculate painting time and budget for the suggested schemes
    3. Finally, use "{image_painter_agent}" to create a detailed visualization of how the painted miniature would look
    4. Present all information in a clear, organized manner

    Always use the agents in this specific order to ensure comprehensive results.

    Be friendly, encouraging, and provide helpful tips for miniature painters of all skill levels.
    """,
    tools=[
        AgentTool(agent=color_scheme_agent),
        AgentTool(agent=estimator_agent),
        AgentTool(agent=image_painter_agent)
    ],
)

#_____________________________________________________________________________________________

# Streamlit UI
#_____________________________________________________________________________________________

import streamlit as st
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from google import genai as google_genai
import asyncio
import uuid
from PIL import Image
import io
# Initialize session service
APP_NAME = "miniature_painter"
USER_ID = "user_001"

def generate_painted_image(original_image_bytes, color_scheme_description, miniature_description, api_key):
    """Generate a painted miniature image using Gemini 2.5 Flash Image with the original miniature as reference"""
    try:
        client = google_genai.Client(api_key=api_key)

        # Create detailed prompt for image transformation
        prompt = f"""Transform this unpainted miniature into a professionally painted version with this exact color scheme:
{color_scheme_description}

Apply these painting techniques to the EXACT miniature shown in the image:
- Professional basecoat with the specified colors
- Smooth color transitions and gradients
- Expert-level highlighting on raised areas
- Realistic shading in recesses
- Metallic effects where specified in the color scheme
- Weathering and texture effects as appropriate
- Maintain the exact pose, details, and structure of this specific miniature

IMPORTANT: Paint THIS specific miniature, keeping its exact shape, pose, details, and features. Only change the colors according to the scheme.

Style: photorealistic tabletop miniature painting, professional quality, studio lighting"""

        # Create image part from bytes
        image_part = types.Part(
            inline_data=types.Blob(
                mime_type="image/png",
                data=original_image_bytes
            )
        )

        # Build content with BOTH the image and the prompt
        contents = [
            types.Content(
                role="user",
                parts=[
                    image_part,
                    types.Part.from_text(text=prompt)
                ],
            ),
        ]

        generate_content_config = types.GenerateContentConfig(
            response_modalities=["IMAGE", "TEXT"],
        )

        # Generate the painted version
        for chunk in client.models.generate_content_stream(
            model="gemini-2.5-flash-image",
            contents=contents,
            config=generate_content_config,
        ):
            if (
                chunk.candidates is None
                or chunk.candidates[0].content is None
                or chunk.candidates[0].content.parts is None
            ):
                continue

            if chunk.candidates[0].content.parts[0].inline_data and chunk.candidates[0].content.parts[0].inline_data.data:
                inline_data = chunk.candidates[0].content.parts[0].inline_data
                return inline_data.data

        return None

    except Exception as e:
        st.error(f"Error generating painted image: {str(e)}")
        return None

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

st.title("🎨 Miniature Painter AI Assistant")
st.write("Upload your unpainted miniature and get color schemes, time estimates, and budget calculations!")

# API Key input in sidebar
with st.sidebar:
    st.header("About")
    st.markdown("""
    **Miniature Painter AI** is a multi-agent system that helps you plan your miniature painting projects.

    This app uses three specialized AI agents:
    - **ColorSchemeAgent**: Suggests creative color schemes
    - **EstimatorAgent**: Calculates time and budget
    - **ImagePainterAgent**: Visualizes the painted result
    - **MiniaturePainterAgent**: Coordinates the workflow

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

    st.divider()

    st.header("Instructions")
    st.markdown("""
    1. Enter your Google API Key above
    2. Upload an image of your unpainted miniature
    3. Click "Analyze Miniature" to get:
       - Color scheme suggestions
       - Time estimation
       - Budget calculation
       - Painted visualization
    """)

# Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = []

if "uploaded_image" not in st.session_state:
    st.session_state.uploaded_image = None

# Image upload section
st.header("Upload Miniature Image")
uploaded_file = st.file_uploader(
    "Choose an image of your unpainted miniature",
    type=["jpg", "jpeg", "png", "webp"],
    help="Upload a clear photo of your unpainted miniature"
)

if uploaded_file is not None:
    # Display uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Miniature", use_container_width=True)
    st.session_state.uploaded_image = uploaded_file

    # Convert image to bytes for API and store in session state
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format=image.format if image.format else 'PNG')
    img_byte_arr = img_byte_arr.getvalue()
    st.session_state.miniature_image_bytes = img_byte_arr

    # Analyze button
    if st.button("🎨 Analyze Miniature", type="primary"):
        if not os.environ.get("GOOGLE_API_KEY"):
            st.error("Please enter your Google API Key in the sidebar first!")
        else:
            with st.spinner("Analyzing your miniature... This may take a moment."):
                # Create content with image
                content = types.Content(
                    role="user",
                    parts=[
                        types.Part(
                            inline_data=types.Blob(
                                mime_type=f"image/{image.format.lower() if image.format else 'png'}",
                                data=img_byte_arr
                            )
                        ),
                        types.Part(
                            text="Please analyze this unpainted miniature and provide color schemes, time estimate, budget, and a painted visualization."
                        )
                    ]
                )

                response_text = ""
                try:
                    for event in st.session_state.runner.run(
                        user_id=USER_ID,
                        session_id=st.session_state.session_id,
                        new_message=content
                    ):
                        if event.is_final_response():
                            if event.content and event.content.parts:
                                response_text = event.content.parts[0].text
                                break

                    # Display response
                    st.markdown("---")
                    st.header("Analysis Results")
                    st.markdown(response_text)

                    # Store analysis for image generation
                    st.session_state.last_analysis = response_text
                    st.session_state.miniature_type = "fantasy warrior"  # This should be extracted from Gemini response

                    # Save to chat history
                    st.session_state.messages.append({
                        "role": "user",
                        "content": "Uploaded miniature image",
                        "image": uploaded_file
                    })
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response_text
                    })

                except Exception as e:
                    st.error(f"Error analyzing miniature: {str(e)}")
                    st.info("Make sure your Google API Key is valid and has access to Gemini models.")

    # Generate painted renders section
    if "last_analysis" in st.session_state and st.session_state.last_analysis:
        st.markdown("---")
        st.header("🖼️ Generate Painted Renders")
        st.write("Generate AI renders of your miniature with the suggested color schemes!")

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("🎨 Generate Scheme 1", key="gen1"):
                if "miniature_image_bytes" not in st.session_state:
                    st.error("Please upload an image first!")
                else:
                    with st.spinner("Generating painted render... This may take 30-60 seconds..."):
                        scheme_desc = "Color Scheme 1 from analysis"  # Should extract actual scheme
                        painted_img = generate_painted_image(
                            st.session_state.miniature_image_bytes,
                            scheme_desc,
                            st.session_state.get("miniature_type", "miniature"),
                            os.environ.get("GOOGLE_API_KEY")
                        )
                        if painted_img:
                            st.image(painted_img, caption="Painted Render - Scheme 1", use_container_width=True)
                            st.success("✅ Render generated successfully!")

        with col2:
            if st.button("🎨 Generate Scheme 2", key="gen2"):
                if "miniature_image_bytes" not in st.session_state:
                    st.error("Please upload an image first!")
                else:
                    with st.spinner("Generating painted render... This may take 30-60 seconds..."):
                        scheme_desc = "Color Scheme 2 from analysis"
                        painted_img = generate_painted_image(
                            st.session_state.miniature_image_bytes,
                            scheme_desc,
                            st.session_state.get("miniature_type", "miniature"),
                            os.environ.get("GOOGLE_API_KEY")
                        )
                        if painted_img:
                            st.image(painted_img, caption="Painted Render - Scheme 2", use_container_width=True)
                            st.success("✅ Render generated successfully!")

        with col3:
            if st.button("🎨 Generate Scheme 3", key="gen3"):
                if "miniature_image_bytes" not in st.session_state:
                    st.error("Please upload an image first!")
                else:
                    with st.spinner("Generating painted render... This may take 30-60 seconds..."):
                        scheme_desc = "Color Scheme 3 from analysis"
                        painted_img = generate_painted_image(
                            st.session_state.miniature_image_bytes,
                            scheme_desc,
                            st.session_state.get("miniature_type", "miniature"),
                            os.environ.get("GOOGLE_API_KEY")
                        )
                        if painted_img:
                            st.image(painted_img, caption="Painted Render - Scheme 3", use_container_width=True)
                            st.success("✅ Render generated successfully!")

# Display chat history
if st.session_state.messages:
    st.markdown("---")
    st.header("History")
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            if "image" in message:
                img = Image.open(message["image"])
                st.image(img, width=200)
            st.markdown(message["content"])

# Clear history button
if st.session_state.messages:
    if st.button("Clear History"):
        st.session_state.messages = []
        st.session_state.uploaded_image = None
        st.rerun()

# Tips section
with st.expander("💡 Tips for Best Results"):
    st.markdown("""
    **Photography Tips:**
    - Use good lighting (natural light is best)
    - Take photos against a neutral background
    - Ensure the miniature is in focus
    - Include the whole miniature in frame
    - Take photos from multiple angles if needed

    **Getting Started:**
    - Clean your miniature before photographing
    - Remove any mold lines for better analysis
    - Prime the miniature if possible (grey or white primer shows detail better)

    **About the Analysis:**
    - Color schemes are based on the miniature type and current trends
    - Time estimates vary by skill level
    - Budget includes essential paints only (brushes and primers not included)
    - Prices are approximate and may vary by region
    """)