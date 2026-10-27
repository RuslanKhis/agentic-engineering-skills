#!/usr/bin/env bash
# Create the session database for G03: one Cloud SQL for PostgreSQL instance, one
# database and one user, in the dev project only. Creates nothing else: no secret,
# no IAM grant, no network (see deploy/README.md for those owed steps).
# Usage: PROJECT_ID=harbour-support-dev REGION=europe-west2 \
#        VPC_NETWORK=<network with private services access> \
#        SESSION_DB_PASSWORD=<password, from your shell, not the command line history> \
#        deploy/create_sessions_db.sh
# Cleanup: deploy/delete_sessions_db.sh (owned by G06).
set -euo pipefail

: "${PROJECT_ID:?set PROJECT_ID}"
: "${REGION:?set REGION}"
: "${VPC_NETWORK:?set VPC_NETWORK (the VPC with private services access already configured)}"
: "${SESSION_DB_PASSWORD:?set SESSION_DB_PASSWORD}"
[ "${PROJECT_ID}" = "harbour-support-dev" ] || { echo "refusing: only harbour-support-dev is authorised" >&2; exit 2; }
[ "${REGION}" = "europe-west2" ] || { echo "refusing: ticket G03 names europe-west2" >&2; exit 2; }

INSTANCE="${INSTANCE:-support-sessions-dev}"
DATABASE="${DATABASE:-sessions}"
DB_USER="${DB_USER:-sessions_app}"

# A name that already exists is not ours to adopt or alter.
existing="$(gcloud sql instances list --project "${PROJECT_ID}" --filter "name=${INSTANCE}" --format 'value(name)' --limit 1)"
[ -z "${existing}" ] || { echo "refusing: instance ${INSTANCE} already exists" >&2; exit 3; }

# Enterprise edition is required for db-custom tiers. No backups or PITR: the
# ticket's cost line lists none, and C2 needs restart survival, not recovery.
gcloud sql instances create "${INSTANCE}" \
  --project "${PROJECT_ID}" \
  --region "${REGION}" \
  --database-version POSTGRES_16 \
  --edition ENTERPRISE \
  --tier db-custom-1-3840 \
  --storage-type SSD \
  --storage-size 10GB \
  --network "projects/${PROJECT_ID}/global/networks/${VPC_NETWORK}" \
  --no-assign-ip \
  --no-backup \
  --labels "env=dev,team=support,app=support-assistant,goal=g03" \
  --quiet

gcloud sql databases create "${DATABASE}" --instance "${INSTANCE}" --project "${PROJECT_ID}" --quiet

# The password comes from the environment, never from an argument default or a log.
gcloud sql users create "${DB_USER}" --instance "${INSTANCE}" --project "${PROJECT_ID}" \
  --password "${SESSION_DB_PASSWORD}" --quiet

gcloud sql instances describe "${INSTANCE}" --project "${PROJECT_ID}" \
  --format 'value(name,state,ipAddresses[0].ipAddress)'
