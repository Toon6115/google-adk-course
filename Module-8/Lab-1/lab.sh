python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

# Run with ADK CLI
adk run weather_agent

# Or run with ADK Web UI
# adk web weather_agent
