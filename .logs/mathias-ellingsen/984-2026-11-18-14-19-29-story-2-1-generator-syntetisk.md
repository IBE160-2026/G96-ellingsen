# Story 2.1: Generator for syntetisk salgshistorikk med fasit

## 2026-11-18 kl. 14:19 — Mathias Ellingsen

### Oppgave
Bygge Story 2.1 med `bmad-build`. Målet er en generator med seed 42 som skriver en syntetisk salgshistorikk (`syntetisk.csv`) og en fasit med kjent trend, sesong og støy (`fasit.json`). Prognosen, backtesten og seedingen ved første oppstart skal kunne sjekkes mot data der svaret er kjent.

### Plan
- Kompilerte epic-konteksten med en subagent: [epic-2-context.md](../../_bmad-output/implementation-artifacts/epic-2-context.md).
- Skrev speccen [spec-2-1-generator-for-syntetisk-salgshistorikk-med-fasit.md](../../_bmad-output/implementation-artifacts/spec-2-1-generator-for-syntetisk-salgshistorikk-med-fasit.md).
  - Brukeren bestemte produktnavnene `P-101`–`P-124`, samme format som i PRD-en og mockupene.
  - Brukeren valgte å beholde speccen selv om den er på omtrent 1 800 tokens.
- En subagent implementerte. Deretter gikk tre uavhengige reviewere gjennom (blind, edge case og verifikasjonsgap), og patchene gikk tilbake til samme subagent.

### Resultat
- **Ny generator `testdata/generator.py`:** bruker bare standardbiblioteket og numpy, med `--seed` (standard 42) og `--mappe`. Den lager 24 produkter:
  - `P-101`–`P-115` har trend.
  - `P-116`–`P-117` er flate med mye støy.
  - `P-118`–`P-120` har sesong uten trend.
  - `P-121`–`P-124` er korte med 8, 15, 20 og 26 måneder.
  - Alle slutter i `2026-10`. Parameterne trekkes fra faste intervaller per kategori (SM-C1).
- **Genererte filer:** `testdata/syntetisk.csv` (789 rader) og `testdata/fasit.json`. Med seed 42 klemmes 2 rader til 0.
- **Tester:** `backend/tests/testdata/test_generator.py` har 21 tester. De dekker determinisme, at de innsjekkede filene er lik en ny generering, CSV-formatet, lengdene, sammensetningen, at CSV-en følger modellen i fasiten, fasitformatet og importene.
- **R2:** hver test er sett rød med en mutasjon av generatoren.
- **Verifisert i PowerShell:**
  - `uv run pytest` i `backend/` ga 53 grønne.
  - `uv run --project backend python testdata/generator.py` ga samme SHA-256 ved ny kjøring.
- **Review:** 15 funn.
  - 5 ble rettet. Det viktigste: ingen test knyttet CSV-verdiene til fasiten, og sammensetningen var ikke testet.
  - 10 ble avvist med begrunnelse. Triageloggen står i speccen.
- **Status:** speccen er `done`, og Story 2.1 står på `review` i sprint-status.

- **Brukeren har gått gjennom testene og generatoren.** Story 2.1 er satt til `done` i sprint-status, og det er lagt til en innførsel i `docs/ki-logg.md`. Koden ligger i commit `d9c59b5`.
- **`.gitattributes` er kontrollert.** Den globale regelen `* text=auto eol=lf` holder testdatafilene uendret både ved innsjekking og utsjekking:
  - **Innsjekking:** det lagrede blobet er identisk med den rå fila, selv om maskinen har `core.autocrlf=true`.
  - **Utsjekking:** en fersk klone med `core.autocrlf=true` er byte-lik og har 0 CR-bytes.
  - **Motprøve:** med regelen fjernet fra både disk og indeks får klonen CRLF i hver linje (790 og 510 CR-bytes). Det er altså regelen som beskytter filene.
  - De egne `-text`-reglene kommer fortsatt i Story 2.2.

### Åpne punkter
Ingen.
