<!-- bmad:context -->
<!-- Verifisert 2026-11-18 mot 0a307b7. Styres av bmad-project-context; endringer inne i blokken erstattes ved refresh. Det du vil beholde, legger du utenfor markørene. -->

## G96-ellingsen – PROGNOS

Gruppeprosjekt i IBE160. PROGNOS lager salgsprognoser for småbedrifter og kjører helt lokalt. Backend er FastAPI, statsforecast og SQLite (uv, Python 3.12) i `backend/`, og frontend er Next.js 16.4.6 i `frontend/`. Planleggingen ligger i `_bmad-output/planning-artifacts/`. Ved konflikt gjelder beslutningsloggen i `docs/research/research-plan.md` først, så PRD-en og så arkitekturspinen.

## Policy

- Skriv norsk i alt: commit-meldinger, dokumenter, brukertekster og identifikatorer. I identifikatorer skrives æ, ø og å som `ae`, `oe` og `aa` (`maaned`, `historikknivaa`).
- Commit bare når brukeren ber om det. Unntaket er `sesjonslogg`-skillen, som committer loggfila lokalt. Push gjør du selv.
- Når en oppgave eller økt avsluttes, og før sluttoppsummeringen: bruk `sesjonslogg`-skillen. Dokumenter Oppgave + Plan + Resultat + åpne punkter i `.logs/<bruker>/`, og før åpne punkter i `.logs/<bruker>/issues.md`.
- Når en story settes til `done`, og etter en retro: legg til en ny innførsel i `docs/ki-logg.md`.
- Ikke skriv om tidligere innførsler i `docs/ki-logg.md` eller eksisterende rader i beslutningsloggen. Før endringer som nye innførsler eller nye rader.
- Ikke endre `_bmad/` eller `.claude/skills/` for hånd. Bruk installasjonen eller `bmad-customize`.
- Ikke endre PRD-, arkitektur- og UX-dokumentene under `_bmad-output/planning-artifacts/` for hånd. Bruk skillen som eier dokumentet, eller `bmad-correct-course`.
- Ikke endre de genererte testdatafilene (`testdata/syntetisk.csv`, `fasit.json`, `uten_stoy.csv`) for hånd. Kjør generatoren på nytt. Data, seed og intervallnivå justeres aldri for å få en test grønn (SM-C1).
- Ingen kode leser miljøvariabler. Stier, porter og frister er konstanter i `backend/src/prognos/konstanter.py` og `frontend/next.config.ts` (AD-11).
- `bmad-build` bruker alltid subagenter til å kompilere konteksten og til uavhengig kodegjennomgang, uten å spørre først.

Regler fra retroen for Epic 1 (`_bmad-output/implementation-artifacts/epic-1-retro-2026-11-18.md`):

- **R1 – Ingen innstillinger uten bestilling.** Hver ny linje i konfig, avhengigheter eller flagg skal kunne vises til i speccen eller i verktøyets egen mal. Det gjelder også verktøy som endrer repoet på egen hånd (for eksempel `next dev`, som skrev `AGENTS.md`). Reviewen spør for hver slik linje: «Hvem ba om denne?»
- **R2 – En test teller først når den er sett feile.** Før en akseptkriterietest regnes som bevis, skal den ha vært rød: brekk betingelsen eller bytt inn feil data. En sjekk som ikke kan slå ut, som `git status` mot en gitignored fil, er ikke bevis. Fasittester skal sammenligne med uavhengige konstanter, ikke med kodens egen output.
- R3 – Kommandoer verifiseres i PowerShell. README anbefaler PowerShell. Nye kommandoer i en spec eller README kjøres der før storyen settes til `done`.

## Hvor ting er

- Bindende arkitektur (AD-1–AD-15): `_bmad-output/planning-artifacts/architecture/architecture-G96-ellingsen-2026-11-17/ARCHITECTURE-SPINE.md`
- Sprintstatus, specs per story og utsatte funn: `_bmad-output/implementation-artifacts/` (`sprint-status.yaml`, `spec-*.md`, `deferred-work.md`)

## Kjøring og verifisering

- Stopp backend og frontend før `npx playwright test`. Den starter begge selv på port 8000 og 3000 mot en midlertidig database, og stopper med «already used» hvis en port er tatt.

<!-- /bmad:context -->
