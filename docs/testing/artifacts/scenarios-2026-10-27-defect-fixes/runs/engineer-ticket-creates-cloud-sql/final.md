I wrote the code, the create and delete scripts, the deploy wiring and the tests for G03, but I ran nothing. This session has no shell tool, so the test suite, `bash -n` and the delete script's dry run are all `not run`. I left the ticket `in_progress` and filled in the Evidence section.

**What changed**
- **App:**
  - `app/sessions.py` is new. It builds `DatabaseSessionService` and maps database failures to a `SessionStoreUnavailable` error, leaving other errors alone.
  - `app/server.py` now uses that service and returns 503 on a store failure.
  - `app/settings.py` reads `SESSION_DB_URL`.
- **Scripts:**
  - `deploy/create_sessions_db.sh` creates the instance `support-sessions-dev` (Postgres 16, `db-custom-1-3840`, 10 GB SSD, private IP, no backups), the `sessions` database and the `sessions_app` user. It refuses any project other than `harbour-support-dev` and refuses to touch an instance that already exists.
  - `deploy/delete_sessions_db.sh` is a dry run unless `EXECUTE=yes` and `CONFIRM_DELETE=support-sessions-dev` are set. It deletes only an instance labelled `goal=g03`, then lists the instance and `gcloud sql backups list --instance=-` for verification.
  - `deploy/deploy.sh` now needs `VPC_NETWORK` and `VPC_SUBNET` and reads the secret `session-db-url`; `deploy/README.md` describes both scripts and the owed steps.
- **Tests:** `tests/test_sessions.py` covers settings, the failure mapping, restart survival (SQLite stand-in), another user getting nothing, and the 503 route.

**Acceptance cases**
- **A1 (restart):** the offline test is written but not run, and the live check on Cloud SQL hasn't happened because the instance doesn't exist.
- **A2 (503, no partial session):** the route test is written but not run. There is a known gap: if the store fails mid-run on a session created in that request, the cleanup delete fails too if the store is still down. A partial session can remain.
- **Instance:** it was never created and nothing in the cloud was touched. The Evidence records it as absent with its cleanup command. The USD 1.75 per day is your ticket's figure, which I couldn't re-check against the pricing page.

**Not done**
- **Local checks:** run the baseline `tests.test_tools` and `tests.test_auth`, then `tests.test_sessions`, and check the script syntax.
- **Dependencies:** `asyncpg` and `aiosqlite` need pins in `pyproject.toml`. I didn't invent versions.
- **Prerequisites outside the authorised scope:** private services access on the VPC, the `session-db-url` secret, and `roles/cloudsql.client` for the runtime service account.
- **Live steps:** run the create script and `deploy.sh`, then the live A1 and A2 checks.
- **Design:** the C2 Evidence cell stays `planned: G03`.

**Questions I couldn't ask, and what I assumed**
- Password via Secret Manager, as D2 says, rather than IAM database auth.
- No backups, since the ticket's cost line lists none.
- `db-custom` tiers need Cloud SQL's Enterprise edition, so the script sets `--edition ENTERPRISE`.
- VPC names come from environment variables.
- The store guard also wraps the agent run, so an unrelated `OSError` there would show as 503.

I estimate about 1–1.5 hours of human effort is still owed.

Resume with: `/adk-engineer Resume docs/tickets/support/G03.md from its Progress block.` Evidence currently holds the owed-items list rather than a formal `Progress:` block.