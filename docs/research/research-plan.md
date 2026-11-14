# Research-plan PROGNOS

## Uavklarte beslutninger
- SQLite eller PostgreSQL? (faglærer anbefalte SQLite)
- Hva skjer med produkter med under 12 måneders historikk? Sesongnaiv trenger minst 12 måneder.
- Kjøres prognosen automatisk etter opplasting, eller med en knapp?
- Negative prognoser: settes P10 til 0? (påvirker F2)
- Scenarioer for 6 måneder totalt: summen av månedlig P10 er ikke P10 for totalen. Hvordan håndterer vi det?
- Backtest: prognoserer hver opprinnelse 1 eller 6 måneder frem?

## Teknisk research
- Les FPP (Hyndman): ETS, prognoseintervaller, tidsserie-kryssvalidering
- Les statsforecast-dokumentasjon: AutoETS, SeasonalNaive, cross_validation
- WAPE: definisjon og hvorfor den brukes i stedet for MAPE
- Testskript (spike): slår ETS baseline? Blir P10 negativ? Hvor god er P10–P90-dekningen?
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
