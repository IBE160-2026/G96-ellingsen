"""Repohygiene og README (NFR-1, NFR-9)."""

import subprocess
from pathlib import Path, PurePosixPath

import pytest

ROT = Path(__file__).resolve().parents[2]

README_KOMMANDOER = [
    "uv sync --frozen",
    "npm ci",
    "npx playwright install chromium",
    "uv run uvicorn prognos.main:app --port 8000",
    "npm run dev",
    "uv run pytest",
    "npm test",
    "npx playwright test",
]


def _readme() -> str:
    return (ROT / "README.md").read_text(encoding="utf-8")


@pytest.mark.parametrize("kommando", README_KOMMANDOER)
def test_readme_har_kommandoen(kommando: str) -> None:
    assert kommando in _readme()


@pytest.mark.parametrize("versjon", ["3.12", "0.13.x", "22.12"])
def test_readme_har_versjonene(versjon: str) -> None:
    assert versjon in _readme()


def test_env_example_finnes() -> None:
    tekst = (ROT / ".env.example").read_text(encoding="utf-8")
    assert "ingen miljøvariabler" in tekst


def _sporede_filer() -> list[str]:
    if not (ROT / ".git").exists():
        pytest.skip("Rotmappa er ikke et git-repo (f.eks. nedlastet som ZIP)")
    ut = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=ROT,
        capture_output=True,
        check=True,
    )
    return [f for f in ut.stdout.decode("utf-8").split("\0") if f]


def test_ingen_db_eller_env_filer_i_git() -> None:
    filer = _sporede_filer()
    assert ".env.example" in filer
    db_endelser = (".db", ".db-journal", ".db-wal", ".db-shm", ".sqlite", ".sqlite3")
    forbudte = [
        f
        for f in filer
        if PurePosixPath(f).name.endswith(db_endelser)
        or (
            PurePosixPath(f).name.startswith(".env")
            and not PurePosixPath(f).name.endswith(".example")
        )
    ]
    assert forbudte == []
