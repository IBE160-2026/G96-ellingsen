# Story 1.3: README, repohygiene og kontroll av oppstarten

## 2026-11-18 kl. 13:43 — Mathias Ellingsen

### Oppgave
Gjennomføre Story 1.3 med `bmad-build`. README skal fortelle sensor hva som må installeres og hvilke kommandoer som starter appen og kjører testene. Om liten stasjonsbokstav i Vitest besluttet brukeren: ikke lage `scripts/test.mjs`. README skal i stedet anbefale PowerShell og ha en kort merknad med rundgangene som er testet for cmd og Git Bash.

### Plan
- Oneshot-rute, siden endringen er liten og ikke har åpne spørsmål. Spec: [spec-1-3-readme-repohygiene-og-kontroll-av-oppstarten.md](../../_bmad-output/implementation-artifacts/spec-1-3-readme-repohygiene-og-kontroll-av-oppstarten.md).
- README, `.env.example`, pytest-tester for README og `git ls-files`, og en kontroll av oppstarten.
- Review med Blind Hunter.

### Resultat
- `README.md` er skrevet om på norsk. Den har forutsetninger med versjoner og installasjonslenker for uv og Node, installasjon (`uv sync --frozen`, `npm ci`, `npx playwright install chromium`), start av backend og frontend og alle tre testkommandoene. Den sier at v1 ikke trenger Docker, miljøvariabler, nøkler eller betalte tjenester, og at bare installasjonen trenger nett. Merknaden om PowerShell anbefaler PowerShell og gir rundgangene for cmd (`cd /d C:\…`) og Git Bash (`cd /C/…`).
- `.env.example` sier at v1 ikke trenger miljøvariabler.
- `backend/tests/test_repo.py` sjekker at kommandoene og versjonene står i README, at `.env.example` finnes, og at git ikke sporer `.db`-, `.db-wal`-, `.sqlite`- eller `.env`-filer. Testen hoppes over uten `.git`.
- Tester: `uv run pytest` ga 32 grønne, og `npm test` fra PowerShell ga 15/15.
- **Oppstartskontroll med nett, 2026-11-18, utviklerens PC** (Windows 11 Home, Node 26.13.1, uv 0.13.8): Jeg flyttet den gamle `backend/data/` til side og startet etter README. `prognos.db` ble opprettet. `GET /api/health` ga `{"status":"ok"}` både gjennom `localhost:3000` og direkte på 8000.
- Review: 12 funn. 3 ble rettet: `.db`-endelser, `.env.*.example` og installasjonslenker. 1 ble utsatt (offline-kontrollen), og 8 ble avvist. Detaljene står i Review Triage Log i speccen.
- Sprint-status: Story 1.3 står på `review`. Koden ligger i `f07911e`.
- Punktet om liten stasjonsbokstav fra Story 1.2 er lukket i `issues.md`.

### Åpne punkter
- Den manuelle offline-kontrollen (F12, NFR-1) gjenstår: koble fra nettverket etter installasjonen, start backend og frontend etter README, og sjekk `/api/health` gjennom frontend. Før resultatet i loggen med dato og maskin.
- Gå gjennom Story 1.3 (står på `review`), og sett den til `done` i sprint-status.
