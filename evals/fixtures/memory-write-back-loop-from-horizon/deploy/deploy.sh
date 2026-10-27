#!/usr/bin/env bash
# Deploy to Cloud Run with sessions in Cloud SQL and Memory Bank on an existing Agent Engine.
set -euo pipefail
: "${PROJECT_ID:?}" "${REGION:?}" "${AGENT_ENGINE_ID:?}" "${SESSION_DB_URL:?}"

adk deploy cloud_run \
  --project "${PROJECT_ID}" \
  --region "${REGION}" \
  --service_name fieldline \
  --session_service_uri "${SESSION_DB_URL}" \
  --memory_service_uri "agentengine://${AGENT_ENGINE_ID}" \
  fieldline
