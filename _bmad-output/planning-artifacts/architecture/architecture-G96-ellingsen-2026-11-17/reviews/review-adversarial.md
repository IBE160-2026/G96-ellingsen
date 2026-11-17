---
type: review
lens: adversarial (par av enheter som følger alle AD-er bokstavelig, men bygger inkompatibelt)
target: ../ARCHITECTURE-SPINE.md
created: '2026-11-17'
---

# Adversarial review: ARCHITECTURE-SPINE.md (PROGNOS v1)

## Dom

**Ikke klar som byggesubstrat ennå.** Spinen er sterk på de store linjene (ren kjerne, alt-eller-ingenting, metrikker lagres én gang, én eier av grensene). Hullene ligger ett nivå ned: i grensesnittet mot statsforecast (datoer, NaN, kallgruppering), i hvilke felt som faktisk lagres (scenariototal, historikklengde, `utfylt`), i HTTP-feilformen (422/409/500), i tid (UTC, tidsavbrudd) og i CSV-parsingen (radnummer, heltall, `produkt_id`). 3 funn er kritiske og 9 er høye. Alle kan lukkes med korte regler. Ingen av dem krever at paradigmet endres.

Enhetene i parene: **A** `domene/` (modeller, backtest, metrikker), **A2** `domene/csv.py` + `validering.py`, **B** `db/`, **C** `api/` + `skjema.py`, **D** frontend (tabeller, format, klient), **E** `testdata/generator.py`, **F** `oppstart.py` (seed).

Funnene står i alvorlighetsrekkefølge. Hvert funn har et par som bygger inkompatibelt, konsekvensen og en regel som foreslås.

---

## Kritisk

### K1. NaN fra SeasonalNaive ved nøyaktig 12 treningspunkter, og to tolkninger av `rund(max(0, x))`

- **Par:** A1 bruker Python `max(0, x)` per verdi. A2 (eller en refaktorering) bruker `np.maximum(0, arr)` og `np.floor(arr + 0.5).astype(int)`.
- **Hull:** SeasonalNaive regner intervallet fra residualene `y_t − y_{t−12}`. Med nøyaktig 12 treningspunkter finnes det ingen residualer, så sigma og P10/P90 blir trolig `NaN`. Dette rammer to tilfeller spinen selv krever: prognosen ved historikklengde 12 (grensetest i FR-5) og første opprinnelse i backtesten ved historikklengde 18 (grensetest i FR-16, der treningslengden er 18 − 6 = 12). Python `max(0, nan)` gir `0`, fordi `nan > 0` er usant. `np.maximum(0, nan)` gir `nan`, og `int(nan)` kaster et unntak. Samme AD-5 gir dermed P10 = 0 hos A1 og kjøringsfeil hos A2. Hvis NaN slipper gjennom til API-et, serialiserer Pydantic v2 den stille som `null`, og da bryter den AD-5 og konvensjonen om at `null` betyr udefinert. `i_spenn` med NaN gir `False` og senker dekningen uten at noen merker det.
- **Forslag til regel (AD-5, nytt ledd):**
  > Før nullgrensen konverteres all modellutdata til `float64`, og hver verdi sjekkes med `math.isfinite`. En verdi som ikke er endelig (NaN eller ±inf), er en `Modellfeil` i `domene/feil.py` og gir status `feilet`. Den settes aldri til 0. `rund` er implementert én gang, i `domene/avrunding.py`, som `int(math.floor(x + 0.5))` på Python-`float`, og ingen annen kode avrunder. Det finnes en spike-test som kjører SeasonalNaive med `level=[80]` på serier med 12 og 13 punkter. Hvis 12 punkter gir NaN, endres grensene i `nivaa.py` (sesongnaiv prognose fra 13, baseline-backtest fra 19). Ellers legges et dokumentert unntak inn i AD-6 før F5 og FR-16 testes.

  Kanskje må dette tilbake til PRD-en: grensene 12 og 18 forutsetter at et intervall finnes med 12 treningspunkter.

### K2. Månedsaritmetikk mot statsforecast: `ds`, `freq`, `cutoff`

- **Par:** A (modeller.py) bygger `ds` som `pd.Timestamp('2026-10-01')` med `freq='M'` eller `'ME'` (månedsslutt). A' (backtest.py) bruker `freq='MS'`, slik spiken gjør. E og B kjenner bare `ÅÅÅÅ-MM`.
- **Hull:** Med `ds` = første dag i måneden og `freq='ME'` blir første prognosedato `2026-10-31`, som formateres som `2026-10`. Det er den siste historiske måneden, og prognosen forskyves én måned. I `cross_validation` heter opprinnelsen `cutoff`, og AD-en sier ikke hvordan `cutoff` og `ds` oversettes til `opprinnelse` og `maaned`, eller hvem som gjør det. Spiken (`spikes/backtest_spike.py`) bruker `freq="MS"`, men det står ikke i spinen.
- **Forslag til regel (ny AD-14 «Måneder inn og ut av modellen»):**
  > Kun `domene/maaned.py` konverterer mellom `ÅÅÅÅ-MM` og modellens tidsakse. Kjernen bruker en heltallsindeks `ds = år*12 + (måned−1)` og `freq=1`. Den bruker ikke pandas-datoer. `maaned.py` har `til_indeks`, `fra_indeks` og `pluss(maaned, n)`, og ingen annen kode regner med måneder. I backtesten er `opprinnelse = fra_indeks(cutoff)` og `maaned = fra_indeks(ds)`. Det sjekkes at `maaned == pluss(opprinnelse, 1)` for hver rad. Prognosemånedene er nøyaktig `pluss(siste_maaned, 1..6)`. År utenfor 1900–2999 er en valideringsfeil.

  Heltallsindeksen fjerner også `pandas.Timestamp`-grensen (1677–2262), som ellers gir `500` for `0001-01`.

### K3. Kallgruppering og ulik serielengde i samme statsforecast-kall

- **Par:** A1 kjører `cross_validation` én gang med begge modellene for alle produkter med lengde ≥ 18, og kaster ETS-radene for lengde < 30 (slik spiken gjør, der alle seriene har lengde 36). A2 kjører ett kall per modell på hver sin produktmengde.
- **Hull:** Hos A1 trener AutoETS på 12–23 punkter. Den kan da velge en ikke-sesongmodell, feile eller bruke mye tid (NFR-7). Det gjør også at resultatet avhenger av hvilke *andre* produkter som er med, hvis en feil i ett produkt stopper hele kallet. Utdataene blir ikke sammenlignbare med A2. Spinen sier heller ikke noe om `n_jobs`, `fallback_model`, rekkefølgen på utdata eller at alle seriene må slutte på `siste_maaned` for at opprinnelsene skal være de samme. `n_jobs=-1` på Windows starter `multiprocessing` med spawn inne i uvicorn sin trådpool. `fallback_model=SeasonalNaive()` gir `prognosemodell = ets` med sesongnaive tall.
- **Forslag til regel (AD-6, nytt ledd):**
  > Modellkall grupperes per modell og per mengde etter tabellen. Det er ett `forecast`-kall per modell med produktene som har den som `prognosemodell`, og ett `cross_validation`-kall per modell med produktene som skal backtestes med den. Ingen modell får se et produkt utenfor sin mengde. Før kallet sjekkes det at hver serie slutter på `siste_maaned` og ikke har hull. Etter kallet sjekkes det at radtallet er nøyaktig 6 × |mengde|, og utdata kobles på (`unique_id`, `ds`), aldri på posisjon. `StatsForecast(n_jobs=1)`, ingen `fallback_model`, og modellene har `alias='ets'` og `alias='sesongnaiv'`, slik at kolonnene heter `ets`, `ets-lo-80` og `ets-hi-80`. `unique_id` er `produkt_id` som `str`.

---

## Høy

### H1. `n` og `m` når |S| = 0: «alle totalene er `null`»

- **Par:** A leser AD-4 «alle totalene er `null`» og setter `m = null`, `n = null`. D følger EXPERIENCE.md, der malen gjelder «Når m = 0», og sjekker `m === 0`. Da faller D gjennom til hovedmalen med `null %`.
- **Forslag (AD-4):**
  > `n` og `m` er alltid heltall ≥ 0, og |S| = 0 gir `m = 0` og `n = 0`. Bare `total_wape[*]` og `total_dekning[*]` blir `null` når |S| = 0. Frontend velger m = 0-malen på `m === 0`.

### H2. Scenariototal, historikklengde og `utfylt` har ingen eier i lagringen

- **Par:** AD-3 lister det som lagres, men `scenariototal`, `historikklengde` og `historikk[].utfylt` er ikke med, selv om AD-9 returnerer dem. B lagrer ikke `scenariototal`, og C summerer `prognose` i API-laget. Det bryter AD-1, fordi bare `domene/` regner scenariototaler, og AD-3, fordi lesere aldri regner på nytt. Alternativt lagrer B bare de opprinnelige CSV-radene i `salg`, og C fyller ut på nytt ved lesing. Da finnes utfyllingen to steder.
- **Forslag (AD-3, utvid listen):**
  > Kjernen lagrer også `produkt.historikklengde`, `produkt.historikknivaa`, `produkt.prognosemodell`, `produkt.scenario_p10`, `scenario_p50` og `scenario_p90`. Alle tre er `NULL` når produktet ikke har prognose. `salg` lagrer serien **etter** utfylling, én rad per måned fra første måned til `siste_maaned`, med `utfylt: bool`. API-et henter `historikk[]` bare fra `salg` og `scenariototal` bare fra disse kolonnene.

### H3. Klienten gir opp etter 120 s, men backend committer likevel

- **Par:** D viser «Kjøringen tok mer enn to minutter og ble stoppet» og «Ingenting er lagret» etter 120 s. C (AD-10) kjører pipelinen videre i trådpoolen og committer etter 140 s. Datasettet dukker da opp i velgeren, og låsen er holdt mens Kari prøver igjen og får `409`.
- **Forslag (AD-10, nytt ledd):**
  > Ruten måler tiden fra mottak. Hvis det har gått mer enn `MAKS_KJORETID_S = 110` sekunder når pipelinen returnerer, skrives ingenting, og svaret er `500` med status `feilet` og meldingen for tidsavbrudd. Det er altså ingen commit etter fristen. Låsen frigjøres alltid i `finally`. Klientens grense (120 s) og `proxyTimeout` (130 s) ligger over denne fristen.

### H4. FastAPIs egne 422-svar kolliderer med `422 {rapport}`

- **Par:** C deklarerer `fil: UploadFile`. Når feltet mangler eller er tomt, svarer FastAPI `422 {detail: [...]}` på engelsk. D sin zod-parser forventer `{rapport}` ved 422, parseren kaster, og Kari ser en generisk feil. Det samme gjelder `GET /api/datasets/abc` (`{detail: [...]}` med engelsk tekst, ikke norsk 404). Generelt kan den samme statuskoden ha to former.
- **Forslag (AD-9, nytt ledd):**
  > Hver statuskode har nøyaktig én form per endepunkt. Det registreres en `RequestValidationError`-handler. For `POST /api/datasets` gir den `422 {rapport}` med status `avvist` og feilen «Fila har ingen datarader» når feltet `fil` mangler eller er tomt. For GET gir den `404 {detail}` med norsk tekst. Uventede unntak gir `500 {rapport}` med status `feilet` for POST og `500 {detail}` for GET. Kontrakttesten dekker alle disse kombinasjonene av status og form.

### H5. `opplastet` mister `Z` gjennom SQLite

- **Par:** B bruker `DateTime` og `datetime.now(timezone.utc)`. SQLite lagrer uten tidssone og leser tilbake et naivt tidspunkt. C serialiserer det som `2026-11-13T08:42:00` uten `Z`. D gjør `new Date(...)`, som tolker strengen som lokal tid, og viser 08.42 i stedet for 09.42. POST og GET kan også gi ulik streng for samme datasett.
- **Forslag (konvensjon *Tidspunkt*):**
  > `opplastet` lagres som `TEXT` på formen `ÅÅÅÅ-MM-DDTHH:MM:SSZ`. Den lages én gang i skallet med `datetime.now(timezone.utc).strftime(...)`, uten mikrosekunder, og sendes uendret. Pydantic-feltet er `str` med regex. zod sjekker at strengen slutter på `Z`.

### H6. Radnummer og blanke linjer i CSV-parsingen

- **Par:** A2 bruker `pandas.read_csv`. Der er `skip_blank_lines=True`, `produkt_id` får automatisk type (`"001"` blir `1`, og `"001"` og `"01"` blir duplikater), og `"12.0"` godtas som heltall. Radnummeret blir `index + 2`, som er feil etter en blank linje. A2' bruker `csv.reader` og `reader.line_num`. Python `int()` godtar også `" 12"`, `"+5"` og `"1_000"`. Generatoren (E) skriver `\r\n` eller `\n` avhengig av OS, og en tom siste linje er vanlig fra Excel.
- **Forslag (ny AD-15 «CSV-leseren»):**
  > `domene/csv.py` bruker `csv.reader` på tekst dekodet som `utf-8-sig`, aldri pandas. Radnummer er `reader.line_num` for raden. Linjer der alle cellene er tomme, hoppes over, men telles med. Overskriftene sammenlignes etter `strip()` og skiller mellom store og små bokstaver. Alle verdier leses som `str`. `produkt_id` er `strip()`-et og ellers uendret. `antall` er gyldig bare når `^[0-9]+$` matcher etter `strip()`. `maaned` må matche `^\d{4}-(0[1-9]|1[0-2])$`. En fil som ikke kan dekodes som UTF-8, avvises (status `avvist`) med koden `tegnkoding` og en tekst som EXPERIENCE.md må fastsette.

  Uten en `strip()`-regel blir `" P-1"` og `"P-1"` to produkter. Det følger av «uendret» i konvensjonen *Id-er*.

### H7. `produkt_id` i URL-stien

- **Par:** D bygger `/api/datasets/3/products/${produkt_id}`. C har `{produkt_id}` som stiparameter. En `produkt_id` som `A/B`, `P#1`, `50%` eller `P 1` (lovlig i CSV) gir 404 eller feil produkt. D bruker `encodeURIComponent`, men Next-rewriten kan dekode `%2F` før den sender videre, og Starlette matcher ikke `/` i en vanlig parameter.
- **Forslag (AD-9):**
  > Ruten er `/api/datasets/{id}/products/{produkt_id:path}`, og klienten bruker alltid `encodeURIComponent(produkt_id)`. En e2e-test bruker produkt-id-ene `A/B`, `P 1`, `50%` og `Æ-1`. Hvis rewriten viser seg å ødelegge `%2F`, legges det i stedet til en valideringsregel om at `produkt_id` ikke kan inneholde `/`, `?`, `#` eller `%`, med en fast tekst i EXPERIENCE.md.

### H8. Hvem bygger den endelige `Valideringsrapport`?

- **Par:** A2 (`validering.py`) bygger rapporten med `per_nivaa` = 0 fordi nivåene ikke er klassifisert ennå. `utfylling.py` lager advarslene. `nivaa.py` teller nivåene. Pipelinen setter sammen? Ingen AD sier hvem som eier objektet. For avviste filer er det også uklart om `antall_produkter` skal være `0` eller `null`, og om advarslene skal være med. D viser da enten «0 produkter» eller ingenting.
- **Forslag (AD-8):**
  > Bare `domene/pipeline.py` konstruerer `Valideringsrapport`. Valideringen returnerer `feil[]`, utfyllingen returnerer `advarsler[]`, og nivåklassifiseringen returnerer tellingene. Ved `avvist` og `feilet` er `antall_produkter`, `per_nivaa` og `antall_kort_historikk` `null`, og `advarsler` er `[]`. Ved `feilet` har `feil[]` nøyaktig ett element med `kode = "kjoring_feilet"` og `rader = []`. `feil[]` sorteres slik: feil på filnivå (`rader = []`) først, deretter etter minste radnummer og så etter `kode`. `advarsler[]` sorteres etter `produkt_id`, og `maaneder[]` stigende. Kodene er en lukket enum i `domene/feil.py`.

### H9. Detaljtabellen: «Måned» er opprinnelse eller målmåned, og hvordan radene kobles

- **Par:** EXPERIENCE.md sier «Én rad per opprinnelse» med kolonnen *Måned*. D1 viser `opprinnelse`. D2 viser `maaned`. Faktisk verdi hører til `maaned`, og D1 viser dermed hver faktisk verdi én måned for tidlig. D kobler også baseline- og ETS-punkter på indeks, mens A returnerer `punkter` i rekkefølgen fra statsforecast.
- **Forslag (konvensjon *Måneder* + AD-9):**
  > Alle lister i API-et (`historikk`, `prognose` og `punkter`) er sortert stigende på `maaned`. I detaljtabellen er kolonnen *Måned* `maaned` (måneden det prognoseres for). `opprinnelse` vises ikke. Baseline og ETS kobles på `maaned`. Sumraden bruker `metrikk.sum_faktisk` og `metrikk.sum_avvik`, ikke summer regnet i TS. Historikktabellen snur rekkefølgen («nyeste øverst»). Det er den eneste omsorteringen i frontend.

---

## Middels

### M1. 409 har ingen gyldig status i rapporten

`409 {rapport}` krever en `status` ∈ {`godkjent`, `avvist`, `feilet`}. C velger `feilet`, og D viser «Prognosen kunne ikke kjøres. Ingenting er lagret.», som er misvisende. EXPERIENCE.md har ingen tekst for dette.
> **Regel:** 409 gir `{rapport}` med status `feilet`, `feil = [{kode: "opptatt", melding: <tekst fra EXPERIENCE.md>, rader: []}]`. Teksten legges inn i EXPERIENCE.md *Faste tekster* før frontend bygges.

### M2. Versjonsvakten slipper gjennom gamle databaser

`create_all` lager tabellen `skjemaversjon` tom i en gammel fil som ikke hadde den. B tolker en tom tabell som «ny database» og setter inn versjonen, og den gamle `produkt`-tabellen (som `create_all` ikke endrer) blir godtatt.
> **Regel:** Vakten kjører **før** `create_all`. Hvis fila har tabeller, men `skjemaversjon` mangler eller har en annen verdi, stopper backend. Bare en fil uten tabeller blir initialisert og får `SKJEMAVERSJON` satt inn i samme transaksjon som `create_all`.

### M3. Frontend gjenskaper grensene 18 og 30

D velger mellom «Ingen backtest (under 18 …)» og «ETS er ikke backtestet (under 30 …)» med `historikklengde < 30` i TS. Da finnes en ny kilde for grensene, i strid med intensjonen i AD-6.
> **Regel:** Frontend velger tilstander bare ut fra `historikknivaa`, om `backtest.*` er `null` og om `dommer` er `null`. Den sammenligner aldri `historikklengde` med et tall. «(6)» i knappeteksten er `punkter.length`.

### M4. `backtest_metrikk` for produkter uten backtest

B skriver rader med `antall_punkt = 0` og `wape = NULL` for alle produkter. C returnerer da `{metrikk, punkter: []}` i stedet for `null`, og D viser en tom tabell med dekning `NaN`.
> **Regel:** En `backtest_metrikk`-rad finnes bare når modellen er backtestet, og da er `antall_punkt = 6` (en invariant som sjekkes i kjernen). Når raden mangler, er `backtest.<modell>` `null`.

### M5. Dommer sammenlignes med flyttall eller med viste verdier

`dommer` regnes ved å sammenligne `wape_ets` og `wape_sesongnaiv` som flyttall. Det går greit fordi nevneren er den samme, men regelen er implisitt. En annen utvikler kan sammenligne tall som er avrundet til én desimal, eller bruke en toleranse. Da kan «lik» i A bli «slår» i D.
> **Regel:** `dommer` avgjøres med heltall: `sum_avvik_ets < sum_avvik_sesongnaiv` gir `ets_slaar`, `>` gir `ets_taper` og `=` gir `lik`. Dette gjelder bare når `sum_faktisk > 0`. Det brukes aldri toleranse. Når `dommer` er `null`, er det JSON `null`, ikke strengen `"null"`.

### M6. Prosentformatering: `x*100` mot Intl

D1 gjør `(wape*100).toFixed(1)`. `0.0745*100` gir `7.449999…`, som vises som «7,4 %», mens Kari regner ut 7,45 og runder til 7,5. D2 bruker `Intl` med `style: 'percent'`, som skalerer eksakt.
> **Regel (konvensjon *Tall*):** `format.ts` formaterer WAPE og dekning bare med `Intl.NumberFormat('nb-NO', {style: 'percent', minimumFractionDigits: 1, maximumFractionDigits: 1})` (dekning med 0 desimaler) på brøken. Ingen kode ganger med 100.

### M7. Generatoren og byte-identitet på Windows

E bruker `csv.writer` med standard `\r\n`, eller `open()` uten `newline=''`. Git med `autocrlf=true` endrer `syntetisk.csv` ved checkout. F9-testen sammenligner da en ny fil med en innsjekket fil og feiler bare på noen maskiner. E kan også bruke `date.today()` som `siste_maaned` og gi en ny fil hver måned. De fire korte produktene kan slutte før `siste_maaned`, og da blir de utfylt og får en annen lengde enn 8, 15, 20 og 26.
> **Regel (ny AD «Generatoren»):** `generator.py` bruker `numpy.random.default_rng(42)` og en fast `SISTE_MAANED`-konstant. Alle produkter slutter på `SISTE_MAANED`, og de korte starter senere. Fila skrives med `\n`, komma, UTF-8 uten BOM, `antall = max(0, round_half_up(...))` som heltall og produktene sortert på (`produkt_id`, `maaned`). `fasit.json` skrives med `json.dumps(..., sort_keys=True, indent=2)` + `\n`. `.gitattributes` har `testdata/* -text`. Den støyfrie serien i FR-24 er en egen testfiksur i `backend/tests/`, ikke et 25. produkt i `syntetisk.csv`.

### M8. Rapporten er «byte-identisk», men inne i et større svar

B lagrer `json.dumps(rapport.model_dump())`. C returnerer den i `POST` via Pydantic og i `GET` ved å parse den lagrede strengen. Rekkefølgen på nøklene og formen på tallene kan være forskjellig, og «byte-identisk» kan ikke testes for et delobjekt.
> **Regel:** Rapporten lagres som `rapport.model_dump_json()`. `GET` validerer den tilbake til `Valideringsrapport` og serialiserer på samme måte som `POST`. Testen sjekker at `POST.rapport == GET.rapport` som parset JSON. Det samme gjelder `sammendrag`.

### M9. Konstante serier og serier med bare nuller i AutoETS

Et ekte datasett kan ha et ets-produkt (≥ 24 mnd) med bare 0 eller med samme verdi i alle månedene. AutoETS kan da feile, og etter AD-2 og FR-7 feiler hele opplastingen av 200 produkter på grunn av ett. Ingen AD sier om dette er ønsket. Den eneste naturlige reparasjonen (`fallback_model`) er stengt av K3.
> **Regel:** Dette tas med i spiken før implementeringen. Hvis AutoETS feiler på slike serier, må PRD-eieren velge mellom kjøringsfeil for hele fila (dagens regel) og en eksplisitt regel i kjernen, for eksempel at konstante serier får `prognosemodell = sesongnaiv` og en advarsel. Begge løsningene er da dokumentert i AD-6, ikke overlatt til statsforecast.

### M10. Fasittesten (NFR-5) kan ikke håndregne AutoETS

Konvensjonen *Tester* sier at fasitdatasettet er håndregnet. A skriver en ende-til-ende-test over pipelinen, og den kan ikke håndregnes fordi P50 kommer fra ETS. B skriver bare en enhetstest av `metrikker.py`.
> **Regel:** `tests/fasit/` inneholder (a) avrundede backtest-punkter som input og forventede `backtest_metrikk`, `sammendrag`, `dommer` og `rang`, og (b) prognoseverdier og forventede scenariototaler. Testen kaller `metrikker.py` og `rangering.py` direkte. Hvis den kaller pipelinen, injiseres modellsteget som en ren funksjon, slik at det kan byttes ut.

---

## Lav

### L1. Rekkefølgen i datasettvelgeren
To opplastinger i samme sekund gir lik `opplastet`. **Regel:** `GET /api/datasets` sorteres med `ORDER BY id DESC`.

### L2. Typen på spørringsnøklene
`Select` gir `id` som streng, mens `prefetchQuery` bruker et tall. Da blir `['produkt', '3', 'P-1']` og `['produkt', 3, 'P-1']` to oppføringer i cachen. `invalidateQueries(['datasett'])` treffer også `['datasett', id]` fordi nøkler matches på prefiks. **Regel:** `id` er alltid `number` i nøklene, og `klient.ts` er eneste konstruktør av nøkler. Invalidering bruker `{queryKey: ['datasett'], exact: true}`.

### L3. `flagg_*` er ikke en kontrakt
AD-9 skriver `flagg_*`. **Regel:** Feltene listes eksplisitt (`flagg_kort_historikk`, `flagg_ets_taper`). Hvilke produkter som er flagget, avgjøres i rangeringen med `flagg_kort_historikk OR flagg_ets_taper`, og det skrives i AD-7.

### L4. `prognose` for nivå *ingen*
**Regel:** `prognose = []` og `scenariototal = null`. `backtest = {sesongnaiv: null, ets: null}`. Det er aldri en manglende nøkkel.

### L5. Filnavn og seed
**Regel:** Seed-datasettet får `filnavn = "syntetisk.csv"`. Et opplastet filnavn er bare grunnnavnet etter `PurePath(...).name`, normalisert til NFC. Hvis seed-kjøringen feiler, stopper backend med en norsk melding. Den starter ikke med tom database.

### L6. Sorteringsrekkefølge for `produkt_id`
AD-1 og AD-7 sier «stigende», men ikke hvordan. **Regel:** Python `str`-sortering (kodepunkt). `P-10` kommer før `P-9`. Rekkefølgen er dokumentert og testet. Ingen naturlig sortering og ingen locale.

### L7. Søk og store/små bokstaver
**Regel:** Søket sammenligner med `toLocaleLowerCase('nb-NO')` på begge sidene, etter `trim()` av søketeksten.

---

## Sjekk etter oppretting

Når K1–K3 og H1–H9 er lukket, bør spinen gjennomgås en gang til mot spiken. Den eneste kjørbare kilden for statsforecast-oppførsel i repoet (`spikes/backtest_spike.py`) dekker bare 36-månedersserier i ett felles kall. Ingen av grensetilfellene 12, 18, 24 og 30 er kjørt.
