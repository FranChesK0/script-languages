from loguru import logger
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from core import settings

engine = create_async_engine(settings.DATABASE_CONNECTION)
session_maker = async_sessionmaker(engine, expire_on_commit=False, autoflush=False)


class Model(DeclarativeBase):
    """Base class for database models."""

    pass


async def _create_table() -> None:
    """Create database tables."""
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)
    logger.warning("Database successfully created")


async def _drop_table() -> None:
    """Drop database tables."""
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)
    logger.warning("Database successfully dropped")


async def setup_db() -> None:
    """Setup database tables."""
    await _drop_table()
    await _create_table()
    logger.info("Database successfully setup")
