# Revisjon av product brief

## 2026-11-14 kl. 17:11 — Mathias Ellingsen

### Oppgave
Revidere `PRODUCT_BRIEF.md` etter tilbakemelding om at omfanget var for stort: velge én primærbruker, bytte forretningsmål ut med testbare funksjonelle kriterier og avgrense v1 til en tydelig kjerneflyt, med resten flyttet til senere trinn og en visjon. Deretter committe, pushe og merge til `main`.

### Plan
- Tre runder med omskriving av briefen, én per tilbakemelding.
- Commit på grenen `revider-product-brief`, push, og deretter merge inn i `main`.

### Resultat
- `PRODUCT_BRIEF.md` er skrevet om:
  - Primærbruker er etterspørselsplanleggeren (persona «Kari»).
  - Nytt avsnitt 4 Omfang: v1 (CSV-import, ETS mot sesongnaiv baseline, tre scenarioer P10/P50/P90, backtest med WAPE, Streamlit-dashbord, syntetiske testdata), trinn 2 (produksjon vs. lager med sikkerhetslager = Σ(P90 − P50) over ledetiden, valgfri LLM-forklaring med mock-modus), senere trinn, visjon og det som er utenfor omfang uansett.
  - Suksesskriterier F1–F10 (v1) og B1–B3, L1 (trinn 2).
- Commit `6da487f` på `revider-product-brief`. `origin/main` hadde fått 4 nye commits fra Bård (tilbakemelding, sesjonslogg-skill, `technology.md`), og disse ble merget inn uten konflikt. Merge-commit `8aacd59` er pushet til `main`.
- Git-identitet er satt lokalt i repoet (`user.name`/`user.email`), siden den manglet.

### Åpne punkter
- Det syntetiske testdatasettet og generatoren finnes ikke ennå. Det trengs før F7–F9 kan testes.
- Valgte terskler må vurderes av gruppen: 24 måneders minimumshistorikk, 6 måneders horisont og 65–95 % intervalldekning (F8).
- `.docs/planning-artifacts/architecture/technology.md` beskriver FastAPI, Next.js og PostgreSQL. Den reviderte briefen bruker Streamlit uten database i v1, så dokumentene må samkjøres.

## 2026-11-14 kl. 17:15 — Mathias Ellingsen

### Oppgave
Samkjøre briefen med Bårds `technology.md`: v1 skal bruke FastAPI, Next.js og PostgreSQL i stedet for Streamlit uten database.

### Plan
- Lese `technology.md` og ta med bare de delene v1 trenger.
- Oppdatere avsnitt 4 og 5 og suksesskriteriene i `PRODUCT_BRIEF.md`, og committe.

### Resultat
- Avsnitt 5 i `PRODUCT_BRIEF.md` er skrevet om:
  - FastAPI-backend, Next.js-dashbord (Recharts) og PostgreSQL 16 med SQLAlchemy og Alembic, kjørt lokalt med Docker Compose.
  - API-endepunkter og datamodell for v1.
  - Mock-fallback og feature flags (`FEATURE_DECISION`, `FEATURE_AI`) for trinn 2.
  - En liste over hva fra `technology.md` som ikke er med i v1: innlogging, betaling, e-post, Supabase, Redis, Caddy, Railway og backup.
- Avsnitt 4.1 sier nå at datasett lagres i databasen og at testdata seedes ved oppstart.
- F10 testes nå med Playwright i stedet for Streamlit `AppTest`. Nye kriterier: F11 (lagring i PostgreSQL) og F12 (`docker compose up` uten hemmeligheter).
- Commit `08a5cda`, pushet til `origin/main`. Punktet om samkjøring med `technology.md` i `issues.md` er lukket.

### Åpne punkter
- Den nye stacken gir mer arbeid i v1 enn Streamlit-løsningen (to språk, database, migrasjoner, Docker). Gruppen bør vurdere om v1 fortsatt rekkes i semesteret.

## 2026-11-14 kl. 18:32 — Mathias Ellingsen

### Oppgave
Fire endringer i `PRODUCT_BRIEF.md`: bytte til SQLite, slik at sensor ikke trenger Docker og F11/F12 blir enkle; legge til «Hva skiller PROGNOS fra andre verktøy»; korte ned avsnitt 5 ved å flytte komponenttabell, API og datamodell til arkitekturdokumentet (steg 4); legge til en skisse av dashbordet.

### Plan
- Arkitekturdokumentet fra steg 4 finnes ikke ennå. Det flyttede innholdet legges derfor i et utkast, `.docs/planning-artifacts/architecture/arkitektur-utkast.md`, oppdatert til SQLite.
- Redigere briefen direkte.

### Resultat
- `PRODUCT_BRIEF.md`:
  - Nytt underavsnitt «Hva skiller PROGNOS fra andre verktøy» sist i avsnitt 2. Det sier at det finnes ERP-prognosemoduler og egne planleggingsverktøy, og at PROGNOS er en studentprototype som viser et prinsipp for bedrifter som bruker regneark: usikkerhet og etterprøving.
  - 4.1: datasett lagres i SQLite. Under «5. Dashbord» er det lagt inn en tekstskisse som viser plasseringen av opplasting/datasettvelger og validering (øverst), produktvelger (venstre), graf (midten), scenariotabell og backtest (under grafen) og WAPE-oversikt (nederst).
  - Avsnitt 5: en kort innledning som begrunner SQLite i stedet for PostgreSQL fra `technology.md`, arkitekturskissen med SQLite, og prinsippene (null konfigurasjon nå også uten Docker). Tabellene for komponenter, API og datamodell og listen «med / ikke med» er fjernet.
  - F11 gjelder nå SQLite. F12 krever at appen starter med README-kommandoene uten Docker eller nøkler, at databasefila opprettes automatisk, og at `/api/health` svarer OK.
- Ny fil `.docs/planning-artifacts/architecture/arkitektur-utkast.md` med komponenttabell (SQLite + `aiosqlite`), API, datamodell og med/ikke med/avvik fra `technology.md`.
- Endringene er ikke committet.

### Åpne punkter
- Innholdet i `arkitektur-utkast.md` skal inn i arkitekturdokumentet i steg 4. Der må vi også velge mellom Alembic og `create_all` for SQLite.
