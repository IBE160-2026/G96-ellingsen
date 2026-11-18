"""Story 2.1: generatoren for syntetisk salgshistorikk med fasit (FR-23, FR-24, F9).

Forventningene er egne konstanter her, ikke verdier importert fra generatoren (R2).
"""

import ast
import json
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

import pytest

ROT = Path(__file__).resolve().parents[3]
TESTDATA = ROT / "testdata"
GENERATOR = TESTDATA / "generator.py"
CSV = "syntetisk.csv"
FASIT = "fasit.json"

OVERSKRIFT = "produkt_id,maaned,antall"
SISTE_MAANED = "2026-10"
ANTALL_LANGE = 20
LANG_LENGDE = 36
KORTE_LENGDER = [8, 15, 20, 26]
MIN_MED_TREND = 15
MIN_FLATE_MED_MYE_STOEY = 2
GRENSE_MYE_STOEY = 0.25
MIN_MED_SESONG = 3
GRENSE_SESONGSPENN = 0.4  # max − min i sesongprofilen
FASIT_TOPPNIVAA = {"seed", "siste_maaned", "produkter"}
FASITFELT = {
    "foerste_maaned",
    "antall_maaneder",
    "nivaa",
    "trend",
    "sesongprofil",
    "stoeynivaa",
}
TILLATTE_TREDJEPART = {"numpy"}
FORBUDTE = ("prognos", "backend")
MAANED = re.compile(r"^\d{4}-(0[1-9]|1[0-2])$")
PRODUKT_ID = re.compile(r"^P-\d{3}$")


def kjoer_generator(*argumenter: str) -> None:
    subprocess.run(
        [sys.executable, str(GENERATOR), *argumenter], check=True, cwd=ROT
    )


@pytest.fixture(scope="module")
def generert(tmp_path_factory: pytest.TempPathFactory) -> Path:
    mappe = tmp_path_factory.mktemp("generert")
    kjoer_generator("--mappe", str(mappe))
    return mappe


def les_rader(mappe: Path) -> list[tuple[str, str, int]]:
    tekst = (mappe / CSV).read_bytes().decode("utf-8")
    linjer = tekst.split("\n")
    assert linjer[0] == OVERSKRIFT
    assert linjer[-1] == ""
    rader = []
    for linje in linjer[1:-1]:
        produkt_id, maaned, antall = linje.split(",")
        rader.append((produkt_id, maaned, int(antall)))
    return rader


def les_fasit(mappe: Path) -> dict:
    return json.loads((mappe / FASIT).read_text(encoding="utf-8"))


def maaned_indeks(maaned: str) -> int:
    aar, mnd = maaned.split("-")
    return int(aar) * 12 + int(mnd) - 1


def serier(rader: list[tuple[str, str, int]]) -> dict[str, list[str]]:
    resultat: dict[str, list[str]] = defaultdict(list)
    for produkt_id, maaned, _ in rader:
        resultat[produkt_id].append(maaned)
    return resultat


# --- Determinisme (F9) ---


def test_samme_seed_gir_byte_identiske_filer(tmp_path: Path) -> None:
    a, b = tmp_path / "a", tmp_path / "b"
    kjoer_generator("--seed", "42", "--mappe", str(a))
    kjoer_generator("--mappe", str(b))
    for navn in (CSV, FASIT):
        assert (a / navn).read_bytes() == (b / navn).read_bytes()


def test_innsjekkede_filer_er_lik_ny_generering(generert: Path) -> None:
    for navn in (CSV, FASIT):
        assert (TESTDATA / navn).read_bytes() == (generert / navn).read_bytes()


def test_annen_seed_gir_annen_csv(tmp_path: Path, generert: Path) -> None:
    kjoer_generator("--seed", "7", "--mappe", str(tmp_path))
    assert (tmp_path / CSV).read_bytes() != (generert / CSV).read_bytes()
    assert les_fasit(tmp_path)["seed"] == 7


def test_uten_argumenter_skrives_filene_ved_siden_av_generatoren(
    tmp_path: Path, generert: Path
) -> None:
    kopi = tmp_path / "generator.py"
    kopi.write_bytes(GENERATOR.read_bytes())
    subprocess.run([sys.executable, str(kopi)], check=True, cwd=ROT)
    for navn in (CSV, FASIT):
        assert (tmp_path / navn).read_bytes() == (generert / navn).read_bytes()


def test_mappa_lages_hvis_den_mangler(tmp_path: Path) -> None:
    mappe = tmp_path / "ny" / "sti"
    kjoer_generator("--mappe", str(mappe))
    assert (mappe / CSV).is_file()
    assert (mappe / FASIT).is_file()


# --- CSV-format ---


def test_csv_bytes_er_utf8_uten_bom_med_lf(generert: Path) -> None:
    data = (generert / CSV).read_bytes()
    assert not data.startswith(b"\xef\xbb\xbf")
    assert b"\r" not in data
    assert data.endswith(b"\n")
    data.decode("utf-8")


def test_csv_rader_er_gyldige(generert: Path) -> None:
    rader = les_rader(generert)
    assert rader
    for produkt_id, maaned, antall in rader:
        assert PRODUKT_ID.match(produkt_id)
        assert MAANED.match(maaned)
        assert antall >= 0


def test_csv_er_sortert_uten_duplikater(generert: Path) -> None:
    rader = les_rader(generert)
    noekler = [(p, m) for p, m, _ in rader]
    assert noekler == sorted(noekler)
    assert len(set(noekler)) == len(noekler)


def test_csv_har_ingen_hull(generert: Path) -> None:
    for produkt_id, maaneder in serier(les_rader(generert)).items():
        indekser = [maaned_indeks(m) for m in maaneder]
        assert indekser == list(range(indekser[0], indekser[0] + len(indekser))), produkt_id


def test_antall_er_heltall_i_teksten(generert: Path) -> None:
    tekst = (generert / CSV).read_text(encoding="utf-8")
    for linje in tekst.splitlines()[1:]:
        assert re.fullmatch(r"\d+", linje.split(",")[2]), linje


# --- Innhold ---


def test_lengder_per_produkt(generert: Path) -> None:
    lengder = sorted(len(m) for m in serier(les_rader(generert)).values())
    assert lengder == sorted(KORTE_LENGDER + [LANG_LENGDE] * ANTALL_LANGE)


def test_alle_slutter_i_samme_siste_maaned(generert: Path) -> None:
    for produkt_id, maaneder in serier(les_rader(generert)).items():
        assert maaneder[-1] == SISTE_MAANED, produkt_id
    assert les_fasit(generert)["siste_maaned"] == SISTE_MAANED


def test_trend_og_flate_med_mye_stoey_ifoelge_fasiten(generert: Path) -> None:
    lange = [
        p
        for p in les_fasit(generert)["produkter"].values()
        if p["antall_maaneder"] == LANG_LENGDE
    ]
    assert len(lange) == ANTALL_LANGE
    med_trend = [p for p in lange if p["trend"] != 0]
    flate_med_mye_stoey = [
        p
        for p in lange
        if p["trend"] == 0 and p["stoeynivaa"] / p["nivaa"] >= GRENSE_MYE_STOEY
    ]
    assert len(med_trend) >= MIN_MED_TREND
    assert len(flate_med_mye_stoey) >= MIN_FLATE_MED_MYE_STOEY
    for p in flate_med_mye_stoey:
        assert p["sesongprofil"] == [1.0] * 12
    med_sesong = [
        p
        for p in lange
        if p["trend"] == 0
        and max(p["sesongprofil"]) - min(p["sesongprofil"]) >= GRENSE_SESONGSPENN
    ]
    assert len(med_sesong) >= MIN_MED_SESONG


def test_korte_produkter_har_trend(generert: Path) -> None:
    korte = [
        p
        for p in les_fasit(generert)["produkter"].values()
        if p["antall_maaneder"] in KORTE_LENGDER
    ]
    assert len(korte) == len(KORTE_LENGDER)
    assert all(p["trend"] != 0 for p in korte)


def test_csv_foelger_modellen_i_fasiten(generert: Path) -> None:
    """Rester mot (nivaa + trend·t)·sesongprofil[kalendermåned] skal se ut som
    støy med sd ≈ stoeynivaa. Rader klemt til 0 hoppes over."""
    produkter = les_fasit(generert)["produkter"]
    rester: dict[str, list[float]] = defaultdict(list)
    for produkt_id, maaned, antall in les_rader(generert):
        if antall == 0:
            continue
        p = produkter[produkt_id]
        t = maaned_indeks(maaned) - maaned_indeks(p["foerste_maaned"])
        kalendermaaned = int(maaned.split("-")[1]) - 1  # 0 = januar
        forventet = (p["nivaa"] + p["trend"] * t) * p["sesongprofil"][kalendermaaned]
        rester[produkt_id].append(antall - forventet)
    for produkt_id, r in rester.items():
        s = produkter[produkt_id]["stoeynivaa"]
        n = len(r)
        snitt = sum(r) / n
        spredning = (sum((x - snitt) ** 2 for x in r) / (n - 1)) ** 0.5
        assert abs(snitt) <= 3 * s / n**0.5 + 1, produkt_id
        assert 0.4 * s <= spredning <= 1.8 * s + 0.5, produkt_id


# --- Fasit ---


def test_fasit_stemmer_med_csv(generert: Path) -> None:
    fasit = les_fasit(generert)
    assert set(fasit) == FASIT_TOPPNIVAA
    assert fasit["seed"] == 42
    produkter = fasit["produkter"]
    for produkt_id, maaneder in serier(les_rader(generert)).items():
        assert produkter[produkt_id]["foerste_maaned"] == maaneder[0]
        assert produkter[produkt_id]["antall_maaneder"] == len(maaneder)
    assert set(produkter) == set(serier(les_rader(generert)))


def test_fasit_har_alle_felt_og_12_faktorer(generert: Path) -> None:
    for produkt_id, produkt in les_fasit(generert)["produkter"].items():
        assert set(produkt) == FASITFELT, produkt_id
        profil = produkt["sesongprofil"]
        assert len(profil) == 12, produkt_id
        assert abs(sum(profil) / 12 - 1) < 1e-4, produkt_id
        for verdi in [produkt["nivaa"], produkt["trend"], produkt["stoeynivaa"], *profil]:
            assert isinstance(verdi, (int, float))
            assert round(verdi, 4) == verdi


def test_fasit_json_formatering(generert: Path) -> None:
    data = (generert / FASIT).read_bytes()
    assert not data.startswith(b"\xef\xbb\xbf")
    assert b"\r" not in data
    tekst = data.decode("utf-8")
    forventet = json.dumps(json.loads(tekst), sort_keys=True, indent=2, ensure_ascii=False) + "\n"
    assert tekst == forventet


# --- Kildekoden ---


def test_sm_c1_kommentar_oeverst() -> None:
    foerste_linje = GENERATOR.read_text(encoding="utf-8").splitlines()[0]
    assert foerste_linje.startswith("#") and "SM-C1" in foerste_linje


def ulovlige_importer(kilde: str) -> list[str]:
    """Importer som verken er standardbibliotek eller numpy, eller som peker på backend."""
    funn: list[str] = []
    for node in ast.walk(ast.parse(kilde)):
        if isinstance(node, ast.Import):
            moduler = [a.name for a in node.names]
        elif isinstance(node, ast.ImportFrom):
            moduler = ["." * node.level + (node.module or "")]
        else:
            continue
        for modul in moduler:
            topp = modul.split(".")[0]
            if modul.startswith(".") or topp in FORBUDTE:
                funn.append(modul)
            elif topp not in sys.stdlib_module_names and topp not in TILLATTE_TREDJEPART:
                funn.append(modul)
    return funn


def test_generator_importerer_bare_stdlib_og_numpy() -> None:
    assert ulovlige_importer(GENERATOR.read_text(encoding="utf-8")) == []


def test_sjekken_fanger_ulovlige_importer() -> None:
    kilde = "\n".join(
        [
            "import json",
            "import numpy as np",
            "from pathlib import Path",
            "import prognos",
            "from prognos.domene import feil",
            "import backend.src",
            "from . import noe",
            "import pandas",
        ]
    )
    assert ulovlige_importer(kilde) == [
        "prognos",
        "prognos.domene",
        "backend.src",
        ".",
        "pandas",
    ]
