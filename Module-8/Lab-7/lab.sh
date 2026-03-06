# MCP tools require the ADK CLI for proper async initialization
# Do NOT run with `python agent.py` — use `adk run` or `adk web`

python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

# Make sure Node.js/npx is installed for MCP server
# node --version
# npx --version

# Run with ADK CLI — pass the agent PACKAGE name
adk run file_assistant

# Or run with ADK Web UI
# adk web file_assistant
