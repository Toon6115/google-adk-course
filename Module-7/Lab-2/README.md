# Lab 2 - Using Vertex AI with GCP Authentication

Run an agent using Vertex AI instead of a Google AI Studio API key.

## Prerequisites

- A Google Cloud project with billing enabled
- `gcloud` CLI installed

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Authenticate with GCP

```bash
gcloud auth application-default login
gcloud auth application-default set-quota-project "your-gcp-project-id"
```

## Configure Environment

Edit `.env` and set your GCP project details:

```
GOOGLE_GENAI_USE_VERTEXAI=TRUE
GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
GOOGLE_CLOUD_LOCATION="your-region"
```

## Run the Agent

```bash
python agent.py
```
