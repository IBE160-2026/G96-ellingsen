from pathlib import Path
from typing import Any

import pytest

import prognos.__main__ as cli
from prognos.konstanter import STANDARD_DB_STI, STANDARD_PORT


def test_standardverdier() -> None:
    argumenter = cli.tolk_argumenter([])
    assert argumenter.db == STANDARD_DB_STI
    assert argumenter.port == STANDARD_PORT


def test_main_bruker_oppgitt_db_og_port(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    kall: dict[str, Any] = {}

    def falsk_run(app: Any, **kwargs: Any) -> None:
        kall["app"] = app
        kall.update(kwargs)

    monkeypatch.setattr(cli.uvicorn, "run", falsk_run)
    sti = tmp_path / "annen.db"

    cli.main(["--db", str(sti), "--port", "8011"])

    assert kall["app"].state.db_sti == sti
    assert kall["host"] == "127.0.0.1"
    assert kall["port"] == 8011
    assert not sti.exists()


def test_standard_db_sti_peker_til_backend_data() -> None:
    import prognos

    backend = Path(prognos.__file__).resolve().parents[2]
    assert STANDARD_DB_STI == backend / "data" / "prognos.db"
    assert (backend / "pyproject.toml").is_file()
