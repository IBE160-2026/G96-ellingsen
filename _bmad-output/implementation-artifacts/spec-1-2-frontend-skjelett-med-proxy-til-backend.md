---
title: 'Story 1.2: Frontend-skjelett med proxy til backend'
type: 'feature'
created: '2026-11-17'
status: 'done'
baseline_commit: '9126a017f3226a327203a3fa5a87794a4d028123'
route: 'dispatch'
review_loop_iteration: 0
context:
  - '{project-root}/_bmad-output/implementation-artifacts/epic-1-context.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Repoet har bare backend. Sensor kan ikke åpne appen i nettleseren, og Epic 6 har ingen Next-app, proxy eller testoppsett (Vitest, Playwright) å bygge dashbordet på.

**Approach:** Lag `frontend/` med `create-next-app@16.4.6` (App Router, TypeScript, Tailwind v4) og `shadcn init`. Fjern Google-fonter, sett `lang="nb"` og en norsk plassholder med ordmerket «PROGNOS». `next.config.ts` får rewrite til backend og de to `experimental`-opsjonene (AD-11). Vitest sjekker oppsettet, og Playwright kjører mot ekte backend på en midlertidig databasefil (AD-14).

## Boundaries & Constraints

**Always:** `"next": "16.4.6"` eksakt. Øvrige pakker følger *Stack*-tabellen, låst på minor med `~` (f.eks. `~19.3.1`), og `package-lock.json` committes. Frontend kaller bare relative `/api/*`. Bare systemfonter. Ingen kode leser `process.env`, heller ikke `playwright.config.ts` eller `vitest.config.ts`. Brukertekster på norsk.

**Never:** Ingen dashbord, API-klient, TanStack Query, zod, Recharts eller designtokens (Epic 6). Ingen route handlers eller Server Actions. Ingen CORS i backend, og ingen endring i `backend/`. Ingen endring i rot-README (Story 1.3). Ingen `next/font/google`, CDN eller eksterne URL-er i appkoden.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Helse via proxy | Backend på 8000, `GET localhost:3000/api/health` | `200 {"status": "ok"}` fra backend | N/A |
| Ukjent API-sti via proxy | `GET localhost:3000/api/finnes-ikke` | Backendens `404 {"detail": "<norsk>"}` sendes uendret videre | N/A |
| Forside | `GET localhost:3000/` | `<html lang="nb">`, synlig «PROGNOS» | N/A |
| Port 8000 opptatt ved `npx playwright test` | Utviklerens backend kjører | Playwright stopper med feil, bruker aldri utviklerens database | `reuseExistingServer: false` |

</frozen-after-approval>

## Code Map

- `backend/src/prognos/__main__.py` -- `python -m prognos --db STI --port N`; lytter på `127.0.0.1`. Brukes av Playwright, endres ikke
- `backend/src/prognos/api/helse.py` -- `GET /api/health` → `{"status": "ok"}`
- `.gitignore` (rot) -- dekker allerede `node_modules/`, `.next/`, `next-env.d.ts`, `test-results/`, `playwright-report/`, `.env*`
- Lokalt miljø: Node 26.13.1, npm 11.20.0. Alle låste versjoner finnes i npm (next 16.4.6, react 19.3.1, typescript 5.9.3, tailwindcss 4.3.5, vitest 5.1.0, @playwright/test 1.65.1, shadcn 4.23.0). Playwright-nettleserne er ikke installert.

## Tasks & Acceptance

**Execution:**
- [x] `frontend/` -- `npx create-next-app@16.4.6 frontend --ts --tailwind --app --no-src-dir --import-alias "@/*" --use-npm`, uten linter; deretter `npx shadcn@4.23.0 init` (base-farge neutral) -- AD-11-oppsett
- [x] `frontend/package.json` -- `next` eksakt; react/react-dom `~19.3.1`, typescript `~5.9.3`, tailwindcss og `@tailwindcss/postcss` `~4.3.5`; dev: vitest `~5.1.0`, `@playwright/test` `~1.65.1`; scripts `predev`/`prebuild`: `next telemetry disable`, `test`: `vitest run` -- låste versjoner, telemetri av
- [x] `frontend/next.config.ts` -- rewrite `/api/:path*` → `http://127.0.0.1:8000/api/:path*`, `experimental: { proxyTimeout: 130000, agentUpgrade: false }` -- AD-11
- [x] `frontend/app/layout.tsx`, `app/globals.css` -- fjern `next/font/google` og Geist-variabler; `<html lang="nb">`; norsk `metadata` med tittel «PROGNOS» -- systemfonter
- [x] `frontend/app/page.tsx` -- enkel norsk plassholder med ordmerket «PROGNOS» -- UX for Epic 1
- [x] Malrester -- slett `frontend/README.md`, ubrukte SVG-er i `public/` og eventuelle `AGENTS.md`/`CLAUDE.md` fra malen -- ingen engelsk boilerplate
- [x] `frontend/vitest.config.ts`, `frontend/tests/oppsett.test.ts` -- miljø `node`, bare `tests/**/*.test.ts`. Tester: `next` er `16.4.6`; `next.config.ts` gir riktig rewrite og `experimental`; ingen fil under `app/`, `components/`, `lib/` inneholder `next/font/google`, `process.env` eller `http://`/`https://` -- storyens Vitest-tester
- [x] `frontend/playwright.config.ts`, `frontend/e2e/helse.spec.ts`, `frontend/e2e/forside.spec.ts` -- Chromium; `webServer`: backend `uv run python -m prognos --db <os.tmpdir()>/prognos-e2e/<tidsstempel>.db --port 8000` med `cwd` `../backend`, vent på `http://127.0.0.1:8000/api/health`; frontend `npm run dev`, vent på `http://localhost:3000`; begge `reuseExistingServer: false`. Testene dekker matrisen -- AD-14

**Acceptance Criteria:**
- Given installert frontend, when `npm test` kjøres fra `frontend/`, then alle Vitest-tester er grønne.
- Given installerte Playwright-nettlesere og ingen prosess på 8000/3000, when `npx playwright test` kjøres fra `frontend/`, then begge serverne startes, testene er grønne, og `backend/data/prognos.db` er ikke rørt.
- Given `npm run build`, when det kjøres, then bygget lykkes uten nettkall til Google Fonts.

## Implementation Notes

- `next dev` i 16.4.6 skriver `frontend/AGENTS.md` på nytt når den oppdager en KI-agent. `agentRules: false` i `next.config.ts` slår det av, og Vitest sjekker at innstillingen står. Uten den kom fila tilbake etter hver Playwright-kjøring.
- `cacheComponents` og `partialPrefetching` var lagt til uten bestilling og er fjernet i review (triage #1). Malen har tom konfig.
- `e2e/database.spec.ts` erstatter `git status`-sjekken som bevis på at utviklerdatabasen ikke røres. `*.db` er gitignored, så `git status` kunne aldri slå ut.
- shadcn init la til `shadcn`, `cn`, `radix-ui`, `lucide-react`, `class-variance-authority` og `tw-animate-css`. `@types/*` kom fra create-next-app. Alle er låst på minor med `~`.
- Matrise-rad 4 (port opptatt) dekkes av en Vitest-test som låser `reuseExistingServer: false` og temp-databasen. Den er ikke prøvd med en faktisk opptatt port. Rad 2 sammenligner proxy-svaret byte for byte med backendens eget 404-svar.
- `vitest run` feiler (`Cannot read properties of undefined (reading 'config')`) når arbeidsmappa har liten stasjonsbokstav (`c:\...`, typisk i cmd og VS Code). Med `C:\...` er den grønn. Feilen ligger i Vitest/Vite, ikke i koden.

## Spec Change Log

## Review Triage Log

Iterasjon 1 (lag: blind-hunter, edge-case-hunter, verification-gap). Sjekket mot treet 2026-11-18.

| # | Lag | Funn | Dom | Rute | Belegg |
|---|-----|------|-----|------|--------|
| 1 | blind | `cacheComponents`/`partialPrefetching` i `next.config.ts` er ikke bestilt | medium | patch | Malen i create-next-app 16.4.6 (`templates/app-tw/ts/next.config.ts`) har tom konfig, så de to linjene er lagt til av oss. Cache Components endrer renderingsmodellen Epic 6 arver. Fiks: slett linjene. |
| 2 | verification-gap, blind | AK «`backend/data/prognos.db` er ikke rørt» sjekkes med `git status`, som aldri kan feile | medium | patch | `git check-ignore` gir `.gitignore:68:backend/data/*.db`. Fiks: en e2e-test som finner temp-databasen og krever at utviklerdatabasen ikke er endret etter at den ble laget. |
| 3 | edge | `npm run dev` bytter til 3001 når 3000 er opptatt | low | patch | `next-dev.js:301`: porten byttes bare når verken `--port` eller `PORT` er satt. Playwright venter da på 3000 til tidsavbrudd. Fiks: `--port 3000`. |
| 4 | edge, blind | Skanningen etter forbudte strenger er smalere enn *Always*-regelen | low | patch | Den filtrerer på filendelse (`.json`/`.svg`/`.md` slipper gjennom) og skanner ikke rotkonfigene etter `process.env`. Fiks: skann alle filer i mappene, og rotkonfigene for `process.env`. |
| 5 | blind | `~`-låsingen er ikke testet | low | patch | `npm install x` legger til `^` som standard, så Epic 6 vil fort møte dette. Fiks: en test over alle avhengigheter. |
| 6 | blind | 404-testen sammenligner ikke `content-type` | low | patch | Bare kroppen sammenlignes. Fiks: én påstand om lik `content-type`. |
| 7 | blind | Git Bash-feilen i Vitest er ikke fulgt opp | medium | defer | Reprodusert: `c:\` feiler, `C:\` er grønn, og cmd feiler. Feilen ligger i verktøyet, ikke i storyens kode. |
| 8 | edge | `statSync` kaster på ødelagt symlenke | low | avvist | Lite sannsynlig, og fiksen legger til en vakt. |
| 9 | edge | Trailing slash gir 308 før rewrite | low | avvist | Frontend kaller bare stier uten skråstrek. Fiksen legger til konfig. |
| 10 | edge | `localhost` løses til `::1` | false | avvist | `next dev` lytter dual-stack, og Playwright nådde `localhost:3000` i tre kjøringer. |
| 11 | edge | Installert next kan avvike fra package.json | low | avvist | `package-lock.json` låser versjonen. Lite sannsynlig. |
| 12 | blind | `package-lock.json` mangler i diffen | false | avvist | Fila ligger på disk. Den var bare holdt utenfor review-diffen som generert. |
| 13 | blind | Sprint-status er ikke `review` | false | avvist | Status synkes i presentasjonssteget. |
| 14 | blind | `agentRules` og ekstra avhengigheter er avvik fra speccen | false | avvist | `agentRules` kreves for at Malrester-oppgaven skal holde. Avhengighetene kommer fra `shadcn init`, som speccen ber om. |
| 15 | blind | `button.tsx` er ubrukt malrest | false | avvist | Den er output fra `shadcn init`, som speccen ber om. Ingen navngitt skade. |
| 16 | blind | Rad 4 (port 8000 opptatt) er ikke prøvd i praksis | false | avvist | Prøvd 2026-11-18 med en dummy på 8000. Playwright stopper med «…/api/health is already used», og `prognos.db` har uendret mtime. |
| 17 | blind | `@types/node` 22 mot Node 26 | false | avvist | `tsc --noEmit` er grønn. Ingen navngitt skade. |
| 18 | blind | `next telemetry disable` skriver global konfig | — | avvist | Speccen ber om det. Fiksen ville vært en specendring. |
| 19 | blind | Gamle temp-databaser hoper seg opp | — | avvist | Design Notes godtar det. Fiksen ville vært en specendring. |
| 20 | verification-gap (annet) | Ingen CI kjører e2e | false | avvist | Det er i tråd med hvordan repoet verifiserer i dag. Ingen defekt i denne endringen. |

## Design Notes

Den midlertidige databasestien regnes ut i `playwright.config.ts` med `os.tmpdir()` og `Date.now()`. Konfigen evalueres på nytt i hver worker og gir da en annen sti, men bare hovedprosessen starter `webServer`, så det er ufarlig. Backend lager selv mappen og fila. Gamle filer blir liggende i OS-temp. Det er akseptert. TanStack Query, zod, Recharts og react-is installeres i Story 6.1, der de tas i bruk.

## Verification

**Commands:**
- `cd frontend && npm test` -- expected: grønt
- `cd frontend && npx playwright install chromium && npx playwright test` -- expected: grønt
- `cd frontend && npm run build` -- expected: bygget lykkes
- `cd frontend && npx playwright test e2e/database.spec.ts` -- expected: grønt (beviser at `backend/data/prognos.db` ikke røres; `git status` kan ikke vise det, fordi `*.db` er gitignored)
