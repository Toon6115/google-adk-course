python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

# Run with ADK CLI
adk run api_agent

# Or run with ADK Web UI
# adk web api_agent
