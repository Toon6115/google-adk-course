# Lab 1 - Deploy to Google Cloud Run

Deploy an ADK agent to Cloud Run with the built-in Web UI.

## Prerequisites

- A Google Cloud project with billing enabled
- `gcloud` CLI installed

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Step 1 - Verify Locally

```bash
adk web .
```

Open http://localhost:8000 and test the agent. Press Ctrl+C when done.

## Step 2 - Configure GCP

Edit `setup_gcp.sh` with your project ID, region, and API key, then run it:

```bash
source setup_gcp.sh
```

Verify the configuration:

```bash
gcloud config list
```

## Step 3 - Deploy to Cloud Run

```bash
adk deploy cloud_run \
  --project=$GOOGLE_CLOUD_PROJECT \
  --region=$GOOGLE_CLOUD_LOCATION \
  --service_name=weather-agent-service \
  --with_ui \
  ./weather_agent
```

## Cleanup

When you are done, run the cleanup script to delete Cloud Run resources:

```bash
source cleanup.sh
```
