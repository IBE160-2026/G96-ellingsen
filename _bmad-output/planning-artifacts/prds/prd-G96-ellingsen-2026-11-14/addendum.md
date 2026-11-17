# Addendum til PRD: PROGNOS v1

Dette er tekniske føringer fra briefens avsnitt 5, beslutningsloggen og arkitekturutkastet. De hører hjemme i arkitekturdokumentet og står her for å binde kravene i PRD-en til valgene som allerede er gjort. Den fullstendige tekniske beskrivelsen finnes i [ARCHITECTURE-SPINE.md](../../architecture/architecture-G96-ellingsen-2026-11-17/ARCHITECTURE-SPINE.md). Den erstattet [arkitektur-utkast.md](../../../../.docs/planning-artifacts/architecture/arkitektur-utkast.md) 2026-11-17.

**Når kildene sier forskjellig:** Ved avvik mellom arkitekturutkastet og beslutningsloggen gjelder beslutningsloggen og PRD-en. Det gjelder nå radene *Total WAPE*, *Sortering av produktlisten*, *Backtest for 12–17 mnd*, *WAPE når faktisk salg er 0* og *Intervalldekning og sortering*. Utkastet oppdateres når arkitekturen lages.

## Teknologi som gjelder kravene

| PRD-krav | Teknisk føring |
|---|---|
| FR-6, NFR-2, NFR-3 | SQLite som lokal fil, SQLAlchemy 2 (async) + `aiosqlite`. Fila opprettes ved første oppstart. Beslutningslogg: *Database*. Avviket fra PostgreSQL i technology.md begrunnes med faglærers tilbakemelding. |
| FR-8, FR-9, FR-10 | `statsforecast`: `AutoETS` og `SeasonalNaive`, `h=6`, `level=[80]`. Nullgrense `max(0, ·)` på P10, P50 og P90 etter modellkjøringen. |
| FR-13–FR-16 | `cross_validation` i `statsforecast` med `n_windows=6`, `h=1` og `step_size=1`. Produkter med under 18 mnd historikk tas ikke med i kjøringen, og produkter med 18–29 mnd kjøres bare med `SeasonalNaive`. |
| FR-18–FR-22 | Next.js 16 (App Router), React 19, TypeScript, Tailwind v4, shadcn/ui, TanStack Query v5, `zod`, Recharts. |
| FR-25 | `seed_if_empty` ved oppstart av backend. |
| NFR-1 | `uv run` (backend) og `npm run dev` (frontend), uten Docker. Frontend videresender `/api/*` til backend (single-origin, ingen CORS). |
| NFR-6 | `pytest` + `pytest-asyncio`, Vitest og Playwright (F10). |
| NFR-7 | Tidtakingen gjøres etter én oppvarmingskjøring. Kaldstart måles og rapporteres, men har ingen grense. *Rettet 2026-11-17:* `statsforecast` 2.1.1 bruker ikke `numba`, så det er ingen kompileringsbuffer å sette opp. Se AD-2 og *Deferred* i arkitekturen. |

## Kjøring uten nett (NFR-1)

- Next.js-telemetrien slås av som del av `npm run dev`, for eksempel med `next telemetry disable` i et `predev`-skript. Det skal ikke kreve miljøvariabler.
- Bare lokale fonter eller systemfonter brukes. Ingen `next/font/google` og ingen CDN.
- v1 har ingen feature flags og ingen mock-fallback, fordi v1 ikke kaller noen ekstern tjeneste. Punktene i utkastets «Med»-liste som gjelder dette, hører til trinn 2.

## API og datamodell

Fra arkitekturutkastet:

- `POST /api/datasets`, `GET /api/datasets`, `GET /api/datasets/{id}/products`, `GET /api/datasets/{id}/products/{produkt_id}`, `GET /api/health`.
- Tabeller: `dataset`, `sales` (med `utfylt`), `product_status` (med `historikknivaa`, `ets_taper`), `forecast`, `backtest_result`.

**Løst i arkitekturen 2026-11-17:** Alle fem punktene under er løst i [ARCHITECTURE-SPINE.md](../../architecture/architecture-G96-ellingsen-2026-11-17/ARCHITECTURE-SPINE.md): punkt 1 og 2 i AD-3 og AD-4, punkt 3 og 4 i AD-8 og AD-9, og punkt 5 i AD-6. Arkitekturen erstatter arkitekturutkastet.

**Utsatt til arkitekturen (funn H6 i PRD-gjennomgangen):** Datamodellen og API-et i utkastet kan ikke levere alt PRD-en krever.

1. Total WAPE (FR-14) er Σ|faktisk − P50| / Σ faktisk over produktene. Den kan ikke regnes ut fra WAPE per produkt alene. Det trengs enten summene per produkt og modell (`sum_abs_feil`, `sum_faktisk`) eller verdiene per opprinnelse.
2. Backtest-tabellen skal kunne vise faktisk verdi og P50 per opprinnelse (FR-21, NFR-5). Forslag: en tabell `backtest_point` (dataset_id, produkt_id, modell, opprinnelse, maaned, faktisk, p10, p50, p90).
3. WAPE-oversikten (FR-22) trenger et oppsummeringsendepunkt, for eksempel `GET /api/datasets/{id}/summary`, eller et oppsummeringsfelt i svaret fra `GET /products`. Den skal bygge på lagrede data, slik at den er lik etter omstart (F11).
4. Valideringsrapporten skal vises igjen når et lagret datasett åpnes (FR-18). Den må derfor lagres i sin helhet, med advarsler og antall produkter per historikknivå.
5. Historikknivået for 12–23 mnd heter *sesongnaiv* i PRD-en. Utkastet bruker `baseline` som verdi i `historikknivaa`.

## Forberedt for trinn 2 (utenfor v1)

Arkitekturutkastet nevner feature flags (`FEATURE_DECISION`, `FEATURE_AI`) og en senere tabell `inventory`. Ingenting av dette bygges i v1. v1 skal ikke være avhengig av en språkmodell eller en API-nøkkel.
