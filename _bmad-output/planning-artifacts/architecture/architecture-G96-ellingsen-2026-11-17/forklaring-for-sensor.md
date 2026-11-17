---
title: 'PROGNOS v1: arkitekturen forklart'
created: 2026-11-17
for: faglærer og sensor
companion_of: ARCHITECTURE-SPINE.md
---

# PROGNOS v1: arkitekturen forklart

Gruppe G96 · IBE160 Programmering med KI · Høst 2026

Det bindende arkitekturdokumentet er [ARCHITECTURE-SPINE.md](ARCHITECTURE-SPINE.md). Det er skrevet kort, slik at gruppen og KI-agentene som koder, følger de samme reglene. Dette dokumentet forklarer valgene bak det: hvilke alternativer vi vurderte, og hvorfor vi valgte som vi gjorde. Regel-ID-ene (AD-1 til AD-15) viser til spine-dokumentet.

## 1. Kort om systemet

PROGNOS v1 er en enbrukerapp som kjører lokalt. Brukeren, Kari, laster opp en CSV-fil med salgshistorikk. Backend validerer fila, lager en prognose for 6 måneder per produkt med ETS-modellen og en sesongnaiv referansemodell (baseline), kjører en backtest og lagrer alt i en SQLite-fil. Dashbordet viser resultatet.

| Del | Teknologi |
|---|---|
| Backend | Python 3.12, FastAPI, SQLAlchemy 2.1 (async) med aiosqlite |
| Prognose | statsforecast 2.1.1 (AutoETS og SeasonalNaive). Ingen andre ML-biblioteker. |
| Database | Én SQLite-fil i `backend/data/`. Ingen databaseserver. |
| Frontend | Next.js 16, React 19, Tailwind v4, shadcn/ui, TanStack Query, zod, Recharts |
| Kjøring | `uv run …` og `npm run dev`. Ingen Docker, ingen miljøvariabler og ingen nøkler. |

Rammene for arkitekturen kom fra PRD-en, faglærers tilbakemelding (SQLite og kjøring uten nøkler) og beslutningsloggen. Beslutningsloggen er bindende, og arkitekturen diskuterer den ikke på nytt.

**ID-er i teksten:**
- **FR-n og NFR-n** er krav i [PRD-en](../../prds/prd-G96-ellingsen-2026-11-14/prd.md).
- **F1–F14** er akseptansekriteriene fra briefen, for eksempel:
  - F7: ETS har lavere total WAPE enn baseline.
  - F8: intervalldekningen ligger mellom 65 % og 95 %.
  - F11: dataene er uendret etter omstart.
- **SM-C2** er motvekten «ikke smalne inn intervallene for å se presise ut».
- **H6** er et funn fra PRD-gjennomgangen. Det sa at datamodellen og API-et i utkastet manglet data som PRD-en krever.
- **AD-n** er reglene i spine-dokumentet.
- **Nullgrensen** er regelen om at ingen prognoseverdi kan være under 0 (FR-9).

## 2. Grunnmønsteret: ren kjerne og tynt skall

Vi vurderte tre mønstre for backend:

| Alternativ | Vurdering |
|---|---|
| Vanlig lagdeling (ruter → tjenester → repo) | Kjent, men tjenestene blander lett beregning og databasekall. Det gjør det vanskeligere å teste regnereglene alene. |
| Heksagonal arkitektur (porter og adaptere) | For mye struktur for én bruker og én datakilde. |
| **Functional core, imperative shell** | **Valgt.** |

Valget betyr to ting:

- **Kjernen** består av rene funksjoner. De tar inn CSV-innholdet og returnerer et ferdig resultat. Kjernen gjør validering, utfylling, historikknivå, modellkjøring, avrunding, WAPE, dekning, dommer og sortering. Den vet ingenting om databasen eller HTTP.
- **Skallet** tar imot fila, kjører kjernen og lagrer resultatet i én databasetransaksjon.

Mønsteret gir oss tre ting:

1. **Testbarhet.** NFR-5 krever at WAPE, dekning og scenariototaler kan regnes etter for hånd. Med en ren kjerne kan testene sende håndregnede tall rett inn i funksjonene, uten database (konvensjonen *Tester*).
2. **«Ingenting lagres ved feil» (FR-7).** Alt regnes ut i minnet før noe skrives. Hvis noe feiler, er det ingenting å rydde opp (AD-2).
3. **Én vei inn.** Både opplastingen og innlastingen av det syntetiske datasettet ved oppstart (FR-25) bruker samme funksjon. Demodataene går altså gjennom nøyaktig samme kode som Karis filer (AD-2).

## 3. Hullene fra PRD-gjennomgangen (H6)

PRD-gjennomgangen fant at datamodellen og API-et i arkitekturutkastet ikke kunne levere alt PRD-en krever. Tabellen viser hvordan de fem punktene er løst:

| Hull | Problem | Løsning |
|---|---|---|
| 1. Total WAPE | Total WAPE er Σ avvik / Σ faktisk over alle produktene. Den kan ikke regnes ut fra WAPE per produkt alene. | Summene `sum_avvik` og `sum_faktisk` lagres per produkt og modell, og totalen regnes ut fra dem (AD-3, AD-4). |
| 2. Detaljer per opprinnelse | Backtest-tabellen skal vise faktisk verdi og P10/P50/P90 for hver modell og hver av de 6 opprinnelsene. | Tabellen `backtest_punkt` lagrer én rad per produkt, modell og måned, med avvik og «i spenn» ferdig regnet ut (AD-3). |
| 3. WAPE-oversikt | Det fantes ikke noe endepunkt for oversikten. | `GET /api/datasets/{id}` returnerer et lagret sammendrag med total WAPE, total dekning og «n av m» (AD-4, AD-9). |
| 4. Valideringsrapport ved gjenåpning | Rapporten ble ikke lagret. | Hele rapporten lagres som JSON på datasettet og returneres uendret (AD-8). |
| 5. Navnet på historikknivået | Utkastet brukte `baseline` for nivået 12–23 mnd, og det kolliderer med modellnavnet. | Nivået heter `sesongnaiv` overalt (AD-6). |

**Det viktigste valget her** var *hvor* tallene regnes ut. Vi vurderte to alternativer:

- **Bare rådata lagres**, og totaler og sortering regnes ut hver gang noen leser. Det krever mindre lagring, men da implementeres reglene for total WAPE, «n av m» og sortering minst to ganger, i Python ved opplasting og i SQL eller TypeScript ved lesing. Hvis implementeringene kommer i utakt, viser dashbordet andre tall enn testene sjekker.
- **Alt regnes ut én gang i kjernen og lagres** (valgt). API-et og frontend leser og viser bare. Reglene finnes da ett sted, og F11 («uendret etter omstart») følger automatisk, fordi ingenting regnes ut på nytt.

## 4. Avrunding til heltall

Kari ser bare heltall: «Forventet 960», ikke «959,63». Hvis WAPE regnes ut fra urundede verdier, går ikke regnestykket opp når hun summerer avvikene i detaljtabellen. Da brytes NFR-5.

Vi valgte derfor å runde P10, P50 og P90 til heltall rett etter nullgrensen, og å regne ut alt annet fra de avrundede tallene (AD-5). Avrundingen bevarer P10 ≤ P50 ≤ P90. Regelen er ny, så den er ført inn i beslutningsloggen (*Avrunding til heltall*) og i PRD §11.3, sammen med en presisering av 5 %-testen i FR-24.

## 5. Der arkitekturutkastet var utdatert

Beslutningsloggen fikk fem nye rader etter at arkitekturutkastet var skrevet. Spine-dokumentet følger loggen:

| Rad i beslutningsloggen | Utkastet sa | Arkitekturen nå |
|---|---|---|
| *Total WAPE* | Summert over alle produkter og vinduer | Bare over produkter med backtest for begge modellene og faktisk salg > 0 (AD-4) |
| *Sortering av produktlisten* | WAPE, de svakeste først | Flaggede først, deretter produkter uten WAPE, så resten etter WAPE, med `produkt_id` ved like verdier (AD-7) |
| *Backtest for 12–17 mnd* | 12–23 mnd fikk baseline-backtest | Under 18 mnd: ingen backtest. 18–29 mnd: bare baseline. 30+ mnd: begge (AD-6) |
| *WAPE når faktisk salg er 0* | Ikke behandlet | WAPE er `null` («–»). Produktet inngår ikke i totalen og får aldri *ETS taper* (AD-3, AD-4, AD-7) |
| *Intervalldekning og sortering* | Dekning bare per produkt | Dekning per modell, per produkt og totalt over samme mengde som total WAPE. F8 gjelder ETS (AD-4) |

Utkastet er ikke slettet. Det har fått en merknad øverst om at det er erstattet, slik at historikken kan spores.

## 6. Andre valg

| Spørsmål | Valg | Alternativet vi forkastet |
|---|---|---|
| Databaseskjema | `create_all` ved oppstart, med versjonsvakt. Ved skjemaendring slettes fila, og demodataene lastes inn på nytt (AD-13). | Alembic-migrasjoner. Det er mer oppsett for en enbrukerapp der dataene kan genereres på nytt. |
| Antall endepunkter | Seks, der rapport og sammendrag kommer fra samme endepunkt som datasettet, fordi de vises samtidig (AD-9). | Egne endepunkter for rapport og sammendrag, som gir flere kall som må koordineres. |
| Typer mellom backend og frontend | Pydantic er kontrakten. zod-skjemaene speiles for hånd og sjekkes mot ekte svar i en kontrakttest (AD-9). | Kodegenerering fra OpenAPI, som gir et ekstra verktøy og byggesteg. |
| CPU-tung modellkjøring | Kjøres i en trådpool, så `/api/health` og lesing svarer imens. Én opplasting om gangen (AD-10). | Synkron rute, som ville blandet synkrone og asynkrone databaseøkter. |
| Feltnavn | Norsk snake_case fra CSV til frontend, uten konvertering. | camelCase i frontend, som gir to navn på hvert felt. |
| CSV-lesing | Pythons `csv`-modul med eksplisitte regler for radnummer, mellomrom og heltall (AD-15). | `pandas.read_csv`, som gjetter typer (`"001"` blir `1`) og gir feil radnummer etter blanke linjer. |

## 7. Det vi sjekket i stedet for å anta

Arkitekturen binder seg til konkrete versjoner og innstillinger. Disse ble sjekket mot PyPI, npm, kildekoden og egne eksperimenter 2026-11-17:

- **pandas må være 2.3.x.** statsforecast 2.1.1 krever `pandas<3.0.0`, selv om pandas 3.1 er den nyeste versjonen.
- **Next.js kutter proxyforespørsler etter 30 sekunder.** Det står i kildekoden til next@16.4.6. Opplastingen kan ta opptil 60 s (NFR-7), så `experimental.proxyTimeout` settes til 130 s (AD-11). Ellers ville store opplastinger feilet uten noen forklaring.
- **SeasonalNaive med nøyaktig 12 måneder** gir ikke manglende verdier, men et intervall med null bredde. Det gjelder ingen produkter som inngår i totalene (AD-5).
- **AutoETS takler serier med bare nuller og konstante serier.** En slik serie velter altså ikke hele opplastingen.
- **Serier med ulik lengde** kan kjøres i samme backtest-kall, og datoene blir riktige med månedsfrekvensen `MS` (AD-6).
- **Avhengigheter som må med**, men som var lette å glemme: `sqlalchemy[asyncio]`, `python-multipart` og `react-is`. I tillegg krever Vitest Node 22.12 eller nyere.
- **Addendumet tok feil om numba.** statsforecast 2.1.1 bruker ikke numba. Addendumet er rettet.

## 8. Kvalitetssikring av arkitekturen

Spine-dokumentet ble gjennomgått av fem uavhengige KI-agenter, hver med sitt fokus:

- avstemming mot PRD og addendum
- avstemming mot UX-spesifikasjonen og beslutningsloggen
- en rubrikk for gode arkitekturdokumenter
- verifisering av teknologi og versjoner
- et «angrep» som prøvde å finne to utviklere som følger alle reglene, men likevel bygger noe som ikke passer sammen

Funnene ble rettet før dokumentet ble satt til `final`. Rettelsene omfattet blant annet:

- en serverfrist på 110 s, slik at «Ingenting er lagret» stemmer selv om klienten har gitt opp
- én fast form på alle feilsvar
- regler for CSV-lesing og rekkefølgen på feil
- et oppsett der testene ikke skriver i den ekte databasen

Ett funn som var merket kritisk, at SeasonalNaive gir manglende verdier med 12 måneders data, ble avkreftet med et eksperiment før vi endret noe. Rapportene ligger i [reviews/](reviews/).

## 9. Det som står åpent

- **F8 kan bli for lav.** Den tekniske utprøvingen (spiken) viste at ETS-intervallene kan være smale. Spiken kjøres på nytt mot det ekte syntetiske datasettet når generatoren finnes. Intervallnivået på 80 % endres ikke (SM-C2).
- **Utenfor v1:** CI, sletting av datasett, flere brukere, utrulling (deploy) og alt i trinn 2 (anbefalinger, LLM og feature flags).
