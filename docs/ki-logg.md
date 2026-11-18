# KI-logg

Logg over hvordan KI er brukt i prosjektet, og hvilke valg gruppen har tatt selv.

## 2026-11-14 — PRD for PROGNOS v1

**Økt:** Laget PRD med `/bmad-prd` (Claude Code), fast path og full gjennomgang i ferdigstillingen. Grunnlaget var PRODUCT_BRIEF.md, faglærers tilbakemelding, beslutningsloggen i research-plan.md og arkitekturutkastet.

**Hva KI-en gjorde:**
- Skrev utkastet til PRD-en: 4 brukerreiser med Kari, FR-1–FR-25, NFR-ene, F1–F14 koblet til kravene og en sporbarhetstabell.
- Kjørte tre gjennomganger som subagenter: avstemming mot brief og tilbakemelding, avstemming mot beslutningslogg og arkitekturutkast, og en kvalitetsgjennomgang mot PRD-rubrikken. Den samlet funnene til 8 høye (H1–H8) og rundt 25 middels og lave.
- Rettet funnene, språkvasket PRD-en og addendum, og førte nye beslutninger inn i beslutningsloggen.

**Valg jeg tok:**
- F1–F14 som akseptansekriterier i stedet for F1–F12, fordi F13 og F14 også er v1-krav.
- H1: Produkter med 12–17 måneders historikk får ingen backtest.
- H2: WAPE vises som «–» når faktisk salg er 0, og produktet står rett etter de flaggede.
- H3: Intervalldekningen regnes per modell og over de samme produktene som WAPE, og F8 gjelder ETS.
- Godkjente rettingene av H4–H8. H6 ble utsatt til arkitekturen.
- Total WAPE regnes over de samme produktene for ETS og baseline, altså bare produkter med backtest for begge modellene.
- Godkjente presiseringene i PRD §11.2.

**Forslag fra KI-en som jeg endret eller presiserte:**
- KI-en foreslo å utsette spørsmålet om total WAPE til arkitekturen. Jeg avgjorde det i PRD-en med en gang og førte det i beslutningsloggen.
- KI-en foreslo rekkefølgen i produktlisten (flaggede øverst). Jeg godkjente den og ba om at den ble ført i beslutningsloggen.
- Jeg ba KI-en sjekke F12 mot NFR-1. Etter det ble NFR-1 presisert: kravet om ingen nettverkstilgang gjelder mens appen kjører, ikke under installasjonen.
- Jeg fjernet «(steg 4) og epics og stories» fra formålet i §0.

**Kilder:**
- Sesjonslogg: [.logs/mathias-ellingsen/996-2026-11-14-19-57-25-prd.md](../.logs/mathias-ellingsen/996-2026-11-14-19-57-25-prd.md)
- Rapportene fra gjennomgangen ligger i [_bmad-output/planning-artifacts/prds/prd-G96-ellingsen-2026-11-14/](../_bmad-output/planning-artifacts/prds/prd-G96-ellingsen-2026-11-14/):
  - `review-rubric.md`
  - `reconcile-brief-tilbakemelding.md`
  - `reconcile-beslutningslogg-arkitektur.md`
  - `.memlog.md`

## 2026-11-14 — Spike for backtest-oppsettet

**Økt:** Ba Claude Code lage og kjøre et testskript som bekrefter backtest-oppsettet i beslutningsloggen. Svarer på åpent spørsmål 1 i PRD §10.

**Hva KI-en gjorde:**
- Skrev [spikes/backtest_spike.py](../spikes/backtest_spike.py): 3 syntetiske produkter med 36 måneder (sesong, trend, støy), AutoETS og SeasonalNaive fra statsforecast, rullerende backtest med 6 opprinnelser og horisont 1, WAPE og P10–P90-dekning med 80 % intervall og nullgrense.
- Kjørte skriptet med `uv run`. Med seed 42 holdt F7 (WAPE 0,074 mot 0,112), men F8 holdt ikke (dekning 61,1 %).
- Kjørte på eget initiativ 20 seeds for å se om resultatet var tilfeldig. F7 og F8 holdt begge i 18 av 20. La deretter til `--seeds` i skriptet, slik at resultatet kan kjøres på nytt.
- Skrev resultatene i [docs/research/teknisk.md](research/teknisk.md), og oppdaterte PRD §10 og beslutningsloggen.

**Valg jeg tok:**
- Spiken committes som en del av researchen.
- Backtest-spørsmålet i PRD §10 regnes som besvart, og beslutningsloggen for backtesten endres ikke.
- Seeden for det syntetiske datasettet er 42. Den er valgt før datasettet er generert og endres ikke etter at resultatene er sett. Ført i beslutningsloggen.

**Forslag fra KI-en som jeg endret eller presiserte:**
- KI-en lot spiken være ukommittert fordi jeg kalte den et eksperiment. Jeg bestemte at den skal committes.

**Kilder:**
- Sesjonslogg: [.logs/mathias-ellingsen/995-2026-11-14-20-11-22-backtest-spike.md](../.logs/mathias-ellingsen/995-2026-11-14-20-11-22-backtest-spike.md)

## 2026-11-14 — UX-spesifikasjon for dashbordet

**Økt:** Laget UX-spesifikasjon med `/bmad-ux` (Claude Code) i rask modus, basert på `prd.md` og `addendum.md`. Primærbruker er Kari, og reisene er UJ-1 til UJ-4. Resultatet er `DESIGN.md` (utseende), `EXPERIENCE.md` (atferd) og to HTML-mockups.

**Hva KI-en gjorde:**
- Trakk ut det UX-relevante fra PRD og addendum med en subagent, og pekte på hull PRD-en ikke dekker: form-faktor, lastetilstand, søk, tilgjengelighet og visuell retning.
- Skrev utkast til `DESIGN.md` og `EXPERIENCE.md` med 19 `[ASSUMPTION]`-merker, som jeg gikk gjennom.
- Kjørte to gjennomganger som subagenter: en rubrikk-gjennomgang (adequate; 0 kritiske, 3 høye, 15 middels, 23 lave) og en tilgjengelighetsgjennomgang mot WCAG 2.1 AA (godkjent med endringer; 0 kritiske, 5 høye, 9 middels, 8 lave). Funnene ble samlet i en valideringsrapport med 63 funn etter sammenslåing (0/7/21/35).
- De 7 høye funnene var:
  - dommerlinjen i backtest-tabellen håndterte ikke lik WAPE
  - inndatakanter med kontrast 1,38:1
  - for svak fokusring fra shadcn
  - ingen modell for høyde og scrolling
  - grafen var både bilde og fokuserbar
  - fokus forsvant etter lastetilstanden
  - reflow var bare dekket for 200 % zoom
- Rendret to mockups (dashbordet med P-109 valgt, og avvist fil med lastetilstand). Arbeidet med dem avdekket blant annet et eksempel med feil tall: fordelingen per historikknivå stemte ikke med antall flaggede.
- Tok inn alle høye og middels funn, oppdaterte mockupene og kontrollerte tallene i dem med skript. Kjørte til slutt en språkgjennomgang av struktur og prosa.

**Valg jeg tok:**
- Form-faktor: desktop og laptop, ned til 1280 px bredde. Ikke nettbrett eller mobil i v1.
- Lastetilstand: en enkel spinner med tekst, og resten av siden deaktivert. Ikke trinnvis fremdrift, fordi det krever ekstra backend-logikk.
- Søk: et enkelt søkefelt som filtrerer produktlisten på `produkt_id`, med sorteringen beholdt. Dette er et tillegg utover PRD-en, og jeg legger det inn som nytt FR.
- Tilgjengelighet: WCAG 2.1 AA (kontrast, tastatur, etiketter, flagg med ikon og tekst). Ingen mørk modus i v1.
- Visuell retning: nøktern og Excel-nær, nøytrale grå nyanser og én blå aksentfarge, høyrejusterte tall med faste sifferbredder og norsk tallformat.
- Grafen er et bilde som ikke kan fokuseres. Under den ligger «Vis historikk som tabell» som tekstalternativ.
- Hele siden scroller, og produktlisten er sticky. Valideringsrapporten er foldet sammen til oppsummeringslinjen.
- Lasteteksten er alltid den generelle: «Kjører validering og prognose – dette kan ta opptil ett minutt».
- De lave funnene fra gjennomgangene ble bevisst ikke tatt inn. Jeg ba bare om de høye og middels. Noen få lave ble likevel rettet underveis.

**Forslag fra KI-en som jeg endret eller presiserte:**
- Antakelse 2: KI-en foreslo at ingen produkter skulle være valgt etter innlasting, slik UJ-1 beskriver. Jeg endret det til at første rad i produktlisten velges automatisk. UJ-1 i PRD-en må oppdateres.
- Antakelse 3: KI-en foreslo WAPE i hele prosent, som i PRD-eksemplene. Jeg endret det til én desimal (for eksempel 7,4 %).
- Jeg ønsket opprinnelig at lasteteksten skulle vise antall produkter. Gjennomgangen viste at frontend ikke kjenner antallet før svaret kommer, fordi alt sendes i én forespørsel (FR-7). Jeg valgte derfor den generelle teksten.
- KI-en anbefalte løsningene for graf og scrolling. Jeg valgte de anbefalte alternativene.

**Kilder:**
- Sesjonslogg: [.logs/mathias-ellingsen/994-2026-11-14-21-07-06-ux-spesifikasjon.md](../.logs/mathias-ellingsen/994-2026-11-14-21-07-06-ux-spesifikasjon.md)
- UX-filene ligger i [_bmad-output/planning-artifacts/ux-designs/ux-G96-ellingsen-2026-11-14/](../_bmad-output/planning-artifacts/ux-designs/ux-G96-ellingsen-2026-11-14/):
  - `DESIGN.md` og `EXPERIENCE.md`
  - `mockups/key-dashbord.html` og `mockups/key-avvist.html`
  - `review-rubric.md`, `review-tilgjengelighet.md` og `validation-report.md`/`.html`
  - `.memlog.md`

## 2026-11-17 — PRD oppdatert med endringer fra UX-økten

**Økt:** Oppdaterte PRD-en med `/bmad-prd` (Claude Code), med Update-intent og lett gjennomgang. Grunnlaget var de to åpne PRD-punktene fra UX-økten.

**Hva KI-en gjorde:**
- La inn det nye kravet FR-26 *Søk i produktlisten* i §4.5, og oppdaterte UJ-1 steg 4 slik at første produkt velges automatisk.
- La FR-26 inn i fire rader i sporbarhetstabellen §9.1, og førte de to beslutningene inn i beslutningsloggen i research-plan.md.
- Sjekket FR-26 mot FR-19 og EXPERIENCE.md. Ingen funn.

**Valg jeg tok:**
- FR-26 får egen ID og ikke en omnummerering, slik at de eksisterende ID-ene står fast.
- Kravet har testbare regler: «inneholder», uavhengig av store og små bokstaver, FR-19-rekkefølgen beholdes, og valgt produkt blir stående. Teller, Esc og forsinkelse blir i UX-dokumentet.
- §0 og NFR-6 er oppdatert til FR-1 til FR-26, slik at søkekravet også dekkes av testkravet.

**Forslag fra KI-en som jeg endret eller presiserte:**
- Ingen. KI-en påpekte at «ikke endre noe annet» ville gjøre §0 og NFR-6 utdatert, og jeg valgte å oppdatere dem.

**Kilder:**
- Sesjonslogg: [.logs/mathias-ellingsen/996-2026-11-14-19-57-25-prd.md](../.logs/mathias-ellingsen/996-2026-11-14-19-57-25-prd.md)
- [prd.md](../_bmad-output/planning-artifacts/prds/prd-G96-ellingsen-2026-11-14/prd.md) og [research-plan.md](research/research-plan.md)

## 2026-11-17 — Arkitektur for PROGNOS v1

**Økt:** Laget arkitekturen med `/bmad-architecture` (Claude Code), coaching path. Grunnlaget var PRD, addendum, UX-spesifikasjonen, beslutningsloggen, teknisk.md, issues.md og arkitekturutkastet. Rammene var SQLite, ingen Docker og statsforecast som eneste ML-bibliotek.

**Hva KI-en gjorde:**
- La fram alternativene for de bærende valgene i to runder, med en anbefaling for hvert.
- Sjekket versjonene mot PyPI og npm og leste kildekoden til Next.js. Fant at statsforecast 2.1.1 krever `pandas<3`, og at rewrite-proxyen i Next.js bryter forespørsler etter 30 s.
- Skrev ARCHITECTURE-SPINE.md med AD-1 til AD-15. Den løser H6 (total WAPE, verdier per opprinnelse, oppsummering og lagret rapport) og de 5 punktene der utkastet var utdatert.
- Kjørte fem uavhengige gjennomganger som subagenter: avstemming mot PRD, avstemming mot UX og logg, rubrikk, teknologiverifisering og et adversarialt angrep. Rettet funnene.
- Kjørte to små eksperimenter med statsforecast. Det ene avkreftet et påstått kritisk funn (NaN ved 12 måneder). Det andre viste at AutoETS takler null-serier og konstante serier.
- Skrev en forklaring for sensor og språkvasket den med `bmad-review`.

**Valg jeg tok:**
- Functional core, imperative shell med pipeline, og alt lagres i én transaksjon.
- WAPE, dekning, totaler og rekkefølge regnes én gang ved opplasting og lagres. API og frontend regner aldri på nytt.
- P10/P50/P90 rundes til heltall før metrikkene regnes ut, slik at tallene Kari ser, kan regnes etter (NFR-5).
- `create_all` med versjonsvakt i stedet for Alembic.
- Seks endepunkter, der rapporten og WAPE-oversikten kommer fra `GET /api/datasets/{id}`.
- Pydantic er kontrakten, og zod speiles for hånd.
- Modellkjøringen går i trådpool, med én opplasting om gangen.
- Norsk snake_case helt ut i frontend.
- Kildene oppstrøms oppdateres: ny rad i beslutningsloggen, PRD §11.3, addendum og en merknad om at utkastet er erstattet.

**Funn fra gjennomgangen som ble rettet:**
- **Avhengigheter:** `sqlalchemy[asyncio]` og `python-multipart` manglet. Uten dem ville backend ikke startet.
- **Tidsavbrudd:** Klienten ga opp etter 120 s, men serveren kunne likevel lagre. Nå forkaster serveren resultatet etter 110 s, slik at «Ingenting er lagret» stemmer.
- **Feilsvar:** FastAPIs egne feilsvar var engelske og hadde en annen form. Alle svar fra opplastingen har nå samme form med norsk melding, og klienten har faste regler for *Kjøring feilet* og *Ingen kontakt*.
- **Lagrede felt:** Scenariototal, `backtest_nivaa` og historikklengde manglet blant de lagrede feltene. «Lik WAPE» sammenlignes nå på heltall.
- **Tom mengde:** Når ingen produkter har backtest for begge modellene, er `m` og `n` 0 i stedet for `null`.
- **Regler for statsforecast:** dato, frekvens og opprinnelse, og hvordan produkter med ulik lengde kjøres i samme kall.
- **CSV-lesing:** radnummer, mellomrom og heltall, valg av skilletegn når en kolonne mangler, rekkefølgen på feil, og to nye feilmaler. Malene og teksten for 409 er ført inn i EXPERIENCE.md.
- **Skjema og tester:** Versjonsvakten kjører før `create_all`, testene bruker en egen database uten miljøvariabler, og generatoren lager byte-identiske filer på alle operativsystemer.
- **Next.js:** `next dev` sjekker versjoner mot npm. Dette er skrudd av der det går, og avgrenset i NFR-1.
- **Avvist funn:** Det kritiske funnet om NaN fra SeasonalNaive ved 12 måneder ble avkreftet med et eksperiment og ikke tatt inn.

**Forslag fra KI-en som jeg endret eller presiserte:**
- Leveransen: jeg ba om en forklaring for sensor i tillegg til spine-dokumentet. Jeg ba også om at utkastet ikke skulle skrives om, men få en merknad om at det er erstattet, slik at historikken kan spores.
- Etterpå ba jeg om at de nye feilmalene og teksten for «opplasting pågår» ble ført inn i EXPERIENCE.md med en gang, i stedet for å stå som åpent punkt.

**Kilder:**
- [ARCHITECTURE-SPINE.md](../_bmad-output/planning-artifacts/architecture/architecture-G96-ellingsen-2026-11-17/ARCHITECTURE-SPINE.md), [forklaring-for-sensor.md](../_bmad-output/planning-artifacts/architecture/architecture-G96-ellingsen-2026-11-17/forklaring-for-sensor.md) og `reviews/` i samme mappe

## 2026-11-17 — Epics og stories for PROGNOS v1

**Økt:** Laget epics og stories med `/bmad-create-epics-and-stories` (Claude Code). Grunnlaget var PRD med addendum, ARCHITECTURE-SPINE.md og UX-spesifikasjonen (DESIGN.md og EXPERIENCE.md). Arbeidet gikk i fire steg: kravuttrekk, epic-struktur, stories én epic om gangen og sluttvalidering. Jeg godkjente hvert steg og hver epic.

**Hva KI-en gjorde:**
- Hentet ut 26 FR, 9 NFR, AD-1 til AD-15 med konvensjonene, og 30 UX-designkrav (UX-DR1–UX-DR30) som egne krav.
- Foreslo seks epics i rekkefølgen jeg ga:
  1. prosjektskjelett og helsesjekk
  2. syntetisk datasett med seed 42
  3. CSV-import, validering og lagring
  4. prognose og scenarioer
  5. backtest
  6. dashbord
- Skrev 28 stories: Epic 1 (3), Epic 2 (2), Epic 3 (7), Epic 4 (3), Epic 5 (5) og Epic 6 (8).
- Hver story har feltene **Dekker** (FR, F, AD og eventuelt NFR og UX-DR) og **Tester i storyen**, i tillegg til akseptansekriterier på formen Given/When/Then. Testene skrives i samme story som koden.
- Hver tabell opprettes i den første storyen som trenger den, med ny `SKJEMAVERSJON` hver gang.
- Kjørte en maskinell dekningskontroll av alle FR, NFR, F, AD og UX-DR, og en sjekk av alle henvisningene mellom storyene.

**Valg jeg tok:**
- UX-DR-ene beholdes som egne krav for sporbarhet, men samles i stories etter skjermdel (topplinje, produktliste, graf, tabeller, WAPE-oversikt og tilgjengelighet), med hver UX-DR som akseptansekriterium. Det blir ikke én story per UX-DR.
- FR-7, FR-19, FR-22 og FR-24 deles over flere epics. Hver story som dekker en del av et slikt krav, sier hvilken del det er (*delvis: …*), og storyen som gjør kravet ferdig, er merket **(fullfører)**:
  - FR-7 (automatisk kjøring): Epic 3 → 4 → 5
  - FR-19 (rekkefølgen i produktlisten): Epic 3 → 5 → 6
  - FR-22 (WAPE-oversikten): Epic 5 → 6
  - FR-24 (innholdet i det syntetiske datasettet): Epic 2 → 4
- Godkjente at FR-19 også får en del i Epic 3. API-kontrakten krever `rang` fra første versjon, og uten WAPE er regelen enkel: flaggede produkter først, deretter etter `produkt_id`.
- Låste rekkefølgen i Epic 6 tidlig, fordi Epic 4 viser til storyen der merknaden om scenariototaler vises.

**Forslag fra KI-en som jeg endret eller presiserte:**
- **Story 3.4 delt.** KI-en hadde lagt lagring, lås og serverfrist i samme story. Jeg ba om at 409 (låsen) og serverfristen ble skilt ut i en egen story, som nå er 3.5. Storyene etter den fikk nytt nummer, og henvisningen i Story 1.3 ble rettet.
- **Story 6.2 delt.** Jeg ba om at de røde rapportvariantene (feilet kjøring, 409, tidsavbrudd og ingen kontakt) ble skilt ut i en egen story, som nå er 6.3. Storyene etter den fikk nytt nummer, og henvisningene i Epic 4 (merknaden fra FR-12) og Epic 5 (NFR-1) ble rettet.
- **NFR-1 rettet.** KI-en merket først NFR-1 som fullført i Story 5.5. Kravet om at UJ-1 fungerer uten nett trenger dashbordet, så kontrollen ble flyttet til den siste storyen i Epic 6.

**Funn fra sluttvalideringen som ble rettet:**
1. **Seedingen og låsen.** Story 3.5 krevde at seedingen tok samme lås, men seedingen lages først i 3.7. Kriteriet og testen er flyttet til 3.7.
2. **Antall endepunkter.** Story 5.4 snakket om «fem» lese-endepunkter, men det finnes fire. Teksten er rettet.
3. **Lastetilstand ved bytte av datasett.** Story 6.2 krevde `Skeleton` i produktlisten og WAPE-linjen, som først lages i senere stories. Kravet er fordelt på storyene for rapporten (6.2), produktlisten (6.4) og WAPE-oversikten (6.7).
4. **Produktvalg og graf.** Testen for produktlisten forutsatte at graf og tabeller fantes. Story 6.4 tester nå at valget endres og at produktdetaljen hentes. Story 6.6 fullfører FR-19 og FR-26 med testen om at graf og tabeller oppdateres.
5. **Testdata for *ETS taper*.** Testene i Epic 6 forutsatte at det syntetiske datasettet har et produkt der ETS taper. Det er ikke garantert, og dataene skal ikke justeres for det (SM-C1). Story 5.3 lagrer nå en konstruert fil, `backend/tests/data/ets_taper.csv`, og testene i Epic 6 laster opp den.

Etter rettingene ble kontrollen kjørt på nytt. Alt var dekket, ingen story avhenger av en senere story, og epics.md ble satt til final.

**Kilder:**
- Sesjonslogg: [.logs/mathias-ellingsen/992-2026-11-17-20-40-46-epics-og-stories.md](../.logs/mathias-ellingsen/992-2026-11-17-20-40-46-epics-og-stories.md)
- [epics.md](../_bmad-output/planning-artifacts/epics.md)

## 2026-11-17 — Story 1.1: Backend-skjelett med automatisk database og helsesjekk

**Økt:** Implementerte Story 1.1 med `/bmad-build` (Claude Code). KI-en skrev en spesifikasjon som jeg godkjente. Deretter implementerte en subagent den, og tre uavhengige reviewere gikk gjennom koden. Etterpå kjørte jeg testene og helsesjekken selv.

**Hva som ble bygget:**
- `backend/` som uv-prosjekt med versjonene fra arkitekturens *Stack*-tabell låst.
- `lag_app(db_sti)` som eneste app-fabrikk, og `python -m prognos --db STI --port N` (AD-14).
- En versjonsvakt før `create_all`. Databasefila og tabellen `skjemaversjon` opprettes automatisk, og et gammelt skjema stopper backend med den faste meldingen (AD-13).
- `GET /api/health` som svarer `{"status": "ok"}`, og norsk `{detail}` på HTTP-feil (AD-9).
- En importtest som sjekker at `domene/` ikke importerer `fastapi`, `sqlalchemy`, `prognos.api` eller `prognos.db` (AD-1).
- 19 pytest-tester, alle grønne.

**Gjennomgang:** De tre reviewerne ga 20 funn. 9 ble rettet: blant annet at en egen feiltekst fra en rute beholdes, at en sti med `#` eller `?` fungerer, flere tester for versjonsvakten og SQLite-sidefiler i `.gitignore`. 11 ble avvist med begrunnelse, fordi de var ikke-nåbare, feilet allerede høylytt eller gjaldt tekst som er fastsatt i arkitekturen. Hele triagen står i spesifikasjonen.

**Åpne punkter:**
- Valideringsfeil (422) og uventede unntak gir fortsatt FastAPIs engelske svar. Det må håndteres i Epic 3, når `POST /api/datasets` kommer (AD-9).
- `fastapi 0.163.2` i `uv.lock` ble publisert samme dag. Vi følger med på om det kommer en rask patch.

**Kilder:**
- Sesjonslogg: [.logs/mathias-ellingsen/990-2026-11-17-21-02-32-story-1-1-backend-skjelett.md](../.logs/mathias-ellingsen/990-2026-11-17-21-02-32-story-1-1-backend-skjelett.md)
- [Spesifikasjon for Story 1.1](../_bmad-output/implementation-artifacts/spec-1-1-backend-skjelett-med-automatisk-database-og-helsesjekk.md)

## 2026-11-18 — Story 1.2: Frontend-skjelett med proxy til backend

**Økt:** Implementerte Story 1.2 med `/bmad-build` (Claude Code). Arbeidet fortsatte fra en spesifikasjon jeg godkjente 2026-11-17. En subagent implementerte, KI-en kontrollerte diffen mot spesifikasjonen, og tre uavhengige reviewere gikk gjennom koden. Etterpå sjekket jeg proxyen og testene selv.

**Hva som ble bygget:**
- `frontend/` med Next 16.4.6 (App Router, TypeScript, Tailwind v4) og `shadcn init`. Bare systemfonter, `lang="nb"` og en norsk plassholder med ordmerket «PROGNOS».
- `next.config.ts` sender `/api/*` videre til `http://127.0.0.1:8000` og har `proxyTimeout: 130000` og `agentUpgrade: false` (AD-11). Frontend kaller bare relative `/api/*`, og ingen kode leser `process.env`.
- 15 Vitest-tester for oppsettet: eksakt next-versjon, `~`-låsing av de andre pakkene, rewrite, at Playwright aldri gjenbruker en kjørende server, og at appkoden er fri for Google-fonter, `process.env` og eksterne URL-er.
- 4 Playwright-tester mot ekte backend på en midlertidig databasefil (AD-14): helse gjennom proxyen, at backendens 404 sendes uendret videre, forsiden, og at utviklerens `backend/data/prognos.db` ikke røres.

**Rettet før review (KI-ens egen kontroll):**
- `next dev` lagde `frontend/AGENTS.md` på nytt hver gang den oppdaget en KI-agent, selv om malfilene skulle slettes. Det er slått av med `agentRules: false`.
- Kanttilfellet «port 8000 opptatt» hadde ingen test. Det er nå testet, og også prøvd i praksis: Playwright stopper med «already used».
- 404-testen sjekket bare formen på svaret. Nå sammenligner den proxy-svaret byte for byte med backendens.

**Gjennomgang:** Reviewerne ga 20 funn.
- **Rettet (6):**
  - `cacheComponents` og `partialPrefetching` var lagt til i `next.config.ts` uten bestilling. Malen har tom konfig. Begge er fjernet, fordi de endrer renderingsmodellen Epic 6 arver.
  - Kontrollen av at utviklerdatabasen ikke røres brukte `git status`, som aldri kan slå ut fordi `*.db` er gitignored. Den er erstattet med en e2e-test som sammenligner tidsstempler.
  - Playwright starter frontend med `--port 3000`, så `next dev` ikke flytter seg til 3001 i stillhet.
  - Skanningen etter forbudte strenger dekker nå alle filer og rotkonfigene.
  - En test sjekker `~`-låsingen.
  - 404-testen sammenligner også `content-type`.
- **Avvist (13):** De var feil, var allerede dekket, var bestemt i spesifikasjonen eller var lite sannsynlige med en dyr fiks. Eksempler: `localhost` mot `::1` (testene nådde `localhost:3000`), `button.tsx` (output fra `shadcn init`, som spesifikasjonen ber om) og at gamle temp-databaser blir liggende (godtatt i Design Notes).
- **Utsatt (1):** se åpne punkter.

Hele triagen står i spesifikasjonen.

**Åpne punkter:**
- `npm test` feiler med «Cannot read properties of undefined (reading 'config')» når arbeidsmappa har liten stasjonsbokstav (`c:\…`). Feilen ligger i Vitest/Vite, ikke i koden vår. Rundgangene er testet:
  - PowerShell virker alltid, og det er standardterminalen i VS Code.
  - cmd virker med `cd /d C:\…`.
  - Git Bash virker med `cd /C/…`.

  Story 1.3 skal beskrive dette i README. En fiks i skriptet finnes, men den er ikke enkel. Punktet er også ført i `deferred-work.md`.

**Kilder:**
- Sesjonslogg: [.logs/mathias-ellingsen/988-2026-11-18-13-30-39-story-1-2-frontend-skjelett.md](../.logs/mathias-ellingsen/988-2026-11-18-13-30-39-story-1-2-frontend-skjelett.md)
- [Spesifikasjon for Story 1.2](../_bmad-output/implementation-artifacts/spec-1-2-frontend-skjelett-med-proxy-til-backend.md)

## 2026-11-18 — Story 1.3: README, repohygiene og kontroll av oppstarten

**Økt:** Implementerte Story 1.3 med `/bmad-build` (Claude Code). Endringen var liten og hadde ingen åpne spørsmål, så KI-en valgte den korte ruten: spesifikasjon, implementering, én uavhengig reviewer og triage i samme økt. På forhånd bestemte jeg hvordan feilen i Vitest ved liten stasjonsbokstav fra Story 1.2 skulle håndteres: ingen fiks i et eget skript, bare en merknad i README.

**Hva som ble bygget:**
- `README.md` på norsk. Den har forutsetningene med versjoner (Python 3.12, uv 0.13.x, Node.js ≥ 22.12) og lenker for å installere dem, og installasjon med `uv sync --frozen`, `npm ci` og `npx playwright install chromium`. Den har også start av backend og frontend og alle tre testkommandoene. Den sier at v1 ikke trenger Docker, miljøvariabler, nøkler eller betalte tjenester, og at bare installasjonen trenger nett.
- En merknad om terminal på Windows: PowerShell anbefales, og rundgangene for cmd (`cd /d C:\…`) og Git Bash (`cd /C/…`) er med.
- `.env.example`, som sier at v1 ikke trenger miljøvariabler (NFR-9).
- `backend/tests/test_repo.py`. Den sjekker at kommandoene og versjonene står ordrett i README, at `.env.example` finnes, og at `git ls-files` ikke viser `.db`-, `.db-wal`-, `.sqlite`- eller `.env`-filer.

**Rettet før review (KI-ens egen kontroll):** I første utkast havnet teksten til `.env.example` i `README.md` ved en feil. KI-en oppdaget det selv og rettet det før testene ble kjørt.

**Gjennomgang:** Revieweren ga 12 funn.
- **Rettet (3):**
  - Testen for databasefiler fanger nå også `-journal`, `-wal`, `-shm` og `.sqlite`, slik `.gitignore` gjør.
  - Testen for `.env` godtar `.env.*.example`, som `.gitignore` tillater.
  - README har lenker for å installere uv og Node, siden sensor skal klare seg uten hjelp.
- **Avvist (8):** De var feil, rammet sjelden, eller lå utenfor storyen. Eksempler: at testen feiler uten git (testen hoppes over når `.git` mangler) og at `engines` mangler i `package.json`.
- **Utsatt (1):** kontrollen uten nett, som jeg måtte gjøre selv.

Hele triagen står i spesifikasjonen.

**Kontroll av oppstarten (F12, NFR-1):**
- **Med nett:** KI-en flyttet den gamle databasefila til side og startet etter README. `prognos.db` ble laget på nytt, og helsesjekken svarte OK både gjennom frontend og direkte mot backend.
- **Uten nett:** Jeg koblet fra nettverket etter installasjonen. Backend og frontend startet, helsesjekken svarte OK gjennom proxyen, siden viste «PROGNOS», og alle testene var grønne (32 i backend og 15 i frontend).

**Åpne punkter:** Ingen. Epic 1 har nå alle tre stories på `done`.

**Kilder:**
- Sesjonslogg: [.logs/mathias-ellingsen/987-2026-11-18-13-43-05-story-1-3-readme-repohygiene.md](../.logs/mathias-ellingsen/987-2026-11-18-13-43-05-story-1-3-readme-repohygiene.md)
- [Spesifikasjon for Story 1.3](../_bmad-output/implementation-artifacts/spec-1-3-readme-repohygiene-og-kontroll-av-oppstarten.md)

## 2026-11-18 — Retrospektiv for Epic 1

**Økt:** Kjørte `/bmad-retrospective` (Claude Code) på Epic 1. Jeg ba om en kort retro med vekt på hva gjennomgangene fanget som KI-en ellers ville gått videre med, og hvilke regler vi tar med videre. KI-en leste triage-loggene i speccene, sesjonsloggene og git-historikken, og kjørte alle testene på nytt.

**Hva gjennomgangene fanget:** De tre storyene fikk 52 reviewfunn til sammen, og 18 ble rettet. Tre typer feil gikk igjen:
- **Innstillinger ingen ba om:** KI-en la `cacheComponents` og `partialPrefetching` inn i `next.config.ts`, men malen har tom konfig. I tillegg skrev `next dev` `AGENTS.md` på nytt av seg selv.
- **En test som aldri kunne feile:** at utviklerdatabasen ikke ble rørt, ble sjekket med `git status`, men `*.db` er gitignored. Den ble erstattet av `e2e/database.spec.ts`. Flere andre tester var smalere enn kravet de skulle sjekke.
- **Liten stasjonsbokstav:** `npm test` feiler fra `c:\…`. README forklarer nå hvordan man kommer rundt det.

Retroen fant også at Verification-delen i speccen for Story 1.2 fortsatt anbefalte `git status`-sjekken. Det er rettet.

**Resultat:** Dommen er *accepted-with-open-items*. Alle akseptkriteriene er oppfylt, og testene er grønne: pytest 32/32, Vitest 15/15 og Playwright 4/4. Epic 1 står på `done`. Jeg bestemte at tre regler skal gjelde videre, og de står nå i `CLAUDE.md`:
- **R1:** ingen innstillinger uten bestilling.
- **R2:** en test teller først når den er sett feile.
- **R3:** kommandoer verifiseres i PowerShell.

Jeg la også inn at `bmad-build` alltid bruker subagenter til å kompilere konteksten og til uavhengig kodegjennomgang.

**Åpne punkter:** Kjøre backtest-spiken på nytt når generatoren i Epic 2 finnes.

**Kilder:**
- [Retro-dokument](../_bmad-output/implementation-artifacts/epic-1-retro-2026-11-18.md)
- Sesjonslogg: [.logs/mathias-ellingsen/986-2026-11-18-13-53-50-retro-epic-1.md](../.logs/mathias-ellingsen/986-2026-11-18-13-53-50-retro-epic-1.md)

## 2026-11-18 — Story 2.1: Generator for syntetisk salgshistorikk med fasit

**Økt:** Bygget Story 2.1 med `/bmad-build` (Claude Code). KI-en kompilerte konteksten for Epic 2 med en subagent og skrev speccen. Etter at jeg godkjente den, implementerte en subagent, og tre uavhengige reviewere gikk gjennom diffen.

**Hva KI-en gjorde:**
- Skrev `testdata/generator.py`. Den bruker bare standardbiblioteket og numpy, har `--seed` (standard 42) og `--mappe`, og skriver `testdata/syntetisk.csv` og `testdata/fasit.json`.
- Modellen er `(nivå + trend·t) · sesongfaktor + støy`. Svaret klemmes til ≥ 0 og rundes til heltall.
- Parameterne trekkes fra faste intervaller per kategori og settes aldri produkt for produkt (SM-C1).
- Laget 21 pytest-tester i `backend/tests/testdata/`. Hver av dem er sett feile med en endring i generatoren før den ble regnet som bevis (R2).

**Valg jeg tok:**
- Produktene heter `P-101` til `P-124`, samme format som i PRD-en og mockupene.
  - P-101–P-115 har trend.
  - P-116–P-117 er flate med mye støy.
  - P-118–P-120 har sesong uten trend.
  - P-121–P-124 har 8, 15, 20 og 26 måneders historikk.
- Beholdt speccen samlet, selv om den var litt over den anbefalte lengden.
- Sjekket testene og generatoren selv før storyen ble satt til `done`.

**Hva gjennomgangen fanget:** 15 funn, og 5 ble rettet.
- **Det viktigste funnet:** ingen test sjekket at tallene i CSV-en faktisk følger trend, sesong og støy i fasiten. Hadde sesongen havnet i feil måned, ville alle testene likevel vært grønne. Nå regner en egen test modellen tilbake fra fasiten.
- **Sammensetningen ble ikke sjekket:** antallet sesongprodukter, flate produkter uten sesong og korte produkter med trend.
- **Avvist (10):** usannsynlige feilsituasjoner, som negativ seed, `python -OO` og dynamiske importer.

Hele triagen står i spesifikasjonen.

**Resultat:** 53 tester grønne i PowerShell. En ny kjøring av generatoren gir byte-identiske filer. Den globale regelen `* text=auto eol=lf` i `.gitattributes` er kontrollert: Git lagrer og sjekker ut testdatafilene uendret, også med `core.autocrlf=true`. De egne `-text`-reglene kommer i Story 2.2.

**Åpne punkter:** Kjøre backtest-spiken på nytt mot det syntetiske datasettet (fra retroen for Epic 1).

**Kilder:**
- Sesjonslogg: [.logs/mathias-ellingsen/984-2026-11-18-14-19-29-story-2-1-generator-syntetisk.md](../.logs/mathias-ellingsen/984-2026-11-18-14-19-29-story-2-1-generator-syntetisk.md)
- [Spesifikasjon for Story 2.1](../_bmad-output/implementation-artifacts/spec-2-1-generator-for-syntetisk-salgshistorikk-med-fasit.md)
