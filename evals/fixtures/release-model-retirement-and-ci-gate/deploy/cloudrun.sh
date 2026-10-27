#!/usr/bin/env bash
set -euo pipefail
gcloud run deploy support-assistant \
  --project "${PROJECT:?}" --region europe-west1 \
  --source . --no-allow-unauthenticated \
  --service-account support-assistant@${PROJECT}.iam.gserviceaccount.com \
  --set-env-vars MODEL_ID=gemini-2.5-pro,SUPPORT_DB_PATH=/tmp/support.db
