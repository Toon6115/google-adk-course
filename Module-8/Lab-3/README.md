# Lab 3 - Code Execution Tool

Build an agent that can write and execute Python code using the built-in code executor.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Add Your API Key

Edit `code_exec_agent/.env` and add your Google AI Studio API key:

```
GOOGLE_API_KEY="your-api-key"
```

## Run the Agent

```bash
adk web code_exec_agent
```

Or use the CLI:

```bash
adk run code_exec_agent
```
