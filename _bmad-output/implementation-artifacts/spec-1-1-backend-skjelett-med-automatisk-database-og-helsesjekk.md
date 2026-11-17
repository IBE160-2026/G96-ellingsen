---
title: 'Story 1.1: Backend-skjelett med automatisk database og helsesjekk'
type: 'feature'
created: '2026-11-17'
status: 'done'
baseline_commit: '3cfcda9d606cf6807b9c54323620c3d0130ec3b6'
route: 'dispatch'
review_loop_iteration: 0
context:
  - '{project-root}/_bmad-output/implementation-artifacts/epic-1-context.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Repoet har ingen backend. Sensor kan ikke starte noe, og senere stories har ikke app-fabrikk, database eller testoppsett å bygge på.

**Approach:** Lag `backend/` som uv-prosjekt med pakken `prognos`: `lag_app(db_sti)`-fabrikk, lifespan som oppretter SQLite-fila og tabellen `skjemaversjon` bak en versjonsvakt (AD-13), `GET /api/health`, norsk 404-`{detail}`, CLI med `--db`/`--port` og pytest-oppsett med importtest for `domene/` (AD-1).

## Boundaries & Constraints

**Always:** Ingen miljøvariabler eller `.env` leses. Stier, port og `SKJEMAVERSJON` er konstanter i `konstanter.py`. Tester bruker alltid midlertidig databasefil (AD-14), aldri `backend/data/prognos.db`. Norske navn i snake_case med `ae`/`oe`/`aa`. Avhengigheter følger arkitekturens *Stack*-tabell, låst i `pyproject.toml` og `uv.lock`.

**Never:** Ingen andre endepunkter enn `/api/health`. Ingen CORS, autentisering eller Alembic. Ingen datatabeller utover `skjemaversjon` (kommer i Epic 3). Ingen frontend eller README-endringer (Story 1.2/1.3). `domene/` importerer aldri `fastapi`, `sqlalchemy`, `prognos.api` eller `prognos.db`.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Første oppstart | Fil og mappe finnes ikke | Mappe + fil opprettes, `skjemaversjon` får én rad med `SKJEMAVERSJON` i samme transaksjon | N/A |
| Ny oppstart | Fil med riktig versjon | Starter, ingen ny rad | N/A |
| Gammelt skjema | Tabeller finnes, `skjemaversjon` mangler | Oppstart stopper | Unntak med «Databasefila har gammelt skjema. Slett backend/data/prognos.db og start på nytt.» |
| Feil versjon | `skjemaversjon` har annen verdi | Oppstart stopper | Samme melding |
| Helse | `GET /api/health` | `200 {"status": "ok"}` | N/A |
| Ukjent sti | `GET /api/finnes-ikke` | `404 {"detail": "<norsk tekst>"}` | N/A |

</frozen-after-approval>

## Code Map

Greenfield: ingen backend-kode finnes. Rotens `.gitignore` har allerede `*.db` og `.venv/`; `.gitattributes` har `* text=auto eol=lf`. `spikes/` skal ikke røres. Python 3.12 og uv 0.13.8 er installert lokalt.

- `backend/pyproject.toml` -- uv-prosjekt, `src/`-layout, pytest-konfig
- `backend/src/prognos/konstanter.py` -- `STANDARD_DB_STI`, `SKJEMAVERSJON`, `GAMMELT_SKJEMA_MELDING`, standard port
- `backend/src/prognos/db/` -- `Base`, modellen `Skjemaversjon`, motor-fabrikk
- `backend/src/prognos/oppstart.py` -- versjonsvakt + `create_all` + lifespan
- `backend/src/prognos/api/` -- helse-ruter og norsk HTTP-unntakshåndterer
- `backend/src/prognos/main.py`, `__main__.py` -- fabrikk og CLI
- `backend/src/prognos/domene/` -- tom ren kjerne (`__init__.py`, `feil.py`)

## Tasks & Acceptance

**Execution:**
- [x] `backend/pyproject.toml` (+ `uv.lock`, `.python-version`) -- opprett med `uv`; avhengigheter fastapi 0.163.x, uvicorn 0.54.x, pydantic 2.14.x, sqlalchemy[asyncio] 2.1.x, aiosqlite 0.22.x, statsforecast==2.1.1, pandas==2.3.3, numpy 2.5.x, python-multipart; dev: pytest 9.2.x, pytest-asyncio 1.5.x, httpx 0.28.x; `requires-python = ">=3.12,<3.13"`; `asyncio_mode = "auto"`, `testpaths = ["tests"]` -- låste versjoner
- [x] `backend/src/prognos/konstanter.py` -- `STANDARD_DB_STI = <backend>/data/prognos.db` regnet fra `__file__`, `SKJEMAVERSJON = 1`, den faste meldingen, `STANDARD_PORT = 8000` -- ingen konfigurasjon
- [x] `backend/src/prognos/domene/__init__.py`, `domene/feil.py` -- tom kjerne med docstring -- AD-1-struktur
- [x] `backend/src/prognos/db/__init__.py`, `db/modeller.py`, `db/okt.py` -- `DeclarativeBase`, tabell `skjemaversjon(versjon int PK)`, `lag_motor(db_sti)` for `sqlite+aiosqlite` -- AD-13
- [x] `backend/src/prognos/oppstart.py` -- `GammeltSkjemaFeil`, `klargjoer_database(motor)` (vakt før `create_all`; tom fil → `create_all` + insert i én `engine.begin()`), `lag_lifespan(db_sti)` som lager mappen, kjører vakten, logger og disposer motoren -- AD-13
- [x] `backend/src/prognos/api/__init__.py`, `api/helse.py`, `api/feil.py` -- `GET /api/health` med Pydantic-svarmodell; håndterer for `StarletteHTTPException` som gir norsk `{detail}` (404 → «Fant ikke ressursen.», andre koder norsk generisk tekst) -- AD-9
- [x] `backend/src/prognos/main.py` -- `lag_app(db_sti: Path) -> FastAPI`, lagrer `db_sti` i `app.state`, `app = lag_app(STANDARD_DB_STI)` -- AD-14
- [x] `backend/src/prognos/__main__.py` -- `tolk_argumenter(argv)` (`--db`, `--port`) og `main(argv)` som kaller `uvicorn.run(lag_app(db), host="127.0.0.1", port=port)` -- AD-14
- [x] `.gitignore` -- legg til eksplisitt `backend/data/*.db` -- NFR-9
- [x] `backend/tests/api/test_helse.py`, `tests/api/test_oppstart.py`, `tests/test_cli.py`, `tests/domene/test_importer.py`, `tests/conftest.py` -- testene listet i storyen; importtesten parser alle `.py` i `domene/` med `ast` og avviser de fire forbudte modulene (også undermoduler), og testes selv mot en forbudt kildetekst -- dekker matrisen

**Acceptance Criteria:**
- Given `backend/`, when `uv run uvicorn prognos.main:app --port 8000` kjøres uten miljøvariabler, then backend starter og `backend/data/prognos.db` opprettes.
- Given `python -m prognos --db STI --port N`, when argumentene tolkes, then appen lages mot `STI` (testet med uvicorn.run byttet ut).
- Given `backend/data/prognos.db` etter kjøring, when `git check-ignore` kjøres, then fila er ignorert.
- Given hele testsuiten, when `uv run pytest` kjøres fra `backend/`, then alle tester er grønne.

## Implementation Notes

- Låste versjoner: fastapi 0.163.2, uvicorn 0.54.0, pydantic 2.14.3, sqlalchemy 2.1.9, aiosqlite 0.22.1, statsforecast 2.1.1, pandas 2.3.3, numpy 2.5.5, python-multipart 0.0.34; pytest 9.2.0, pytest-asyncio 1.5.0, httpx 0.28.1.
- `logging.basicConfig(level=INFO)` ligger i `main.py`, slik at `uv run uvicorn prognos.main:app` også logger `prognos`-meldinger.
- 400, 405 og 500 har egne norske tekster i tillegg til 404. Andre koder får en generisk tekst.

## Spec Change Log

## Review Triage Log

Pass 1 (blind-hunter, edge-case-hunter, verification-gap):

| # | Funn | Verdikt | Begrunnelse / rute |
|---|------|---------|--------------------|
| 1 | `http_feil` kaster `feil.detail` (B, E) | medium | Senere `HTTPException(404, "<norsk>")` i Epic 3 ville fått generisk tekst. → patch |
| 2 | 422 og uhåndterte unntak gir engelsk svar (B, E×2, V) | low | Ikke nåbart: bare `/api/health` uten parametere, og ruten kan ikke kaste. Fiksen legger til håndterere for Epic 3s POST-kontrakt (AD-9). Avvist, ført som åpent punkt til Epic 3 |
| 3 | `basicConfig` ved import (B) | low | Flytting til `__main__` ville fjerne INFO-logging når appen startes med `uvicorn prognos.main:app`. Avvist |
| 4 | Korrupt databasefil gir rå traceback (B, E) | low | Sjelden, og den feiler høylytt. Fiksen gir en ny gren. Avvist |
| 5 | Vakten er ikke testet med tom tabell eller to rader (B, V) | medium | Forhåndsverifisert gap. → patch |
| 6 | `PRAGMA foreign_keys` mangler (B) | false | Ingen fremmednøkler finnes i denne storyen |
| 7 | `parents[2]` ved installasjon uten editable (B) | low | `uv sync` installerer prosjektet editable. Avvist |
| 8 | `STANDARD_DB_STI` er ikke festet av noen test (V) | medium | Forhåndsverifisert. → patch |
| 9 | 405-testen er svak, og `Allow` er ikke sjekket (B, V) | low | → patch (bare testen endres) |
| 10 | `.gitignore` mangler `-journal`, `-wal` og `-shm` (B, E) | low | Journalfila dukker opp under skriving. Direkte tillegg. → patch |
| 11 | Importsjekken løser relative importer feil i underpakker (B, E×2, V) | low | Latent feil i håndhevingen av AD-1. Rettes direkte i testhjelperen. → patch |
| 12 | Dynamisk import (`importlib`) fanges ikke (E) | low | Lite sannsynlig, og fiksen gir mer kompleksitet. Avvist |
| 13 | Ingen øvre grense for `python-multipart` (B) | low | Direkte retting. → patch |
| 14 | Relativ `--db` løses mot cwd (B) | false | Vanlig CLI-oppførsel, og standardstien er absolutt |
| 15 | `--db` peker på en mappe, eller forelderen er en fil (E) | false | Feiler høylytt. Det er riktig oppførsel |
| 16 | To prosesser oppretter samme nye fil samtidig (E) | false | Enbrukerapp (NFR-8) med én backend-prosess. Ikke nåbart |
| 17 | `?`, `#` eller `%` i stien bryter URL-en (E) | low | Direkte retting med `URL.create`. → patch |
| 18 | `--port` utenfor 1–65535 (E) | false | uvicorn feiler høylytt |
| 19 | Meldingen nevner standardstien selv ved egen `--db` (E) | low | Teksten er fastsatt i AD-13. Avvist |
| 20 | `sqlite3`-forbindelser lukkes ikke i testene (E) | low | Direkte retting med `closing`. → patch |

## Design Notes

Vakten avgjør på tabellnavn (`inspect` via `run_sync`): ingen tabeller → initialiser; tabeller men ingen `skjemaversjon` eller annen verdi → `GammeltSkjemaFeil(GAMMELT_SKJEMA_MELDING)`; riktig verdi → `create_all` (no-op nå, nye tabeller senere krever uansett ny `SKJEMAVERSJON`). Unntaket i lifespan gjør at uvicorn stopper med meldingen i loggen. Senere stories legger seed (`seed_if_empty`) inn i samme lifespan.

## Verification

**Commands:**
- `cd backend && uv sync && uv run pytest` -- expected: alle tester grønne
- `cd backend && uv run python -m prognos --db <tmp>/x.db --port 8011` + `curl 127.0.0.1:8011/api/health` -- expected: `{"status":"ok"}`, fila opprettet
- `git check-ignore backend/data/prognos.db` -- expected: stien skrives ut
