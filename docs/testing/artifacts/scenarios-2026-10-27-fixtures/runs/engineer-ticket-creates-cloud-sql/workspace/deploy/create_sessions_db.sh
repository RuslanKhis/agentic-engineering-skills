#!/usr/bin/env bash
# Create the Cloud SQL instance, database and user that hold ADK sessions (G03).
# Usage: PROJECT_ID=harbour-support-dev REGION=europe-west2 NETWORK=<vpc> \
#          DB_PASSWORD_SECRET=sessions-db-password deploy/create_sessions_db.sh [--dry-run]
# Creates only: the instance, one database, one user. It does not create the
# secret, the private-services peering or any IAM binding (see deploy/README.md).
set -euo pipefail

: "${PROJECT_ID:?set PROJECT_ID}"
: "${REGION:?set REGION}"
: "${NETWORK:?set NETWORK (VPC with private services access already configured)}"
: "${DB_PASSWORD_SECRET:?set DB_PASSWORD_SECRET (existing Secret Manager secret holding the db user password)}"
INSTANCE="${INSTANCE:-support-sessions-dev}"
DATABASE="${DATABASE:-sessions}"
DB_USER="${DB_USER:-sessions_app}"

if [[ "${PROJECT_ID}" != "harbour-support-dev" ]]; then
  echo "refusing: instance creation is authorised for harbour-support-dev only" >&2
  exit 1
fi

DRY=""
[[ "${1:-}" == "--dry-run" ]] && DRY=1
exec_or_print() {
  if [[ -n "${DRY}" ]]; then printf 'DRY RUN:'; printf ' %q' "$@"; printf '\n'; else "$@"; fi
}

exec_or_print gcloud sql instances create "${INSTANCE}" \
  --project "${PROJECT_ID}" \
  --region "${REGION}" \
  --database-version POSTGRES_16 \
  --edition ENTERPRISE \
  --tier db-custom-1-3840 \
  --storage-type SSD \
  --storage-size 10GB \
  --network "projects/${PROJECT_ID}/global/networks/${NETWORK}" \
  --no-assign-ip \
  --labels "env=dev,team=support,app=support-assistant,owner-ticket=g06"

exec_or_print gcloud sql databases create "${DATABASE}" \
  --project "${PROJECT_ID}" --instance "${INSTANCE}"

if [[ -n "${DRY}" ]]; then
  echo "DRY RUN: gcloud sql users create ${DB_USER} --password <from secret ${DB_PASSWORD_SECRET}>"
else
  gcloud secrets versions access latest --secret "${DB_PASSWORD_SECRET}" --project "${PROJECT_ID}" |
    { read -r pw; gcloud sql users create "${DB_USER}" --project "${PROJECT_ID}" \
        --instance "${INSTANCE}" --password "${pw}"; }
fi

echo "Created ${INSTANCE}. Idle cost about USD 1.75/day until deploy/delete_sessions_db.sh runs (G06)."
