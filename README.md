# G96 — Agent47

Gruppeprosjekt i **IBE160 Programmering med KI** ved Høgskolen i Molde, høsten 2026 (15 studiepoeng).

Repoet inneholder gruppens applikasjon PROGNOS (salgsprognoser for småbedrifter) og dokumentasjon av utvikling, testing og kvalitetssikring med KI.

## Medlemmer

- Mathias Ellingsen

## Kjøre PROGNOS lokalt

PROGNOS kjører helt lokalt. Du trenger ikke Docker, miljøvariabler, `.env`-fil, API-nøkler eller betalte tjenester. Bare installasjonen trenger nett. Etter installasjonen virker appen og testene uten nett.

### Forutsetninger

| Verktøy | Versjon |
|---------|---------|
| Python | 3.12 (uv henter den selv hvis den mangler) |
| uv | 0.13.x |
| Node.js | ≥ 22.12 (med npm) |
| git | for å klone repoet |

uv installeres etter oppskriften på <https://docs.astral.sh/uv/getting-started/installation/>. Node.js (med npm) lastes ned fra <https://nodejs.org/>.

### Terminal på Windows

Bruk **PowerShell**, som er standardterminalen i VS Code. `npm test` (Vitest) feiler med «Cannot read properties of undefined (reading 'config')» når arbeidsmappa har liten stasjonsbokstav (`c:\…`). Feilen ligger i Vitest/Vite. PowerShell skriver stasjonsbokstaven om til `C:` og er ikke rammet. Testede rundganger i andre terminaler:

- **cmd:** gå til mappa med stor bokstav, `cd /d C:\…\frontend`.
- **Git Bash:** bruk stor bokstav i stien, `cd /C/…/frontend` (ikke `/c/…`).

### Installasjon

Fra rotmappa i repoet:

```
cd backend
uv sync --frozen
cd ../frontend
npm ci
npx playwright install chromium
```

`uv sync --frozen` og `npm ci` installerer de låste versjonene fra `backend/uv.lock` og `frontend/package-lock.json`. Den siste kommandoen laster ned nettleseren Playwright-testene bruker.

### Start

Start backend og frontend i hver sin terminal.

Backend, fra `backend/`:

```
uv run uvicorn prognos.main:app --port 8000
```

Frontend, fra `frontend/`:

```
npm run dev
```

Åpne <http://localhost:3000>. Databasefila `backend/data/prognos.db` opprettes automatisk ved første oppstart. Helsesjekken svarer `{"status":"ok"}` på <http://localhost:3000/api/health> (gjennom frontend) og på <http://127.0.0.1:8000/api/health> (direkte).

### Tester

Backend-tester, fra `backend/`:

```
uv run pytest
```

Frontend-tester (Vitest), fra `frontend/`:

```
npm test
```

Ende-til-ende-tester (Playwright), fra `frontend/`. Stopp backend og frontend først, siden testene starter begge selv på port 8000 og 3000, mot en midlertidig database:

```
npx playwright test
```
