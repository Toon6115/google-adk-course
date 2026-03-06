# Lab 7 - MCP Tool Integration (Filesystem)

Build an agent that connects to an MCP filesystem server for safe, read-only file access.

## Prerequisites

- Node.js and npx installed (for the MCP server)

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Add Your API Key

Edit `file_assistant/.env` and add your Google AI Studio API key:

```
GOOGLE_API_KEY="your-api-key"
```

## Run the Agent

**Important** - This agent must be run with `adk run` or `adk web` (not `python agent.py`) because the MCP toolset requires async initialization that the ADK CLI handles automatically.

```bash
adk web file_assistant
```

Or use the CLI:

```bash
adk run file_assistant
```
