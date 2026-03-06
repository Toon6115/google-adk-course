# Lab 2 - Session State Management

Save and retrieve user preferences using session state with ToolContext.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Add Your API Key

Edit `preferences_agent/.env` and add your Google AI Studio API key:

```
GOOGLE_API_KEY="your-api-key"
```

## Run the Agent

```bash
python -m preferences_agent.agent
```
