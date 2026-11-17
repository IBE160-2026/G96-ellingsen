---
type: review
target: ../ARCHITECTURE-SPINE.md
lens: rubrikk (konsistenskontrakt)
date: 2026-11-17
---

# Rubrikk-review: ARCHITECTURE-SPINE.md (PROGNOS v1)

## Dom

**Godkjent med endringer.** Spinen er sterk der den mest trengs: regnereglene (AD-3 til AD-7) er låst ett sted, med lagrede verdier, så backend, API og frontend ikke kan regne ulikt. Paradigmet er tydelig og håndhevbart. Versjonene stemmer med memlog. Ingen funn er kritiske.

Svakhetene ligger i grensene mot drift og test. Testmiljøet kolliderer med regelen om null konfigurasjon (DB-stien er en konstant, men testene trenger en midlertidig DB). CI, README-innhold, testkommandoer og pakkehåndtering er nesten tause. Formatet på generatorens utdata (CSV og `fasit.json`) er ikke låst, selv om generatoren og testene bygges hver for seg. I tillegg er det noen kontraktshull i API-et: tidssone ved lesing fra SQLite, `produkt_id` i URL, formen på 409/422-svarene og hvor `scenariototal` regnes.

| Alvorlighet | Antall |
|---|---|
| Kritisk | 0 |
| Høy | 3 |
| Middels | 7 |
| Lav | 10 |

## Sjekkliste

| # | Punkt | Vurdering |
|---|---|---|
| 1 | Reelle divergenspunkter fikset | Ja for regning, rang, rapport, API, datahenting og skjema. Mangler: testisolasjon, generatorformat, tidssone, `produkt_id` i URL og en felles innlastingsfunksjon (H1, H3, M1, M2, M5). |
| 2 | Rule håndhevbar, hindrer Prevents | Stort sett. AD-1 og AD-9 har tester. AD-3, AD-8 («byte-identisk») og AD-10 mangler konkret håndhevelse (M4, L3, L4). |
| 3 | Deferred som lar enheter divergere | Ingen alvorlige. Kaldstart av numba bør få en utløser og eier (M7). |
| 4 | Teknologi verifisert | Ja, alt stemmer med memlog. Unntak: httpx «gjeldende» og Node «22 eller nyere» er ikke låst (L6). |
| 5 | PRD-dekning | Alle FR og NFR er bundet. NFR-4, NFR-6 og NFR-8 mangler i kapabilitetskartet (L7). `scenariototal` har ingen eier (M3). |
| 6 | Dimensjoner avgjort, utsatt eller åpne | Drift og miljø er delvis tause: CI, testkommandoer, README, pakkehåndtering og lockfiler, lint/format og plattform (H1, H2, M6, L8). |
| 7 | Terse og gyldig mermaid | Stort sett terse. Avsnittet om avstemming med beslutningsloggen er historikk (L9). `\n` i nodetekster er ikke portabelt (L10). |

## Funn

### Høy

**H1. Testmiljøet bryter regelen om at DB-stien er en konstant og at ingen kode leser miljøvariabler.**
*Sjekkliste 1, 6.* Konvensjonen *Konfigurasjon* sier at stier er konstanter i `konstanter.py`, og AD-11 sier at ingen kode leser miljøvariabler. Konvensjonen *Tester* sier samtidig at skallet testes mot en midlertidig SQLite-fil, og at Playwright kjører mot ekte backend med seed. Spinen sier ikke hvordan testene får en annen DB-fil. Uten en regel kommer pytest-fixtures, kontrakttesten og Playwright til å løse dette hver for seg, for eksempel med monkeypatching, en miljøvariabel som sniker seg inn, eller ved å kjøre mot utviklerens egen `backend/data/prognos.db`. Det siste gjør e2e-testene avhengige av hvilke datasett som allerede finnes (FR-25 seeder bare når DB-en er tom).
**Forslag:** Legg til en AD eller konvensjon: «`main.py` eksponerer `lag_app(db_sti: Path = konstanter.DB_STI)`. pytest bruker `lag_app(tmp_path / 'test.db')`. Playwright starter backend med `uv run python -m prognos.e2e_server` (eller et CLI-argument `--db`) mot en fersk fil i `frontend/e2e/.tmp/`, som slettes før hver kjøring. Ingen test bruker `backend/data/prognos.db`.» Et CLI-argument er ikke en miljøvariabel, så NFR-1 holder.

**H2. Drift og testkjøring er nesten tause: CI, testkommandoer, README og hvordan Playwright starter tjenestene.**
*Sjekkliste 6.* NFR-1 krever at README lister forutsetninger med versjoner og kommandoer for installasjon, start og *alle testene*. NFR-6 krever en grønn testkjøring, og F12 testes ut fra README. Spinen gir bare startkommandoene og sier at «den eksakte ordlyden står i README». Den sier ikke:
- hvilke kommandoer som kjører pytest, Vitest, kontrakttesten og Playwright, og fra hvilken mappe,
- om Playwright starter backend og frontend selv (`webServer` i `playwright.config.ts`) eller forutsetter at de kjører,
- om prosjektet har CI eller ikke. Det er helt tause, og det er et funn i seg selv,
- hvem som eier README, og hva den skal inneholde utover NFR-1.

**Forslag:** Legg til en rad *Drift* i konvensjonene, eller en kort AD-14:
- Installasjon: `uv sync` i `backend/` og `npm ci` i `frontend/`.
- Tester: `uv run pytest` i `backend/`, `npm test` (Vitest) og `npm run e2e` (Playwright) i `frontend/`. Playwright har `webServer` for begge tjenestene, mot test-DB-en fra H1.
- Kontrakttesten kjører som en del av `npm run e2e` (den trenger ekte backend).
- CI: enten «Ingen CI i v1, testene kjøres lokalt før innlevering» (under Deferred) eller «GitHub Actions kjører pytest og Vitest på push». Velg én.
- README eies av repoet og har minst: forutsetninger med versjoner, installasjon, start, alle testkommandoene, maskinspesifikasjonen for NFR-7 og en setning om FR-25.

**H3. Formatet på generatorens utdata er ikke låst, selv om generatoren og testene bygges hver for seg.**
*Sjekkliste 1, 5.* Generatoren (FR-23, FR-24) skriver `syntetisk.csv` og `fasit.json`, og disse leses av `seed_if_empty`, F7/F8-testene og FR-24-testen (P50 innenfor 5 % av fasiten). Spinen låser bare seed 42. Det mangler:
- skilletegn, koding (UTF-8 uten BOM?) og linjeskift i CSV-fila. På Windows skriver Pythons `csv`-modul `\r\n` hvis fila ikke åpnes med `newline=''`. Da kan to maskiner gi ulike bytes, og F9 (byte-identisk) blir plattformavhengig,
- skjemaet for `fasit.json` (felt per produkt: trend, sesongprofil, støynivå, og hvordan tallene formateres),
- om det støyfrie FR-24-produktet ligger i `syntetisk.csv` (og dermed påvirker F7/F8 og WAPE-oversikten i demoen) eller i en egen fil,
- om `syntetisk.csv` og `fasit.json` er sjekket inn (`seed_if_empty` forutsetter det), og om en test sjekker at den innsjekkede fila er lik generatorens utdata,
- hvordan NFR-7-fila (200 × 36) lages: av generatoren med et annet argument, eller av testen.

**Forslag:** Legg til en konvensjon *Testdata*: «`syntetisk.csv`: komma, UTF-8 uten BOM, `\n`, kolonnene `produkt_id,maaned,antall`. `fasit.json`: `{produkt_id: {trend, sesongprofil[12], stoey}}`, skrevet med `json.dumps(..., sort_keys=True, indent=2)` og `\n`. Det støyfrie produktet ligger ikke i `syntetisk.csv`, men lages av testen med generatorens funksjon. Begge filene er sjekket inn, og en test sjekker at generatoren gir identiske bytes. NFR-7-fila lages i testen med `generator.lag(antall_produkter=200, seed=…)`.» Lås numpy-versjonen sammen med seed, siden `default_rng` bare er stabil innenfor samme versjon.

### Middels

**M1. `opplastet` mister tidssonen ved lesing fra SQLite.**
*Sjekkliste 1.* Konvensjonen sier UTC og ISO 8601 med `Z`. SQLite har ingen tidssonetype, og SQLAlchemys `DateTime(timezone=True)` gir naive verdier tilbake fra aiosqlite. Pydantic serialiserer da uten `Z`, og frontend tolker tiden som lokal tid. Da vises den 1–2 timer feil i `Europe/Oslo`. DB-laget og API-et kan løse dette ulikt.
**Forslag:** Lås det i konvensjonen *Tidspunkt*: «`opplastet` lagres som tekst i formatet `ÅÅÅÅ-MM-DDTHH:MM:SSZ` (eller med en `TypeDecorator` som setter UTC ved lesing). zod-skjemaet krever `Z` (`z.iso.datetime()` uten offset).» Legg til en test som sjekker at strengen slutter på `Z` etter omstart.

**M2. `produkt_id` i URL-stien er ikke definert for tegn som `/`, `#`, `%` og mellomrom.**
*Sjekkliste 1.* `produkt_id` er strengen fra CSV-fila uendret og brukes i `GET …/products/{produkt_id}`. Starlette dekoder stien før rutingen, så `%2F` blir `/` og ruten treffer ikke. Frontend (`encodeURIComponent`) og backend kan da være uenige, og en gyldig fil kan gi produkter som ikke kan åpnes. Det er heller ikke sagt om ledende og etterfølgende mellomrom fjernes.
**Forslag:** Velg én av to: (a) Valideringen avviser `produkt_id` som ikke matcher `^[A-Za-z0-9._-]+$`, med en egen feilkode og norsk melding, eller (b) ruten bruker `{produkt_id:path}` og klienten bruker `encodeURIComponent`. Legg også til i konvensjonen *Id-er*: «Mellomrom foran og bak fjernes ved innlesing (eller: gir feil).» (a) er enklest og kan testes.

**M3. `scenariototal` har ingen eier i lagringsmodellen.**
*Sjekkliste 1, 5.* AD-1 sier at bare `domene/` regner ut scenariototaler, og AD-3 sier at lesere aldri regner. Men AD-3 lister ikke `scenariototal` blant de lagrede verdiene, og det finnes ikke i ER-diagrammet. AD-9 returnerer `scenariototal{p10, p50, p90}`. Da kan API-et (eller en SQL-`SUM`) komme til å summere `prognose` ved lesing, og det bryter AD-3.
**Forslag:** Legg til i AD-3: «`produkt.scenariototal_p10/p50/p90` (heltall, `NULL` uten prognose), regnet i kjernen fra avrundede verdier (AD-5).» Alternativt: si eksplisitt at API-et summerer `prognose` i Python med én navngitt funksjon fra `domene/`.

**M4. Formen på feilsvar fra `POST /api/datasets` er ikke fullstendig.**
*Sjekkliste 1, 2.* (a) `409 {rapport}`: `status` har bare `godkjent`, `avvist` og `feilet`. Det er ikke sagt hvilken status og melding en 409-rapport har. (b) Hvis feltet `fil` mangler, eller forespørselen ikke er multipart, svarer FastAPI med standard `422 {detail: [...]}`. Det kolliderer med `422 {rapport}`, og zod-parsingen i klienten feiler. (c) En uventet 500 har en «generisk norsk melding», men det er ikke sagt om den kommer som `{rapport}` eller `{detail}`.
**Forslag:** I AD-9: «Alle ikke-2xx-svar fra `POST /api/datasets` er `{rapport}`. 409 gir `status: feilet` med `feil[0].kode = 'opptatt'`. En egen `RequestValidationError`-handler oversetter manglende eller ugyldig `fil` til `422 {rapport}` med `kode = 'mangler_fil'`. Uventede unntak gir `500 {rapport}` med `kode = 'intern'`.» Lås listen over `kode`-verdier i `domene/feil.py` (se L1).

**M5. Den felles innlastingsfunksjonen for opplasting og seed er ikke navngitt.**
*Sjekkliste 1, 2.* AD-2 sier at `seed_if_empty` bruker samme pipeline og samme skrivefunksjon. Men orkestreringen rundt (filnavn, `opplastet`, hva som skjer med rapporten, logging per steg, `feilet`-håndtering) ligger mellom pipelinen og skrivingen og kan skrives to ganger, i `api/` og i `oppstart.py`. Det er heller ikke sagt hva backend gjør hvis seedingen selv feiler: stopper den, eller starter den med tom DB?
**Forslag:** Navngi én funksjon, for eksempel `db/innlasting.py: last_inn(bytes, filnavn, naa) -> Kjoreresultat | Valideringsrapport`, som både ruten og `oppstart.py` kaller. Legg til i AD-2: «Hvis seedingen feiler, logges rapporten, og backend stopper med en norsk melding.» (eller «starter med tom DB»). Velg én.

**M6. Pakkehåndtering, lockfiler og plattform er ikke låst.**
*Sjekkliste 6.* `npm run dev` antyder npm, men det står ikke at `package-lock.json` og `uv.lock` er sjekket inn, eller at installasjonen bruker `npm ci` og `uv sync --frozen`. Uten låste filer kan to medlemmer (og sensor) få ulike underavhengigheter, og det rammer særlig statsforecast/numba/pandas. Det er heller ikke sagt hvilke operativsystemer README skal fungere på. Repoet utvikles på Windows, og `predev`-skript og stier må fungere der.
**Forslag:** Konvensjon *Avhengigheter*: «npm og `package-lock.json`, uv og `uv.lock`, begge sjekket inn. Installasjonen bruker `npm ci` og `uv sync --frozen`. Skriptene i `package.json` er plattformuavhengige (ingen `rm`, `&&`-kjeder bare der npm støtter dem). Støttes: Windows 11 og macOS.»

**M7. Kaldstart av numba er utsatt uten utløser, og kan treffe 120 s-grensen.**
*Sjekkliste 3.* Utsettelsen er rimelig fordi NFR-7 gjelder varm kjøring. Men når DB-en ikke er tom, hopper oppstarten over seedingen, og den første opplastingen etter en omstart kompilerer numba kaldt. Det skjer også i Playwright hvis e2e-DB-en ikke er tom. Hvis kompileringen tar lang tid, nærmer det seg klientens 120 s (AD-11), og UJ-4 etterfulgt av UJ-1 kan feile hos sensor. Det berører både backend (oppstart) og frontend (timeout), så det er ikke rent lokalt.
**Forslag:** Gi utsettelsen en utløser og en eier: «Måles i NFR-7-testen. Hvis kald kjøring av 200 × 36 tar over 60 s, varmer `oppstart.py` opp med én liten pipelinekjøring i bakgrunnen. Eier: backend, før epic for opplasting er ferdig.»

### Lav

**L1. Feilkodene i `Valideringsrapport.feil[].kode` er ikke listet.**
Frontend viser bare `melding`, men testene for FR-3/F4 og M4 trenger stabile koder. Lås en enum i `domene/feil.py`, for eksempel `mangler_kolonne`, `ugyldig_maaned`, `ugyldig_antall`, `tom_celle`, `duplikat`, `ingen_rader`, `ukjent_skilletegn`, `ugyldig_koding`, `kjoring_feilet`, `opptatt`, `mangler_fil`, `intern`.

**L2. «Lik» og «ETS taper» sammenligner flyttall.**
AD-7 avgjør dommeren ut fra WAPE. Begge modellene har samme `sum_faktisk`, så sammenligningen kan gjøres eksakt på heltallene `sum_avvik`. Legg til i AD-7: «Dommeren avgjøres ved å sammenligne `sum_avvik` (heltall), ikke `wape`.» Da kan ikke avrundingsstøy gi `ets_taper` når verdiene egentlig er like.

**L3. «Byte-identisk» i AD-8 er vanskelig å håndheve.**
Rapporten returneres som en del av et større objekt og serialiseres på nytt av Pydantic. Skriv heller: «`GET /api/datasets/{id}` returnerer en `rapport` som er lik (etter parsing) den som ble returnert av `POST`, og en test sjekker det.»

**L4. AD-3 og AD-10 mangler konkret håndhevelse.**
AD-3: legg til en test som søker etter `func.sum`, `func.avg` og WAPE-regning i `db/`, `api/` og `frontend/` (grep-test eller lint-regel). AD-10: prosesslåsen gjelder bare én prosess. Skriv at uvicorn startes uten `--workers` (og uten `--reload` i e2e).

**L5. AD-1 sin determinismeregel må unnta skilletegnet for F13.**
«Samme CSV-innhold gir identisk `Kjoreresultat`» dekker ikke F13, der innholdet er ulikt (komma og semikolon). Skriv: «Filer som bare skiller seg i skilletegn, gir identisk `Kjoreresultat` bortsett fra `skilletegn`.»

**L6. To versjoner er ikke låst.**
`httpx` står som «gjeldende», og Node som «22 LTS eller nyere» (lokalt kjører Node 26). Lås httpx til en sjekket minorversjon. Skriv Node som «22 eller 24 LTS» og legg `engines` i `package.json`. Python 3.12 bør stå i `requires-python` og `.python-version`.

**L7. Kapabilitetskartet mangler NFR-4, NFR-6, NFR-8 og NFR-9.**
De er bundet i frontmatter og dekket av konvensjonene (*Tekster*, *Tester*) og AD-9/AD-13, men ikke i kartet. Legg til fire rader for sporbarheten.

**L8. Lint og formatering er tause.**
To utviklere og KI-agenter som skriver kode hver for seg, vil formatere ulikt. Avgjør eller utsett eksplisitt: for eksempel ruff (lint + format) i backend og ESLint + Prettier (eller Biome) i frontend, med kommandoer i README.

**L9. Avsnittet «Avstemt mot beslutningsloggen» er historikk, ikke beslutninger.**
Det forteller hva som var utdatert i utkastet. Flytt det til `forklaring-for-sensor.md` eller memlog, og behold bare setningen om at historikknivået heter `sesongnaiv`, som allerede står i AD-6. AD-9 til AD-13 mangler også statusmerket `[ADOPTED]`, som AD-1 til AD-8 har. Merk dem likt.

**L10. `\n` i mermaid-nodetekster er ikke portabelt.**
Diagrammene er syntaktisk gyldige: flowchart med kantetiketter `-->|…|` og `-.->|…|`, subgraph med tittel og erDiagram med siterte relasjonsetiketter. Men `\n` i nodetekster, for eksempel `N[klassifiser\nhistorikknivå]`, vises som linjeskift bare i noen renderere. Andre viser `\n` som tekst. Bruk `<br/>` i stedet. Vurder også å vise `scenariototal` (M3) og `skjemaversjon` (AD-13) i ER-diagrammet.

## Det som fungerer godt

- **AD-3 til AD-7** låser alle regnereglene ett sted og lagrer resultatet. Det fjerner den største divergensrisikoen i prosjektet (WAPE, totaler, n av m og rang regnet på flere måter).
- **AD-5** fastsetter avrundingen eksplisitt (`floor(x + 0.5)`, ikke Pythons bankavrunding) og rekkefølgen nullgrense → avrunding → metrikker. Det gjør NFR-5 etterprøvbar.
- **AD-6** gir tabellen med inklusive grenser og én eier (`nivaa.py`), og løser den gamle uklarheten rundt 12–17 måneder.
- **AD-11** er verifisert mot kildekoden i Next 16.4.6 (`proxyTimeout || 30000`), og det er akkurat den typen fallgruve en spine skal fange.
- **AD-9 + AD-12** gir én kontrakt (Pydantic), en kopi med test (zod) og faste spørringsnøkler.
- **Stack-tabellen** stemmer med versjonsoppføringene i memlog. Låsingen av pandas 2.3.3 og TypeScript 5.9 er begrunnet i memlog.
