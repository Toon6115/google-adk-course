# Lab 5 - LangChain Tool Integration (Wikipedia)

Build a research agent that wraps LangChain's Wikipedia tool using LangchainTool.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Add Your API Key

Edit `research_agent/.env` and add your Google AI Studio API key:

```
GOOGLE_API_KEY="your-api-key"
```

## Run the Agent

```bash
adk web research_agent
```

Or use the CLI:

```bash
adk run research_agent
```
