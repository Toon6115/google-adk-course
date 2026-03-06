# Lab 1 - Function Tools (Weather Agent)

Build an agent with custom Python function tools for weather lookup and temperature conversion.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Add Your API Key

Edit `weather_agent/.env` and add your Google AI Studio API key:

```
GOOGLE_API_KEY="your-api-key"
```

## Run the Agent

```bash
adk web weather_agent
```

Or use the CLI:

```bash
adk run weather_agent
```
