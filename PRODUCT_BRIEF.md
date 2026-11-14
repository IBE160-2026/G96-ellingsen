# Product Brief — PROGNOS

**AI-støttet prognoseverktøy for etterspørselsplanleggeren**

Gruppe G96 · IBE160 Programmering med KI · Høgskolen i Molde · Høst 2026

---

## Executive brief

PROGNOS er en webapplikasjon for etterspørselsplanleggere i små og mellomstore produksjonsbedrifter. Planleggeren laster opp historiske salgstall som CSV, og PROGNOS lager en månedlig prognose per produkt med usikkerhetsintervall og tre scenarioer: forventet, optimistisk og pessimistisk. En backtest viser om prognosen treffer bedre enn en enkel referanse. Et dashbord viser historikk, prognose og intervaller for hvert produkt.

Problemet er at MRP-systemet bare er så godt som prognosen det får inn, og i mange bedrifter lages den prognosen i regneark ut fra fjorårets tall og magefølelse. Planleggeren får ett tall per produkt og vet ikke hvor sikkert det er, eller om metoden faktisk er bedre enn å gjenta fjoråret.

Omfanget er delt i **v1** (kjerneflyten som leveres i emnet), **senere trinn** og en **langsiktig visjon**. Avsnitt 4 beskriver hva som hører til hvor.

---

## 1. Problem

Etterspørselsplanleggeren lager prognosene som MRP-systemet planlegger materialbehov ut fra. I dag har dette arbeidet tre svakheter:

- **Manuelle og statiske prognoser.** Prognoser lages ofte som glidende gjennomsnitt eller «fjoråret + X %» i regneark, og oppdateres sjelden.
- **Ingen håndtering av usikkerhet.** Planleggeren leverer ett tall per produkt og periode, uten noe mål på hvor sikkert det er eller hva som skjer hvis salget blir høyere eller lavere enn ventet.
- **Ingen etterprøving.** Det blir sjelden målt om prognosemetoden faktisk treffer bedre enn en enkel referanse.

**Konsekvenser:** Feil prognoser forplanter seg gjennom materialplanen og gir for mye lager av noen varer, utsolgte produkter av andre, og hasteordrer.

---

## 2. Målgruppe

**Primærbruker: etterspørselsplanleggeren**

Kari er etterspørselsplanlegger i en produksjonsbedrift med ca. 100 ansatte og rundt 200 aktive produkter. Hver måned eksporterer hun salgshistorikk fra ERP-systemet og lager prognoser for de neste månedene i Excel.

| Behov | Hvordan v1 dekker det |
|---|---|
| Få en prognose per produkt uten å bygge den manuelt i regneark | Last opp CSV → prognose for alle produkter |
| Vite hvor sikker prognosen er | P10/P50/P90 og tre scenarioer per produkt |
| Kunne stole på metoden | Backtest med WAPE mot sesongnaiv baseline |
| Få oversikt raskt | Dashbord med historikk, prognose og intervall per produkt |

**Hennes arbeidsflyt i v1:**

1. Eksporterer månedlig salg per produkt fra ERP til CSV.
2. Laster opp filen i PROGNOS og ser valideringsresultatet. Når filen er godkjent, lages prognosen automatisk.
3. Ser produktlisten, der de svakeste prognosene ligger øverst, og velger et produkt og ser historikk, prognose for 6 måneder, intervall og de tre scenarioene.
4. Sjekker backtesten: treffer modellen bedre enn sesongnaiv baseline for dette produktet?

Andre roller, som materialplanlegger, innkjøp, salg, marked og ledelse, kan ha nytte av prognosen, men PROGNOS er ikke laget for dem i v1.

**Målvirksomhet:** Små og mellomstore produksjonsbedrifter som har et MRP/ERP-system, men ikke et eget verktøy for etterspørselsplanlegging.

### Hva skiller PROGNOS fra andre verktøy

Det finnes allerede kommersielle verktøy for etterspørselsplanlegging. Mange ERP-systemer har en innebygd prognosemodul, og det finnes egne planleggingsverktøy med statistiske prognoser, sikkerhetslager og scenarioer. Slike verktøy koster mye og er krevende å innføre, så mange mindre bedrifter fortsetter å bruke regneark. PROGNOS skal ikke konkurrere med disse verktøyene. Det er en studentprototype som viser et prinsipp for bedrifter som i dag bruker regneark: prognosen skal vise hvor usikker den er, og den skal etterprøves mot en enkel referanse.

---

## 3. Mål

**Produktmål (v1)**

1. Gjøre om en CSV med månedlig salgshistorikk til en prognose per produkt med P10/P50/P90 og tre scenarioer.
2. Vise treffsikkerheten med backtest (WAPE) mot sesongnaiv baseline.
3. Vise historikk, prognose og intervaller oversiktlig i et dashbord.

**Læringsmål (prosjekt)**

- Vise hvordan KI kan brukes både *i* produktet (prognosemodell) og *i* utviklingsprosessen (koding, testing, kvalitetssikring).

Forretningsmål som lavere lagerbinding og høyere leveringsgrad hører til visjonen (avsnitt 4.4) og måles ikke i emnet.

---

## 4. Omfang

| | **v1** (leveres i emnet) | **Trinn 2** (hvis tiden tillater) | **Senere trinn** | **Visjon** |
|---|---|---|---|---|
| **Data** | CSV med salgshistorikk | + lager og ledetid per produkt | Kampanjer, kundebestillinger | Alle etterspørselssignaler samlet |
| **Modell** | ETS mot sesongnaiv baseline | — | LightGBM, Prophet, modellvalg | Automatisk beste modell per produkt |
| **Usikkerhet** | P10/P50/P90, tre scenarioer | — | «Hva hvis»-scenarioer | Scenarioer for S&OP |
| **Kvalitet** | Backtest med WAPE | — | — | Løpende måling og FVA |
| **Beslutning** | — | Produksjon vs. lager | Optimering, outsourcing | Full beslutningsstøtte |
| **Forklaring** | — | LLM-forklaring med mock-modus (valgfritt) | SHAP | Forklarbare anbefalinger |
| **Flyt og integrasjon** | Dashbord | — | Overstyring, godkjenning, MRP-eksport | Integrert modul i MRP |

### 4.1 v1 — kjerneflyt

v1 består av fem deler. Alt som ikke står her, er utenfor v1.

**1. CSV-import med enkel validering**
- Opplasting av én CSV-fil med kolonnene `produkt_id`, `maaned` (ÅÅÅÅ-MM) og `antall` fra dashbordet til backend.
- Godkjente datasett lagres i en lokal SQLite-database, slik at planleggeren kan åpne dem igjen senere.
- Komma eller semikolon som skilletegn gjenkjennes automatisk (norsk Excel bruker ofte semikolon).
- `antall` må være et heltall ≥ 0.
- Tydelige feilmeldinger ved manglende kolonner, ugyldige datoer, negative verdier eller verdier som ikke er heltall, og duplikater (samme produkt og måned).
- Manglende måneder fylles med 0 og gir en advarsel i valideringsrapporten.
- Hvor lang historikk et produkt har, avgjør hva det får:

  | Historikk | Prognose |
  |---|---|
  | Under 12 måneder | Ingen prognose. Produktet flagges. |
  | 12–23 måneder | Bare sesongnaiv. Produktet flagges. |
  | 24 måneder eller mer | ETS og sesongnaiv baseline. |

- Prognosen kjøres automatisk når filen er godkjent.

**2. Én modell mot baseline**
- Månedlig prognose per produkt, 6 måneder frem (fast horisont).
- Modell: **ETS** (`AutoETS` fra `statsforecast`), som gir både punktestimat og prediksjonsintervaller.
- Baseline: **sesongnaiv** (samme måned i fjor).
- Output per produkt og måned: **P10, P50 og P90**. P10 og P90 er grensene i et 80 % prediksjonsintervall (`level=[80]` i `statsforecast`).
- Salg kan ikke være negativt, så alle verdier settes til minst 0.

**3. Tre scenarioer**

| Scenario | Definisjon |
|---|---|
| **Pessimistisk** | P10 |
| **Forventet** | P50 |
| **Optimistisk** | P90 |

Totalt volum for de 6 månedene vises for hvert scenario, regnet som summen av de månedlige verdiene. Grensesnittet har en merknad om at spennet mellom pessimistisk og optimistisk total da blir bredere enn det reelle. Det er enkelt å regne etter, og simulering ville vært for komplisert for v1.

I grensesnittet er Pessimistisk, Forventet og Optimistisk hovedordene, og P10, P50 og P90 står som forklaring. Planleggere forstår scenarioer bedre enn kvantiler.

**4. Backtest**
- Rullerende backtest med 6 opprinnelser over de siste 6 månedene av historikken. Hver opprinnelse prognoserer 1 måned frem, og opprinnelsen flyttes én måned om gangen.
- **WAPE** for ETS og sesongnaiv baseline, per produkt og totalt.
- Intervalldekning: andel faktiske verdier innenfor P10–P90.
- ETS trenger 24 måneders trening ved hver opprinnelse. Produkter med under 30 måneders historikk får derfor bare baseline-backtest, selv om de får ETS-prognose.
- Hvis ETS taper mot baseline for et produkt, vises ETS-prognosen likevel. Produktet flagges, og begge WAPE-tallene vises.

**5. Dashbord**
- Next.js-app med opplasting, datasettvelger og produktvelger.
- Dashbordet starter med produktlisten sortert etter WAPE, med de svakeste prognosene øverst. Produkter med kort historikk og produkter der ETS taper mot baseline er flagget.
- Graf per produkt (Recharts): historikk, prognose (P50) og intervall (P10–P90) som skyggelagt bånd.
- Tabell med scenarioer og backtest-resultat for valgt produkt, og en WAPE-oversikt for alle produkter.

Skisse av dashbordet (én side):

```
┌──────────────────────────────────────────────────────────────────────┐
│ PROGNOS     Datasett: [salg_2026-10.csv ▾]          [ Last opp CSV ] │
│             ✓ 20 produkter godkjent · 2 flagget (kort historikk)     │
├────────────────────┬─────────────────────────────────────────────────┤
│ PRODUKTER          │ GRAF: P-104 Ventilhus                           │
│ (svakeste øverst)  │                                                 │
│                    │ antall                                          │
│   P-109 ⚠ ETS taper│   │       historikk          prognose           │
│   P-117 ⚠ kort     │   │  /\    /\    /\       ░░▒▒▒▒▒░░ ← P10–P90   │
│ ● P-104  WAPE 14 % │   │ /  \__/  \__/  \____▒▒───────▒▒ ← P50       │
│   P-101  WAPE 12 % │   │                       ░░▒▒▒▒▒░░             │
│   P-102  WAPE  9 % │   └───────────────────────┼──────────── måned   │
│   ...              │                         i dag                   │
│                    ├────────────────────────┬────────────────────────┤
│                    │ SCENARIOER (6 mnd)     │ BACKTEST (siste 6 mnd) │
│                    │ Pessimistisk (P10)  820│ WAPE ETS          14 % │
│                    │ Forventet    (P50)  960│ WAPE sesongnaiv   21 % │
│                    │ Optimistisk  (P90) 1110│ ETS slår baseline   ✓  │
│                    │ * spennet er for bredt │ Dekning P10–P90   80 % │
├────────────────────┴────────────────────────┴────────────────────────┤
│ WAPE-OVERSIKT, ALLE PRODUKTER:  ETS 13 % · sesongnaiv 19 % · 17/20 ✓ │
└──────────────────────────────────────────────────────────────────────┘
```

- **Øverst:** datasettvelger og knapp for opplasting. Valideringsresultatet vises rett under, med feilmeldinger hvis filen blir avvist.
- **Venstre:** produktvelger sortert etter WAPE, med de svakeste øverst. Produkter med kort historikk og produkter der ETS taper er flagget.
- **Midten:** graf for valgt produkt med historikk, P50 og P10–P90 som skyggelagt bånd.
- **Under grafen:** scenariotabell til venstre, med merknaden om spennet, og backtest til høyre.
- **Nederst:** WAPE-oversikt for alle produkter, ETS mot baseline.

Tallene i skissen er bare eksempler.

**Syntetiske testdata (støtte for v1)**
- Et skript genererer et datasett med **kjent trend, sesong og støy** (fast seed, så dataene blir like hver gang).
- Ca. 20 produkter med 36 måneders historikk. De fleste har trend i tillegg til sesong og støy, slik at ETS har noe å slå sesongnaiv på (F7). Noen har andre mønstre, som en flat serie med mye støy.
- Ett produkt med under 12 måneders historikk og ett med 12–23 måneder, slik at alle tre historikknivåene blir testet.
- Datasettet brukes i automatiske tester og i demo, og lastes inn i databasen ved oppstart hvis den er tom. Siden sesong og trend er kjent, kan vi sjekke at modellen fanger dem opp.

### 4.2 Trinn 2 — beslutningspunkt

Trinn 2 bygges først når v1 er ferdig og testet.

**Produksjon vs. lager.** Planleggeren legger inn `lager` (nåværende beholdning) og `ledetid_mnd` (produksjonsledetid i måneder) per produkt. PROGNOS bruker en enkel og åpen regel:

- **Behov i ledetiden** = summen av P50 for de første `ledetid_mnd` prognosemånedene.
- **Sikkerhetslager** = summen av (P90 − P50) for de samme månedene.
- Hvis `lager` ≥ behov + sikkerhetslager → **Lever fra lager**.
- Ellers → **Produser**, med foreslått mengde = behov + sikkerhetslager − `lager`.

Anbefalingen vises sammen med tallene den bygger på, slik at planleggeren kan regne den etter selv.

**Forklaring i klartekst (valgfritt).** En kort tekst per produkt som forklarer prognosen og anbefalingen, laget fra strukturerte modellresultater. **Mock-modus er standard:** teksten lages fra en fast mal, uten nettverk eller API-nøkkel. Med API-nøkkel satt kan en språkmodell (Claude via `pydantic-ai`) brukes i stedet.

Begge funksjonene i trinn 2 slås av og på med feature flags (`FEATURE_DECISION`, `FEATURE_AI`), slik at v1 kan leveres uten dem.

### 4.3 Senere trinn

Utenfor emnet, i omtrent prioritert rekkefølge:

1. Overstyring av prognosen med begrunnelse, og godkjenningsflyt.
2. Flere modeller (LightGBM, Prophet) med automatisk modellvalg per produkt basert på backtest.
3. Forklarbarhet med SHAP, brukt som grunnlag for LLM-forklaringer.
4. Kampanjer og kundebestillinger som ekstra signaler.
5. Egendefinerte «hva hvis»-scenarioer.
6. Optimering av produksjon og lager.
7. Outsourcing-analyse: intern kapasitet vs. outsourcing.
8. Eksport til MRP via fil eller API.

### 4.4 Visjon

På lang sikt kan PROGNOS bli en komplett modul for etterspørselsstyring som er koblet inn i MRP-systemet. Den samler salgshistorikk, kampanjer, markedsdata, kundebestillinger og selgernes prognoser, velger beste modell per produkt og gir forklarbare anbefalinger for produksjon, lager og outsourcing. Prognosene godkjennes og sendes rett til MRP. Målet for bedriften er lavere lagerbinding, høyere leveringsgrad, færre utsolgt-situasjoner og færre hasteordrer. Dette kan bare måles i en ekte bedrift over flere planleggingssykluser.

### 4.5 Utenfor omfang uansett

- **Full MRP-funksjonalitet** (BOM, netto behov, innkjøpsordrer) og detaljert produksjonsplanlegging. PROGNOS leverer etterspørselen som MRP planlegger ut fra.
- **Automatiske beslutninger.** Systemet anbefaler, og et menneske bestemmer.
- **Prisoptimalisering, leverandørstyring, budsjettering og regnskap.**
- **Innsamling av ekstern markedsdata.** Data må leveres av brukeren.

---

## 5. Teknisk tilnærming (v1)

PROGNOS v1 er en enbrukerapp som kjører lokalt: backend i FastAPI, frontend i Next.js og en lokal **SQLite**-database. For backend og frontend følger vi stacken i [technology.md](.docs/planning-artifacts/architecture/technology.md). Den bruker PostgreSQL, men vi bruker SQLite etter anbefaling fra faglærer i tilbakemeldingen på briefen: en enbrukerapp trenger ingen egen databaseserver, og da trenger verken gruppen eller sensor Docker for å kjøre appen. Innlogging, betaling, e-post, Redis, proxy og deploy er ikke med i v1. Komponenter, API og datamodell beskrives i arkitekturdokumentet (steg 4). Utkastet ligger i [arkitektur-utkast.md](.docs/planning-artifacts/architecture/arkitektur-utkast.md).

### Arkitektur

```
Nettleser
   │  relative /api-kall (single-origin)
   ▼
frontend (Next.js)  ──/api──►  backend (FastAPI)  ──►  SQLite (lokal fil)
 opplasting, dashbord,          validering, ETS +        datasett, salgsdata,
 grafer og tabeller             sesongnaiv, scenarioer,  prognoser og
                                backtest (WAPE)          backtest-resultater
```

Backend og frontend startes med én kommando hver, uten Docker. Databasefila opprettes automatisk første gang backend starter. Frontend videresender `/api/*` til backend, så nettleseren bare snakker med én adresse og det ikke trengs CORS.

### Prinsipper

- **Null konfigurasjon:** Appen starter lokalt uten Docker, hemmeligheter eller API-nøkler. Integrasjoner som mangler nøkkel, som språkmodellen i trinn 2, faller tilbake til deterministiske mock-svar.
- **Baseline først:** ETS måles alltid mot sesongnaiv. Hvis ETS ikke slår baseline for et produkt, vises det tydelig.
- **Kjente data:** Utvikling og testing skjer på syntetiske data med kjent fasit.
- **Etterprøvbart:** Scenarioer og beslutningsregler er enkle nok til at brukeren kan regne dem etter.
- **Norsk:** Grensesnitt, PRD og dokumentasjon skrives på norsk, fordi brukeren og målgruppen er norsk.
- **KI i utviklingen:** KI-assistenter brukes til koding, testgenerering og kodegjennomgang, og bruken dokumenteres.

---

## 6. Hvordan vi måler suksess

### v1 — funksjonelle kriterier (testtilfeller)

| # | Kriterium |
|---|---|
| F1 | En opplastet CSV med 24 måneders salg for ett produkt gir en prognose for 6 måneder med P10/P50/P90. |
| F2 | For hver prognosemåned gjelder P10 ≤ P50 ≤ P90, og ingen verdi er negativ. |
| F3 | En CSV med flere produkter gir én prognoseserie per produkt, og alle `produkt_id` fra input finnes i output. |
| F4 | En CSV som mangler en påkrevd kolonne, har ugyldig dato, negativt antall, antall som ikke er et heltall, eller duplikater (samme produkt og måned), blir avvist med en feilmelding som sier hva som er feil. |
| F5 | Et produkt med 12–23 måneders historikk blir flagget og får bare sesongnaiv prognose. Et produkt med under 12 måneders historikk blir flagget og får ingen prognose. |
| F6 | Hvert produkt får tre scenarioer der pessimistisk = P10, forventet = P50 og optimistisk = P90, og pessimistisk ≤ forventet ≤ optimistisk. |
| F7 | Backtesten viser lavere total WAPE for ETS enn for sesongnaiv baseline på det syntetiske datasettet. |
| F8 | Intervalldekningen for P10–P90 i backtesten på det syntetiske datasettet ligger mellom 65 % og 95 %. |
| F9 | Generatoren for syntetiske data gir identisk datasett ved samme seed. |
| F10 | Dashbordet viser historikk, prognose, intervall og scenarioer for valgt produkt uten feil (testet med Playwright). |
| F11 | Et opplastet datasett med prognose og backtest lagres i SQLite-databasen og kan hentes uendret via API etter at backend er startet på nytt. |
| F12 | Backend og frontend starter med kommandoene i README uten Docker, hemmeligheter eller API-nøkler. Databasefila opprettes automatisk, og `GET /api/health` svarer OK. |
| F13 | En CSV med semikolon som skilletegn gir samme resultat som samme fil med komma. |
| F14 | En manglende måned i en produktserie fylles med 0 og gir en advarsel i valideringsrapporten. |

### Trinn 2 — funksjonelle kriterier

| # | Kriterium |
|---|---|
| B1 | Med kjent prognose, lager og ledetid beregnes sikkerhetslager som summen av (P90 − P50) over ledetiden. |
| B2 | Når lager ≥ behov + sikkerhetslager, blir anbefalingen «Lever fra lager». |
| B3 | Når lager < behov + sikkerhetslager, blir anbefalingen «Produser» med mengde = behov + sikkerhetslager − lager. |
| L1 | *(Valgfritt)* I mock-modus lages en forklaring uten nettverk eller API-nøkkel, og teksten inneholder produktets forventede volum og anbefaling. |

### Prosjektsuksess (IBE160)

- Fungerende prototype som dekker hele v1, med alle kriteriene F1–F14 dekket av automatiske tester som kjører grønt.
- Trinn 2 med produksjon vs. lager (B1–B3) er levert hvis tiden tillater det.
- Dokumentert bruk av KI i utvikling, testing og kvalitetssikring.
