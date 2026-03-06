python -m venv .venv
source .venv/bin/activate

# pip install google-adk==1.23.0
pip install -r requirements.txt

adk --version

adk create --type=config hello_agent

tree
cd hello_agent
ls -la
cat .env
cat root_agent.yaml
cd ..

adk run hello_agent