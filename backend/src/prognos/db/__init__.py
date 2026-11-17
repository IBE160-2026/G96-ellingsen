"""Databaselaget: modeller og motor."""

from prognos.db.modeller import Base, Skjemaversjon
from prognos.db.okt import lag_motor

__all__ = ["Base", "Skjemaversjon", "lag_motor"]
