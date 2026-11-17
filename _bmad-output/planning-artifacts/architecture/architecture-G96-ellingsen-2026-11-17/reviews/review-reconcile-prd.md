# Avstemming: ARCHITECTURE-SPINE.md mot prd.md og addendum.md

Dato: 2026-11-17 · Reviewer: avstemmingsreviewer (KI) · Kilder lest i sin helhet: `prd.md`, `addendum.md`, `ARCHITECTURE-SPINE.md` (EXPERIENCE.md sjekket punktvis for ordrette tekster).

## Dom

**Godkjent med rettinger.** Spinen dekker kildene godt, og ingen funn er kritiske. Alle fem punktene i H6 er løst. Grensene i FR-5/FR-16, mengden *S* (FR-14/15/22), sorteringen i FR-19 og detaljtabellen i FR-21 stemmer med PRD-en. De viktigste svakhetene er én tolkning som ikke står i PRD-en (heltallsavrunding, AD-5), som kan felle FR-24-testen og påvirke F8, og et motsetningsforhold om hvor scenariototalen regnes ut (AD-1/AD-3 mot AD-9). I tillegg er det noen hull i CSV-parsingen (FR-2/FR-3) og i feilhåndteringen (NFR-4).

## Sjekkliste for punktene som ble bedt om

| Punkt | Status | Merknad |
|---|---|---|
| H6.1 total WAPE fra summer | OK | `backtest_metrikk.sum_avvik`, `sum_faktisk`, `antall_treff`, `antall_punkt` (AD-3), totaler i AD-4 |
| H6.2 verdier per opprinnelse | OK | `backtest_punkt` med modell, opprinnelse, maaned, faktisk, p10, p50, p90 (+ avvik, i_spenn) |
| H6.3 oppsummering for WAPE-oversikten | OK | `datasett.sammendrag` i `GET /api/datasets/{id}` |
| H6.4 rapporten lagres i sin helhet | OK, se M-6/L-5 | `datasett.rapport` (AD-8) med advarsler, `per_nivaa`, `antall_kort_historikk` |
| H6.5 `sesongnaiv` i stedet for `baseline` | OK | AD-6, egen setning i kapabilitetskartet |
| FR-3 duplikat med begge radnumre | OK | `feil[].rader[]`. Se L-3 om tre eller flere like rader |
| FR-4 advarsel lister måneder | OK | `advarsler[].maaneder[]`, én per produkt |
| FR-5/FR-16 grenser | OK | AD-6 stemmer med begge tabellene og alle grensetestene (11/12, 17/18, 23/24, 29/30) |
| FR-12 scenariototal | Avvik | Se H-2 |
| FR-14/15/22 mengden S | OK | AD-4 = «backtest for begge modellene og definert WAPE» |
| FR-18 rapport ved gjenåpning | OK | Se L-5 om «byte-identisk» |
| FR-19 sortering | OK | AD-7 følger de tre gruppene og produkt_id ved like verdier. Se L-7 |
| FR-21 detaljtabell | OK | `punkter[]` gir faktisk og P50 (og P10/P90, så dekningen også kan regnes etter) |
| FR-25 | OK | Samme pipeline og samme skrivefunksjon. Se L-9 |
| NFR-1 | OK, se M-4 | AD-11 |
| NFR-7 | Delvis | Se M-4 og L-1 |
| NFR-9 | OK, se L-8 | |
| F11 | OK | Alt lagres, ingenting regnes ut ved lesing |
| F13 | OK, se L-4 | |

## Funn

### H-1 (høy) Heltallsavrunding er en tolkning som ikke står i PRD-en, og den kan felle FR-24 og påvirke F8

- **Kilde:** PRD §3 (*P10 / P50 / P90*: «Ingen verdi er under 0»), FR-9, FR-14 (WAPE = Σ|faktisk − P50| / Σ faktisk), FR-15, FR-24 siste konsekvens («P50 fra ETS innenfor 5 % av fasiten i hver måned»), addendum («Nullgrense `max(0, ·)` … etter modellkjøringen»). PRD-en sier ingenting om avrunding.
- **Spine:** AD-5 (`rund(max(0, x))`, «Etter dette steget finnes bare heltall», WAPE og dekning regnes bare fra heltallene). Konvensjonen *Tall*.
- **Problem:** (c) Spinen har innført en ny regel som endrer tallene i akseptansekriteriene. (1) FR-24-testen: for et støyfritt produkt med lavt volum (f.eks. fasit 8 per måned) gir avrundingen alene opptil 0,5 / 8 ≈ 6 % avvik, og testen feiler selv om modellen er perfekt. (2) F8/SM-2: avrunding av P10 og P90 kan gjøre intervallene smalere eller bredere for produkter med lavt volum (P10 = P50 = P90 er mulig), og det flytter total dekning. Det kommer i tillegg til spørsmålet som allerede er utsatt om at ETS-intervallene er for smale. (3) Regelen er ikke ført inn i PRD §11 eller i beslutningsloggen, så den har lavere rang enn kildene etter spinens egen konfliktrekkefølge.
- **Forslag:** Velg én av to: (a) Behold avrundingen, men før den inn som tolkning i PRD §11.2 (eller beslutningsloggen), og presiser FR-24 slik at 5 %-testen gjøres på urundet P50 fra kjernen (eller at det støyfrie produktet har volum ≥ 100). Kjør spiken for F8 med avrunding slått på. (b) Lagre urundede verdier og la frontend avrunde bare til visning. Da må NFR-5-fasiten regnes på urundede tall, og detaljtabellen viser desimaler. Alternativ (a) passer best med NFR-5.

### H-2 (høy) Scenariototalen har ingen eier i datamodellen

- **Kilde:** FR-12 (scenariototal = sum av månedlige verdier), FR-21, NFR-5.
- **Spine:** AD-1 («Bare `domene/` … regner ut … scenariototaler»), AD-3 (listen over hva som lagres nevner ikke scenariototal), AD-9 (`GET …/products/{produkt_id}` returnerer `scenariototal{p10, p50, p90} | null`), ER-diagrammet (ingen kolonne).
- **Problem:** (b) Det står ikke hvor `scenariototal` kommer fra. Den er ikke lagret, og hvis API-et summerer `prognose`-radene, bryter det AD-1 og AD-3 («Lesere regner aldri på nytt», «Ingen SQL-`SUM`»). To utviklere vil løse dette forskjellig: en med SQL-`SUM`, en med en kolonne og en i frontend.
- **Forslag:** Legg `scenariototal_p10`, `scenariototal_p50` og `scenariototal_p90` (heltall, `NULL` når `prognosemodell` er `null`) på `produkt`, og før dem opp i AD-3. Alternativt kan det stå i AD-3 at API-et kaller en ren funksjon `domene.scenario.totaler()`. Den første løsningen er mest i tråd med AD-3.

### M-1 (middels) FR-2 og FR-3 kolliderer når en påkrevd kolonne mangler, og spinen avgjør ikke hvilken feil som vinner

- **Kilde:** FR-2 («Hvis verken komma eller semikolon gir de tre påkrevde kolonnene, avvises fila med en feil»), FR-3 («En manglende påkrevd kolonne gir en feil som nevner kolonnen ved navn»), F4.
- **Spine:** AD-8 (bare formen på `feil[]`), kapabilitetskartet (`domene/csv.py`).
- **Problem:** (b) En fil som mangler `antall`, gir per definisjon ingen skilletegn med tre påkrevde kolonner. Etter FR-2 blir det en skilletegnfeil, men F4 og FR-3 krever en feil som nevner `antall`. Uten en regel får testen for F4 feil melding.
- **Forslag:** Fastsett i AD-8 (eller en ny regel for `csv.py`): velg skilletegnet som gir flest påkrevde kolonner (ved likt antall går semikolon foran, eller komma, men det må fastsettes). Hvis minst én påkrevd kolonne finnes, rapporteres de manglende kolonnene ved navn (kode `mangler_kolonne`). Skilletegnfeilen gis bare når ingen påkrevd kolonne gjenkjennes med noen av tegnene.

### M-2 (middels) Rader med feil antall felt er ikke håndtert: stille feiltolkning eller 500

- **Kilde:** FR-2 (eksempelet med `12,5`), FR-3 («alle feilene», radnummer), FR-1 (ekstra kolonner ignoreres).
- **Spine:** AD-8, konvensjonen *Feil* («Uventede unntak … gir `500`»).
- **Problem:** (b) I en kommafil blir `P-1,2025-03,12,5` til fire felt. Med `pandas.read_csv` gir det enten `ParserError` (→ 500, ikke en feil i rapporten) eller, hvis alle rader har fire felt, en stille forskyvning der `12` blir antall. Regelen om at ekstra *kolonner* ignoreres, gjelder kolonner i overskriften, ikke ekstra felt i én rad.
- **Forslag:** Legg til en valideringsregel: en datarad med et annet antall felt enn overskriften gir feil med radnummer (f.eks. «Rad {r}: har {k} felt, overskriften har {n}»). Les fila med `csv`-modulen linje for linje (ikke pandas), slik at radnummeret alltid er linjenummeret i fila (FR-3), også når det finnes tomme linjer. Legg malen inn i EXPERIENCE.md.

### M-3 (middels) FastAPI sine egne feilsvar er engelske og bruker samme statuskode som en avvist fil

- **Kilde:** NFR-4 (ingen engelske brukertekster, feilmeldinger på norsk), FR-3, FR-18.
- **Spine:** AD-9 (`422 {rapport}` når status er `avvist`, «GET-feil (404) gir `{detail}` med norsk tekst»).
- **Problem:** (b) En opplasting uten feltet `fil`, med tomt filnavn eller med feil content-type gir FastAPIs `RequestValidationError`: `422 {detail: [...]}` på engelsk. Frontend-zod forventer `{rapport}` på 422 og feiler i parsingen. Ukjente ruter gir `404 {"detail": "Not Found"}`, og en `id` som ikke er et tall gir 422 på engelsk.
- **Forslag:** I AD-9: registrer en egen handler for `RequestValidationError` og `StarletteHTTPException` som gir norsk tekst. For `POST /api/datasets` skal en manglende eller tom fil gi `422 {rapport}` med status `avvist` og feilen «Fila er tom» eller en tilsvarende mal. Lag en kontrakttest for dette.

### M-4 (middels) Numba-cache: addendum krever `cache=True`, men spinen forbyr miljøvariabler og utsetter alt om kaldstart

- **Kilde:** Addendum, NFR-7-raden («Kompileringen bufres (`cache=True`), og tidtakingen gjøres etter én oppvarmingskjøring. Kaldstart måles og rapporteres»). NFR-1 (ingen miljøvariabler).
- **Spine:** AD-11 («Ingen kode leser miljøvariabler»), AD-10/AD-11 (klienten gir opp etter 120 s), Deferred (*Kaldstart av numba*).
- **Problem:** (a/b) statsforecast slår på numba-cache med en miljøvariabel (`NIXTLA_NUMBA_CACHE`). Spinen nevner ikke cachen, og regelen om miljøvariabler blir lett lest som et forbud mot å bruke den. Uten diskcache kompileres numba på nytt etter hver omstart. Første opplasting etter omstart av en database som ikke er tom, kan da nærme seg eller passere klientgrensen på 120 s med 200 × 36, og Kari får en feil mens datasettet likevel lagres (se L-1). At addendumet sier at kaldstart skal *måles og rapporteres*, står heller ikke i spinen.
- **Forslag:** Legg til i AD-10 eller AD-11: `prognos/konstanter.py` (eller `main.py`) setter `os.environ.setdefault("NIXTLA_NUMBA_CACHE", "1")` før statsforecast importeres, og det er lov fordi brukeren ikke trenger å sette noe. Presiser at «ingen miljøvariabler» betyr at ingen må settes av brukeren. Ta med i NFR-7-testen at kaldstarttiden logges og skrives i README. Kontroller navnet på variabelen mot statsforecast 2.1.1.

### M-5 (middels) FR-10: «sesongnaiv baseline beregnes også» er tolket som bare backtest, uten at det står

- **Kilde:** §4.2 («sesongnaiv baseline beregnes ved siden av»), FR-10 tredje konsekvens, FR-5-tabellen («ETS, med sesongnaiv baseline ved siden av»), NFR-6 (hver testbare konsekvens skal ha en test).
- **Spine:** AD-6 («Bare `prognosemodell` sin horisontprognose lagres i `prognose`»).
- **Problem:** (c) Spinen beregner ikke den sesongnaive prognosen for horisonten for produkter på nivå *ets*. Det er forsvarlig (FR-10 utenfor omfang sier at baseline der bare brukes i backtesten), men tolkningen står ikke. Konsekvensen kan da ikke testes slik den står.
- **Forslag:** Legg til én setning i AD-6: «For nivå *ets* oppfylles ‹sesongnaiv baseline beregnes også› av baseline-backtesten (24–29 og ≥ 30 mnd). Det lagres ingen sesongnaiv horisontprognose.» Testen for FR-10 sjekker da at `backtest.sesongnaiv` ikke er `null` for alle produkter med nivå *ets*.

### M-6 (middels) Formen på rapporten er ikke fastsatt for avvist, feilet og 409

- **Kilde:** §3 *Valideringsrapport* (status, feil, advarsler, antall per nivå), FR-3, FR-7 («valideringsrapporten viser en feilmelding»), FR-18.
- **Spine:** AD-8, AD-9 (`409 {rapport}`).
- **Problem:** (b) Det står ikke om `antall_produkter`, `per_nivaa` og `antall_kort_historikk` er `null` eller 0 i en avvist fil (der nivåene kanskje ikke kan regnes ut), eller hvilken `status` en 409-rapport har. Zod-skjemaet og kontrakttesten trenger svaret.
- **Forslag:** I AD-8: tellerne er `null` når `status ≠ godkjent`. Ved `feilet` og 409 er `feil[]` ett element med fast `kode` (`kjoring_feilet` eller `opplasting_pagar`) og en norsk mal fra EXPERIENCE.md. 409 bruker `status = feilet`, eller en egen verdi `opptatt`.

### L-1 (lav) Tidsavbrudd i klienten mens serveren fullfører

- **Kilde:** FR-7 (alt i én forespørsel, ingenting lagres ved feil), FR-18 (nytt datasett blir valgt).
- **Spine:** AD-10, AD-11 (klienten gir opp etter 120 s, proxyen etter 130 s).
- **Problem:** Hvis klienten gir opp, fortsetter `run_in_threadpool` og committer. Kari ser en feil, men et nytt datasett dukker opp i velgeren.
- **Forslag:** Skriv at dette er akseptert, og at frontend invaliderer `['datasett']` også etter tidsavbrudd. Eventuelt kan skallet hoppe over commit hvis forespørselen er koblet fra (`request.is_disconnected()`).

### L-2 (lav) Generatoren lager ikke fila på 200 × 36 som NFR-7 trenger

- **Kilde:** NFR-7 («en generert fil av denne størrelsen»).
- **Spine:** Strukturen (`testdata/generator.py` skriver bare `syntetisk.csv` og `fasit.json`).
- **Forslag:** Gi generatoren et parameter for antall produkter (standard = FR-24-innholdet), eller la tidtakingstesten lage fila selv i `tmp_path`. Fila skal ikke sjekkes inn.

### L-3 (lav) Duplikat med tre eller flere like rader

- **Kilde:** FR-3 («begge radnumrene»), EXPERIENCE-malen «(rad {r1} og {r2})».
- **Spine:** AD-8 (`rader[]`).
- **Forslag:** Fastsett at `rader[]` inneholder alle linjene med samme (`produkt_id`, `maaned`), og at meldingen lister alle («rad 17, 90 og 233»). Alternativt gis én feil per par. Oppdater malen.

### L-4 (lav) F13 og skilletegnet

- **Kilde:** FR-2 (identisk resultat, «Filnavn og tidspunkt er unntatt»), F13.
- **Spine:** AD-1 («samme CSV-innhold gir identisk `Kjoreresultat`»), `datasett.skilletegn`.
- **Problem:** Innholdet er ikke byte-likt i F13, og `skilletegn` er et felt som er ulikt i de to datasettene, men PRD-en unntar bare filnavn og tidspunkt.
- **Forslag:** Skriv i AD-1 «samme tolkede innhold». Si at F13-testen sammenligner alt unntatt `id`, `filnavn`, `opplastet` og `skilletegn`, og at `skilletegn` er metadata, ikke resultat.

### L-5 (lav) «Byte-identisk» rapport

- **Spine:** AD-8 («returneres byte-identisk av `GET /api/datasets/{id}`»).
- **Problem:** POST serialiserer en Pydantic-modell, og GET leser JSON fra SQLite. Byte-likhet krever at begge går gjennom samme serialisering. Kravet (FR-18, F11) er likt innhold.
- **Forslag:** Endre til «lagres som `rapport.model_dump(mode='json')` og valideres tilbake til `Valideringsrapport` ved lesing, slik at svaret er likt i innhold». Eller behold kravet, men skriv at begge veier bruker samme `model_dump_json`.

### L-6 (lav) CSV som ikke er UTF-8

- **Kilde:** FR-1 («Fila leses som UTF-8, med eller uten BOM»), UJ-1 (norsk Excel, som ofte lagrer i Windows-1252).
- **Spine:** Ikke nevnt. `UnicodeDecodeError` blir et uventet unntak og gir 500.
- **Forslag:** Ta med i valideringen: en fil som ikke kan dekodes som UTF-8, gir feilen «Fila er ikke lagret som UTF-8» i rapporten (status `avvist`). BOM fjernes med `utf-8-sig`.

### L-7 (lav) Definisjonen av «flagget» og sammenligningen av WAPE i AD-7

- **Kilde:** §3 *Flagg*, FR-17 («strengt høyere»), FR-19.
- **Spine:** AD-7.
- **Problem:** AD-7 sier ikke at «flagget» betyr `flagg_kort_historikk ∨ flagg_ets_taper`. Den sier heller ikke at `ets_slaar`/`ets_taper` avgjøres ved å sammenligne flyttall. Fordi `sum_faktisk` er lik for begge modellene, er det sikrere å sammenligne heltallene `sum_avvik`. Rekkefølgen etter `produkt_id` (kodepunkt eller locale) er heller ikke fastsatt.
- **Forslag:** Skriv tre ting i AD-7: flagget = minst ett flagg; dommer avgjøres ved å sammenligne `sum_avvik[ets]` med `sum_avvik[sesongnaiv]` (heltall); `produkt_id` sorteres etter Python-strengsortering (kodepunkt).

### L-8 (lav) NFR-9: `.env.example` og test-databaser

- **Kilde:** NFR-9 (`.env.example` finnes, `git ls-files` lister ingen `.db`).
- **Spine:** Konvensjonen *Konfigurasjon* nevner `.env.example`, men strukturen viser den ikke. Skalltestene bruker «en midlertidig SQLite-fil».
- **Forslag:** Ta med `.env.example` i rottreet. Skriv at testdatabasen ligger i pytest `tmp_path`, og at `.gitignore` ignorerer `*.db` globalt, ikke bare `backend/data/`.

### L-9 (lav) FR-25: hva skjer hvis seed feiler

- **Kilde:** FR-25, NFR-2 (`/api/health` svarer OK etter første oppstart).
- **Spine:** AD-2, AD-13.
- **Problem:** Hvis `syntetisk.csv` mangler eller pipelinen feiler, står det ikke om backend stopper eller starter uten data.
- **Forslag:** Fastsett at en feil i seed logges med stakk og stopper oppstarten med en norsk melding (slik som versjonsvakten i AD-13). Det gjør feilen synlig for sensor. Det motsatte valget er også greit, men da må det stå.

## Det som ble sjekket uten funn

FR-1 (ekstra kolonner), FR-6 (ny opplasting gir nytt datasett, autoinkrementert id), FR-7 (én forespørsel, alt eller ingenting), FR-8/F3 (produkter på nivå *ingen* står i `produkt` og i listen), FR-9 (`level=[80]`, F2 etter avrunding), FR-11, FR-13 (h=1, n_windows=6, step_size=1, historikk til og med opprinnelsen), FR-14 (WAPE `NULL` ved Σ faktisk = 0, utenfor S, aldri *ETS taper*), FR-15 (total dekning over S), FR-17, FR-20 (`historikk[].utfylt`, horisont), FR-21 (begge tekstene finnes ordrett i EXPERIENCE.md og eies av `tekster.ts`), FR-22 (`n`/`m`, `null` når |S| = 0), FR-26 (filtrerer i klienten og beholder `rang`), NFR-2, NFR-8 (ingen autentisering), ordrett merknad i FR-12 (identisk i EXPERIENCE.md), addendum *Kjøring uten nett* (telemetri i `predev`, systemfonter, ingen feature flags). Det som er utsatt under Deferred, er ikke farlig, bortsett fra kaldstartspunktet, som henger sammen med M-4.
