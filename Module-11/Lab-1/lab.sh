#!/bin/bash

# Lab-1: Build, Setup GCP & Deploy to Cloud Run
# This creates a deployment-ready agent, sets up GCP, and deploys to Cloud Run

# ============================================
# PART 1: Build the Agent & Verify Locally
# ============================================

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Launch the ADK Web UI to verify the agent works locally
# Open http://localhost:8000 in your browser
# Press Ctrl+C when done testing
adk web .

# ============================================
# PART 2: GCP Environment Setup
# ============================================
# Edit setup_gcp.sh with your project ID and API key first
# nano setup_gcp.sh

# source setup_gcp.sh

# Verify everything is configured
gcloud config list
echo "GOOGLE_CLOUD_PROJECT=$GOOGLE_CLOUD_PROJECT"
echo "GOOGLE_CLOUD_LOCATION=$GOOGLE_CLOUD_LOCATION"

# ============================================
# PART 3: Deploy to Cloud Run
# ============================================
# --with_ui: deploys the ADK Web UI alongside the API
# The CLI handles everything: Dockerfile, build, push, deploy

adk deploy cloud_run \
  --project=$GOOGLE_CLOUD_PROJECT \
  --region=$GOOGLE_CLOUD_LOCATION \
  --service_name=weather-agent-service \
  --with_ui \
  ./weather_agent
