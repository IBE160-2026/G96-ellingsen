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
2. Laster opp filen i PROGNOS og ser valideringsresultatet.
3. Velger et produkt i dashbordet og ser historikk, prognose for 6 måneder, intervall og de tre scenarioene.
4. Sjekker backtesten: treffer modellen bedre enn sesongnaiv baseline for dette produktet?

Andre roller, som materialplanlegger, innkjøp, salg, marked og ledelse, kan ha nytte av prognosen, men PROGNOS er ikke laget for dem i v1.

**Målvirksomhet:** Små og mellomstore produksjonsbedrifter som har et MRP/ERP-system, men ikke et eget verktøy for etterspørselsplanlegging.

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
- Godkjente datasett lagres i PostgreSQL, slik at planleggeren kan åpne dem igjen senere.
- Tydelige feilmeldinger ved manglende kolonner, ugyldige datoer og negative eller ikke-numeriske verdier.
- Produkter med under 24 måneders historikk blir flagget og får bare baseline-prognose.

**2. Én modell mot baseline**
- Månedlig prognose per produkt, 6 måneder frem (fast horisont).
- Modell: **ETS** (`AutoETS` fra `statsforecast`), som gir både punktestimat og prediksjonsintervaller.
- Baseline: **sesongnaiv** (samme måned i fjor).
- Output per produkt og måned: **P10, P50 og P90**.

**3. Tre scenarioer**

| Scenario | Definisjon |
|---|---|
| **Pessimistisk** | P10 |
| **Forventet** | P50 |
| **Optimistisk** | P90 |

Totalt volum for de 6 månedene vises for hvert scenario.

**4. Backtest**
- Rullerende backtest over de siste 6 månedene av historikken (opprinnelse flyttes én måned om gangen).
- **WAPE** for ETS og sesongnaiv baseline, per produkt og totalt.
- Intervalldekning: andel faktiske verdier innenfor P10–P90.

**5. Dashbord**
- Next.js-app med opplasting, datasettvelger og produktvelger.
- Graf per produkt (Recharts): historikk, prognose (P50) og intervall (P10–P90) som skyggelagt bånd.
- Tabell med scenarioer og backtest-resultat for valgt produkt, og en WAPE-oversikt for alle produkter.

**Syntetiske testdata (støtte for v1)**
- Et skript genererer et datasett med **kjent trend, sesong og støy** (fast seed, så dataene blir like hver gang).
- Ca. 20 produkter med 36 måneders historikk og ulike mønstre: sterk sesong, ren trend, flat serie med mye støy, og ett produkt med kort historikk.
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

Stacken følger gruppens arkitekturbeskrivelse i [technology.md](.docs/planning-artifacts/architecture/technology.md): backend i FastAPI, frontend i Next.js og database i PostgreSQL. Vi tar bare med de delene v1 trenger.

### Arkitektur

```
Nettleser
   │  relative /api-kall (single-origin)
   ▼
frontend (Next.js)  ──/api──►  backend (FastAPI)  ──►  PostgreSQL 16
 opplasting, dashbord,          validering, ETS +        datasett, salgsdata,
 grafer og tabeller             sesongnaiv, scenarioer,  prognoser og
                                backtest (WAPE)          backtest-resultater
```

Lokalt kjøres alle tre tjenestene med Docker Compose. Frontend videresender `/api/*` til backend, så nettleseren bare snakker med én adresse og det ikke trengs CORS.

### Komponenter

| Lag | Teknologi | Kommentar |
|---|---|---|
| **Backend** | Python 3.12, **FastAPI** + Uvicorn, Pydantic 2, `uv` | API for opplasting, prognose og resultater. |
| **Prognose** | `statsforecast` (`AutoETS`, `SeasonalNaive`), `pandas`, `numpy` | Kjøres i backend og gir prediksjonsintervaller direkte. |
| **Database** | **PostgreSQL 16** (Docker), SQLAlchemy 2 (async) + `asyncpg`, Alembic | Lagrer datasett, salgsdata, prognoser og backtest. |
| **Frontend** | **Next.js 16** (App Router), React 19, TypeScript 5, Tailwind CSS v4, shadcn/ui | Dashbordet. |
| **Data i frontend** | TanStack Query v5, `zod` | Henting og validering av API-svar. |
| **Grafer** | Recharts | Historikk, P50 og P10–P90-bånd. |
| **Lokal kjøring** | Docker Compose (`frontend`, `backend`, `db`) | `docker compose up` starter hele appen. |
| **Tester** | `pytest` + `pytest-asyncio` (backend), Vitest (frontend), Playwright (e2e) | Kriteriene i avsnitt 6 skrives som testtilfeller. |

### API (v1)

| Endepunkt | Funksjon |
|---|---|
| `POST /api/datasets` | Laster opp CSV, validerer og lagrer datasettet. Gir valideringsrapport eller feilmeldinger. |
| `POST /api/datasets/{id}/forecast` | Kjører ETS, sesongnaiv, scenarioer og backtest, og lagrer resultatet. |
| `GET /api/datasets/{id}/products` | Lister produkter med WAPE for ETS og baseline. |
| `GET /api/datasets/{id}/products/{produkt_id}` | Historikk, prognose (P10/P50/P90), scenarioer og backtest for ett produkt. |
| `GET /api/health` | Helsesjekk. |

### Datamodell (v1)

| Tabell | Innhold |
|---|---|
| `dataset` | id, filnavn, opplastet tidspunkt, valideringsstatus |
| `sales` | dataset_id, produkt_id, maaned, antall |
| `forecast` | dataset_id, produkt_id, maaned, modell, p10, p50, p90 |
| `backtest_result` | dataset_id, produkt_id, modell, wape, intervalldekning |

Trinn 2 legger til en tabell `inventory` (produkt_id, lager, ledetid_mnd) og endepunkter for anbefaling og forklaring.

### Fra technology.md: med og ikke med i v1

- **Med:** FastAPI, Next.js og PostgreSQL med Alembic-migrasjoner, Docker Compose lokalt, mock-fallback-prinsippet, seeding ved oppstart (`seed_if_empty`) og feature flags for trinn 2.
- **Ikke med:** innlogging og brukerkontoer, betaling (Stripe/Vipps), e-post, Supabase Storage, Redis, Caddy-proxy, capability-tokens, Railway-deploy, backup og overvåking. PROGNOS v1 er en enbrukerapp som kjører lokalt.

### Prinsipper

- **Null konfigurasjon:** Appen starter lokalt uten hemmeligheter eller API-nøkler. Integrasjoner som mangler nøkkel, som språkmodellen i trinn 2, faller tilbake til deterministiske mock-svar.
- **Baseline først:** ETS måles alltid mot sesongnaiv. Hvis ETS ikke slår baseline for et produkt, vises det tydelig.
- **Kjente data:** Utvikling og testing skjer på syntetiske data med kjent fasit.
- **Etterprøvbart:** Scenarioer og beslutningsregler er enkle nok til at brukeren kan regne dem etter.
- **KI i utviklingen:** KI-assistenter brukes til koding, testgenerering og kodegjennomgang, og bruken dokumenteres.

---

## 6. Hvordan vi måler suksess

### v1 — funksjonelle kriterier (testtilfeller)

| # | Kriterium |
|---|---|
| F1 | En opplastet CSV med 24 måneders salg for ett produkt gir en prognose for 6 måneder med P10/P50/P90. |
| F2 | For hver prognosemåned gjelder P10 ≤ P50 ≤ P90, og ingen verdi er negativ. |
| F3 | En CSV med flere produkter gir én prognoseserie per produkt, og alle `produkt_id` fra input finnes i output. |
| F4 | En CSV som mangler en påkrevd kolonne, eller har ugyldig dato eller negativt antall, blir avvist med en feilmelding som sier hva som er feil. |
| F5 | Et produkt med under 24 måneders historikk blir flagget og får baseline-prognose i stedet for ETS. |
| F6 | Hvert produkt får tre scenarioer der pessimistisk = P10, forventet = P50 og optimistisk = P90, og pessimistisk ≤ forventet ≤ optimistisk. |
| F7 | Backtesten viser lavere total WAPE for ETS enn for sesongnaiv baseline på det syntetiske datasettet. |
| F8 | Intervalldekningen for P10–P90 i backtesten på det syntetiske datasettet ligger mellom 65 % og 95 %. |
| F9 | Generatoren for syntetiske data gir identisk datasett ved samme seed. |
| F10 | Dashbordet viser historikk, prognose, intervall og scenarioer for valgt produkt uten feil (testet med Playwright). |
| F11 | Et opplastet datasett med prognose og backtest lagres i PostgreSQL og kan hentes uendret via API etter at backend er startet på nytt. |
| F12 | `docker compose up` starter frontend, backend og database uten at noen hemmeligheter eller API-nøkler er satt, og `GET /api/health` svarer OK. |

### Trinn 2 — funksjonelle kriterier

| # | Kriterium |
|---|---|
| B1 | Med kjent prognose, lager og ledetid beregnes sikkerhetslager som summen av (P90 − P50) over ledetiden. |
| B2 | Når lager ≥ behov + sikkerhetslager, blir anbefalingen «Lever fra lager». |
| B3 | Når lager < behov + sikkerhetslager, blir anbefalingen «Produser» med mengde = behov + sikkerhetslager − lager. |
| L1 | *(Valgfritt)* I mock-modus lages en forklaring uten nettverk eller API-nøkkel, og teksten inneholder produktets forventede volum og anbefaling. |

### Prosjektsuksess (IBE160)

- Fungerende prototype som dekker hele v1, med alle kriteriene F1–F12 dekket av automatiske tester som kjører grønt.
- Trinn 2 med produksjon vs. lager (B1–B3) er levert hvis tiden tillater det.
- Dokumentert bruk av KI i utvikling, testing og kvalitetssikring.
