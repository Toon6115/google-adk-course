python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

# This demo runs as a standalone script (not adk run)
# because we need to control session creation and inspection
python -m session_agent.agent
