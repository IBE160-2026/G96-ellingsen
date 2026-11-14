# Arkitektur — utkast (input til steg 4)

Flyttet fra avsnitt 5 i [PRODUCT_BRIEF.md](../../../PRODUCT_BRIEF.md) og oppdatert til SQLite. Dette er grunnlaget for arkitekturdokumentet vi lager i steg 4. Det er ikke et ferdig dokument.

## Komponenter

| Lag | Teknologi | Kommentar |
|---|---|---|
| **Backend** | Python 3.12, **FastAPI** + Uvicorn, Pydantic 2, `uv` | API for opplasting, prognose og resultater. |
| **Prognose** | `statsforecast` (`AutoETS`, `SeasonalNaive`), `pandas`, `numpy` | Kjøres i backend og gir prediksjonsintervaller direkte. |
| **Database** | **SQLite** (lokal fil), SQLAlchemy 2 (async) + `aiosqlite` | Lagrer datasett, salgsdata, prognoser og backtest. Fila opprettes ved første oppstart. |
| **Frontend** | **Next.js 16** (App Router), React 19, TypeScript 5, Tailwind CSS v4, shadcn/ui | Dashbordet. |
| **Data i frontend** | TanStack Query v5, `zod` | Henting og validering av API-svar. |
| **Grafer** | Recharts | Historikk, P50 og P10–P90-bånd. |
| **Lokal kjøring** | `uv run` (backend) og `npm run dev` (frontend), uten Docker | Kommandoene står i README. |
| **Tester** | `pytest` + `pytest-asyncio` (backend), Vitest (frontend), Playwright (e2e) | Kriteriene i avsnitt 6 i briefen skrives som testtilfeller. |

Åpent spørsmål til steg 4: Alembic-migrasjoner eller `create_all` ved oppstart. Med SQLite og én bruker holder trolig `create_all`.

## API (v1)

| Endepunkt | Funksjon |
|---|---|
| `POST /api/datasets` | Laster opp CSV, validerer og lagrer datasettet. Gir valideringsrapport eller feilmeldinger. |
| `POST /api/datasets/{id}/forecast` | Kjører ETS, sesongnaiv, scenarioer og backtest, og lagrer resultatet. |
| `GET /api/datasets/{id}/products` | Lister produkter med WAPE for ETS og baseline. |
| `GET /api/datasets/{id}/products/{produkt_id}` | Historikk, prognose (P10/P50/P90), scenarioer og backtest for ett produkt. |
| `GET /api/health` | Helsesjekk. |

## Datamodell (v1)

| Tabell | Innhold |
|---|---|
| `dataset` | id, filnavn, opplastet tidspunkt, valideringsstatus |
| `sales` | dataset_id, produkt_id, maaned, antall |
| `forecast` | dataset_id, produkt_id, maaned, modell, p10, p50, p90 |
| `backtest_result` | dataset_id, produkt_id, modell, wape, intervalldekning |

Trinn 2 legger til en tabell `inventory` (produkt_id, lager, ledetid_mnd) og endepunkter for anbefaling og forklaring.

## Fra technology.md: med og ikke med i v1

- **Med:** FastAPI, Next.js, mock-fallback-prinsippet, seeding ved oppstart (`seed_if_empty`) og feature flags for trinn 2.
- **Avvik:** SQLite i stedet for PostgreSQL, og ingen Docker Compose. PROGNOS v1 er en enbrukerapp som kjører lokalt, og trenger verken en egen databasetjeneste eller containere.
- **Ikke med:** innlogging og brukerkontoer, betaling (Stripe/Vipps), e-post, Supabase Storage, Redis, Caddy-proxy, capability-tokens, Railway-deploy, backup og overvåking.
