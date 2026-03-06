# Lab 1 - Creating Your First Agent (Code-Based)

Build a basic ADK agent using Python code.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Add Your API Key

Edit `hello_agent/.env` and add your Google AI Studio API key:

```
GOOGLE_GENAI_USE_VERTEXAI=0
GOOGLE_API_KEY="your-api-key"
```

## Run the Agent

```bash
adk web hello_agent
```

Or use the CLI:

```bash
adk run hello_agent
```