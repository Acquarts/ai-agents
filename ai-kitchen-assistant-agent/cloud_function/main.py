"""
Cloud Function for Food Image Analysis
Uses Gemini Vision to analyze food images and return ingredient lists
"""

import functions_framework
import vertexai
from vertexai.generative_models import GenerativeModel, Part
import json
import os
from typing import Dict, Any

# Configuration
PROJECT_ID = os.environ.get('PROJECT_ID', 'your-project-id')
LOCATION = os.environ.get('LOCATION', 'us-central1')
MODEL_NAME = os.environ.get('MODEL_NAME', 'gemini-3-flash-preview')


@functions_framework.http
def analyze_food_image(request) -> tuple:
    """
    Cloud Function to analyze food images using Gemini Vision.
    
    Args:
        request: HTTP request with JSON body containing:
            - image_uri (str): GCS URI (gs://...) or public URL
            - detail_level (str, optional): 'basic' or 'detailed' (default: 'detailed')
    
    Returns:
        tuple: (response_json, status_code, headers)
    """
    
    # CORS preflight request
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }
        return ('', 204, headers)
    
    # Standard CORS headers
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/json; charset=utf-8'
    }
    
    try:
        # Parse request
        request_json = request.get_json(silent=True)
        
        if not request_json:
            return json.dumps({
                'error': 'Invalid JSON in request body',
                'usage': 'POST with JSON: {"image_uri": "gs://bucket/image.jpg"}'
            }), 400, headers
        
        image_uri = request_json.get('image_uri')
        detail_level = request_json.get('detail_level', 'detailed')
        
        if not image_uri:
            return json.dumps({
                'error': 'Missing required parameter: image_uri',
                'usage': 'POST with JSON: {"image_uri": "gs://bucket/image.jpg", "detail_level": "detailed"}'
            }), 400, headers
        
        # Validate URI format
        if not (image_uri.startswith('gs://') or image_uri.startswith('http')):
            return json.dumps({
                'error': 'Invalid image_uri format',
                'message': 'URI must start with gs:// or http(s)://',
                'provided': image_uri
            }), 400, headers
        
        # Initialize Vertex AI
        vertexai.init(project=PROJECT_ID, location=LOCATION)
        
        # Analyze image
        result = _analyze_with_gemini(image_uri, detail_level)
        
        return json.dumps(result, ensure_ascii=False), 200, headers
        
    except Exception as e:
        error_response = {
            'error': 'Internal server error',
            'message': str(e),
            'status': 'failed'
        }
        return json.dumps(error_response), 500, headers


def _analyze_with_gemini(image_uri: str, detail_level: str) -> Dict[str, Any]:
    """
    Analyze image using Gemini Vision model.
    
    Args:
        image_uri: GCS URI or public URL of the image
        detail_level: 'basic' or 'detailed'
    
    Returns:
        Dict containing analysis results
    """
    
    # Initialize model
    model = GenerativeModel(MODEL_NAME)
    
    # Determine MIME type from URI
    mime_type = _get_mime_type(image_uri)
    
    # Load image
    image_part = Part.from_uri(image_uri, mime_type=mime_type)
    
    # Create prompt based on detail level
    if detail_level == 'basic':
        prompt = """Analyze this food image and list all visible ingredients.

Return a simple comma-separated list of ingredients.
Example: tomatoes, pasta, garlic, olive oil, basil"""
    
    else:  # detailed
        prompt = """Analyze this food image in detail and identify all visible ingredients and food items.

For each item, provide:
- Name of the ingredient
- Approximate quantity or state it as "visible"
- State/condition (raw, cooked, fresh, processed, dried, canned, etc.)
- Any notable characteristics

Format your response as a structured list:

INGREDIENTS IDENTIFIED:
- [Ingredient name]: [quantity estimate] - [state/condition]

Example format:
INGREDIENTS IDENTIFIED:
- Tomatoes: 3-4 pieces - fresh, red, ripe
- Pasta: ~200g visible - dry, uncooked, spaghetti
- Garlic: 2-3 cloves - fresh, peeled
- Olive oil: small amount visible - extra virgin

Be thorough and precise. If you're uncertain about something, indicate it."""
    
    # Generate content
    response = model.generate_content([prompt, image_part])
    
    # Parse response
    ingredients_text = response.text.strip()
    
    # Build result
    result = {
        'ingredients': ingredients_text,
        'image_uri': image_uri,
        'detail_level': detail_level,
        'model': MODEL_NAME,
        'status': 'success'
    }
    
    # Try to extract structured data for detailed responses
    if detail_level == 'detailed':
        result['structured_data'] = _parse_detailed_response(ingredients_text)
    
    return result


def _get_mime_type(uri: str) -> str:
    """Determine MIME type from URI extension."""
    uri_lower = uri.lower()
    
    if uri_lower.endswith('.jpg') or uri_lower.endswith('.jpeg'):
        return 'image/jpeg'
    elif uri_lower.endswith('.png'):
        return 'image/png'
    elif uri_lower.endswith('.webp'):
        return 'image/webp'
    elif uri_lower.endswith('.gif'):
        return 'image/gif'
    else:
        # Default to JPEG
        return 'image/jpeg'


def _parse_detailed_response(text: str) -> Dict[str, Any]:
    """
    Attempt to parse detailed response into structured data.
    
    Args:
        text: Raw response text
    
    Returns:
        Dict with parsed ingredient data
    """
    try:
        ingredients = []
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            if line.startswith('-') and ':' in line:
                # Parse line like: "- Tomatoes: 3-4 pieces - fresh, red"
                line = line[1:].strip()  # Remove leading dash
                parts = line.split(':', 1)
                if len(parts) == 2:
                    name = parts[0].strip()
                    details = parts[1].strip()
                    ingredients.append({
                        'name': name,
                        'details': details
                    })
        
        return {
            'count': len(ingredients),
            'items': ingredients
        }
    
    except Exception:
        # If parsing fails, return empty structure
        return {'count': 0, 'items': []}


# Health check endpoint
@functions_framework.http
def health_check(request):
    """Simple health check endpoint."""
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/json'
    }
    
    return json.dumps({
        'status': 'healthy',
        'service': 'food-image-analyzer',
        'version': '1.0.0'
    }), 200, headers
