---
title: PROGNOS
status: final
created: 2026-11-14
updated: 2026-11-17
---

# PRD: PROGNOS v1

**AI-støttet prognoseverktøy for etterspørselsplanleggeren**

Gruppe G96 · IBE160 Programmering med KI · Høgskolen i Molde · Høst 2026

## 0. Om dokumentet

Denne PRD-en beskriver hva PROGNOS v1 skal gjøre. Den er skrevet for gruppen, for faglærer og sensor, og som grunnlag for arkitektur. Den bygger på:

- [PRODUCT_BRIEF.md](../../../../PRODUCT_BRIEF.md), særlig avsnitt 4.1 (v1) og avsnitt 6 (F1–F14)
- [tilbakemelding-product-brief.md](../../../../tilbakemelding-product-brief.md) fra faglærer
- beslutningsloggen i [docs/research/research-plan.md](../../../../docs/research/research-plan.md)
- [arkitektur-utkast.md](../../../../.docs/planning-artifacts/architecture/arkitektur-utkast.md)

Beslutningene i beslutningsloggen er bindende og diskuteres ikke på nytt her. Omfanget er v1 fra briefens avsnitt 4.1. Trinn 2, senere trinn og visjon nevnes bare som «utenfor v1».

**Slik er dokumentet bygd opp:** Ordlista (§3) fastsetter begrepene, og resten av dokumentet bruker dem slik de er definert der. Funksjonene (§4) har globalt nummererte krav (FR-1 til FR-26). Tverrgående krav har egne ID-er (NFR-1 til NFR-9). Akseptansekriteriene F1–F14 er hentet uendret fra briefen (§8.1). Sporbarhetstabellene (§9) viser veien fra brief og tilbakemelding til krav og kriterium. Tolkninger som ikke stod i kildene, er samlet i §11. Teknologivalg står i [addendum.md](addendum.md) og i [arkitekturen](../../architecture/architecture-G96-ellingsen-2026-11-17/ARCHITECTURE-SPINE.md), som har erstattet arkitekturutkastet.

## 1. Visjon for v1

I mange små og mellomstore produksjonsbedrifter lages prognosen som MRP-systemet planlegger ut fra, i et regneark: fjorårets tall pluss en prosentsats og litt magefølelse. Planleggeren leverer ett tall per produkt og måned. Hun vet ikke hvor sikkert tallet er, eller om metoden treffer bedre enn å gjenta fjoråret.

PROGNOS v1 lar etterspørselsplanleggeren laste opp salgshistorikken sin som CSV og få en prognose for 6 måneder per produkt med det samme. Hver prognose har et prediksjonsintervall, tre scenarioer (Pessimistisk, Forventet og Optimistisk) og en backtest som viser om modellen treffer bedre enn sesongnaiv baseline. Dashbordet åpner med de svakeste prognosene øverst, så hun ser først hvor hun bør være skeptisk.

**Tesen:** En prognose som viser hvor usikker den er, og som er etterprøvd mot en enkel baseline, er mer nyttig for planleggeren enn ett tall hun ikke kan vurdere. PROGNOS konkurrerer ikke med kommersielle planleggingsverktøy. Det er en studentprototype som viser dette prinsippet for bedrifter som bruker regneark i dag.

## 2. Målbruker

### 2.1 Jobber som skal gjøres

Primærbruker er **Kari**, etterspørselsplanlegger i en produksjonsbedrift med rundt 100 ansatte og rundt 200 aktive produkter. Hver måned eksporterer hun salgshistorikk fra ERP-systemet og lager prognoser i Excel.

- **Funksjonelt:** Få en prognose per produkt uten å bygge den for hånd i regneark.
- **Funksjonelt:** Vite hvor sikker prognosen er, uttrykt som scenarioer hun kan bruke.
- **Tillit:** Kunne vise, for seg selv og for materialplanleggeren, at metoden treffer bedre enn sesongnaiv baseline («samme måned i fjor»), og se det tydelig når den ikke gjør det.
- **Tid:** Få oversikt raskt og bruke tiden på produktene der prognosen er svak.

### 2.2 Ikke-brukere i v1

Materialplanlegger, innkjøp, salg, marked og ledelse kan ha nytte av prognosen, men PROGNOS v1 er ikke laget for dem. Det finnes ingen roller, ingen innlogging og ingen deling. v1 er en enbrukerapp som kjører lokalt.

### 2.3 Brukerreiser

Brukerreisene følger Karis arbeidsflyt i briefens avsnitt 2: eksport, opplasting, produktliste og graf, og til slutt backtest.

**UJ-1. Kari lager månedens prognose.**
Kari har akkurat eksportert oktober-salget fra ERP-systemet til `salg_2026-10.csv`. Fila har kolonnene `produkt_id`, `maaned` og `antall` og semikolon som skilletegn, slik norsk Excel lagrer. Hun åpner PROGNOS i nettleseren. Ingen innlogging trengs.
1. Hun klikker **Last opp CSV** og velger fila.
2. Valideringsrapporten vises rett under topplinjen. Fila er godkjent med 200 produkter. 2 produkter har en advarsel om utfylte måneder, og 3 produkter har flagget *kort historikk*.
3. Prognosen kjøres automatisk. Hun trenger ikke trykke på noe mer.
4. Produktlisten vises med de svakeste prognosene øverst, og det første produktet er valgt automatisk. Hun ser salgshistorikken, P50 for de neste 6 månedene og prediksjonsintervallet som et skyggelagt bånd. Hun kan velge et annet produkt i listen.
5. Under grafen viser scenariotabellen scenariototalene for de 6 månedene: Pessimistisk 820, Forventet 960 og Optimistisk 1110, med P10/P50/P90 som forklaring.

**Klimaks:** Hun har et tall hun kan gi videre til MRP, og et spenn hun kan bruke i samtalen om sikkerhetsmargin med materialplanleggeren. Selve vurderingen gjør hun selv, for PROGNOS v1 regner ikke ut sikkerhetslager.
**Resultat:** Datasettet er lagret og kan åpnes igjen senere (UJ-4).
**Kanttilfelle:** Et nytt produkt med 8 måneders historikk står i produktlisten med flagget *kort historikk* og uten prognose. Kari vet at hun må anslå det selv.

**UJ-2. Kari får fila avvist og retter den.**
Kari laster opp en eksport der to rader har samme produkt og måned, og der én rad har `antall` = `12,5`. Hele fila avvises, og valideringsrapporten viser hver feil, med radnummer der det gjelder. Eksempler er «Duplikat: P-104, 2025-03 (rad 17 og 233)» og «Rad 418: antall må være et heltall ≥ 0». Ingenting lagres. Hun retter fila i Excel og laster den opp på nytt, og da blir den godkjent. Videre går det som i UJ-1.

**UJ-3. Kari sjekker om hun kan stole på prognosen.**
Kari ser produkt P-109 blant de flaggede øverst i produktlisten, med flagget *ETS taper*. Hun velger det. Backtest-tabellen viser WAPE for ETS (24 %) og for sesongnaiv baseline (19 %) over de siste 6 månedene, og intervalldekningen for begge modellene. ETS-prognosen vises likevel, men nå vet hun at «samme måned i fjor» har truffet bedre for dette produktet, og hun bruker skjønn. Nederst viser WAPE-oversikten at ETS har lavere total WAPE enn baseline, og at ETS slår baseline for 162 av de 180 produktene som har backtest for begge modellene.

**UJ-4. Kari åpner forrige måneds datasett igjen.**
Neste dag starter Kari PROGNOS på nytt. I datasettvelgeren velger hun `salg_2026-10.csv`. Valideringsrapporten fra opplastingen, produktlisten, prognosene og backtestene vises akkurat som i går, uten at noe kjøres på nytt.

## 3. Ordliste

**Data og validering**

- **Datasett** — Én godkjent CSV-opplasting, lagret med salgshistorikk, valideringsrapport, prognoser og backtest-resultater. Datasettet vises i grensesnittet med filnavn og tidspunkt for opplasting. Bare godkjente filer blir datasett. Et datasett har ett eller flere produkter.
- **Produkt** — En vare identifisert med `produkt_id` i et datasett.
- **Salgshistorikk** — Månedlig `antall` solgt per produkt, med `maaned` på formatet ÅÅÅÅ-MM.
- **Siste måned i datasettet** — Den seneste `maaned` i fila. Den er felles for alle produktene i datasettet.
- **Utfylt måned** — En måned som manglet i fila og er fylt inn med `antall` = 0. Utfylling gjelder fra produktets første måned til og med siste måned i datasettet.
- **Historikklengde** — Antall måneder fra og med produktets første måned til og med siste måned i datasettet, etter utfylling. Eksempel: 2024-11 til 2026-10 er 24 måneder.
- **Historikknivå** — Klassifisering av et produkt etter historikklengde: *ingen* (under 12 mnd), *sesongnaiv* (12–23 mnd) eller *ets* (24 mnd eller mer).
- **Valideringsrapport** — Resultatet av en opplasting: status (godkjent eller avvist), feil, advarsler og antall produkter per historikknivå.
- **Feil** — Brudd på en valideringsregel. Én eller flere feil avviser hele fila.
- **Advarsel** — Merknad som ikke stopper opplastingen. I v1 gis det én advarsel per produkt som har utfylte måneder.

**Prognose og scenarioer**

- **ETS** — Eksponentiell glatting (error, trend, season), modellen i PROGNOS v1.
- **Sesongnaiv baseline** (kort: **baseline**) — Referanseprognose der hver måned får samme verdi som samme måned året før.
- **Prognose** — Månedlige verdier P10, P50 og P90 for ett produkt gjennom horisonten. Prognosen til ett produkt kalles også **prognoseserie**.
- **Horisont** — De 6 månedene etter siste måned i datasettet. Fast i v1.
- **P10 / P50 / P90** — Nedre grense, punktprognose og øvre grense i et 80 % prediksjonsintervall. Ingen verdi er under 0.
- **Prediksjonsintervall** — Spennet P10–P90 for én måned.
- **Scenario** — *Pessimistisk* (= P10), *Forventet* (= P50) eller *Optimistisk* (= P90). Scenarionavnene er hovedordene i grensesnittet, og P10/P50/P90 står som forklaring.
- **Scenariototal** — Summen av de månedlige verdiene i et scenario gjennom horisonten.

**Backtest**

- **Backtest** — Rullerende etterprøving med 6 opprinnelser over de siste 6 månedene i datasettet. Hver opprinnelse prognoserer 1 måned frem.
- **Opprinnelse** — Siste måned modellen får trene på i ett backtest-steg.
- **WAPE** — Weighted Absolute Percentage Error = Σ|faktisk − P50| / Σ faktisk. Beregnes per produkt og modell, og totalt. WAPE er udefinert når Σ faktisk = 0.
- **Intervalldekning** — Andelen faktiske verdier i backtesten som ligger innenfor P10–P90.
- **ETS slår baseline** — ETS har strengt lavere WAPE enn sesongnaiv baseline for et produkt. Når verdiene er like, slår ikke ETS baseline, og ETS taper heller ikke.
- **Flagg** — Markering av et produkt i produktlisten. v1 har to flagg: *kort historikk* (historikknivå *ingen* eller *sesongnaiv*) og *ETS taper* (ETS har strengt høyere WAPE enn sesongnaiv baseline).

**Dashbord**

- **Dashbord** — Den ene siden i PROGNOS. Den består av topplinje, produktliste, graf, scenariotabell, backtest-tabell og WAPE-oversikt.
- **Topplinje** — Øverste del av dashbordet med datasettvelgeren, knappen **Last opp CSV** og valideringsrapporten.
- **Datasettvelger** — Nedtrekksliste med alle lagrede datasett.
- **Produktliste** — Listen over produktene i valgt datasett, med WAPE og flagg.
- **Scenariotabell** — Tabell med de tre scenarioene og scenariototalene for valgt produkt.
- **Backtest-tabell** — Tabell med WAPE og intervalldekning per modell for valgt produkt.
- **WAPE-oversikt** — Linje nederst med total WAPE for begge modellene og antall produkter der ETS slår baseline.

**Testdata**

- **Syntetisk CSV-fil** — Generert salgshistorikk med kjent trend, sesong og støy, laget med fast seed. Når den er lastet inn, blir den et datasett som alle andre.
- **Fasit** — Parameterne som den syntetiske CSV-fila er generert fra: trend, sesongprofil og støynivå per produkt.

## 4. Funksjoner

### 4.1 CSV-import og validering

**Beskrivelse:** Kari laster opp én CSV-fil fra dashbordet. PROGNOS gjenkjenner skilletegnet, validerer fila og gir en valideringsrapport. Hvis det finnes én eller flere feil, avvises hele fila, og ingenting lagres. Advarsler stopper ikke opplastingen. En godkjent fil blir et datasett som lagres lokalt, og prognose og backtest kjøres automatisk. Funksjonen realiserer UJ-1, UJ-2 og UJ-4.

#### FR-1: Opplasting av CSV

Kari kan laste opp én CSV-fil med kolonnene `produkt_id`, `maaned` og `antall` fra topplinjen. Realiserer UJ-1.

**Konsekvenser (testbare):**
- En gyldig fil gir en valideringsrapport med status godkjent og antall produkter per historikknivå.
- Kolonner i fila utover de tre påkrevde ignoreres.
- Fila leses som UTF-8, med eller uten BOM.

**Utenfor omfang:**
- Flere filer i samme opplasting.

#### FR-2: Automatisk gjenkjenning av skilletegn

Systemet gjenkjenner komma eller semikolon som skilletegn uten at Kari må velge. Skilletegnet bestemmes ut fra overskriftslinja: det tegnet som gir de tre påkrevde kolonnene, gjelder. Realiserer UJ-1. Verifiseres av **F13**.

**Konsekvenser (testbare):**
- Samme innhold med komma og med semikolon gir identisk salgshistorikk, prognose og backtest. Filnavn og tidspunkt er unntatt.
- I en fil med semikolon gir verdien `12,5` feilen for heltall fra FR-3, ikke en feil om skilletegnet.
- Hvis verken komma eller semikolon gir de tre påkrevde kolonnene, avvises fila med en feil.

#### FR-3: Validering og avvisning

Systemet avviser en fil som bryter en valideringsregel, og sier hva som er feil. Radnummer er linjenummeret i fila, og overskriftslinja er linje 1. Realiserer UJ-2. Verifiseres av **F4**.

**Konsekvenser (testbare):**
- En manglende påkrevd kolonne gir en feil som nevner kolonnen ved navn.
- `maaned` som ikke er på formatet ÅÅÅÅ-MM med måned 01–12, gir en feil med radnummer.
- `antall` som er negativt eller ikke er et heltall, gir en feil med radnummer.
- En tom celle i en påkrevd kolonne gir en feil med radnummer.
- To rader med samme `produkt_id` og `maaned` gir en feil som nevner produktet, måneden og begge radnumrene.
- En fil uten datarader gir en feil.
- Én eller flere feil avviser hele fila, og ingenting lagres.
- Valideringsrapporten viser alle feilene i fila, ikke bare den første.

#### FR-4: Utfylling av manglende måneder

Systemet fyller manglende måneder fra produktets første måned til og med siste måned i datasettet med `antall` = 0, og gir en advarsel. Realiserer UJ-1. Verifiseres av **F14**.

**Konsekvenser (testbare):**
- En serie med én manglende måned får én utfylt måned med `antall` = 0.
- Et produkt som mangler de siste månedene frem til og med siste måned i datasettet, får dem fylt med 0.
- Valideringsrapporten har én advarsel per produkt med utfylte måneder, og advarselen lister de utfylte månedene.
- Fila godkjennes hvis det ikke finnes andre feil.

#### FR-5: Historikknivå per produkt

Systemet gir hvert produkt et historikknivå ut fra historikklengden, og flagger produkter med kort historikk. Realiserer UJ-1 (kanttilfelle). Verifiseres av **F5**. Beslutningslogg: *Kort historikk*.

| Historikklengde | Historikknivå | Prognose | Flagg |
|---|---|---|---|
| Under 12 mnd | *ingen* | Ingen | *kort historikk* |
| 12–23 mnd | *sesongnaiv* | Bare sesongnaiv baseline | *kort historikk* |
| 24 mnd eller mer | *ets* | ETS, med sesongnaiv baseline ved siden av | — |

**Konsekvenser (testbare):**
- Historikklengden regnes etter utfylling (FR-4), med begge endepunktene medregnet.
- Grensetester: 11 og 12, 23 og 24 måneder gir hvert sitt historikknivå slik tabellen viser.
- Valideringsrapporten viser antall produkter per historikknivå.

#### FR-6: Lagring og gjenåpning av datasett

Systemet lagrer et godkjent datasett i en lokal SQLite-database, og Kari kan åpne det igjen senere. Realiserer UJ-4. Verifiseres av **F11**. Beslutningslogg: *Database*.

**Konsekvenser (testbare):**
- Svarene fra API-et for produktlisten og for ett produkt er like før og etter omstart av backend.
- Å åpne et lagret datasett kjører ikke prognose eller backtest på nytt.
- En ny opplasting av samme fil gir et nytt datasett. Eksisterende datasett blir ikke overskrevet eller slettet.

**Utenfor omfang:**
- Sletting og omdøping av datasett.

#### FR-7: Automatisk prognosekjøring

Når fila er godkjent, kjøres prognose, scenarioer og backtest automatisk, uten at Kari må gjøre noe mer. Opplasting, validering, prognose og backtest skjer i én og samme forespørsel. Realiserer UJ-1. Beslutningslogg: *Prognosen kjøres automatisk*.

**Konsekvenser (testbare):**
- Svaret på en godkjent opplasting inneholder datasettets id, og produktlisten for datasettet kan hentes rett etterpå uten flere handlinger.
- En avvist fil starter ingen prognosekjøring.
- Hvis prognose- eller backtest-kjøringen feiler, lagres ingenting, og valideringsrapporten viser en feilmelding.

### 4.2 Prognose

**Beskrivelse:** For hvert produkt med historikknivå *ets* eller *sesongnaiv* lager PROGNOS en månedlig prognose gjennom horisonten. Produkter med historikknivå *ets* får prognosen fra ETS, og sesongnaiv baseline beregnes ved siden av. Produkter med historikknivå *sesongnaiv* får bare sesongnaiv baseline. Hver måned i prognosen har P10, P50 og P90. Funksjonen realiserer UJ-1.

#### FR-8: Prognose per produkt

Systemet lager én prognoseserie per produkt med historikknivå *ets* eller *sesongnaiv*. Realiserer UJ-1. Verifiseres av **F1** og **F3**.

**Konsekvenser (testbare):**
- En CSV med 24 måneders salg for ett produkt gir en prognose for 6 måneder med P10/P50/P90 (F1).
- En CSV med flere produkter gir én prognoseserie per produkt med historikknivå *ets* eller *sesongnaiv*.
- Alle `produkt_id` fra input finnes i output (F3). Produkter med historikknivå *ingen* finnes i output med flagget *kort historikk*, men uten prognoseserie.
- Horisonten er de 6 månedene etter siste måned i datasettet, og den er lik for alle produktene.

#### FR-9: Prediksjonsintervall og nullgrense

Systemet gir P10 og P90 som grensene i et 80 % prediksjonsintervall og setter alle verdier til minst 0. Realiserer UJ-1. Verifiseres av **F2**. Beslutningslogg: *Intervaller* og *P10, P50 og P90 settes til minst 0*.

**Konsekvenser (testbare):**
- For hver prognosemåned gjelder P10 ≤ P50 ≤ P90.
- Ingen P10-, P50- eller P90-verdi er negativ.

#### FR-10: Modell etter historikknivå

Systemet velger modell ut fra historikknivået (FR-5). Realiserer UJ-1. Verifiseres av **F5**.

**Konsekvenser (testbare):**
- Et produkt med historikknivå *sesongnaiv* (12–23 mnd) får bare sesongnaiv prognose.
- Et produkt med historikknivå *ingen* (under 12 mnd) får ingen prognose.
- Et produkt med historikknivå *ets* (24 mnd eller mer) får ETS-prognose, og sesongnaiv baseline beregnes også.
- Prognosen som vises i graf og scenariotabell, er ETS-prognosen for historikknivå *ets* og den sesongnaive prognosen for historikknivå *sesongnaiv*.

**Utenfor omfang:**
- Visning av den sesongnaive prognosen for produkter med historikknivå *ets*. Baseline brukes der bare i backtesten.
- Andre modeller, automatisk modellvalg og overstyring av prognosen. Utenfor v1.

### 4.3 Scenarioer

**Beskrivelse:** Hvert produkt med prognose får tre scenarioer fra prognosen som vises (FR-10). Scenarionavnene er hovedordene i grensesnittet, og P10/P50/P90 står som forklaring, fordi planleggere forstår scenarioer bedre enn kvantiler. Funksjonen realiserer UJ-1. Beslutningslogg: *Pessimistisk/Forventet/Optimistisk*.

#### FR-11: Tre scenarioer per produkt

Systemet viser scenarioene Pessimistisk = P10, Forventet = P50 og Optimistisk = P90 for hver måned i horisonten. Realiserer UJ-1. Verifiseres av **F6**.

**Konsekvenser (testbare):**
- For hvert produkt med prognose gjelder Pessimistisk ≤ Forventet ≤ Optimistisk i hver måned.
- Scenarioverdiene er identiske med de tilsvarende P10-, P50- og P90-verdiene.
- Produkter med historikknivå *ingen* har ingen scenarioer.

#### FR-12: Scenariototal for horisonten

Systemet viser scenariototalen for hvert scenario som summen av de månedlige verdiene, sammen med en merknad om at spennet mellom scenariototalene er bredere enn det reelle. Realiserer UJ-1. Verifiseres av **F6**. Beslutningslogg: *Scenarioer for 6 mnd*.

**Konsekvenser (testbare):**
- Scenariototalen for Forventet er lik summen av P50 gjennom horisonten. Det samme gjelder for Pessimistisk (P10) og Optimistisk (P90).
- Merknaden vises alltid sammen med scenariototalene, med denne teksten: «Totalene er summer av månedlige verdier. Det reelle spennet mellom Pessimistisk og Optimistisk er smalere enn det som vises.»

**Utenfor omfang:**
- Simulering av totaler og egendefinerte «hva hvis»-scenarioer. Utenfor v1.

### 4.4 Backtest

**Beskrivelse:** PROGNOS etterprøver modellen mot sesongnaiv baseline på de siste 6 månedene i datasettet. Ved hver av de 6 opprinnelsene prognoserer modellen 1 måned frem, og opprinnelsen flyttes 1 måned om gangen. Prinsippet er *baseline først*: ETS vises aldri uten WAPE for sesongnaiv baseline ved siden av. ETS trenger 24 måneders salgshistorikk ved hver opprinnelse, og sesongnaiv baseline trenger 12. Når ETS taper mot baseline, vises ETS-prognosen likevel, men produktet flagges, og begge WAPE-tallene vises. Funksjonen realiserer UJ-3. Beslutningslogg: *Backtest*, *Når ETS taper*, *Backtest for 12–17 mnd* og *Total WAPE*.

#### FR-13: Rullerende backtest

Systemet kjører en rullerende backtest med 6 opprinnelser. Hver opprinnelse prognoserer 1 måned frem, og opprinnelsen flyttes 1 måned om gangen. Realiserer UJ-3.

**Konsekvenser (testbare):**
- Et produkt med 36 måneders historikk får 6 backtest-prognoser per modell, én for hver av de siste 6 månedene i datasettet.
- Ved hver opprinnelse bruker modellen bare salgshistorikk til og med opprinnelsen.

#### FR-14: WAPE per produkt og totalt

Systemet beregner WAPE for ETS og for sesongnaiv baseline, per produkt og totalt. Realiserer UJ-3. Verifiseres av **F7**.

**Konsekvenser (testbare):**
- WAPE beregnes som Σ|faktisk − P50| / Σ faktisk over de 6 opprinnelsene.
- Total WAPE for ETS og for sesongnaiv baseline summeres over de samme produktene og opprinnelsene, altså bare over produkter som har backtest for begge modellene. Produkter med bare baseline-backtest får WAPE per produkt, men inngår ikke i totalen.
- Når Σ faktisk = 0 for et produkt, vises WAPE som «–». Produktet inngår ikke i totalen og kan ikke få flagget *ETS taper*. Beslutningslogg: *WAPE når faktisk salg er 0*.
- På det syntetiske datasettet har ETS lavere total WAPE enn sesongnaiv baseline (F7).

#### FR-15: Intervalldekning

Systemet beregner intervalldekningen for P10–P90 i backtesten per modell, per produkt og totalt. Realiserer UJ-3. Verifiseres av **F8**. Beslutningslogg: *Intervalldekning og sortering*.

**Konsekvenser (testbare):**
- Intervalldekningen beregnes etter nullgrensen (FR-9).
- Total intervalldekning regnes over de samme produktene og opprinnelsene som total WAPE (FR-14).
- F8 gjelder total intervalldekning for ETS. På det syntetiske datasettet ligger den mellom 65 % og 95 %.

#### FR-16: Backtest etter historikklengde

Systemet tilpasser backtesten til historikklengden. Realiserer UJ-3.

| Historikklengde | Backtest |
|---|---|
| Under 18 mnd | Ingen |
| 18–29 mnd | Bare sesongnaiv baseline |
| 30 mnd eller mer | ETS og sesongnaiv baseline |

**Konsekvenser (testbare):**
- Et produkt med 12–17 måneders historikk får sesongnaiv prognose, men ingen backtest. WAPE vises som «–».
- Et produkt med 18–29 måneders historikk får bare baseline-backtest, også når det får ETS-prognose (24–29 mnd).
- Grensetester: 17 og 18, 29 og 30 måneder gir backtest slik tabellen viser.

#### FR-17: Flagget *ETS taper*

Når ETS har strengt høyere WAPE enn sesongnaiv baseline for et produkt, vises ETS-prognosen likevel, men produktet får flagget *ETS taper*, og begge WAPE-tallene vises. Realiserer UJ-3.

**Konsekvenser (testbare):**
- Et produkt der ETS har strengt høyere WAPE enn baseline, har flagget *ETS taper* og viser begge WAPE-tallene.
- Prognosen som vises for produktet, er fortsatt ETS-prognosen.
- Like WAPE-verdier gir ikke flagget.
- Produkter uten ETS-backtest får aldri flagget *ETS taper*.
- Flagget testes med en konstruert serie der ETS taper, uavhengig av det syntetiske datasettet.

### 4.5 Dashbord

**Beskrivelse:** PROGNOS har én side. Topplinjen ligger øverst. Produktlisten står til venstre, med de svakeste prognosene øverst, og grafen for valgt produkt står i midten. Under grafen ligger scenariotabellen til venstre og backtest-tabellen til høyre. WAPE-oversikten ligger nederst. Skissen i briefens avsnitt 4.1 del 5 viser oppsettet. Funksjonen realiserer UJ-1, UJ-2, UJ-3 og UJ-4. F10 verifiserer graf og scenariotabell. Resten av kravene dekkes av NFR-6.

#### FR-18: Topplinje med datasettvelger, opplasting og valideringsrapport

Kari kan velge et lagret datasett, laste opp en ny fil og se valideringsrapporten i topplinjen. Realiserer UJ-1, UJ-2 og UJ-4.

**Konsekvenser (testbare):**
- Datasettvelgeren viser alle lagrede datasett med filnavn og tidspunkt for opplasting. Nyeste datasett er valgt som standard.
- Etter opplasting vises valideringsrapporten rett under topplinjen. En avvist fil viser feilene. En godkjent fil viser en linje på formen «✓ 200 produkter godkjent · 3 flagget (kort historikk)», og under den advarslene.
- Når et lagret datasett velges, vises valideringsrapporten fra opplastingen av det.
- Etter en godkjent opplasting blir det nye datasettet valgt.

#### FR-19: Produktliste med de svakeste øverst

Systemet viser produktene i valgt datasett sortert slik at de svakeste prognosene står øverst, med flagg. Realiserer UJ-1 og UJ-3. Beslutningslogg: *Sortering av produktlisten* og *Intervalldekning og sortering*.

**Konsekvenser (testbare):**
- Rekkefølgen er:
  1. Flaggede produkter, sortert etter WAPE med høyest først. Flaggede produkter uten WAPE kommer sist i gruppen.
  2. Uflaggede produkter med WAPE «–».
  3. Resten, sortert etter WAPE med høyest først.
- Like verdier sorteres etter `produkt_id` stigende, så rekkefølgen er alltid den samme.
- WAPE i produktlisten er WAPE for ETS når produktet har ETS-backtest, ellers WAPE for sesongnaiv baseline.
- Hvert produkt med flagget *kort historikk* eller *ETS taper* viser flagget i produktlisten.
- Når Kari velger et produkt, oppdateres graf, scenariotabell og backtest-tabell.

#### FR-26: Søk i produktlisten

Kari kan filtrere produktlisten på `produkt_id` med et søkefelt. Sorteringen fra FR-19 beholdes. Realiserer UJ-1 og UJ-3. Beslutningslogg: *Søk i produktlisten*.

**Konsekvenser (testbare):**
- Treffene er produktene der `produkt_id` inneholder søketeksten, uavhengig av store og små bokstaver.
- Treffene står i samme rekkefølge som i FR-19.
- Et tomt søkefelt viser alle produktene.
- Valgt produkt blir stående i graf og tabeller, også når det faller utenfor filteret.

**Utenfor omfang:**
- Søk på andre felt enn `produkt_id`.

#### FR-20: Graf per produkt

Systemet viser en graf for valgt produkt med salgshistorikk, P50 og prediksjonsintervallet P10–P90 som et skyggelagt bånd. Realiserer UJ-1. Verifiseres av **F10**.

**Konsekvenser (testbare):**
- Salgshistorikken og prognosen vises langs samme månedsakse. Prognosen tegnes med stiplet linje, og en loddrett markør står ved første måned i horisonten.
- Et produkt med historikknivå *ingen* viser salgshistorikken og teksten «Ingen prognose: under 12 måneders historikk».

#### FR-21: Scenariotabell og backtest-tabell

Systemet viser scenariotabellen og backtest-tabellen for valgt produkt. Realiserer UJ-1 og UJ-3. Scenariotabellen verifiseres av **F10**.

**Konsekvenser (testbare):**
- Scenariotabellen viser Pessimistisk, Forventet og Optimistisk med scenariototal og P10/P50/P90 som forklaring, og merknaden fra FR-12.
- Backtest-tabellen viser WAPE og intervalldekning for ETS og for sesongnaiv baseline, og om ETS slår baseline.
- Backtest-tabellen kan utvides til å vise faktisk verdi og P50 for hver modell ved hver av de 6 opprinnelsene, slik at WAPE kan regnes etter (NFR-5).
- Når produktet bare har baseline-backtest, viser ETS-kolonnen teksten «ETS er ikke backtestet (under 30 måneders historikk)».
- Når produktet ikke har noen backtest, viser backtest-tabellen teksten «Ingen backtest (under 18 måneders historikk)».

#### FR-22: WAPE-oversikt for alle produkter

Systemet viser total WAPE for ETS og for sesongnaiv baseline, og antall produkter der ETS slår baseline. Realiserer UJ-3.

**Konsekvenser (testbare):**
- WAPE-oversikten viser total WAPE for begge modellene over de samme produktene (FR-14), og «n av m» produkter der ETS slår baseline. Her er m antall produkter med backtest for begge modellene og definert WAPE.
- WAPE-oversikten bygger på lagrede backtest-data og er lik før og etter omstart (F11).

### 4.6 Syntetisk datasett

**Beskrivelse:** Et skript genererer en syntetisk CSV-fil med kjent trend, sesong og støy, og skriver fasiten ved siden av. Fila brukes i automatiske tester og i demo, og lastes inn som datasett ved oppstart hvis databasen er tom. Fordi fasiten er kjent, kan gruppen sjekke at ETS fanger opp sesong og trend. Funksjonen støtter verifiseringen av F7, F8 og F9, og gjør at sensor ser data med en gang appen starter. Beslutningslogg: *Syntetiske data*.

#### FR-23: Generator med fast seed

Skriptet gir identisk syntetisk CSV-fil ved samme seed. Verifiseres av **F9**.

**Konsekvenser (testbare):**
- To kjøringer med samme seed gir byte-identiske filer, både CSV-fila og fasiten.

#### FR-24: Innholdet i den syntetiske CSV-fila

Den syntetiske CSV-fila dekker alle historikknivåene og backtest-grensene, og gir ETS noe reelt å slå baseline på.

**Konsekvenser (testbare):**
- 20 produkter har 36 måneders historikk. Minst 15 av dem har trend i tillegg til sesong og støy, og minst 2 er flate serier med mye støy.
- I tillegg finnes 4 produkter med kortere historikk: ett med 8 mnd, ett med 15 mnd, ett med 20 mnd og ett med 26 mnd.
- Generatoren skriver fasiten for hvert produkt (trend, sesongprofil og støynivå) til en egen fil.
- For et produkt generert uten støy, med kjent trend og sesong, ligger P50 fra ETS innenfor 5 % av fasiten i hver måned i horisonten.

#### FR-25: Innlasting ved tom database

Når backend starter og databasen er tom, lastes den syntetiske CSV-fila inn og blir et datasett med prognose og backtest.

**Konsekvenser (testbare):**
- Første oppstart med tom database gir ett datasett i datasettvelgeren.
- Oppstart med en database som allerede har data, legger ikke til noe nytt.

## 5. Tverrgående krav (NFR)

| ID | Krav | Testbar betingelse | Kriterium |
|---|---|---|---|
| **NFR-1** | **Lokal kjøring uten Docker, nøkler eller betalte tjenester.** Backend og frontend starter med kommandoene i README uten Docker, hemmeligheter eller API-nøkler. Appen bruker ingen betalte tjenester og kaller ingen eksterne tjenester mens den kjører. Bare installasjonen av avhengigheter trenger nett. README lister forutsetningene med versjoner og kommandoene for installasjon, start og alle testene. Den forteller også at den syntetiske CSV-fila lastes inn automatisk (FR-25). | Kommandoene i README starter appen på en maskin uten Docker og uten miljøvariabler eller `.env`-fil. UJ-1 fungerer med nettverket koblet fra etter installasjonen. | F12 |
| **NFR-2** | **Automatisk database og helsesjekk.** Databasefila opprettes automatisk første gang backend starter. | `GET /api/health` svarer OK etter første oppstart. | F12 |
| **NFR-3** | **Varig lagring.** Data overlever omstart av backend. Kravet står i FR-6. Denne raden finnes for sporbarheten til F11. | Se FR-6. | F11 |
| **NFR-4** | **Norsk.** Grensesnitt, feilmeldinger, valideringsrapport og dokumentasjon er på norsk. Beslutningslogg: *Språk*. | Ingen engelske brukertekster i dashbordet, bortsett fra fagbegrepene i ordlista (§3). Playwright-testen sjekker overskriftene og scenarionavnene. | — |
| **NFR-5** | **Etterprøvbarhet.** Scenariototaler, WAPE og intervalldekning kan regnes etter for hånd fra tallene som vises (FR-21). | Et lite testdatasett med håndregnet fasit for scenariototaler, WAPE og intervalldekning ligger sammen med testene, og testene sjekker mot den. | F6, F7, F8 |
| **NFR-6** | **Testdekning.** F1–F14 er dekket av automatiske tester som kjører grønt, og F10 testes med Playwright. I tillegg har hver testbare konsekvens i FR-1 til FR-26 minst ett automatisk testtilfelle. | Testkjøringen er grønn. | F1–F14 |
| **NFR-7** | **Svartid.** Opplasting av et datasett på Karis størrelse (200 produkter × 36 måneder) gir valideringsrapport, prognose og backtest innen 60 sekunder. | Tidtaking i en test med en generert fil av denne størrelsen, kjørt etter én oppvarmingskjøring på utviklerens PC. Maskinens spesifikasjon står i README. | — |
| **NFR-8** | **Enbrukerapp.** Ingen innlogging, roller eller samtidige brukere. | Ingen API-endepunkter krever autentisering, og dashbordet har ingen innloggingsside. | — |
| **NFR-9** | **Ryddig repo.** Generatoren og den syntetiske CSV-fila med fasit ligger i en egen mappe for testdata. Databasefila ligger i en fast mappe som er ignorert i git. Repoet inneholder ingen hemmeligheter. `.env.example` finnes og forklarer at v1 ikke trenger miljøvariabler. | `git ls-files` lister ingen `.db`- eller `.env`-filer. | — |

## 6. Ikke-mål

PROGNOS er ikke, og blir ikke:

- **Et MRP-system.** Ingen BOM, netto behov, innkjøpsordrer eller detaljert produksjonsplanlegging. PROGNOS leverer etterspørselen som MRP planlegger ut fra.
- **En beslutningsmaskin.** Et menneske bestemmer alltid. I v1 viser systemet prognoser og gir ingen anbefalinger. Anbefalinger kommer først i trinn 2.
- **Et verktøy for prisoptimalisering, leverandørstyring, budsjettering eller regnskap.**
- **En innsamler av markedsdata.** Brukeren leverer dataene.
- **En konkurrent til kommersielle planleggingsverktøy.** PROGNOS er en prototype som viser et prinsipp.

## 7. Omfang

### 7.1 I v1

v1 består av de fem delene i briefens avsnitt 4.1, pluss det syntetiske datasettet som støtte:

1. CSV-import med enkel validering og lokal lagring (§4.1)
2. Én modell (ETS) mot sesongnaiv baseline, med P10/P50/P90 (§4.2)
3. Tre scenarioer med scenariototal (§4.3)
4. Backtest med WAPE og intervalldekning (§4.4)
5. Dashbord på én side (§4.5)
6. Syntetisk datasett med fast seed og fasit (§4.6)

### 7.2 Utenfor v1

Følgende er utenfor v1 og beskrives ikke nærmere i denne PRD-en:

- **Trinn 2** (briefens avsnitt 4.2): beslutningspunktet produksjon vs. lager, med sikkerhetslager, og forklaring i klartekst med mock-modus. Kriteriene B1–B3 og L1 i briefens avsnitt 6 hører hit.
- **Senere trinn** (briefens avsnitt 4.3): overstyring og godkjenning, flere modeller og modellvalg, SHAP, kampanjer og kundebestillinger, «hva hvis»-scenarioer, optimering, outsourcing-analyse og MRP-eksport.
- **Visjon** (briefens avsnitt 4.4): en integrert modul for etterspørselsstyring i MRP.
- Innlogging, brukerkontoer, deling, deploy og flere samtidige brukere.
- Flere filer per opplasting, eksport fra dashbordet og datasett større enn 200 produkter × 36 måneder (NFR-7).

## 8. Suksesskriterier

### 8.1 Akseptansekriterier F1–F14

Kriteriene er hentet uendret fra briefens avsnitt 6. Hvert kriterium blir minst ett automatisk testtilfelle.

| # | Kriterium | Krav |
|---|---|---|
| F1 | En opplastet CSV med 24 måneders salg for ett produkt gir en prognose for 6 måneder med P10/P50/P90. | FR-8, FR-9 |
| F2 | For hver prognosemåned gjelder P10 ≤ P50 ≤ P90, og ingen verdi er negativ. | FR-9 |
| F3 | En CSV med flere produkter gir én prognoseserie per produkt, og alle `produkt_id` fra input finnes i output. | FR-8 |
| F4 | En CSV som mangler en påkrevd kolonne, har ugyldig dato, negativt antall, antall som ikke er et heltall, eller duplikater (samme produkt og måned), blir avvist med en feilmelding som sier hva som er feil. | FR-3 |
| F5 | Et produkt med 12–23 måneders historikk blir flagget og får bare sesongnaiv prognose. Et produkt med under 12 måneders historikk blir flagget og får ingen prognose. | FR-5, FR-10 |
| F6 | Hvert produkt får tre scenarioer der pessimistisk = P10, forventet = P50 og optimistisk = P90, og pessimistisk ≤ forventet ≤ optimistisk. | FR-11, FR-12 |
| F7 | Backtesten viser lavere total WAPE for ETS enn for sesongnaiv baseline på det syntetiske datasettet. | FR-13, FR-14, FR-24 |
| F8 | Intervalldekningen for P10–P90 i backtesten på det syntetiske datasettet ligger mellom 65 % og 95 %. | FR-13, FR-15, FR-24 |
| F9 | Generatoren for syntetiske data gir identisk datasett ved samme seed. | FR-23 |
| F10 | Dashbordet viser historikk, prognose, intervall og scenarioer for valgt produkt uten feil (testet med Playwright). | FR-20, FR-21 |
| F11 | Et opplastet datasett med prognose og backtest lagres i SQLite-databasen og kan hentes uendret via API etter at backend er startet på nytt. | FR-6, FR-22, NFR-3 |
| F12 | Backend og frontend starter med kommandoene i README uten Docker, hemmeligheter eller API-nøkler. Databasefila opprettes automatisk, og `GET /api/health` svarer OK. | NFR-1, NFR-2 |
| F13 | En CSV med semikolon som skilletegn gir samme resultat som samme fil med komma. | FR-2 |
| F14 | En manglende måned i en produktserie fylles med 0 og gir en advarsel i valideringsrapporten. | FR-4 |

Ved lesing av kriteriene gjelder dette: F3 og F6 omfatter produkter med historikknivå *ingen* uten prognoseserie og uten scenarioer (FR-8, FR-11). I F9 betyr «identisk datasett» byte-identisk syntetisk CSV-fil (FR-23).

### 8.2 Kvalitetsmål

- **SM-1 (primær): Modellen slår baseline.** ETS har lavere total WAPE enn sesongnaiv baseline i backtesten på det syntetiske datasettet (F7). Faglærer anbefalte at dette skulle være det viktigste kvalitetskriteriet. Validerer FR-13 og FR-14.
- **SM-2: Intervallene er ærlige.** Total intervalldekning for ETS ligger mellom 65 % og 95 % (F8). Validerer FR-9 og FR-15.
- **SM-3: Hele v1 er testet.** F1–F14 og alle testbare konsekvenser er dekket av automatiske tester som kjører grønt (NFR-6).

**Motvekter (skal ikke optimeres):**
- **SM-C1: Ikke tilpass det syntetiske datasettet for å få F7 grønn.** Datasettet skal beholde flate serier med mye støy, der ETS kan tape (FR-24). Trend og støy skal ikke justeres produkt for produkt for å senke WAPE. Motvekt til SM-1.
- **SM-C2: Ikke smalne inn intervallene for å se presise ut.** Dekning over 95 % er like galt som under 65 %. Intervallnivået ligger fast på 80 %. Motvekt til SM-2.

### 8.3 Prosjektsuksess (IBE160)

- En fungerende prototype som dekker hele v1, med F1–F14 grønne.
- Dokumentert bruk av KI både *i* produktet (prognosemodellen) og *i* utviklingen (koding, testing og kvalitetssikring).
- Om PROGNOS faktisk er mer nyttig for planleggeren, måles ikke i v1. SM-1 og SM-2 måles på data gruppen har generert selv.
- Forretningsmål som lavere lagerbinding og høyere leveringsgrad hører til visjonen og måles ikke i emnet.

## 9. Sporbarhet

### 9.1 Brief → PRD → kriterium

| Brief-avsnitt | Innhold | Krav i PRD | F-kriterium |
|---|---|---|---|
| Executive brief, §1 Problem | Prognose med usikkerhet og etterprøving i stedet for ett tall i regneark | §1, FR-8, FR-9, FR-11, FR-14 | F1, F2, F6, F7 |
| §2 Målgruppe, behov «prognose uten regneark» | Last opp CSV → prognose for alle produkter | FR-1, FR-7, FR-8, UJ-1 | F1, F3 |
| §2 Målgruppe, behov «vite hvor sikker» | P10/P50/P90 og tre scenarioer | FR-9, FR-11, FR-12, UJ-1 | F2, F6 |
| §2 Målgruppe, behov «stole på metoden» | Backtest med WAPE mot sesongnaiv baseline | FR-13–FR-17, UJ-3 | F7, F8 |
| §2 Målgruppe, behov «oversikt raskt» | Dashbord med historikk, prognose og intervall | FR-18–FR-22, FR-26, UJ-1 | F10 |
| §2 Arbeidsflyt steg 1–2 | Eksport, opplasting, validering, lagring, automatisk prognose | FR-1–FR-7, UJ-1, UJ-2, UJ-4 | F4, F5, F11, F13, F14 |
| §2 Arbeidsflyt steg 3 | Produktliste med de svakeste øverst, flagg, graf og scenarioer | FR-5, FR-11, FR-12, FR-17, FR-19–FR-21, FR-26, UJ-1 | F5, F6, F10 |
| §2 Arbeidsflyt steg 4 | Sjekk backtest mot baseline | FR-13–FR-17, FR-21, FR-22, UJ-3 | F7, F8 |
| §2 Ikke-brukere, målvirksomhet | Én primærbruker, enbrukerapp | §2.2, NFR-8 | — |
| §2 Hva skiller PROGNOS | Prototype som viser et prinsipp | §1 (tesen), §6 | — |
| §3 Produktmål 1 | CSV → prognose med P10/P50/P90 og scenarioer | FR-1–FR-12 | F1–F6, F11, F13, F14 |
| §3 Produktmål 2 | Treffsikkerhet med backtest (WAPE) | FR-13–FR-17, SM-1, SM-2 | F7, F8 |
| §3 Produktmål 3 | Oversiktlig dashbord | FR-18–FR-22, FR-26 | F10 |
| §3 Læringsmål og forretningsmål | KI i produktet og i utviklingen. Forretningsmål hører til visjonen | §8.3 | — |
| §4 Omfangstabell | v1, trinn 2, senere trinn, visjon | §7 | — |
| §4.1 del 1 CSV-import | Kolonner, skilletegn, validering, utfylling, historikknivå, lagring, automatisk kjøring | FR-1–FR-7, UJ-4 | F4, F5, F11, F13, F14 |
| §4.1 del 2 Én modell mot baseline | ETS, sesongnaiv, 6 mnd, 80 % intervall, nullgrense | FR-8–FR-10 | F1, F2, F3, F5 |
| §4.1 del 3 Tre scenarioer | Scenarioer, scenariototal med merknad, scenarionavn som hovedord | FR-11, FR-12, FR-21 | F6, F10 |
| §4.1 del 4 Backtest | 6 opprinnelser, 1 måned frem, WAPE, dekning, 30-månedersgrense, *ETS taper* | FR-13–FR-17 | F7, F8 |
| §4.1 del 5 Dashbord | Én side, produktliste med søk, graf, tabeller, WAPE-oversikt | FR-18–FR-22, FR-26 | F10 |
| §4.1 Syntetiske testdata | Fast seed, trend/sesong/støy, alle historikknivåer, innlasting ved oppstart | FR-23–FR-25, NFR-9 | F7, F8, F9 |
| §4.2 Trinn 2, §4.3 Senere trinn, §4.4 Visjon | — | §7.2 (utenfor v1) | — |
| §4.5 Utenfor omfang uansett | MRP, automatiske beslutninger m.m. | §6 | — |
| §5 Prinsipp «null konfigurasjon» | Lokal kjøring uten Docker, hemmeligheter eller nøkler. SQLite | NFR-1, NFR-2, FR-6, [addendum.md](addendum.md) | F11, F12 |
| §5 Prinsipp «baseline først» | ETS måles alltid mot sesongnaiv | §4.4, FR-14, FR-17, FR-21, FR-22 | F7 |
| §5 Prinsipp «kjente data» | Syntetiske data med kjent fasit | FR-23, FR-24, SM-C1 | F7, F8, F9 |
| §5 Prinsipp «etterprøvbart» | Scenarioer og regler kan regnes etter | NFR-5, FR-12, FR-21 | F6 |
| §5 Prinsipp «norsk» | Grensesnitt og dokumentasjon på norsk | NFR-4 | — |
| §5 Prinsipp «KI i utviklingen» | KI til koding, testing og gjennomgang, dokumentert | §8.3 | — |
| §6 Suksesskriterier | F1–F14, prosjektsuksess, B1–B3 og L1 | §8, NFR-6, §7.2 (B1–B3, L1) | F1–F14 |

### 9.2 Faglærers tilbakemelding → PRD

| Punkt i tilbakemeldingen | Hvor i PRD-en |
|---|---|
| Velg én kjerneflyt for v1 | §4, §7.1, UJ-1 |
| Én primærbruker: etterspørselsplanleggeren | §2 (Kari) |
| Funksjonelle, testbare kriterier | §8.1 (F1–F14), NFR-6 |
| «Modellen slår baseline» som viktigste kvalitetskriterium | SM-1 |
| Lag fasitserier | FR-24 (fasit), NFR-5 (håndregnet testdatasett) |
| SQLite i stedet for PostgreSQL | FR-6, NFR-2, addendum |
| Kjørbar for sensor uten nøkler eller betalte kontoer | NFR-1, F12 |
| Mock-forklaringer og LLM | §7.2 (trinn 2, utenfor v1) |
| `.env.example` og egen mappe for syntetiske testdata | NFR-9 |
| Skisse av prognosevisningen og scenariosammenligningen | §4.5, FR-20, FR-21 |
| Ærlig om hva som skiller PROGNOS | §1, §6 |

## 10. Åpne spørsmål

1. ~~**Bekreftelse i testskriptet (spike).**~~ **Besvart 2026-11-14:** Spiken bekrefter oppsettet, og beslutningsloggen trenger ikke endres. F7 holdt i 18 av 20 seeds og F8 i 18 av 20. Med 3 produkter er F8 støyfølsomt, så F7 og F8 sjekkes på nytt på det syntetiske datasettet. Se [docs/research/teknisk.md](../../../../docs/research/teknisk.md). Opprinnelig spørsmål: Beslutningsloggen sier at backtest-oppsettet bekreftes i testskriptet. Hvis spiken viser at oppsettet ikke holder, endres det i beslutningsloggen med ny dato, og PRD-en oppdateres. Det syntetiske datasettet kan bare justeres innenfor FR-24 og SM-C1, ikke for å få F7 eller F8 grønn. Eier: gruppen, før implementering. Blokkerer ikke PRD-en.
2. **Hvordan ser ERP-eksporter ut i praksis?** Fra research-planen: desimalkomma, store bokstaver i kolonnenavn og andre datoformater kan gi avvisninger som overrasker brukeren. v1 holder seg til reglene i FR-1 til FR-3. Funn fra researchen kan gi bedre feilmeldinger, men ikke nye formater. Eier: gruppen. Blokkerer ikke.
3. **Stemmer personaen og arbeidsflyten?** Fra research-planen: stillingsannonser for etterspørselsplanleggere og en mulig samtale med en planlegger. Samtalen bør også teste om planleggeren forstår «80 % prediksjonsintervall» og merknaden om scenariototalene. Funnene kan endre brukerreisene, ordvalget og tallene i NFR-7 og FR-24, men ikke beslutningsloggen. Eier: gruppen. Blokkerer ikke.

## 11. Tolkninger

### 11.1 Bekreftet av gruppen

Disse punktene stod ikke direkte i kildene. De ble foreslått i PRD-arbeidet og bekreftet av gruppen 2026-11-14. De er krav på lik linje med resten. De som også er ført inn i beslutningsloggen, er merket med navnet på raden.

- **FR-1** — Kolonner utover de tre påkrevde ignoreres og gir ikke feil.
- **FR-3** — Valideringsrapporten viser alle feilene i fila, ikke bare den første.
- **FR-6** — En ny opplasting av samme fil gir et nytt datasett. Ingenting overskrives eller slettes.
- **FR-8** — F3 og F5 leses sammen: produkter med historikknivå *ingen* finnes i output med flagget *kort historikk*, men uten prognoseserie.
- **FR-14, FR-22** — Total WAPE for ETS og baseline regnes over de samme produktene, altså bare produkter med backtest for begge modellene. Beslutningslogg: *Total WAPE*.
- **FR-14, FR-19** — Når Σ faktisk = 0, vises WAPE som «–». Produktet inngår ikke i totalen og står rett etter de flaggede produktene. Beslutningslogg: *WAPE når faktisk salg er 0*.
- **FR-15, FR-19** — Intervalldekningen regnes per modell, per produkt og totalt over de samme produktene som total WAPE, og F8 gjelder ETS. Flaggede produkter sorteres internt etter WAPE med høyest først, og like verdier sorteres etter `produkt_id`. Beslutningslogg: *Intervalldekning og sortering*.
- **FR-16** — Produkter med 12–17 måneders historikk får ingen backtest, og produkter med 18–29 måneder får baseline-backtest. Beslutningslogg: *Backtest for 12–17 mnd*.
- **FR-18** — Nyeste datasett er valgt som standard i datasettvelgeren.
- **FR-19** — Flaggede produkter står øverst. Deretter kommer uflaggede produkter med WAPE «–», og så resten sortert etter WAPE med høyest først. Beslutningslogg: *Sortering av produktlisten*.
- **FR-19** — WAPE i produktlisten er WAPE for ETS når ETS-backtest finnes, ellers WAPE for baseline.
- **FR-21** — Når produktet bare har baseline-backtest, vises det tydelig at ETS ikke er backtestet.
- **NFR-7** — Svartidsgrensen er 60 sekunder for 200 produkter × 36 måneder.
- **NFR-6, NFR-9, FR-24 (fasit)** — Disse ble lagt til etter gjennomgangen og godkjent av gruppen.

### 11.2 Presiseringer fra gjennomgangen

Gruppen godkjente at funn med middels og lav alvorlighetsgrad skulle rettes. Disse presiseringene ble valgt i rettingen og godkjent av gruppen 2026-11-14:

- **Horisont og utfylling (§3, FR-4, FR-8)** — Siste måned i datasettet er felles for alle produktene. Et produkt som mangler de siste månedene, fylles med 0 til og med den og får en advarsel. Horisonten og backtest-månedene er dermed like for alle produktene.
- **Historikklengde (§3, FR-5)** — Begge endepunktene telles med (2024-11 til 2026-10 = 24 måneder).
- **Historikknivå** — Nivået for 12–23 måneder heter *sesongnaiv* i stedet for *baseline*, slik at det ikke kolliderer med modellnavnet.
- **FR-7** — Hele kjøringen skjer i én forespørsel. Hvis prognose- eller backtest-kjøringen feiler, lagres ingenting.
- **FR-10** — Grafen og scenariotabellen viser ETS-prognosen for historikknivå *ets*. Den sesongnaive prognosen vises ikke for disse produktene.
- **FR-12, FR-20, FR-21** — Tekstene i grensesnittet er fastsatt ordrett, slik at de kan testes.
- **FR-24** — Tallene for innholdet i den syntetiske CSV-fila, og grensen på 5 % mot fasiten.
- **«ETS slår baseline»** — Betyr strengt lavere WAPE. Like verdier gir verken seier eller flagget *ETS taper*.

### 11.3 Fra arkitekturen

Godkjent av gruppen 2026-11-17 i arkitekturøkten:

- **FR-9, FR-12, FR-14, FR-15, NFR-5** — P10, P50 og P90 rundes halvt opp til heltall rett etter nullgrensen. Scenariototaler, WAPE og intervalldekning regnes bare fra de avrundede verdiene, slik at tallene som vises, gir nøyaktig samme resultat når de regnes etter. Beslutningslogg: *Avrunding til heltall*.
- **FR-24** — 5 %-testen mot fasiten måles på de avrundede P50-verdiene. Det støyfrie produktet har derfor et nivå på minst 20, slik at avrundingen alene ikke kan gi mer enn 2,5 % avvik.
