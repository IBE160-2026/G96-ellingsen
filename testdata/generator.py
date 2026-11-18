# SM-C1: Parameterne trekkes fra rng innenfor faste intervaller per kategori.
# Trend, sesong og støy settes aldri produkt for produkt for å få bedre WAPE,
# og de flate seriene med mye støy beholdes. Seed 42 er låst. Feiler F7 eller
# F8 senere på dette datasettet, føres det som funn i issues.md og testen merkes
# xfail(strict=True). Data, seed og intervaller endres ikke for å få en test grønn.
"""Generator for syntetisk salgshistorikk med fasit (FR-23, FR-24, F9).

Kjøres fra rotmappa med:

    uv run --project backend python testdata/generator.py [--seed 42] [--mappe STI]

Skriver `syntetisk.csv` og `fasit.json`. Modell per måned:

    y = (nivaa + trend·t) · sesongprofil[kalendermåned] + støy,  støy ~ N(0, stoeynivaa)
    antall = max(0, round(y))
"""

import argparse
import json
import math
from pathlib import Path

import numpy as np

SISTE_MAANED = "2026-10"
STANDARD_SEED = 42
CSV_NAVN = "syntetisk.csv"
FASIT_NAVN = "fasit.json"
DESIMALER = 4

# Faste intervaller per kategori (SM-C1). Støynivået er en andel av nivået.
KATEGORIER: dict[str, dict[str, tuple[float, float]]] = {
    "trend": {
        "nivaa": (40.0, 120.0),
        "trend": (0.3, 2.0),
        "sesongamplitude": (0.1, 0.3),
        "stoeyandel": (0.05, 0.15),
    },
    "flat": {
        "nivaa": (20.0, 60.0),
        "trend": (0.0, 0.0),
        "sesongamplitude": (0.0, 0.0),
        "stoeyandel": (0.3, 0.5),
    },
    "sesong": {
        "nivaa": (40.0, 120.0),
        "trend": (0.0, 0.0),
        "sesongamplitude": (0.3, 0.5),
        "stoeyandel": (0.08, 0.15),
    },
}

# (produkt_id, kategori, antall måneder), i den rekkefølgen parameterne trekkes.
PRODUKTER: list[tuple[str, str, int]] = (
    [(f"P-{101 + i}", "trend", 36) for i in range(15)]
    + [(f"P-{116 + i}", "flat", 36) for i in range(2)]
    + [(f"P-{118 + i}", "sesong", 36) for i in range(3)]
    + [
        ("P-121", "trend", 8),
        ("P-122", "trend", 15),
        ("P-123", "trend", 20),
        ("P-124", "trend", 26),
    ]
)


def maaned_til_indeks(maaned: str) -> int:
    aar, mnd = maaned.split("-")
    return int(aar) * 12 + int(mnd) - 1


def indeks_til_maaned(indeks: int) -> str:
    return f"{indeks // 12:04d}-{indeks % 12 + 1:02d}"


def _trekk(rng: np.random.Generator, intervall: tuple[float, float]) -> float:
    lav, hoey = intervall
    return round(float(rng.uniform(lav, hoey)), DESIMALER)


def sesongprofil(rng: np.random.Generator, amplitude: float) -> list[float]:
    """12 faktorer (januar–desember) med snitt 1: sinus med tilfeldig fase."""
    fase = float(rng.uniform(0.0, 12.0))
    return [
        round(1.0 + amplitude * math.sin(2.0 * math.pi * (m - fase) / 12.0), DESIMALER)
        for m in range(12)
    ]


def generer(seed: int) -> tuple[list[tuple[str, str, int]], dict]:
    rng = np.random.default_rng(seed)
    siste = maaned_til_indeks(SISTE_MAANED)
    rader: list[tuple[str, str, int]] = []
    produkter: dict[str, dict] = {}

    for produkt_id, kategori, antall_maaneder in PRODUKTER:
        intervaller = KATEGORIER[kategori]
        nivaa = _trekk(rng, intervaller["nivaa"])
        trend = _trekk(rng, intervaller["trend"])
        amplitude = _trekk(rng, intervaller["sesongamplitude"])
        stoeynivaa = round(nivaa * _trekk(rng, intervaller["stoeyandel"]), DESIMALER)
        profil = sesongprofil(rng, amplitude)
        stoey = rng.normal(0.0, stoeynivaa, antall_maaneder)

        foerste = siste - antall_maaneder + 1
        for t in range(antall_maaneder):
            indeks = foerste + t
            y = (nivaa + trend * t) * profil[indeks % 12] + float(stoey[t])
            rader.append((produkt_id, indeks_til_maaned(indeks), max(0, int(round(y)))))

        produkter[produkt_id] = {
            "foerste_maaned": indeks_til_maaned(foerste),
            "antall_maaneder": antall_maaneder,
            "nivaa": nivaa,
            "trend": trend,
            "sesongprofil": profil,
            "stoeynivaa": stoeynivaa,
        }

    rader.sort(key=lambda r: (r[0], r[1]))
    fasit = {"seed": seed, "siste_maaned": SISTE_MAANED, "produkter": produkter}
    return rader, fasit


def skriv(mappe: Path, seed: int) -> None:
    rader, fasit = generer(seed)
    mappe.mkdir(parents=True, exist_ok=True)

    linjer = ["produkt_id,maaned,antall"] + [f"{p},{m},{a}" for p, m, a in rader]
    with open(mappe / CSV_NAVN, "w", encoding="utf-8", newline="") as f:
        f.write("\n".join(linjer) + "\n")

    with open(mappe / FASIT_NAVN, "w", encoding="utf-8", newline="") as f:
        json.dump(fasit, f, sort_keys=True, indent=2, ensure_ascii=False)
        f.write("\n")


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--seed", type=int, default=STANDARD_SEED)
    parser.add_argument("--mappe", type=Path, default=Path(__file__).resolve().parent)
    argumenter = parser.parse_args(argv)
    skriv(argumenter.mappe, argumenter.seed)


if __name__ == "__main__":
    main()
