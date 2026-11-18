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

## Spike på nytt mot det syntetiske datasettet (2026-11-18)

Retrotiltak 5 fra Epic 1. Spiken fra 2026-11-14 brukte et forenklet spike-datasett. Her kjøres den mot det ekte syntetiske datasettet fra Story 2.1 (`testdata/syntetisk.csv`, seed 42), med hele oppsettet fra beslutningsloggen. Datasettet, seeden, generatoren og intervallnivået er ikke endret (SM-C1).

```powershell
uv run spikes/backtest_spike.py --csv testdata/syntetisk.csv
```

### Oppsett

- **Data:** 24 produkter og 789 rader. 20 produkter har 36 måneder, og P-121–P-124 har 8, 15, 20 og 26 måneder. Alle seriene ender i 2026-10.
- **Hvilke produkter får backtest** (*Backtest*, *Backtest for 12–17 mnd*): de 20 produktene med 30+ mnd får ETS og sesongnaiv. P-123 og P-124 (18–29 mnd) får bare sesongnaiv. P-121 og P-122 (under 18 mnd) får ingen backtest.
- **Backtest:** som før, `cross_validation(h=1, n_windows=6, step_size=1, level=[80])`, med kontrollen av FR-13 per produkt.
- **Nullgrense og avrunding** (*Avrunding til heltall*, AD-5): P10, P50 og P90 settes først til minst 0, og rundes så halvt opp til heltall. WAPE og dekning regnes bare fra de avrundede verdiene.
- **Totaler** (*Total WAPE*, *Intervalldekning og sortering*, *WAPE når faktisk salg er 0*): total WAPE og dekning regnes for begge modellene over de samme 20 produktene med backtest for begge modellene. Produkter med faktisk sum 0 i backtestmånedene ville vært holdt utenfor, men ingen produkter har det.
- **Versjoner:** statsforecast 2.1.1, pandas 2.3.3, numpy 2.5.5, Python 3.12.

### Resultat

| | ETS | Sesongnaiv |
|---|---|---|
| Total WAPE (20 produkter) | **0,106** | 0,140 |
| Total P10–P90-dekning (120 prognoser) | **80,8 %** (97/120) | 85,0 % (102/120) |

- **F7 holder:** ETS har lavere total WAPE (0,106) enn sesongnaiv (0,140).
- **F8 holder:** ETS-dekningen er 80,8 %, godt innenfor 65–95 %. Grensene ligger 19 treff under og 17 treff over.
- **ETS taper** mot sesongnaiv for 6 av 20 produkter: P-104, P-107, P-109, P-113, P-115 og P-119.
- De flate produktene med mye støy har høyest WAPE: P-116 med 0,360 og P-117 med 0,457 for ETS.
- **Bare baseline:** P-123 har WAPE 0,209 og dekning 33,3 %. P-124 har WAPE 0,151 og dekning 50,0 %.
- **Negative P10 før nullgrensen:** 0 for ETS og 2 for sesongnaiv. Nullgrensen ble altså brukt.

Utskriften per produkt får du ved å kjøre kommandoen over.

### Kan sjekkene slå ut? (R2)

Spiken er også kjørt på kopier av datasettet som er brukket med vilje. Kopiene ligger bare i en midlertidig mappe og er ikke sjekket inn.

- **Hver serie er de første 12 månedene gjentatt** (perfekt sesong uten støy): F7 holder ikke, fordi begge modellene får WAPE 0,000. F8 holder ikke, fordi dekningen blir 100 %. Begge sjekkene kan altså slå ut.
- **Månedene er stokket innenfor hver serie:** F7 og F8 holder fortsatt. Sesongnaiv blir enda dårligere på ren støy.
- **De siste 6 månedene er ganget med 3:** F8 holder så vidt, med 65,8 %.

### Vurdering

- **Begge kriteriene holder på datasettet som skal brukes,** uten justering. Det xfail-merket i beslutningsloggen trenges trolig ikke i Story 5.4. Dette gjelder hvis kjernen regner likt med spiken.
- **Dekningen havner nær det nominelle nivået på 80 %.** Med 120 prognoser er standardavviket omtrent 3,7 prosentpoeng, slik spiken fra 2026-11-14 forutså. Mistanken om for smale ETS-intervaller fra den gangen bekreftes ikke på dette datasettet.
- **6 av 20 produkter får flagget *ETS taper*.** Flagget og visningen av begge WAPE-tallene i Epic 5 og 6 får dermed ekte tilfeller å testes mot.
- **Resultatet er ikke en fasit for kjernen.** Story 5.1–5.4 skal regne ut WAPE og dekning selv. Fasittestene der skal sammenligne med uavhengige konstanter (R2), ikke med tallene fra denne spiken.
