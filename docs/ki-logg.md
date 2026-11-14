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
