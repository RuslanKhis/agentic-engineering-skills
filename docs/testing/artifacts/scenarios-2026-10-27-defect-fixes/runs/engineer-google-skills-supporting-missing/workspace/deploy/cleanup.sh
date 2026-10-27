#!/usr/bin/env bash
# Remove what deploy.sh created. Prints commands by default; --apply runs them, and needs
# a separate confirmation naming the service (pilot teardown goal). Shared resources
# (the secret itself, harbour-web-lb, the NEG) are not touched.
set -euo pipefail

PROJECT="harbour-support-dev"
REGION="europe-west2"
SERVICE="support-agent"
RUNTIME_SA="support-agent-run@${PROJECT}.iam.gserviceaccount.com"
PAYMENTS_SECRET="${PAYMENTS_SECRET:-payments-api-key}"

APPLY=0
[[ "${1:-}" == "--apply" ]] && APPLY=1

run() {
  printf '+ %s\n' "$*"
  if [[ $APPLY -eq 1 ]]; then "$@"; fi
}

run gcloud run services delete "$SERVICE" --project="$PROJECT" --region="$REGION" --quiet
run gcloud secrets remove-iam-policy-binding "$PAYMENTS_SECRET" --project="$PROJECT" \
  --member="serviceAccount:${RUNTIME_SA}" --role="roles/secretmanager.secretAccessor"
run gcloud projects remove-iam-policy-binding "$PROJECT" \
  --member="serviceAccount:${RUNTIME_SA}" --role="roles/aiplatform.user" --condition=None
run gcloud iam service-accounts delete "$RUNTIME_SA" --project="$PROJECT" --quiet

# Source-deploy leftovers to inventory and remove only if listed as created by this service:
# the Cloud Run source image repository (cloud-run-source-deploy) and the source staging bucket.
printf '# Check: gcloud artifacts docker images list %s-docker.pkg.dev/%s/cloud-run-source-deploy --project=%s\n' \
  "$REGION" "$PROJECT" "$PROJECT"
