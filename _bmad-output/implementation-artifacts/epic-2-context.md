# Epic 2 Context: Syntetisk datasett med seed 42

<!-- Compiled from planning artifacts. Edit freely. Regenerate with compile-epic-context if planning docs change. -->

## Goal

Gruppen og sensor skal kunne generere en kjent salgshistorikk med fasit (trend, sesongprofil og støynivå per produkt). Den skal dekke alle historikknivåene og backtest-grensene og være byte-identisk ved hver kjøring med samme seed. Filene sjekkes inn og er grunnlaget for senere epics: seeding ved tom database (Epic 3), 5 %-testen mot fasiten med ETS (Epic 4), F7/F8 og svartidsmålingen (Epic 5) og demoen sensor ser ved første oppstart. Datasettet skal gi ETS noe reelt å slå baseline på, uten at det er tilpasset for å gjøre testene grønne.

## Stories

- Story 2.1: Generator for syntetisk salgshistorikk med fasit
- Story 2.2: Støyfritt kontrollprodukt og stort datasett for svartid

## Requirements & Constraints

- **Determinisme (F9):** to kjøringer med samme seed gir byte-identisk `syntetisk.csv`, `fasit.json` og `uten_stoy.csv`. En annen seed gir en annen `syntetisk.csv`. Standardseed er 42.
- **Seed 42 er låst.** Den ble valgt før datasettet ble generert og endres aldri etter at resultatene er sett. Spiken viste at F8 kan feile med enkelte seeds, så seeden må ikke brukes som justeringsknapp.
- **SM-C1:** trend og støy justeres ikke produkt for produkt for å få bedre WAPE, og de flate seriene med mye støy beholdes. Dette skal stå som kommentar øverst i generatoren. Hvis F7 eller F8 senere feiler på datasettet, føres det som funn i `issues.md` og testen merkes `xfail(strict=True)`. Data, seed og intervallnivå endres ikke.
- **Innhold i `syntetisk.csv`:** 20 produkter med 36 måneder. Minst 15 av dem har trend i tillegg til sesong og støy, og minst 2 er flate serier med mye støy. I tillegg 4 produkter med 8, 15, 20 og 26 måneder, slik at historikknivåene *ingen*/*sesongnaiv*/*ets* og backtest-nivåene *ingen*/*sesongnaiv*/*begge* dekkes. Alle produktene slutter i samme siste måned, som er en konstant i generatoren.
- **Gyldig etter importreglene:** overskriften `produkt_id,maaned,antall`, `antall` heltall ≥ 0, `maaned` som `ÅÅÅÅ-MM`, ingen duplikater og ingen hull. Fila skal godkjennes uten advarsler om utfylling.
- **Fasit:** én oppføring per produkt med trend, sesongprofil (12 faktorer) og støynivå.
- **Støyfritt kontrollprodukt (`uten_stoy.csv`):** ett produkt med 36 måneder, kjent trend og sesong, ingen støy og nivå ≥ 20 i hver måned. Nivået gjør at heltallsavrundingen alene ikke kan gi mer enn 2,5 % avvik i 5 %-testen. Fasiten skal også inneholde de forventede verdiene for de 6 månedene etter siste måned. Verdiene i fila skal stemme nøyaktig med fasiten etter avrunding til heltall.
- **Stort datasett (NFR-7):** generatoren tar valg for antall produkter, måneder og utfil (for eksempel `--produkter 200 --maaneder 36 --ut STI`) og skriver en gyldig CSV i samme format. Denne fila genereres i testen og sjekkes ikke inn.
- **NFR-9:** generatoren og filene ligger i egen mappe `testdata/` i rotmappa.
- **Testregler (retro Epic 1):** en akseptkriterietest teller først når den er sett feile (brekk betingelsen eller bytt inn feil data). Fasittester sammenligner med uavhengige konstanter, ikke med kodens egen output. Kommandoer i spec eller README verifiseres i PowerShell.
- De genererte filene endres aldri for hånd. De lages på nytt ved å kjøre generatoren.

## Technical Decisions

- **Plassering og kjøring:** `testdata/generator.py` kjøres med `uv run --project backend python testdata/generator.py`. Den bruker bare standardbiblioteket og numpy (`numpy.random.default_rng(seed)`, numpy 2.5.x er allerede en backend-avhengighet). Den importerer ingenting fra `backend/`/`prognos`. Arkitekturen sier at generatoren skriver filer og ikke importerer backend. Testen sjekker importene statisk.
- **Format for `syntetisk.csv` og `uten_stoy.csv`:** komma som skilletegn, UTF-8 uten BOM, `\n` som linjeskift, sortert på `produkt_id` og så `maaned`.
- **Format for `fasit.json`:** `json.dump` med `sort_keys=True`, `indent=2` og `ensure_ascii=False`, og avsluttende `\n`.
- **Git og bytes:** `.gitattributes` har i dag den globale regelen `* text=auto eol=lf`, men ikke testdatareglene. Story 2.2 legger til `testdata/*.csv -text` og `testdata/*.json -text`, slik at Git ikke endrer bytes på Windows. `syntetisk.csv`, `fasit.json` og `uten_stoy.csv` sjekkes inn.
- **Konvensjoner:** norsk snake_case. Æ/ø/å skrives `ae`/`oe`/`aa` i identifikatorer og filnavn (`uten_stoy`, `maaned`). Ingen miljøvariabler. Valg tas som CLI-argumenter.
- **Tester:** pytest i `backend/tests/testdata/`. Byte-identitet testes ved å generere to ganger i hver sin midlertidige mappe og ved å sammenligne de innsjekkede filene med en ny generering, så de ikke kan bli utdaterte. Testene sjekker også formatet, antall produkter per historikklengde, felles siste måned, trend/flat-fordelingen ifølge fasiten, feltene i fasiten og formateringen.
- Historikknivåer og backtest-grenser (12/18/24/30) eies av `domene/nivaa.py` i Epic 3–5. Generatoren trenger bare å produsere lengdene 8, 15, 20, 26 og 36.

## Cross-Story Dependencies

- **2.1 → 2.2:** 2.2 utvider samme generator, `fasit.json` og testoppsettet. Det skal ikke lages en egen generator.
- **Byte-identitetstest i 2.1 og `.gitattributes` i 2.2:** testen i 2.1 som sammenligner innsjekkede filer med ny generering, er avhengig av at Git ikke konverterer bytes. Reglene som sikrer det, kommer først i 2.2.
- **Epic 3 (Story 3.7):** `seed_if_empty` leser `testdata/syntetisk.csv` og laster den inn via `last_inn_datasett` med filnavnet `syntetisk.csv`. Story 3.3 tester `per_nivaa` mot denne fila. Feilet seeding stopper backend, så fila må alltid bestå valideringen.
- **Epic 4 (Story 4.2):** 5 %-testen leser `uten_stoy.csv` og `fasit.json` og sammenligner avrundet ETS-P50 med de forventede horisontverdiene. Story 4.1 og 4.3 bruker `syntetisk.csv`.
- **Epic 5:** Story 5.4 tester F7 (ETS slår baseline) og F8 (ETS-dekning 65–95 %) på `syntetisk.csv`. Story 5.5 bruker valget for stort datasett (200 × 36) til tidtakingen.
