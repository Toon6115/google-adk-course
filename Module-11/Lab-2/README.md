# Lab 2 - Deploy to Vertex AI Agent Engine

Deploy an ADK agent to Google's fully managed Agent Engine (serverless, no containers needed).

## Prerequisites

- A Google Cloud project with billing enabled
- `gcloud` CLI installed
- GCP environment configured (run `setup_gcp.sh` if not already done)

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Step 1 - Configure GCP

Edit `setup_gcp.sh` with your project ID, region, and API key, then run it:

```bash
source setup_gcp.sh
```

## Step 2 - Deploy to Agent Engine

```bash
adk deploy agent_engine \
  --project=$GOOGLE_CLOUD_PROJECT \
  --region=$GOOGLE_CLOUD_LOCATION \
  --display_name="Weather Agent" \
  ./weather_agent
```

Save the Resource Name from the output. You will need it in the next step.

## Step 3 - Interact with the Deployed Agent

Edit `test_agent_engine.py` and set your PROJECT_ID, LOCATION, and RESOURCE_NAME, then run:

```bash
python test_agent_engine.py
```

## Cleanup

Edit `cleanup.py` with your PROJECT_ID and LOCATION, then run it to delete all Agent Engine resources:

```bash
python cleanup.py
```
