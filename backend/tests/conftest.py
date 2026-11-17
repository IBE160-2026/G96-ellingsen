"""Felles fixtures. Testene bruker alltid en midlertidig databasefil (AD-14)."""

from collections.abc import AsyncIterator
from pathlib import Path

import httpx
import pytest

from prognos.main import lag_app


@pytest.fixture
def db_sti(tmp_path: Path) -> Path:
    return tmp_path / "data" / "prognos.db"


@pytest.fixture
async def klient(db_sti: Path) -> AsyncIterator[httpx.AsyncClient]:
    app = lag_app(db_sti)
    async with app.router.lifespan_context(app):
        transport = httpx.ASGITransport(app=app)
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as k:
            yield k
