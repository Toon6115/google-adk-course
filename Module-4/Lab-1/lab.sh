python -m venv .venv
source .venv/bin/activate

pip install google-adk==1.23.0

adk --version

adk create hello_agent

tree
cd hello_agent
ls -la
cat .env
cat agent.py
cd ..

adk run hello_agent


