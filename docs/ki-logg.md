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
- Skrev 30 stories: Epic 1 (3), Epic 2 (2), Epic 3 (7), Epic 4 (3), Epic 5 (5) og Epic 6 (8).
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
