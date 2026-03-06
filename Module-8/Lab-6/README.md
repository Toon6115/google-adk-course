# Lab 6 - CrewAI Tool Integration (Web Scraping)

Build an agent that wraps CrewAI's web scraping tool using CrewaiTool.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Add Your API Key

Edit `web_reader_agent/.env` and add your Google AI Studio API key:

```
GOOGLE_API_KEY="your-api-key"
```

## Run the Agent

```bash
adk web web_reader_agent
```

Or use the CLI:

```bash
adk run web_reader_agent
```
