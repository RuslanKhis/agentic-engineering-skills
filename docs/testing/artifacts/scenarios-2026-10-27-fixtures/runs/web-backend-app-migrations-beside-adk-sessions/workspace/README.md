# Support assistant

Customer-support assistant for Harbour Outfitters' online shop, built on
Google ADK. It answers order questions, searches the help-centre articles,
reads inbound support emails, issues refunds through the payments provider
and sends replies. Signed-in customers reach it through the web chat; the
FastAPI service runs on Cloud Run behind IAP.

## Layout

- `app/agent.py` builds the ADK agent (`build_agent()`, `root_agent`).
- `app/prompts.py` holds the instruction text.
- `app/tools/` holds the tool functions; they import nothing from ADK so the
  unit tests can load them without the SDK.
- `app/clients/` wraps the payments and mail providers.
- `app/store.py` is the SQLite store (orders, customer profiles, refunds).
- `app/auth.py` turns the IAP assertion into a `Principal`.
- `app/server.py` is the FastAPI app.
- `app/db.py`, `app/saved_answers.py` hold the saved-answers table and queries.

## Migrations

Application tables (`app/db.py`) are managed by Alembic (`migrations/`). The
database is shared with ADK's session tables (`sessions`, `events`,
`app_states`, `user_states`, `adk_internal_metadata`); `migrations/env.py`
excludes them, so Alembic never creates, alters or drops them. ADK upgrades
its own tables with `adk migrate session`.

Run migrations as a release step or Cloud Run job, not at instance start:

```bash
DATABASE_URL=... alembic upgrade head
```

If `saved_answers` already exists in a database (the app used to create it at
startup), do not run `upgrade`; run `alembic stamp head` once after checking
that its columns match `migrations/versions/0001_create_saved_answers.py`.

New change: edit `app/db.py`, run `alembic revision --autogenerate -m "..."`,
review the file by hand.

## Tests

```bash
python -m unittest discover -s tests -t .
```

The tests use fakes for the providers and need neither ADK nor network.
