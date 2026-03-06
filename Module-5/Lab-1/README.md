# Lab 1 - Running Agents (CLI, Web UI, and API Server)

Explore the three ways to interact with an ADK agent.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Add Your API Key

Edit `hello_agent/.env` and add your Google AI Studio API key:

```
GOOGLE_GENAI_USE_VERTEXAI=0
GOOGLE_API_KEY="your-api-key"
```

## Option 1 - ADK Web UI

```bash
adk web
```

Open http://localhost:8000 in your browser.

## Option 2 - ADK CLI

```bash
adk run hello_agent
```

## Option 3 - API Server

```bash
adk api_server
```

In another terminal, create a session and send a message:

```bash
curl -X POST "http://localhost:8000/apps/hello_agent/users/user_1/sessions/session_1" \
  -H "Content-Type: application/json"

curl -X POST "http://localhost:8000/run" \
  -H "Content-Type: application/json" \
  -d '{
    "appName": "hello_agent",
    "userId": "user_1",
    "sessionId": "session_1",
    "newMessage": {
      "role": "user",
      "parts": [{"text": "What is the capital of India?"}]
    }
  }'
```
