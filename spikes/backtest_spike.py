# /// script
# requires-python = ">=3.10"
# dependencies = ["statsforecast", "pandas", "numpy"]
# ///
"""Spike: bekrefter backtest-oppsettet i beslutningsloggen.

- 3 syntetiske produkter, 36 måneder (sesong + trend + støy), fast seed
- AutoETS (season_length=12) og SeasonalNaive (season_length=12)
- Rullerende backtest: 6 opprinnelser, horisont 1, step 1
- 80 % prediksjonsintervall (level=[80]) -> P10/P90, nullgrense før dekning (FR-9)
- WAPE = sum|faktisk - P50| / sum faktisk, per produkt og totalt
- F7: total WAPE ETS < SeasonalNaive.  F8: total P10-P90-dekning for ETS i [65 %, 95 %]

Kjør: uv run spikes/backtest_spike.py              (seed 42, full utskrift)
      uv run spikes/backtest_spike.py --seeds 20   (seed 0-19, oppsummering)
Eksperiment, ikke produksjonskode.
"""

import argparse

import numpy as np
import pandas as pd
from statsforecast import StatsForecast
from statsforecast.models import AutoETS, SeasonalNaive

SEED = 42
N_MONTHS = 36
N_WINDOWS = 6
H = 1
LEVEL = 80

# (produkt_id, nivå, trend per mnd, sesongamplitude, støy-sd)
PRODUCTS = [
    ("P1", 200.0, 3.0, 40.0, 10.0),
    ("P2", 500.0, 6.0, 120.0, 30.0),
    ("P3", 80.0, 1.0, 20.0, 8.0),
]


def make_data(seed: int) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    t = np.arange(N_MONTHS)
    ds = pd.date_range("2023-01-01", periods=N_MONTHS, freq="MS")
    frames = []
    for pid, level, trend, amp, sd in PRODUCTS:
        y = level + trend * t + amp * np.sin(2 * np.pi * t / 12) + rng.normal(0, sd, N_MONTHS)
        frames.append(pd.DataFrame({"unique_id": pid, "ds": ds, "y": np.maximum(y, 0)}))
    return pd.concat(frames, ignore_index=True)


def run(seed: int, verbose: bool = True) -> tuple[float, float, float]:
    """Returnerer (WAPE ETS, WAPE SNaive, dekning ETS) totalt."""
    df = make_data(seed)
    sf = StatsForecast(
        models=[AutoETS(season_length=12), SeasonalNaive(season_length=12)],
        freq="MS",
        n_jobs=1,
    )
    cv = sf.cross_validation(df=df, h=H, n_windows=N_WINDOWS, step_size=1, level=[LEVEL])

    # Sjekk FR-13: 6 prognoser per produkt og modell, én per de siste 6 månedene
    counts = cv.groupby("unique_id").size()
    assert (counts == N_WINDOWS).all(), counts
    last6 = sorted(df["ds"].unique())[-N_WINDOWS:]
    assert sorted(cv["ds"].unique()) == list(last6)
    assert (cv["cutoff"] < cv["ds"]).all()

    models = {"ETS": "AutoETS", "SNaive": "SeasonalNaive"}
    neg_p10 = {}
    rows = []
    for label, col in models.items():
        lo, hi = f"{col}-lo-{LEVEL}", f"{col}-hi-{LEVEL}"
        neg_p10[label] = int((cv[lo] < 0).sum())
        p50 = cv[col].clip(lower=0)
        p10 = cv[lo].clip(lower=0)
        p90 = cv[hi].clip(lower=0)
        tmp = pd.DataFrame({
            "unique_id": cv["unique_id"],
            "abs_err": (cv["y"] - p50).abs(),
            "y": cv["y"],
            "inside": (cv["y"] >= p10) & (cv["y"] <= p90),
        })
        for pid, g in tmp.groupby("unique_id"):
            rows.append({
                "modell": label, "produkt": pid,
                "wape": g["abs_err"].sum() / g["y"].sum(),
                "dekning": g["inside"].mean(),
            })
        rows.append({
            "modell": label, "produkt": "TOTAL",
            "wape": tmp["abs_err"].sum() / tmp["y"].sum(),
            "dekning": tmp["inside"].mean(),
        })

    res = pd.DataFrame(rows)
    tot = res[res["produkt"] == "TOTAL"].set_index("modell")
    result = (tot.loc["ETS", "wape"], tot.loc["SNaive", "wape"], tot.loc["ETS", "dekning"])
    if not verbose:
        return result
    pd.set_option("display.float_format", "{:.3f}".format)
    print("\nBacktest-prognoser (utdrag):")
    print(cv.head(N_WINDOWS).to_string(index=False))
    print("\nWAPE og P10–P90-dekning:")
    print(res.pivot(index="produkt", columns="modell", values=["wape", "dekning"]).to_string())
    print(f"\nNegative P10 før nullgrense: {neg_p10}")

    f7 = tot.loc["ETS", "wape"] < tot.loc["SNaive", "wape"]
    cov = tot.loc["ETS", "dekning"]
    f8 = 0.65 <= cov <= 0.95
    print(f"\nF7 (ETS WAPE {tot.loc['ETS', 'wape']:.3f} < SNaive {tot.loc['SNaive', 'wape']:.3f}): "
          f"{'HOLDER' if f7 else 'HOLDER IKKE'}")
    print(f"F8 (ETS-dekning {cov:.1%} i [65 %, 95 %], n={N_WINDOWS * len(PRODUCTS)}): "
          f"{'HOLDER' if f8 else 'HOLDER IKKE'}")
    return result


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=0, help="kjør seed 0..N-1 og oppsummer")
    args = ap.parse_args()
    if not args.seeds:
        run(SEED)
        return
    print("seed  WAPE_ETS  WAPE_SNaive  dekning_ETS   F7   F8")
    f7n = f8n = 0
    covs = []
    for s in range(args.seeds):
        e, n, c = run(s, verbose=False)
        f7, f8 = e < n, 0.65 <= c <= 0.95
        f7n += f7
        f8n += f8
        covs.append(c)
        print(f"{s:>4}  {e:8.3f}  {n:11.3f}  {c:11.1%}  {'ja' if f7 else 'nei':>3}  {'ja' if f8 else 'nei':>3}")
    print(f"\nF7 holder: {f7n}/{args.seeds}   F8 holder: {f8n}/{args.seeds}   "
          f"snitt dekning ETS: {np.mean(covs):.1%}")


if __name__ == "__main__":
    main()
