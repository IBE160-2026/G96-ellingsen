"""Kommandolinje: `python -m prognos --db STI --port N` (AD-14)."""

import argparse
from collections.abc import Sequence
from pathlib import Path

import uvicorn

from prognos.konstanter import STANDARD_DB_STI, STANDARD_PORT, STANDARD_VERT
from prognos.main import lag_app


def tolk_argumenter(argv: Sequence[str] | None = None) -> argparse.Namespace:
    tolker = argparse.ArgumentParser(prog="prognos", description="Start PROGNOS-backend.")
    tolker.add_argument(
        "--db", type=Path, default=STANDARD_DB_STI, help="Sti til SQLite-fila."
    )
    tolker.add_argument("--port", type=int, default=STANDARD_PORT, help="Port å lytte på.")
    return tolker.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> None:
    argumenter = tolk_argumenter(argv)
    uvicorn.run(lag_app(argumenter.db), host=STANDARD_VERT, port=argumenter.port)


if __name__ == "__main__":
    main()
