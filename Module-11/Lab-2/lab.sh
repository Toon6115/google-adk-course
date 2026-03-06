#!/bin/bash

# Lab-2: Deploy to Vertex AI Agent Engine & Interact
# Prerequisites: Run Lab-1 setup_gcp.sh first

# Verify environment
echo "Project:  $GOOGLE_CLOUD_PROJECT"
echo "Region:   $GOOGLE_CLOUD_LOCATION"

# Install dependencies (includes Vertex AI SDK for interacting with Agent Engine)
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# ============================================
# PART 1: Update .env for Vertex AI
# ============================================
# Agent Engine uses Vertex AI (GCP credentials), NOT an API key.
# If .env has GOOGLE_API_KEY from Lab-1, replace it:
echo "GOOGLE_GENAI_USE_VERTEXAI=TRUE" > ./weather_agent/.env

# ============================================
# PART 2: Deploy to Agent Engine
# ============================================
# No Dockerfile, no containers, no staging bucket needed
# Fully managed by Google

adk deploy agent_engine \
  --project=$GOOGLE_CLOUD_PROJECT \
  --region=$GOOGLE_CLOUD_LOCATION \
  --display_name="Weather Agent" \
  ./weather_agent

# The CLI outputs the Resource Name:
# projects/<project>/locations/<region>/reasoningEngines/<resource_id>
# Save this — you'll need it to interact with the agent

# ============================================
# PART 3: Interact with Agent Engine
# ============================================
# Edit test_agent_engine.py with your PROJECT_ID, LOCATION, and RESOURCE_NAME first

python test_agent_engine.py
