#!/usr/bin/env bash
# Delete what deploy/create_sessions_db.sh created: the user, database and
# instance (dependants before owner). Owned by G06 Pilot teardown.
# Usage: PROJECT_ID=harbour-support-dev CONFIRM_DELETE=support-sessions-dev \
#          deploy/delete_sessions_db.sh [--dry-run]
# Deleting the instance removes its data; sessions are lost.
set -euo pipefail

: "${PROJECT_ID:?set PROJECT_ID}"
INSTANCE="${INSTANCE:-support-sessions-dev}"
DATABASE="${DATABASE:-sessions}"
DB_USER="${DB_USER:-sessions_app}"

if [[ "${PROJECT_ID}" != "harbour-support-dev" || "${INSTANCE}" != "support-sessions-dev" ]]; then
  echo "refusing: this script deletes support-sessions-dev in harbour-support-dev only" >&2
  exit 1
fi

DRY=""
[[ "${1:-}" == "--dry-run" ]] && DRY=1
if [[ -z "${DRY}" && "${CONFIRM_DELETE:-}" != "${INSTANCE}" ]]; then
  echo "refusing: set CONFIRM_DELETE=${INSTANCE} to delete" >&2
  exit 1
fi

exec_or_print() {
  if [[ -n "${DRY}" ]]; then printf 'DRY RUN:'; printf ' %q' "$@"; printf '\n'; else "$@"; fi
}

exec_or_print gcloud sql users delete "${DB_USER}" --project "${PROJECT_ID}" --instance "${INSTANCE}" --quiet
exec_or_print gcloud sql databases delete "${DATABASE}" --project "${PROJECT_ID}" --instance "${INSTANCE}" --quiet
exec_or_print gcloud sql instances delete "${INSTANCE}" --project "${PROJECT_ID}" --quiet

echo "Verify absence: gcloud sql instances list --project ${PROJECT_ID}"
