---
name: PROGNOS
status: final
created: 2026-11-14
updated: 2026-11-14
sources:
  - ../../prds/prd-G96-ellingsen-2026-11-14/prd.md
  - ../../prds/prd-G96-ellingsen-2026-11-14/addendum.md
---

# PROGNOS: opplevelsesspesifikasjon

Krav-ID-ene (FR-, NFR-, UJ-) og de ordrette tekstene kommer fra [prd.md](../../prds/prd-G96-ellingsen-2026-11-14/prd.md). Denne fila sier hvordan kravene oppfører seg i grensesnittet, og gjentar dem ikke. Hvis denne fila og PRD-en er uenige om en tekst som er fastsatt ordrett (FR-12, FR-20, FR-21, se PRD §11.2), gjelder PRD-en.

To bevisste avvik fra PRD-en (søk i produktlisten og autovalg av første produkt) og API-hull som arkitekturen må løse, står i *Åpne punkter* nederst.

## Foundation

- **Plattform:** nettapp på én flate, bare for desktop og laptop, fra 1280 × 720 px. Nettbrett og mobil er utenfor v1.
- **Teknologi** (fra addendum): Next.js 16 (App Router), React 19, Tailwind v4, shadcn/ui, Recharts og TanStack Query v5. Visuell identitet: [DESIGN.md](DESIGN.md). Denne fila beskriver bare oppførselen der den avviker fra shadcn-standarden.
- **Bruk:** én bruker, lokalt og offline (NFR-1), uten innlogging (NFR-8).
- **Første oppstart:** dashbordet har alltid data, fordi det syntetiske datasettet lastes inn ved tom database (FR-25).
- **Språk:** norsk bokmål overalt, `<html lang="nb">` (NFR-4).

## Information Architecture

Dashbordet er én side som scroller. Alle delene er alltid til stede, og det finnes ingen ruter, faner eller modaler. Den eneste flaten som legger seg over siden, er lasteboksen.

| Del (PRD-navn) | Plassering | Formål | Krav | Reise |
|---|---|---|---|---|
| Topplinje | Øverst | Ordmerke, datasettvelger, **Last opp CSV** og kolonnekravet | FR-1, FR-18 | UJ-1, UJ-2 |
| Datasettvelger | Topplinje, venstre | Bytte mellom lagrede datasett (filnavn og tidspunkt), nyeste valgt som standard | FR-6, FR-18 | UJ-4 |
| Valideringsrapport | Rett under topplinjen, full bredde | Resultatet av validering og kjøring for valgt datasett, eller avvisning av en ny fil | FR-3–FR-5, FR-7, FR-18 | UJ-1, UJ-2 |
| Produktliste | Venstre kolonne, sticky | Alle produkter, sortert etter FR-19, med søk på `produkt_id` | FR-19 + søk (åpent PRD-punkt) | UJ-1, UJ-3 |
| Graf | Midten | Historikk, prognose og P10–P90-bånd for valgt produkt, med historikktabell som tekstalternativ | FR-10, FR-20 | UJ-1 |
| Scenariotabell | Under grafen, venstre | Scenarioer per måned og totaler, med merknad | FR-11, FR-12, FR-21 | UJ-1 |
| Backtest-tabell | Under grafen, høyre | WAPE og dekning for baseline og ETS, med detaljer per opprinnelse | FR-17, FR-21 | UJ-3 |
| WAPE-oversikt | Nederst, festet fra 1024 px bredde | Total WAPE for begge modellene og «n av m» | FR-22 | UJ-3 |

I PRD-ordlista hører valideringsrapporten til *Topplinje*. Her står den som en egen del rett under topplinjen, slik FR-18 beskriver.

**Landemerker og overskrifter:**
- `<header>` er topplinjen.
- `<main>` har en visuelt skjult `<h1>` «PROGNOS – dashbord».
- Produktlisten er `<nav aria-label="Produkter">`.
- Hvert panel har en `<h2>` med teksten fra panelhodet.
- Rapportoverskriften er også en `<h2>`.

→ Visuell referanse:
- [mockups/key-dashbord.html](mockups/key-dashbord.html): godkjent tilstand med P-109 valgt
- [mockups/key-avvist.html](mockups/key-avvist.html): avvist fil og lastetilstand

Ved konflikt gjelder DESIGN.md og denne fila foran mockupene.

## Voice and Tone

Merkevarestemmen ligger i DESIGN.md (*Brand & Style*). Her er reglene for mikrotekst:

- Skriv saklig og kort, og bruk fagordene fra PRD-ordlista.
- Systemet konstaterer, men anbefaler aldri noe (PRD: «ingen anbefalinger»).
- Scenarionavnene er hovedordene, og P10/P50/P90 står bare som forklaring.

| Gjør | Ikke gjør |
|---|---|
| «Fila ble avvist. Ingenting er lagret.» | «Oi! Noe gikk galt 😕» |
| «Rad 418: antall må være et heltall ≥ 0» (eksempel fra UJ-2) | «Ugyldig verdi i fila» |
| «ETS taper mot baseline» | «Vi anbefaler å bruke baseline» |
| «Pessimistisk 820 · Forventet 960 · Optimistisk 1 110» | «P10: 820, P50: 960, P90: 1110» som hovedtekst |
| «Kjører validering og prognose – dette kan ta opptil ett minutt» | «Laster…» uten forklaring |
| Engelske ord bare der de står i ordlista (ETS, WAPE, P10/P50/P90) | «Upload», «Loading», «Error» |
| Ingen utropstegn | «Ferdig!» |

### Faste tekster

De fire første tekstene er fastsatt ordrett i PRD-en (§11.2). Resten er maler denne spesifikasjonen fastsetter, slik at Playwright-testene har noe å sjekke mot (NFR-4). `{…}` er variabler.

| Tekst | Kilde | Hvor |
|---|---|---|
| «Totalene er summer av månedlige verdier. Det reelle spennet mellom Pessimistisk og Optimistisk er smalere enn det som vises.» | FR-12, ordrett | Alltid under scenariotabellen, også når produktet ikke har prognose |
| «Ingen prognose: under 12 måneders historikk» | FR-20, ordrett | Midt i grafen, oppå historikkurven, og i scenariotabellen i stedet for rader |
| «ETS er ikke backtestet (under 30 måneders historikk)» | FR-21, ordrett | I ETS-kolonnen i backtest-tabellen |
| «Ingen backtest (under 18 måneders historikk)» | FR-21, ordrett | I backtest-tabellen i stedet for hele tabellen |
| «✓ {n} produkter godkjent · {k} flagget (kort historikk)» | FR-18, mal | Oppsummeringslinjen i godkjent rapport. Ved n = 1 står «1 produkt godkjent». Ved k = 0 utelates «· 0 flagget (kort historikk)». |
| «Fordeling: ingen {a} · sesongnaiv {b} · ets {c}» | FR-5, mal | Under oppsummeringslinjen. Alltid a + b = k og a + b + c = n, fordi både *ingen* og *sesongnaiv* får flagget *kort historikk*. |
| «{produkt_id}: {antall} måned(er) fylt inn med 0 ({ÅÅÅÅ-MM}, {ÅÅÅÅ-MM}, …)» | FR-4, mal | Én linje per produkt i advarslene, for eksempel «P-031: 2 måneder fylt inn med 0 (2025-03, 2025-07)» |
| «Kjører validering og prognose – dette kan ta opptil ett minutt» | denne spesifikasjonen | Lasteboksen |

**Panelhoder:**
- «Produkter»
- «Prognose – {produkt_id}», med underteksten «ETS · 6 måneder fram» eller «Sesongnaiv baseline · 6 måneder fram». For produkter med historikknivå *ingen* står det ingen undertekst.
- «Scenarioer»
- «Backtest (siste 6 måneder)»

**Dommerlinjen** i backtest-tabellen har fire varianter:
- «ETS slår baseline» (strengt lavere WAPE)
- «ETS taper mot baseline» (gir flagget *ETS taper*)
- «ETS og baseline har lik WAPE»
- «Kan ikke sammenlignes (WAPE er udefinert når faktisk salg er 0)»

**WAPE-oversikten:**
- Mal: «Total WAPE: Sesongnaiv baseline {x} % · ETS {y} % · ETS slår baseline for {n} av {m} produkter»
- Når m = 0: «Total WAPE: ingen produkter har backtest for begge modellene»

**Feilmeldinger ved avvist fil** (FR-2, FR-3). Radnummeret er linjenummeret i fila, og overskriftsraden er linje 1.

| Regel | Mal |
|---|---|
| Manglende påkrevd kolonne | «Mangler påkrevd kolonne: {kolonne}» |
| Skilletegn ikke gjenkjent (FR-2) | «Fant ikke kolonnene produkt_id, maaned og antall med komma eller semikolon som skilletegn» |
| `maaned` i feil format | «Rad {r}: maaned må ha formatet ÅÅÅÅ-MM med måned 01–12» |
| `antall` negativt eller ikke heltall | «Rad {r}: antall må være et heltall ≥ 0» |
| Tom celle | «Rad {r}: tom celle i {kolonne}» |
| Duplikat | «Duplikat: {produkt_id}, {ÅÅÅÅ-MM} (rad {r1} og {r2})» |
| Ingen datarader | «Fila har ingen datarader» |

**Øvrige faste tekster.** Tilstandene i *State Patterns* viser hit.

| Tekst | Hvor |
|---|---|
| «Fila ble avvist. Ingenting er lagret.» + «{n} feil» | Overskrift i rød rapport, *Fil avvist* |
| «Prognosen kunne ikke kjøres. Ingenting er lagret.» | Overskrift i rød rapport, *Kjøring feilet* |
| «Kjøringen tok mer enn to minutter og ble stoppet.» | Under overskriften ved tidsavbrudd |
| «Får ikke kontakt med PROGNOS-tjenesten. Sjekk at den kjører, og last siden på nytt.» | Rød rapport, *Ingen kontakt med backend* |
| «Kunne ikke hente data for {produkt_id}» + «Prøv igjen» | Grafområdet, *Produktdetalj kunne ikke hentes* |
| «Ingen produkter matcher «{søk}».» + «Tøm søk» | Produktlisten, *Søk uten treff* |
| «Viser {x} av {n}» | Søketelleren |
| «Vis advarsler ({n})» / «Skjul advarsler» | Godkjent rapport |
| «Vis historikk som tabell» / «Skjul historikktabell» · «Vis detaljer per opprinnelse (6)» / «Skjul detaljer per opprinnelse» | Lenkeknapper under graf og backtest-tabell |
| «Lukk» | Rød rapport |
| «Hopp til produktlisten» | Hopplenke |
| «CSV med kolonnene produkt_id, maaned, antall» | Under **Last opp CSV** |
| «Prognose for {produkt_id}: historikk fra {måned} til {måned}, Forventet {sum} over 6 måneder, spenn {p10-sum}–{p90-sum}.» | `aria-label` på grafen |

## Tall- og datoformat

Denne seksjonen finnes fordi tallene er produktet. Kari skal kunne regne etter for hånd (NFR-5).

- **Antall:** heltall, formatert med `Intl.NumberFormat('nb-NO')`. Det gir hardt mellomrom som tusenskille: «1 110». Grafen og tabellene skal aldri vise desimaler for antall.
- **Prosent:** Det står mellomrom før prosenttegnet.
  - **WAPE vises med én desimal**, for eksempel «7,4 %» eller «24,0 %», slik at nesten like verdier for baseline og ETS ikke ser like ut.
  - Intervalldekning vises i hele prosent, for eksempel «83 %».
- **Udefinert WAPE** vises som «–» (tankestrek, PRD-regel). Den står høyrejustert som et tall. For skjermleser er den merket opp som `<span aria-hidden="true">–</span><span class="sr-only">udefinert</span>`. Når produktet ikke har backtest, er den skjulte teksten «ingen backtest».
- **Måneder:**
  - grafaksen, scenariotabellen, historikktabellen og detaljtabellen bruker kort norsk form, for eksempel «nov. 2026»
  - valideringsmeldinger og advarsler bruker formatet fra fila, for eksempel `2025-03`, slik at Kari finner raden i Excel
- **Tidspunkt i datasettvelgeren:** alltid fullt format, for eksempel «salg_2026-10.csv · 13.11.2026 kl. 09.42». Det brukes ingen relativ dato som «i dag».
- **Desimalskilletegn** er komma overalt der det trengs. Punktum brukes aldri.

## Component Patterns

Her står oppførselen. Utseendet står i DESIGN.md under *Components*.

| Komponent | Atferd |
|---|---|
| **Topplinje** | Er ikke festet. Den scroller bort med siden. Kolonnekravet under **Last opp CSV** er synlig hele tiden og knyttet til knappen med `aria-describedby`. |
| **Last opp CSV** | Åpner nettleserens filvelger, avgrenset til `.csv`. Når en fil er valgt, starter én forespørsel (FR-7) og lasteboksen vises. Det er ingen ekstra bekreftelse. Hvis Kari avbryter filvelgeren, skjer ingenting. En fil som ikke er CSV (valgt via «Alle filer»), sendes og avvises på vanlig måte med feilmeldingen om skilletegn eller kolonner. |
| **Datasettvelger** | shadcn `Select`, med nyeste datasett øverst og valgt som standard. Et valg laster datasettet uten ny kjøring (FR-6, UJ-4), og da gjelder tilstanden *Datasett byttes*. Etter godkjent opplasting blir det nye datasettet valgt automatisk (FR-18). Like filnavn skilles fra hverandre med tidspunktet. |
| **Valideringsrapport** | Er alltid synlig for valgt datasett (FR-18). **Godkjent:** sammenfoldet til tre linjer: oppsummeringslinjen, fordelingslinjen (for eksempel «Fordeling: ingen 1 · sesongnaiv 2 · ets 197») og lenkeknappen «Vis advarsler ({n})». Knappen vises bare når n > 0. Et klikk folder ut alle advarslene (FR-4), og knappeteksten skifter til «Skjul advarsler». Rapporten folder seg sammen igjen når et annet datasett velges. **Avvist eller feilet:** se *State Patterns*. |
| **Søk i produktlisten** | Synlig etikett «Søk produkt-ID». Feltet filtrerer fortløpende på `produkt_id` (inneholder, uavhengig av store og små bokstaver), og sorteringen etter FR-19 beholdes i treffene. Telleren «Viser {x} av {n}» oppdateres for skjermleser 500 ms etter siste tastetrykk. Esc tømmer feltet. Hvis valgt produkt faller utenfor filteret, blir det likevel stående i graf og tabeller. |
| **Produktliste** | Sortert etter FR-19, med flagg og WAPE i hver rad. WAPE er for ETS når ETS-backtest finnes, ellers for baseline (PRD §11.1). Flaggede produkter uten WAPE står sist blant de flaggede (FR-19). Et klikk eller en piltast velger produktet, og graf, scenariotabell og backtest-tabell oppdateres (FR-19). Første rad i FR-19-rekkefølgen, altså det svakeste produktet, velges automatisk etter innlasting, etter en godkjent kjøring og etter bytte av datasett. Kari kan velge et annet produkt når hun vil. Valgt rad scrolles inn i synsfeltet med `scrollIntoView({block: 'nearest'})`. Produktdetaljer hentes 200 ms etter siste trykk på en piltast, og naboproduktene hentes på forhånd (TanStack Query `prefetchQuery`). |
| **Flagg-merke** | Er ikke interaktivt og har ingen tooltip. Teksten står alltid ved siden av ikonet. Ikonet er `aria-hidden`. |
| **Graf** | Viser ETS-prognosen for produkter med historikknivå *ets* og den sesongnaive prognosen for nivå *sesongnaiv*. Baseline vises aldri i grafen for *ets*-produkter (FR-10). Aksen viser hele historikken pluss 6 prognosemåneder. Tooltip ved hover: historiske måneder viser «Faktisk», og prognosemåneder viser Pessimistisk / Forventet / Optimistisk. Esc skjuler tooltipen til neste pekerbevegelse. Forklaringen (legend) har «Historikk», «Forventet (P50)» og «Spenn Pessimistisk–Optimistisk (P10–P90)». «Spenn» er ikke et ord fra ordlista. Det er valgt for å unngå «80 % prediksjonsintervall» (se *Åpne punkter*). |
| **Historikktabell** | Lenkeknappen «Vis historikk som tabell» viser og skjuler en tabell med kolonnene *Måned · Faktisk*, nyeste måned øverst. Utfylte måneder (FR-4) har «(fylt inn)» etter tallet. Tabellen er tekstalternativet til historikkdelen av grafen, mens scenariotabellen dekker prognosedelen. Økten husker om tabellen er åpen eller lukket. |
| **Scenariotabell** | Seks månedsrader og en sumrad (FR-11, FR-21). Tabellen er statisk og kan ikke sorteres. Merknaden fra FR-12 vises alltid og er knyttet til tabellen med `aria-describedby`. |
| **Backtest-tabell** | Kolonnene er *Sesongnaiv baseline* og *ETS*, og radene er WAPE og Intervalldekning. Dommerlinjen står under (se *Faste tekster*). Ved *ETS taper* vises begge WAPE-tallene, og ETS-prognosen ligger fortsatt i grafen (FR-17). Lenkeknappen «Vis detaljer per opprinnelse (6)» vises bare når produktet har backtest, og åpner detaljtabellen. Økten husker om detaljtabellen er åpen eller lukket, også når Kari bytter produkt. |
| **Detaljer per opprinnelse** | Én rad per opprinnelse (6), med kolonnene *Måned · Faktisk · Baseline P50 · Baseline avvik · Baseline i spenn · ETS P50 · ETS avvik · ETS i spenn*. «Avvik» er \|faktisk − P50\|, og «i spenn» er «ja» eller «nei» for P10 ≤ faktisk ≤ P90. Sumraden har Σ faktisk og Σ avvik per modell, så WAPE = Σ avvik / Σ faktisk kan regnes etter (NFR-5). Antall «ja» delt på 6 gir dekningen. Har produktet bare baseline-backtest, vises bare baseline-kolonnene. Tabellen har den synlige `<caption>` «Detaljer per opprinnelse – {produkt_id}». Øverste venstre celle i backtest-tabellen har den skjulte teksten «Mål». |
| **WAPE-oversikt** | Viser totalen etter malen i *Faste tekster*, for eksempel «Total WAPE: Sesongnaiv baseline 21,3 % · ETS 18,1 % · ETS slår baseline for 162 av 180 produkter» (FR-22). Linjen er statisk og ikke klikkbar. Den oppdateres når et annet datasett velges. |
| **Lasteboks** | Se *Kjøring pågår*. Boksen ligger i DOM som søsken til app-roten, utenfor elementet som får `inert`. |

## State Patterns

| Tilstand | Del | Behandling |
|---|---|---|
| **Første oppstart** | Hele siden | Det syntetiske datasettet er valgt (FR-25), og siden ser ut som etter en vanlig godkjent opplasting, med første produkt valgt. |
| **Kjøring pågår** (opptil 60 s, NFR-7) | Hele siden | App-roten får `inert` og et hvitt slør. Lasteboksen viser spinneren og teksten «Kjører validering og prognose – dette kan ta opptil ett minutt». Boksen får fokus (`tabindex="-1"`), og teksten skrives inn i en `role="status"`-region som alltid finnes i DOM. Boksen ligger utenfor app-roten. Det er ingen avbrytknapp og ingen trinnvis fremdrift. Etter 120 s slutter klienten å vente og går til *Kjøring feilet*. |
| **Godkjent etter kjøring** | Rapport og liste | Det nye datasettet blir valgt. Rapporten vises sammenfoldet (fokus: se *Fokusstyring*). Listen er sortert, og første rad er valgt. |
| **Fil avvist** (FR-3, UJ-2) | Valideringsrapport | Overskrift og «{n} feil» etter *Faste tekster*. **Alle** feilene listes i filrekkefølge med radnummer, etter malene i *Faste tekster*. Når listen er høyere enn 320 px, scroller den inne i rapporten. Feillisten er da en fokuserbar region (`tabindex="0"`, `role="region"`, `aria-label="Feil i fila"`). Fokus: se *Fokusstyring*. Datasettvelgeren og resten av dashbordet viser fortsatt datasettet som var valgt før. **«Lukk»** fjerner avvisningen, viser den godkjente rapporten for valgt datasett igjen. En ny opplasting eller et nytt datasettvalg fjerner også avvisningen. |
| **Kjøring feilet** (FR-7, eller tidsavbrudd) | Valideringsrapport | Samme røde variant som *Fil avvist*, med overskrift etter *Faste tekster*. Under står feilmeldingen fra backend på norsk, eller teksten for tidsavbrudd. «Lukk» virker som over. |
| **Ingen kontakt med backend** | Valideringsrapport | Rød variant med teksten fra *Faste tekster*. Fokus flyttes til teksten. Tilstanden finnes ikke i PRD-en, men følger av at frontend og backend er adskilt. |
| **Datasett byttes** (UJ-4) | Rapport, liste, graf, tabeller, WAPE | Det kommer ikke noe slør, og datasettvelgeren kan fortsatt brukes. Rapport, liste og WAPE-linje viser `Skeleton` til dataene er kommet, og deretter velges første produkt. Panelene har `aria-busy="true"` mens de laster. |
| **Produktdetalj lastes** | Graf og tabeller | Forrige produkt blir stående i 150 ms. Deretter vises `Skeleton` til dataene er kommet. Panelene har `aria-busy="true"` mens de laster. |
| **Produktdetalj kunne ikke hentes** | Graf og tabeller | En dempet linje midt i grafområdet viser teksten og lenkeknappen fra *Faste tekster*. Tabellene er tomme. |
| **Historikknivå *ingen*** | Graf, scenario, backtest | Grafen viser bare historikk, med den faste teksten fra FR-20. Scenariotabellen viser den samme teksten og merknaden. Backtest-tabellen viser «Ingen backtest (under 18 måneders historikk)», og knappen for detaljer vises ikke. |
| **Ingen backtest** (12–17 mnd) | Backtest-tabell | «Ingen backtest (under 18 måneders historikk)», uten dommerlinje og uten knapp for detaljer. |
| **Bare baseline-backtest** (18–29 mnd) | Backtest-tabell | Baseline-kolonnen vises. ETS-kolonnen viser «ETS er ikke backtestet (under 30 måneders historikk)». Dommerlinjen vises ikke, og detaljene har bare baseline-kolonnene. |
| **Flagget *ETS taper*** | Liste og backtest | Flagget står i raden. Backtest-tabellen viser begge WAPE-tallene og «ETS taper mot baseline», og grafen viser ETS. Systemet gir ingen anbefaling (FR-17). |
| **Lik WAPE** | Backtest-tabell | «ETS og baseline har lik WAPE». Produktet får ikke flagget *ETS taper* (PRD §11.2). |
| **WAPE udefinert** (Σ faktisk = 0) | Liste og backtest | WAPE vises som «–». Dommerlinjen er «Kan ikke sammenlignes (WAPE er udefinert når faktisk salg er 0)». Produktet står rett etter de flaggede produktene i listen (FR-19). |
| **WAPE-oversikt uten grunnlag** (m = 0) | WAPE-oversikt | Malen for m = 0 i *Faste tekster*. |
| **Søk uten treff** | Produktliste | Teksten og lenkeknappen fra *Faste tekster*. Graf og tabeller viser fortsatt valgt produkt. |

## Interaction Primitives

- **Musen er det vanlige verktøyet, men alt kan gjøres med tastaturet.** Det er ingen hurtigtaster i v1 utover Esc i søkefeltet og Esc for tooltipen i grafen.
- **Produktlisten** er en ARIA-`listbox` (`aria-label="Produkter, svakeste først"`) med roving tabindex og *selection follows focus*:
  - Pil opp og ned flytter fokus og velger produktet med en gang, slik at Kari kan bla gjennom de svake produktene uten å trykke Enter. Valget er en innholdsendring på samme side, ikke en kontekstendring (WCAG 3.2.1/3.2.2).
  - Home og End går til første og siste treff.
  - Når Kari tabber inn i listen, får valgt rad fokus hvis den er synlig i filteret. Ellers får første treff fokus **uten** å bli valgt. Valget skjer først ved piltast, Enter eller klikk.
  - Hver rad har et tilgjengelig navn, for eksempel «P-109, WAPE 24,0 %, flagg: ETS taper». Foran tallet står et visuelt skjult «WAPE».
- **Grafen** har ingen tastaturinteraksjon (se *Accessibility Floor*). Tooltipen vises ved hover og er et tillegg.
- **Klikk og Enter.** Alt utføres med klikk eller Enter. Det finnes ingen hover-only-funksjoner, ingen dra-og-slipp og ingen høyreklikkmenyer.
- **Forbudt:** modaler, bekreftelsesdialoger, toast-varsler for resultater (resultatet står i valideringsrapporten), uendelig scrolling og animasjoner i grafen.

## Accessibility Floor

Målet er WCAG 2.1 AA. Her står kravene til oppførsel. Kontrastverdiene står i tabellen i DESIGN.md (*Colors*).

- **Tastatur:**
  - Tab-rekkefølgen:
    1. Hopplenke («Hopp til produktlisten»; målelementet har `tabindex="-1"`)
    2. Datasettvelger
    3. Last opp CSV
    4. Rapporten: «Vis advarsler», «Lukk» og feillisten når den scroller
    5. Søk
    6. Produktliste (ett tabstopp)
    7. Vis historikk som tabell
    8. Vis detaljer per opprinnelse
    9. Scrollende regioner ved reflow
  - Statiske tabeller er ikke tabstopp.
  - Fokusringen følger `{components.focus-ring}` i DESIGN.md og er alltid synlig.
- **Fokusstyring** (eneste kilde for fokusreglene):
  - Under kjøring har lasteboksen fokus (se *Kjøring pågår*).
  - Når sløret fjernes, flyttes fokus alltid til rapportoverskriften: ved godkjent kjøring, avvist fil og feilet kjøring.
  - Etter «Lukk» går fokus til **Last opp CSV**.
  - Fokus havner aldri på `<body>`.
- **Etiketter:**
  - Alle kontroller har et synlig navn: «Datasett», «Søk produkt-ID» og **Last opp CSV**.
  - Kolonnekravet står synlig under knappen, og `aria-describedby` peker til den samme teksten.
- **Annonsering:**
  - Lasteboksen: `role="status"`, se *Kjøring pågår*.
  - Resultatet av en kjøring annonseres ved at fokus flyttes til rapportoverskriften, ikke med `aria-live` eller `role="alert"`, slik at teksten ikke leses to ganger.
  - Søketelleren er `aria-live="polite"`, med 500 ms forsinkelse.
- **Ikke bare farge:**
  - Flaggene har ikon og tekst.
  - Valgt rad har en stripe og `aria-selected`.
  - Historikk og prognose i grafen har forskjellig linjestil, og båndet har kantlinjer.
  - Dommerlinjen er tekst.
- **Grafen:**
  - Grafen har `role="img"` og en `aria-label`, for eksempel: «Prognose for P-109: historikk fra jan. 2023 til okt. 2026, Forventet 960 over 6 måneder, spenn 820–1 110.»
  - Grafen kan ikke fokuseres og har ingen piltaster.
  - Historikktabellen og scenariotabellen utgjør sammen tekstalternativet (WCAG 1.1.1).
- **Tabeller:**
  - Bruk ekte `<table>` med `<caption>`. Den kan være visuelt skjult.
  - Måned og «Sum» er `<th scope="row">`, og kolonneoverskriftene er `<th scope="col">`.
  - Når ETS-kolonnen erstattes av den faste teksten, beholdes `<th scope="col">ETS</th>`, og teksten spenner over cellene.
- **Symboler:**
  - «✓» og «→» er `aria-hidden`, og teksten bærer meningen.
  - «–» for udefinert WAPE har en visuelt skjult tekst (se *Tall- og datoformat*).
- **Inert under kjøring:** se *Kjøring pågår*.
- **Bevegelse:** Spinneren respekterer `prefers-reduced-motion`.
- **Tekstavstand:** Elementer med tekst har ingen faste høyder (WCAG 1.4.12, se DESIGN.md).
- **Zoom og reflow:** se *Responsive & Platform*.

## Responsive & Platform

| Bredde (CSS-px) | Atferd |
|---|---|
| ≥ 1280 | Målbredden, med full layout som i DESIGN.md (*Layout & Spacing*). |
| 1024–1279 | Samme layout, men tettere. Produktlisten har `{spacing.sidebar-width-compact}`. |
| < 1024, ned til 320 (zoom 200–400 %) | Reflow i én kolonne: topplinje → rapport → produktliste → graf → scenario → backtest → detaljer → WAPE. Dette er ikke mobilstøtte. Reflow gjør zoom brukbar (WCAG 1.4.10). Topplinjen og WAPE-oversikten er ikke festet, og WAPE-linjen ligger sist i flyten. Produktlisten er ikke sticky og har `max-height: max(50vh, 240px)`. Lasteboksen har `max-width: calc(100vw - 32px)`. Grafen og tabellene kan scrolle vannrett, siden todimensjonalt innhold er unntatt fra reflow-kravet. De er da fokuserbare regioner med navn. |

**Høyde:** se DESIGN.md, *Layout & Spacing*.

**Test:** Playwright kjører layouten ved 1280 × 720, 1280 × 1080 og 320 × 256.

**Nettlesere:** PRD-en sier ikke noe om nettleserstøtte. Antakelsen er siste versjon av Chrome og Edge, fordi Playwright kjører mot Chromium.

## Inspiration & Anti-patterns

- **Hentet fra Excel:** høyrejusterte tall med faste sifferbredder, tynne rutenettlinjer, tette rader og tabeller som ser ut som regneark. Kari skal kjenne seg hjemme med en gang.
- **Hentet fra PRD-prinsippet *baseline først*:** ETS står aldri alene. Baseline står først i backtest-tabellen, i detaljene og i WAPE-oversikten.
- **Forkastet: KPI-kort med store tall.** De gjør tallene til pynt og konkurrerer med tabellene.
- **Forkastet: trafikklys på WAPE.** De antyder en dom systemet ikke skal felle, og de bygger bare på farge.
- **Forkastet: anbefalinger og «AI-innsikt».** PRD-en sier uttrykkelig at systemet ikke anbefaler noe.
- **Forkastet: toast-varsler for resultater.** Resultatet hører hjemme i valideringsrapporten, der det blir stående.
- **Forkastet: trinnvis fremdrift og antall produkter i lasteteksten.** Begge krever ekstra backend- eller klientlogikk, og FR-7 sender alt i én forespørsel.
- **Forkastet: interaktiv graf med piltaster.** Tabellene gir de samme tallene på en enklere og mer robust måte.

## Key Flows

### UJ-1. Kari lager månedens prognose

Kari, etterspørselsplanlegger, siste uka i måneden. Hun har nettopp eksportert `salg_2026-10.csv` fra ERP.

1. Kari åpner PROGNOS i nettleseren. Forrige datasett er valgt.
2. Hun klikker **Last opp CSV** og velger fila. Lasteboksen viser «Kjører validering og prognose – dette kan ta opptil ett minutt», og siden er låst.
3. Etter cirka 40 sekunder forsvinner sløret, og fokus står på rapportoverskriften. Datasettvelgeren viser nå `salg_2026-10.csv · 13.11.2026 kl. 09.42`. Rapporten under topplinjen viser:
   - «✓ 200 produkter godkjent · 3 flagget (kort historikk)»
   - «Fordeling: ingen 1 · sesongnaiv 2 · ets 197»
   - «Vis advarsler (2)»
4. Produktlisten viser de svakeste produktene øverst, og første rad er allerede valgt. Graf og tabeller viser det produktet uten at Kari har klikket. (I PRD-ens UJ-1 velger Kari selv. Autovalget er et bevisst avvik, se *Åpne punkter*.)
5. Grafen viser hele historikken som en heltrukket linje, en stiplet Forventet-linje 6 måneder fram og et blått bånd med kantlinjer. Markøren «Prognose →» står der horisonten starter.
6. **Klimaks:** Scenariotabellen viser sumraden *Pessimistisk 820 · Forventet 960 · Optimistisk 1 110*, med merknaden under. Kari har et tall å gi videre til MRP (materialbehovsplanleggingen) og et spenn å ta med til samtalen om sikkerhetsmargin med materialplanleggeren. Vurderingen gjør hun selv.

**Kanttilfelle:** Hun velger et produkt med 8 måneders historikk. Grafen viser bare historikken og «Ingen prognose: under 12 måneders historikk». Flagget *kort historikk* står i raden.

**Feil:** Kjøringen feiler eller tar mer enn to minutter. Rapporten blir rød med «Prognosen kunne ikke kjøres. Ingenting er lagret.», og forrige datasett blir stående (*Kjøring feilet*).

### UJ-2. Kari får fila avvist og retter den

1. Kari laster opp en fil med et duplikat og én rad der `antall` er `12,5`. Lasteboksen vises kort.
2. Rapporten blir rød: «Fila ble avvist. Ingenting er lagret. · 2 feil», og fokus står på overskriften. Under står «Duplikat: P-104, 2025-03 (rad 17 og 233)» og «Rad 418: antall må være et heltall ≥ 0». Datasettvelgeren viser fortsatt forrige datasett.
3. **Klimaks:** Alle feilene står på én liste, med radnumre hun kan slå opp i Excel. Hun retter begge feilene i én omgang, uten å prøve seg fram.
4. Hun laster opp på nytt. Rapporten blir godkjent, og videre går det som i UJ-1.

### UJ-3. Kari sjekker om hun kan stole på prognosen

1. Øverst i produktlisten står P-109 med flagget *ETS taper* (pil-ned-ikon og tekst). Raden er valgt automatisk.
2. Grafen viser ETS-prognosen som vanlig. Backtest-tabellen viser:
   - Sesongnaiv baseline: WAPE 19,0 %
   - ETS: WAPE 24,0 %
   - intervalldekning for begge
   - dommerlinjen «ETS taper mot baseline»
3. Hun åpner «Vis detaljer per opprinnelse (6)». Under tabellene ser hun avviket per måned for begge modellene. Baseline har lavere avvik i fire av seks måneder, og sumraden gir de samme WAPE-tallene som tabellen.
4. **Klimaks:** Blikket går ned til WAPE-oversikten: «ETS slår baseline for 162 av 180 produkter», og ETS har lavere total WAPE. Hun ser at metoden holder totalt sett, men at akkurat P-109 må vurderes med skjønn. Systemet sier ikke hva hun skal gjøre.

### UJ-4. Kari åpner forrige måneds datasett igjen

1. Neste morgen åpner Kari PROGNOS. Det nyeste datasettet er valgt.
2. Hun åpner datasettvelgeren og velger `salg_2026-10.csv`.
3. **Klimaks:** Etter et kort øyeblikk med `Skeleton` er valideringsrapporten, produktlisten, prognosene og backtestene der, akkurat som i går. Det kommer ingen lasteboks og ingen ny kjøring. Hun kan fortsette der hun slapp.

**Feil:** Datasettet kan ikke hentes. Rapporten viser *Ingen kontakt med backend*.

## Åpne punkter

- **PRD spm. 3:** Forstår Kari «80 % prediksjonsintervall» og merknaden om scenariototalene? Svaret kan endre forklaringen i grafen («Spenn …») og plasseringen av merknaden. Spesifikasjonen unngår «80 %» i hovedteksten og bruker scenarionavnene.
- **Addendum H6:** Disse delene trenger API-støtte som ikke finnes ennå:
  - WAPE-oversikten og total WAPE
  - detaljtabellen per opprinnelse, som trenger faktisk, P10, P50 og P90 per modell og opprinnelse
  - gjenvisning av valideringsrapporten

  UX-en forutsetter at arkitekturen løser dette.
- **Åpent punkt for PRD-en: søk i produktlisten.** Søk er et tillegg utover PRD-en. Det legges inn som et nytt funksjonskrav (FR) etter UX-økten.
- **Åpent punkt for PRD-en: autovalg i UJ-1.** UJ-1 steg 4 bør oppdateres, fordi første produkt nå velges automatisk.
