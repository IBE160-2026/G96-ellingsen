# Avstemming: PRD mot beslutningslogg og arkitekturutkast

Dato: 2026-11-14
Avstemt dokument: [prd.md](prd.md) og [addendum.md](addendum.md)
Kilder:
- **A:** `docs/research/research-plan.md`: beslutningsloggen (bindende) og spørsmålene om brukerbehov
- **B:** `.docs/planning-artifacts/architecture/arkitektur-utkast.md`

Rammer: bare v1. Beslutningsloggen diskuteres ikke på nytt, men PRD-en må gjengi den riktig. Appen skal kunne kjøres lokalt uten API-nøkler eller betalte tjenester. PRD-en er ikke endret.

Alvorlighetsgrader: **kritisk** (motsier en bindende beslutning, eller gjør v1 umulig å levere), **høy** (et krav kan ikke implementeres eller testes slik det står), **middels** (uklart eller ufullstendig, og vil gi ulike tolkninger), **lav** (kosmetisk, eller en anbefaling).

## Sammendrag

- Ingen kritiske funn. Alle de 15 radene i beslutningsloggen står i PRD-en eller i addendum, og ingen er gjengitt feil.
- 3 høye funn: backtest-grensen for baseline (12–17 mnd) kan ikke gjennomføres, åpent spørsmål 1 motsier motvekten SM-C1, og datamodellen og API-et kan ikke levere total WAPE eller etterprøvbarheten i NFR-5.
- Arkitekturutkastet er utdatert på to punkter som beslutningsloggen senere har avgjort (total WAPE og sortering). Addendum viser likevel til utkastet som «den fullstendige beskrivelsen».
- Spørsmålene om brukerbehov er bare delvis ført opp. ERP-eksport er med, men validering av personaen og samtalen med en planlegger mangler.

| # | Grad | Kilde | Kort |
|---|---|---|---|
| R-1 | høy | A rad 7 / B | Baseline-backtest med 6 opprinnelser er umulig for 12–17 mnd |
| R-2 | høy | A rad 7 | Åpent spørsmål 1 motsier SM-C1 |
| R-3 | høy | B datamodell/API | Total WAPE og NFR-5 kan ikke leveres av datamodellen og API-et |
| R-4 | middels | B | Utkastet er utdatert om total WAPE og sortering, men addendum peker på det |
| R-5 | middels | B | Intervalldekning: uklart hvilken modell og hvilket aggregat (F8) |
| R-6 | middels | A rad 14 / B | WAPE er udefinert når Σ faktisk = 0 |
| R-7 | middels | A rad 10 / B | Produkter som slutter før datasettets siste måned |
| R-8 | middels | A rad 3 / B | «Fra første til siste måned»: inklusive eller ikke? |
| R-9 | middels | B | Feature flags og mock-fallback: «med» i utkastet, «ikke bygd» i addendum |
| R-10 | middels | Rammer / NFR-1 | Next.js-telemetri og `next/font/google` kaller eksterne tjenester |
| R-11 | middels | A rad 10 / B | Tom fil, bare overskrift og tomme celler er ikke dekket av valideringsreglene |
| R-12 | middels | A brukerbehov | Validering av personaen og samtale med planlegger er ikke åpne spørsmål |
| R-13 | lav | A rad 12, 14 | Rekkefølgen innenfor de flaggede produktene og uavgjort WAPE er ikke definert |
| R-14 | lav | B | Hvilken modell P50 i grafen og scenarioene kommer fra, er ikke sagt for *ets*-produkter |
| R-15 | lav | PRD §11 | «Byte-identiske filer» (FR-23) og tallene i FR-24 er ikke ført som tolkninger |
| R-16 | lav | PRD UJ-2 | Eksempelet på duplikat har ikke radnummer, men teksten lover radnummer |
| R-17 | lav | B | Det syntetiske datasettet har ikke noe produkt med 24–29 mnd (FR-16) |
| R-18 | lav | B | Tekniske detaljer i hovedteksten: hører hjemme i addendum? |
| R-19 | lav | B | Advarsler og skilletegn lagres, men PRD-en sier ikke om de vises ved gjenåpning |
| R-20 | lav | A brukerbehov | Spørsmål som er besvart av beslutninger, bør merkes som besvart |
| R-21 | lav | B | `numba`-kompilering ved første kjøring kan påvirke NFR-7 |

---

## 1. Beslutningsloggen (kilde A), rad for rad

| # | Beslutning | Hvor i PRD/addendum | Gjengitt riktig? | Merknad |
|---|---|---|---|---|
| 1 | Database: SQLite | FR-6, NFR-3, F11, addendum (FR-6/NFR-2/NFR-3) | Ja | Begrunnelsen og avviket fra technology.md står i addendum. |
| 2 | Språk: norsk | NFR-4 | Ja | NFR-4 viser ikke til beslutningsloggen. Lav, se R-18. |
| 3 | Kort historikk: <12 / 12–23 / 24+ | FR-5 (tabell), FR-10, ordliste *Historikknivå*, F5 | Ja | At 12–23 mnd også flagges, kommer fra F5 og utkastet, ikke fra loggen. Det er i samsvar. Definisjonen av lengde er uklar, se R-8. |
| 4 | Prognosen kjøres automatisk | FR-7, UJ-1 trinn 3 | Ja | — |
| 5 | P10/P50/P90 ≥ 0 | FR-9, ordliste, addendum | Ja | — |
| 6 | Scenarioer for 6 mnd = sum + merknad | FR-12, FR-21 | Ja | — |
| 7 | Backtest: 6 opprinnelser, h=1, step 1, <30 mnd bare baseline. «Bekreftes i testskriptet» | §4.4, FR-13, FR-16, addendum, åpent spørsmål 1 | Delvis | Reglene er gjengitt riktig. Forbeholdet om at testskriptet skal bekrefte oppsettet er gjort om til «juster datasettet» (R-2). Grensen for baseline-backtest er ikke gjennomførbar for 12–17 mnd (R-1). |
| 8 | 80 % intervall (`level=[80]`) | FR-9, ordliste, addendum, SM-C2 | Ja | — |
| 9 | ETS taper: vis ETS, flagg, vis begge WAPE | FR-17, UJ-3 | Ja | Uavgjort er ikke definert (R-13). |
| 10 | CSV-regler | FR-2, FR-3, FR-4 | Ja | Kanttilfeller mangler (R-11, R-7). |
| 11 | Scenarionavn som hovedord | FR-11, ordliste *Scenario*, §4.3 | Ja | — |
| 12 | Dashbordet starter med listen sortert etter WAPE, med flagg | FR-19, §1 | Ja | Rad 14 presiserer rad 12, og PRD-en følger rad 14. |
| 13 | Syntetiske data med trend | FR-24 | Ja | FR-24 legger til «noen har andre mønstre» (fra SM-C1). Det er forenlig med «de fleste». |
| 14 | Sortering: flaggede øverst, deretter WAPE med høyest først | FR-19, §11 | Ja | Utkastet er utdatert (R-4). |
| 15 | Total WAPE over de samme produktene (30+ mnd) | FR-14, FR-22, §11 | Ja | Utkastet sier noe annet (R-4). Datamodellen kan ikke beregne totalen (R-3). |

### R-1 (høy): Baseline-backtest med 6 opprinnelser er umulig for 12–17 mnd

**Sted:** PRD §4.4 (tabellen: «12–29 mnd: Bare sesongnaiv baseline»), FR-16, FR-24 («ett har 12–23 måneder»). Kilde B, tabellen over historikknivåer (12–23 mnd: «Bare baseline»).

**Problem:** Sesongnaiv trenger 12 måneder trening for å prognosere måned *t* (verdien fra *t*−12). Den første av 6 opprinnelser ligger 6 måneder før slutten, så baseline-backtest med 6 opprinnelser krever minst 12 + 6 = **18 måneder**. Det er samme regnestykke som ga 30-månedersgrensen for ETS (24 + 6), men det er ikke brukt for baseline. For produkter med 12–17 mnd er backtesten udefinert. `cross_validation` vil enten feile eller gi færre vinduer, og da får produktet ingen WAPE å sortere på i FR-19. Hvis det syntetiske produktet med 12–23 mnd får under 18 mnd, feiler testene.

Beslutningsloggen (rad 7) sier bare at produkter under 30 mnd får baseline-backtest. Den tar ikke stilling til produkter under 18 mnd. Dette er derfor et hull i loggen, ikke en motsigelse mot den.

**Forslag:** Før det inn som åpent spørsmål i §10 med eieren «gruppen, før implementering», og avgjør det i beslutningsloggen. Det er to alternativer: (a) 12–17 mnd gir *ingen backtest*, eller (b) 12–17 mnd gir baseline-backtest med færre opprinnelser (*n* − 12). Oppdater så tabellen i §4.4, FR-16 (ny konsekvens for 12–17 mnd) og FR-19 (WAPE mangler for disse, og de står uansett blant de flaggede). Inntil det er avgjort, bør FR-24 kreve at det syntetiske baseline-produktet har 18–23 mnd.

### R-2 (høy): Åpent spørsmål 1 motsier motvekten SM-C1

**Sted:** PRD §10 punkt 1 mot §8.2 SM-C1. Kilde A rad 7 («Bekreftes i testskriptet»).

**Problem:** Spørsmål 1 sier at hvis spiken viser at F7 eller F8 ikke holder, «må datasettet eller generatoren justeres». SM-C1 sier: «Ikke tilpass det syntetiske datasettet for å få F7 grønn.» De to peker hver sin vei. I tillegg gjelder forbeholdet i loggen selve *backtest-oppsettet*, men PRD-en omtaler det som et spørsmål om datasettet.

**Forslag:** Skriv punkt 1 om. Spiken bekrefter oppsettet i rad 7. Hvis den viser at oppsettet ikke holder, endres det i beslutningsloggen med ny dato, og PRD-en oppdateres. Datasettet kan bare justeres så lenge FR-24 og SM-C1 fortsatt holder (det skal finnes produkter der ETS taper, og trenden skal være realistisk). Vis til SM-C1 i spørsmålet.

### Andre merknader om loggen

- Rad 2 (språk) og rad 8 (intervall) er gjengitt riktig, men PRD-en viser ikke til loggen der, slik den gjør for *Total WAPE* og *Sortering*. Se R-18.
- §11 sier at «To av dem er også ført inn i beslutningsloggen». Det stemmer: *Sortering av produktlisten* og *Total WAPE* står begge i loggen.

---

## 2. Arkitekturutkastet (kilde B)

### 2.1 Regler for historikknivå og backtest

PRD-tabellene i §4.4 og FR-5 er i samsvar med utkastets fire nivåer (<12, 12–23, 24–29, 30+). Utkastets begrunnelse for 24–29 mnd («for lite til 24 mnd trening + 6 opprinnelser») gjengis i §4.4. Avvikene står under.

#### R-4 (middels): Utkastet er utdatert om total WAPE og sortering, men addendum peker på det

**Sted:** Kilde B, Backtest («totalt (summert over alle produkter og vinduer)») og API (`GET /api/datasets/{id}/products`: «sortert etter WAPE, de svakeste først»). Addendum, innledningen: «Den fullstendige beskrivelsen finnes i arkitektur-utkast.md».

**Problem:** Beslutningsloggen rad 14 og 15 avgjør begge punktene annerledes: totalen regnes bare over produkter med backtest for begge modellene, og flaggede produkter står øverst. PRD-en følger loggen, og det er riktig. Men addendum sender leseren til et dokument som sier noe annet, og arkitekturen i steg 4 bygger på utkastet.

**Forslag:** Legg til en linje i addendum: «Der utkastet og beslutningsloggen sier forskjellig, gjelder loggen. Dette gjelder foreløpig *Total WAPE* og *Sortering av produktlisten*.» Ta det med som oppgave i steg 4 (arkitekturen).

#### R-5 (middels): Intervalldekning: uklart hvilken modell og hvilket aggregat

**Sted:** FR-15, F8, SM-2, FR-21. Kilde B, datamodellen (`backtest_result` har `intervalldekning` per `modell`).

**Problem:** Utkastet lagrer intervalldekningen per modell. PRD-en sier ikke om F8 gjelder ETS, baseline eller begge, og heller ikke om dekningen er total eller per produkt, og i så fall over hvilke produkter. F8 kan da tolkes på flere måter, og testen kan bli grønn eller rød avhengig av tolkningen.

**Forslag:** Legg til en konsekvens i FR-15: «Intervalldekningen beregnes per produkt og modell. F8 gjelder total dekning for ETS over de samme produktene og opprinnelsene som total WAPE (FR-14).» Før det inn i §11 som bekreftet tolkning, eller i beslutningsloggen hvis gruppen mener det er en beslutning.

#### R-6 (middels): WAPE er udefinert når Σ faktisk = 0

**Sted:** Ordliste *WAPE*, FR-14, FR-19. Kilde B, Backtest.

**Problem:** Et produkt med 0 salg i alle de 6 backtest-månedene (et utgått produkt, eller måneder som er fylt med 0) gir divisjon med null. Det påvirker sorteringen i FR-19, flagget *ETS taper* og visningen i FR-21.

**Forslag:** Legg til en konsekvens i FR-14: «Når Σ faktisk = 0 for et produkt, er WAPE udefinert. Den vises som "–", produktet får ikke flagget *ETS taper*, og det sorteres sist blant de uflaggede.» Alternativet er å velge en annen regel og føre den i §11.

#### R-7 (middels): Produkter som slutter før datasettets siste måned

**Sted:** Ordliste *Utfylt måned* og *Horisont*, FR-4, FR-8 («Horisonten starter måneden etter siste måned i salgshistorikken»). Kilde B, CSV-validering («mellom første og siste måned»).

**Problem:** Utfyllingen gjelder bare mellom produktets *egen* første og siste måned. Et produkt med siste salg i 2025-06 i en fil som går til 2026-10, får da en horisont som ligger i fortiden, og backtesten måles på andre måneder enn for resten av produktene. Det er uklart om «salgshistorikken» i FR-8 betyr produktets historikk eller datasettets.

**Forslag:** Bestem og før inn i §11: enten (a) at horisonten og backtest-månedene gjelder for hele datasettet (siste måned i fila), og at produkter fylles med 0 frem til datasettets siste måned med advarsel, eller (b) at produkter uten salg i datasettets siste måned flagges og ikke får prognose. Alternativ (a) utvider regelen om utfylling i rad 10. Da bør den føres i beslutningsloggen.

#### R-8 (middels): «Fra første til siste måned»: inklusive eller ikke?

**Sted:** Ordliste *Historikklengde*, FR-5, FR-10, F1 («24 måneders salg»). Kilde B, Historikknivå.

**Problem:** 2024-01 til 2025-12 er 24 måneder hvis begge endepunktene telles med, men 23 måneders avstand. Grensene på 12, 24 og 30 mnd avhenger av dette, og F1 og F5 tester rett på grensene.

**Forslag:** Endre ordlisten til «Antall måneder fra og med produktets første til og med siste måned, etter utfylling. 2024-01 til 2025-12 = 24 måneder.» Legg til en grensetest i FR-5 (11, 12, 23, 24, 29 og 30 mnd).

### 2.2 CSV-valideringstabellen

Alle de seks reglene i utkastet finnes i FR-2, FR-3 og FR-4 med samme følge ved brudd (kolonnenavn, radnummer, produkt og måned, advarsel per produkt). At én feil avviser hele fila, står i FR-3. At advarsler ikke stopper opplastingen, står i §4.1 og FR-4.

#### R-11 (middels): Tom fil, bare overskrift og tomme celler er ikke dekket av valideringsreglene

**Sted:** FR-3. Kilde B, tabellen over CSV-validering.

**Problem:** Verken utkastet eller PRD-en sier hva som skjer med en tom fil, en fil med bare overskriftsraden, en tom `produkt_id`, en tom `antall`, eller en fil som ikke er UTF-8. Med reglene som de står, kan en fil uten datarader bli godkjent som et tomt datasett.

**Forslag:** Legg til konsekvenser i FR-3: «En fil uten datarader gir en feil.» «Tom `produkt_id` eller tom `antall` gir en feil med radnummer.» Dette er presiseringer innenfor rad 10 i loggen, ikke nye formater. Før dem i §11. Tegnsett og BOM hører til åpent spørsmål 2.

#### R-16 (lav): Eksempelet på duplikat har ikke radnummer

**Sted:** UJ-2 («viser hver feil med radnummer, for eksempel «Duplikat: P-104, 2025-03»»).

**Problem:** FR-3 og utkastet sier at duplikater rapporteres med produkt og måned, ikke med radnummer. UJ-2 lover radnummer for hver feil.

**Forslag:** Endre UJ-2 til «viser hver feil, med radnummer der det gjelder». Eventuelt kan duplikatmeldingen få begge radnumrene («Duplikat: P-104, 2025-03 (rad 17 og 233)»), og FR-3 oppdateres tilsvarende.

### 2.3 Valideringsrapporten

Utkastet sier at rapporten inneholder feil, advarsler og antall produkter per historikknivå. Det samsvarer med ordlisten, FR-1, FR-5 og FR-18.

#### R-19 (lav): Advarsler og skilletegn lagres, men PRD-en sier ikke om de vises ved gjenåpning

**Sted:** FR-6, FR-18. Kilde B, datamodellen (`dataset`: skilletegn og advarsler).

**Problem:** Utkastet lagrer advarslene og skilletegnet. PRD-en sier ikke om valideringsrapporten (advarslene og antall per historikknivå) vises igjen når et lagret datasett åpnes (UJ-4).

**Forslag:** Legg til en konsekvens i FR-18: «Når et lagret datasett velges, vises advarslene og antall produkter per historikknivå fra opplastingen.» Alternativt kan det stå eksplisitt at rapporten bare vises rett etter opplasting.

### 2.4 API og datamodell

#### R-3 (høy): Total WAPE og NFR-5 kan ikke leveres av datamodellen og API-et

**Sted:** FR-14, FR-22, NFR-5. Kilde B, API og datamodell. Addendum, «API og datamodell».

**Problem:**
1. Ingen av endepunktene leverer WAPE-oversikten (total WAPE for begge modellene og «n av m»). `GET /products` gir én WAPE per produkt.
2. `backtest_result` lagrer bare `wape` og `intervalldekning` per produkt og modell. Total WAPE er Σ|feil| / Σ faktisk over produktene, og den kan ikke regnes ut fra WAPE-verdiene per produkt uten summene. Frontend kan derfor ikke beregne totalen selv.
3. NFR-5 krever at WAPE og dekning kan regnes etter for hånd «fra tallene som vises». De faktiske verdiene og backtest-prognosene per opprinnelse verken lagres eller vises.
4. F11 krever at backtest-resultatene hentes «uendret» etter omstart. Totalen må derfor enten lagres eller kunne beregnes fra data som er lagret.

**Forslag:**
- PRD: Legg til en konsekvens i FR-21: «Backtest-tabellen viser faktisk verdi, P10/P50/P90 for hver modell og hver opprinnelse», slik at NFR-5 kan oppfylles. I FR-22: «Oversikten hentes fra API-et og er ikke regnet ut i frontend», eller tilsvarende.
- Addendum: Legg til en tabell `backtest_point` (dataset_id, produkt_id, modell, opprinnelse, maaned, faktisk, p10, p50, p90), eller felt for `sum_abs_feil` og `sum_faktisk` i `backtest_result`. Legg til `GET /api/datasets/{id}/summary`, eller et oppsummeringsfelt i svaret fra `GET /products`, for FR-22. Merk det som avvik fra utkastet, som tas inn i steg 4.

#### R-9 (middels): Feature flags og mock-fallback: «med» i utkastet, «ikke bygd» i addendum

**Sted:** Kilde B, «Fra technology.md» («Med: … mock-fallback-prinsippet … feature flags for trinn 2»). Addendum, «Forberedt for trinn 2» («Ingenting av dette bygges i v1»).

**Problem:** Utkastet tar med feature flags og mock-fallback i v1, men addendum sier at ingenting av dette bygges. Mock-fallback gir bare mening når det finnes en ekstern tjeneste, og v1 har ingen. Utviklerne får to beskjeder som ikke stemmer overens.

**Forslag:** Skriv i addendum: «I v1 finnes ingen feature flags og ingen mock-fallback, fordi v1 ikke kaller noen ekstern tjeneste. Utkastets "Med"-liste for disse gjelder trinn 2.» Ta det med som oppgave i steg 4. Dette er i tråd med rammen om at appen skal kjøre uten API-nøkler.

#### R-14 (lav): Hvilken modell P50 i grafen og scenarioene kommer fra

**Sted:** FR-8, FR-11, FR-20. Kilde B, `forecast` (har `modell`).

**Problem:** For produkter med nivå *ets* lagres prognoser for begge modellene. PRD-en sier «sesongnaiv baseline beregnes også», men ikke om baseline-prognosen vises, eller at grafen og scenarioene bruker ETS.

**Forslag:** Legg til en konsekvens i FR-20: «For historikknivå *ets* viser grafen og scenarioene ETS-prognosen. For *baseline* viser de sesongnaiv prognose.» Hvis baseline-prognosen ikke skal vises for *ets*-produkter, bør det stå under «Utenfor omfang».

#### Ellers i samsvar

- `POST /api/datasets` validerer, lagrer og kjører alt synkront, slik FR-7 og NFR-7 forutsetter.
- `GET /api/datasets` gir filnavn og tidspunkt (FR-18).
- `GET /products` gir historikknivå og flaggene `kort_historikk` og `ets_taper` (FR-19). `kort_historikk` er avledet av `historikknivaa`, så den trenger ingen egen kolonne.
- Merknaden om scenariospennet kommer fra API-et (utkastet) og vises alltid (FR-12).
- `GET /api/health` (NFR-2, F12).
- Åpent spørsmål i utkastet om Alembic eller `create_all` hører hjemme i steg 4 og trenger ikke stå i PRD-en.

### 2.5 Tekniske detaljer i hovedteksten og kapasiteter som mangler

#### R-18 (lav): Tekniske detaljer i hovedteksten

**Sted:** FR-6 («lokal SQLite-database»), NFR-1 (`uv`, `npm`), NFR-2 (`GET /api/health`), NFR-6 (Playwright), §4.4 («ETS trenger 24 måneders trening»).

**Vurdering:** Hovedteksten er stort sett fri for teknologi. Detaljene som står der, kommer rett fra akseptansekriteriene i briefen (F10, F11, F12), så de kan bli stående. Begrunnelsen i §4.4 forklarer en regel og hører hjemme der. Det finnes ingen bibliotek- eller parameternavn (`statsforecast`, `n_windows`, `level=[80]`) i hovedteksten. Disse står riktig i addendum.

**Forslag:** Ingen flytting er nødvendig. Vurder å vise til beslutningsloggen også i NFR-4 (*Språk*), FR-9 (*Intervaller* og *Nullgrense*), FR-5 (*Kort historikk*) og FR-13 (*Backtest*), slik det allerede gjøres for *Total WAPE* og *Sortering*. Det gjør sporingen mot den bindende loggen fullstendig.

#### R-10 (middels): Next.js-telemetri og `next/font/google` kaller eksterne tjenester

**Sted:** NFR-1 («kaller ingen eksterne tjenester mens den kjører», «Hele v1-flyten fungerer uten nettverk»). Addendum (Next.js 16).

**Problem:** Next.js sender anonym telemetri som standard når `next dev` kjører. `next/font/google`, som shadcn-maler ofte bruker, henter fonter fra Google. Begge bryter den bokstavelige ordlyden i NFR-1, og fonthentingen kan gi feil uten nett. NFR-1 utelukker også miljøvariabler, så `NEXT_TELEMETRY_DISABLED` i en `.env`-fil er ikke en løsning.

**Forslag:** Skriv i addendum under NFR-1: «Telemetrien slås av i `npm run dev`-skriptet (for eksempel `next telemetry disable` i et `predev`-skript, eller variabelen satt i selve skriptet). Bare lokale fonter eller systemfonter. Ingen `next/font/google` og ingen CDN.» Legg til i testbetingelsen for NFR-1: «UJ-1 kjøres med nettverket koblet fra.»

#### R-21 (lav): `numba`-kompilering ved første kjøring

**Sted:** NFR-7. Addendum (`statsforecast`).

**Problem:** `statsforecast` bruker `numba`, som kompilerer ved første kall. Det kan ta en vesentlig del av grensen på 60 sekunder, særlig hvis den første opplastingen skjer rett etter oppstart (eller hvis `seed_if_empty` gjør den første kjøringen).

**Forslag:** Skriv i addendum at kompileringsbufferen til `numba` brukes (`cache=True`, som er standard i `statsforecast`), og at tidtakingen i NFR-7 gjøres både kaldt og varmt. Det er greit å stramme kravet til at bare varm kjøring må holde seg innenfor 60 s, men da må det stå eksplisitt.

#### R-17 (lav): Det syntetiske datasettet har ikke noe produkt med 24–29 mnd

**Sted:** FR-24, FR-16, utkastets tabell (24–29 mnd).

**Problem:** FR-24 har produkter med 36, under 12 og 12–23 mnd. Nivået som får ETS-prognose men bare baseline-backtest, finnes ikke i demodataene. Det testes bare i enhetstester.

**Forslag:** Legg til i FR-24: «Ett produkt har 24–29 måneders historikk.» Juster da tallene i UJ-3 («17 av 18») tilsvarende. Alternativt kan det stå at FR-16 bare testes med egne testdata.

### 2.6 Andre punkter i PRD-en

#### R-13 (lav): Rekkefølgen blant de flaggede produktene og uavgjort WAPE

**Sted:** FR-19, FR-17, FR-22.

**Problem:** Rekkefølgen innenfor gruppen med flaggede produkter er ikke definert, og produkter med nivå *ingen* har ingen WAPE. Det er heller ikke sagt om lik WAPE gir *ETS taper* eller teller som at ETS slår baseline («n av m»). Det gjør testene i FR-19 og FR-22 ikke-deterministiske.

**Forslag:** Legg til i FR-19: «Innenfor de flaggede: *ETS taper* først, deretter *kort historikk*. Innenfor hver gruppe WAPE med høyest først, og produkter uten WAPE sist, sortert etter `produkt_id`.» Legg til i FR-17 og FR-22: «Lik WAPE gir ikke flagget, og teller ikke som at ETS slår baseline.» Før begge i §11.

#### R-15 (lav): Tolkninger som ikke er ført i §11

**Sted:** FR-23 («byte-identiske filer»), FR-24 («rundt 20 produkter med 36 måneders historikk»).

**Problem:** F9 sier «identisk datasett». «Byte-identiske filer» er en strengere tolkning. Antallet produkter og lengden på 36 mnd finnes verken i loggen eller i utkastet. Hvis tallene ikke står i briefen, er de tolkninger som skulle stått i §11.

**Forslag:** Sjekk tallene mot briefen. Før dem som mangler kildegrunnlag, inn i §11, sammen med «byte-identisk».

---

## 3. Spørsmål om brukerbehov i research-planen (kilde A)

| Spørsmål i research-planen | Relevant for v1? | Står i PRD-en? | Vurdering |
|---|---|---|---|
| Hvordan ser en CSV-eksport fra ERP ut? (semikolon, desimalkomma, datoformat, manglende måneder) | Ja | §10 punkt 2 | Dekket. Semikolon og manglende måneder er avgjort (rad 10). Desimalkomma, BOM og datoformat står som åpne. Godt formulert («ikke nye formater»). |
| Hva gjør en etterspørselsplanlegger? (stillingsannonser) | Ja, det validerer personaen (Kari, 200 produkter, månedlig) | Nei | R-12 |
| Hva trenger Kari å se først i dashbordet? | Delvis besvart | Nei (besvart av rad 12 og 14) | R-20 |
| Hvordan forstår en planlegger P10/P90? Bedre ord? | Delvis besvart | Nei (besvart av rad 11) | R-20. Det som gjenstår, er om «80 % intervall» og merknaden om spennet blir forstått. |
| Mulig samtale med en planlegger | Ja, det er den eneste valideringen av UJ-1 til UJ-4 mot en ekte bruker | Nei | R-12 |

#### R-12 (middels): Validering av personaen og samtale med planlegger er ikke åpne spørsmål

**Sted:** PRD §10, §2.1, §2.3.

**Problem:** Personaen og brukerreisene bygger på antakelser fra briefen. Research-planen har to spørsmål som skal teste dem (stillingsannonser og samtale med en planlegger), men de er ikke ført opp. Hvis funnene endrer for eksempel antallet produkter eller horisonten, påvirker det NFR-7 og FR-24, og det er derfor ikke likegyldig når svaret kommer.

**Forslag:** Legg til §10 punkt 3: «Stemmer personaen og arbeidsflyten? Fra research-planen: stillingsannonser for etterspørselsplanleggere og en mulig samtale med en planlegger. Funnene kan endre brukerreisene, ordbruken og tallene i NFR-7 og FR-24, men ikke beslutningsloggen. Eier: gruppen. Blokkerer ikke.» Ta med spørsmålet om planleggeren forstår «80 % intervall» og merknaden om scenariospennet, som et delspørsmål til samtalen.

#### R-20 (lav): Spørsmål som er besvart av beslutninger, bør merkes som besvart

**Sted:** research-plan.md, avsnittet Brukerbehov. Gjelder kilden, ikke PRD-en.

**Problem:** «Hva trenger Kari å se først» og «Bedre ord for P10/P90» er i praksis besvart av rad 11, 12 og 14, men de står fortsatt som åpne i research-planen. Det kan gi inntrykk av at PRD-en mangler noe.

**Forslag:** Stryk dem i research-planen med en henvisning til beslutningsraden, slik det er gjort under «Uavklarte beslutninger». Alternativt kan PRD-en få en setning i §10 om at de er besvart av beslutningsloggen.

---

## 4. Det som må gjøres, i prioritert rekkefølge

1. **R-1:** Avgjør backtest for 12–17 mnd i beslutningsloggen. Oppdater §4.4, FR-16 og FR-24.
2. **R-2:** Skriv åpent spørsmål 1 om, slik at det ikke motsier SM-C1.
3. **R-3:** Legg til backtest-verdier per opprinnelse og et endepunkt for oppsummering i addendum. Legg til konsekvenser i FR-21 og FR-22.
4. **R-4, R-9:** Skriv i addendum at loggen gjelder foran utkastet, og at v1 ikke har feature flags eller mock-fallback.
5. **R-5, R-6, R-7, R-8, R-11:** Presiseringer som skal inn i §11 (dekning, WAPE = 0/0, produkter som slutter tidlig, inklusiv lengde, tomme filer og celler).
6. **R-10:** Føringer for å kjøre uten nett i addendum (telemetri og fonter).
7. **R-12:** Nytt åpent spørsmål om personaen og en samtale med en planlegger.
8. Lave funn (R-13 til R-21) tas sammen ved neste revisjon.
