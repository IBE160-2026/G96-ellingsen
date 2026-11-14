# Avstemming: PRD mot brief og faglærers tilbakemelding

**PRD:** `prd.md` og `addendum.md` (2026-11-14)
**Kilder:** A = `PRODUCT_BRIEF.md` (avsnitt 4.1, 5 og 6), B = `tilbakemelding-product-brief.md` (faglærer, 2026-10-06)
**Dato:** 2026-11-14

Disse rammene er besluttet og blir ikke flagget: bare v1 er med, F1–F14 står ordrett med samme ID-er, Kari er eneste primærbruker, total WAPE regnes over produkter med backtest for begge modellene, og flaggede produkter står øverst.

## Sammendrag

| # | Funn | Kilde | Alvorlighet | Sted i PRD |
|---|---|---|---|---|
| 1 | Baseline-backtest kan ikke gjennomføres for produkter med 12–17 mnd historikk | A | Høy | §4.4-tabellen, FR-16 |
| 2 | Ingen krav om fasitserier eller test av at modellen fanger opp trend og sesong | A, B | Høy | §4.6, FR-23/FR-24, NFR-6 |
| 3 | Ingen krav om ryddig repo: mappe for syntetiske testdata, `.env.example`/`.gitignore`, plassering av databasefila | B | Høy | §5 (mangler NFR) |
| 4 | Intervalldekning er udefinert for modell og aggregering | A | Middels | FR-15, FR-21 |
| 5 | Det er uklart om horisonten gjelder per produkt eller per datasett når produktserier slutter på ulike måneder | A | Middels | §3 Horisont, FR-4, FR-8 |
| 6 | WAPE er udefinert når Σ faktisk = 0 | A | Middels | §3 WAPE, FR-14, FR-19 |
| 7 | NFR-5 (etterprøvbarhet) kan ikke oppfylles med tallene som dashbordet viser | A | Middels | NFR-5, FR-21 |
| 8 | NFR-6 krever bare test av F1–F14, så FR-16, FR-17, FR-19 og FR-25 kan stå uten test | B | Middels | NFR-6 |
| 9 | §9 knytter «baseline først» og «kjente data» til feil krav og mangler flere rader | A | Middels | §9 |
| 10 | Tilbakemeldingen fra faglærer er ikke sporet noe sted | B | Middels | §9 |
| 11 | Tallene i UJ-3 henger ikke sammen («17 av 18» i et datasett med 200 produkter) | A | Middels | UJ-3 |
| 12 | Kravene til README er bare «kommandoene»: forutsetninger og testkommando mangler | B | Middels | NFR-1 |
| 13–20 | Mindre presiseringer (se under) | A, B | Lav | Diverse |

**F1–F14:** Teksten er sammenlignet maskinelt mot briefen avsnitt 6, og alle 14 kriteriene er ordrett like, med de samme ID-ene. Ingen funn.

---

## Kilde A: PRODUCT_BRIEF.md

### A1. Baseline-backtest er umulig for 12–17 mnd historikk (høy)

**Sted:** tabellen i §4.4 («12–29 mnd: Bare sesongnaiv baseline»), FR-16 og FR-5.
**Problem:** Sesongnaiv baseline trenger minst 12 måneders historikk før hver opprinnelse. Med 6 opprinnelser over de siste 6 månedene må et produkt ha minst 18 måneder for å få en full baseline-backtest. Den samme logikken gir 24 + 6 = 30 måneder for ETS, og den grensen er riktig. Briefen sier bare at produkter med «under 30 måneders historikk får bare baseline-backtest», og PRD-en har gjort det om til et absolutt intervall, 12–29. Et produkt med 12–17 måneder kan ikke få 6 baseline-backtest-prognoser. Det syntetiske produktet med «12–23 mnd» (FR-24) kan derfor gi en test som feiler eller er udefinert.
**Forslag:** Del raden: «12–17 mnd: ingen backtest (eller færre opprinnelser)» og «18–29 mnd: bare sesongnaiv baseline». Legg tolkningen inn i §11. Fastsett også lengden på det syntetiske 12–23-produktet i FR-24, for eksempel 18 mnd, eller legg til ett produkt på 12–17 mnd og ett på 18–23 mnd.

### A2. «Kjente data» og fasit har ikke blitt et krav (høy)

**Sted:** beskrivelsen i §4.6, FR-23 og FR-24.
**Problem:** Briefen (4.1 og prinsippet «Kjente data» i 5) sier at sesong og trend er kjent, «så vi kan sjekke at modellen fanger dem opp». PRD-en nevner dette bare i beskrivelsen av §4.6. Ingen FR-konsekvens krever at generatoren lagrer fasiten (trend, sesongprofil og støynivå per produkt), og ingen test sjekker modellen mot fasiten. Faglærer ba uttrykkelig om fasitserier (se B1).
**Forslag:** Legg til en konsekvens i FR-24: «Generatoren skriver fasitparametre per produkt (trend, sesongprofil, støy) ved siden av CSV-fila.» Legg til et nytt testbart krav: «For en serie uten støy med kjent trend og sesong ligger ETS P50 innenfor X % av fasiten.»

### A3. Intervalldekning: hvilken modell, og per produkt eller totalt? (middels)

**Sted:** FR-15, FR-21 (backtest-tabellen) og §3 Intervalldekning.
**Problem:** Briefen sier bare «andel faktiske verdier innenfor P10–P90». PRD-en sier ikke om dekningen gjelder intervallene fra ETS, fra sesongnaiv baseline eller begge. Den sier heller ikke om F8 skal regnes totalt (over hvilke produkter?) eller per produkt. For produkter med bare baseline-backtest viser FR-21 intervalldekning uten å si hvilken modell tallet gjelder.
**Forslag:** Presiser FR-15: «Dekning beregnes per produkt for modellen som gir den viste prognosen (ETS når ETS-backtest finnes, ellers baseline). F8 gjelder total dekning for ETS over de samme produktene som total WAPE (FR-14).» Legg tolkningen inn i §11.

### A4. Horisont og utfylling når produktene slutter på ulike måneder (middels)

**Sted:** §3 (Horisont, Utfylt måned, Historikklengde), FR-4 og FR-8.
**Problem:** Briefen sier «manglende måneder fylles med 0». PRD-en fyller bare mellom produktets første og siste måned, og horisonten starter «måneden etter siste måned i salgshistorikken». Hvis ett produkt slutter i 2026-08 og resten i 2026-10, er det uklart om horisonten skal gjelde produktets siste måned eller datasettets siste måned, og om månedene 09–10 skal fylles med 0. Tolkningen «mellom første og siste måned» står heller ikke i §11.
**Forslag:** Bestem at datasettets siste måned er felles slutt, og fyll hvert produkt fram til den (eller velg en annen regel). Skriv regelen i FR-4 og FR-8, og legg den inn i §11.

### A5. WAPE når Σ faktisk = 0 (middels)

**Sted:** §3 WAPE, FR-14, FR-17 og FR-19.
**Problem:** Hvis et produkt har bare nuller i backtest-vinduet, for eksempel en serie med mange utfylte måneder, deler WAPE på null. Da blir sorteringen i FR-19 og flagget *ETS taper* i FR-17 udefinert.
**Forslag:** Legg til en konsekvens: «Når Σ faktisk = 0, vises WAPE som ‹ikke definert›. Produktet får ikke flagget *ETS taper* og sorteres sist blant de uflaggede.»

### A6. NFR-5 kan ikke regnes etter fra tallene som vises (middels)

**Sted:** NFR-5 og FR-21.
**Problem:** Prinsippet «Etterprøvbart» er gjort om til «kan regnes etter for hånd fra tallene som vises». Backtest-tabellen viser bare WAPE i prosent og dekning, ikke faktisk og prognose per opprinnelse. Brukeren kan derfor ikke regne etter WAPE fra dashbordet. Testbetingelsen i NFR-5 er dessuten en enhetstest, ikke en sjekk av det som vises.
**Forslag:** Gjør ett av to: (a) Legg til i FR-21 at backtest-tabellen kan utvides til å vise faktisk, prognose og avvik for hver av de 6 opprinnelsene, eller (b) skriv om NFR-5 til «Scenariototaler kan regnes etter fra de viste månedsverdiene, og WAPE kan regnes etter fra backtest-dataene i API-et.»

### A7. Tallene i UJ-3 henger ikke sammen (middels)

**Sted:** UJ-1 og UJ-3.
**Problem:** UJ-1 har 200 produkter, der 3 er flagget for kort historikk. UJ-3 sier at ETS slår baseline «for 17 av de 18 produktene som har backtest for begge modellene». Da har bare 18 av de 197 andre produktene minst 30 mnd historikk, noe som er lite troverdig for Karis datasett. Tallene ser ut til å være hentet fra skissen i briefen («17/20»), som bygger på det syntetiske datasettet med 20 produkter.
**Forslag:** Bruk realistiske tall for Karis datasett (for eksempel «162 av 190»), eller la UJ-3 bruke det syntetiske datasettet.

### A8. FR-11 snevrer inn F6 uten at det står i §11 (lav)

**Sted:** FR-11 og §11.
**Problem:** F6 sier «Hvert produkt får tre scenarioer». FR-11 sier «for hvert produkt med prognose». Det er en rimelig lesning sammen med F5, på samme måte som F3/F5 er lest sammen i §11, men den er ikke ført opp som tolkning. Det står heller ikke eksplisitt at produkter med historikknivå *baseline* får scenarioer fra intervallene til sesongnaiv baseline.
**Forslag:** Legg til i §11: «F6 og F5 leses sammen: produkter med historikknivå *ingen* har ingen scenarioer. Produkter med historikknivå *baseline* får scenarioer fra intervallene til sesongnaiv baseline.» Speil dette i FR-11.

### A9. Ugyldig dato er bare en formatsjekk (lav)

**Sted:** FR-3.
**Problem:** Briefen sier «ugyldige datoer». FR-3 sjekker bare formatet ÅÅÅÅ-MM, så `2025-13` består formatsjekken.
**Forslag:** «`maaned` må være på formatet ÅÅÅÅ-MM med måned 01–12.» Legg i tillegg til tom fil og fil med bare overskrift som feil.

### A10. «Identisk» i FR-2 må unnta metadata (lav)

**Sted:** FR-2.
**Problem:** To opplastinger gir to datasett med ulikt filnavn og tidspunkt. «Identisk datasett» er derfor strengt tatt ikke testbart.
**Forslag:** «… gir identisk salgshistorikk, prognose og backtest (filnavn og tidspunkt unntatt).»

### A11. Sortering innenfor flaggede produkter er udefinert (lav)

**Sted:** FR-19.
**Problem:** Det står ikke hvordan produkter med *ETS taper* og *kort historikk* sorteres seg imellom, eller innenfor hver gruppe. Skissen i briefen viser *ETS taper* først.
**Forslag:** «Blant flaggede: *ETS taper* først (høyest WAPE først), deretter *kort historikk* (sortert etter `produkt_id`).»

### A12. Kvalitative idéer som er svekket (lav)

- **«Baseline først»** (5) er dekket av FR-14, FR-17, FR-21 og FR-22, men står ikke som eget prinsipp. Skriv det i innledningen til §4.4 som en føring: «ETS vises aldri uten baseline ved siden av.»
- **Læringsmålet «KI *i* produktet (prognosemodell)»** (3) er borte. §8.3 nevner bare KI i utviklingen. Ta med én linje.
- **Ikke-mål «beslutningsmaskin»** (§6): briefen sier «Systemet *anbefaler*». PRD-en har endret til «viser prognoser». Det passer for v1, men endringen bør nevnes.
- **Skissen** brukes som referanse (§4.5) og er ikke kopiert inn. Det er greit, men FR-20 bør nevne markøren «i dag» mellom historikk og prognose, og FR-18 bør vise valideringslinjen i formen «✓ N produkter godkjent · M flagget».

### A13. Trinn 2-kriteriene B1–B3 og L1 er ikke nevnt (lav)

**Sted:** §7.2 og §8.3.
**Problem:** Prosjektsuksess i briefen avsnitt 6 har med «Trinn 2 … (B1–B3) levert hvis tiden tillater». PRD-en har tatt det bort helt. I tråd med rammen bør det nevnes som utenfor v1.
**Forslag:** Legg til i §7.2: «Kriteriene B1–B3 og L1 (briefens avsnitt 6) hører til trinn 2. Utenfor v1.»

---

## Kilde B: Faglærers tilbakemelding

### B1. Testbarhet og fasitserier (høy)

**Sted:** §4.6, NFR-5 og NFR-6.
**Problem:** Faglærer sier: «Lag fasitserier og funksjonelle kriterier i tillegg.» De funksjonelle kriteriene finnes (F1–F14), men fasitserier mangler (se A2). NFR-5 nevner et «lite datasett» med håndregnede verdier, men ikke hvor det ligger eller hva det inneholder.
**Forslag:** Legg til et krav om et lite håndregnet testdatasett (for eksempel 2 produkter × 36 mnd) med regnearkfasit for scenariototaler, WAPE og dekning. Lag det sammen med fasitparametrene fra A2.

### B2. Repoet er ikke ryddig nok: testdata, hemmeligheter og dokumentasjon (høy)

**Sted:** §5. Ingen NFR dekker dette.
**Problem:** Kriterium 7 i tilbakemeldingen: «Planlegg `.env.example` for API-nøkkelen og en egen mappe for syntetiske testdata.» PRD-en sier ingenting om
- hvilken mappe generatoren og det syntetiske datasettet skal ligge i,
- `.env.example`. v1 har ingen nøkkel, men det bør stå eksplisitt, og trinn 2 trenger fila,
- hvor SQLite-fila ligger, og at den er ignorert i git. Dagens `.gitignore` har ingen regel for `*.db`/`*.sqlite`,
- hvor dokumentasjonen ligger. Det finnes i dag både `.docs/planning-artifacts/` og `_bmad-output/planning-artifacts/`, så planleggingsartefaktene er spredt.
**Forslag:** Legg til **NFR-9 Ryddig repo:** «Syntetiske data og generatoren ligger i en egen mappe (for eksempel `data/synthetic/`). Testfixtures ligger i `backend/tests/fixtures/`. Databasefila ligger i en fast mappe som er ignorert i git. Repoet har ingen hemmeligheter. v1 trenger ingen `.env`, og `.env.example` følger med trinn 2 (eller lages tom nå med en kommentar). Planleggingsdokumentene samles på ett sted.» Testbar betingelse: `git ls-files` inneholder ingen `.db`- eller `.env`-filer.

### B3. Kjørbar for sensor: README-kravet er tynt (middels)

**Sted:** NFR-1 og F12.
**Problem:** NFR-1 sikrer null konfigurasjon, men sier ikke hva README skal inneholde. Sensor trenger forutsetningene (versjoner av Python, Node og `uv`), installasjon, start, testkjøring (pytest, Vitest, Playwright inkludert nettleserinstallasjon) og hvor demodataene kommer fra.
**Forslag:** Legg til en konsekvens i NFR-1: «README lister forutsetninger med versjoner, kommandoer for installasjon, start og alle testene, og forteller at det syntetiske datasettet lastes automatisk (FR-25).»

### B4. Testdekningen er knyttet bare til F1–F14 (middels)

**Sted:** NFR-6.
**Problem:** Mange «testbare konsekvenser» har ikke noe F-kriterium. Det gjelder FR-16 (backtest etter lengde), FR-17 (*ETS taper*), FR-19 (sortering), FR-25 (seeding) og FR-6 (ny opplasting gir nytt datasett). NFR-6 krever ikke test av dem. SM-C1 forutsetter at *ETS taper* blir testet, men om det syntetiske datasettet faktisk gir et produkt der ETS taper, er tilfeldig.
**Forslag:** Utvid NFR-6: «Alle konsekvenser merket ‹testbare› dekkes av automatiske tester.» Legg til i FR-17: «Testen bruker en konstruert serie der ETS garantert taper, uavhengig av det syntetiske datasettet.»

### B5. Tilbakemeldingen fra faglærer er ikke sporet (middels)

**Sted:** §0 og §9.
**Problem:** Tilbakemeldingen er en kilde (§0), men §9 sporer bare briefens avsnitt. Faglærer legger vekt på at sensor skal kunne følge «en sporbar vei fra plan til ferdig app», og at historikken viser hvordan planen har utviklet seg.
**Forslag:** Legg til en tabell §9.2 «Tilbakemelding → PRD». Eksempler på rader: SQLite i stedet for PostgreSQL → NFR-1/addendum; mock/ingen nøkkel → NFR-1, §7.2; én primærbruker → §2; testbare kriterier → §8.1; «modellen slår baseline» som viktigste kriterium → SM-1; fasitserier → (A2/B1, nytt krav); `.env.example` og mappe for testdata → (B2, ny NFR-9); skisse av prognosevisningen → §4.5.

### B6. Punkter fra tilbakemeldingen som er dekket (ingen funn)

Disse punktene er dekket: én kjerneflyt (§4, UJ-1), én primærbruker (§2), funksjonelle testkriterier (§8.1), «modellen slår baseline» som viktigste kvalitetskriterium (SM-1), SQLite uten Docker (NFR-1, NFR-2, addendum), ingen nøkkel eller betalt API i v1 (NFR-1, addendum), det ærlige «hva skiller PROGNOS» (§1, §6), forretningsmålene flyttet til visjonen (§8.3), og kontroll for hånd med enkle modeller (FR-10, NFR-5).

### B7. NFR-4 er vanskelig å teste (lav)

**Sted:** NFR-4.
**Problem:** «Ingen engelske brukertekster» kan ikke testes automatisk uten en konkret metode.
**Forslag:** «Alle brukertekster ligger i én tekstfil eller modul på norsk. Playwright-testen (F10) sjekker de viktigste overskriftene og scenarioordene.»

---

## Sporbarhetstabellen i §9

| Rad i §9 | Funn | Alvorlighet | Forslag |
|---|---|---|---|
| §5 Teknisk tilnærming og prinsipper | «Baseline først» er knyttet til NFR-1–NFR-5, men ingen av dem dekker prinsippet. Det dekkes av FR-14, FR-17, FR-21 og FR-22. «Kjente data» (→ FR-23, FR-24) og «KI i utviklingen» (→ §8.3) er ikke nevnt. | Middels | Del raden i én rad per prinsipp med riktige krav. |
| §2 Arbeidsflyt steg 1–2 | F-kolonnen mangler F5 (FR-5) og F11 (FR-6). | Lav | Legg til F5 og F11. |
| §2 Arbeidsflyt steg 3 | Scenarioer (FR-11, FR-12 → F6) og flagg (FR-5, FR-17) mangler. | Lav | Legg til FR-5, FR-11, FR-12, FR-17 og F6. |
| §2 Arbeidsflyt steg 4 | FR-13–FR-16 og F8 mangler. | Lav | Legg til. |
| §3 Produktmål 1 | F11 (FR-6) mangler. | Lav | Legg til F11. |
| §3 Læringsmål og forretningsmål | Rader mangler. | Lav | Legg til → §8.3. |
| §4 Omfangstabell | Rad mangler. | Lav | Legg til → §7. |
| §4.1 del 3 | F10 mangler, selv om FR-21 er med. | Lav | Legg til F10. |
| §6 Suksesskriterier | B1–B3, L1 og «trinn 2 hvis tiden tillater» er ikke nevnt. | Lav | Legg til → §7.2 (utenfor v1). |
| §8.1 F8 → krav | FR-13 (rullerende backtest) mangler. | Lav | F8 → FR-13, FR-15, FR-24. |
| Kravene uten opphav | NFR-6 (fra briefens avsnitt 6, prosjektsuksess), NFR-7 (tolkning i §11) og NFR-8 (fra avsnitt 5) er ikke ført opp i §9. | Lav | Legg dem inn i de relevante radene. |
| Tilbakemeldingen | Ikke sporet. | Middels | Se B5. |

Ellers er §9 riktig: hver rad viser til et avsnitt som finnes i briefen, og alle FR-ene (FR-1–FR-25) kan spores til minst ett avsnitt.

## Tillegg utover v1 eller i strid med briefen

Ingen funn er kritiske. Alle tilleggene er innenfor v1 og står i §11. Kommentarer:
- NFR-7 (60 s) og datasettvelgerens standardvalg (FR-18) er nye, men står i §11 som bekreftede tolkninger. OK.
- Addendum: teknologien for frontend (Next.js 16, shadcn/ui, TanStack Query, `zod`) står ikke i briefen, men er tekniske føringer fra arkitekturutkastet. OK. Avsnittet «Forberedt for trinn 2» nevner feature flags og tabellen `inventory` og sier at de ikke bygges. OK.
- UJ-1 «Klimaks» (sikkerhetsmargin med materialplanleggeren) ligger nær beregningen av sikkerhetslager i trinn 2, men er formulert som skjønn hos brukeren og ikke som en funksjon. Lav. Det bør stå tydelig at PROGNOS v1 ikke regner sikkerhetslager.
