"""
Configuration file for Recipe AI Streamlit App
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Google Cloud Project Configuration
PROJECT_ID = os.getenv('PROJECT_ID', 'your-project-id')
REGION = os.getenv('REGION', 'us-central1')
LOCATION = os.getenv('LOCATION', 'us-central1')

# Cloud Storage Configuration
BUCKET_NAME = os.getenv('BUCKET_NAME', f'{PROJECT_ID}-recipe-images')

# Vertex AI Agent Configuration
AGENT_ID = os.getenv('AGENT_ID', '')  # Will be set after agent deployment

# Model Configuration
MODEL_NAME = os.getenv('MODEL_NAME', 'gemini-3-flash-preview')

# App Configuration
APP_TITLE = "Recipe AI Assistant"
APP_ICON = "🍳"
DEFAULT_CUISINE = "Italian"

# Supported cuisines
CUISINES = [
    "Italian",
    "Mexican", 
    "Thai",
    "Japanese",
    "Chinese",
    "French",
    "Spanish",
    "Indian",
    "Greek",
    "Vietnamese",
    "Korean",
    "Lebanese",
    "Brazilian",
    "Moroccan",
    "Turkish",
    "American",
    "Mediterranean",
    "Caribbean",
]

# Image settings
MAX_IMAGE_SIZE_MB = 10
ALLOWED_IMAGE_TYPES = ['jpg', 'jpeg', 'png', 'webp']

# Feature flags
ENABLE_IMAGE_ANALYSIS = True
ENABLE_AGENT_MODE = True  # Set to False to use direct Gemini calls
DEBUG_MODE = os.getenv('DEBUG_MODE', 'false').lower() == 'true'

# Validate configuration
def validate_config():
    """Validate that required configuration is set"""
    errors = []
    
    if PROJECT_ID == 'your-project-id':
        errors.append("PROJECT_ID not set in environment variables")
    
    if ENABLE_AGENT_MODE and not AGENT_ID:
        errors.append("AGENT_ID not set but ENABLE_AGENT_MODE is True")
    
    return errors


if __name__ == "__main__":
    # Test configuration
    print("Configuration:")
    print(f"  PROJECT_ID: {PROJECT_ID}")
    print(f"  REGION: {REGION}")
    print(f"  BUCKET_NAME: {BUCKET_NAME}")
    print(f"  AGENT_ID: {AGENT_ID or 'Not set'}")
    print(f"  MODEL_NAME: {MODEL_NAME}")
    print(f"  DEBUG_MODE: {DEBUG_MODE}")
    
    errors = validate_config()
    if errors:
        print("\n⚠️  Configuration Errors:")
        for error in errors:
            print(f"  - {error}")
    else:
        print("\n✅ Configuration valid!")
