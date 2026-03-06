# Lab 1 - Multi-Turn Conversations with Gemini

Run a multi-turn conversation using the Runner class with Gemini 2.5 Flash.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Add Your API Key

Edit `.env` and add your Google AI Studio API key:

```
GOOGLE_API_KEY="your-api-key"
GOOGLE_GENAI_USE_VERTEXAI=FALSE
```

## Run the Agent

```bash
python agent.py
```
