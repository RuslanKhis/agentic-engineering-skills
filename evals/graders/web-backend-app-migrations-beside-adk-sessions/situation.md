# web-backend-app-migrations-beside-adk-sessions: what the fixture holds

Base: support-assistant. Overlay:

- `app/server.py`: `DatabaseSessionService(db_url=settings.database_url)` and the application
  engine share one database (`DATABASE_URL`, Cloud SQL for PostgreSQL in production, SQLite in
  tests). ADK creates its own session tables there (A1: they must be excluded from Alembic,
  e.g. a separate schema or an `include_object` filter, and application tables prefixed; A2: ADK's
  schema is left to `adk migrate session`).
- `app/db.py`: `metadata.create_all(engine)` at import of the server, i.e. schema created at
  instance start, no Alembic (A2: migrations run as a job, not at instance start).
- `app/saved_answers.py` `get()` filters by id only, and `GET /api/saved-answers/{answer_id}`
  returns any user's record (A4: filter by the verified principal and return the same 404 body as
  an unknown id, "saved answer not found").
- `tests/test_saved_answers.py`: SQLite tests, skipped when SQLAlchemy is absent (the suite passes
  offline with the standard library). A3 expects a test that `alembic check` is clean on a
  database that holds ADK's tables and that those tables are unchanged; the agent cannot run it
  (no shell, nothing installed), so it should be written and reported as not run.

Original context (unchanged): "An ADK 2.12 FastAPI app using DatabaseSessionService on Cloud SQL
for PostgreSQL; no Alembic yet; tests run against SQLite locally."
