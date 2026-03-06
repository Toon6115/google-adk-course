# Lab 1 - Model Callbacks (Request Logging and Response Monitoring)

Intercept LLM requests and responses using before_model_callback and after_model_callback.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Add Your API Key

Edit `logging_agent/.env` and add your Google AI Studio API key:

```
GOOGLE_API_KEY="your-api-key"
```

## Run the Agent

```bash
python -m logging_agent.agent
```
