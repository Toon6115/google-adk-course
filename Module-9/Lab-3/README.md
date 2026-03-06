# Lab 3 - Long-Term Memory (Cross-Session Recall)

Share information across sessions using InMemoryMemoryService and the load_memory tool.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Add Your API Key

Edit `memory_agent/.env` and add your Google AI Studio API key:

```
GOOGLE_API_KEY="your-api-key"
```

## Run the Agent

```bash
python -m memory_agent.agent
```
