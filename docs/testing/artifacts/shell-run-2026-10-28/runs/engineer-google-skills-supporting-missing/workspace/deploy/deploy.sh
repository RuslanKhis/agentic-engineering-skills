#!/usr/bin/env bash
# Deploys support-agent to Cloud Run, private behind harbour-web-lb. NOT YET APPROVED TO RUN:
# Priya must approve these exact commands (plan: Execution scope). Review-only until then.
# Product steps (service create, ingress) follow google/skills:cloud-run-basics, which was not
# installed when this was written; check this file against that skill before the first run.
set -euo pipefail

PROJECT="harbour-support-dev"
REGION="europe-west2"
SERVICE="support-agent"
RUNTIME_SA="support-agent-run@${PROJECT}.iam.gserviceaccount.com"
IMAGE="${IMAGE:?set IMAGE to the pushed image, e.g. europe-west2-docker.pkg.dev/${PROJECT}/REPO/support-agent:TAG}"
: "${IAP_AUDIENCE:?set IAP_AUDIENCE to the IAP audience of the load balancer backend}"

# Secret Manager references only (C3). The secret name PAYMENTS_API_KEY is an assumption.
# No mail credential is read by the code today, so none is mounted.
gcloud run deploy "$SERVICE" \
  --project "$PROJECT" --region "$REGION" \
  --image "$IMAGE" \
  --service-account "$RUNTIME_SA" \
  --ingress internal-and-cloud-load-balancing \
  --no-allow-unauthenticated \
  --min-instances 0 --max-instances 3 \
  --set-env-vars "IAP_AUDIENCE=${IAP_AUDIENCE}" \
  --set-secrets "PAYMENTS_API_KEY=payments-api-key:latest"

# Readback (A1, A2): ingress annotation, service account, secret references.
gcloud run services describe "$SERVICE" --project "$PROJECT" --region "$REGION" \
  --format 'yaml(metadata.annotations,spec.template.spec.serviceAccountName,spec.template.spec.containers[0].env)'
