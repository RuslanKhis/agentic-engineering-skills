#!/usr/bin/env bash
# Removes the Cloud Run service this ticket owns. Requires a typed confirmation; NOT approved to run.
# Does not touch the serverless NEG or URL map (web platform team), the runtime service account,
# secrets, or pushed images; remove those separately once confirmed as owned by this ticket.
set -euo pipefail
PROJECT="harbour-support-dev"; REGION="europe-west2"; SERVICE="support-agent"
read -r -p "Type '${SERVICE}' to delete it from ${PROJECT}/${REGION}: " answer
[ "$answer" = "$SERVICE" ] || { echo "not confirmed"; exit 1; }
gcloud run services delete "$SERVICE" --project "$PROJECT" --region "$REGION" --quiet
