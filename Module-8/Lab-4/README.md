# Lab 4 - OpenAPI/REST API Integration

Build an agent that auto-generates tools from an OpenAPI specification.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Add Your API Key

Edit `api_agent/.env` and add your Google AI Studio API key:

```
GOOGLE_API_KEY="your-api-key"
```

## Run the Agent

```bash
adk web api_agent
```

Or use the CLI:

```bash
adk run api_agent
```
