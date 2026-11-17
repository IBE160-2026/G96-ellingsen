"""Faste verdier for backend. Ingen miljøvariabler eller konfigurasjonsfiler leses."""

from pathlib import Path

# backend/ regnet fra denne fila: backend/src/prognos/konstanter.py
BACKEND_MAPPE: Path = Path(__file__).resolve().parents[2]

STANDARD_DB_STI: Path = BACKEND_MAPPE / "data" / "prognos.db"

STANDARD_VERT: str = "127.0.0.1"
STANDARD_PORT: int = 8000

# Økes ved hver endring av databaseskjemaet (AD-13).
SKJEMAVERSJON: int = 1

GAMMELT_SKJEMA_MELDING: str = (
    "Databasefila har gammelt skjema. Slett backend/data/prognos.db og start på nytt."
)
