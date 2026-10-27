#!/usr/bin/env bash
# Deploy to Cloud Run with sessions in Cloud SQL and Memory Bank on an existing Agent Engine.
# Not run in this session (no credentials). Memory is reached through fieldline.services.governor(), so
# --memory_service_uri is deliberately absent: the CLI would build an ungoverned memory service beside it.
# MEMORY_LEDGER_DB must be a durable, shared store; the shipped SQLite ledger is a local file (see README).
set -euo pipefail
: "${PROJECT_ID:?}" "${REGION:?}" "${AGENT_ENGINE_ID:?}" "${SESSION_DB_URL:?}" "${MEMORY_LEDGER_DB:?}"

adk deploy cloud_run \
  --project "${PROJECT_ID}" \
  --region "${REGION}" \
  --service_name fieldline \
  --session_service_uri "${SESSION_DB_URL}" \
  fieldline \
  -- --set-env-vars "AGENT_ENGINE_ID=${AGENT_ENGINE_ID},GOOGLE_CLOUD_PROJECT=${PROJECT_ID},GOOGLE_CLOUD_LOCATION=${REGION},MEMORY_LEDGER_DB=${MEMORY_LEDGER_DB}"
