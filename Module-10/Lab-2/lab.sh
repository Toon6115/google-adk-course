python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

# Standalone script to see callback output in the terminal
python -m tool_validator_agent.agent
