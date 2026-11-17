"""AD-1: `domene/` importerer aldri rammeverk eller ytre lag."""

import ast
from pathlib import Path

import prognos.domene

FORBUDTE = ("fastapi", "sqlalchemy", "prognos.api", "prognos.db")
DOMENE_PAKKE = "prognos.domene"
DOMENE_MAPPE = Path(prognos.domene.__file__).parent
UTENFOR_PAKKEN = "<relativ import utenfor pakken>"


def _er_forbudt(modul: str) -> bool:
    return any(modul == f or modul.startswith(f + ".") for f in FORBUDTE)


def pakke_for(fil: Path) -> str:
    """Pakken en fil hører til. For `__init__.py` er det pakken selv,
    for andre moduler pakken de ligger i; i begge tilfeller mappen."""
    deler = fil.parent.relative_to(DOMENE_MAPPE).parts
    return ".".join((DOMENE_PAKKE, *deler))


def forbudte_importer(kilde: str, pakke: str = DOMENE_PAKKE) -> list[str]:
    funn: list[str] = []
    for node in ast.walk(ast.parse(kilde)):
        if isinstance(node, ast.Import):
            funn += [a.name for a in node.names if _er_forbudt(a.name)]
        elif isinstance(node, ast.ImportFrom):
            if node.level:
                # Relativ import: løs opp mot filens egen pakke.
                deler = pakke.split(".")
                if node.level > len(deler):
                    funn.append(UTENFOR_PAKKEN)
                    continue
                basis = ".".join(deler[: len(deler) - (node.level - 1)])
                modul = f"{basis}.{node.module}" if node.module else basis
            else:
                modul = node.module or ""
            if _er_forbudt(modul):
                funn.append(modul)
            else:
                funn += [
                    f"{modul}.{a.name}" for a in node.names if _er_forbudt(f"{modul}.{a.name}")
                ]
    return funn


def test_domene_har_moduler() -> None:
    assert list(DOMENE_MAPPE.rglob("*.py"))


def test_pakke_for_fil() -> None:
    assert pakke_for(DOMENE_MAPPE / "__init__.py") == "prognos.domene"
    assert pakke_for(DOMENE_MAPPE / "feil.py") == "prognos.domene"
    assert pakke_for(DOMENE_MAPPE / "under" / "__init__.py") == "prognos.domene.under"
    assert pakke_for(DOMENE_MAPPE / "under" / "x.py") == "prognos.domene.under"


def test_domene_importerer_ingen_forbudte_moduler() -> None:
    brudd = {
        str(fil.relative_to(DOMENE_MAPPE)): funn
        for fil in DOMENE_MAPPE.rglob("*.py")
        if (funn := forbudte_importer(fil.read_text(encoding="utf-8"), pakke_for(fil)))
    }
    assert brudd == {}


def test_sjekken_fanger_forbudte_importer() -> None:
    kilde = "\n".join(
        [
            "import fastapi",
            "import sqlalchemy.orm",
            "from sqlalchemy.ext.asyncio import AsyncEngine",
            "from prognos.api.helse import ruter",
            "from prognos import db",
            "from ..db import modeller",
            "import pandas",
            "from prognos.domene import feil",
            "import prognos.dbx",
            "from ... import noe",
        ]
    )
    assert forbudte_importer(kilde) == [
        "fastapi",
        "sqlalchemy.orm",
        "sqlalchemy.ext.asyncio",
        "prognos.api.helse",
        "prognos.db",
        "prognos.db",
        UTENFOR_PAKKEN,
    ]


def test_sjekken_loeser_relative_importer_i_underpakke() -> None:
    kilde = "\n".join(
        [
            "from ..feil import DomeneFeil",
            "from ...db import modeller",
            "from ...api import helse",
        ]
    )
    assert forbudte_importer(kilde, "prognos.domene.under") == [
        "prognos.db",
        "prognos.api",
    ]
