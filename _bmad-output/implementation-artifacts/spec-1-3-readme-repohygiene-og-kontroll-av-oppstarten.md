---
title: 'Story 1.3: README, repohygiene og kontroll av oppstarten'
type: 'feature'
created: '2026-11-18'
status: 'done'
route: 'oneshot'
review_loop_iteration: 0
context: []
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** README i rotmappa forteller ikke sensor hva som må installeres eller hvilke kommandoer som starter appen og kjører testene. `.env.example` mangler, og ingen test sikrer at kommandoene står i README eller at repoet er fritt for `.db`- og `.env`-filer (NFR-1, NFR-9, F12).

**Approach:** Skriv om README på norsk med forutsetninger med versjoner (Python 3.12, uv 0.13.x, Node.js ≥ 22.12), installasjon, start av backend og frontend og alle testkommandoene ordrett, og si at v1 ikke trenger Docker, miljøvariabler, nøkler eller betalte tjenester, og at bare installasjonen trenger nett. Legg til `.env.example` som forklarer at v1 ikke trenger variabler, og pytest-tester for README-kommandoene og `git ls-files`. Den manuelle offline-kontrollen (F12) føres i sesjonsloggen med dato og maskin.

**Beslutning (bruker, 2026-11-18) om liten stasjonsbokstav i Vitest:** Ikke lag `scripts/test.mjs`. README anbefaler PowerShell (standardterminalen i VS Code) og har en kort merknad med de testede rundgangene: cmd `cd /d C:\…\frontend`, Git Bash `cd /C/…` (stor bokstav).

</frozen-after-approval>

## Implementation Notes

- Filer: `README.md` (beholder gruppe- og medlemsinfo), `.env.example`, `backend/tests/test_repo.py`.
- Installasjon: `uv sync --frozen` i `backend/`, `npm ci` i `frontend/`, `npx playwright install chromium`. Låsefilene er sjekket inn.
- Testene finner rotmappa via `Path(__file__).resolve().parents[2]`. `git ls-files`-testen hoppes over (skip) når rotmappa ikke er et git-repo (f.eks. nedlastet ZIP), siden NFR-9 måles med `git ls-files`.
- Oppstartskontroll 2026-11-18 på utviklerens PC (Windows 11 Home, Node 26.13.1, uv 0.13.8), **med nett**: `backend/data/` flyttet til side, backend og frontend startet med README-kommandoene, `prognos.db` ble opprettet, og `GET /api/health` ga `{"status":"ok"}` både gjennom `localhost:3000` og direkte på 8000. `npm test` i PowerShell: 15/15. `uv run pytest`: 32 grønne.
- **Ikke gjort:** offline-delen av F12 (nettverket koblet fra). Den må brukeren gjøre for hånd. Ført i deferred-work og issues.md.
- Overraskelse: første skriving la `.env.example`-teksten i README.md ved en feil. Rettet før testing.

## Review Triage Log

Iterasjon 1 (lag: blind-hunter). Ingen lag hoppet over.

| # | Funn | Dom | Rute | Belegg |
|---|------|-----|------|--------|
| 1 | Offline-kontrollen (F12) er ikke gjort eller logget | medium | defer | Krever at nettverket kobles fra. Kontrollen med nett er gjort og logget. |
| 2 | `.db`-testen fanger ikke `-journal`/`-wal`/`-shm`/`.sqlite` | low | patch | `.gitignore` ignorerer disse. Testen sjekker nå alle endelsene. |
| 3 | `.env`-testen avviser `.env.*.example`, som `.gitignore` tillater | low | patch | Testen godtar nå alle navn som slutter på `.example`. |
| 4 | Versjonstesten sammenlignes ikke med pinnene i `pyproject.toml` | low | avvist | Rammer sjelden. Fiksen ville lagt til parsing. |
| 5 | Kommandotesten sjekker ikke seksjon eller kodeblokk | low | avvist | AK krever at kommandoene står ordrett, ikke hvor de står. |
| 6 | Ingen `engines`/`.nvmrc` for Node ≥ 22.12 | low | avvist | Fantes fra før og ligger utenfor storyen. |
| 7 | README sier ikke hvordan uv og Node installeres | medium | patch | Sensor skal klare seg uten hjelp. La til lenker. |
| 8 | `playwright install` uten `--with-deps` på Linux | low | avvist | Sensor bruker sannsynligvis Windows eller macOS. |
| 9 | Ingen feilsøkingsdel (gammelt skjema, opptatte porter) | low | avvist | Backend skriver selv hva du skal gjøre ved gammelt skjema. README sier at serverne må stoppes før Playwright. |
| 10 | Testen kaster `FileNotFoundError` uten git | false | avvist | Finnes `.git`, er repoet klonet med git. Uten `.git` hoppes testen over før git kalles. |
| 11 | Speccen og sprint-status ligger utenfor staging | false | avvist | Commit-steget tar med alt. |
| 12 | `.env.example` peker feil for frister, og «NFR-9» er sjargong | false | avvist | `proxyTimeout` er en frist i `next.config.ts`. Sjargongen er kosmetisk. |
