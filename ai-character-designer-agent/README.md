# 🐱‍🚀 Character Designer Agent

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
- Streamlit
- Google AI API Key (get one at [Google AI Studio](https://aistudio.google.com/app/apikey))

### Installation

1. Clone or download this project

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the App

1. Start the Streamlit application:
```bash
streamlit run agent.py
```

2. Open your browser to `http://localhost:8501`

3. Enter your Google API Key in the sidebar Configuration section

4. Start creating fantasy characters!

### Using the Interface

- **API Key**: Enter your Google AI API key in the sidebar (required for first use in each session)
- **Chat Input**: Describe the character you want to create in the text box at the bottom
- **Clear Chat**: Click the "Clear Chat" button in the sidebar to start a new conversation
- **Example Prompts**: Check the sidebar for inspiration

### Example Prompts

- "Create a mysterious elven rogue with a dark past"
- "I need a powerful wizard character for D&D"
- "Design a noble knight with a tragic backstory"
- "Generate a chaotic villain for a fantasy campaign"
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
