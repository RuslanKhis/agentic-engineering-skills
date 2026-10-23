# Application data and migrations beside ADK's tables

Read when the application has its own tables, or when sessions move to
`DatabaseSessionService`.

`DatabaseSessionService` creates its schema itself with SQLAlchemy's
`metadata.create_all`: `sessions`, `events`, `app_states`, `user_states` and
`adk_internal_metadata` (the v0 schema lacks the last). ADK upgrades its own
schema with `adk migrate session --source_db_url ... --dest_db_url ...`.
Application migrations must never manage these tables: with no filter,
Alembic's autogenerate compares the database with the application's metadata
and proposes dropping all five (shown by this skill's runtime contracts).

Choose one, in order of preference:

1. A separate database, or a separate schema on PostgreSQL, for application
   tables.
2. A shared database with an `include_object` filter in `migrations/env.py`:

   ```python
   ADK_TABLES = frozenset({"sessions", "events", "app_states", "user_states", "adk_internal_metadata"})

   def include_object(obj, name, type_, reflected, compare_to):
       return not (type_ == "table" and name in ADK_TABLES)

   context.configure(connection=connection, target_metadata=Base.metadata,
                     include_object=include_object)
   ```

Either way:

- Prefix application tables (`app_documents`) so a name never collides with
  ADK's.
- Run `alembic upgrade head` as a job (a Cloud Run job or a release step),
  not at instance start, where several instances would race.
- Use async drivers beside the async Runner (`asyncpg`,
  `sqlite+aiosqlite` locally); SQLAlchemy's asyncio extension also needs
  `greenlet` (`sqlalchemy[asyncio]`).
- Every query on owned records filters by the principal's subject in SQL, not
  after loading (SB04).
- `alembic check` after `upgrade head` on an empty database exits 0, and ADK's
  table definitions are unchanged afterwards.

Session storage choice, retention and erasure belong to
`adk-memory-architecture`.
