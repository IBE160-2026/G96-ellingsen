"""Motor-fabrikk for SQLite."""

from pathlib import Path

from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine


def lag_motor(db_sti: Path) -> AsyncEngine:
    return create_async_engine(URL.create("sqlite+aiosqlite", database=str(Path(db_sti))))
