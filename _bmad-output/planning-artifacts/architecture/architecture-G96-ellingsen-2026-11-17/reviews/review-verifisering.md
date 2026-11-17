---
review: verifisering
target: ../ARCHITECTURE-SPINE.md
lens: Er hver bindende beslutning nett-undersøkt eller realitetssjekket (versjoner, at teknologiene finnes og passer sammen, at API-er og opsjoner finnes i de versjonene)?
date: 2026-11-17
---

# Review: verifisering av stack og API-er

## Dom

**Godkjent med rettinger.** Versjonstabellen stemmer med PyPI og npm per 2026-11-17, og memloggen viser at proxyTimeout faktisk ble sjekket i kildekoden. Alle API-ene spinen binder for statsforecast, FastAPI, SQLAlchemy og Next finnes og fungerer i de oppgitte versjonene. Men to avhengigheter mangler i stacken, og uten dem starter ikke backend. Påstanden «null eksterne kall» (AD-11) holder heller ikke helt for `next dev`. Ingen funn krever at en beslutning endres. Alle kan rettes med en linje i Stack eller en presisering i en AD.

## Metode

- Metadata: `curl https://pypi.org/pypi/<pkg>/json` og `https://registry.npmjs.org/<pkg>/latest` (versjon, `requires_python`, `requires_dist`, `engines`, `peerDependencies`).
- Kjøring: isolerte miljøer med `uv run --no-project --python 3.12 --with ...`. Skriptene lå i scratchpad, ikke i repoet.
  - statsforecast 2.1.1 + pandas 2.3.3 + numpy 2.5.5: modellene, signaturene og kolonnene i `cross_validation` og `forecast`.
  - fastapi 0.163.2 + sqlalchemy 2.1.9 + aiosqlite 0.22.1 + httpx 0.28.1: UploadFile, lifespan, `run_in_threadpool`, `create_all` via `run_sync` og JSON-kolonne, med og uten python-multipart.
- Kildekode: tarball av `next@16.4.6` og `create-next-app@16.4.6` fra registry.npmjs.org. Lest: `proxy-request.js`, `config-shared.*`, `body-streams.js`, `resolve-routes.js`, `router-server.js`, `hot-reloader-*.js`, `lib/upgrade/*`, `cli/next-telemetry.js` og malen `app-tw`.
- Registret til shadcn: `ui.shadcn.com/r/styles/*/chart.json`. Node: `nodejs.org/dist/index.json` og `nodejs/Release/schedule.json`.

## Funn

### V-1 [Høy] SQLAlchemy 2.1 tar ikke med `greenlet`, så async-motoren krasjer ved import

**Bevis:** I `sqlalchemy 2.1.9` er `requires_dist` bare `greenlet>=1; extra == "asyncio"`. I 2.0.x ble greenlet installert automatisk på x86_64/AMD64. Med `--with sqlalchemy==2.1.* --with aiosqlite==0.22.*` feiler `from sqlalchemy.ext.asyncio import create_async_engine` med `ImportError: The SQLAlchemy asyncio module requires that the Python 'greenlet' library is installed`.
**Konsekvens:** AD-2, AD-10 og AD-13 bygger på `AsyncSession` og async `create_all`. Backend starter ikke.
**Retting:** Endre raden i Stack til `SQLAlchemy (async) | 2.1.x, installert som sqlalchemy[asyncio]`. Alternativt `sqlalchemy[aiosqlite]`, som drar med både asyncio-ekstraen og aiosqlite. Etter rettingen er dette verifisert: `create_all` via `conn.run_sync` og en JSON-kolonne med æøå går rundt uendret.

### V-2 [Høy] `python-multipart` mangler i stacken, og `POST /api/datasets` kan ikke registreres

**Bevis:** I `fastapi 0.163.2` ligger `python-multipart` bare i ekstraene `standard` og `all`. Uten pakken kaster FastAPI `RuntimeError: Form data requires "python-multipart" to be installed` når ruten med `UploadFile = File(...)` defineres, altså allerede ved import av appen. Med `python-multipart 0.0.34` gir en multipart-POST med felt `fil` 200, og `filename` kommer med.
**Konsekvens:** AD-9 (multipart, felt `fil`) og FR-1 får ikke kjørt i det hele tatt.
**Retting:** Legg til `python-multipart | 0.0.x (0.0.34 per 2026-11-17)` i Stack. Ikke bruk `fastapi[standard]`, for den drar med fastapi-cli, cloud-CLI og annet NFR-1 ikke trenger.

### V-3 [Middels] `next dev` gjør eksterne kall som `next telemetry disable` ikke stopper (AD-11, NFR-1)

**Bevis i next@16.4.6:**
- `server/dev/hot-reloader-shared-utils.js` `getVersionInfo()` kaller `fetch('https://registry.npmjs.org/-/package/next/dist-tags')`. Kallet går lazy ved første HMR-`SYNC` til nettleseren (`hot-reloader-turbopack.js` linje ~1422), og feil svelges stille.
- `experimental.agentUpgrade` er `'security'` som standard (`config-shared.js`), og `router-server.js` kaller `nudgeUpgrade(...)` i dev. `lib/upgrade/prepare-upgrade.js` gjør `fetch(url)`, og `nudge.js` refererer `https://registry.npmjs.org/next/latest`.
- Telemetri-flagget (`cli/next-telemetry.js`, `disable`) styrer bare telemetrien.
**Konsekvens:** NFR-1-testen («UJ-1 fungerer med nettverket koblet fra») består fordi feilene svelges. Men spinens regel «null eksterne kall» stemmer ikke når maskinen er på nett. En sensor som ser på nettverkstrafikken, vil se kall til npm.
**Retting:** I AD-11:
1. Sett `experimental: { proxyTimeout: 130000, agentUpgrade: false }` i `next.config.ts`. Opsjonen finnes i `ExperimentalConfig` i 16.4.6.
2. Skriv eksplisitt at `next dev` sjekker versjonen mot registry.npmjs.org i dev-modus, og at kallet feiler stille uten nett. Alternativt kan sensor kjøre `next build && next start`, siden versjonssjekken bare finnes i hot-reloaderen. Rewrites og proxyTimeout gjelder også der.
3. Hvis `npm run build` brukes, må telemetrien også slås av i `prebuild`, ikke bare i `predev`.

### V-4 [Middels] Malen i `create-next-app@16.4.6` bryter AD-11 fra start (`next/font/google`)

**Bevis:** `templates/app-tw/ts/app/layout.tsx` har `import { Geist, Geist_Mono } from "next/font/google"`. Malen bruker ellers `typescript: "^5"` og `tailwindcss: "4.3.3"`, så TS 5.9-låsen stemmer.
**Konsekvens:** Første `next dev` eller `next build` henter fonter fra Google, med mindre layouten skrives om ved init.
**Retting:** Under AD-11 eller i Structural Seed: «Ved init fjernes `next/font/google` fra `app/layout.tsx`. En test eller lint-regel (grep etter `next/font/google` og `https://` i `frontend/app` og `frontend/components`) håndhever det.» Kjør samme sjekk etter `npx shadcn init`, siden CLI-en (4.23.0) kan legge til fontoppsett avhengig av preset. Det er ikke verifisert.

### V-5 [Middels] Skalltestene med `httpx.AsyncClient` kjører ikke lifespan

**Bevis:** Med `httpx.ASGITransport(app=app)` ble `lifespan start` aldri skrevet ut i testkjøringen, fordi ASGITransport ikke sender lifespan-hendelser. httpx 0.28 krever dessuten `transport=ASGITransport(...)`, og snarveien `app=` er fjernet. I tillegg peker `starlette 1.10.0` (avhengighet av fastapi 0.163) nå på `httpx2`. `testclient.py` sier at bruk av `httpx` er utdatert («install `httpx2` instead»). `httpx` står fortsatt på 0.28.1.
**Konsekvens:** Konvensjonen *Tester* sier at skallet testes med `httpx.AsyncClient`. Da blir `create_all`, versjonsvakten og `seed_if_empty` (AD-13, FR-25) ikke kjørt i testene uten et ekstra steg, og testene kan feile med «no such table».
**Retting:** Presiser i *Tester*: «Fixturen åpner `app.router.lifespan_context(app)` (eller bruker `asgi-lifespan`) før `AsyncClient(transport=ASGITransport(app))`.» Lås `httpx` til `0.28.x` i Stack i stedet for «gjeldende». Ta et bevisst valg mellom `httpx` og `httpx2`.

### V-6 [Lav] Rewrite-proxyen kutter forespørsler over 10 MB uten feil

**Bevis:** I `resolve-routes.js` brukes `getCloneableBody(req, config.experimental.proxyClientMaxBodySize)`, og standardverdien er `10485760` (`config-shared.js`). Over grensen skriver `body-streams.js` bare `console.warn` og avslutter strømmen, og `router-server.js` sender den avkortede kroppen videre til `proxyRequest`.
**Konsekvens:** Karis fil (200 × 36 rader, godt under 1 MB) er ikke berørt. En fil over 10 MB kommer frem avkortet, og backend gir en uforståelig multipart- eller CSV-feil i stedet for en norsk melding.
**Retting:** Legg en maks filstørrelse i `prognos/konstanter.py` (for eksempel 5 MB) med egen kode og norsk melding i `Valideringsrapport`, og sjekk den også i klienten før opplasting. Alternativt kan `experimental.proxyClientMaxBodySize` settes eksplisitt over grensen.

### V-7 [Lav] Det utsatte punktet om kaldstart av numba bygger på en utdatert antakelse

**Bevis:** `statsforecast 2.1.1` har `requires_dist` med `coreforecast`, `scipy`, `statsmodels`, `utilsforecast`, `fugue` og andre, men **ikke numba**. Numba ble ikke installert, og det finnes ingen forekomst av `numba` i `statsforecast/**/*.py`. Import av `AutoETS` tok ~1,4 s.
**Retting:** Skriv om punktet under Deferred til «Kaldstart (import og første tilpasning) av statsforecast (NFR-7)». Selve beslutningen (mål først) kan stå.

### V-8 [Lav] Node-kravet er for løst

**Bevis:** `next@16.4.6` krever `node >=20.9.0`, men `vitest@5.1.0` krever `^22.12.0 || ^24.0.0 || >=26.0.0`. Node 22 (Jod) har vært i maintenance siden 2025-10-21 og når EOL 2027-04-30. Node 24 (Krypton) er i maintenance-LTS, og Node 26 (Lithium) har vært aktiv LTS siden 2026-10-28. Lokalt kjøres 26.13.1.
**Retting:** Endre til «Node.js 24 LTS eller 26 LTS (minst 22.12)». Legg `"engines": {"node": ">=22.12"}` i `frontend/package.json`.

### V-9 [Lav] `shadcn add chart` nedgraderer Recharts

**Bevis:** I alle de tre registerstilene (`new-york-v4`, `base-nova`, `radix-nova`) har `chart.json` `dependencies: ["recharts@3.8.0", ...]`. Spinen låser `3.11.x`.
**Retting:** Bestem i Stack enten «Grafen bruker Recharts direkte, ikke shadcn `chart`» eller «etter `shadcn add chart` låses `recharts` tilbake til 3.11.x».

### V-10 [Lav] Peer-avhengigheten `react-is` til Recharts er ikke nevnt

**Bevis:** `recharts@3.11.0` har peer `react-is: ^16.8 || ... || ^19.0.0`. Siste versjon av `react-is` er 19.3.1.
**Retting:** Legg `react-is` 19.3.x (lik React) eksplisitt i `frontend/package.json`, så npm ikke velger en versjon som ikke passer.

### V-11 [Info] Bekreftet uten avvik

| Påstand i spinen | Status | Bevis |
|---|---|---|
| statsforecast 2.1.1 har `AutoETS(season_length=12)` og `SeasonalNaive(season_length=12)` | OK | Kjørt |
| `StatsForecast.cross_validation(h, df, n_windows, step_size, level, ...)` | OK | Signaturen lest med `inspect`. Kjøring med `h=1, n_windows=6, step_size=1, level=[80]` gir 6 rader per serie |
| Kolonnene i CV | OK | `unique_id, ds, cutoff, y, AutoETS, AutoETS-lo-80, AutoETS-hi-80, SeasonalNaive, SeasonalNaive-lo-80, SeasonalNaive-hi-80`, med `cutoff < ds`. `forecast(h=6, level=[80])` gir de samme kolonnene uten `cutoff` og `y` |
| SeasonalNaive-backtest på 18 mnd og ETS-backtest på 24 mnd | OK | Begge gir 6 rader uten unntak |
| statsforecast krever `pandas<3` | OK | `requires_dist`: `pandas<3.0.0`. pandas 3.1.1 finnes, så låsen er nødvendig |
| pandas 2.3.3 på Python 3.12 og numpy 2.5 | OK | Har cp312-hjul. Krever `numpy>=1.26.0` for py≥3.12 og har ingen øvre grense. Kjørt med numpy 2.5.5 |
| Python 3.12 | OK, og er gulvet | numpy 2.5.5 har `requires_python >=3.12`. FastAPI og SQLAlchemy 2.1 krever ≥3.11 |
| `run_in_threadpool` (AD-10) | OK | Finnes i `starlette.concurrency` (starlette 1.10.0) og er samme objekt som `fastapi.concurrency.run_in_threadpool`. Det er en tynn wrapper rundt `anyio.to_thread.run_sync` |
| `FastAPI(lifespan=...)` | OK | Registreres. `on_startup` brukes ikke, som er riktig for Starlette 1.x |
| `create_all` via `async with engine.begin(): await conn.run_sync(...)` og `JSON`-kolonne i SQLite | OK (med V-1) | Kjørt. Dict med æøå går rundt med `==` |
| `experimental.proxyTimeout`, standard 30000 ms | OK | `proxy-request.js`: `proxyTimeout === null ? undefined : proxyTimeout \|\| 30000`. Typen er `proxyTimeout?: number`. Brukes for rewrites i `router-server.js` (gjelder både dev og start). Memloggen har korrekt bevis |
| `next telemetry disable` | OK | `cli/next-telemetry.js` håndterer `disable`. Skriver til global brukerkonfig (se V-3 for dekningen) |
| TypeScript 5.9 med Next 16.4 | OK | `verify-typescript-setup.js` krever bare ≥5.1.0. `create-next-app` bruker `^5`, og 5.9.3 er siste 5.x. TS 7.0.2 er `latest` på npm, så låsen til 5.9.x må stå i `package.json` (ikke `^5` ukontrollert, og ikke `latest`) |
| React 19.3 med Next, TanStack Query, Recharts | OK | Peers: next `^19.0.0`, react-query `^18 \|\| ^19`, recharts `^19.0.0` |
| zod 4.6.7, TanStack Query 5.108.0, Recharts 3.11.0, Vitest 5.1.0, Playwright 1.65.1, Tailwind 4.3.5, shadcn 4.23.0 | Finnes | npm `latest`. Next 16.4.6 har peer `@playwright/test ^1.51.1`, og Vitest 5.1 krever peer `vite ^6.4 \|\| ^7 \|\| ^8` |
| uv 0.13.x | OK | PyPI 0.13.9, lokalt 0.13.8 |
| pytest 9.2.0 / pytest-asyncio 1.5.0 | OK | pytest-asyncio krever `pytest>=8.4` |

### V-12 [Info] Små ting som bør bindes, fordi spinen forutsetter dem

- **`freq="MS"`** for `StatsForecast(...)` er ikke nevnt i AD-6. Uten den samme frekvensen i prognose og backtest blir `ds` og `cutoff` feil, og «`maaned` = opprinnelse + 1 måned» holder ikke. Legg den til i AD-6.
- **Én `StatsForecast` per modellgruppe.** Et objekt med begge modellene kjører ETS-backtest også for 24–29 mnd. Det gikk uten feil på 24 mnd. AD-6 bør si at `nivaa.py` velger modellisten per produktgruppe før kallet, ellers lagres eller kastes data som ikke skulle beregnes.
- **P50 = punktprognosen.** For AutoETS er den forventningsverdien. Med symmetriske normalintervaller er det det samme som medianen, så navnet er forsvarlig. Det bør likevel stå én setning om det i forklaringen for sensor.
- **`RuntimeWarning: divide by zero encountered in scalar divide`** kom fra statsforecast under testkjøringen. Det er ufarlig, men bør filtreres eller logges bevisst, så det ikke støyer i stdout (konvensjonen *Logging*).
- **FastAPI 0.163 har `opentelemetry-api>=1.44` som fast avhengighet.** Det er bare API-et (no-op) og gjør ingen kall. Det er nevnt fordi NFR-1 er streng.
- **«Byte-identisk» rapport (AD-8)** gjelder JSON-innholdet. Bytene i HTTP-svaret avhenger av Pydantic-serialiseringen. Presiser til «semantisk identisk» eller «serialisert av samme Pydantic-modell».

## Oppsummert retting av Stack-tabellen

| Navn | Fra | Til |
|---|---|---|
| SQLAlchemy (async) | 2.1.x | 2.1.x som `sqlalchemy[asyncio]` (V-1) |
| python-multipart | (mangler) | 0.0.x (V-2) |
| httpx | gjeldende | 0.28.x, eller bevisst valg av httpx2 (V-5) |
| Node.js | 22 LTS eller nyere | 24 LTS eller 26 LTS, minst 22.12 (V-8) |
| react-is | (mangler) | 19.3.x (V-10) |
| next.config.ts | proxyTimeout | proxyTimeout + `agentUpgrade: false` (V-3) |
