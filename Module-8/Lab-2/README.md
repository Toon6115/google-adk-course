# Lab 2 - Built-in Google Search Tool

Build an agent that uses the built-in Google Search tool.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Add Your API Key

Edit `search_agent/.env` and add your Google AI Studio API key:

```
GOOGLE_API_KEY="your-api-key"
```

## Run the Agent

```bash
adk web search_agent
```

Or use the CLI:

```bash
adk run search_agent
```
