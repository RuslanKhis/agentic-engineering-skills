#!/usr/bin/env bash
# Delete the G03 session instance (the database and user go with it). Owned by G06.
# Dry run by default: prints the commands and changes nothing.
# Usage: PROJECT_ID=harbour-support-dev deploy/delete_sessions_db.sh            # dry run
#        PROJECT_ID=harbour-support-dev CONFIRM_DELETE=support-sessions-dev EXECUTE=yes \
#          deploy/delete_sessions_db.sh
# Stop or redeploy the Cloud Run service without SESSION_DB_URL first, or its chat
# route returns 503 once the instance is gone. This script does not touch the
# service, the Secret Manager secret or IAM grants; they are not created here.
set -euo pipefail

: "${PROJECT_ID:?set PROJECT_ID}"
[ "${PROJECT_ID}" = "harbour-support-dev" ] || { echo "refusing: only harbour-support-dev is in scope" >&2; exit 2; }
INSTANCE="${INSTANCE:-support-sessions-dev}"
[ "${INSTANCE}" = "support-sessions-dev" ] || { echo "refusing: only support-sessions-dev is owned by G03" >&2; exit 2; }

run() {
  if [ "${EXECUTE:-no}" = "yes" ]; then "$@"; else echo "DRY RUN: $*"; fi
}

# Ownership: delete only an instance carrying the label this ticket's script set.
goal="$(gcloud sql instances describe "${INSTANCE}" --project "${PROJECT_ID}" --format 'value(settings.userLabels.goal)' 2>/dev/null || true)"
if [ -z "${goal}" ]; then
  echo "instance ${INSTANCE} not found or inaccessible; nothing deleted (state unknown if access failed)" >&2
  exit 0
fi
[ "${goal}" = "g03" ] || { echo "refusing: ${INSTANCE} is not labelled goal=g03" >&2; exit 3; }

if [ "${EXECUTE:-no}" = "yes" ] && [ "${CONFIRM_DELETE:-}" != "${INSTANCE}" ]; then
  echo "refusing: set CONFIRM_DELETE=${INSTANCE} to execute" >&2; exit 4
fi

run gcloud sql instances delete "${INSTANCE}" --project "${PROJECT_ID}" --quiet

# Verification starts here: the list must be empty, and retained backups checked.
run gcloud sql instances list --project "${PROJECT_ID}" --filter "name=${INSTANCE}" --format 'value(name)' --limit 5
run gcloud sql backups list --instance=- --project "${PROJECT_ID}" --limit 20
