"""
Recipe Multi-Agent - Streamlit UI
Upload food images and get recipe recommendations
"""

import streamlit as st
import vertexai
from vertexai.generative_models import GenerativeModel, Part
from google.cloud import storage
from google.cloud import aiplatform
import uuid
import os
from datetime import datetime
import io
from PIL import Image
import json


PROJECT_ID= "gen-lang-client-0495395701"       # ← Mismo
REGION= "us-central1"               # ← Mismo
LOCATION= "us-central1"              # ← Mismo
BUCKET_NAME= "adribucket2"
AGENT_ID= "5676977545812115456"                  # Diferente (opcional)
MODEL_NAME= "gemini-2.0-flash"   # ← Modelo estable
DEBUG_MODE= False




# Import config
from config import (
    PROJECT_ID,
    REGION,
    BUCKET_NAME,
    AGENT_ID
)

# Page config
st.set_page_config(
    page_title="Recipe AI Assistant",
    page_icon="🍳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    /* SIDEBAR - FONDO CLARO, TEXTO NEGRO (SIMPLE) */
    [data-testid="stSidebar"] {
        background-color: #f0f2f6 !important;
    }
    [data-testid="stSidebar"] * {
        color: #1a1a1a !important;
    }
    
    /* SELECTBOX BLANCO */
    [data-testid="stSidebar"] .stSelectbox > div > div {
        background-color: white !important;
        color: #1a1a1a !important;
    }
    
    /* Contenido principal */
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #FF6B6B;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #FF6B6B;
        color: white;
        font-weight: bold;
        padding: 0.75rem;
        border-radius: 8px;
    }
    .stButton>button:hover {
        background-color: #ff5252;
    }
</style>
""", unsafe_allow_html=True)


# Initialize session state
if 'ingredients_detected' not in st.session_state:
    st.session_state.ingredients_detected = None
if 'recipes_generated' not in st.session_state:
    st.session_state.recipes_generated = None
if 'image_uploaded' not in st.session_state:
    st.session_state.image_uploaded = False


def initialize_services():
    """Initialize Google Cloud services"""
    try:
        vertexai.init(project=PROJECT_ID, location=REGION)
        return True
    except Exception as e:
        st.error(f"Failed to initialize services: {e}")
        return False


def upload_image_to_gcs(image_file):
    """Upload image to Google Cloud Storage"""
    try:
        # Create unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_extension = image_file.name.split('.')[-1]
        filename = f"food_images/{timestamp}_{uuid.uuid4()}.{file_extension}"
        
        # Initialize storage client
        try:
            storage_client = storage.Client(project=PROJECT_ID)
        except Exception as e:
            st.error(f"Failed to initialize Storage client: {e}")
            return None, None
        
        try:
            bucket = storage_client.bucket(BUCKET_NAME)
        except Exception as e:
            st.error(f"Failed to access bucket {BUCKET_NAME}: {e}")
            return None, None
        
        blob = bucket.blob(filename)
        
        # Upload file
        image_file.seek(0)
        try:
            blob.upload_from_file(image_file, content_type=image_file.type)
        except Exception as e:
            st.error(f"Failed to upload file: {e}")
            return None, None
        
        # Make public (optional - remove if you want private)
        try:
            blob.make_public()
        except Exception as e:
            st.warning(f"Could not make blob public (continuing anyway): {e}")
        
        # Return GCS URI
        gs_uri = f"gs://{BUCKET_NAME}/{filename}"
        public_url = blob.public_url
        
        return gs_uri, public_url
        
    except Exception as e:
        st.error(f"Failed to upload image: {e}")
        st.exception(e)
        return None, None


def analyze_food_image(image_file):
    """Analyze food image using Gemini Vision"""
    try:
        with st.spinner("🔍 Analyzing your ingredients..."):
            # Upload to GCS
            st.info("📤 Uploading image to Cloud Storage...")
            gs_uri, public_url = upload_image_to_gcs(image_file)
            
            if not gs_uri:
                st.error("❌ Failed to upload image to Cloud Storage")
                return None
            
            st.success(f"✅ Image uploaded: {gs_uri}")
            
            # Initialize Gemini model (use 2.0-flash for vision - stable and available)
            st.info("🤖 Initializing Gemini Vision model...")
            model = GenerativeModel("gemini-2.0-flash")
            
            # Load image - fix mime type
            mime_type = image_file.type
            if mime_type == "image/jpg":
                mime_type = "image/jpeg"
            
            st.info(f"📸 Loading image with mime type: {mime_type}")
            image_part = Part.from_uri(gs_uri, mime_type=mime_type)
            
            # Create prompt
            prompt = """Analyze this food image in detail and identify all visible ingredients.

For each ingredient, provide:
- Name of the ingredient
- Approximate quantity or "visible"
- State (fresh, cooked, raw, processed, etc.)

Format your response as a clear list:

INGREDIENTS IDENTIFIED:
- [Ingredient name]: [quantity] - [state]

Example:
INGREDIENTS IDENTIFIED:
- Tomatoes: 3-4 pieces - fresh, ripe
- Pasta: ~200g - dry, uncooked
- Garlic: 2-3 cloves - fresh, peeled

Be thorough and precise."""

            
            # Generate response
            st.info("🧠 Analyzing ingredients with AI...")
            response = model.generate_content([prompt, image_part])
            
            if response and response.text:
                st.success("✅ Analysis complete!")
                return response.text.strip()
            else:
                st.error("❌ Gemini returned empty response")
                return None
            
    except Exception as e:
        st.error(f"❌ Error analyzing image: {str(e)}")
        st.exception(e)  # Show full stack trace for debugging
        return None


def generate_recipes_with_agent(ingredients_text, cuisine):
    """Generate recipes using Vertex AI Agent"""
    from config import AGENT_ID, PROJECT_ID, REGION

    try:
        with st.spinner(f"👨‍🍳 Creating {cuisine} recipes for you..."):

            if AGENT_ID and AGENT_ID.strip():
                st.info("🤖 Connecting to Vertex AI Agent...")

                try:
                    import vertexai
                    from vertexai import agent_engines

                    # Initialize Vertex AI
                    vertexai.init(project=PROJECT_ID, location=REGION)

                    # Get the deployed agent
                    agent_resource_name = f"projects/562289298058/locations/{REGION}/reasoningEngines/{AGENT_ID}"
                    remote_app = agent_engines.get(agent_resource_name)
                    st.success("✅ Connected to agent!")

                    # Create query - direct recipe generation request
                    query_input = f"""SKIP GREETING. Generate recipes immediately.

VALIDATED INGREDIENTS (already analyzed):
{ingredients_text}

TARGET CUISINE: {cuisine}

TASK: Generate 3-5 authentic {cuisine} recipes using these ingredients NOW.
Do NOT ask for more information. Do NOT ask about image URLs.
The ingredients above are TEXT, not URLs - proceed directly to recipe generation.

For each recipe provide:
- Recipe name and regional origin
- Complete ingredients list with amounts
- Step-by-step cooking instructions
- Prep time, cook time, difficulty
- Chef's tips"""

                    st.info("🤖 Agent is generating recipes...")

                    response_text = ""
                    import asyncio

                    # Use async_stream_query (the correct async method)
                    async def get_agent_response():
                        result = ""
                        events = 0
                        async for event in remote_app.async_stream_query(
                            user_id="streamlit_user",
                            message=query_input,
                        ):
                            events += 1
                            text = extract_text_from_event(event)
                            if text:
                                result += text
                        return result, events

                    # Run async function
                    response_text, event_count = asyncio.run(get_agent_response())
                    st.write(f"📊 Events received: {event_count}")

                    if response_text:
                        st.success("✅ Recipes generated by multi-agent system!")
                        return response_text
                    else:
                        st.warning("⚠️ Agent returned empty response, using fallback")
                        return generate_recipes_direct(ingredients_text, cuisine)

                except ImportError as import_error:
                    st.error(f"❌ Library not available: {str(import_error)}")
                    st.info("📝 Using direct Gemini instead...")
                    return generate_recipes_direct(ingredients_text, cuisine)
                except Exception as agent_error:
                    st.error(f"❌ Agent error: {str(agent_error)}")
                    st.exception(agent_error)
                    st.info("📝 Falling back to direct Gemini...")
                    return generate_recipes_direct(ingredients_text, cuisine)
            else:
                st.info("ℹ️ No AGENT_ID configured - using direct Gemini")
                return generate_recipes_direct(ingredients_text, cuisine)

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        st.exception(e)
        return None


def extract_text_from_event(event):
    """Extract text content from various event formats"""
    if event is None:
        return ""

    # If it's a string, return directly
    if isinstance(event, str):
        return event

    # If it's a dict, try various keys
    if isinstance(event, dict):
        # Try 'content' key (Gemini format)
        if 'content' in event:
            content = event['content']
            if isinstance(content, str):
                return content
            if isinstance(content, dict):
                # Try parts array
                if 'parts' in content:
                    texts = []
                    for part in content['parts']:
                        if isinstance(part, dict) and 'text' in part:
                            texts.append(part['text'])
                        elif isinstance(part, str):
                            texts.append(part)
                    return ''.join(texts)
                # Try text directly
                if 'text' in content:
                    return content['text']

        # Try 'output' key
        if 'output' in event:
            output = event['output']
            if isinstance(output, str):
                return output
            return str(output)

        # Try 'text' key directly
        if 'text' in event:
            return event['text']

        # Try 'message' key
        if 'message' in event:
            msg = event['message']
            if isinstance(msg, str):
                return msg
            if isinstance(msg, dict) and 'text' in msg:
                return msg['text']

        # Try 'response' key
        if 'response' in event:
            return str(event['response'])

    # If it has a text attribute
    if hasattr(event, 'text'):
        return event.text

    # If it has content attribute
    if hasattr(event, 'content'):
        return str(event.content)

    return ""


def generate_recipes_direct(ingredients_text, cuisine):
    """Fallback: Generate recipes using direct Gemini call"""
    try:
        st.info("🤖 Using Gemini model directly...")

        # Use direct Gemini call (gemini-2.0-flash is stable and available)
        model = GenerativeModel("gemini-2.0-flash")
        
        agent_prompt = f"""You are an expert chef specializing in {cuisine} cuisine.

INGREDIENTS AVAILABLE:
{ingredients_text}

Generate 3-5 authentic {cuisine} recipes using these ingredients.

For each recipe, provide:

**[Recipe Name]**
Origin: [Region/City]
Difficulty: [Easy/Medium/Hard]
Prep Time: [X minutes]
Cook Time: [X minutes]
Servings: [number]

**Ingredients:**
- [Each ingredient with amount]

**Instructions:**
1. [Detailed step]
2. [Continue...]

**Chef's Tips:**
- [Helpful cooking tip]

---

Make recipes authentic and delicious!"""
        
        response = model.generate_content(agent_prompt)
        
        if response and response.text:
            return response.text
        else:
            st.error("Empty response from Gemini")
            return None
        
    except Exception as e:
        st.error(f"❌ Error in direct generation: {str(e)}")
        st.exception(e)
        return None


def main():
    """Main Streamlit application"""
    
    # Header
    st.markdown('<div class="main-header">🍳 Recipe AI Assistant</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Upload a photo of your ingredients and discover delicious recipes!</div>', unsafe_allow_html=True)
    
    # Initialize services
    if not initialize_services():
        st.stop()
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")
        
        cuisine = st.selectbox(
            "Choose cuisine style:",
            [
                "Italian", "Mexican", "Thai", "Japanese", "Chinese",
                "French", "Spanish", "Indian", "Greek", "Vietnamese",
                "Korean", "Lebanese", "Brazilian", "Moroccan", "Turkish"
            ],
            index=0
        )
        
        st.divider()
        
        st.header("ℹ️ How it works")
        st.markdown("""
        1. **Upload** a photo of your ingredients
        2. **AI analyzes** and identifies them
        3. **Get** authentic recipes instantly!
        """)
        
        st.divider()
        
        if st.button("🔄 Reset"):
            st.session_state.ingredients_detected = None
            st.session_state.recipes_generated = None
            st.session_state.image_uploaded = False
            st.rerun()
    
    # Main content
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📸 Upload Your Ingredients")
        
        uploaded_file = st.file_uploader(
            "Choose an image...",
            type=['jpg', 'jpeg', 'png', 'webp'],
            help="Upload a clear photo of your food ingredients"
        )
        
        if uploaded_file:
            # Display uploaded image
            image = Image.open(uploaded_file)
            st.image(image, caption="Your ingredients", use_column_width=True)
            
            # Analyze button
            if st.button("🔍 Analyze Ingredients", type="primary"):
                ingredients = analyze_food_image(uploaded_file)
                
                if ingredients:
                    st.session_state.ingredients_detected = ingredients
                    st.session_state.image_uploaded = True
                    st.success("✅ Ingredients identified!")
                    st.rerun()
    
    with col2:
        st.header("📝 Detected Ingredients")
        
        if st.session_state.ingredients_detected:
            # Usar un container con fondo para mejor visualización
            with st.container():
                st.markdown(
                    f"""
                    <div style='background-color: #e3f2fd; padding: 1rem; border-radius: 8px; margin: 1rem 0;'>
                        <div style='color: #1a1a1a; white-space: pre-wrap;'>{st.session_state.ingredients_detected}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            
            # Generate recipes button
            if st.button("👨‍🍳 Generate Recipes", type="primary"):
                recipes = generate_recipes_with_agent(
                    st.session_state.ingredients_detected,
                    cuisine
                )
                
                if recipes:
                    st.session_state.recipes_generated = recipes
                    st.success("✅ Recipes ready!")
                    st.rerun()
        else:
            st.info("👆 Upload an image to get started!")
    
    # Recipes section
    if st.session_state.recipes_generated:
        st.divider()
        st.header(f"🍽️ {cuisine} Recipes for You")
        
        # Mostrar recetas con formato legible
        with st.container():
            st.markdown(
                f"""
                <div style='background-color: #f8f9fa; padding: 1.5rem; border-radius: 10px; margin: 1rem 0; border-left: 4px solid #FF6B6B;'>
                    <div style='color: #1a1a1a; white-space: pre-wrap;'>{st.session_state.recipes_generated}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        # Download button
        st.download_button(
            label="📥 Download Recipes",
            data=st.session_state.recipes_generated,
            file_name=f"recipes_{cuisine.lower()}_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain"
        )
    
    # Footer
    st.divider()
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 2rem;">
        Made with ❤️ using Google Cloud AI | Powered by Gemini & Vertex AI
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()