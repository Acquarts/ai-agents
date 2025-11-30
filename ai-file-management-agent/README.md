# 📂 File Management Agent

Conversational Python agent that enables file system interaction through natural language. Uses the OpenAI API to process commands and execute file reading, writing, and editing operations.

## Features

The agent provides three main tools:

- **list_files_in_dir**: Lists files and folders in a directory
- **read_file**: Reads file contents
- **edit_file**: Edits existing files or creates new ones

## How it works

1. User writes commands in natural language (Spanish)
2. The OpenAI model interprets the intent and decides which tool to use
3. The agent executes the corresponding function on the file system
4. Results are sent back to the model to generate a response to the user

The agent maintains a conversation history, enabling contextual interactions and chained operations.

## Installation

### Prerequisites
- Python 3.7 or higher
- An OpenAI API key

### Installation steps

1. Clone or download this repository

2. Create a virtual environment (recommended):
```bash
python -m venv env
```

3. Activate the virtual environment:
   - Windows: `env\Scripts\activate`
   - Linux/Mac: `source env/bin/activate`

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Create a `.env` file in the project root with your API key:
```
OPENAI_API_KEY=your_api_key_here
```

## Usage

Run the agent:
```bash
python main.py
```

Example commands you can use:
- "List files in the current directory"
- "Read the config.json file"
- "Create a file called hello.txt with the text 'Hello world'"
- "Edit the test.py file and replace X with Y"

To exit, type: `salir`, `exit`, `quit`, or `Taluego!`

## Project structure

```
list_read_edit_files/
├── agent.py          # Agent class with tool definitions
├── main.py           # Main interaction loop
├── requirements.txt  # Project dependencies
├── .env             # Environment variables (API keys)
└── README.md        # This file
```

## Dependencies

- `openai==2.8.1` - OpenAI API client
- `python-dotenv==1.2.1` - Environment variable management
