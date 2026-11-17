---
status: final
stepsCompleted: [1, 2, 3, 4]
inputDocuments:
  - _bmad-output/planning-artifacts/prds/prd-G96-ellingsen-2026-11-14/prd.md
  - _bmad-output/planning-artifacts/prds/prd-G96-ellingsen-2026-11-14/addendum.md
  - _bmad-output/planning-artifacts/architecture/architecture-G96-ellingsen-2026-11-17/ARCHITECTURE-SPINE.md
  - _bmad-output/planning-artifacts/ux-designs/ux-G96-ellingsen-2026-11-14/DESIGN.md
  - _bmad-output/planning-artifacts/ux-designs/ux-G96-ellingsen-2026-11-14/EXPERIENCE.md
---

# PROGNOS v1 – epics og stories

## Oversikt

Dette dokumentet deler PROGNOS v1 opp i epics og stories. Det bygger på kravene i PRD-en (med addendum), beslutningene i arkitekturspinen (AD-1 til AD-15) og UX-spesifikasjonen (DESIGN.md og EXPERIENCE.md).

**Regler for alle stories:**

- Hver story oppgir hvilke FR-krav, F-kriterier og AD-regler den dekker.
- Testene skrives i samme story som koden de tester. En story er ikke ferdig før testene er grønne.
- Et krav som er delt over flere stories, merkes *delvis: …* med den delen storyen dekker. Storyen som gjør kravet ferdig, merkes **(fullfører)**.
- Hver story har feltene **Dekker** (FR, F, AD og eventuelt NFR og UX-DR) og **Tester i storyen** i tillegg til akseptansekriteriene.
- Krav-ID-ene følger PRD-en (FR-1 til FR-26, NFR-1 til NFR-9, F1 til F14). Ved konflikt gjelder beslutningsloggen, så PRD-en, så arkitekturen. Faste tekster eies av EXPERIENCE.md.

## Kravinventar

### Funksjonelle krav

**CSV-import og validering (PRD §4.1)**

- **FR-1: Opplasting av CSV.** Kari kan laste opp én CSV-fil med kolonnene `produkt_id`, `maaned` og `antall` fra topplinjen. En gyldig fil gir en valideringsrapport med status godkjent og antall produkter per historikknivå. Ekstra kolonner ignoreres. Fila leses som UTF-8 med eller uten BOM. (UJ-1)
- **FR-2: Automatisk gjenkjenning av skilletegn.** Komma eller semikolon gjenkjennes ut fra overskriftslinja. Samme innhold med komma og semikolon gir identisk salgshistorikk, prognose og backtest. `12,5` i en semikolonfil gir heltallsfeilen fra FR-3. Fila avvises hvis ingen av tegnene gir de tre kolonnene. (F13)
- **FR-3: Validering og avvisning.** Manglende kolonne (nevnt ved navn), ugyldig `maaned`, negativt eller ikke-heltallig `antall`, tom celle, duplikat (produkt, måned og begge radnumrene) og fil uten datarader gir feil. Radnummer = linjenummer, overskriften er linje 1. Én feil avviser hele fila, ingenting lagres, og alle feilene listes. (F4, UJ-2)
- **FR-4: Utfylling av manglende måneder.** Manglende måneder fra produktets første måned til og med siste måned i datasettet fylles med `antall` = 0. Én advarsel per produkt med utfylte måneder, som lister månedene. Fila godkjennes hvis det ikke finnes andre feil. (F14)
- **FR-5: Historikknivå per produkt.** Historikklengde (etter utfylling, begge endepunkter med) gir nivå *ingen* (< 12), *sesongnaiv* (12–23) eller *ets* (≥ 24). *ingen* og *sesongnaiv* flagges med *kort historikk*. Grensetester 11/12 og 23/24. Rapporten viser antall per nivå. (F5)
- **FR-6: Lagring og gjenåpning av datasett.** Godkjent datasett lagres i lokal SQLite. API-svarene for produktliste og ett produkt er like før og etter omstart. Gjenåpning kjører ikke prognose eller backtest på nytt. Ny opplasting av samme fil gir nytt datasett, ingenting overskrives. (F11, UJ-4)
- **FR-7: Automatisk prognosekjøring.** Opplasting, validering, prognose og backtest skjer i én forespørsel. Svaret har datasettets id. Avvist fil starter ingen kjøring. Feiler kjøringen, lagres ingenting og rapporten viser en feilmelding.

**Prognose (PRD §4.2)**

- **FR-8: Prognose per produkt.** Én prognoseserie (6 måneder, P10/P50/P90) per produkt med nivå *ets* eller *sesongnaiv*. Alle `produkt_id` fra input finnes i output. *ingen*-produkter finnes med flagget *kort historikk*, men uten prognose. Horisonten er lik for alle produktene. (F1, F3)
- **FR-9: Prediksjonsintervall og nullgrense.** P10 og P90 er grensene i et 80 % intervall. P10 ≤ P50 ≤ P90 og ingen verdi er negativ. Verdiene rundes halvt opp til heltall etter nullgrensen (PRD §11.3). (F2)
- **FR-10: Modell etter historikknivå.** *sesongnaiv* får bare sesongnaiv prognose, *ingen* får ingen, *ets* får ETS-prognose og sesongnaiv baseline beregnes også. Graf og scenariotabell viser ETS for *ets* og sesongnaiv for *sesongnaiv*. (F5)

**Scenarioer (PRD §4.3)**

- **FR-11: Tre scenarioer per produkt.** Pessimistisk = P10, Forventet = P50, Optimistisk = P90 for hver måned, med Pessimistisk ≤ Forventet ≤ Optimistisk. *ingen* har ingen scenarioer. (F6)
- **FR-12: Scenariototal for horisonten.** Scenariototal = sum av månedsverdiene. Merknaden vises alltid ordrett: «Totalene er summer av månedlige verdier. Det reelle spennet mellom Pessimistisk og Optimistisk er smalere enn det som vises.» (F6)

**Backtest (PRD §4.4)**

- **FR-13: Rullerende backtest.** 6 opprinnelser, 1 måned frem, opprinnelsen flyttes 1 måned om gangen. Et produkt med 36 måneder får 6 backtest-prognoser per modell. Modellen bruker bare historikk til og med opprinnelsen.
- **FR-14: WAPE per produkt og totalt.** WAPE = Σ|faktisk − P50| / Σ faktisk. Total WAPE regnes bare over produkter med backtest for begge modellene. Σ faktisk = 0 gir «–», produktet inngår ikke i totalen og kan ikke få *ETS taper*. ETS har lavere total WAPE enn baseline på det syntetiske datasettet. (F7)
- **FR-15: Intervalldekning.** Dekning for P10–P90 per modell, per produkt og totalt, regnet etter nullgrensen og over samme mengde som total WAPE. Total ETS-dekning på det syntetiske datasettet er mellom 65 % og 95 %. (F8)
- **FR-16: Backtest etter historikklengde.** < 18 mnd: ingen backtest (WAPE «–»). 18–29 mnd: bare baseline-backtest. ≥ 30 mnd: ETS og baseline. Grensetester 17/18 og 29/30.
- **FR-17: Flagget *ETS taper*.** Strengt høyere ETS-WAPE gir flagget, ETS-prognosen vises fortsatt og begge WAPE-tallene vises. Like verdier gir ikke flagget. Produkter uten ETS-backtest får aldri flagget. Testes med en konstruert serie der ETS taper.

**Dashbord (PRD §4.5)**

- **FR-18: Topplinje med datasettvelger, opplasting og valideringsrapport.** Datasettvelgeren viser alle datasett med filnavn og tidspunkt, nyeste valgt. Rapporten vises rett under topplinjen: feil ved avvisning, «✓ 200 produkter godkjent · 3 flagget (kort historikk)» og advarsler ved godkjenning. Valgt datasett viser rapporten fra opplastingen. Etter godkjent opplasting velges det nye datasettet.
- **FR-19: Produktliste med de svakeste øverst.** Rekkefølge: (1) flaggede etter WAPE synkende, uten WAPE sist, (2) uflaggede med WAPE «–», (3) resten etter WAPE synkende. Like verdier etter `produkt_id` stigende. WAPE i listen er ETS-WAPE når ETS-backtest finnes, ellers baseline. Flagg vises. Valg oppdaterer graf og tabeller.
- **FR-20: Graf per produkt.** Historikk, P50 (stiplet) og P10–P90-bånd langs samme månedsakse, loddrett markør ved første horisontmåned. *ingen* viser historikk og «Ingen prognose: under 12 måneders historikk». (F10)
- **FR-21: Scenariotabell og backtest-tabell.** Scenariotabell med scenarioer, total, P10/P50/P90 som forklaring og merknaden. Backtest-tabell med WAPE og dekning for begge modellene og dommer, utvidbar til faktisk og P50 per opprinnelse. Faste tekster «ETS er ikke backtestet (under 30 måneders historikk)» og «Ingen backtest (under 18 måneders historikk)». (F10)
- **FR-22: WAPE-oversikt for alle produkter.** Total WAPE for begge modellene over samme mengde, og «n av m» produkter der ETS slår baseline. Bygger på lagrede data og er lik etter omstart. (F11)
- **FR-26: Søk i produktlisten.** Filtrerer på `produkt_id` (inneholder, uten hensyn til store og små bokstaver). Sorteringen fra FR-19 beholdes. Tomt felt viser alt. Valgt produkt blir stående selv om det faller utenfor filteret.

**Syntetisk datasett (PRD §4.6)**

- **FR-23: Generator med fast seed.** To kjøringer med samme seed gir byte-identisk CSV og fasit. (F9)
- **FR-24: Innholdet i den syntetiske CSV-fila.** 20 produkter med 36 måneder (minst 15 med trend + sesong + støy, minst 2 flate med mye støy), og 4 produkter med 8, 15, 20 og 26 måneder. Fasit (trend, sesongprofil, støynivå) i egen fil. For et støyfritt produkt (nivå ≥ 20) ligger avrundet ETS-P50 innenfor 5 % av fasiten i hver horisontmåned.
- **FR-25: Innlasting ved tom database.** Første oppstart med tom database gir ett datasett. Oppstart med data legger ikke til noe.

### Ikke-funksjonelle krav

- **NFR-1: Lokal kjøring uten Docker, nøkler eller betalte tjenester.** Kommandoene i README starter appen uten Docker, miljøvariabler eller `.env`. UJ-1 fungerer uten nett etter installasjon. README lister forutsetninger med versjoner, kommandoer for installasjon, start og alle testene, og nevner automatisk innlasting (FR-25). (F12)
- **NFR-2: Automatisk database og helsesjekk.** Databasefila opprettes ved første oppstart, og `GET /api/health` svarer OK. (F12)
- **NFR-3: Varig lagring.** Data overlever omstart (se FR-6). (F11)
- **NFR-4: Norsk.** Grensesnitt, feilmeldinger, rapport og dokumentasjon på norsk. Ingen engelske brukertekster utover fagbegrepene i ordlista. Playwright sjekker overskrifter og scenarionavn.
- **NFR-5: Etterprøvbarhet.** Scenariototaler, WAPE og dekning kan regnes etter fra tallene som vises. Et lite testdatasett med håndregnet fasit ligger sammen med testene. (F6, F7, F8)
- **NFR-6: Testdekning.** F1–F14 dekket av automatiske tester som er grønne, F10 med Playwright, og hver testbare konsekvens i FR-1 til FR-26 har minst ett testtilfelle.
- **NFR-7: Svartid.** 200 produkter × 36 måneder gir rapport, prognose og backtest innen 60 s, målt etter én oppvarmingskjøring. Maskinen står i README.
- **NFR-8: Enbrukerapp.** Ingen endepunkter krever autentisering, ingen innloggingsside.
- **NFR-9: Ryddig repo.** Generator, syntetisk CSV og fasit i egen testdatamappe. Databasefila i fast, git-ignorert mappe. Ingen hemmeligheter. `.env.example` forklarer at v1 ikke trenger variabler. `git ls-files` viser ingen `.db`- eller `.env`-filer.

### Tilleggskrav fra arkitekturen

**Startmal (påvirker Epic 1, Story 1):** Arkitekturen bruker ingen ferdig startmal for hele løsningen. Backend opprettes som et `uv`-prosjekt (`backend/pyproject.toml`, `src/prognos/`). Frontend opprettes med `create-next-app` (App Router, TypeScript, Tailwind v4) og `shadcn/ui` init, og deretter fjernes `next/font/google` fra malen (AD-11). Next.js låses til eksakt `16.4.6`.

**AD-regler (bindende for stories):**

- **AD-1: Ren og deterministisk kjerne.** Bare `domene/` kaller statsforecast og regner ut metrikker. `domene/` importerer aldri `fastapi`, `sqlalchemy`, `prognos.api` eller `prognos.db` (håndheves av en importtest). Produkter behandles sortert på `produkt_id`, `n_jobs=1`, ingen `fallback_model`. NaN eller inf er kjøringsfeil.
- **AD-2: Alt eller ingenting, én innlastingsvei, serverfrist.** `db/innlasting.py::last_inn_datasett(innhold, filnavn)` er eneste vei inn, både for opplasting og seed. Én transaksjon. `SERVERFRIST_S = 110` gir `feilet` med kode `tidsavbrudd`. Feilet seeding stopper backend.
- **AD-3: Metrikker regnes én gang i kjernen og lagres.** Tabellene `salg`, `prognose`, `backtest_punkt`, `backtest_metrikk`, felt på `produkt` og `datasett.sammendrag`. API serialiserer uendret, ingen SQL- eller TS-beregning av WAPE, dekning, summer eller rekkefølge.
- **AD-4: Én definisjon av mengden S for totalene.** S = produkter med `backtest_nivaa = begge` og sum_faktisk > 0. Total WAPE, total dekning, `n` og `m` regnes over S. |S| = 0 gir `m = n = 0` og `total_* = null`.
- **AD-5: Nullgrense og heltallsavrunding i én funksjon.** `domene/avrunding.py::rund_ikke_negativ` = `floor(max(x, 0) + 0.5)` på alle P-verdier i prognose og backtest. P10 ≤ P50 ≤ P90 sjekkes etter avrunding, brudd er kjøringsfeil.
- **AD-6: Modell- og backtesttabell i `domene/nivaa.py`.** Grensene 12, 18, 24 og 30 finnes bare der. `freq="MS"`, `AutoETS(season_length=12)`, `SeasonalNaive(season_length=12)`, `level=[80]`. Prognose: ett `forecast(h=6)` per modell. Backtest: ett `cross_validation(h=1, n_windows=6, step_size=1)` per modell. Frontend velger backtest-tilstand bare ut fra `backtest_nivaa`.
- **AD-7: Dommer, flagg og rang er lagrede verdier.** `dommer` ∈ {null, `kan_ikke_sammenlignes`, `ets_slaar`, `ets_taper`, `lik`} ved sammenligning av heltallige `sum_avvik`. `flagg_kort_historikk`, `flagg_ets_taper`, `liste_wape`, `rang` etter FR-19. Frontend sorterer aldri, søket filtrerer i klienten.
- **AD-8: Valideringsrapporten er ett objekt.** Pydantic-modellen `Valideringsrapport` (`status`, `feil[]`, `advarsler[]`, `antall_produkter`, `per_nivaa`, `antall_kort_historikk`). Kjernen bygger `godkjent`/`avvist`, skallet bare `feilet` (kodene `kjoring`, `tidsavbrudd`, `opptatt`, `ugyldig_forespoersel`, `uventet`). Lagres som JSON og returneres uendret.
- **AD-9: Seks endepunkter eid av Pydantic.** `POST /api/datasets` (201/422/500/409), `GET /api/datasets`, `GET /api/datasets/{id}`, `GET …/products`, `GET …/products/{produkt_id:path}`, `GET /api/health`. Månedslister stigende. Alle svar fra POST har formen `{rapport}` med norsk melding. zod-kopi i frontend med kontrakttest mot ekte backend.
- **AD-10: CPU-arbeid i trådpool, én opplasting om gangen.** `run_in_threadpool`, prosessvid `asyncio.Lock`, låst lås gir straks 409. Lesing tar ikke låsen.
- **AD-11: Én origin, lang proxytid, ingen eksterne kall.** Relative `/api/*`, rewrite til `http://127.0.0.1:8000`, `proxyTimeout: 130000`, `agentUpgrade: false`, Next 16.4.6 eksakt, telemetri av i `predev`/`prebuild`, bare systemfonter, ingen CORS, ingen miljøvariabler.
- **AD-12: All datahenting via én klient og TanStack Query.** Én klientkomponent i `app/page.tsx`, `lib/api/klient.ts` med zod og klassifisering (rapport / ingen kontakt / tidsavbrudd etter 120 s). Faste spørringsnøkler, `staleTime: Infinity`, godkjent opplasting invaliderer bare `['datasett']`.
- **AD-13: `create_all` med versjonsvakt.** Vakten kjører før `create_all`. Tom fil initialiseres med `SKJEMAVERSJON`. Gammelt skjema stopper backend med fast norsk melding. Ingen Alembic.
- **AD-14: Testbar app uten miljøvariabler.** `lag_app(db_sti)`, `python -m prognos --db STI --port N`, skalltester med midlertidig fil og `ASGITransport`, Playwright `webServer` med `--db` mot midlertidig fil, F11 ved å lage appen på nytt mot samme fil.
- **AD-15: CSV-leseren og rekkefølgen på feil.** `csv.reader` på `utf-8-sig`, aldri `pandas.read_csv`. Radnummer = `reader.line_num`. Tomme linjer hoppes over, men telles. Regler for valg av skilletegn, regex for `antall` og `maaned`, kodene `antall_felt`, `tom_celle`, `duplikat`, `tegnkoding`, og fast rekkefølge på feilene.

**Konvensjoner fra arkitekturen:**

- Norsk snake_case i CSV, DB, JSON og TS uten alias. Æ/ø/å skrives `ae`/`oe`/`aa`. Modell-id-er `ets` og `sesongnaiv`.
- Måneder som `ÅÅÅÅ-MM`. `opprinnelse` er siste treningsmåned, `maaned` = opprinnelse + 1.
- `opplastet` lagres som naiv UTC og serialiseres med `Z`. Frontend viser i `Europe/Oslo` som «13.11.2026 kl. 09.42».
- Heltall for antall, P-verdier, summer og avvik. WAPE og dekning er urundede brøker. `null` betyr udefinert, aldri 0. All formatering i `frontend/lib/format.ts`.
- Domenefeil i `domene/feil.py`. Logging til stdout, kjøretid per pipelinesteg på INFO.
- Ingen konfigurasjon: konstanter i `prognos/konstanter.py` og `next.config.ts`.
- Faste tekster i `frontend/lib/tekster.ts`, ordrett fra EXPERIENCE.md. Meldinger i rapporten eies av backend.
- Testdata: `testdata/generator.py` (seed 42) skriver `syntetisk.csv` (komma, UTF-8 uten BOM, `\n`, sortert), `fasit.json` (`sort_keys`, `indent=2`, `ensure_ascii=False`, avsluttende `\n`) og `uten_stoy.csv`. Filene sjekkes inn, `.gitattributes` har `testdata/*.csv -text` og `testdata/*.json -text`. Fila på 200 × 36 for NFR-7 genereres i testen.
- Tester: kjernen med pytest uten DB, NFR-5-fasit i `backend/tests/fasit/`, skallet etter AD-14, Playwright mot ekte backend med seed.
- Stack-versjoner som i arkitekturens tabell *Stack* (Python 3.12, FastAPI 0.163.x, statsforecast 2.1.1, pandas 2.3.3, Next.js 16.4.6, React 19.3.x, Tailwind 4.3.x, TanStack Query 5.108.x, zod 4.6.x, Recharts 3.11.x, Vitest 5.1.x, Playwright 1.65.x).
- Ingen CI i v1. Testene kjøres lokalt med kommandoene i README.

### UX-designkrav

**Designtokens og globale overstyringer (DESIGN.md)**

- **UX-DR1: Fargetokens.** Implementer alle fargetokens fra DESIGN.md (`background`, `foreground`, `surface-subtle`, `muted-foreground`, `border`, `input`, `gridline`, `primary`, `primary-foreground`, `primary-subtle`, `ring`, `destructive`, `destructive-subtle`, `chart-*`) som CSS-variabler i Tailwind v4/shadcn-temaet. Bare lys modus.
- **UX-DR2: Typografi.** Bare systemfontstakken. Rollene title 16/600, panel-heading 14/600, body 14/400, table 13/400, label 12/500, caption 12/400. Alle tall med `tabular-nums` og høyrejustert. Ingen versaler eller sperring.
- **UX-DR3: Radius og flater.** `rounded.sm` 2 px (flagg, inndatafelt), `rounded.md` 4 px (knapper, paneler, nedtrekk, tooltip, lasteboks), `full` bare på spinneren. Ingen skygger eller gradienter.
- **UX-DR4: Fokusring.** Global overstyring: 2 px heltrukken `ring`, full opasitet, 2 px offset i `background`. Erstatter shadcns `ring-ring/50`.
- **UX-DR5: Inndatakant.** `Input` og `Select`-trigger bruker `{colors.input}` (#767C85) som kant, aldri `{colors.border}`.
- **UX-DR6: Layoutmål.** Topplinje min. 56 px, produktliste 300 px (260 px ved 1024–1279), panelpadding og -gap 16 px, graf 360 px (300 px under 800 px vindushøyde), feilliste maks 320 px, `min-height` i stedet for `height` på elementer med tekst.

**Komponenter (DESIGN.md + EXPERIENCE.md)**

- **UX-DR7: Topplinje.** `<header>` med ordmerket «PROGNOS», datasettvelger med etiketten «Datasett», primærknappen **Last opp CSV** og kolonnekravet «CSV med kolonnene produkt_id, maaned, antall» under knappen, koblet med `aria-describedby`. Ikke festet.
- **UX-DR8: Datasettvelger.** shadcn `Select`, nyeste øverst og valgt, format «salg_2026-10.csv · 13.11.2026 kl. 09.42». Bytte gir tilstanden *Datasett byttes* uten ny kjøring.
- **UX-DR9: Last opp CSV.** Filvelger avgrenset til `.csv`. Valgt fil starter én forespørsel og lasteboksen. Avbrutt filvelger gjør ingenting. Ingen bekreftelse.
- **UX-DR10: Valideringsrapport, godkjent.** Variant `report-approved`. Sammenfoldet til oppsummeringslinje (mal med entall og utelatt «0 flagget»), fordelingslinjen «Fordeling: ingen {a} · sesongnaiv {b} · ets {c}» og «Vis advarsler ({n})» / «Skjul advarsler» (bare når n > 0). Advarselslinjer etter malen fra FR-4. Folder seg sammen ved bytte av datasett. Overskriften er `<h2>`, ✓ er `aria-hidden`.
- **UX-DR11: Valideringsrapport, rød.** Variant `report-rejected` for *Fil avvist* («Fila ble avvist. Ingenting er lagret.» + «{n} feil»), *Kjøring feilet* («Prognosen kunne ikke kjøres. Ingenting er lagret.» + melding eller tidsavbruddsteksten), *Opplasting pågår allerede* (409-tekst fra backend) og *Ingen kontakt med backend*. Feillisten scroller over 320 px og er da region med `tabindex="0"` og `aria-label="Feil i fila"`. «Lukk» viser godkjent rapport for valgt datasett igjen. Dashbordet viser fortsatt forrige datasett.
- **UX-DR12: Søk i produktlisten.** Synlig etikett «Søk produkt-ID», fortløpende filtrering, teller «Viser {x} av {n}» med `aria-live="polite"` og 500 ms forsinkelse, Esc tømmer, tilstand *Søk uten treff* med «Ingen produkter matcher «{søk}».» og «Tøm søk».
- **UX-DR13: Produktliste.** `<nav aria-label="Produkter">` med ARIA-`listbox` (`aria-label="Produkter, svakeste først"`), roving tabindex, selection follows focus, Home/End, tilgjengelig navn per rad («P-109, WAPE 24,0 %, flagg: ETS taper»). Rad med `produkt_id` og WAPE på linje 1 og flagg på linje 2. Valgt rad med `primary-subtle` og 3 px blå stripe, `aria-selected`. Sticky, egen scroll. Første rad autovelges etter innlasting, godkjent kjøring og datasettbytte. `scrollIntoView({block: 'nearest'})`. Detaljhenting 200 ms etter siste piltast og `prefetchQuery` for naboene. Tab inn: valgt rad får fokus hvis synlig, ellers første treff uten valg.
- **UX-DR14: Flagg-merke.** Lucide-ikon (klokke for *kort historikk*, pil ned for *ETS taper*) + tekst alltid, ikon `aria-hidden`, ikke interaktivt, aldri rødt.
- **UX-DR15: Graf.** Recharts med hele historikken + 6 prognosemåneder, y-akse fra 0, horisontale rutenettlinjer, historikk heltrukket 2 px, P50 stiplet 2 px (6/4), bånd med fyll og 1 px kanter, start i siste faktiske punkt, horisontmarkør med «Prognose →», ingen animasjon. Panelhode «Prognose – {produkt_id}» med «ETS · 6 måneder fram» eller «Sesongnaiv baseline · 6 måneder fram». `role="img"` og `aria-label` etter malen. Legend med «Historikk», «Forventet (P50)», «Spenn Pessimistisk–Optimistisk (P10–P90)». Tooltip med «Faktisk» eller scenarionavnene, Esc skjuler. Nivå *ingen*: bare historikk og den faste teksten.
- **UX-DR16: Historikktabell.** «Vis historikk som tabell» / «Skjul historikktabell», kolonnene Måned · Faktisk, nyeste øverst, «(fylt inn)» ved utfylte måneder. Økten husker om den er åpen.
- **UX-DR17: Scenariotabell.** Kolonnene Måned · Pessimistisk · Forventet · Optimistisk med P10/P50/P90 som undertekst, 6 månedsrader og sumrad i vekt 600, merknaden fra FR-12 alltid under og koblet med `aria-describedby`. Nivå *ingen*: fast tekst i stedet for rader, merknaden står fortsatt.
- **UX-DR18: Backtest-tabell.** Kolonnene *Sesongnaiv baseline* og *ETS* (baseline først), radene WAPE og Intervalldekning, dommerlinjen med fire varianter som tekst. Tilstandene *Ingen backtest*, *Bare baseline-backtest* (fast tekst i ETS-kolonnen, `<th scope="col">ETS</th>` beholdes), *ETS taper*, *Lik WAPE* og *WAPE udefinert*. Skjult «Mål» i øverste venstre celle.
- **UX-DR19: Detaljer per opprinnelse.** «Vis detaljer per opprinnelse (6)» / «Skjul detaljer per opprinnelse», bare når produktet har backtest. Kolonnene Måned · Faktisk · Baseline P50 · Baseline avvik · Baseline i spenn · ETS P50 · ETS avvik · ETS i spenn («ja»/«nei»), sumrad med Σ faktisk og Σ avvik. Bare baseline-kolonnene ved baseline-backtest. Synlig `<caption>` «Detaljer per opprinnelse – {produkt_id}». Økten husker åpen/lukket på tvers av produkter.
- **UX-DR20: WAPE-oversikt.** Én linje, `wape-overview`, festet nederst fra 1024 px med `scroll-padding-bottom`. Malen «Total WAPE: Sesongnaiv baseline {x} % · ETS {y} % · ETS slår baseline for {n} av {m} produkter» og malen for m = 0. Ikke klikkbar.
- **UX-DR21: Lasteboks og kjøring pågår.** App-roten får `inert` og hvitt slør 80 %, boksen ligger utenfor app-roten, har spinner og teksten «Kjører validering og prognose – dette kan ta opptil ett minutt», får fokus (`tabindex="-1"`), teksten skrives i en `role="status"`-region som alltid finnes. Spinner står stille med `prefers-reduced-motion`. Ingen avbrytknapp. Klienten gir opp etter 120 s.
- **UX-DR22: Laste- og feiltilstander per del.** `Skeleton` og `aria-busy="true"` ved *Datasett byttes* (uten slør) og *Produktdetalj lastes* (forrige produkt står i 150 ms). *Produktdetalj kunne ikke hentes*: «Kunne ikke hente data for {produkt_id}» + «Prøv igjen».
- **UX-DR23: Hopplenke.** «Hopp til produktlisten», skjult til fokus, vises som `button-primary`, mål har `tabindex="-1"`.

**Tilgjengelighet, språk og format (EXPERIENCE.md)**

- **UX-DR24: Landemerker.** `<html lang="nb">`, `<header>`, `<main>` med skjult `<h1>` «PROGNOS – dashbord», `<h2>` i hvert panel og i rapporten.
- **UX-DR25: Tab-rekkefølge og fokusstyring.** Rekkefølgen hopplenke → datasettvelger → Last opp CSV → rapport → søk → produktliste → historikkknapp → detaljknapp → scrollende regioner. Etter kjøring (godkjent, avvist, feilet) går fokus til rapportoverskriften. Etter «Lukk» til **Last opp CSV**. Fokus havner aldri på `<body>`. Resultat annonseres ved fokusflytting, ikke `aria-live`.
- **UX-DR26: Tabeller tilgjengelige.** Ekte `<table>` med `<caption>`, `<th scope="row">` for måned og «Sum», `<th scope="col">` for kolonner. Statiske tabeller er ikke tabstopp.
- **UX-DR27: Tall- og datoformat.** Antall med `Intl.NumberFormat('nb-NO')` (hardt mellomrom), WAPE med én desimal, dekning i hele prosent, mellomrom før %, komma som desimaltegn. Udefinert WAPE som «–» med skjult «udefinert» eller «ingen backtest». Måneder som «nov. 2026» i graf og tabeller, `ÅÅÅÅ-MM` i rapporten. Alt i `lib/format.ts`.
- **UX-DR28: Faste tekster.** Alle faste tekster fra EXPERIENCE.md (*Faste tekster* og *Øvrige faste tekster*) ligger ordrett i `frontend/lib/tekster.ts`. Ingen engelske brukertekster, ingen utropstegn, ingen anbefalinger.
- **UX-DR29: Responsiv layout og reflow.** ≥ 1280 full layout, 1024–1279 tettere, < 1024 én kolonne (topplinje → rapport → liste → graf → scenario → backtest → detaljer → WAPE), liste ikke sticky med `max-height: max(50vh, 240px)`, WAPE-linjen ikke festet, lasteboks `max-width: calc(100vw - 32px)`, graf og tabeller med vannrett scroll som navngitte fokuserbare regioner. Playwright ved 1280 × 720, 1280 × 1080 og 320 × 256.
- **UX-DR30: Forbudte mønstre.** Ingen modaler, bekreftelsesdialoger, toast-varsler, uendelig scrolling, grafanimasjoner, trafikklysfarger, KPI-kort eller mørk modus.

### Dekningskart for FR

Fire krav er delt over flere epics: FR-7, FR-19, FR-22 og FR-24. Hver story som dekker en del av et slikt krav, sier hvilken del den dekker (*delvis: …*). Storyen som fullfører kravet, er merket **(fullfører)**.

| Krav | Epic | Del |
|---|---|---|
| FR-1 | Epic 3 | Opplasting av CSV |
| FR-2 | Epic 3 | Gjenkjenning av skilletegn |
| FR-3 | Epic 3 | Validering og avvisning |
| FR-4 | Epic 3 | Utfylling av manglende måneder |
| FR-5 | Epic 3 | Historikknivå og flagget *kort historikk* |
| FR-6 | Epic 3 | Lagring og gjenåpning |
| FR-7 | Epic 3 → 4 → 5 | Epic 3: én forespørsel med validering og lagring. Epic 4: prognosen i samme forespørsel. Epic 5: backtesten i samme forespørsel (fullfører) |
| FR-8 | Epic 4 | Prognose per produkt |
| FR-9 | Epic 4 | Intervall, nullgrense og avrunding |
| FR-10 | Epic 4 | Modell etter historikknivå |
| FR-11 | Epic 4 | Tre scenarioer |
| FR-12 | Epic 4 | Scenariototal (beregning). Merknaden vises i Epic 6 |
| FR-13 | Epic 5 | Rullerende backtest |
| FR-14 | Epic 5 | WAPE per produkt og totalt |
| FR-15 | Epic 5 | Intervalldekning |
| FR-16 | Epic 5 | Backtest etter historikklengde |
| FR-17 | Epic 5 | Flagget *ETS taper* |
| FR-18 | Epic 6 | Topplinje, datasettvelger og rapport |
| FR-19 | Epic 3 → 5 → 6 | Epic 3: `rang` etter flagget *kort historikk* og `produkt_id`, uten WAPE. Epic 5: `liste_wape` og full `rang` med WAPE. Epic 6: produktlisten i dashbordet (fullfører) |
| FR-20 | Epic 6 | Graf |
| FR-21 | Epic 6 | Scenariotabell og backtest-tabell |
| FR-22 | Epic 5 → 6 | Epic 5: `sammendrag` i backend. Epic 6: WAPE-oversikten i dashbordet (fullfører) |
| FR-23 | Epic 2 | Generator med fast seed |
| FR-24 | Epic 2 → 4 | Epic 2: innhold og fasit. Epic 4: 5 %-testen mot fasiten med ETS (fullfører) |
| FR-25 | Epic 3 | Innlasting ved tom database |
| FR-26 | Epic 6 | Søk i produktlisten |

NFR-6 (testdekning) gjelder alle epics, fordi testene skrives i samme story som koden.

## Epic-liste

### Epic 1: Kjørbart prosjektskjelett med helsesjekk
Sensor kan klone repoet og starte backend og frontend med kommandoene i README, uten Docker, miljøvariabler eller nøkler. Databasefila opprettes automatisk, og `GET /api/health` svarer OK både direkte og gjennom Next-proxyen.
**Dekker:** NFR-1, NFR-2, NFR-8, NFR-9 · F12 · AD-1, AD-9, AD-11, AD-13, AD-14

### Epic 2: Syntetisk datasett med seed 42
Gruppen og sensor kan generere en kjent salgshistorikk med fasit. Den dekker alle historikknivåene og backtest-grensene og er byte-identisk ved hver kjøring.
**Dekker:** FR-23, FR-24 (delvis: innhold og fasit) · F9 · NFR-9

### Epic 3: CSV-import, validering og lagring
Kari kan laste opp en CSV gjennom API-et og få en fullstendig valideringsrapport med alle feilene og radnumrene, eller en godkjenning med utfylling, historikknivå og flagget *kort historikk*. Datasettet lagres og kan hentes uendret etter omstart. Det syntetiske datasettet lastes inn automatisk når databasen er tom.
**Dekker:** FR-1–FR-6, FR-7 (delvis), FR-19 (delvis), FR-25 · F4, F5, F11, F13, F14 · AD-2, AD-8, AD-9, AD-10, AD-13, AD-15

### Epic 4: Prognose med prediksjonsintervall og scenarioer
Hvert produkt med nok historikk får en prognose for 6 måneder med P10, P50 og P90 i hele tall og uten negative verdier, med modell etter historikknivå. Kari får de tre scenarioene med scenariototal, lagret og servert av API-et.
**Dekker:** FR-7 (delvis), FR-8–FR-12, FR-24 (fullfører) · F1, F2, F3, F5, F6, F13 · AD-3, AD-5, AD-6 · NFR-5

### Epic 5: Backtest mot sesongnaiv baseline
Kari kan se om ETS treffer bedre enn «samme måned i fjor»: WAPE og intervalldekning per produkt og totalt, dommer, flagget *ETS taper*, rangering og WAPE-sammendrag, lagret og etterprøvbart. Hele kjøringen skjer i én forespørsel innen 60 s.
**Dekker:** FR-7 (fullfører), FR-13–FR-17, FR-19 (delvis), FR-22 (delvis) · F7, F8, F11, F13 · AD-3, AD-4, AD-7 · NFR-5, NFR-7

### Epic 6: Dashbord på én side
Kari gjør hele arbeidsflyten i nettleseren: opplasting, rapport, produktlisten med de svakeste øverst, graf, scenarioer, backtest, WAPE-oversikt og gjenåpning av lagrede datasett, med tastatur og skjermleser.
**Dekker:** FR-18, FR-19 (fullfører), FR-20, FR-21, FR-22 (fullfører), FR-26 · F10 · NFR-4, NFR-6 · AD-9, AD-12 · UX-DR1–UX-DR30

## Epic 1: Kjørbart prosjektskjelett med helsesjekk

Sensor kan klone repoet og starte backend og frontend med kommandoene i README, uten Docker, miljøvariabler eller nøkler. Databasefila opprettes automatisk, og `GET /api/health` svarer OK både direkte og gjennom Next-proxyen. Etter denne epicen finnes testoppsettet for pytest, Vitest og Playwright, så alle senere stories kan skrive testene sine i samme story.

### Story 1.1: Backend-skjelett med automatisk database og helsesjekk

Som sensor,
vil jeg starte backend med én kommando og få en database og en helsesjekk som svarer,
slik at jeg vet at backend kjører uten oppsett, nøkler eller Docker.

**Dekker:** NFR-2 · NFR-8 · NFR-9 (delvis: databasefila i git-ignorert mappe) · F12 (delvis: backend) · AD-1 (importtesten) · AD-9 (delvis: `GET /api/health` og norsk `{detail}`) · AD-13 · AD-14

**Akseptansekriterier:**

**Given** et tomt repo med Python 3.12 og uv installert
**When** backend opprettes som et uv-prosjekt i `backend/` med `src/prognos/` (`domene/`, `db/`, `api/`, `konstanter.py`, `oppstart.py`, `main.py`, `__main__.py`) og versjonene fra arkitekturens *Stack*-tabell låst i `pyproject.toml`
**Then** `uv run uvicorn prognos.main:app --port 8000` fra `backend/` starter backend uten miljøvariabler eller `.env`-fil
**And** `main.py::lag_app(db_sti: Path) -> FastAPI` er eneste fabrikk, og `app = lag_app(STANDARD_DB_STI)` med `STANDARD_DB_STI` i `konstanter.py` peker til `backend/data/prognos.db`
**And** `python -m prognos --db STI --port N` starter appen mot en annen databasefil

**Given** at databasefila ikke finnes
**When** backend starter
**Then** fila og mappen opprettes automatisk, tabellen `skjemaversjon` opprettes med `create_all`, og `SKJEMAVERSJON` settes inn i samme transaksjon (AD-13)
**And** `GET /api/health` svarer `200 {"status": "ok"}`

**Given** en databasefil som har tabeller, men der `skjemaversjon` mangler eller har en annen verdi enn `SKJEMAVERSJON`
**When** backend starter
**Then** vakten kjører før `create_all`, og backend stopper med meldingen «Databasefila har gammelt skjema. Slett backend/data/prognos.db og start på nytt.»

**Given** at backend kjører
**When** en klient kaller en ukjent `GET`-sti under `/api/`
**Then** svaret er `404` med `{detail}` på norsk (AD-9)
**And** ingen endepunkter krever autentisering (NFR-8)

**Given** pakken `prognos.domene`
**When** importtesten kjører
**Then** ingen modul i `domene/` importerer `fastapi`, `sqlalchemy`, `prognos.api` eller `prognos.db` (AD-1)

**Given** `.gitignore`
**When** backend har kjørt
**Then** `backend/data/*.db` er ignorert av git

**Tester i storyen:**
- pytest: `/api/health` gir 200 og `{"status": "ok"}` gjennom `lifespan_context` og `httpx.AsyncClient(transport=ASGITransport(app))` mot en midlertidig fil (AD-14).
- pytest: databasefila og `skjemaversjon` opprettes ved første oppstart. En ny oppstart mot samme fil går fint.
- pytest: versjonsvakten stopper med den faste meldingen både når `skjemaversjon` mangler og når versjonen er feil.
- pytest: en ukjent `GET`-sti gir 404 med norsk `{detail}`.
- pytest: importtesten for `domene/` (AD-1).
- pytest: `python -m prognos --db` bruker den oppgitte fila (argumentparsingen testes uten å starte uvicorn).

### Story 1.2: Frontend-skjelett med proxy til backend

Som sensor,
vil jeg starte frontend med `npm run dev` og nå backend gjennom samme adresse,
slik at appen kjører lokalt uten CORS, miljøvariabler eller nettkall.

**Dekker:** NFR-1 (delvis: frontend uten miljøvariabler, systemfonter, telemetri av) · F12 (delvis: frontend) · AD-11 · AD-14 (delvis: Playwright `webServer`)

**Akseptansekriterier:**

**Given** Node.js ≥ 22.12
**When** frontend opprettes i `frontend/` med `create-next-app` (App Router, TypeScript, Tailwind v4) og `shadcn init`
**Then** `package.json` har `"next": "16.4.6"` uten `^` eller `~`, og de andre versjonene følger *Stack*-tabellen
**And** importen av `next/font/google` er fjernet, og siden bruker bare systemfonter
**And** `<html lang="nb">` er satt, og forsiden viser en enkel norsk plassholder med ordmerket «PROGNOS»

**Given** `next.config.ts`
**When** frontend starter
**Then** det finnes en rewrite fra `/api/:path*` til `http://127.0.0.1:8000/api/:path*`
**And** `experimental` har `proxyTimeout: 130000` og `agentUpgrade: false`
**And** `predev` og `prebuild` slår av Next-telemetrien uten miljøvariabler

**Given** at backend og frontend kjører
**When** nettleseren kaller `http://localhost:3000/api/health`
**Then** svaret er `200 {"status": "ok"}` fra backend gjennom proxyen

**Given** kildekoden i `frontend/`
**When** den sjekkes
**Then** ingen kode leser `process.env`, og ingen kode kaller absolutte URL-er mot backend eller eksterne tjenester

**Given** Playwright-oppsettet
**When** `npx playwright test` kjører
**Then** `webServer` starter backend med `--db` mot en midlertidig fil og frontend med `npm run dev`, og testene kjører mot dem (AD-14)

**Tester i storyen:**
- Vitest: `package.json` har `next` låst til nøyaktig `16.4.6`.
- Vitest: `next.config.ts` eksporterer riktig rewrite, `proxyTimeout: 130000` og `agentUpgrade: false`.
- Vitest: ingen fil under `frontend/app`, `frontend/components` eller `frontend/lib` inneholder `next/font/google` eller `process.env`.
- Playwright: `GET /api/health` gjennom frontend-adressen gir `{"status": "ok"}`.
- Playwright: forsiden har `lang="nb"` og viser «PROGNOS».

### Story 1.3: README, repohygiene og kontroll av oppstarten

Som sensor,
vil jeg ha en README som forteller nøyaktig hva jeg må installere og hvilke kommandoer jeg skal kjøre,
slik at jeg kan starte appen og kjøre alle testene uten hjelp fra gruppen.

**Dekker:** NFR-1 (delvis: README og offline-kjøring) · NFR-9 (fullfører) · F12 (fullfører)

**Akseptansekriterier:**

**Given** README i rotmappa
**When** sensor leser den
**Then** den lister forutsetningene med versjoner (Python 3.12, uv 0.13.x, Node.js ≥ 22.12)
**And** den har kommandoene for installasjon, start av backend (`uv run uvicorn prognos.main:app --port 8000` fra `backend/`), start av frontend (`npm run dev` fra `frontend/`), `uv run pytest`, `npm test` og `npx playwright test`
**And** den sier at v1 ikke trenger Docker, miljøvariabler, nøkler eller betalte tjenester, og at bare installasjonen trenger nett
**And** README er på norsk (NFR-4)

**Given** repoet
**When** `git ls-files` kjøres
**Then** det finnes ingen `.db`- eller `.env`-filer
**And** `.env.example` finnes og forklarer at v1 ikke trenger miljøvariabler

**Given** en maskin uten Docker og uten `.env`
**When** sensor følger README og kobler fra nettverket etter installasjonen
**Then** backend og frontend starter, databasefila opprettes, og `GET /api/health` svarer OK gjennom frontend (F12)

**Tester i storyen:**
- pytest: `git ls-files` lister ingen `.db`- eller `.env`-filer, og `.env.example` finnes (NFR-9).
- pytest: README inneholder hver av start- og testkommandoene ordrett, så de ikke kan forsvinne i en senere endring.
- Manuell kontroll (F12, NFR-1): oppstart etter README med nettverket koblet fra. Resultatet føres i sesjonsloggen med dato og maskin. Senere stories utvider README med automatisk innlasting (Story 3.7) og maskinen for NFR-7 (Story 5.5).

## Epic 2: Syntetisk datasett med seed 42

Gruppen og sensor kan generere en kjent salgshistorikk med fasit. Den dekker alle historikknivåene og backtest-grensene og er byte-identisk ved hver kjøring. Filene sjekkes inn, slik at senere epics kan bruke dem i tester og ved oppstart. Generatoren importerer ikke backend (arkitekturens importregler).

### Story 2.1: Generator for syntetisk salgshistorikk med fasit

Som gruppe,
vil jeg ha et skript som med seed 42 lager en syntetisk CSV-fil og en fasit med kjent trend, sesong og støy,
slik at vi kan sjekke prognosen og backtesten mot data der vi vet svaret.

**Dekker:** FR-23 · FR-24 (delvis: innholdet i `syntetisk.csv` og fasiten, uten 5 %-testen) · F9 · NFR-9 (delvis: egen mappe for testdata) · konvensjonen *Testdata*

**Akseptansekriterier:**

**Given** `testdata/generator.py`
**When** det kjøres med `uv run --project backend python testdata/generator.py` (seed 42 som standard)
**Then** det skriver `testdata/syntetisk.csv` og `testdata/fasit.json`
**And** generatoren bruker bare standardbiblioteket og numpy (`numpy.random.default_rng(seed)`), og importerer ikke noe fra `backend/`

**Given** den genererte `syntetisk.csv`
**When** den leses
**Then** den har overskriften `produkt_id,maaned,antall`, komma som skilletegn, UTF-8 uten BOM og `\n` som linjeskift, og radene er sortert på `produkt_id` og `maaned`
**And** alle `antall` er heltall ≥ 0, alle `maaned` er på formatet `ÅÅÅÅ-MM`, og det finnes ingen duplikater og ingen manglende måneder, så fila blir godkjent etter reglene i FR-3
**And** alle produktene slutter i samme siste måned, som er en konstant i generatoren

**Given** innholdet i `syntetisk.csv`
**When** produktene telles
**Then** 20 produkter har 36 måneders historikk. Minst 15 av dem har trend i tillegg til sesong og støy, og minst 2 er flate serier med mye støy (FR-24)
**And** 4 produkter har kortere historikk: ett med 8, ett med 15, ett med 20 og ett med 26 måneder. Dermed dekkes historikknivåene *ingen*, *sesongnaiv* og *ets* og backtest-nivåene *ingen*, *sesongnaiv* og *begge*

**Given** `fasit.json`
**When** den leses
**Then** den har én oppføring per produkt med trend, sesongprofil (12 faktorer) og støynivå
**And** den er skrevet med `sort_keys=True`, `indent=2`, `ensure_ascii=False` og avsluttende `\n`

**Given** to kjøringer med samme seed
**When** filene sammenlignes
**Then** både `syntetisk.csv` og `fasit.json` er byte-identiske (F9)
**And** en kjøring med en annen seed gir en annen `syntetisk.csv`

**Given** at parameterne for produktene er satt
**When** generatoren endres senere
**Then** trend og støy er ikke justert produkt for produkt for å få bedre WAPE. De flate seriene med mye støy beholdes (SM-C1). Dette står som kommentar øverst i generatoren.

**Tester i storyen:**
- pytest (`backend/tests/testdata/`): generatoren kjøres to ganger med seed 42 i hver sin midlertidige mappe, og begge filene er byte-identiske (F9).
- pytest: filene som er sjekket inn, er byte-identiske med en ny generering, så de ikke kan bli utdatert.
- pytest: format på CSV (overskrift, skilletegn, ingen BOM, `\n`, sortering, heltall ≥ 0, ingen duplikater og ingen hull).
- pytest: antall produkter per historikklengde (20 × 36, og 8, 15, 20 og 26), felles siste måned, og minst 15 med trend og minst 2 flate med mye støy ifølge fasiten.
- pytest: `fasit.json` har riktige felt per produkt og riktig formatering.
- pytest: generatoren importerer ingenting fra `prognos` (statisk sjekk av importene).

### Story 2.2: Støyfritt kontrollprodukt og stort datasett for svartid

Som gruppe,
vil jeg kunne lage et støyfritt kontrollprodukt og et datasett på Karis størrelse med samme generator,
slik at 5 %-testen mot fasiten og svartidstesten har data uten at vi lager egne generatorer senere.

**Dekker:** FR-24 (delvis: `uten_stoy.csv` som grunnlag for 5 %-testen) · NFR-7 (delvis: datagrunnlaget for tidtakingen) · NFR-9 (fullfører for testdata) · konvensjonen *Testdata*

**Akseptansekriterier:**

**Given** generatoren
**When** den kjøres med standardvalgene
**Then** den skriver også `testdata/uten_stoy.csv` med ett produkt som har 36 måneder, kjent trend og sesong, ingen støy og et nivå på minst 20 i hver måned
**And** fasiten for produktet står i `fasit.json`, inkludert de forventede verdiene for de 6 månedene etter siste måned

**Given** generatoren
**When** den kjøres med valg for antall produkter, antall måneder og utfil (for eksempel `--produkter 200 --maaneder 36 --ut STI`)
**Then** den skriver en gyldig CSV med 200 produkter × 36 måneder i samme format som `syntetisk.csv`
**And** denne fila sjekkes ikke inn

**Given** `.gitattributes`
**When** filene i `testdata/` sjekkes inn
**Then** `.gitattributes` har `testdata/*.csv -text` og `testdata/*.json -text` i tillegg til den globale regelen `eol=lf`, så Git ikke endrer bytes på Windows
**And** `syntetisk.csv`, `fasit.json` og `uten_stoy.csv` er sjekket inn

**Tester i storyen:**
- pytest: `uten_stoy.csv` har ett produkt med 36 måneder, nivå ≥ 20 i hver måned, og verdier som stemmer nøyaktig med fasiten (etter avrunding til heltall).
- pytest: `uten_stoy.csv` er byte-identisk ved ny generering.
- pytest: valgene for stort datasett gir 200 × 36 rader i riktig format, skrevet til en midlertidig mappe.
- pytest: `.gitattributes` inneholder de to reglene for `testdata/`.
- 5 %-testen mot ETS kommer i Story 4.2, og tidtakingen for NFR-7 i Story 5.5.

## Epic 3: CSV-import, validering og lagring

Kari kan laste opp en CSV gjennom API-et og få en fullstendig valideringsrapport: enten alle feilene med radnummer, eller en godkjenning med utfylling, historikknivå og flagget *kort historikk*. Datasettet lagres og kan hentes uendret etter omstart, og det syntetiske datasettet lastes inn automatisk når databasen er tom. Epicen lager den eneste innlastingsveien (AD-2) og alle de seks endepunktene. Epic 4 og 5 fyller inn prognose- og backtest-feltene uten å lage en ny vei inn.

### Story 3.1: CSV-leser med gjenkjenning av skilletegn

Som Kari,
vil jeg kunne laste opp fila slik Excel lagrer den, med komma eller semikolon og med eller uten BOM,
slik at jeg slipper å velge skilletegn eller lagre fila på en spesiell måte.

**Dekker:** FR-1 (delvis: lesing, UTF-8 med og uten BOM, ekstra kolonner) · FR-2 · FR-3 (delvis: feil i fila som helhet) · F4 (delvis: manglende kolonne) · F13 (delvis: lesing) · AD-1 · AD-15 · NFR-4

**Akseptansekriterier:**

**Given** `domene/csv.py`, `domene/typer.py` og `domene/feil.py`
**When** CSV-leseren får bytes
**Then** den dekoder med `utf-8-sig` og bruker `csv.reader`, aldri `pandas.read_csv`
**And** alle verdier leses som `str` og `strip()`-es, og overskriftene skiller mellom store og små bokstaver
**And** radnummeret for hver rad er `reader.line_num`, med overskriften som linje 1
**And** linjer der alle cellene er tomme, hoppes over, men telles med i radnummeret

**Given** en fil med kolonnene `produkt_id`, `maaned` og `antall` og eventuelt flere kolonner
**When** fila leses
**Then** kolonner utover de tre påkrevde ignoreres uten feil (FR-1)

**Given** en overskriftslinje
**When** skilletegnet velges
**Then** det tegnet (`,` eller `;`) som gir flest påkrevde kolonner, velges
**And** hvis ingen av dem gir noen påkrevd kolonne, eller begge gir like mange, gir det feilen `skilletegn` med meldingen «Fant ikke kolonnene produkt_id, maaned og antall med komma eller semikolon som skilletegn»
**And** hvis det valgte tegnet gir færre enn tre påkrevde kolonner, gir det én `mangler_kolonne`-feil per kolonne som mangler, med meldingen «Mangler påkrevd kolonne: {kolonne}»

**Given** en fil som ikke kan dekodes som UTF-8
**When** den leses
**Then** gir det feilen `tegnkoding` med meldingen «Fila er ikke lagret som UTF-8. Lagre den som «CSV UTF-8» i Excel og prøv igjen.»

**Given** en fil med bare overskrift, eller med bare tomme linjer etter overskriften
**When** den leses
**Then** gir det feilen `ingen_datarader` med meldingen «Fila har ingen datarader»

**Given** det samme innholdet lagret med komma og med semikolon
**When** begge leses
**Then** gir de de samme radene med de samme radnumrene (F13, lesedelen)

**Tester i storyen:**
- pytest uten DB: UTF-8 med og uten BOM gir samme resultat.
- pytest: ekstra kolonner ignoreres, også når de står før de påkrevde.
- pytest: valg av skilletegn for komma, semikolon, uavgjort og ingen treff.
- pytest: hver feilkode i fila som helhet (`tegnkoding`, `skilletegn`, `mangler_kolonne`, `ingen_datarader`) med ordrett melding.
- pytest: radnummer med tomme linjer midt i fila.
- pytest: komma og semikolon gir like rader (F13).

### Story 3.2: Validering av rader med fullstendig feilliste

Som Kari,
vil jeg se alle feilene i fila på én gang, med radnummer jeg kan slå opp i Excel,
slik at jeg kan rette alt i én omgang og ikke prøve meg fram.

**Dekker:** FR-3 · F4 · AD-8 (delvis: `Valideringsrapport` og status `avvist`) · AD-15 · NFR-4 · UJ-2

**Akseptansekriterier:**

**Given** Pydantic-modellen `Valideringsrapport` i `domene/typer.py`
**When** den defineres
**Then** den har feltene `status` (`godkjent`, `avvist` eller `feilet`), `feil[]` med `{kode, melding, rader[]}`, `advarsler[]` med `{produkt_id, maaneder[], melding}`, `antall_produkter`, `per_nivaa` med `{ingen, sesongnaiv, ets}` og `antall_kort_historikk`

**Given** rader fra CSV-leseren
**When** `domene/validering.py` validerer dem
**Then** gir hver av disse en feil med radnummer og ordrett melding fra EXPERIENCE.md:
- tom celle i en påkrevd kolonne: `tom_celle`, «Rad {r}: tom celle i {kolonne}»
- flere felt enn overskriften: `antall_felt`, «Rad {r}: har {k} felt, men overskriften har {h}». Færre felt der en påkrevd celle mangler, gir `tom_celle`
- `maaned` som ikke matcher `^\d{4}-(0[1-9]|1[0-2])$`: `maaned_format`, «Rad {r}: maaned må ha formatet ÅÅÅÅ-MM med måned 01–12»
- `antall` som ikke matcher `^[0-9]+$` (negativt, desimal eller tekst): `antall_ugyldig`, «Rad {r}: antall må være et heltall ≥ 0»
- samme `produkt_id` og `maaned` igjen: `duplikat`, én feil per ekstra rad, «Duplikat: {produkt_id}, {maaned} (rad {første} og {r})»

**Given** en fil med flere feil
**When** den valideres
**Then** lister rapporten **alle** feilene, ikke bare den første
**And** feilene i fila som helhet kommer først, deretter radfeil etter radnummer og innenfor en rad etter kolonnerekkefølgen
**And** status er `avvist`

**Given** en semikolonfil der `antall` er `12,5`
**When** den valideres
**Then** gir det `antall_ugyldig` og ikke en feil om skilletegnet (FR-2)

**Given** en kommafil der `antall` er `12,5`
**When** den valideres
**Then** gir det `antall_felt` for raden

**Given** at `produkt_id` er `"001"` i én rad og `"1"` i en annen
**When** de valideres
**Then** er de to ulike produkter

**Tester i storyen:**
- pytest uten DB: én test per feilkode med ordrett melding og radnummer.
- pytest: UJ-2-eksempelet (duplikat og `12,5` i samme fil) gir begge feilene i riktig rekkefølge.
- pytest: tre duplikater av samme produkt og måned gir to feil som begge viser til første rad.
- pytest: rekkefølgen er stabil ved like rader og flere feil i samme rad.
- pytest: `12,5` med semikolon og med komma gir hver sin kode.
- pytest: `"001"` og `"1"` er ulike produkter.

### Story 3.3: Utfylling, historikknivå og godkjent rapport

Som Kari,
vil jeg at manglende måneder fylles med 0 og at produkter med kort historikk flagges,
slik at jeg vet hvilke produkter jeg må vurdere selv og hvilke tall som er fylt inn.

**Dekker:** FR-4 · FR-5 · F14 · F5 (delvis: historikknivå og flagget *kort historikk*) · FR-19 (delvis: `rang` etter FR-19 når ingen produkter har WAPE ennå) · AD-6 (delvis: tabellen i `nivaa.py`) · AD-7 (delvis: `flagg_kort_historikk` og `rang`) · AD-8 (delvis: status `godkjent`) · AD-4 (delvis: `sammendrag` med tom mengde *S*)

**Akseptansekriterier:**

**Given** en godkjent mengde rader
**When** `domene/utfylling.py` kjører
**Then** fylles manglende måneder fra produktets første måned til og med siste måned i datasettet med `antall` = 0 og `utfylt` = sant
**And** et produkt som mangler de siste månedene frem til siste måned i datasettet, får dem fylt med 0
**And** det gis én advarsel per produkt med utfylte måneder, med meldingen «{produkt_id}: {antall} måned(er) fylt inn med 0 ({ÅÅÅÅ-MM}, …)». Advarslene sorteres på `produkt_id`, og månedene stigende

**Given** `domene/nivaa.py`
**When** historikklengden regnes ut
**Then** telles begge endepunktene med, fra produktets første måned til og med siste måned i datasettet, etter utfylling
**And** `nivaa.py` er eneste kilde for grensene 12, 18, 24 og 30, og setter `historikknivaa`, `prognosemodell` og `backtest_nivaa` etter tabellen i AD-6

**Given** produkter med 11, 12, 17, 18, 23, 24, 29 og 30 måneder
**When** de klassifiseres
**Then** får de nivå, prognosemodell og backtest-nivå nøyaktig som tabellen i AD-6 viser
**And** `flagg_kort_historikk` er sant for nivå `ingen` og `sesongnaiv`

**Given** `domene/pipeline.py` i første versjon
**When** den får bytes og filnavn
**Then** returnerer den enten en `Valideringsrapport` med status `avvist`, eller et `Kjoreresultat` med salg, produkter og en rapport med status `godkjent`
**And** rapporten har `antall_produkter`, `per_nivaa` og `antall_kort_historikk`, der `per_nivaa.ingen + per_nivaa.sesongnaiv = antall_kort_historikk`
**And** produktene behandles sortert på `produkt_id`
**And** `domene/rangering.py` setter `liste_wape` = `null`, `flagg_ets_taper` = usant, `dommer` = `null` og `rang` etter reglene i FR-19: flaggede først og deretter uflaggede, og innenfor hver gruppe etter `produkt_id` stigende med Pythons `str`-sammenligning
**And** `sammendrag` har `m = 0`, `n = 0` og alle `total_*` = `null`, slik AD-4 sier når *S* er tom

**Tester i storyen:**
- pytest uten DB: én manglende måned gir én utfylt måned og én advarsel (F14).
- pytest: manglende siste måneder fylles frem til siste måned i datasettet.
- pytest: advarselsteksten er ordrett med entall og flertall, og sorteringen er riktig.
- pytest: grensetestene 11/12, 17/18, 23/24 og 29/30 for alle tre feltene (F5, FR-5, FR-16).
- pytest: historikklengden 2024-11 til 2026-10 er 24.
- pytest: `per_nivaa` og `antall_kort_historikk` stemmer for `syntetisk.csv`.
- pytest: `rang` gir flaggede først og deretter `produkt_id`, også når `produkt_id` har ulik lengde.
- pytest: pipelinen gir samme `Kjoreresultat` to ganger på samme input (AD-1).

### Story 3.4: Opplasting gjennom API-et med lagring i én transaksjon

Som Kari,
vil jeg laste opp fila og få valideringsrapporten tilbake i samme svar,
slik at en godkjent fil lagres som et datasett, og en avvist eller feilet fil aldri etterlater noe.

**Dekker:** FR-1 (delvis: opplasting gjennom API) · FR-3 (delvis: ingenting lagres ved avvisning) · FR-6 (delvis: lagring) · FR-7 (delvis: én forespørsel med validering og lagring, avvist fil starter ingen kjøring, feilet kjøring lagrer ingenting) · AD-2 · AD-8 (delvis: status `feilet` fra skallet, kodene `kjoring`, `uventet` og `ugyldig_forespoersel`) · AD-9 (delvis: `POST /api/datasets` med 201, 422 og 500) · AD-10 (delvis: pipelinen i trådpool) · AD-13 (ny `SKJEMAVERSJON`)

**Akseptansekriterier:**

**Given** SQLAlchemy-modellene i `db/`
**When** skjemaet opprettes
**Then** finnes tabellene `datasett` (`id`, `filnavn`, `opplastet`, `skilletegn`, `siste_maaned`, `rapport` som JSON, `sammendrag` som JSON), `salg` (`antall`, `utfylt`) og `produkt` (`historikklengde`, `historikknivaa`, `prognosemodell`, `backtest_nivaa`, `dommer`, `flagg_kort_historikk`, `flagg_ets_taper`, `liste_wape`, `rang`), med sammensatte primærnøkler som begynner med (`datasett_id`, `produkt_id`)
**And** `SKJEMAVERSJON` er økt, så en databasefil fra Story 1.1 stopper med meldingen fra AD-13

**Given** `db/innlasting.py::last_inn_datasett(innhold: bytes, filnavn: str)`
**When** den kalles
**Then** kjører den pipelinen med `run_in_threadpool` og skriver `datasett` og alle barnetabeller i **én** `AsyncSession`-transaksjon
**And** `opplastet` lagres som naiv UTC
**And** dette er den eneste veien inn i databasen

**Given** en godkjent fil
**When** Kari sender `POST /api/datasets` med feltet `fil`
**Then** er svaret `201 {datasett_id, rapport}` med status `godkjent`

**Given** en avvist fil
**When** den sendes
**Then** er svaret `422 {rapport}` med status `avvist`, og det finnes ingen nye rader i noen tabell

**Given** at pipelinen kaster et uventet unntak eller gir en ikke-endelig verdi
**When** fila sendes
**Then** er svaret `500 {rapport}` med status `feilet` og én feil med kode `kjoring` eller `uventet` og norsk melding, og ingenting lagres
**And** det uventede unntaket logges med stakk til stdout

**Given** en forespørsel uten feltet `fil` eller med feil form
**When** den sendes
**Then** gir globale unntakshåndterere `{rapport}` med status `feilet`, koden `ugyldig_forespoersel` og norsk melding

**Given** samme fil lastet opp to ganger
**When** begge opplastingene er godkjent
**Then** finnes det to datasett, og det første er uendret (FR-6)

**Tester i storyen:**
- pytest (AD-14): godkjent opplasting gir 201 og rader i `datasett`, `salg` og `produkt`.
- pytest: avvist opplasting gir 422 og null nye rader i alle tabeller.
- pytest: et konstruert unntak i pipelinen gir 500 med `kjoring` eller `uventet` og null nye rader.
- pytest: manglende `fil` gir `ugyldig_forespoersel` i formen `{rapport}`.
- pytest: samme fil to ganger gir to datasett.
- pytest: databasefil med gammel `SKJEMAVERSJON` stopper backend.

### Story 3.5: Én opplasting om gangen og serverfrist

Som Kari,
vil jeg få beskjed med en gang hvis en annen opplasting allerede kjører, og få et tydelig svar hvis kjøringen tar for lang tid,
slik at «Ingenting er lagret» alltid er sant, og to kjøringer aldri konkurrerer om maskinen.

**Dekker:** FR-7 (delvis: ingenting lagres ved tidsavbrudd) · AD-2 (delvis: `SERVERFRIST_S` og koden `tidsavbrudd`) · AD-8 (delvis: kodene `tidsavbrudd` og `opptatt`) · AD-9 (delvis: `409 {rapport}`) · AD-10 · NFR-2 (helsesjekken svarer under kjøring) · NFR-4

**Akseptansekriterier:**

**Given** `SERVERFRIST_S = 110` i `konstanter.py`
**When** pipelinen bruker mer enn fristen
**Then** forkastes resultatet uten skriving, og svaret er `500 {rapport}` med status `feilet`, koden `tidsavbrudd` og norsk melding
**And** fristen kan sendes inn som parameter til `last_inn_datasett`, slik at testene kan bruke en lav frist uten miljøvariabler

**Given** at en innlasting allerede pågår
**When** en ny `POST /api/datasets` kommer
**Then** svarer backend straks `409 {rapport}` med status `feilet`, koden `opptatt` og meldingen «En annen opplasting pågår allerede. Vent til den er ferdig, og prøv igjen.»
**And** låsen er en prosessvid `asyncio.Lock` som tas før pipelinen starter

**Given** at serverfristen har gått ut, men pipelinetråden fortsatt kjører
**When** en ny opplasting kommer
**Then** er låsen fortsatt holdt, og svaret er 409, til tråden er ferdig

**Given** at en innlasting pågår
**When** en klient kaller `GET /api/health` eller et av lese-endepunktene
**Then** svarer de uten å vente på innlastingen, og lesing tar aldri låsen

**Tester i storyen:**
- pytest (AD-14): lav frist og en treg pipeline gir `500` med `tidsavbrudd` og null nye rader.
- pytest: to samtidige opplastinger gir én 201 og én 409 med ordrett melding.
- pytest: etter tidsavbrudd gir en ny opplasting 409 til pipelinetråden er ferdig, og deretter 201.
- pytest: `/api/health` svarer mens en treg innlasting pågår.
- pytest: låsen er sluppet etter avvisning, feilet kjøring og godkjent kjøring.

### Story 3.6: Lese-endepunkter og gjenåpning etter omstart

Som Kari,
vil jeg kunne hente opp et lagret datasett med rapport, produkter og salgshistorikk,
slik at jeg kan fortsette neste dag uten å laste opp eller kjøre noe på nytt.

**Dekker:** FR-6 · F11 (delvis: rapport, salg og produktfelt) · F13 (delvis: salgshistorikk) · F5 (delvis: nivå og flagg gjennom API) · AD-3 (delvis: API serialiserer lagrede verdier uendret) · AD-8 (rapporten lagres og returneres uendret) · AD-9 (delvis: de fire lese-endepunktene) · NFR-3 · UJ-4

**Akseptansekriterier:**

**Given** lagrede datasett
**When** Kari kaller `GET /api/datasets`
**Then** får hun `[{id, filnavn, opplastet}]` sortert på `opplastet` og deretter `id`, nyeste først
**And** `opplastet` er serialisert som ISO 8601 med `Z`

**Given** et lagret datasett
**When** Kari kaller `GET /api/datasets/{id}`
**Then** får hun `{id, filnavn, opplastet, skilletegn, siste_maaned, rapport, sammendrag}`, og `rapport` er samme JSON-verdi som ble lagret ved opplastingen

**Given** et lagret datasett
**When** Kari kaller `GET /api/datasets/{id}/products`
**Then** får hun `[{produkt_id, historikknivaa, backtest_nivaa, liste_wape, flagg_kort_historikk, flagg_ets_taper, rang}]` sortert på `rang`

**Given** et produkt i et lagret datasett
**When** Kari kaller `GET /api/datasets/{id}/products/{produkt_id:path}`
**Then** får hun `{produkt_id, historikklengde, historikknivaa, prognosemodell, backtest_nivaa, dommer, flagg_kort_historikk, flagg_ets_taper, historikk[{maaned, antall, utfylt}], prognose[], scenariototal: null, backtest: {sesongnaiv: null, ets: null}}`
**And** `historikk` er sortert stigende på `maaned`
**And** en `produkt_id` med `/` eller mellomrom kan hentes når den er URL-kodet

**Given** et ukjent datasett eller produkt
**When** det hentes
**Then** er svaret 404 med `{detail}` på norsk

**Given** at backend lages på nytt med `lag_app` mot samme databasefil
**When** de samme fire endepunktene kalles
**Then** er svarene identiske med svarene før omstarten (F11, FR-6)
**And** ingen lesing kjører pipelinen, og lesing tar ikke opplastingslåsen

**Given** samme innhold lastet opp med komma og med semikolon
**When** produktdetaljene hentes
**Then** er `historikk` og produktfeltene identiske. Bare `filnavn`, `opplastet`, `skilletegn` og `id` er ulike (F13, salgshistorikkdelen)

**Tester i storyen:**
- pytest (AD-14): hvert endepunkt gir riktig form og sortering.
- pytest: `rapport` fra `GET /api/datasets/{id}` er lik `rapport` fra `POST`-svaret.
- pytest: F11-test ved å lage appen på nytt mot samme fil og sammenligne alle fire svarene.
- pytest: F13-test med komma og semikolon gjennom API-et.
- pytest: `produkt_id` med `/` hentes med URL-koding.
- pytest: 404 med norsk `{detail}` for ukjent datasett og ukjent produkt.
- pytest: en spion på pipelinen viser at lesing ikke kjører den.

### Story 3.7: Syntetisk datasett ved første oppstart

Som sensor,
vil jeg se data med en gang appen starter første gang,
slik at jeg kan prøve PROGNOS uten å ha en egen CSV-fil.

**Dekker:** FR-25 · AD-2 (seeding gjennom `last_inn_datasett`, og feilet seeding stopper backend) · AD-10 (seedingen tar samme lås som opplastingen) · AD-13 · NFR-1 (delvis: README nevner automatisk innlasting)

**Akseptansekriterier:**

**Given** en tom databasefil
**When** backend starter
**Then** kjører `oppstart.py` versjonsvakten, `create_all` og `seed_if_empty` i den rekkefølgen
**And** `seed_if_empty` leser `testdata/syntetisk.csv` og kaller `last_inn_datasett` med filnavnet `syntetisk.csv`
**And** `GET /api/datasets` gir nøyaktig ett datasett

**Given** en databasefil som allerede har minst ett datasett
**When** backend starter
**Then** legges det ikke til noe nytt

**Given** at seedingen feiler (for eksempel fordi fila mangler eller blir avvist)
**When** backend starter
**Then** stopper backend med en norsk feilmelding

**Given** at seedingen og en opplasting begge går gjennom `last_inn_datasett`
**When** låsen fra Story 3.5 tas
**Then** gjelder den samme prosessvide låsen begge veiene inn (AD-2, AD-10)

**Given** README
**When** sensor leser den
**Then** står det at det syntetiske datasettet lastes inn automatisk ved første oppstart

**Tester i storyen:**
- pytest (AD-14): første oppstart med tom fil gir ett datasett med status `godkjent`.
- pytest: andre oppstart mot samme fil gir fortsatt ett datasett.
- pytest: en manglende seedfil (stien sendes inn i testen) stopper oppstarten med norsk melding.
- pytest: README nevner automatisk innlasting.
- pytest: `seed_if_empty` tar den samme låsen som `POST /api/datasets` (en opplasting som holder låsen, gjør at seedingen venter).
- Playwright-testene fra Story 1.2 starter fortsatt, nå med seed.

## Epic 4: Prognose med prediksjonsintervall og scenarioer

Hvert produkt med nok historikk får en prognose for 6 måneder med P10, P50 og P90 i hele tall og uten negative verdier, med modell etter historikknivået. Kari får de tre scenarioene med scenariototal, lagret og servert av API-et. Prognosen kjøres i samme forespørsel som valideringen, gjennom innlastingsveien fra Epic 3.

### Story 4.1: Prognose per produkt med nullgrense og heltallsavrunding

Som Kari,
vil jeg få en prognose for de neste 6 månedene med et nedre og et øvre anslag for hvert produkt med nok historikk,
slik at jeg slipper å bygge prognosen i regneark og ser hvor usikker den er.

**Dekker:** FR-8 · FR-9 · FR-10 · F1 · F2 · F3 (delvis: i kjernen) · F5 (delvis: modellvalget) · AD-1 · AD-5 · AD-6 (delvis: `forecast`-kallet)

**Akseptansekriterier:**

**Given** `domene/avrunding.py`
**When** `rund_ikke_negativ(x)` kalles
**Then** returnerer den `np.floor(np.maximum(x, 0) + 0.5)` som `int64`
**And** dette er den eneste funksjonen som runder P-verdier

**Given** produkter med `prognosemodell` `ets` og `sesongnaiv` fra `nivaa.py`
**When** `domene/modeller.py` lager prognosen
**Then** kjøres ett `forecast(h=6)`-kall per modell over alle produktene med den `prognosemodell`
**And** `ds` er `pd.Timestamp` for den første i måneden, `freq="MS"`, modellene er `AutoETS(season_length=12)` og `SeasonalNaive(season_length=12)` med `level=[80]`, og P10 er `-lo-80` og P90 er `-hi-80`
**And** statsforecast kjøres med `n_jobs=1` og uten `fallback_model`, og produktene behandles sortert på `produkt_id`

**Given** prognoseverdiene fra statsforecast
**When** de behandles
**Then** sjekkes det først at alle verdier er endelige. NaN eller inf gir en kjøringsfeil (`domene/feil.py`)
**And** deretter kalles `rund_ikke_negativ` på P10, P50 og P90
**And** deretter sjekkes P10 ≤ P50 ≤ P90 for hver måned, og brudd gir en kjøringsfeil

**Given** et produkt med historikknivå `ets` (24 måneder eller mer)
**When** prognosen lages
**Then** får det ETS-prognosen, og bare den lagres som produktets prognose (FR-10)

**Given** et produkt med historikknivå `sesongnaiv` (12–23 måneder)
**When** prognosen lages
**Then** får det bare den sesongnaive prognosen

**Given** et produkt med historikknivå `ingen` (under 12 måneder)
**When** prognosen lages
**Then** får det ingen prognose, men det finnes fortsatt i resultatet (F3)

**Given** et datasett med flere produkter
**When** prognosen lages
**Then** er horisonten de 6 månedene etter siste måned i datasettet, lik for alle produktene, på formatet `ÅÅÅÅ-MM`

**Tester i storyen:**
- pytest uten DB: `rund_ikke_negativ` på negative tall, .5-grensen (2,5 → 3, −0,4 → 0) og store tall.
- pytest: én CSV med 24 måneder for ett produkt gir 6 måneder med P10, P50 og P90 (F1).
- pytest: P10 ≤ P50 ≤ P90 og ingen negative verdier for alle produktene i `syntetisk.csv` (F2).
- pytest: en serie nær 0 der statsforecast gir negative grenser, blir 0 etter nullgrensen (F2).
- pytest: et konstruert NaN-resultat gir en kjøringsfeil.
- pytest: modellvalget for 11, 12, 23 og 24 måneder (F5, FR-10).
- pytest: alle `produkt_id` fra input finnes i output, og *ingen*-produkter har ingen prognose (F3).
- pytest: horisonten er lik for alle produktene og starter måneden etter siste måned i datasettet.
- pytest: to kjøringer på samme input gir identiske prognoser (AD-1).

### Story 4.2: Scenarioer, scenariototaler og kontroll mot fasiten

Som Kari,
vil jeg se prognosen som Pessimistisk, Forventet og Optimistisk, med totaler for de 6 månedene,
slik at jeg har et tall å gi videre til MRP og et spenn å bruke i samtalen om sikkerhetsmargin.

**Dekker:** FR-11 · FR-12 (delvis: beregningen av scenariototalen. Merknaden vises i Story 6.6) · FR-24 (fullfører: 5 %-testen mot fasiten) · F6 (delvis: i kjernen) · NFR-5 (delvis: håndregnet fasit for scenariototaler) · AD-3 (delvis: scenariototal regnes i kjernen) · AD-5

**Akseptansekriterier:**

**Given** `domene/scenario.py`
**When** den får en avrundet prognose for et produkt
**Then** er Pessimistisk = P10, Forventet = P50 og Optimistisk = P90 for hver måned
**And** Pessimistisk ≤ Forventet ≤ Optimistisk i hver måned
**And** `scenario_p10`, `scenario_p50` og `scenario_p90` er summene av P10, P50 og P90 over de 6 månedene, regnet bare fra de avrundede heltallene

**Given** et produkt med historikknivå `ingen`
**When** scenarioene lages
**Then** har det ingen scenarioer, og alle tre totalene er `null`

**Given** `backend/tests/fasit/`
**When** NFR-5-fasiten for scenarioene legges inn
**Then** finnes det en liten håndskrevet prognose (heltall) med håndregnede scenariototaler, og testen sender den direkte til `scenario.py`

**Given** `testdata/uten_stoy.csv` og fasiten i `fasit.json`
**When** prognosen lages for produktet
**Then** ligger den avrundede ETS-P50 innenfor 5 % av fasiten i hver av de 6 månedene i horisonten (FR-24)
**And** hvis testen feiler, føres det som et funn i `issues.md`. Fasiten og generatoren justeres ikke for å få testen grønn (SM-C1)

**Tester i storyen:**
- pytest uten DB: scenarioverdiene er identiske med P10, P50 og P90 i hver måned (F6).
- pytest: Pessimistisk ≤ Forventet ≤ Optimistisk for alle produktene i `syntetisk.csv` (F6).
- pytest: scenariototalene mot den håndregnede fasiten i `tests/fasit/` (NFR-5).
- pytest: *ingen*-produkter har `null` i alle tre totalene.
- pytest: 5 %-testen på `uten_stoy.csv` mot `fasit.json` (FR-24).

### Story 4.3: Prognose og scenarioer i opplastingen og i API-et

Som Kari,
vil jeg at prognosen og scenarioene lages automatisk når fila er godkjent, og at de er der når jeg åpner datasettet igjen,
slik at jeg slipper å trykke på noe mer og kan stole på at tallene ikke endrer seg.

**Dekker:** FR-7 (delvis: prognose og scenarioer i samme forespørsel) · FR-8 (gjennom API) · F1, F2, F3 og F6 (fullfører gjennom API) · F5 (fullfører) · F11 (delvis: prognose og scenariototal etter omstart) · F13 (delvis: prognosen) · AD-2 · AD-3 (delvis: tabellen `prognose` og scenariofeltene) · AD-9 (delvis: `prognose` og `scenariototal` i produktdetaljen) · AD-13 (ny `SKJEMAVERSJON`)

**Akseptansekriterier:**

**Given** skjemaet
**When** det opprettes
**Then** finnes tabellen `prognose` med (`datasett_id`, `produkt_id`, `maaned`) som nøkkel og `p10`, `p50` og `p90` som heltall
**And** `produkt` har feltene `scenario_p10`, `scenario_p50` og `scenario_p90` (`NULL` uten prognose)
**And** `SKJEMAVERSJON` er økt

**Given** `domene/pipeline.py`
**When** en fil er godkjent
**Then** kjører pipelinen prognose (Story 4.1) og scenarioer (Story 4.2) etter klassifiseringen, og `Kjoreresultat` inneholder dem
**And** `last_inn_datasett` skriver prognosene og scenariofeltene i samme transaksjon som resten
**And** en kjøringsfeil i prognosen gir `500 {rapport}` med koden `kjoring`, og ingenting lagres

**Given** et lagret produkt med prognose
**When** Kari kaller `GET /api/datasets/{id}/products/{produkt_id}`
**Then** har svaret `prognose[{maaned, p10, p50, p90}]` med 6 måneder sortert stigende, og `scenariototal{p10, p50, p90}` med de lagrede summene, serialisert uendret
**And** `prognosemodell` er `ets` eller `sesongnaiv` etter historikknivået

**Given** et lagret produkt med historikknivå `ingen`
**When** det hentes
**Then** er `prognose` en tom liste og `scenariototal` `null`

**Given** at backend lages på nytt mot samme databasefil
**When** produktdetaljene hentes
**Then** er `prognose` og `scenariototal` identiske med svarene før omstarten (F11)

**Given** samme innhold lastet opp med komma og med semikolon
**When** produktdetaljene hentes
**Then** er `prognose` og `scenariototal` identiske (F13, prognosedelen)

**Tester i storyen:**
- pytest (AD-14): opplasting av en CSV med 24 måneder for ett produkt gir 6 prognosemåneder med P10, P50 og P90 gjennom API-et (F1).
- pytest: opplasting av `syntetisk.csv` gir prognose for alle *ets*- og *sesongnaiv*-produkter, ingen for *ingen*, og alle `produkt_id` finnes i `GET …/products` (F3, F5).
- pytest: P10 ≤ P50 ≤ P90 og ingen negative verdier i alle API-svarene (F2).
- pytest: `scenariototal` er lik summen av `prognose` i API-svaret (F6).
- pytest: en kjøringsfeil i prognosen gir 500 og null nye rader i alle tabeller.
- pytest: F11 for `prognose` og `scenariototal` ved at appen lages på nytt.
- pytest: F13 for prognosen med komma og semikolon.
- pytest: databasefil med forrige `SKJEMAVERSJON` stopper backend.

## Epic 5: Backtest mot sesongnaiv baseline

Kari kan se om ETS treffer bedre enn «samme måned i fjor»: WAPE og intervalldekning per produkt og totalt, dommer, flagget *ETS taper*, rangering og WAPE-sammendrag, lagret og etterprøvbart. Etter denne epicen kjøres hele løpet i én forespørsel innen 60 s, og FR-7 er ferdig. Prinsippet *baseline først* gjelder: ETS får aldri en WAPE uten at baseline har en ved siden av.

### Story 5.1: Rullerende backtest i kjernen

Som Kari,
vil jeg at modellene etterprøves på de siste 6 månedene, én måned frem om gangen,
slik at jeg kan se hvor godt de ville ha truffet på salg jeg allerede kjenner.

**Dekker:** FR-13 · FR-16 · AD-1 · AD-5 · AD-6 (delvis: `cross_validation`-kallet og mapping av måneder)

**Akseptansekriterier:**

**Given** produkter med `backtest_nivaa` fra `nivaa.py`
**When** `domene/backtest.py` kjører
**Then** kjøres ett `cross_validation(h=1, n_windows=6, step_size=1)`-kall per modell over alle produktene som skal backtestes med den modellen: `sesongnaiv` for `backtest_nivaa` ∈ {`sesongnaiv`, `begge`} og `ets` for `begge`
**And** serier med ulik lengde går i samme kall, med `freq="MS"`, `level=[80]`, `n_jobs=1` og uten `fallback_model`
**And** produkter med `backtest_nivaa = ingen` tas ikke med

**Given** resultatet fra `cross_validation`
**When** det mappes
**Then** blir `cutoff` til `opprinnelse` og `ds` til `maaned`, begge på formatet `ÅÅÅÅ-MM`, og `maaned` = `opprinnelse` + 1 måned
**And** de 6 `maaned`-verdiene er de 6 siste månedene i datasettet, like for alle produktene

**Given** P10, P50 og P90 fra backtesten
**When** de behandles
**Then** sjekkes det at verdiene er endelige, så kalles `rund_ikke_negativ`, så sjekkes P10 ≤ P50 ≤ P90, akkurat som i prognosen (AD-5)
**And** hvert backtest-punkt får `faktisk`, `p10`, `p50`, `p90`, `avvik` = |faktisk − p50| og `i_spenn` = p10 ≤ faktisk ≤ p90, alle regnet fra heltallene

**Given** et produkt med 36 måneders historikk
**When** backtesten kjører
**Then** får det 6 backtest-punkter per modell, ett for hver av de siste 6 månedene (FR-13)

**Given** et produkt
**When** en verdi etter en opprinnelse endres
**Then** endres ikke backtest-punktet for den opprinnelsen. Modellen bruker bare historikk til og med opprinnelsen (FR-13)

**Given** produkter med 17, 18, 29 og 30 måneder
**When** backtesten kjører
**Then** får 17 ingen backtest, 18 og 29 bare baseline-backtest, og 30 begge (FR-16)

**Tester i storyen:**
- pytest uten DB: 36 måneder gir 6 punkter per modell med riktige `opprinnelse` og `maaned`.
- pytest: grensetestene 17/18 og 29/30 (FR-16).
- pytest: et produkt med 24–29 måneder får ETS-prognose, men bare baseline-backtest.
- pytest: endring av en verdi etter en opprinnelse endrer ikke punktet for den opprinnelsen (FR-13).
- pytest: `avvik` og `i_spenn` regnes fra avrundede heltall, også når P10 er avrundet opp til faktisk.
- pytest: med nøyaktig 12 treningspunkter gir SeasonalNaive P10 = P50 = P90 uten feil (AD-5).
- pytest: to kjøringer gir identiske punkter (AD-1).

### Story 5.2: WAPE, intervalldekning og totaler

Som Kari,
vil jeg få WAPE og intervalldekning per modell, per produkt og totalt, regnet slik at jeg kan regne det etter,
slik at jeg kan vise at metoden treffer bedre enn baseline, og se det når den ikke gjør det.

**Dekker:** FR-14 (delvis: beregning i kjernen) · FR-15 (delvis: beregning i kjernen) · FR-22 (delvis: `sammendrag` i kjernen) · NFR-5 (delvis: håndregnet fasit for WAPE og dekning) · AD-3 (delvis: `backtest_metrikk`) · AD-4

**Akseptansekriterier:**

**Given** backtest-punktene for et produkt og en modell
**When** `domene/metrikker.py` regner
**Then** får `backtest_metrikk` feltene `antall_punkt` (alltid 6), `sum_faktisk`, `sum_avvik`, `wape` = sum_avvik / sum_faktisk, `antall_treff` og `dekning` = antall_treff / antall_punkt
**And** `wape` er `null` når sum_faktisk = 0
**And** metrikker lages bare for modeller som er backtestet

**Given** alle produktene i et datasett
**When** sammendraget regnes
**Then** er mengden *S* produktene med `backtest_nivaa = begge` og sum_faktisk > 0
**And** `total_wape[modell]` = Σ sum_avvik / Σ sum_faktisk over *S*, og `total_dekning[modell]` = Σ antall_treff / Σ antall_punkt over *S*
**And** `m` = |*S*|
**And** når |*S*| = 0 er `m = 0`, `n = 0` og alle `total_*` `null`
**And** produkter med bare baseline-backtest får WAPE per produkt, men inngår ikke i totalen (FR-14)

**Given** `backend/tests/fasit/`
**When** NFR-5-fasiten for backtesten legges inn
**Then** finnes det håndskrevne backtest-punkter (heltall) for noen få produkter, med håndregnet WAPE, dekning, totaler og `m`, og et produkt med sum_faktisk = 0 og et produkt med bare baseline-backtest er med
**And** testene sender punktene direkte til `metrikker.py`, uten AutoETS

**Tester i storyen:**
- pytest uten DB: WAPE og dekning per produkt mot den håndregnede fasiten (NFR-5).
- pytest: totalene og `m` mot fasiten. Produktet med sum_faktisk = 0 og produktet med bare baseline er utenfor *S*.
- pytest: `wape` er `null` når sum_faktisk = 0.
- pytest: |*S*| = 0 gir `m = 0`, `n = 0` og `null` i alle totalene.
- pytest: total WAPE er ikke gjennomsnittet av WAPE per produkt (et tilfelle der de er ulike).

### Story 5.3: Dommer, flagget *ETS taper* og rangering med WAPE

Som Kari,
vil jeg at produktene der ETS taper mot baseline, flagges og står øverst sammen med de svakeste prognosene,
slik at jeg bruker tiden min på produktene der jeg bør være skeptisk.

**Dekker:** FR-17 · FR-19 (delvis: `liste_wape` og full `rang` i backend) · FR-14 (delvis: produkter med WAPE «–» kan ikke få *ETS taper*) · FR-22 (delvis: `n` i `sammendrag`) · AD-7

**Akseptansekriterier:**

**Given** metrikkene for et produkt
**When** `dommer` settes
**Then** er den `null` når `backtest_nivaa ≠ begge`
**And** ellers `kan_ikke_sammenlignes` når sum_faktisk = 0
**And** ellers er den resultatet av å sammenligne heltallene `sum_avvik[ets]` og `sum_avvik[sesongnaiv]`: mindre gir `ets_slaar`, større gir `ets_taper`, og like gir `lik`
**And** `n` i `sammendrag` er antallet i *S* med `dommer = ets_slaar`

**Given** dommeren
**When** flaggene settes
**Then** er `flagg_ets_taper` sant bare når `dommer = ets_taper`
**And** like WAPE-verdier gir ikke flagget, og produkter uten ETS-backtest får det aldri
**And** et produkt med *ETS taper* beholder ETS som `prognosemodell` og ETS-prognosen (FR-17)

**Given** produktene i et datasett
**When** `domene/rangering.py` regner
**Then** er `liste_wape` ETS-WAPE når `backtest_nivaa = begge`, ellers baseline-WAPE, ellers `null`
**And** `rang` = 1…N følger FR-19:
  1. Flaggede produkter etter `liste_wape` synkende, med `null` sist
  2. Uflaggede produkter med `liste_wape` `null`
  3. Resten etter `liste_wape` synkende
**And** like verdier sorteres etter `produkt_id` stigende med Pythons `str`-sammenligning
**And** WAPE-verdiene sammenlignes som brøken sum_avvik / sum_faktisk, slik at rekkefølgen er stabil

**Given** en konstruert CSV der ETS taper mot baseline (for eksempel et brudd i nivået rett før backtest-perioden), uavhengig av det syntetiske datasettet
**When** den kjøres gjennom kjernen
**Then** får produktet `dommer = ets_taper` og `flagg_ets_taper` = sant, og begge WAPE-tallene finnes (FR-17)
**And** CSV-fila lagres som `backend/tests/data/ets_taper.csv` (minst 30 måneder, så produktet får backtest for begge modellene), slik at Playwright-testene i Epic 6 kan laste den opp

**Tester i storyen:**
- pytest uten DB: alle fem dommerverdiene med håndskrevne metrikker, også `lik`.
- pytest: like `sum_avvik` gir `lik` og ikke flagget.
- pytest: produkter med bare baseline-backtest har `dommer = null` og aldri flagget.
- pytest: FR-19-rekkefølgen med en håndskrevet liste som har alle tre gruppene, `null` blant de flaggede og like WAPE-verdier.
- pytest: `liste_wape` velger ETS når den finnes, ellers baseline.
- pytest: den konstruerte serien der ETS taper, gjennom de ekte modellene (FR-17).

### Story 5.4: Backtest i opplastingen og i API-et

Som Kari,
vil jeg at backtesten kjøres automatisk med prognosen, og at tallene er de samme når jeg åpner datasettet igjen,
slik at jeg kan stole på dem og regne dem etter fra tallene som vises.

**Dekker:** FR-7 (fullfører: hele løpet i én forespørsel) · FR-14 (fullfører) · FR-15 (fullfører) · FR-16 og FR-17 (gjennom API) · FR-19 (delvis: `GET …/products` sortert på full `rang`) · FR-22 (delvis: `sammendrag` gjennom API) · F7 · F8 · F11 (fullfører) · F13 (fullfører) · AD-3 · AD-9 (delvis: `backtest` i produktdetaljen) · AD-13 (ny `SKJEMAVERSJON`)

**Akseptansekriterier:**

**Given** skjemaet
**When** det opprettes
**Then** finnes tabellene `backtest_punkt` (per produkt, modell og `maaned`: `opprinnelse`, `faktisk`, `p10`, `p50`, `p90`, `avvik`, `i_spenn`) og `backtest_metrikk` (per produkt og modell: `antall_punkt`, `sum_faktisk`, `sum_avvik`, `wape`, `antall_treff`, `dekning`)
**And** `SKJEMAVERSJON` er økt

**Given** `domene/pipeline.py`
**When** en fil er godkjent
**Then** kjører pipelinen validering, utfylling, klassifisering, prognose, scenarioer, backtest, metrikker, dommer, rang og sammendrag i den rekkefølgen
**And** `last_inn_datasett` skriver alt i én transaksjon, og en feil i backtesten gir `500 {rapport}` og ingen rader
**And** kjøretiden per pipelinesteg logges på INFO

**Given** et lagret produkt
**When** Kari kaller `GET /api/datasets/{id}/products/{produkt_id}`
**Then** har `backtest` nøklene `sesongnaiv` og `ets`, der hver er `null` eller `{metrikk{antall_punkt, sum_faktisk, sum_avvik, wape, antall_treff, dekning}, punkter[{maaned, opprinnelse, faktisk, p10, p50, p90, avvik, i_spenn}]}`
**And** punktene er sortert stigende på `maaned`, og verdiene er serialisert uendret fra databasen
**And** `dommer`, `flagg_ets_taper` og `liste_wape` er de lagrede verdiene

**Given** et lagret datasett
**When** Kari kaller `GET /api/datasets/{id}/products` og `GET /api/datasets/{id}`
**Then** er produktlisten sortert på den lagrede `rang`, og `sammendrag` har `total_wape`, `total_dekning`, `n` og `m` fra kjernen
**And** ingen SQL-`SUM` eller `AVG` brukes til å regne ut noe av dette (AD-3)

**Given** det syntetiske datasettet
**When** det er lastet inn
**Then** er `total_wape.ets` lavere enn `total_wape.sesongnaiv` (F7)
**And** `total_dekning.ets` ligger mellom 0,65 og 0,95 (F8)
**And** hvis F7 eller F8 feiler, føres det som et funn i `issues.md`. Datasettet justeres ikke for å få testen grønn (SM-C1), og intervallnivået endres ikke (SM-C2). Dette lukker også det åpne punktet om å kjøre spiken på nytt mot `syntetisk.csv`
**And** en F7- eller F8-test som feiler, merkes med `pytest.mark.xfail(strict=True)` og en `reason` som viser til funnet i `issues.md` (se beslutningsloggen i `docs/research/research-plan.md`)

**Given** at backend lages på nytt mot samme databasefil
**When** alle de fire lese-endepunktene kalles
**Then** er svarene identiske med svarene før omstarten, inkludert backtest og `sammendrag` (F11)

**Given** samme innhold med komma og med semikolon
**When** begge lastes opp
**Then** er salgshistorikk, prognose og backtest identiske for alle produktene (F13)

**Tester i storyen:**
- pytest (AD-14): opplasting av `syntetisk.csv` gir `backtest` i riktig form for produkter med nivå `ingen`, `sesongnaiv` og `begge`.
- pytest: F7 mot `sammendrag.total_wape` på det syntetiske datasettet.
- pytest: F8 mot `sammendrag.total_dekning.ets` på det syntetiske datasettet.
- pytest: `wape` i `metrikk` er lik `sum_avvik / sum_faktisk` fra punktene i samme svar (NFR-5 gjennom API-et).
- pytest: produktlisten er sortert på `rang`, og de flaggede står først.
- pytest: en kjøringsfeil i backtesten gir 500 og null nye rader i alle tabeller.
- pytest: F11 for alle lese-endepunktene ved at appen lages på nytt.
- pytest: F13 for hele resultatet med komma og semikolon.
- pytest: databasefil med forrige `SKJEMAVERSJON` stopper backend.

### Story 5.5: Svartid for et datasett på Karis størrelse

Som Kari,
vil jeg at en fil med 200 produkter og 36 måneder er ferdig behandlet innen ett minutt,
slik at jeg kan laste opp månedens tall og fortsette arbeidet med en gang.

**Dekker:** NFR-7 · NFR-1 (delvis: README nevner maskinen. Kontrollen av UJ-1 uten nett kommer i Story 6.8) · AD-2 (serverfristen holder for Karis størrelse) · AD-10

**Akseptansekriterier:**

**Given** generatorens valg for stort datasett fra Story 2.2
**When** testen lager en fil med 200 produkter × 36 måneder i en midlertidig mappe
**Then** sjekkes ikke fila inn

**Given** den store fila
**When** den lastes opp to ganger gjennom `POST /api/datasets`
**Then** er den første kjøringen en oppvarming, og tiden for den måles og skrives ut, uten grense
**And** den andre kjøringen gir `201` med rapport, prognose og backtest innen 60 sekunder (NFR-7)

**Given** at testen tar tid
**When** testene kjøres
**Then** er tidtakingen merket som treg i pytest og kjøres med en egen kommando som står i README
**And** README oppgir maskinen tiden er målt på (prosessor, minne og operativsystem) og den målte tiden

**Given** at den kalde kjøringen nærmer seg `SERVERFRIST_S = 110` sekunder
**When** det skjer
**Then** føres det som et funn i `issues.md`, i tråd med *Deferred* i arkitekturen (oppvarming ved oppstart)

**Tester i storyen:**
- pytest (merket treg): oppvarming og deretter tidtaking under 60 s for 200 × 36 gjennom API-et.
- pytest: README inneholder kommandoen for de trege testene og en linje om maskinen.

## Epic 6: Dashbord på én side

Kari gjør hele arbeidsflyten i nettleseren: opplasting, rapport, produktlisten med de svakeste øverst, graf, scenarioer, backtest, WAPE-oversikt og gjenåpning av lagrede datasett, med tastatur og skjermleser. Frontend er et rent presentasjonslag (AD-3, AD-7): den henter, formaterer og filtrerer, men regner aldri ut prognoser, metrikker, summer eller rekkefølge. Storyene følger skjermdelene. Hver UX-DR er akseptansekriterium i storyen for den skjermdelen den hører til.

**Testoppsett for epicen:** Rene funksjoner (`format.ts`, `klient.ts`, zod-skjemaene) testes med Vitest. Komponentene testes med Playwright mot ekte backend med seed (AD-14). Tilstander som krever feil fra backend (409, tidsavbrudd, ingen kontakt), lages med `page.route` i Playwright.

### Story 6.1: API-klient, kontrakt og dashbordskall med designtokens

Som Kari,
vil jeg at dashbordet har et rolig, Excel-nært uttrykk og viser tall og datoer på norsk,
slik at jeg kjenner meg igjen og kan lese tallene uten å tenke på formatet.

**Dekker:** AD-9 (fullfører: kontrakttest med zod) · AD-12 · NFR-4 (delvis: faste tekster og format) · UX-DR1 · UX-DR2 · UX-DR3 · UX-DR4 · UX-DR5 · UX-DR6 · UX-DR24 · UX-DR27 · UX-DR28 · UX-DR30 (delvis: ingen mørk modus, ingen skygger eller gradienter)

**Akseptansekriterier:**

**Given** `frontend/lib/api/skjema.ts`
**When** det skrives
**Then** er det en håndskrevet zod-kopi av Pydantic-skjemaene i `api/skjema.py` for alle seks endepunktene, med norsk snake_case og uten alias

**Given** `frontend/lib/api/klient.ts`
**When** et kall gjøres
**Then** går alle kall gjennom klienten, bare mot relative `/api/*`, og svarene parses med zod
**And** et svar med gyldig `{rapport}` klassifiseres som rapport
**And** nettverksfeil, svar som ikke er JSON, svar som ikke passer skjemaet, og status 502, 503 og 504 klassifiseres som *Ingen kontakt med backend*
**And** avbrudd etter 120 s klassifiseres som *Kjøring feilet* med teksten for tidsavbrudd
**And** `produkt_id` kodes med `encodeURIComponent`

**Given** `frontend/lib/api/sporringer.ts`
**When** data hentes
**Then** brukes TanStack Query med de faste nøklene `['datasett']`, `['datasett', id]`, `['produkter', id]` og `['produkt', id, produkt_id]` og `staleTime: Infinity`

**Given** `app/page.tsx`
**When** dashbordet rendres
**Then** er det én klientkomponent uten route handlers og uten Server Actions
**And** det har landemerkene `<header>`, `<main>` med den visuelt skjulte `<h1>` «PROGNOS – dashbord», og plassene for rapport, produktliste, graf, tabeller og WAPE-oversikt etter layouten i DESIGN.md

**Given** temaet i Tailwind v4 og shadcn
**When** det settes opp
**Then** finnes alle fargetokens fra DESIGN.md som CSS-variabler, bare lys modus (UX-DR1)
**And** typografirollene, systemfontstakken og `tabular-nums` for tall er satt opp (UX-DR2)
**And** radius er 2 px og 4 px, uten skygger og gradienter (UX-DR3)
**And** fokusringen er 2 px heltrukken `ring` med 2 px offset og full opasitet, globalt i stedet for `ring-ring/50` (UX-DR4)
**And** `Input` og `Select`-triggeren har kanten `{colors.input}` (UX-DR5)
**And** layoutmålene er satt som tokens, og elementer med tekst bruker `min-height`, ikke `height` (UX-DR6)

**Given** `frontend/lib/format.ts`
**When** tall og datoer formateres
**Then** formateres antall med `Intl.NumberFormat('nb-NO')`, WAPE med én desimal og dekning i hele prosent med `Intl.NumberFormat('nb-NO', {style: 'percent', …})`, måneder som «nov. 2026», og `opplastet` i `Europe/Oslo` som «13.11.2026 kl. 09.42» (UX-DR27)
**And** `null` for WAPE gir «–», aldri 0
**And** ingen annen fil formaterer tall eller datoer

**Given** `frontend/lib/tekster.ts`
**When** faste tekster brukes
**Then** står alle tekstene fra EXPERIENCE.md (*Faste tekster* og *Øvrige faste tekster*) der ordrett, med malene som funksjoner (UX-DR28)
**And** meldingene i valideringsrapporten tas fra backend og står ikke i `tekster.ts`

**Tester i storyen:**
- Vitest: `format.ts` for antall med hardt mellomrom («1 110»), WAPE («7,4 %», «24,0 %»), dekning («83 %»), «–» for `null`, månedsformat og tidspunkt i `Europe/Oslo` på begge sider av sommertid.
- Vitest: klassifiseringen i `klient.ts` for `{rapport}`, nettverksfeil, svar som ikke er JSON, skjemafeil, 502/503/504 og avbrudd.
- Vitest: malene i `tekster.ts`, blant annet entall og flertall i oppsummeringslinjen og malen for m = 0.
- Kontrakttest (Vitest mot ekte backend startet med midlertidig database og seed): ekte svar fra alle seks endepunktene parses med zod uten feil, også produkter med nivå `ingen`, `sesongnaiv` og `begge`.
- Playwright: siden har `<header>`, `<main>` og den skjulte `<h1>`.

### Story 6.2: Topplinje, opplasting og valideringsrapport

Som Kari,
vil jeg kunne velge et lagret datasett, laste opp en ny fil og se valideringsrapporten rett under topplinjen,
slik at jeg vet om fila ble godkjent, og hva jeg må rette hvis den ble avvist.

**Dekker:** FR-18 · FR-1 (fullfører: opplasting fra topplinjen) · FR-3 (visning av feillisten) · FR-6 (gjenåpning i dashbordet) · UJ-1 · UJ-2 · UJ-4 · UX-DR7 · UX-DR8 · UX-DR9 · UX-DR10 · UX-DR11 (delvis: *Fil avvist* og «Lukk») · UX-DR21 · UX-DR22 (delvis: *Datasett byttes*) · UX-DR25 (delvis: fokus etter kjøring og etter «Lukk») · AD-12

**Akseptansekriterier:**

**Given** dashbordet
**When** det åpnes
**Then** viser topplinjen ordmerket «PROGNOS», datasettvelgeren med etiketten «Datasett» og knappen **Last opp CSV** med teksten «CSV med kolonnene produkt_id, maaned, antall» under, koblet med `aria-describedby` (UX-DR7)
**And** topplinjen er ikke festet

**Given** lagrede datasett
**When** Kari åpner datasettvelgeren
**Then** viser den alle datasettene, nyeste øverst og valgt som standard, på formen «salg_2026-10.csv · 13.11.2026 kl. 09.42» (UX-DR8)
**And** et valg laster datasettet uten ny kjøring, og rapporten viser `Skeleton` med `aria-busy="true"` til dataene er kommet, uten slør (UX-DR22, *Datasett byttes*). Produktlisten og WAPE-linjen får den samme oppførselen i Story 6.4 og 6.7

**Given** et valgt datasett
**When** det vises
**Then** viser rapporten den lagrede rapporten fra opplastingen: oppsummeringslinjen etter malen, fordelingslinjen og «Vis advarsler ({n})» når n > 0 (UX-DR10)
**And** et klikk folder ut advarslene og bytter teksten til «Skjul advarsler», og rapporten folder seg sammen igjen ved bytte av datasett
**And** rapportoverskriften er en `<h2>`, og ✓ er `aria-hidden`

**Given** at Kari klikker **Last opp CSV**
**When** hun velger en fil
**Then** åpnes filvelgeren avgrenset til `.csv`, én forespørsel starter med en gang, og ingen bekreftelse vises (UX-DR9)
**And** app-roten får `inert` og et hvitt slør, og lasteboksen utenfor app-roten viser spinneren og «Kjører validering og prognose – dette kan ta opptil ett minutt», får fokus og skriver teksten i en `role="status"`-region som alltid finnes (UX-DR21)
**And** spinneren står stille med `prefers-reduced-motion`
**And** avbryter Kari filvelgeren, skjer ingenting

**Given** en godkjent opplasting
**When** svaret kommer
**Then** blir det nye datasettet valgt, bare `['datasett']` invalideres, rapporten vises sammenfoldet, og fokus flyttes til rapportoverskriften (FR-18, UX-DR25)

**Given** en avvist fil
**When** svaret kommer
**Then** blir rapporten rød med «Fila ble avvist. Ingenting er lagret.» og «{n} feil», og alle feilene listes i filrekkefølge med meldingene fra backend (UX-DR11)
**And** feillisten scroller når den er høyere enn 320 px og er da en region med `tabindex="0"` og `aria-label="Feil i fila"`
**And** datasettvelgeren og resten av dashbordet viser fortsatt datasettet som var valgt før
**And** fokus flyttes til rapportoverskriften

**Given** en rød rapport for avvist fil
**When** Kari klikker «Lukk», laster opp på nytt eller velger et annet datasett
**Then** forsvinner avvisningen, og den godkjente rapporten for valgt datasett vises igjen
**And** «Lukk» er bygget slik at Story 6.3 kan bruke den for de andre røde variantene
**And** etter «Lukk» får **Last opp CSV** fokus (UX-DR25)

**Tester i storyen:**
- Playwright: datasettvelgeren viser seed-datasettet med riktig format og er valgt.
- Playwright: godkjent opplasting av en liten CSV gir lasteboks, nytt datasett valgt, sammenfoldet rapport og fokus på rapportoverskriften.
- Playwright: UJ-2-fila gir rød rapport med begge feilene ordrett, og forrige datasett blir stående.
- Playwright: en fil med mange feil gir scrollende feilliste med `role="region"`.
- Playwright: «Vis advarsler» og «Skjul advarsler» for en fil med utfylte måneder.
- Playwright: bytte av datasett viser rapporten fra den opplastingen uten ny kjøring (UJ-4).
- Playwright: «Lukk» etter avvist fil gir den godkjente rapporten igjen og fokus på **Last opp CSV**.
- Playwright: lasteboksen har `role="status"`-teksten, og app-roten er `inert` under kjøring.

### Story 6.3: Rapport ved feilet kjøring, opptatt tjeneste, tidsavbrudd og ingen kontakt

Som Kari,
vil jeg få en tydelig og ærlig beskjed når kjøringen feiler, tar for lang tid, en annen opplasting pågår, eller PROGNOS-tjenesten ikke svarer,
slik at jeg vet at ingenting er lagret, og hva jeg kan gjøre videre.

**Dekker:** FR-7 (visning av feilet kjøring) · FR-18 (rapporten ved feil) · UJ-1 (feilgrenen) · UJ-4 (feilgrenen) · UX-DR11 (fullfører: *Kjøring feilet*, *Opplasting pågår allerede* og *Ingen kontakt med backend*) · UX-DR25 (delvis: fokus ved feil) · AD-8 (frontend viser meldingen fra backend uendret) · AD-12 (klassifiseringen i `klient.ts`)

**Akseptansekriterier:**

**Given** et svar `500 {rapport}` med status `feilet` og koden `kjoring` eller `uventet`
**When** det kommer
**Then** blir rapporten rød med overskriften «Prognosen kunne ikke kjøres. Ingenting er lagret.», og meldingen fra backend står uendret under
**And** datasettvelgeren og resten av dashbordet viser fortsatt datasettet som var valgt før
**And** fokus flyttes til rapportoverskriften

**Given** et svar med koden `tidsavbrudd` fra backend, eller at klienten gir opp etter 120 s
**When** det skjer
**Then** viser den røde rapporten samme overskrift og teksten «Kjøringen tok mer enn to minutter og ble stoppet.»
**And** sløret og lasteboksen forsvinner, og fokus flyttes til rapportoverskriften

**Given** et svar `409 {rapport}` med koden `opptatt`
**When** det kommer
**Then** viser den røde rapporten overskriften «Prognosen kunne ikke kjøres. Ingenting er lagret.» og teksten fra backend: «En annen opplasting pågår allerede. Vent til den er ferdig, og prøv igjen.»

**Given** at `klient.ts` klassifiserer et svar som *Ingen kontakt med backend* (nettverksfeil, ikke JSON, skjemafeil eller 502/503/504)
**When** det skjer ved opplasting, ved første innlasting eller når et datasett velges (UJ-4)
**Then** viser den røde rapporten «Får ikke kontakt med PROGNOS-tjenesten. Sjekk at den kjører, og last siden på nytt.»
**And** fokus flyttes til teksten

**Given** en av disse røde variantene
**When** Kari klikker «Lukk», laster opp på nytt eller velger et annet datasett
**Then** forsvinner feilen, og den godkjente rapporten for valgt datasett vises igjen
**And** etter «Lukk» får **Last opp CSV** fokus

**Given** alle røde varianter
**When** de vises
**Then** brukes `report-rejected` med rød stripe, uten ikon utover tekst, uten toast og uten `role="alert"`, fordi resultatet annonseres med fokusflyttingen

**Tester i storyen:**
- Playwright med `page.route`: 500 med `kjoring` gir riktig overskrift, meldingen fra backend uendret og fokus på overskriften.
- Playwright med `page.route`: 500 med `tidsavbrudd` gir teksten for tidsavbrudd.
- Vitest: klientens grense på 120 s gir klassifiseringen tidsavbrudd (med falske timere). Playwright viser teksten når svaret avbrytes.
- Playwright med `page.route`: 409 gir teksten fra backend.
- Playwright med `page.route`: nettverksfeil, 502 og et svar som ikke er JSON gir *Ingen kontakt* ved opplasting og ved bytte av datasett, med fokus på teksten.
- Playwright: «Lukk» etter hver variant gir den godkjente rapporten igjen og fokus på **Last opp CSV**.
- Playwright: forrige datasett blir stående i datasettvelgeren i alle variantene.

### Story 6.4: Produktliste med de svakeste øverst og søk

Som Kari,
vil jeg se produktene med de svakeste prognosene øverst og kunne søke etter et produkt,
slik at jeg bruker tiden min der prognosen er svak og finner et bestemt produkt raskt.

**Dekker:** FR-19 (delvis: listen, rekkefølgen, flaggene og valget. Oppdateringen av graf og tabeller fullføres i Story 6.6) · FR-26 (delvis: filtreringen og valgt produkt beholdes. Visningen i graf og tabeller fullføres i Story 6.6) · UJ-1 · UJ-3 · UX-DR12 · UX-DR13 · UX-DR14 · UX-DR22 (delvis: *Datasett byttes* for produktlisten) · AD-7 (frontend sorterer ikke, søket filtrerer i klienten)

**Akseptansekriterier:**

**Given** et valgt datasett
**When** produktlisten vises
**Then** står produktene i rekkefølgen fra `GET …/products` (sortert på `rang`), og frontend sorterer aldri på nytt
**And** hver rad viser `produkt_id` til venstre og `liste_wape` høyrejustert på linje 1, og flaggene på linje 2 (UX-DR13)
**And** udefinert WAPE vises som «–» med den skjulte teksten «udefinert», eller «ingen backtest» når produktet ikke har backtest

**Given** et produkt med flagg
**When** raden vises
**Then** har hvert flagg et Lucide-ikon (klokke for *kort historikk*, pil ned for *ETS taper*) og tekst, ikonet er `aria-hidden`, og flagget er ikke interaktivt og aldri rødt (UX-DR14)

**Given** produktlisten
**When** den brukes med tastatur
**Then** er den en `<nav aria-label="Produkter">` med en ARIA-`listbox` med `aria-label="Produkter, svakeste først"`, roving tabindex og *selection follows focus*
**And** pil opp og ned velger produktet med en gang, og Home og End går til første og siste treff
**And** når Kari tabber inn, får valgt rad fokus hvis den er synlig i filteret, ellers får første treff fokus uten å bli valgt
**And** hver rad har et tilgjengelig navn som «P-109, WAPE 24,0 %, flagg: ETS taper»
**And** valgt rad har `aria-selected`, `primary-subtle` som bakgrunn og en 3 px blå stripe, og hover gir `surface-subtle`

**Given** innlasting, en godkjent kjøring eller bytte av datasett
**When** produktlisten er hentet
**Then** velges første rad automatisk
**And** valgt rad scrolles inn med `scrollIntoView({block: 'nearest'})`

**Given** at et annet datasett velges
**When** produktlisten hentes
**Then** viser listen `Skeleton` med `aria-busy="true"` til dataene er kommet (UX-DR22, *Datasett byttes*)

**Given** at Kari velger et produkt med klikk eller piltast
**When** valget endres
**Then** lagres valget som valgt produkt i dashbordets tilstand, og produktdetaljen hentes med nøkkelen `['produkt', id, produkt_id]`
**And** ved piltaster hentes produktdetaljen 200 ms etter siste tastetrykk, og naboproduktene hentes på forhånd med `prefetchQuery`

**Given** søkefeltet med etiketten «Søk produkt-ID»
**When** Kari skriver
**Then** filtreres listen fortløpende med `produkt_id.toLowerCase().includes(sok.toLowerCase())`, og rekkefølgen fra `rang` beholdes (FR-26)
**And** telleren «Viser {x} av {n}» oppdateres i en `aria-live="polite"`-region 500 ms etter siste tastetrykk
**And** Esc tømmer feltet, og et tomt felt viser alle produktene
**And** valgt produkt beholdes som valgt i dashbordets tilstand selv om det faller utenfor filteret
**And** uten treff vises «Ingen produkter matcher «{søk}».» og «Tøm søk» (UX-DR12)

**Given** layouten
**When** bredden er 1024 px eller mer
**Then** er listen sticky under topplinjen, har bredden 300 px (260 px ved 1024–1279 px) og scroller for seg selv

**Tester i storyen:**
- Playwright: rekkefølgen i listen er lik `rang` fra API-et for seed-datasettet, og de flaggede står øverst.
- Playwright: første rad er valgt etter innlasting.
- Playwright: pil ned flytter `aria-selected` til neste rad og gir én forespørsel mot produktdetaljen for det produktet etter 200 ms. Home og End virker.
- Playwright: det tilgjengelige navnet på en flagget rad.
- Playwright: søk på små bokstaver gir treff på store, rekkefølgen beholdes, telleren oppdateres, og Esc tømmer.
- Playwright: valgt produkt er fortsatt valgt når søket fjerner det fra listen, og blir markert igjen når søket tømmes.
- Playwright: bytte av datasett gir `aria-busy="true"` på listen til produktene er kommet.
- Playwright: *Søk uten treff* og «Tøm søk».
- Playwright: flagget har ikon og tekst, og ikonet er `aria-hidden`.

### Story 6.5: Graf med historikk, prognose og spenn

Som Kari,
vil jeg se salgshistorikken og prognosen med spennet i samme graf,
slik at jeg ser med en gang om prognosen henger sammen med historikken, og hvor usikker den er.

**Dekker:** FR-20 · FR-10 (visningen: ETS for *ets*, sesongnaiv for *sesongnaiv*) · F10 (delvis: historikk, prognose og intervall) · UJ-1 · UX-DR15 · UX-DR16 · UX-DR22 (delvis: *Produktdetalj lastes* og *Produktdetalj kunne ikke hentes*)

**Akseptansekriterier:**

**Given** et valgt produkt med prognose
**When** grafen vises
**Then** viser Recharts hele historikken og de 6 prognosemånedene langs samme månedsakse, med y-aksen fra 0 og horisontale rutenettlinjer
**And** historikken er en heltrukket linje på 2 px, P50 en stiplet linje på 2 px (6/4), og båndet P10–P90 har fyll og 1 px heltrukne kanter
**And** P50 og båndet starter i siste faktiske punkt, så kurven henger sammen
**And** en loddrett markør står ved første prognosemåned med etiketten «Prognose →» (→ er `aria-hidden`)
**And** grafen har ingen animasjon
**And** grafen viser prognosen fra API-et uten å regne om noe

**Given** grafens panel
**When** det vises
**Then** er panelhodet «Prognose – {produkt_id}» som `<h2>`, med underteksten «ETS · 6 måneder fram» eller «Sesongnaiv baseline · 6 måneder fram» etter `prognosemodell`
**And** forklaringen under grafen har «Historikk», «Forventet (P50)» og «Spenn Pessimistisk–Optimistisk (P10–P90)» med linjeutsnitt i samme stil som seriene

**Given** grafen
**When** den leses av skjermleser
**Then** har den `role="img"` og `aria-label` etter malen «Prognose for {produkt_id}: historikk fra {måned} til {måned}, Forventet {sum} over 6 måneder, spenn {p10-sum}–{p90-sum}.» med summene fra `scenariototal`
**And** den kan ikke fokuseres og har ingen piltaster

**Given** at pekeren står over grafen
**When** tooltipen vises
**Then** viser historiske måneder «Faktisk», og prognosemåneder viser Pessimistisk, Forventet og Optimistisk
**And** Esc skjuler tooltipen til neste pekerbevegelse

**Given** et produkt med historikknivå `ingen`
**When** grafen vises
**Then** viser den bare historikken og teksten «Ingen prognose: under 12 måneders historikk», uten undertekst i panelhodet, og `aria-label` er den faste teksten fra `tekster.ts`

**Given** lenkeknappen «Vis historikk som tabell»
**When** Kari klikker den
**Then** vises en tabell med kolonnene Måned og Faktisk, nyeste måned øverst, og «(fylt inn)» etter tallet for utfylte måneder
**And** knappen bytter til «Skjul historikktabell», og økten husker om tabellen er åpen eller lukket (`sessionStorage` med try/catch) (UX-DR16)

**Given** at Kari velger et annet produkt
**When** detaljen lastes
**Then** blir forrige produkt stående i 150 ms, og deretter vises `Skeleton` med `aria-busy="true"` til dataene er kommet
**And** feiler hentingen, viser grafområdet «Kunne ikke hente data for {produkt_id}» og «Prøv igjen». Tabellene får den samme tilstanden i Story 6.6

**Tester i storyen:**
- Playwright: for et *ets*-produkt finnes historikklinjen, den stiplede P50-linjen, båndet og markøren, og panelhodet sier «ETS · 6 måneder fram» (F10).
- Playwright: for et *sesongnaiv*-produkt sier panelhodet «Sesongnaiv baseline · 6 måneder fram».
- Playwright: for produktet med 8 måneder vises den faste teksten og ingen prognose (FR-20).
- Playwright: `aria-label` på grafen inneholder summene fra API-et.
- Playwright: historikktabellen har nyeste måned øverst og «(fylt inn)» for en fil med utfylte måneder, og den forblir åpen ved bytte av produkt.
- Playwright med `page.route`: feil i produktdetaljen gir teksten og «Prøv igjen», og «Prøv igjen» henter på nytt.

### Story 6.6: Scenariotabell, backtest-tabell og detaljer per opprinnelse

Som Kari,
vil jeg se scenarioene med totaler og backtesten mot baseline med detaljer per måned,
slik at jeg har tall å gi videre og kan regne etter om metoden treffer.

**Dekker:** FR-21 · FR-11 (visningen) · FR-12 (fullfører: merknaden i grensesnittet) · FR-17 (visningen: begge WAPE-tallene og dommerlinjen) · FR-19 (fullfører: valg i listen oppdaterer graf, scenariotabell og backtest-tabell) · FR-26 (fullfører: valgt produkt står i graf og tabeller utenfor filteret) · UX-DR22 (delvis: laste- og feiltilstand for tabellene) · F10 (delvis: scenarioer) · NFR-5 (fullfører: tallene kan regnes etter fra det som vises) · UJ-1 · UJ-3 · UX-DR17 · UX-DR18 · UX-DR19 · UX-DR26

**Akseptansekriterier:**

**Given** et produkt med prognose
**When** scenariotabellen vises
**Then** har den panelhodet «Scenarioer», kolonnene Måned, Pessimistisk, Forventet og Optimistisk med P10, P50 og P90 som undertekst, 6 månedsrader og en sumrad i vekt 600 med kantlinje over (UX-DR17)
**And** sumraden viser `scenariototal` fra API-et uendret
**And** merknaden «Totalene er summer av månedlige verdier. Det reelle spennet mellom Pessimistisk og Optimistisk er smalere enn det som vises.» står alltid under tabellen og er koblet med `aria-describedby` (FR-12)

**Given** et produkt med historikknivå `ingen`
**When** scenariotabellen vises
**Then** står teksten «Ingen prognose: under 12 måneders historikk» i stedet for radene, og merknaden står fortsatt

**Given** et produkt med `backtest_nivaa = begge`
**When** backtest-tabellen vises
**Then** har den panelhodet «Backtest (siste 6 måneder)», kolonnene *Sesongnaiv baseline* og *ETS* i den rekkefølgen, og radene WAPE og Intervalldekning (UX-DR18)
**And** øverste venstre celle har den skjulte teksten «Mål»
**And** dommerlinjen under tabellen er tekst uten farge: «ETS slår baseline», «ETS taper mot baseline», «ETS og baseline har lik WAPE» eller «Kan ikke sammenlignes (WAPE er udefinert når faktisk salg er 0)», valgt bare ut fra den lagrede `dommer`

**Given** et produkt med `backtest_nivaa = sesongnaiv`
**When** backtest-tabellen vises
**Then** vises baseline-kolonnen, og ETS-kolonnen viser «ETS er ikke backtestet (under 30 måneders historikk)» over cellene, med `<th scope="col">ETS</th>` beholdt
**And** dommerlinjen vises ikke

**Given** et produkt med `backtest_nivaa = ingen`
**When** backtest-tabellen vises
**Then** står «Ingen backtest (under 18 måneders historikk)» i stedet for tabellen, uten dommerlinje og uten knapp for detaljer

**Given** et produkt med backtest
**When** Kari klikker «Vis detaljer per opprinnelse (6)»
**Then** åpnes en tabell i full bredde under begge tabellene med den synlige `<caption>` «Detaljer per opprinnelse – {produkt_id}» og kolonnene Måned, Faktisk, Baseline P50, Baseline avvik, Baseline i spenn, ETS P50, ETS avvik og ETS i spenn («ja» eller «nei») (UX-DR19)
**And** sumraden viser Σ faktisk og Σ avvik per modell fra `metrikk`, så WAPE = Σ avvik / Σ faktisk kan regnes etter (NFR-5)
**And** ved bare baseline-backtest vises bare baseline-kolonnene
**And** knappen bytter til «Skjul detaljer per opprinnelse», og økten husker om tabellen er åpen, også ved bytte av produkt

**Given** alle tabellene
**When** de rendres
**Then** er de ekte `<table>` med `<caption>` (som kan være visuelt skjult), `<th scope="row">` for måned og «Sum», `<th scope="col">` for kolonnene, og de er ikke tabstopp (UX-DR26)
**And** tall er høyrejustert med `tabular-nums`

**Given** at Kari velger et annet produkt i listen
**When** detaljen er hentet
**Then** viser graf, scenariotabell og backtest-tabell det nye produktet (FR-19)
**And** mens detaljen lastes, viser tabellene `Skeleton` med `aria-busy="true"` etter samme regel som grafen, og feiler hentingen, er tabellene tomme (UX-DR22)

**Given** at valgt produkt faller utenfor søkefilteret
**When** søket endres
**Then** viser graf og tabeller fortsatt det valgte produktet, også ved *Søk uten treff* (FR-26)

**Tester i storyen:**
- Playwright: scenariotabellen har scenarionavnene, P10/P50/P90 som undertekst, 6 rader, sumrad lik `scenariototal` fra API-et og merknaden ordrett (F10, FR-12).
- Playwright: *ingen*-produktet viser den faste teksten og merknaden.
- Playwright: backtest-tabellen for et *begge*-produkt viser begge kolonnene i riktig rekkefølge og dommerlinjen.
- Playwright: etter opplasting av `backend/tests/data/ets_taper.csv` fra Story 5.3 viser produktet begge WAPE-tallene og «ETS taper mot baseline», og grafen viser fortsatt ETS (FR-17).
- Playwright: valg av et annet produkt med klikk og med piltast oppdaterer grafens panelhode, scenariotabellen og backtest-tabellen (FR-19).
- Playwright: et valgt produkt som søket fjerner fra listen, står fortsatt i graf og tabeller, også ved *Søk uten treff* (FR-26).
- Playwright med `page.route`: feil i produktdetaljen gir tomme tabeller.
- Playwright: produktene med 15 og 20 måneder viser hver sin faste tekst (FR-21).
- Playwright: summen av «avvik» delt på summen av «Faktisk» i detaljtabellen gir samme WAPE (avrundet til én desimal) som backtest-tabellen (NFR-5).
- Playwright: detaljtabellen forblir åpen ved bytte av produkt.
- Playwright: tabellene har `<caption>` og riktige `scope`-attributter.

### Story 6.7: WAPE-oversikt for alle produkter

Som Kari,
vil jeg se nederst på siden om ETS slår baseline totalt sett, og for hvor mange produkter,
slik at jeg kan vise materialplanleggeren at metoden holder, selv om enkelte produkter må vurderes med skjønn.

**Dekker:** FR-22 (fullfører: WAPE-oversikten i dashbordet) · F11 (visningen bygger på lagrede data) · UJ-3 · UX-DR20 · UX-DR22 (fullfører: *Datasett byttes* for WAPE-linjen)

**Akseptansekriterier:**

**Given** et valgt datasett med `m > 0`
**When** WAPE-oversikten vises
**Then** viser den «Total WAPE: Sesongnaiv baseline {x} % · ETS {y} % · ETS slår baseline for {n} av {m} produkter» med verdiene fra `sammendrag`, formatert i `format.ts`
**And** baseline står før ETS

**Given** et datasett med `m = 0`
**When** WAPE-oversikten vises
**Then** viser den «Total WAPE: ingen produkter har backtest for begge modellene»

**Given** layouten
**When** bredden er 1024 px eller mer
**Then** er linjen festet nederst med grå flate og kantlinje over, og siden har `scroll-padding-bottom` lik linjens høyde, slik at linjen aldri dekker elementet som har fokus
**And** linjen er ikke klikkbar, og den oppdateres når et annet datasett velges
**And** mens det nye datasettet lastes, viser linjen `Skeleton` med `aria-busy="true"` (UX-DR22, *Datasett byttes*)

**Tester i storyen:**
- Playwright: teksten for seed-datasettet stemmer med `sammendrag` fra API-et.
- Playwright: et opplastet datasett uten produkter med 30 måneder eller mer gir malen for m = 0.
- Playwright: linjen bytter innhold ved bytte av datasett og har `aria-busy="true"` mens det lastes.
- Playwright: et fokusert element nederst på siden er ikke dekket av linjen ved 1280 × 720.

### Story 6.8: Tilgjengelighet, responsiv layout og hele arbeidsflyten

Som Kari,
vil jeg kunne bruke hele dashbordet med tastatur, skjermleser og zoom, uten nett,
slik at PROGNOS virker for meg uansett hvordan jeg jobber, og sensor kan se at hele v1 henger sammen.

**Dekker:** F10 (fullfører) · NFR-1 (fullfører: UJ-1 uten nett) · NFR-4 (fullfører) · NFR-6 (fullfører) · UJ-1 · UJ-2 · UJ-3 · UJ-4 · UX-DR23 · UX-DR25 (fullfører) · UX-DR29 · UX-DR30 (fullfører)

**Akseptansekriterier:**

**Given** dashbordet
**When** Kari trykker Tab første gang
**Then** vises hopplenken «Hopp til produktlisten» som `button-primary`, og den flytter fokus til produktlisten, som har `tabindex="-1"` (UX-DR23)

**Given** dashbordet med tastatur
**When** Kari tabber gjennom siden
**Then** er rekkefølgen hopplenke, datasettvelger, **Last opp CSV**, rapporten («Vis advarsler», «Lukk» og feillisten når den scroller), søk, produktliste (ett tabstopp), «Vis historikk som tabell», «Vis detaljer per opprinnelse» og scrollende regioner ved reflow
**And** fokusringen er synlig på alle kontrollene, og fokus havner aldri på `<body>` (UX-DR25)

**Given** bredder under 1024 px, ned til 320 px
**When** siden vises
**Then** ligger panelene i én kolonne i rekkefølgen topplinje, rapport, produktliste, graf, scenario, backtest, detaljer og WAPE (UX-DR29)
**And** produktlisten er ikke sticky og har `max-height: max(50vh, 240px)`, WAPE-linjen er ikke festet, og lasteboksen har `max-width: calc(100vw - 32px)`
**And** grafen og tabellene kan scrolle vannrett og er da fokuserbare regioner med navn
**And** siden har ingen vannrett scroll utenfor disse regionene

**Given** høyden 720 px og 1080 px
**When** siden vises ved 1280 px bredde
**Then** bruker grafen 300 px under 800 px vindushøyde og 360 px ellers, og ved 1080 px er hele dashbordet synlig uten scrolling

**Given** hele dashbordet
**When** det sjekkes
**Then** finnes ingen modaler, bekreftelsesdialoger, toast-varsler, uendelig scrolling, grafanimasjoner, trafikklysfarger, KPI-kort eller mørk modus (UX-DR30)
**And** ingen synlige brukertekster er på engelsk utover fagbegrepene i ordlista (ETS, WAPE, P10/P50/P90), og overskriftene og scenarionavnene er de norske (NFR-4)

**Given** at appen er installert
**When** nettverket kobles fra og sensor følger UJ-1 med en egen CSV-fil
**Then** fungerer opplasting, rapport, produktliste, graf og tabeller uten nett (NFR-1)

**Given** alle F-kriteriene
**When** sporbarheten sjekkes
**Then** er F1–F14 hvert dekket av minst én automatisk test som kjører grønt (F12 og NFR-1 har i tillegg den manuelle kontrollen), og README lister alle testkommandoene (NFR-6)

**Tester i storyen:**
- Playwright: UJ-1 fra opplasting til scenariotabell, uten feil i nettleserkonsollen (F10).
- Playwright: UJ-2 med avvist fil, retting og ny opplasting.
- Playwright: UJ-3 med opplasting av `backend/tests/data/ets_taper.csv` fra Story 5.3, produktet med *ETS taper* øverst i listen, detaljtabellen og WAPE-oversikten.
- Playwright: UJ-4 med bytte til et eldre datasett uten lasteboks.
- Playwright: Tab-rekkefølgen og hopplenken.
- Playwright: layouten ved 1280 × 720, 1280 × 1080 og 320 × 256 (UX-DR29), uten vannrett scroll på siden.
- Playwright: overskriftene «Produkter», «Scenarioer», «Backtest (siste 6 måneder)» og scenarionavnene står på norsk, og en liste med forbudte engelske ord («Upload», «Loading», «Error», «Forecast») finnes ikke i synlig tekst (NFR-4).
- Playwright: spinneren står stille med `prefers-reduced-motion: reduce`.
- Sporbarhetstabell i README eller i `docs/` som viser hvilken test som dekker hvert av F1–F14 (NFR-6).
- Manuell kontroll (NFR-1): UJ-1 med nettverket koblet fra. Resultatet føres i sesjonsloggen med dato og maskin.
