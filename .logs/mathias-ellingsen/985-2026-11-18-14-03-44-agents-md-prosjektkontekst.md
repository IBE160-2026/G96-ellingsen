# AGENTS.md med prosjektkontekst

## 2026-11-18 kl. 14:03 — Mathias Ellingsen

### Oppgave
Kjøre `bmad-project-context` og få reglene fra CLAUDE.md, også R1–R3, inn i en verifisert agentinstruks. Målet er én fil som agentene alltid laster.

### Plan
- Adopt: CLAUDE.md hadde innhold, men det fantes ingen AGENTS.md. Hver instruksjon i CLAUDE.md ble en post i ledgeren.
- Leste README, retroen for Epic 1, ARCHITECTURE-SPINE.md, testene i `test_repo.py`, `test_importer.py` og `oppsett.test.ts`, `next.config.ts`, `playwright.config.ts`, `issues.md` og sesjonslogg 988.
- Intervjuet dekket commit og språk, hvilke KI-verktøy gruppen bruker, KI-loggen og frosne mapper.

### Resultat
- Ny `AGENTS.md` med en styrt blokk (`<!-- bmad:context -->`, verifisert mot `0a307b7`). Den inneholder orientering, policy, R1–R3 ordrett, hvor ting er og ett punkt om Playwright.
- `CLAUDE.md` er redusert til `@AGENTS.md`. Gruppen bruker bare Claude Code, som henter inn AGENTS.md gjennom den importen.
- Hvor instruksjonene i CLAUDE.md havnet:
  - Sesjonslogg, R1–R3 og subagenter i `bmad-build` står ordrett i blokken.
  - «Gruppens egne regler gjelder foran dette» er erstattet av selve reglene: norsk i alt, og commit bare på bestilling. `sesjonslogg` er et uttalt unntak, godkjent av Mathias.
- Nye regler fra intervjuet:
  - En ny innførsel i `docs/ki-logg.md` per story som settes til `done`, og etter retro.
  - Tidligere innførsler i ki-loggen og rader i beslutningsloggen skrives aldri om.
  - `_bmad/`, `.claude/skills/`, planleggingsdokumentene og de genererte testdatafilene (SM-C1) endres ikke for hånd.
- Fra AD-11: ingen kode leser miljøvariabler.
- Utelatt fordi tester allerede håndhever det: at `domene/` er ren, at `next` er låst til 16.4.6, `~`-låsing og `agentRules: false`.
- To kandidater ble prøvd og forkastet, fordi `npm test` fra Git Bash med `/c/…` og ren `pytest` begge virket her.
- `uv run pytest tests/test_repo.py`: 13/13 grønne.
- README sier nå om Git Bash at `cd /c/…/frontend` kan feile, avhengig av hvordan terminalen startes, og anbefaler fortsatt `/C/…`. Det lukker punktet i `issues.md`. AGENTS.md, CLAUDE.md og README ligger i `eb8aeb7`.

### Åpne punkter
Ingen.
