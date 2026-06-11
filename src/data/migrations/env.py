from __future__ import annotations

from logging.config import fileConfig
from typing import Any, cast

from alembic import context
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from src.config.settings import settings

# IMPORTANT
# Import all models here
from src.data.models.postgres import *  # noqa
from src.data.models.postgres.base import Base

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

assert settings.DATABASE_URL is not None

config.set_main_option(
    "sqlalchemy.url",
    settings.DATABASE_URL,
)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    config_section = config.get_section(config.config_ini_section)
    assert config_section is not None

    connectable = async_engine_from_config(
        cast(dict[str, Any], config_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    import asyncio

    asyncio.run(run_migrations_online())
