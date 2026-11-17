> **Erstattet 2026-11-17.** Dette utkastet gjelder ikke lenger. Det er erstattet av [ARCHITECTURE-SPINE.md](../../../_bmad-output/planning-artifacts/architecture/architecture-G96-ellingsen-2026-11-17/ARCHITECTURE-SPINE.md), som også retter de fem punktene der utkastet var utdatert mot beslutningsloggen (*Total WAPE*, *Sortering av produktlisten*, *Backtest for 12–17 mnd*, *WAPE når faktisk salg er 0* og *Intervalldekning og sortering*). Teksten under står uendret for sporbarheten.

# Arkitektur — utkast (input til steg 4)

Flyttet fra avsnitt 5 i [PRODUCT_BRIEF.md](../../../PRODUCT_BRIEF.md) og oppdatert etter beslutningsloggen i [research-plan.md](../../../docs/research/research-plan.md). Dette er grunnlaget for arkitekturdokumentet vi lager i steg 4. Det er ikke et ferdig dokument.

## Komponenter

| Lag | Teknologi | Kommentar |
|---|---|---|
| **Backend** | Python 3.12, **FastAPI** + Uvicorn, Pydantic 2, `uv` | API for opplasting, prognose og resultater. |
| **Prognose** | `statsforecast` (`AutoETS`, `SeasonalNaive`), `pandas`, `numpy` | Kjøres i backend. 80 % prediksjonsintervall (`level=[80]`) gir P10 og P90 direkte. |
| **Database** | **SQLite** (lokal fil), SQLAlchemy 2 (async) + `aiosqlite` | Lagrer datasett, salgsdata, prognoser og backtest. Fila opprettes ved første oppstart. |
| **Frontend** | **Next.js 16** (App Router), React 19, TypeScript 5, Tailwind CSS v4, shadcn/ui | Dashbordet. |
| **Data i frontend** | TanStack Query v5, `zod` | Henting og validering av API-svar. |
| **Grafer** | Recharts | Historikk, P50 og P10–P90-bånd. |
| **Lokal kjøring** | `uv run` (backend) og `npm run dev` (frontend), uten Docker | Kommandoene står i README. |
| **Tester** | `pytest` + `pytest-asyncio` (backend), Vitest (frontend), Playwright (e2e) | Kriteriene i avsnitt 6 i briefen skrives som testtilfeller. |

Åpent spørsmål til steg 4: Alembic-migrasjoner eller `create_all` ved oppstart. Med SQLite og én bruker holder trolig `create_all`.

## Regler for prognose og backtest

**Historikknivå per produkt** (antall måneder fra første til siste måned, etter utfylling):

| Historikk | Prognose | Backtest |
|---|---|---|
| Under 12 mnd | Ingen. Produktet flagges. | Ingen |
| 12–23 mnd | Bare sesongnaiv. Produktet flagges. | Bare baseline |
| 24–29 mnd | ETS og sesongnaiv | Bare baseline (for lite til 24 mnd trening + 6 opprinnelser) |
| 30 mnd eller mer | ETS og sesongnaiv | ETS og baseline |

**Prognose**
- Horisont 6 måneder, `level=[80]`. P10 = nedre grense, P50 = punktprognose, P90 = øvre grense.
- Nullgrense: `p10 = max(0, p10)`, `p50 = max(0, p50)` og `p90 = max(0, p90)` etter modellkjøringen. Dette bevarer P10 ≤ P50 ≤ P90 (F2).
- Scenarioer for 6 mnd: summen av de månedlige P10/P50/P90. API-et returnerer en merknad om at spennet er bredere enn det reelle.

**Backtest**
- `cross_validation` i `statsforecast` med `n_windows=6`, `h=1` og `step_size=1`.
- WAPE = Σ|faktisk − prognose| / Σ faktisk, per produkt og totalt (summert over alle produkter og vinduer).
- Intervalldekning = andel faktiske verdier innenfor P10–P90 (etter nullgrensen).
- Hvis ETS har høyere WAPE enn baseline, vises ETS likevel, men produktet får flagget `ets_taper`.
- Oppsettet bekreftes i testskriptet (spike) før implementeringen.

## CSV-validering

| Regel | Ved brudd |
|---|---|
| Skilletegn komma eller semikolon, gjenkjent automatisk | Feil hvis ingen av dem gir de tre kolonnene |
| Kolonnene `produkt_id`, `maaned` og `antall` finnes | Feil, med navnet på kolonnen som mangler |
| `maaned` har formatet ÅÅÅÅ-MM | Feil, med radnummer |
| `antall` er et heltall ≥ 0 | Feil, med radnummer |
| Ingen duplikater (samme `produkt_id` og `maaned`) | Feil, med produkt og måned |
| Manglende måneder mellom første og siste måned | Fylles med 0. Advarsel per produkt |

Én eller flere feil avviser hele filen. Advarsler stopper ikke opplastingen. Valideringsrapporten inneholder feil, advarsler og antall produkter per historikknivå.

## API (v1)

| Endepunkt | Funksjon |
|---|---|
| `POST /api/datasets` | Laster opp CSV og validerer. Når filen er godkjent, lagres datasettet, og prognose, scenarioer og backtest kjøres automatisk. Gir valideringsrapporten (feil eller advarsler). |
| `GET /api/datasets` | Lister lagrede datasett (til datasettvelgeren). |
| `GET /api/datasets/{id}/products` | Lister produkter sortert etter WAPE, de svakeste først, med historikknivå og flagg (`kort_historikk`, `ets_taper`). |
| `GET /api/datasets/{id}/products/{produkt_id}` | Historikk, prognose (P10/P50/P90), scenarioer og backtest for ett produkt. |
| `GET /api/health` | Helsesjekk. |

## Datamodell (v1)

| Tabell | Innhold |
|---|---|
| `dataset` | id, filnavn, opplastet tidspunkt, skilletegn, advarsler |
| `sales` | dataset_id, produkt_id, maaned, antall, utfylt (true hvis fylt med 0) |
| `product_status` | dataset_id, produkt_id, antall_mnd, historikknivaa (`ingen` / `baseline` / `ets`), ets_taper |
| `forecast` | dataset_id, produkt_id, maaned, modell, p10, p50, p90 |
| `backtest_result` | dataset_id, produkt_id, modell, wape, intervalldekning |

Bare godkjente filer lagres, så `dataset` har ingen valideringsstatus.

Trinn 2 legger til en tabell `inventory` (produkt_id, lager, ledetid_mnd) og endepunkter for anbefaling og forklaring.

## Fra technology.md: med og ikke med i v1

- **Med:** FastAPI, Next.js, mock-fallback-prinsippet, seeding ved oppstart (`seed_if_empty`) og feature flags for trinn 2.
- **Avvik:** SQLite i stedet for PostgreSQL, etter anbefaling fra faglærer, og ingen Docker Compose. PROGNOS v1 er en enbrukerapp som kjører lokalt, og trenger verken en egen databaseserver eller containere.
- **Ikke med:** innlogging og brukerkontoer, betaling (Stripe/Vipps), e-post, Supabase Storage, Redis, Caddy-proxy, capability-tokens, Railway-deploy, backup og overvåking.
