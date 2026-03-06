# Lab 2 - Tool Callbacks (Validation and Enrichment)

Validate tool arguments and enrich results using before_tool_callback and after_tool_callback.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Add Your API Key

Edit `tool_validator_agent/.env` and add your Google AI Studio API key:

```
GOOGLE_API_KEY="your-api-key"
```

## Run the Agent

```bash
python -m tool_validator_agent.agent
```
