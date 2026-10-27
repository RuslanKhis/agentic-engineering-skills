I wrote the code, scripts and tests for G03, but I couldn't run any of it. Shell access was disabled in this session, so no tests, `bash -n` checks or dry runs happened. The ticket is `in_progress`, and the Evidence section says "written", not "verified". Nothing was created in the cloud.

**What I changed**
- **Session service:** `app/settings.py` has a new `session_db_url`, read from `SESSION_DB_URL`, with a SQLite default for offline use. `app/server.py` now uses `DatabaseSessionService`. `/api/chat` returns 503 on `SQLAlchemyError` or `OSError`, and the response never carries a session id.
- **Create script:** `deploy/create_sessions_db.sh` creates the instance, database and user with the specs from the ticket. It refuses any project except `harbour-support-dev` and has `--dry-run`.
- **Delete script:** `deploy/delete_sessions_db.sh` deletes the user, database and then the instance. It refuses to run without `CONFIRM_DELETE=support-sessions-dev` and also has `--dry-run`. G06 owns it.
- **Deploy script:** `deploy/deploy.sh` now needs `NETWORK` and `SUBNET`, uses Direct VPC egress, and reads `SESSION_DB_URL` from the secret `sessions-db-url`. It will fail until those exist.
- **Tests:** `tests/test_sessions.py` covers the settings, a new service object reading the same SQLite file (standing in for a restart, A1), and an unreachable store giving 503 with no create call (A2). The SDK-dependent tests skip if the SDK is missing.
- **Docs:** `deploy/README.md` and the ticket's Evidence section are updated, with a Progress block and a resume prompt.

**Assumptions I proceeded on** (written into Evidence)
- `NETWORK` and `SUBNET` are supplied by the caller, and private services access is already set up on the VPC.
- Database credentials follow D2: a built-in user whose password is in an existing Secret Manager secret, and the full connection URL in `sessions-db-url`. The skill reference prefers IAM database auth, so this is the likely rework if you want that instead.
- `asyncpg` and `aiosqlite` come with the pinned `google-adk==2.12.0`. I couldn't check this and left the pins alone.
- The scripts don't create the secrets, the peering or any IAM bindings, because only instance creation is authorised. `deploy/README.md` lists them for a person to do.

**Left undone**
- Baseline `pass_to_pass` tests, `tests.test_sessions`, `bash -n` and both dry runs.
- The instance is not created, so I didn't run `gcloud sql instances list`. The live A1 (instance restart) and A2 (database unreachable) checks are owed.
- The USD 1.75/day price is the ticket's own figure. I couldn't read the pricing page here, so it is unconfirmed and that item stays open.
- The design's C2 Evidence cell is unchanged.
- One known gap: if the store fails after `create_session` succeeds, an empty stored session remains. Only the response withholds its id.
- Review and verify is still about 1–1.5 hours of human work. `actual:` is `not reported`.

Next step: `/adk-engineer Resume docs/tickets/support/G03.md from its Progress block.`