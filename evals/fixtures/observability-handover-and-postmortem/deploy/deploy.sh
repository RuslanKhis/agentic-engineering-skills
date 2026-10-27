#!/usr/bin/env bash
set -euo pipefail
gcloud run deploy claims-intake \
  --project kestrel-claims-prod --region europe-west2 \
  --source . --no-allow-unauthenticated --ingress internal-and-cloud-load-balancing \
  --service-account claims-intake@kestrel-claims-prod.iam.gserviceaccount.com \
  --set-secrets POLICY_API_TOKEN=policy-api-token:latest \
  --set-env-vars GOOGLE_CLOUD_PROJECT=kestrel-claims-prod,GOOGLE_GENAI_USE_VERTEXAI=true
