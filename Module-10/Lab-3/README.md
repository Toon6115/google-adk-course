# Lab 3 - Input and Output Guardrails

Protect an agent with input guardrails (blocked keywords, injection detection) and output guardrails (PII redaction, length enforcement).

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Add Your API Key

Edit `input_guard_agent/.env` and add your Google AI Studio API key:

```
GOOGLE_API_KEY="your-api-key"
```

## Run the Agent

```bash
python -m input_guard_agent.agent
```
