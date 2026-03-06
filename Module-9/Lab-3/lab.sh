python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

# This demo runs as a standalone script (not adk run)
# because we need to inspect memory across multiple sessions programmatically
python -m memory_agent.agent
