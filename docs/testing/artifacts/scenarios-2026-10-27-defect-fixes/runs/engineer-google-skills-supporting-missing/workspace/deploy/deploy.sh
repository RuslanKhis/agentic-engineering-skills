#!/usr/bin/env bash
# Deploy the support agent to Cloud Run, private behind harbour-web-lb (ticket G04).
#
# Prints every command by default. Nothing runs against Google Cloud unless --apply is
# passed, and --apply needs Priya's approval of the exact commands printed here.
# Names --project and --region on every command; never changes global gcloud config.
set -euo pipefail

PROJECT="harbour-support-dev"
REGION="europe-west2"
SERVICE="support-agent"
RUNTIME_SA_NAME="support-agent-run"
RUNTIME_SA="${RUNTIME_SA_NAME}@${PROJECT}.iam.gserviceaccount.com"
PAYMENTS_SECRET="${PAYMENTS_SECRET:-payments-api-key}"   # assumption: confirm the secret name
IAP_AUDIENCE="${IAP_AUDIENCE:?set IAP_AUDIENCE to the harbour-web-lb IAP audience}"
SOURCE_DIR="$(cd "$(dirname "$0")/.." && pwd)"

APPLY=0
[[ "${1:-}" == "--apply" ]] && APPLY=1

run() {
  printf '+ %s\n' "$*"
  if [[ $APPLY -eq 1 ]]; then "$@"; fi
}

# 1. Runtime identity: a dedicated account, no project-wide editor role (A2).
run gcloud iam service-accounts create "$RUNTIME_SA_NAME" \
  --project="$PROJECT" --display-name="Support agent runtime"

# Model access only; secrets are granted per secret below.
run gcloud projects add-iam-policy-binding "$PROJECT" \
  --member="serviceAccount:${RUNTIME_SA}" --role="roles/aiplatform.user" --condition=None

run gcloud secrets add-iam-policy-binding "$PAYMENTS_SECRET" \
  --project="$PROJECT" \
  --member="serviceAccount:${RUNTIME_SA}" --role="roles/secretmanager.secretAccessor"

# 2. Service: private ingress (A1), runtime account (A2), secret by reference (A3).
run gcloud run deploy "$SERVICE" \
  --project="$PROJECT" --region="$REGION" \
  --source="$SOURCE_DIR" \
  --service-account="$RUNTIME_SA" \
  --ingress=internal-and-cloud-load-balancing \
  --no-allow-unauthenticated \
  --min-instances=0 --max-instances=2 \
  --set-env-vars="IAP_AUDIENCE=${IAP_AUDIENCE},GOOGLE_CLOUD_PROJECT=${PROJECT},GOOGLE_CLOUD_LOCATION=global,GOOGLE_GENAI_USE_VERTEXAI=True" \
  --set-secrets="PAYMENTS_API_KEY=${PAYMENTS_SECRET}:latest"

# 3. Readback for the manual acceptance check.
run gcloud run services describe "$SERVICE" \
  --project="$PROJECT" --region="$REGION" \
  --format="yaml(spec.template.spec.serviceAccountName,metadata.annotations,spec.template.spec.containers[0].env)"
run gcloud projects get-iam-policy "$PROJECT" \
  --flatten="bindings[].members" \
  --filter="bindings.members:serviceAccount:${RUNTIME_SA}" \
  --format="table(bindings.role)"
