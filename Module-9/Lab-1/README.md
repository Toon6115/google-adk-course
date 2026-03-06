# Lab 1 - Session-Based Memory

Demonstrate how sessions maintain conversation history within a session but not across sessions.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Add Your API Key

Edit `session_agent/.env` and add your Google AI Studio API key:

```
GOOGLE_API_KEY="your-api-key"
```

## Run the Agent

```bash
python -m session_agent.agent
```
