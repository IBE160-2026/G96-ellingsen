# Research-plan PROGNOS

## Uavklarte beslutninger
- ~~SQLite eller PostgreSQL? (faglærer anbefalte SQLite)~~ **Besluttet:** SQLite. Se beslutningsloggen: *Database*.
- ~~Hva skjer med produkter med under 12 måneders historikk? Sesongnaiv trenger minst 12 måneder.~~ **Besluttet:** ingen prognose, og produktet flagges. Se beslutningsloggen: *Kort historikk*.
- ~~Kjøres prognosen automatisk etter opplasting, eller med en knapp?~~ **Besluttet:** automatisk etter godkjent opplasting. Se beslutningsloggen: *Prognosen kjøres automatisk*.
- ~~Negative prognoser: settes P10 til 0? (påvirker F2)~~ **Besluttet:** P10, P50 og P90 settes til minst 0. Se beslutningsloggen: *P10, P50 og P90 settes til minst 0*.
- ~~Scenarioer for 6 måneder totalt: summen av månedlig P10 er ikke P10 for totalen. Hvordan håndterer vi det?~~ **Besluttet:** summen av de månedlige verdiene, med en merknad om at spennet blir bredere enn det reelle. Se beslutningsloggen: *Scenarioer for 6 mnd*.
- ~~Backtest: prognoserer hver opprinnelse 1 eller 6 måneder frem?~~ **Besluttet:** 1 måned frem, 6 opprinnelser. Se beslutningsloggen: *Backtest*.

## Teknisk research
- Les FPP (Hyndman): ETS, prognoseintervaller, tidsserie-kryssvalidering
- Les statsforecast-dokumentasjon: AutoETS, SeasonalNaive, cross_validation
- WAPE: definisjon og hvorfor den brukes i stedet for MAPE
- ~~Testskript (spike): slår ETS baseline? Blir P10 negativ? Hvor god er P10–P90-dekningen?~~ **Besvart 2026-11-14:** ETS slår baseline i 18 av 20 seeds, P10 ble ikke negativ med seed 42, og P10–P90-dekningen for ETS var i snitt 76,7 % (innenfor 65–95 % i 18 av 20). Se [teknisk.md](teknisk.md).
- Syntetiske data: hvordan lage serier slik at F7 og F8 holder?

## Brukerbehov
- Hvordan ser en CSV-eksport fra ERP ut? (semikolon, desimalkomma, datoformat, manglende måneder)
- Hva gjør en etterspørselsplanlegger? (stillingsannonser)
- Hva trenger Kari å se først i dashbordet?
- Hvordan forstår en planlegger P10/P90? Bedre ord i grensesnittet?
- Mulig samtale med en planlegger

## Lignende løsninger
- Dynamics 365 demand forecasting, SAP IBP, Netstock, Slimstock, GMDH Streamline, Forecast Pro
- Hvordan viser de usikkerhet og treffsikkerhet?
- Hva tar vi bevisst ikke med?
- Utkast til avsnittet «Hva skiller PROGNOS»

## Spørsmål til læreren
- (fylles ut underveis)

## Beslutningslogg
| Beslutning | Begrunnelse | Dato |
|---|---|---|
| Database: SQLite i stedet for PostgreSQL | Faglærer anbefalte det. Enbrukerapp som kjører lokalt, og sensor trenger ingen databaseserver. Avvik fra technology.md begrunnes med tilbakemeldingen. | 2026-11-14 |
| Språk: PRD, dokumentasjon og grensesnitt skrives på norsk | Brukeren og målgruppen er norsk. | 2026-11-14 |
| Kort historikk: under 12 mnd gir ingen prognose og flagges; 12–23 mnd gir bare sesongnaiv; 24+ mnd gir ETS og baseline | Sesongnaiv trenger minst ett år, ETS med sesong trenger to. | 2026-11-14 |
| Prognosen kjøres automatisk etter godkjent opplasting | Færre klikk for brukeren, én sammenhengende flyt. | 2026-11-14 |
| P10, P50 og P90 settes til minst 0 | Salg kan ikke være negativt. Sikrer F2. | 2026-11-14 |
| Scenarioer for 6 mnd = summen av månedlige P10/P50/P90, med merknad om at spennet er bredere enn det reelle | Enkelt og etterprøvbart. Simulering er for komplisert for v1. | 2026-11-14 |
| Backtest: rullerende, 6 opprinnelser, horisont 1 måned, step 1. Produkter med under 30 mnd får bare baseline-backtest | Følger briefen. ETS trenger 24 mnd trening. Bekreftes i testskriptet. | 2026-11-14 |
| Intervaller: 80 % prediksjonsintervall (level=[80]) | Gir P10 og P90 direkte fra statsforecast. | 2026-11-14 |
| Når ETS taper mot baseline vises ETS, men produktet flagges med begge WAPE-tall | Følger prinsippet «baseline først» uten å skjule noe. | 2026-11-14 |
| CSV: komma eller semikolon (autodeteksjon), dato ÅÅÅÅ-MM, antall heltall ≥ 0, duplikater gir feil, manglende måneder fylles med 0 og gir advarsel | Norsk Excel bruker ofte semikolon. Holder valideringen enkel og testbar. | 2026-11-14 |
| Pessimistisk/Forventet/Optimistisk brukes som hovedord i grensesnittet, med P10/P50/P90 som forklaring | Planleggere forstår scenarioer bedre enn kvantiler. | 2026-11-14 |
| Dashbordet starter med produktliste sortert etter WAPE, med flagg for kort historikk og der ETS taper | Brukeren ser først hvor prognosen er svakest. | 2026-11-14 |
| Syntetiske data: de fleste produkter har trend i tillegg til sesong og støy | Med trend slår ETS sesongnaiv, så F7 blir realistisk. | 2026-11-14 |
| Sortering av produktlisten: flaggede produkter (kort historikk, ETS taper) øverst, resten sortert etter WAPE med høyest først | Følger skissen i briefen. Brukeren ser først produktene der prognosen er svak eller mangler. | 2026-11-14 |
| Total WAPE: ETS og sesongnaiv baseline summeres over de samme produktene, altså bare produkter med backtest for begge modellene (30+ mnd). Produkter med bare baseline-backtest får WAPE per produkt, men inngår ikke i totalen | Gir en rettferdig sammenligning i F7 og WAPE-oversikten. | 2026-11-14 |
| Backtest for 12–17 mnd: ingen backtest. 18–29 mnd gir bare baseline-backtest, 30+ mnd gir ETS og baseline | Sesongnaiv trenger 12 mnd før hver av de 6 opprinnelsene, altså minst 18 mnd. Samme regnestykke som ga 30-månedersgrensen for ETS. | 2026-11-14 |
| WAPE når faktisk salg er 0: vises som «–», inngår ikke i total WAPE, gir aldri *ETS taper*, og produktet står rett etter de flaggede i produktlisten | WAPE deler på summen av faktisk salg, som da er 0. Produktet skal likevel være synlig. | 2026-11-14 |
| Seed for syntetisk datasett: 42. Valgt før datasettet er generert, og endres ikke etter at resultatene er sett | Hindrer at seeden velges for å få F7 eller F8 grønn (SM-C1). Spiken viste at F8 kan feile med enkelte seeds, se [teknisk.md](teknisk.md). | 2026-11-14 |
| Intervalldekning og sortering: dekningen regnes per modell, per produkt og totalt over de samme produktene som total WAPE, og F8 gjelder ETS. Flaggede produkter sorteres internt etter WAPE med høyest først, og like verdier etter produkt_id | Samme logikk som for WAPE. Gir en rekkefølge som alltid er den samme, slik at testene blir stabile. | 2026-11-14 |
| Søk i produktlisten: et søkefelt filtrerer på produkt_id (inneholder, uavhengig av store og små bokstaver), og sorteringen i produktlisten beholdes i treffene (FR-26) | Kom fra UX-økten. Med rundt 200 produkter trenger Kari en rask måte å finne et bestemt produkt på, uten å miste rekkefølgen med de svakeste øverst. | 2026-11-14 |
| Første produkt i produktlisten velges automatisk etter innlasting, og Kari kan velge et annet (UJ-1 steg 4) | Kom fra UX-økten. Dashbordet viser da graf og tabeller med en gang, og det første produktet er det med svakest prognose. | 2026-11-14 |
| Avrunding til heltall: P10, P50 og P90 rundes halvt opp til heltall rett etter nullgrensen, både i prognosen og i backtesten. Scenariototaler, WAPE og intervalldekning regnes bare fra de avrundede verdiene | Kom fra arkitekturøkten. Kari ser bare heltall, og NFR-5 krever at WAPE og dekning kan regnes etter fra tallene som vises. Se AD-5 i [ARCHITECTURE-SPINE.md](../../_bmad-output/planning-artifacts/architecture/architecture-G96-ellingsen-2026-11-17/ARCHITECTURE-SPINE.md). | 2026-11-17 |
| Next.js låst til eksakt 16.4.6 (`"next": "16.4.6"` uten `^` eller `~`) | `experimental.proxyTimeout`, som hever grensen på 30 s for opplasting gjennom rewrite, er en eksperimentell opsjon uten stabilitetsgaranti. Den er verifisert i kildekoden til 16.4.6. Med eksakt versjon får sensor samme oppsett som gruppen har testet. Se AD-11 i [ARCHITECTURE-SPINE.md](../../_bmad-output/planning-artifacts/architecture/architecture-G96-ellingsen-2026-11-17/ARCHITECTURE-SPINE.md). | 2026-11-17 |
| Hvis F7- eller F8-testen feiler på det syntetiske datasettet i Story 5.4, merkes den med `pytest.mark.xfail(strict=True)` og en `reason` som viser til funnet i `issues.md`. Datasettet, seeden og intervallnivået endres ikke | Avviket blir stående synlig i testkjøringen uten at regelen om grønne tester brytes. `strict=True` gjør at testen blir rød igjen hvis den plutselig består, slik at merket ikke blir liggende glemt. Følger SM-C1 og SM-C2. | 2026-11-17 |
