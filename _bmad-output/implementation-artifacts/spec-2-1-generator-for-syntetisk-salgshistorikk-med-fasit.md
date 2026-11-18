---
title: 'Story 2.1: Generator for syntetisk salgshistorikk med fasit'
type: 'feature'
created: '2026-11-18'
status: 'done'
baseline_commit: '603eef73fff58dd70c5a5d740ac122e345bb923f'
route: 'dispatch'
review_loop_iteration: 0
context:
  - '{project-root}/_bmad-output/implementation-artifacts/epic-2-context.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Vi har ingen salgshistorikk der svaret er kjent. Prognosen (Epic 4), backtesten (Epic 5) og seedingen ved første oppstart (Story 3.7) trenger en fast, gyldig CSV og en fasit med trend, sesong og støy per produkt (FR-23, FR-24, F9).

**Approach:** Lag `testdata/generator.py` (bare standardbibliotek + numpy, `default_rng(seed)`, seed 42 som standard) som trekker parameterne per produkt fra rng innenfor faste kategorier og skriver `testdata/syntetisk.csv` og `testdata/fasit.json`. Pytest i `backend/tests/testdata/` sjekker format, innhold, fasit, determinisme og importer.

**Beslutning (bruker, 2026-11-18):** Produktene heter `P-101` til `P-124`, samme format som i PRD-en og mockupene (f.eks. `P-109`). Alle har like mange sifre, så sorteringen blir riktig. De 20 med 36 måneder er `P-101`–`P-120`, og de korte er `P-121`–`P-124` (8, 15, 20 og 26 måneder).

## Boundaries & Constraints

**Always:**
- Produkter: 20 × 36 måneder (15 med trend, 2 flate med mye støy, 3 med sesong og moderat støy uten trend) og 4 korte med 8, 15, 20 og 26 måneder (med trend). Alle slutter i konstanten `SISTE_MAANED = "2026-10"`.
- Modell per måned: `y = (nivaa + trend·t) · sesongprofil[kalendermåned] + støy`, støy ~ N(0, stoeynivaa); `antall = max(0, round(y))` som heltall. Sesongprofilen har 12 faktorer (januar–desember) med snitt 1. Flate produkter har `trend = 0`.
- Parametere trekkes fra rng innenfor faste intervaller per kategori, aldri satt per produkt (SM-C1). Kommentar om SM-C1 øverst i generatoren.
- CSV: `produkt_id,maaned,antall`, komma, UTF-8 uten BOM, `\n`, sortert på `produkt_id` og `maaned`.
- `fasit.json`: `{"seed", "siste_maaned", "produkter": {id: {"foerste_maaned", "antall_maaneder", "nivaa", "trend", "sesongprofil", "stoeynivaa"}}}`, skrevet med `sort_keys=True, indent=2, ensure_ascii=False` og avsluttende `\n`. Flyttall rundes til 4 desimaler. Strukturen gir plass til kontrollproduktet i Story 2.2.
- CLI: `--seed` (standard 42) og `--mappe` (standard mappa der generatoren ligger). Ingen andre valg.
- R2: hver akseptkriterietest skal sees rød én gang (brekk betingelsen) før den regnes som bevis. Testene bruker egne konstanter (20, 36, 8/15/20/26, 15, 2, `"2026-10"`, grense for mye støy), ikke verdier importert fra generatoren.

**Never:**
- Ingen import fra `backend/` eller `prognos`. Ingen nye avhengigheter. Ingen miljøvariabler.
- Ikke `uten_stoy.csv`, stort datasett eller `.gitattributes`-regler (Story 2.2). Ikke README-endringer.
- Ikke rediger de genererte filene for hånd, og ikke bytt seed eller intervaller for å få en test grønn.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Standard | ingen argumenter | skriver begge filene i `testdata/` | N/A |
| Samme seed to ganger | `--seed 42 --mappe A`, `--mappe B` | byte-identiske filer | N/A |
| Annen seed | `--seed 7` | annen `syntetisk.csv` | N/A |
| Støy gir negativ y | flat serie med mye støy | `antall` = 0 | klemmes, ingen feil |
| Mappa finnes ikke | `--mappe ny/sti` | mappa lages | N/A |

</frozen-after-approval>

## Code Map

- `testdata/generator.py` -- ny. Kjøres med `uv run --project backend python testdata/generator.py`.
- `testdata/syntetisk.csv`, `testdata/fasit.json` -- nye, genereres av skriptet og skal ligge i arbeidstreet.
- `backend/tests/testdata/__init__.py`, `backend/tests/testdata/test_generator.py` -- nye. Rotmappa finnes via `Path(__file__).resolve().parents[3]`. Generatoren kjøres som underprosess med `sys.executable`.
- `backend/tests/domene/test_importer.py` -- mønster for statisk importsjekk med `ast`. Gjenbruk idéen, ikke modulen.
- `backend/pyproject.toml` -- numpy 2.5.x finnes allerede. Ikke endre.
- `.gitattributes` -- `* text=auto eol=lf` holder LF-filer uendret. Ikke endre (Story 2.2).

## Tasks & Acceptance

**Execution:**
- [x] `testdata/generator.py` -- skriv generatoren etter Boundaries -- FR-23/FR-24/F9
- [x] `testdata/syntetisk.csv`, `testdata/fasit.json` -- generer med standardkommandoen -- innsjekkede filer
- [x] `backend/tests/testdata/test_generator.py` -- tester: determinisme i to tmp-mapper, innsjekket = ny generering, annen seed gir annen CSV, CSV-format (overskrift, komma, ingen BOM, `\n`, sortering, heltall ≥ 0, `ÅÅÅÅ-MM`, ingen duplikater/hull), lengder per produkt og felles siste måned, ≥ 15 med trend og ≥ 2 flate med `stoeynivaa/nivaa ≥ 0,25` ifølge fasiten, fasitfelt (12 faktorer) og JSON-formatering, SM-C1-kommentar, ingen import av `prognos`/`backend` (med en negativ test av sjekken) -- AK i storyen

**Acceptance Criteria:**
- Given generatoren, when den kjøres med standardkommandoen, then begge filene skrives og alle testene i `backend/tests/testdata/` er grønne.
- Given hver akseptkriterietest, when betingelsen brytes midlertidig, then testen feiler (R2, notert i Implementation Notes).

## Implementation Notes

- Kategorier og intervaller (konstanten `KATEGORIER`, trekkes i fast rekkefølge P-101 → P-124): *trend* (P-101–P-115 og de korte P-121–P-124): nivå 40–120, trend 0,3–2,0 per måned, sesongamplitude 0,1–0,3, støy 5–15 % av nivået. *flat* (P-116–P-117): nivå 20–60, trend 0, ingen sesong (alle faktorer 1,0), støy 30–50 % av nivået. *sesong* (P-118–P-120): nivå 40–120, trend 0, amplitude 0,3–0,5, støy 8–15 %. Sesongprofilen er en sinus med tilfeldig fase og snitt 1 (avrundet til 4 desimaler, snittet avviker < 1e-4). `t` = 0 i første måned. Data genereres med de avrundede fasitparameterne.
- Med seed 42 klemmes 2 rader til `antall` = 0 (kanttilfellet i matrisen er dermed dekket av de innsjekkede dataene).
- R2: hver test er sett rød med en mutasjon av generatoren (skript i scratchpad, generatoren gjenopprettet etterpå): `default_rng()` uten seed → determinisme + innsjekket; `default_rng(42)` fast → annen seed; fjernet `mkdir` → mappe lages; `utf-8-sig` → BOM; `\r\n` → LF; `;` i overskrift → format; `antall − 500` → heltall ≥ 0; omvendt sortering → sortering; ekstra rad → duplikater; hoppet over én måned → hull; `a.0` → heltall i teksten; P-124 27 mnd → lengder; P-110 slutter en måned for tidlig → felles siste måned; 14 trendprodukter → trend-fordeling; flat støy 10–20 % → mye støy; manglende `stoeynivaa` → fasitfelt; 13 faktorer i fasit og snitt 1,1 → 12 faktorer/snitt; uavrundet støynivå → 4 desimaler; `indent=4` og manglende avsluttende `\n` → JSON-formatering; feil `foerste_maaned` → fasit mot CSV; fjernet «SM-C1» → kommentartest; `import prognos` → importsjekk. Den negative testen av importsjekken bruker en egen kildestreng.
- Etter review (iterasjon 1): `test_csv_foelger_modellen_i_fasiten` regner ut `(nivaa + trend·t)·sesongprofil[kalendermåned]` fra fasiten med testens egen månedshjelper (t = 0 i `foerste_maaned`, indeks 0 = januar). Den hopper over rader med `antall` = 0 og sjekker per produkt at snittet av restene er ≤ 3·s/√n + 1 og at spredningen ligger mellom 0,4·s og 1,8·s + 0,5 (s = `stoeynivaa`). Sammensetningen sjekkes også: minst 3 lange produkter med trend 0 og sesongspenn (max − min) ≥ 0,4 (`MIN_MED_SESONG`, `GRENSE_SESONGSPENN`), flate produkter med mye støy har bare faktorer 1,0, og de 4 korte har trend ≠ 0. Toleransen for profilsnittet er strammet til 1e-4, og toppnøklene i fasiten må være nøyaktig `seed`, `siste_maaned` og `produkter`. R2: `profil[t % 12]`, fjernet `trend * t` og støy-sd/10 → modelltesten; sesongamplitude 0,1–0,15 og flat amplitude 0,1–0,2 → sammensetningen; P-121 som sesong → korte har trend; profil + 0,0005 → snitt 1e-4; ekstra toppnøkkel → fasit mot CSV.
- Testen `test_innsjekkede_filer_er_lik_ny_generering` er avhengig av at Git ikke endrer bytes. `* text=auto eol=lf` holder LF-filene uendret; `-text`-reglene kommer i Story 2.2.
- Matrisesjekk: raden «ingen argumenter» var bare dekket indirekte. La til `test_uten_argumenter_skrives_filene_ved_siden_av_generatoren` (kopierer generatoren til en tmp-mappe og kjører den uten argumenter). Sett rød med standardmappe `Path.cwd() / "feil"`. 19 generatortester, 51 i alt, grønne i PowerShell. Standardkommandoen er kjørt i PowerShell. Fordi `testdata/` ikke er committet ennå, ble ny kjøring kontrollert med SHA-256 i stedet for `git diff --stat`.

## Spec Change Log

## Review Triage Log

Iterasjon 1 (lag: blind-hunter, edge-case-hunter, verification-gap). Ingen lag hoppet over.

| # | Funn | Dom | Rute | Belegg |
|---|------|-----|------|--------|
| 1 | Ingen test knytter CSV-verdiene til modellen i fasiten (VG, BH) | medium | patch | Bekreftet: `profil[t % 12]` gir bare grønne tester etter ny generering. Ny modelltest. |
| 2 | Sammensetningen er ikke testet: 3 sesongprodukter, flate med profil 1,0, korte med trend (VG, BH) | medium | patch | Testen teller bare trend ≥ 15 og flate ≥ 2. Nye påstander. |
| 3 | Toleransen for sesongsnitt er 1e-3, notatet sier 1e-4 | low | patch | Direkte retting. |
| 4 | Toppnivået i fasiten sjekkes ikke | low | patch | Én påstand. |
| 5 | Død `[:5]` i SM-C1-testen | low | patch | Direkte sletting. Svakt innhold i sjekken avvist: AK krever bare kommentaren. |
| 6 | Klemmingen har ingen egen test (BH) | low | avvist | Data har to 0-rader, og `antall ≥ 0` testes. `abs()` er usannsynlig. |
| 7 | Fasit mangler `kategori`-felt (BH) | low | avvist | Feltlista er låst i Intent. Trend/støy/profil skiller kategoriene. |
| 8 | Importsjekken fanger ikke `importlib`/`__import__` (BH, EC) | low | avvist | Ingen skriver slik kode i generatoren. Fiksen legger til kompleksitet. |
| 9 | Sprint-status `in-progress` mens speccen er `in-review` (BH) | false | avvist | Workflowen synker sprint-status ved avslutning. |
| 10 | Negativ `--seed` gir numpy-traceback (BH, EC) | low | avvist | Feiler høyt og tydelig. Ingen bruker det. |
| 11 | Byte-testen avhenger av `.gitattributes` (BH) | low | avvist | `-text`-reglene er allerede planlagt i Story 2.2. |
| 12 | `python -OO` gir `__doc__ = None` (EC) | low | avvist | Kjøres aldri med `-OO`. |
| 13 | `--mappe` peker på en fil (EC) | false | avvist | `mkdir` feiler høyt. Det er riktig oppførsel. |
| 14 | Ikke-atomisk skriving av to filer (EC) | low | avvist | Ny kjøring retter det. Byte-testen fanger utdaterte filer. |
| 15 | Annen numpy-versjon utenfor uv (EC) | low | avvist | Kommandoen bruker `uv run --project backend` med låst numpy. Byte-testen fanger avvik. |

## Verification

**Commands:**
- `uv run --project backend python testdata/generator.py` (PowerShell, fra rotmappa) -- skriver filene, `git diff --stat` viser ingen endring ved ny kjøring
- `uv run pytest` (i `backend/`) -- alle grønne
