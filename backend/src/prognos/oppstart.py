"""Oppstart: versjonsvakt, tabelloppretting og lifespan (AD-13)."""

import logging
from collections.abc import AsyncIterator, Callable
from contextlib import AbstractAsyncContextManager, asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from sqlalchemy import Connection, inspect, select
from sqlalchemy.ext.asyncio import AsyncEngine

from prognos.db import Base, Skjemaversjon, lag_motor
from prognos.konstanter import GAMMELT_SKJEMA_MELDING, SKJEMAVERSJON

logger = logging.getLogger(__name__)


class GammeltSkjemaFeil(RuntimeError):
    """Databasefila har et skjema som ikke stemmer med `SKJEMAVERSJON`."""


def _tabellnavn(forbindelse: Connection) -> list[str]:
    return inspect(forbindelse).get_table_names()


async def klargjoer_database(motor: AsyncEngine) -> None:
    """Kjør versjonsvakten før `create_all`.

    Tom fil: tabeller og `SKJEMAVERSJON` opprettes i samme transaksjon.
    Tabeller uten `skjemaversjon` eller med annen verdi: `GammeltSkjemaFeil`.
    """
    async with motor.begin() as forbindelse:
        tabeller = await forbindelse.run_sync(_tabellnavn)

        if not tabeller:
            await forbindelse.run_sync(Base.metadata.create_all)
            await forbindelse.execute(
                Skjemaversjon.__table__.insert().values(versjon=SKJEMAVERSJON)
            )
            logger.info("Opprettet ny database med skjemaversjon %s.", SKJEMAVERSJON)
            return

        if Skjemaversjon.__tablename__ not in tabeller:
            raise GammeltSkjemaFeil(GAMMELT_SKJEMA_MELDING)

        versjoner = (await forbindelse.execute(select(Skjemaversjon.versjon))).scalars().all()
        if list(versjoner) != [SKJEMAVERSJON]:
            raise GammeltSkjemaFeil(GAMMELT_SKJEMA_MELDING)

        await forbindelse.run_sync(Base.metadata.create_all)


def lag_lifespan(
    db_sti: Path,
) -> Callable[[FastAPI], AbstractAsyncContextManager[None]]:
    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        db_sti.parent.mkdir(parents=True, exist_ok=True)
        motor = lag_motor(db_sti)
        try:
            try:
                await klargjoer_database(motor)
            except GammeltSkjemaFeil:
                logger.error(GAMMELT_SKJEMA_MELDING)
                raise
            app.state.motor = motor
            logger.info("Database klar: %s", db_sti)
            yield
        finally:
            await motor.dispose()

    return lifespan
