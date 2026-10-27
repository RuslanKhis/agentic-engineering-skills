I set up Alembic for the `saved_answers` table, but none of it has been run. I had no shell here, so I couldn't run the tests, `alembic upgrade head` or `alembic check`. I also couldn't install anything, so the new Alembic dependency isn't installed.

**What I changed**
- **Alembic config:** I added `alembic.ini` and `migrations/` with the usual `script.py.mako`.
- **ADK tables excluded:** `migrations/env.py` leaves out ADK's five tables (`sessions`, `events`, `app_states`, `user_states`, `adk_internal_metadata`). Without that, autogenerate would propose dropping them, because they live in the same Postgres. It reads `DATABASE_URL` through `Settings` and imports nothing from ADK.
- **First migration:** `migrations/versions/0001_create_saved_answers.py` creates `saved_answers` and its `user_id` index.
- **`create_all` removed:** `app/db.py`'s `make_engine` used to call `metadata.create_all()` at startup. That would race with migrations, so it now only builds the engine. The saved-answers tests now call `metadata.create_all` themselves on SQLite.
- **New pin:** `pyproject.toml` gains `alembic==1.16.5`. No existing pins changed. I picked that version from memory, so check it resolves alongside `sqlalchemy==2.0.43`.
- **README:** it now has a Migrations section.

**Questions I couldn't ask, and what I assumed**
- **Does `saved_answers` already exist in production?** The old `create_all` would have created it on first start. I assumed it might. If so, don't run `upgrade` there. Run `alembic stamp head` once after confirming the columns match. This is in the README.
- **Table name:** I kept `saved_answers` rather than adding an `app_` prefix. Renaming a live table is a separate decision.
- **Driver:** the migration uses the app's existing sync psycopg URL. Migrations run as a short job, so I didn't add an async engine.

**Left undone**
- Run `pip install -e .`, then the tests, then `alembic upgrade head` followed by `alembic check` on an empty database.
- Run `alembic upgrade head` as a release step or Cloud Run job. I didn't wire that up, and I didn't touch any real database.

**A bug I noticed and didn't fix**
`GET /api/saved-answers/{id}` in `app/server.py` and `saved_answers.get` don't filter by user. Any signed-in user can read another user's saved answer by guessing the ID. The fix is to filter by `user_id` in the query and return the same 404 as for an unknown ID. I left it alone because it is outside the migrations request. I'd fix it before shipping.