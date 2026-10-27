"""Alembic environment for the application tables.

The database is shared with ADK's DatabaseSessionService, which creates and
upgrades its own tables (`adk migrate session`). Alembic must never touch
them, so every ADK table is filtered out of autogenerate and `alembic check`.
"""
from logging.config import fileConfig

from alembic import context
from sqlalchemy import create_engine, pool

from app.db import metadata
from app.settings import Settings

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = metadata

ADK_TABLES = frozenset({"sessions", "events", "app_states", "user_states", "adk_internal_metadata"})


def include_object(obj, name, type_, reflected, compare_to):
    return not (type_ == "table" and name in ADK_TABLES)


def _url() -> str:
    return config.get_main_option("sqlalchemy.url") or Settings.from_env().database_url


def run_migrations_offline() -> None:
    context.configure(url=_url(), target_metadata=target_metadata, literal_binds=True,
                      include_object=include_object, dialect_opts={"paramstyle": "named"})
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    engine = create_engine(_url(), poolclass=pool.NullPool)
    with engine.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata,
                          include_object=include_object)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
