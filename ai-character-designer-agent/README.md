# Character Designer Agent

AI agent that generates and refines creative and innovative fantasy character ideas.

## What does it do?

This multi-agent system coordinates a two-tier process to create unique fantasy characters:
- Generates initial character ideas based on your preferences
- Refines and improves the ideas, selecting the most interesting ones
- Delivers detailed and engaging character concepts

## How does it work?

The system uses three specialized agents working in sequence:

1. **IdeaAgent**: Generates innovative fantasy character ideas based on your request
2. **RefinerAgent**: Reviews generated ideas, improves them, and selects the best one
3. **CharacterDesignerAgent** (root): Coordinates the other agents ensuring proper workflow

Each agent has access to Google Search to research and enrich the ideas.

## How to use it?

### Requirements

- Python 3.10 or higher
- Google ADK (Agent Development Kit)
- Model: Gemini 2.5 Flash
- Google AI API Key (get one at [Google AI Studio](https://aistudio.google.com/app/apikey))

### Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up your Google API key:
```bash
# Option 1: Set environment variable
export GOOGLE_API_KEY="your-api-key-here"

# Option 2: Enter it in the Streamlit UI sidebar
```

### Running the App

Start the Streamlit application:
```bash
streamlit run agent.py
```

Then open your browser to `http://localhost:8501` and enter your API key in the sidebar if you haven't set it as an environment variable.

### Example requests

- "I need an elven warrior character with a tragic backstory"
- "Create a villain for a medieval fantasy story"
- "Design a mage with unique time-control abilities"

## Architecture

```
CharacterDesignerAgent (root)
    ├── IdeaAgent
    └── RefinerAgent
```

The root agent coordinates the workflow, ensuring each request flows through idea generation first, then refinement, before delivering the final result.
