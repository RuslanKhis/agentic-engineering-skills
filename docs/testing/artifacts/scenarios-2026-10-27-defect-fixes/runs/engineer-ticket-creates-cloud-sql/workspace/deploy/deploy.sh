#!/usr/bin/env bash
# Build and deploy the support assistant to Cloud Run in the dev project.
# Usage: PROJECT_ID=harbour-support-dev REGION=europe-west2 deploy/deploy.sh
set -euo pipefail

: "${PROJECT_ID:?set PROJECT_ID}"
: "${REGION:?set REGION}"
: "${VPC_NETWORK:?set VPC_NETWORK (reaches the private-IP session database)}"
: "${VPC_SUBNET:?set VPC_SUBNET}"
SERVICE="${SERVICE:-support-assistant}"
SA="support-assistant-run@${PROJECT_ID}.iam.gserviceaccount.com"
IMAGE="${REGION}-docker.pkg.dev/${PROJECT_ID}/apps/${SERVICE}:$(git rev-parse --short HEAD)"

gcloud builds submit --project "${PROJECT_ID}" --region "${REGION}" --tag "${IMAGE}" .

gcloud run deploy "${SERVICE}" \
  --project "${PROJECT_ID}" \
  --region "${REGION}" \
  --image "${IMAGE}" \
  --service-account "${SA}" \
  --ingress internal-and-cloud-load-balancing \
  --no-allow-unauthenticated \
  --set-env-vars "MODEL_ID=gemini-3.5-flash" \
  --network "${VPC_NETWORK}" --subnet "${VPC_SUBNET}" --vpc-egress private-ranges-only \
  --set-secrets "PAYMENTS_API_KEY=payments-api-key:latest,SESSION_DB_URL=session-db-url:latest" \
  --labels "env=dev,team=support,app=support-assistant"

gcloud run services describe "${SERVICE}" --project "${PROJECT_ID}" --region "${REGION}" \
  --format 'value(status.url,status.latestReadyRevisionName)'
