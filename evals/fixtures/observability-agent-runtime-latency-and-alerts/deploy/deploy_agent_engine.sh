#!/usr/bin/env bash
# Deploys the support agent to Agent Runtime (Vertex AI Agent Engine).
set -euo pipefail
PROJECT="${PROJECT:?set PROJECT}"
REGION="${REGION:-europe-west1}"
adk deploy agent_engine \
  --project "$PROJECT" \
  --region "$REGION" \
  --display_name support-assistant \
  --env_file deploy/agent_engine.env \
  app
