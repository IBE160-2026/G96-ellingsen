# Avstemmingsreview: arkitekturspine mot UX, beslutningslogg og åpne punkter

- **Dato:** 2026-11-17
- **Gjennomgått:** [ARCHITECTURE-SPINE.md](../ARCHITECTURE-SPINE.md)
- **Kilder:** EXPERIENCE.md (hele), DESIGN.md (tekniske føringer), research-plan.md (beslutningsloggen, bindende), teknisk.md, `.logs/mathias-ellingsen/issues.md`, `.docs/planning-artifacts/architecture/arkitektur-utkast.md`. PRD (FR-1 til FR-26) er brukt som støtte der UX viser til den.

## Dom

**Godkjent med endringer.** Spinen dekker nesten alt UX trenger: detaljtabellen, sumraden (via `metrikk.sum_faktisk` og `sum_avvik`), dommerlinjens fire varianter, fordelingslinjen, advarslene, historikktabellen med «(fylt inn)», datasettvelgerens format og grafens `aria-label`. Alle 20 radene i beslutningsloggen er fulgt, og ingen blir motsagt. Ingen funn er kritiske. Det er to høye funn. Begge gjelder feiltilstandene. Med spinen slik den står nå, kan dashbordet vise «Ingenting er lagret» selv om datasettet faktisk blir lagret, og det kan få et feilsvar som zod ikke klarer å parse. I tillegg finnes en del hull i kontrakten som bør tettes før implementeringen begynner.

| Alvorlighet | Antall |
|---|---|
| Kritisk | 0 |
| Høy | 2 |
| Middels | 9 |
| Lav | 12 |

---

## Høy

### H-1. Tidsavbrudd etter 120 s stopper ikke kjøringen, så teksten «Ingenting er lagret» kan være feil

- **Kilde:** EXPERIENCE.md, *State Patterns* → *Kjøring pågår* («Etter 120 s slutter klienten å vente og går til *Kjøring feilet*»), *Faste tekster* («Prognosen kunne ikke kjøres. Ingenting er lagret.» og «Kjøringen tok mer enn to minutter og ble stoppet.»), UJ-1 *Feil* («forrige datasett blir stående»).
- **Spinen:** AD-10 og AD-11 («Klienten gir opp etter 120 s», `proxyTimeout: 130000`).
- **Problem:** Spinen har bare en tidsgrense i klienten. Når klienten gir opp, fortsetter pipelinen i trådpoolen. Deretter skriver den og committer (AD-2), og låsen blir holdt hele tiden. Det gir tre feil:
  1. Kari leser «Ingenting er lagret» og «ble stoppet», men datasettet dukker opp i velgeren noen sekunder senere.
  2. Prøver hun på nytt, får hun `409`, og det finnes ingen UX-tekst for det (se M-5).
  3. Proxyen gir opp etter 130 s og svarer da med en feil som verken er `{rapport}` eller en nettverksfeil (se H-2).
- **Forslag:** Legg inn en tidsgrense på serveren i AD-10. Ruten måler tiden fra forespørselen starter. Når pipelinen er ferdig og tidsgrensen er passert (for eksempel 110 s, altså under klientens 120 s), forkaster skallet resultatet uten å skrive noe. Det svarer da `500 {rapport}` med `status: feilet`, `kode: tidsavbrudd` og meldingen «Kjøringen tok mer enn to minutter og ble stoppet.». Skriv også at tråden ikke kan avbrytes, men at det som avgjør er at **ingenting committes etter tidsgrensen**. Låsen frigjøres først når tråden er ferdig. Rekkefølgen tidsgrense på serveren < klientens grense (120 s) < `proxyTimeout` (130 s) bør stå i AD-11. Legg til en test der pipelinen blir forsinket kunstig og ingen rad blir skrevet.

### H-2. Formen på feilsvaret ved uventede unntak og ved proxyfeil er ikke definert. Klienten kan ikke skille *Kjøring feilet* fra *Ingen kontakt med backend*

- **Kilde:** EXPERIENCE.md, *State Patterns* → *Kjøring feilet* («Under står feilmeldingen fra backend på norsk») og *Ingen kontakt med backend* (rød variant med egen tekst, «Fokus flyttes til teksten»), UJ-4 *Feil*.
- **Spinen:** AD-9 (`500 {rapport}` når status er `feilet`), *Consistency Conventions* → *Feil* («Uventede unntak … gir `500` med en generisk norsk melding»), AD-12 (alle kall parses med zod).
- **Problem:**
  - Det står ikke at et uventet unntak også skal pakkes i `{rapport}`. FastAPI og Starlette svarer som standard `500` med teksten `Internal Server Error`. Da feiler zod-parsingen, og frontend vet ikke hvilken tilstand den skal vise.
  - Når backend ikke kjører, svarer Next-proxyen med en egen 5xx-feil. Det er ikke et nettverksbrudd i `fetch`. Spinen sier ikke hvordan `klient.ts` klassifiserer dette.
  - For `status: feilet` er det ikke sagt hvor «feilmeldingen fra backend» ligger, for eksempel i `feil[0].melding`.
- **Forslag:**
  1. AD-9 får en global unntakshåndterer for `POST /api/datasets` som alltid svarer `500 {rapport: {status: "feilet", feil: [{kode: "uventet", melding: "<generisk norsk tekst>", rader: []}], …}}`. Teksten føres inn i EXPERIENCE.md.
  2. Ved `feilet` har `feil[]` nøyaktig ett element. Frontend viser overskriften fra `tekster.ts` og `feil[0].melding` under.
  3. Klassifiseringen i `klient.ts` skrives inn i AD-12. Et svar som parses som `{rapport}` gir *Fil avvist* eller *Kjøring feilet*. Et `{detail}` med 404 gir *Produktdetalj kunne ikke hentes*. Alt annet gir *Ingen kontakt med backend*: nettverksfeil, svar som ikke er JSON, 5xx som ikke kan parses, og tidsavbrudd i GET-kall. Klientens eget tidsavbrudd ved POST (120 s) gir *Kjøring feilet* med teksten for tidsavbrudd.
  4. Legg til kontrakttester for alle tre tilfellene.

---

## Middels

### M-1. Produktlisten kan ikke skille «ingen backtest» fra «udefinert» når WAPE vises som «–»

- **Kilde:** EXPERIENCE.md, *Tall- og datoformat* («For skjermleser … `udefinert` … Når produktet ikke har backtest, er den skjulte teksten «ingen backtest»»), *Interaction Primitives* (det tilgjengelige navnet på raden).
- **Spinen:** AD-9, `GET …/products` gir `{produkt_id, historikknivaa, liste_wape, flagg_kort_historikk, flagg_ets_taper, rang}`.
- **Problem:** `liste_wape = null` betyr enten 12–17 mnd (ingen backtest) eller 18 mnd eller mer med Σ faktisk = 0 (udefinert). Begge tilfellene kan ha nivået `sesongnaiv`, så nivået sier ikke hvilket det er. Frontend måtte da kjenne 18-månedersgrensen, og det bryter AD-6 («`nivaa.py` er eneste kilde for grensene»).
- **Forslag:** Legg til et lagret felt i listeelementet, for eksempel `har_backtest: bool` eller `wape_status ∈ {definert, udefinert, ingen_backtest}`. Feltet settes i kjernen sammen med `liste_wape`.

### M-2. Scenariototalen er verken lagret eller plassert i kjernen

- **Kilde:** EXPERIENCE.md, *Scenariotabell* (sumraden), *Accessibility Floor* → *Grafen* (`aria-label` med «Forventet {sum} … spenn {p10-sum}–{p90-sum}»).
- **Spinen:** AD-1 («Bare `domene/` … regner ut … scenariototaler»), AD-3 (listen over lagrede verdier har ikke med scenariototalen), AD-9 (`scenariototal{p10, p50, p90} | null` i svaret).
- **Problem:** Hvis lesestien summerer `prognose`-radene i SQL eller i API-et, bryter det AD-1 og AD-3 («Ingen SQL-`SUM`»). Hvis den ikke gjør det, finnes det ingen kilde for feltet. ER-diagrammet og AD-3 viser ingen kolonne for det.
- **Forslag:** Ta med `produkt.scenario_p10`, `scenario_p50` og `scenario_p90` (heltall, `NULL` for nivå *ingen*) i AD-3. De regnes i kjernen fra de avrundede verdiene (AD-5). API-et serialiserer dem uendret.

### M-3. «Lik WAPE» sammenlignes på flyttall

- **Kilde:** EXPERIENCE.md, *Dommerlinjen* («strengt lavere WAPE», «lik WAPE»), *State Patterns* → *Lik WAPE*. Beslutningsloggen: *Når ETS taper* og *Intervalldekning og sortering* (stabile tester).
- **Spinen:** AD-7 (`dommer` ∈ {…, `lik`, …}), AD-3 (`wape` = sum_avvik / sum_faktisk).
- **Problem:** Det står ikke hva dommeren sammenligner. To brøker med samme verdi kan avvike i siste bit, og da blir `lik` aldri truffet, eller den blir truffet tilfeldig.
- **Forslag:** I AD-7: dommeren sammenligner `sum_avvik` for ETS med `sum_avvik` for baseline. Det er heltall, og nevneren er den samme for begge modellene. Testen bruker en konstruert serie med lik `sum_avvik`.

### M-4. Ved |S| = 0 blir `m` `null`, men UX bruker m = 0

- **Kilde:** EXPERIENCE.md, *WAPE-oversikten* («Når m = 0: …») og *State Patterns* → *WAPE-oversikt uten grunnlag (m = 0)*.
- **Spinen:** AD-4 («Når |S| = 0, er alle totalene `null`»), *Structural Seed* (`sammendrag` = {total_wape, total_dekning, n, m}).
- **Problem:** Det er uklart om «alle totalene» også omfatter `n` og `m`. Hvis `m` blir `null`, må frontend tolke `null` som 0. Det bryter konvensjonen «`null` betyr udefinert, aldri 0».
- **Forslag:** Skriv i AD-4: `n` og `m` er alltid heltall (0 når |S| = 0), mens `total_wape` og `total_dekning` er `null`. Frontend velger malen for m = 0 på `m === 0`.

### M-5. `409` (opplasting pågår) har verken rapportstatus eller UX-tekst

- **Kilde:** EXPERIENCE.md, *Faste tekster* (ingen tekst for dette) og *State Patterns* (ingen tilstand).
- **Spinen:** AD-9 (`409 {rapport}`), AD-8 (`status` ∈ {godkjent, avvist, feilet}, og backend skriver `melding` «etter malene i EXPERIENCE.md»).
- **Problem:** Det finnes ingen mal for `409`, og det er ikke sagt hvilken status rapporten får. Fra én fane kan dette ikke skje, fordi siden er `inert`. Men det skjer med to faner, og etter et tidsavbrudd (H-1).
- **Forslag:** `409` gir `status: feilet` og `kode: opplasting_pagaar`. Legg teksten inn i EXPERIENCE.md, for eksempel «En annen opplasting kjører allerede. Vent til den er ferdig, og prøv igjen.». Den vises i tilstanden *Kjøring feilet*.

### M-6. Rekkefølgen og granulariteten i `feil[]` er ikke fastsatt, og kodene er ikke listet

- **Kilde:** EXPERIENCE.md, *Fil avvist* («**Alle** feilene listes i filrekkefølge med radnummer»), tabellen over feilmaler (sju regler, én melding per forekomst), overskriften «{n} feil». UJ-2 forventer «2 feil».
- **Spinen:** AD-8 (`feil[]` med {`kode`, `melding`, `rader[]`}).
- **Problem:** `rader[]` kan forstås slik at like feil grupperes med flere rader. Da stemmer ikke «{n} feil» med UJ-2, og malene «Rad {r}: …» passer ikke. Rekkefølgen er heller ikke sagt.
- **Forslag:** I AD-8: én `feil` per forekomst. `rader[]` har én rad, eller to ved duplikat (`r1 < r2`). Feil uten rad (manglende kolonne, skilletegn, ingen datarader) har `rader: []` og står først. Resten sorteres på `rader[0]`, deretter på kolonnerekkefølgen. List `kode`-ene som en enum, én per mal i EXPERIENCE.md, og vis til H-2 og M-5 for `feilet`.

### M-7. Avrunding til heltall er en ny bindende regel som ikke står i beslutningsloggen

- **Kilde:** research-plan.md, beslutningsloggen: *P10, P50 og P90 settes til minst 0* (bare nullgrense). teknisk.md (spiken målte F7 og F8 på urundede verdier).
- **Spinen:** AD-5 (`rund(max(0, x))` med `floor(x + 0.5)`).
- **Problem:** Regelen motsier ikke loggen, og den er god for NFR-5. Men den endrer tall som F7 og F8 måles på. Spinen sier selv at loggen står over spinen, så en ny regel av denne vekten bør føres i loggen. Avrunding kan flytte dekningen for produkter med lavt volum, så spike-tallene er ikke lenger direkte sammenlignbare.
- **Forslag:** Før en ny rad i beslutningsloggen: «P10/P50/P90 avrundes til heltall (halv opp) etter nullgrensen, og all videre beregning bruker heltallene». Legg også inn i *Deferred* at spiken kjøres på nytt med avrunding (sammen med punktet om F8).

### M-8. Fila er ikke UTF-8: verken mal eller kode

- **Kilde:** PRD FR-1 («Fila leses som UTF-8, med eller uten BOM»). EXPERIENCE.md, tabellen over feilmaler (ingen mal for tegnkoding). Beslutningsloggen *CSV* (norsk Excel). Norsk Excel lagrer ofte CSV som Windows-1252.
- **Spinen:** AD-8 (backend skriver meldingen «etter malene i EXPERIENCE.md»).
- **Problem:** En fil med «æøå» i Windows-1252 feiler ved dekoding. Det finnes ingen mal for denne feilen, så backend må finne på en tekst selv, eller unntaket ender som `500` (H-2).
- **Forslag:** Legg til `kode: tegnkoding` i AD-8. Legg inn malen i EXPERIENCE.md, for eksempel «Fila er ikke lagret som UTF-8. Lagre den som «CSV UTF-8» i Excel og prøv igjen.». Fila skal da avvises (`422`), ikke feile.

### M-9. Mock-fallback og feature flags fra utkastet forsvinner uten at det er begrunnet

- **Kilde:** arkitektur-utkast.md, *Fra technology.md* («**Med:** … mock-fallback-prinsippet, seeding ved oppstart (`seed_if_empty`) og feature flags for trinn 2»).
- **Spinen:** *Deferred* («Trinn 2 (… feature flags). Utenfor v1, og ingen forberedelse i koden»). Mock-fallback er ikke nevnt.
- **Problem:** Spinen sier at den erstatter utkastet. To punkter som utkastet sa eksplisitt «Med» om, blir stille fjernet, eller i ett av tilfellene snudd. For sensor ser det ut som et avvik fra technology.md uten begrunnelse.
- **Forslag:** Skriv en linje under *Deferred*, eller i den avstemte listen, om at mock-fallback ikke trengs fordi `seed_if_empty` gir ekte data (FR-25), og at feature flags tas bort med begrunnelsen YAGNI. Ta også med en kort «Ikke med»-linje fra utkastet: innlogging, betaling, e-post, Redis, Caddy, deploy og overvåking.

---

## Lav

### L-1. Feltene i `salg` og `prognose` står ingen steder

- **Kilde:** arkitektur-utkast.md, *Datamodell* (`sales`: … `utfylt`, `forecast`: … `modell`, p10, p50, p90).
- **Spinen:** *Structural Seed* («Feltene i de andre tabellene står i AD-3, AD-6 og AD-7»). Feltene `salg.maaned`, `antall` og `utfylt` og alle feltene i `prognose` står bare indirekte i AD-9. Det samme gjelder `produkt.historikklengde` og `prognosemodell`.
- **Forslag:** Legg inn én linje per tabell: `salg(datasett_id, produkt_id, maaned, antall, utfylt)`, `prognose(datasett_id, produkt_id, maaned, p10, p50, p90)` (modellen ligger i `produkt.prognosemodell`) og `produkt(…, historikklengde, historikknivaa, prognosemodell, dommer, flagg_*, liste_wape, rang, scenario_*)`.

### L-2. Det er ikke sagt hvordan `backtest.metrikk` er formet i svaret, og rekkefølgen på `punkter[]` er ikke fastsatt

- **Kilde:** EXPERIENCE.md, *Detaljer per opprinnelse* (én rad per opprinnelse, og sumraden med Σ faktisk og Σ avvik per modell).
- **Spinen:** AD-9 (`{metrikk, punkter[…]}`), AD-3 (feltene i `backtest_metrikk`).
- **Problem:** Det står ikke at `metrikk` er de lagrede feltene fra AD-3. Det er heller ikke sagt at sumraden skal bruke `sum_faktisk` og `sum_avvik` i stedet for å summere i TS. Detaljtabellen slår sammen baseline og ETS per `maaned`, og trenger en fast rekkefølge.
- **Forslag:** `metrikk` = {antall_punkt, sum_faktisk, sum_avvik, wape, antall_treff, dekning}. `punkter` er sortert stigende på `opprinnelse`. Sumraden viser `metrikk.sum_*` uendret, i tråd med AD-3.

### L-3. Det er ikke sagt hva som vinner, `null` eller `kan_ikke_sammenlignes`

- **Kilde:** EXPERIENCE.md, *Bare baseline-backtest* («Dommerlinjen vises ikke») og *WAPE udefinert* («Dommerlinjen er «Kan ikke sammenlignes …»»).
- **Spinen:** AD-7.
- **Problem:** For et produkt med 18–29 mnd og Σ faktisk = 0 sier UX begge deler.
- **Forslag:** Skriv i AD-7: `null` vinner når produktet ikke har backtest for begge modellene. Dommerlinjen vises da ikke. Gi også UX beskjed, slik at *WAPE udefinert* gjelder bare for 30 mnd eller mer.

### L-4. Grafens `aria-label` har ingen variant for historikknivå *ingen*

- **Kilde:** EXPERIENCE.md, *Faste tekster* (`aria-label` på grafen).
- **Spinen:** AD-9 (`scenariototal: null`). Data finnes, men teksten mangler.
- **Forslag:** Dette er et UX-punkt: legg inn en mal, for eksempel «Historikk for {produkt_id} fra {måned} til {måned}. Ingen prognose: under 12 måneders historikk.». Spinen trenger ingen endring.

### L-5. Advarselsmalen har «måned(er)», og rekkefølgen på advarslene er ikke fastsatt

- **Kilde:** EXPERIENCE.md, malen for FR-4 («{antall} måned(er)», eksempelet bruker «2 måneder»).
- **Spinen:** AD-8.
- **Forslag:** Backend velger «måned» når antall er 1 og «måneder» ellers. `advarsler[]` sorteres på `produkt_id`, og `maaneder[]` sorteres stigende.

### L-6. «Byte-identisk» rapport er upresist

- **Spinen:** AD-8 («returneres byte-identisk av `GET /api/datasets/{id}`»).
- **Problem:** Rapporten ligger inne i et større JSON-svar, så det er JSON-verdien som skal være lik, ikke bytene.
- **Forslag:** Skriv «lik som JSON-verdi (samme felt og samme verdier) som `rapport` i 201-svaret», og test det med `==` etter parsing.

### L-7. `produkt_id` i URL-stien

- **Spinen:** AD-9 (`GET …/products/{produkt_id}`), *Id-er* («strengen fra CSV-fila uendret»).
- **Problem:** Valideringen begrenser ikke tegnene i `produkt_id`. En id med `/`, `?`, `#` eller mellomrom gir feil rute eller 404.
- **Forslag:** Frontend bruker `encodeURIComponent`, og ruten bruker `{produkt_id:path}`. Ta med en test med `P/1` og `P 1`. Det andre alternativet er å avvise slike tegn i FR-3, men det må da inn i PRD og EXPERIENCE.

### L-8. `python-multipart` mangler i stacken

- **Spinen:** *Stack*, og AD-9 (multipart, feltet `fil`).
- **Problem:** FastAPI trenger `python-multipart` for å ta imot `UploadFile`. Uten pakken feiler oppstarten.
- **Forslag:** Legg til `python-multipart` med låst versjon i tabellen.

### L-9. Malen fra create-next-app henter Google-fonter

- **Kilde:** DESIGN.md, typografien («Kun systemfonter (NFR-1 offline: ingen next/font/google, ingen CDN)») og *Do's and Don'ts*.
- **Spinen:** AD-11 forbyr dette allerede.
- **Problem:** Standardmalen bruker `next/font/google` (Geist) i `layout.tsx`, og shadcn init kan bygge videre på den. Regelen blir brutt allerede ved oppsettet hvis ingen fjerner den.
- **Forslag:** Legg inn i AD-11: «Fjern Geist og `next/font` fra malen ved init. En test eller lint sjekker at `next/font` ikke importeres.». Lucide (`lucide-react`) bør stå i stacken, fordi DESIGN.md krever lokale ikoner.

### L-10. shadcn og `experimental.proxyTimeout` er ikke låst eller verifisert

- **Spinen:** *Stack* («shadcn/ui (CLI) gjeldende ved init»), AD-11 (`experimental.proxyTimeout`).
- **Forslag:** Før opp versjonen av shadcn CLI når init er kjørt. Sjekk at `experimental.proxyTimeout` fortsatt virker i Next 16.4 for rewrites, med en test som bruker et kunstig tregt endepunkt. Opsjonen er eksperimentell.

### L-11. Det står ikke hvordan `produkt_id` sorteres

- **Kilde:** Beslutningsloggen, *Intervalldekning og sortering* («like verdier etter produkt_id»).
- **Spinen:** AD-1 og AD-7 («`produkt_id` stigende»).
- **Forslag:** Skriv «ren strengsortering på kodepunkter (Python `sorted` på `str`)», slik at `P-10` kommer før `P-9`, og at testene og fasiten sorterer likt.

### L-12. Utkastet og issues.md er ikke oppdatert

- **Kilde:** issues.md, linje 7, 13, 14 og 21 (alle er fortsatt `[ ]`). arkitektur-utkast.md har ingen merknad om at det er erstattet.
- **Spinen:** Toppteksten («Dette dokumentet erstatter …»).
- **Forslag:** Når spinen er godkjent, skal disse fire punktene krysses av med «(løst 2026-11-17, spine AD-x)». Legg også en linje øverst i utkastet om at det er erstattet av spinen, med lenke.

---

## Sjekk av hver rad i beslutningsloggen

| Rad i loggen | Spinen | Status |
|---|---|---|
| Database: SQLite | Stack, AD-13, Structural Seed | OK |
| Språk: norsk | NFR-4, konvensjonene *Navn* og *Tekster* | OK |
| Kort historikk (<12 / 12–23 / 24+) | AD-6 | OK. «24+ gir ETS og baseline» er oppfylt ved at baseline brukes i backtesten. Alle produkter med 24 mnd eller mer har baseline-backtest. Spinen bør skrive denne tolkningen av FR-10 («baseline beregnes også») eksplisitt (lav). |
| Prognosen kjøres automatisk | AD-2, AD-9 (én POST) | OK |
| P10, P50 og P90 settes til minst 0 | AD-5 | OK. Avrunding er lagt til uten egen rad i loggen (M-7). |
| Scenarioer = sum av månedlige verdier + merknad | AD-1, AD-5, `tekster.ts` | OK. Lagring mangler (M-2). Merknaden er flyttet fra API-et (utkastet) til frontend, og det er i tråd med EXPERIENCE. |
| Backtest 6 opprinnelser, h=1, step 1, under 30 bare baseline | AD-6 | OK |
| Intervaller `level=[80]` | AD-6 | OK |
| ETS taper: vis ETS, flagg, begge WAPE | AD-7, AD-9 (begge metrikkene) | OK. Sammenligningen er uklar (M-3). |
| CSV-regler | AD-8, `domene/csv.py`, `validering.py`, `utfylling.py` | OK. Tegnkoding (M-8) og rekkefølgen på feilene (M-6) mangler. |
| Pessimistisk/Forventet/Optimistisk | `tekster.ts` | OK |
| Dashbordet starter med listen sortert etter WAPE og flagg | AD-7 | OK |
| Syntetiske data med trend | `testdata/generator.py` | OK. Detaljene hører til generatoren. |
| Sortering: flaggede øverst, resten etter WAPE synkende | AD-7 | OK |
| Total WAPE over samme produkter (30+ mnd) | AD-4 | OK. Kravet Σ faktisk > 0 følger av raden om WAPE = 0. |
| Backtest for 12–17 mnd: ingen | AD-6 | OK |
| WAPE når faktisk = 0: «–», ikke i totalen, aldri ETS taper, rett etter de flaggede | AD-3, AD-4, AD-7 | OK |
| Seed 42, endres ikke | Structural Seed, kartet | OK. «Endres ikke» kunne stått eksplisitt. |
| Dekning per modell, per produkt og totalt, F8 for ETS, sortering med `produkt_id` ved like verdier | AD-3, AD-4, AD-7 | OK. Hvordan `produkt_id` sorteres er ikke sagt (L-11). |
| Søk FR-26 | AD-7, AD-12 (i klienten) | OK |
| Autovalg av første produkt | AD-7 (`ORDER BY rang`) | OK. Det skjer i frontend og står ikke eksplisitt, men det er heller ikke nødvendig. |

**Konklusjon:** Spinen motsier ingen av radene i loggen.

## UX-data mot API-svaret

| UX-behov | Kilde i API-et | Status |
|---|---|---|
| Kolonnene i detaljtabellen (Måned, Faktisk, P50, avvik og i spenn per modell) | `backtest.{modell}.punkter[]` | OK (rekkefølgen: L-2) |
| Sumrad Σ faktisk / Σ avvik | `backtest.{modell}.metrikk.sum_*` | OK, men formen bør stå eksplisitt (L-2) |
| Dommerlinjen, 4 varianter + ingen linje | `dommer` | OK (M-3, L-3) |
| WAPE-oversikt + m = 0 | `sammendrag` | OK (M-4) |
| Fordelingslinje + oppsummeringslinje | `rapport.per_nivaa`, `antall_produkter`, `antall_kort_historikk` | OK |
| Advarsler + «Vis advarsler ({n})» | `rapport.advarsler[]` | OK (L-5) |
| Feilmaler + «{n} feil» | `rapport.feil[]` | Uklart (M-6, M-8) |
| Kjøring feilet | `500 {rapport}` | Hull (H-2) |
| Tidsavbrudd 120 s | bare i klienten | Feil (H-1) |
| Ingen kontakt med backend | ikke definert | Hull (H-2) |
| Opplasting pågår | `409 {rapport}` | Ingen tekst (M-5) |
| `aria-label` på grafen (periode, summer) | `historikk[]`, `scenariototal` | Data finnes, men lagringen mangler (M-2). Variant for *ingen* mangler (L-4). |
| Historikktabell med «(fylt inn)» | `historikk[].utfylt` | OK |
| Datasettvelger «filnavn · dd.mm.åååå kl. tt.mm» | `GET /api/datasets` (`filnavn`, `opplastet` i UTC) | OK |
| Undertekst i panelhodet (ETS / Sesongnaiv) | `prognosemodell` | OK |
| «–» med «udefinert» eller «ingen backtest» i listen | `liste_wape` | Hull (M-1) |
| Valgt produkt og produkter hentet på forhånd | spørringsnøkler i AD-12 | OK |

## Tekniske føringer i DESIGN.md

| Føring | Spinen | Status |
|---|---|---|
| Bare systemfonter, ingen `next/font/google` eller CDN | AD-11 | OK (L-9) |
| Offline, Lucide lokalt | AD-11 | OK, men Lucide står ikke i stacken (L-9) |
| Recharts uten animasjon | Stack (3.11.x) | OK. Animasjonen er et frontend-valg. |
| shadcn/ui | Stack | OK, men versjonen er ikke låst (L-10) |

## Åpne punkter i issues.md som gjelder arkitekturen

| Punkt | Løst i spinen | Merknad |
|---|---|---|
| Linje 7: flytte utkastet inn, Alembic eller `create_all` | AD-13 (`create_all` + versjonsvakt) | Løst. Punktet må krysses av (L-12). |
| Linje 13: H6 (total WAPE, verdier per opprinnelse, oppsummering, lagret rapport) | AD-3, AD-4, AD-8, AD-9 | Løst. Oppsummeringen ligger i `GET /datasets/{id}` i stedet for et eget endepunkt, og det holder. |
| Linje 14: fem utdaterte punkter i utkastet | Den avstemte listen i spinen | Løst. Mock-fallback og feature flags er falt ut (M-9). |
| Linje 21: detaljtabellen trenger faktisk, P10, P50 og P90 per modell og opprinnelse | AD-3, AD-9 | Løst |
| Linje 17 og 18: kjøre spiken på nytt, ETS-intervaller for smale | *Deferred* | Riktig utsatt. Ta med avrundingen (M-7). |
| Linje 16: PRD §10 (ERP-formater) | *Deferred* | Riktig utsatt. Tegnkoding bør løses nå (M-8). |

## Utkastet: er noe nyttig falt bort?

- Komponenttabellen, reglene for prognose og backtest, CSV-reglene, API-et og datamodellen er tatt med, rettet og utvidet.
- Det som er falt bort:
  - mock-fallback og feature flags (M-9)
  - listen «Ikke med» (M-9)
  - feltene i `sales` og `forecast` (L-1)
- Det at merknaden om scenariototaler er flyttet fra API-et til frontend, er riktig, fordi EXPERIENCE eier teksten.
