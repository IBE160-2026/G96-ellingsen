# Teknisk research

## Spike: backtest-oppsettet (2026-11-14)

Spiken sjekker om backtest-oppsettet i beslutningsloggen (*Backtest*, *Intervaller*) kan oppfylle F7 og F8, før implementeringen begynner. Den svarer på åpent spørsmål 1 i PRD §10.

Skript: [spikes/backtest_spike.py](../../spikes/backtest_spike.py)

```sh
uv run spikes/backtest_spike.py              # seed 42, full utskrift
uv run spikes/backtest_spike.py --seeds 20   # seed 0–19, oppsummering
```

### Oppsett

- **Data:** 3 syntetiske produkter med 36 måneder hver, laget som nivå + lineær trend + sinus-sesong (12 mnd) + normalfordelt støy, og satt til minst 0. Hvert produkt har sitt eget nivå, sin egen trend, sesongamplitude og støy. Dette er et forenklet spike-datasett, ikke datasettet fra FR-23–FR-25: det har ingen flate serier og ingen korte historikker.
- **Modeller:** `AutoETS(season_length=12)` og `SeasonalNaive(season_length=12)` fra statsforecast.
- **Backtest:** `cross_validation(h=1, n_windows=6, step_size=1, level=[80])`. Det gir 6 opprinnelser, horisont 1 måned og step 1. Skriptet sjekker at hvert produkt får 6 prognoser per modell, én for hver av de siste 6 månedene, og at hver opprinnelse ligger før måneden den prognoserer (FR-13).
- **Nullgrense:** P10, P50 og P90 settes til minst 0 før WAPE og dekning regnes ut (FR-9, FR-15).
- **WAPE:** Σ|faktisk − P50| / Σ faktisk, per produkt og totalt over alle produktene (FR-14).
- **Dekning:** andelen faktiske verdier der P10 ≤ faktisk ≤ P90, per produkt og totalt (FR-15).
- **Versjoner:** statsforecast 2.1.1, pandas 2.3.3, numpy 2.5.4, Python 3.12.

### Resultat med seed 42

| Produkt | WAPE ETS | WAPE sesongnaiv | Dekning ETS | Dekning sesongnaiv |
|---|---|---|---|---|
| P1 | 0,040 | 0,137 | 83,3 % | 100,0 % |
| P2 | 0,081 | 0,096 | 50,0 % | 83,3 % |
| P3 | 0,122 | 0,137 | 50,0 % | 50,0 % |
| **Totalt** | **0,074** | **0,112** | **61,1 %** | **77,8 %** |

- **F7 holder:** ETS har lavere total WAPE (0,074) enn sesongnaiv (0,112).
- **F8 holder ikke:** ETS-dekningen er 61,1 %, altså 11 av 18 treff, og det er under grensen på 65 %.
- Ingen P10-verdier var negative før nullgrensen, så nullgrensen ble ikke brukt.

### Resultat over 20 seeds (0–19)

| | Holder | Feiler |
|---|---|---|
| F7 | 18 av 20 | seed 12 (0,072 mot 0,069) og seed 13 (0,094 mot 0,084) |
| F8 | 18 av 20 | seed 2 (100 %) og seed 10 (61,1 %) |

ETS-dekningen var i snitt 76,7 % og lå mellom 61,1 % og 100 %. ETS hadde lavere WAPE enn sesongnaiv i alle seeds unntatt to, og forskjellen var vanligvis stor: WAPE lå rundt 0,05–0,09 for ETS og 0,10–0,14 for sesongnaiv.

### Vurdering

- **Oppsettet virker.** statsforecast gir backtesten som beslutningsloggen beskriver direkte, med P10 og P90 fra `level=[80]`. Beslutningsloggen trenger ikke endres.
- **F7 er robust.** Med trend i dataene slår ETS sesongnaiv nesten alltid, og med god margin. Det stemmer med beslutningen *Syntetiske data*.
- **F8 er støyfølsomt med få produkter.** Med 18 prognoser flytter hvert treff dekningen 5,6 prosentpoeng. Ett treff mindre enn 12 gir 61 %, og alle 18 gir 100 %. Begge grensene kan derfor brytes av tilfeldigheter. Med det virkelige datasettet på rundt 20 produkter blir det rundt 120 prognoser, og da svinger dekningen mindre. Til sammenligning gir 80 % dekning med 120 prognoser et standardavvik på omtrent 3,7 prosentpoeng, mot 9,4 med 18.
- **ETS-intervallene kan være for smale.** Med seed 42 hadde to av tre produkter 50 % dekning, men snittet over 20 seeds (76,7 %) ligger nær det nominelle nivået på 80 %. Spiken gir ikke grunn til å endre intervallnivået, men det bør sjekkes på det virkelige datasettet.
- **Observasjon:** for P1 ved opprinnelsen 2025-07 er ETS-prognosen lik siste faktiske verdi. AutoETS valgte trolig en modell uten sesong ved den opprinnelsen. Modellvalget kan altså variere mellom opprinnelsene.
- **Seed:** spiken kan ikke brukes til å velge seed for det virkelige datasettet. Seeden er låst til 42 i beslutningsloggen (*Seed for syntetisk datasett*), og F7 og F8 må sjekkes på nytt når datasettet er generert.
