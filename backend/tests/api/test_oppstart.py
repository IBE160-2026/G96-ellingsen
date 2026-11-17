import sqlite3
from contextlib import closing
from pathlib import Path

import pytest

from prognos.konstanter import GAMMELT_SKJEMA_MELDING, SKJEMAVERSJON
from prognos.main import lag_app
from prognos.oppstart import GammeltSkjemaFeil


async def _start(db_sti: Path) -> None:
    app = lag_app(db_sti)
    async with app.router.lifespan_context(app):
        pass


def _versjoner(db_sti: Path) -> list[int]:
    with closing(sqlite3.connect(db_sti)) as forbindelse:
        return [r[0] for r in forbindelse.execute("SELECT versjon FROM skjemaversjon")]


def _lag_versjonstabell(db_sti: Path, versjoner: list[int]) -> None:
    db_sti.parent.mkdir(parents=True)
    with closing(sqlite3.connect(db_sti)) as forbindelse:
        forbindelse.execute("CREATE TABLE skjemaversjon (versjon INTEGER PRIMARY KEY)")
        forbindelse.executemany(
            "INSERT INTO skjemaversjon (versjon) VALUES (?)", [(v,) for v in versjoner]
        )
        forbindelse.commit()


async def _forvent_gammelt_skjema(db_sti: Path) -> None:
    with pytest.raises(GammeltSkjemaFeil) as feil:
        await _start(db_sti)
    assert str(feil.value) == GAMMELT_SKJEMA_MELDING


async def test_foerste_oppstart_oppretter_mappe_fil_og_versjon(db_sti: Path) -> None:
    assert not db_sti.parent.exists()
    await _start(db_sti)
    assert db_sti.is_file()
    assert _versjoner(db_sti) == [SKJEMAVERSJON]


async def test_ny_oppstart_mot_samme_fil_gaar_fint(db_sti: Path) -> None:
    await _start(db_sti)
    await _start(db_sti)
    assert _versjoner(db_sti) == [SKJEMAVERSJON]


async def test_vakten_stopper_naar_skjemaversjon_mangler(db_sti: Path) -> None:
    db_sti.parent.mkdir(parents=True)
    with closing(sqlite3.connect(db_sti)) as forbindelse:
        forbindelse.execute("CREATE TABLE gammel (id INTEGER PRIMARY KEY)")
        forbindelse.commit()

    await _forvent_gammelt_skjema(db_sti)


async def test_vakten_stopper_ved_feil_versjon(db_sti: Path) -> None:
    _lag_versjonstabell(db_sti, [SKJEMAVERSJON + 1])
    await _forvent_gammelt_skjema(db_sti)
    assert _versjoner(db_sti) == [SKJEMAVERSJON + 1]


async def test_vakten_stopper_ved_tom_versjonstabell(db_sti: Path) -> None:
    _lag_versjonstabell(db_sti, [])
    await _forvent_gammelt_skjema(db_sti)
    assert _versjoner(db_sti) == []


async def test_vakten_stopper_ved_to_versjonsrader(db_sti: Path) -> None:
    _lag_versjonstabell(db_sti, [SKJEMAVERSJON, SKJEMAVERSJON + 1])
    await _forvent_gammelt_skjema(db_sti)
    assert _versjoner(db_sti) == [SKJEMAVERSJON, SKJEMAVERSJON + 1]


def test_meldingen_er_den_faste_teksten() -> None:
    assert GAMMELT_SKJEMA_MELDING == (
        "Databasefila har gammelt skjema. Slett backend/data/prognos.db og start på nytt."
    )
