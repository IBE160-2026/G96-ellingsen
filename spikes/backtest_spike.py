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

Med --csv leses et ekte datasett (produkt_id,maaned,antall) i stedet, og oppsettet
følger beslutningsloggen fullt ut (retrotiltak 5 fra Epic 1):
- 30+ mnd: ETS og sesongnaiv. 18-29 mnd: bare sesongnaiv. Under 18 mnd: ingen backtest
- nullgrense, så avrunding halvt opp til heltall, før WAPE og dekning (AD-5)
- WAPE med faktisk sum 0 vises som «–» og holdes utenfor totalen
- total WAPE og dekning bare over produkter med backtest for begge modellene

Kjør: uv run spikes/backtest_spike.py              (seed 42, full utskrift)
      uv run spikes/backtest_spike.py --seeds 20   (seed 0-19, oppsummering)
      uv run spikes/backtest_spike.py --csv testdata/syntetisk.csv
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


MIN_ETS = 30       # 24 mnd trening + 6 opprinnelser
MIN_BASELINE = 18  # 12 mnd trening + 6 opprinnelser


def read_csv(path: str) -> pd.DataFrame:
    raw = pd.read_csv(path, dtype={"produkt_id": str, "maaned": str, "antall": int})
    return pd.DataFrame({
        "unique_id": raw["produkt_id"],
        "ds": pd.to_datetime(raw["maaned"] + "-01"),
        "y": raw["antall"].astype(float),
    })


def round_half_up(x: pd.Series) -> pd.Series:
    """Nullgrense og så avrunding halvt opp til heltall (AD-5)."""
    return np.floor(x.clip(lower=0) + 0.5)


def backtest(df: pd.DataFrame, models: list) -> pd.DataFrame:
    sf = StatsForecast(models=models, freq="MS", n_jobs=1)
    cv = sf.cross_validation(df=df, h=H, n_windows=N_WINDOWS, step_size=1, level=[LEVEL])
    # FR-13: 6 prognoser per produkt, én for hver av de siste 6 månedene, opprinnelse før måneden
    counts = cv.groupby("unique_id").size()
    assert (counts == N_WINDOWS).all(), counts
    for pid, g in cv.groupby("unique_id"):
        last6 = sorted(df.loc[df["unique_id"] == pid, "ds"])[-N_WINDOWS:]
        assert sorted(g["ds"]) == list(last6), pid
    assert (cv["cutoff"] < cv["ds"]).all()
    return cv


def score(cv: pd.DataFrame, col: str) -> pd.DataFrame:
    """Avrundede P10/P50/P90 og treff per prognose for én modell."""
    p50 = round_half_up(cv[col])
    p10 = round_half_up(cv[f"{col}-lo-{LEVEL}"])
    p90 = round_half_up(cv[f"{col}-hi-{LEVEL}"])
    return pd.DataFrame({
        "unique_id": cv["unique_id"].values,
        "ds": cv["ds"].values,
        "y": cv["y"].values,
        "p10": p10.values, "p50": p50.values, "p90": p90.values,
        "abs_err": (cv["y"] - p50).abs().values,
        "inside": ((cv["y"] >= p10) & (cv["y"] <= p90)).values,
        "neg_p10": (cv[f"{col}-lo-{LEVEL}"] < 0).values,
    })


def per_product(s: pd.DataFrame) -> pd.DataFrame:
    g = s.groupby("unique_id")
    out = pd.DataFrame({"sum_y": g["y"].sum(), "sum_err": g["abs_err"].sum(),
                        "treff": g["inside"].sum(), "n": g.size()})
    out["wape"] = np.where(out["sum_y"] > 0, out["sum_err"] / out["sum_y"].where(out["sum_y"] > 0), np.nan)
    out["dekning"] = out["treff"] / out["n"]
    return out


def run_csv(path: str) -> None:
    df = read_csv(path)
    lengths = df.groupby("unique_id").size()
    both_ids = lengths[lengths >= MIN_ETS].index
    base_ids = lengths[lengths >= MIN_BASELINE].index
    none_ids = lengths[lengths < MIN_BASELINE].index

    cv_both = backtest(df[df["unique_id"].isin(both_ids)],
                       [AutoETS(season_length=12), SeasonalNaive(season_length=12)])
    only_base = base_ids.difference(both_ids)
    cv_base = backtest(df[df["unique_id"].isin(only_base)], [SeasonalNaive(season_length=12)])

    ets = score(cv_both, "AutoETS")
    sn_both = score(cv_both, "SeasonalNaive")
    sn_only = score(cv_base, "SeasonalNaive")

    e = per_product(ets)
    n = per_product(pd.concat([sn_both, sn_only]))

    def fmt_w(x: float) -> str:
        return "–" if np.isnan(x) else f"{x:.3f}"

    print(f"Datasett: {path}  ({len(lengths)} produkter, {len(df)} rader)")
    print(f"ETS + sesongnaiv (30+ mnd): {len(both_ids)}  bare sesongnaiv (18–29): "
          f"{list(only_base)}  ingen backtest (<18): {list(none_ids)}")
    print("\nprodukt  mnd  WAPE_ETS  WAPE_SN  dekn_ETS  dekn_SN  ETS taper")
    for pid in lengths.index:
        if pid in none_ids:
            print(f"{pid:7}  {lengths[pid]:>3}  ingen backtest")
            continue
        ew = e.loc[pid, "wape"] if pid in e.index else np.nan
        nw = n.loc[pid, "wape"]
        ed = f"{e.loc[pid, 'dekning']:7.1%}" if pid in e.index else "      –"
        loses = "ja" if pid in e.index and not np.isnan(ew) and ew > nw else ""
        print(f"{pid:7}  {lengths[pid]:>3}  {fmt_w(ew):>8}  {fmt_w(nw):>7}  {ed:>8}  "
              f"{n.loc[pid, 'dekning']:7.1%}  {loses}")

    # Totaler: bare produkter med backtest for begge modellene. WAPE-totalen hopper i tillegg
    # over produkter med faktisk sum 0, og dekningen regnes over de samme produktene.
    total_ids = [p for p in both_ids if e.loc[p, "sum_y"] > 0]
    et, nt = e.loc[total_ids], n.loc[total_ids]
    wape_e = et["sum_err"].sum() / et["sum_y"].sum()
    wape_n = nt["sum_err"].sum() / nt["sum_y"].sum()
    cov_e = et["treff"].sum() / et["n"].sum()
    cov_n = nt["treff"].sum() / nt["n"].sum()
    print(f"\nTotalt over {len(total_ids)} produkter ({int(et['n'].sum())} prognoser per modell):")
    print(f"  WAPE   ETS {wape_e:.3f}   sesongnaiv {wape_n:.3f}")
    print(f"  Dekning ETS {cov_e:.1%} ({int(et['treff'].sum())}/{int(et['n'].sum())})   "
          f"sesongnaiv {cov_n:.1%} ({int(nt['treff'].sum())}/{int(nt['n'].sum())})")
    print(f"  ETS taper i {sum(1 for p in total_ids if e.loc[p, 'wape'] > n.loc[p, 'wape'])} av "
          f"{len(total_ids)} produkter")
    print(f"  Negative P10 før nullgrense: ETS {int(ets['neg_p10'].sum())}, "
          f"sesongnaiv {int(pd.concat([sn_both, sn_only])['neg_p10'].sum())}")

    f7 = wape_e < wape_n
    f8 = 0.65 <= cov_e <= 0.95
    print(f"\nF7 (ETS WAPE {wape_e:.3f} < sesongnaiv {wape_n:.3f}): {'HOLDER' if f7 else 'HOLDER IKKE'}")
    print(f"F8 (ETS-dekning {cov_e:.1%} i [65 %, 95 %]): {'HOLDER' if f8 else 'HOLDER IKKE'}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=0, help="kjør seed 0..N-1 og oppsummer")
    ap.add_argument("--csv", help="les produkt_id,maaned,antall fra fil i stedet for spike-data")
    args = ap.parse_args()
    if args.csv:
        run_csv(args.csv)
        return
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
