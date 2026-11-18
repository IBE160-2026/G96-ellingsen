# Story 1.2: Frontend-skjelett med proxy til backend

## 2026-11-18 kl. 13:30 — Mathias Ellingsen

### Oppgave
Fortsette Story 1.2 fra i går med `bmad-build`. Utgangspunktet var sprint-status.yaml, spesifikasjonen for 1.2 og det ukommitterte `frontend/`. Målet er en Next-app som sensor kan åpne, med proxy til backend og testoppsett som Epic 6 kan bygge på.

### Plan
- Spesifikasjon: [spec-1-2-frontend-skjelett-med-proxy-til-backend.md](../../_bmad-output/implementation-artifacts/spec-1-2-frontend-skjelett-med-proxy-til-backend.md). Den stod på `in-progress`, så arbeidet fortsatte i implementeringssteget.
- Implementeringsagent mot speccen, deretter egen kontroll av diffen mot oppgaver, akseptkriterier og I/O-matrisen.
- Review i tre lag (blind hunter, edge case hunter, verification gap), triage i speccen og patcher tilbake til implementeringsagenten.

### Resultat
- `frontend/`: Next 16.4.6 (App Router, TypeScript, Tailwind v4, shadcn), `lang="nb"`, norsk plassholder med «PROGNOS» og bare systemfonter. `next.config.ts` sender `/api/*` videre til `127.0.0.1:8000` og har `experimental: { proxyTimeout: 130000, agentUpgrade: false }`.
- Rettet ved egen kontroll:
  - `next dev` lager `frontend/AGENTS.md` på nytt når den oppdager en KI-agent. Det er slått av med `agentRules: false`.
  - Rad 4 i matrisen (port 8000 opptatt) har fått en test.
  - 404-testen sammenligner nå proxy-svaret byte for byte med backendens eget svar.
- Rettet etter review (6 patcher):
  - `cacheComponents` og `partialPrefetching` er fjernet. De var lagt til uten bestilling, og malen har tom konfig.
  - Ny `e2e/database.spec.ts` beviser at utviklerdatabasen ikke røres. Den gamle `git status`-sjekken kunne aldri slå ut, fordi `*.db` er gitignored.
  - Playwright starter frontend med `--port 3000`.
  - Skanningen etter forbudte strenger dekker nå alle filer i appmappene og rotkonfigene.
  - En test sjekker at alle pakker er låst med `~`.
  - 404-testen sammenligner også `content-type`.
- 13 reviewfunn er avvist, med begrunnelse i speccens Review Triage Log.
- Rad 4 er også prøvd i praksis: med en annen prosess på port 8000 stopper Playwright med «already used», og `backend/data/prognos.db` er urørt.
- Verifisert: Vitest 15/15, `tsc --noEmit` er grønn, `npm run build` lykkes, og Playwright 4/4. `backend/data/prognos.db` har uendret mtime.
- Speccen er `done`. Koden ligger i `97aa02e`.
- Mathias sjekket proxyen og testene selv, og Story 1.2 er satt til `done` i sprint-status. Innførselen i `docs/ki-logg.md` dekker det som ble bygget, alle 20 reviewfunn (6 rettet, 13 avvist, 1 utsatt) og den utsatte feilen med liten stasjonsbokstav (`3d32048`).

### Åpne punkter
- `npm test` i `frontend/` feiler når arbeidsmappa har liten stasjonsbokstav (`c:\…`). Story 1.3 skal ta det i README. Rundgangene er testet:
  - PowerShell virker alltid, og det er standardterminalen i VS Code.
  - cmd virker med `cd /d C:\…`.
  - Git Bash virker med `cd /C/…`.

  En fiks i skriptet med `process.chdir(fs.realpathSync.native('.'))` virker, men er ikke enkel. Detaljene står i `issues.md`, og punktet er også ført i `deferred-work.md`.
