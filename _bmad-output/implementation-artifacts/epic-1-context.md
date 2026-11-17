# Epic 1 Context: Kjørbart prosjektskjelett med helsesjekk

<!-- Compiled from planning artifacts. Edit freely. Regenerate with compile-epic-context if planning docs change. -->

## Goal

Sensor skal kunne klone repoet og starte backend og frontend med kommandoene i README, uten Docker, miljøvariabler, nøkler eller betalte tjenester. Databasefila opprettes automatisk ved første oppstart, og `GET /api/health` svarer OK både direkte og gjennom Next-proxyen. Epicen legger også testoppsettet for pytest, Vitest og Playwright, slik at alle senere stories kan skrive testene sine i samme story som koden. Uten dette skjelettet kan ingen av de senere epicene (data, import, prognose, backtest, dashbord) bygges eller testes.

## Stories

- Story 1.1: Backend-skjelett med automatisk database og helsesjekk
- Story 1.2: Frontend-skjelett med proxy til backend
- Story 1.3: README, repohygiene og kontroll av oppstarten

## Requirements & Constraints

- **Lokal kjøring:** Appen starter med kommandoene i README uten Docker, miljøvariabler eller `.env`. Etter installasjonen skal alt fungere uten nett (testes manuelt med nettverket koblet fra).
- **Automatisk database og helse:** Databasefila og mappen opprettes ved første oppstart. `GET /api/health` svarer `200 {"status": "ok"}`.
- **Enbrukerapp:** Ingen endepunkter krever autentisering, ingen innloggingsside.
- **Ryddig repo:** Databasefila ligger i fast, git-ignorert mappe (`backend/data/`). `git ls-files` viser ingen `.db`- eller `.env`-filer. `.env.example` finnes og sier at v1 ikke trenger variabler. Ingen hemmeligheter.
- **Norsk:** README, feilmeldinger og brukertekster på norsk. Feil på GET gir `{detail}` med norsk tekst (også 404 for ukjent sti under `/api/`).
- **README** lister forutsetninger med versjoner (Python 3.12, uv 0.13.x, Node.js ≥ 22.12) og kommandoene ordrett: installasjon, `uv run uvicorn prognos.main:app --port 8000` (fra `backend/`), `npm run dev` (fra `frontend/`), `uv run pytest`, `npm test`, `npx playwright test`. En test sjekker at kommandoene står der. Senere stories utvider README (automatisk innlasting og maskin for svartidsmåling).
- **Testregel:** En story er ikke ferdig før testene i den er grønne. Ingen CI i v1, testene kjøres lokalt.

## Technical Decisions

- **Ingen ferdig startmal for hele løsningen.** Backend er et `uv`-prosjekt (`backend/pyproject.toml`, `src/prognos/` med `domene/`, `db/`, `api/`, `konstanter.py`, `oppstart.py`, `main.py`, `__main__.py`). Frontend lages med `create-next-app` (App Router, TypeScript, Tailwind v4) og `shadcn init`, deretter fjernes `next/font/google`.
- **Låste versjoner:** Python 3.12, FastAPI 0.163.x, Uvicorn 0.54.x, Pydantic 2.14.x, SQLAlchemy 2.1.x `[asyncio]`, aiosqlite 0.22.x, statsforecast 2.1.1, pandas 2.3.3, numpy 2.5.x, pytest 9.2.x / pytest-asyncio 1.5.x, httpx 0.28.x, python-multipart. Frontend: Next.js `"16.4.6"` eksakt (uten `^`/`~`), React 19.3.x, TypeScript 5.9.x, Tailwind 4.3.x, TanStack Query 5.108.x, zod 4.6.x, Recharts 3.11.x, Vitest 5.1.x, Playwright 1.65.x.
- **Ren kjerne:** `domene/` importerer aldri `fastapi`, `sqlalchemy`, `prognos.api` eller `prognos.db`. En importtest håndhever dette fra starten.
- **App-fabrikk og testbarhet:** `main.py::lag_app(db_sti: Path) -> FastAPI` er eneste fabrikk. `app = lag_app(STANDARD_DB_STI)`, der `STANDARD_DB_STI` i `konstanter.py` peker til `backend/data/prognos.db`. `python -m prognos --db STI --port N` starter mot annen fil. Skalltester lager appen mot en midlertidig fil, åpner `app.router.lifespan_context(app)` og kaller `httpx.AsyncClient(transport=httpx.ASGITransport(app))`. Aldri mot utviklerens database.
- **Skjema og versjonsvakt:** I lifespan (`oppstart.py`) kjører vakten **før** `create_all`. Fil uten tabeller: `create_all` og `SKJEMAVERSJON` settes inn i samme transaksjon (tabell `skjemaversjon`). Fil med tabeller der `skjemaversjon` mangler eller har annen verdi: backend stopper med «Databasefila har gammelt skjema. Slett backend/data/prognos.db og start på nytt.» Ingen Alembic.
- **Ingen konfigurasjon:** Stier, port og frister er konstanter i `prognos/konstanter.py` og `next.config.ts`. Ingen kode leser miljøvariabler (heller ikke `process.env` i frontend).
- **Én origin og proxy:** Frontend kaller bare relative `/api/*`. `next.config.ts` har rewrite `/api/:path*` → `http://127.0.0.1:8000/api/:path*` og `experimental: { proxyTimeout: 130000, agentUpgrade: false }`. Backend har ingen CORS. Next-telemetrien slås av i `predev` og `prebuild` uten miljøvariabler. Bare systemfonter, ingen CDN eller eksterne kall.
- **API-flaten er fast:** Bare seks endepunkter skal noen gang finnes; i denne epicen bare `GET /api/health`. Pydantic eier kontrakten.
- **Konvensjoner:** Norsk snake_case i kode, DB og JSON; æ/ø/å skrives `ae`/`oe`/`aa`. Moduler og filer har norske navn. Standard `logging` til stdout. Domenefeil i `domene/feil.py`.
- **Playwright:** `webServer` starter backend med `--db` mot en midlertidig fil og frontend med `npm run dev`.
- **Linjeslutt:** `.gitattributes` med global `eol=lf` (testdata-reglene kommer i Epic 2).

## UX & Interaction Patterns

- Forsiden er bare en enkel norsk plassholder med ordmerket «PROGNOS» og `<html lang="nb">`. Selve dashbordet, designtokens og komponentene kommer i Epic 6.

## Cross-Story Dependencies

- Story 1.2 forutsetter at backend fra Story 1.1 kjører på port 8000 og støtter `--db` (for proxytesten og Playwright `webServer`).
- Story 1.3 forutsetter 1.1 og 1.2: README-kommandoene og oppstartskontrollen gjelder begge delene.
- Alle senere epics bygger på strukturen, `lag_app`/`--db`-mønsteret, versjonsvakten (hver skjemaendring øker `SKJEMAVERSJON`) og testoppsettet herfra. Epic 3 legger til de øvrige endepunktene og datatabellene.
