python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

adk run hello_agent

adk web

adk api_server

# In other terminal
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
      "parts": [{"text": "What is the capital of India"}]
    }
  }'

# Optional - Install jq from https://jqlang.org/
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
  }' | jq 