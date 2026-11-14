# Validation Report — G96-ellingsen

- **DESIGN.md:** `_bmad-output/planning-artifacts/ux-designs/ux-G96-ellingsen-2026-11-14/DESIGN.md`
- **EXPERIENCE.md:** `_bmad-output/planning-artifacts/ux-designs/ux-G96-ellingsen-2026-11-14/EXPERIENCE.md`
- **Run at:** 2026-11-14T20:53:19+01:00

## Overall verdict

**Rubrikken: adequate. Kontrakten er brukbar etter at de høye funnene er rettet.** Paret er stramt og godt forankret i kildene. Alle fire brukerreisene finnes med navnene ordrett fra PRD-en, med protagonist, nummererte steg og klimaks. Alle `{token}`-referansene resolver, alle farger har hex, seksjonsrekkefølgen følger spesifikasjonen, og de ordrette tekstene for FR-20 og FR-21 er riktige. Tre punkter tvinger likevel en nedstrøms konsument til å gjette eller bryte et krav: dommerlinjen i backtest-tabellen er binær og motsier PRD-ordlista om like og udefinerte WAPE-verdier, inndatakantene har 1,38:1 og bryter WCAG 1.4.11, og det finnes ingen modell for vertikal scrolling eller noe høydebudsjett for 720 CSS-px. Resten er middels og lave presiseringer: manglende feilmeldingsmaler, interne motsetninger i DESIGN.md, komponentnavn som ikke stemmer mellom filene, og noen manglende tilstander.

**Tilgjengelighetsreviewen (godkjent med endringer, 5 høye) skjerper bildet.** Tre saker som rubrikken førte som middels, er reelle AA-brudd hvis spinen implementeres som skrevet, og løftes derfor til høy: fokusringen arver shadcn sin 50 %-ring (2,27:1), grafen er både `role="img"` og fokuserbar og mangler tekstalternativ for historikken, og fokus går tapt etter avvisning, feil og «Lukk». I tillegg kommer reflow ned til 320 CSS-px som ny høy sak. Begge reviewerne fant inndatakanten, fokusringen, båndkontrasten, grafmodellen, fokus etter avvisning og tidsavbruddet; de er slått sammen nedenfor. Etter sammenslåing står spinen med 7 høye funn, og 5 av dem gjelder tilgjengelighet. Mockup-renderingen bekrefter at panelhoder og advarselstekst mangler, og fant én faktisk inkonsistens i eksempeltallene. Ingen funn er kritiske.

## Category verdicts

- Flow coverage — adequate
- Token completeness — adequate
- Component coverage — adequate
- State coverage — thin
- Visual reference coverage — venter på promotering (mockupene ligger i `.working/key-dashbord.html` og `.working/key-avvist.html`)
- Bloat & overspecification — strong
- Inheritance discipline — adequate
- Shape fit — strong

## Findings by severity

Etter sammenslåing: critical 0 · high 7 · medium 21 · low 35 (63 i alt). Funn som begge reviewerne fant, er merket *Funnet av begge*, og den høyeste alvorligheten gjelder.

### Critical (0)

Ingen.

### High (7)

**[Token completeness]** — Kant på inndatafelt (søk, datasettvelger) er 1,38:1 og bryter 1.4.11 (§ DESIGN frontmatter `colors`, Components: Input, Select)
`input` arves fra shadcn og er ikke overstyrt. `#D9DCE0` gir 1,38:1 mot hvitt (shadcn-standarden ~1,26:1). Kontrollene identifiseres bare av kanten, og kravet er 3:1. *Funnet av begge: rubrikk §2 (high), tilgjengelighet H2 (high).*
Fix: Eget token `input` på minst 3:1, for eksempel `#767C85` (4,21:1) eller `#8A919A` (3,18:1). Behold `border` for paneler, og la Input og Select bruke `{colors.input}`.

**[Token completeness]** — Fokusringen arver shadcn sin 50 %-ring og feiler 1.4.11 / svekker 2.4.7 (§ DESIGN frontmatter `ring`, EXPERIENCE Accessibility Floor)
`ring-ring/50` gir effektivt `#8FAFD6`: 2,27:1 mot hvitt, 2,81:1 rundt primærknappen, 2,14:1 i valgt rad. Spinen oppgir ikke bredde, offset eller opasitet. *Funnet av begge: rubrikk §2 (medium), tilgjengelighet H1 (high). Løftet til høy.*
Fix: 2 px heltrukken `#1F5FAD` i 100 % opasitet med 2 px offset i `{colors.background}`, og overstyr `ring-ring/50` globalt.

**[Component coverage]** — Grafen er både `role="img"` og fokuserbar med piltaster, og historikken mangler tekstalternativ (§ EXPERIENCE Interaction Primitives, Accessibility Floor → Grafen, Component Patterns → Graf)
`role="img"` gjør tooltip-innholdet usynlig for skjermleser og bryter 4.1.2 for en interaktiv kontroll. De historiske månedsverdiene finnes bare i grafen (1.1.1/1.3.1). *Funnet av begge: rubrikk §3 (medium), tilgjengelighet H3 (high). Løftet til høy.*
Fix: Velg én modell. Anbefalt: `role="img"` med `aria-label`, ikke fokuserbar, og en `Collapsible` «Vis historikk som tabell». Alternativt `role="group"` + `aria-roledescription="graf"` + `aria-live`-region for måneden som har fokus.

**[State coverage]** — Dommerlinjen i backtest-tabellen har bare to verdier (§ EXPERIENCE Component Patterns → Backtest-tabell)
Like WAPE-verdier blir «taper», noe som motsier PRD §3 og §11.2. Det finnes ingen tekst for udefinert WAPE (FR-14).
Fix: Fire tilfeller: «ETS slår baseline», «ETS taper mot baseline», «ETS og baseline har lik WAPE», «Kan ikke sammenlignes (WAPE er udefinert når faktisk salg er 0)», med tilsvarende rader i State Patterns.

**[State coverage]** — Ingen modell for vertikal scrolling og intet høydebudsjett (§ DESIGN Layout & Spacing, EXPERIENCE Responsive & Platform)
Innholdet er nesten 950 px, mot 720 CSS-px på en laptop med 150 % skalering. Klimakset i UJ-1 kan havne under bretten.
Fix: Minimumshøyde 720 px. Siden scroller, og listen er `sticky` med høyde `100vh − topplinje − WAPE`. Vurder sammenfoldbar godkjent rapport.

**[State coverage]** — Fokus går tapt etter avvist fil, feilet kjøring, backend-feil og «Lukk» (§ EXPERIENCE State Patterns → Fil avvist, Accessibility Floor → Inert under kjøring)
Bare godkjent kjøring flytter fokus. `inert` kaster fokus til `<body>`. Det står ikke hva «Lukk» viser etterpå (FR-18). *Funnet av begge: rubrikk §4 (medium), tilgjengelighet H4 (high). Løftet til høy.*
Fix: Når sløret fjernes, flytt fokus til rapportoverskriften (`tabindex="-1"`) for alle utfall. «Lukk» viser rapporten for valgt datasett igjen. Fokus går til rapportoverskriften når en rapport kommer tilbake, ellers til **Last opp CSV**. Reviewerne foreslo ulike mål her.

**[Tilgjengelighetsreview]** — H5. Reflow er bare spesifisert for 200 %, ikke 320 CSS-px, og den festede WAPE-linja spiser viewporten (1.4.10) (§ DESIGN Layout & Spacing, EXPERIENCE Responsive & Platform)
Ved 400 % (~341×192 CSS-px) tar WAPE-linja halve høyden, og produktlisten blir ~96 px.
Fix: Reflow ned til 320 CSS-px. Under 1024 px er WAPE-linja og topplinja ikke festet, listen får `max-height: max(50vh, 240px)`, og lasteboksen `max-width: calc(100vw - 32px)`. Test i Playwright med 320×256.

### Medium (21)

**[Flow coverage]** — Feilmeldingene for avvist fil har bare to eksempler (§ EXPERIENCE Voice and Tone, Key Flows UJ-2)
Minst fem feiltyper fra FR-2/FR-3 mangler mal, så NFR-4-testene har ingenting å sjekke mot.
Fix: Tabell «Feilmeldinger (FR-2, FR-3)» under Faste tekster med én mal per regel.

**[Flow coverage]** — Advarselsteksten for utfylte måneder (FR-4) mangler mal (§ EXPERIENCE Component Patterns → Valideringsrapport)
Bare «én per produkt med månedene listet». Mocken måtte finne opp teksten.
Fix: For eksempel «P-031: 2 måneder fylt inn med 0 (2025-03, 2025-07)».

**[Token completeness]** — P10–P90-båndet har 1,42:1 mot hvitt (1.4.11) (§ DESIGN frontmatter `chart-band`, Colors → Grafen)
Båndet bærer informasjon (FR-20). Scenariotabellen dekker verdiene, så det er ikke blokkerende. *Funnet av begge: rubrikk §2 (medium), tilgjengelighet M1 (medium).*
Fix: 1 px kantlinjer på P10 og P90 i nytt token `chart-band-edge`, for eksempel `#4A74B5` (4,71:1). Samme kant på forklaringsfeltet.

**[Token completeness]** — Kontrasttallene er ikke samlet (§ DESIGN Colors)
EXPERIENCE henviser til tall som ikke finnes. «Minst 6:1» gjelder bare mot hvitt.
Fix: Kontrasttabell i DESIGN Colors. Tallene står i begge reviewfilene.

**[Component coverage]** — Komponentnavnene er ikke like i de to filene (§ DESIGN Components, EXPERIENCE Component Patterns)
«Prognosegraf»/«Graf», «Produktrad»/«Produktliste». Topplinje, Flagg-merke og Lasteboks mangler i EXPERIENCE.
Fix: Bruk PRD-navnet «Graf», og legg inn de manglende radene.

**[Component coverage]** — Kolonnene i backtest-utvidelsen er ikke definert (§ EXPERIENCE Component Patterns → Backtest-tabell)
FR-21 og NFR-5 krever at WAPE kan regnes etter.
Fix: *Opprinnelse · Måned · Faktisk · P50 baseline · P50 ETS*, eventuelt |feil| og sumrad. Si hva som vises ved bare baseline-backtest.

**[Component coverage]** — Teksten i panelhodene er ikke fastsatt (§ DESIGN `panel-header`, EXPERIENCE IA)
NFR-4 sjekker overskriftene, og mocken måtte finne dem opp.
Fix: «Prognose – {produkt_id}», «Scenarioer», «Backtest (siste 6 måneder)», «Produkter» under Faste tekster.

**[State coverage]** — Ingen tilstand for lasting ved bytte av datasett (§ EXPERIENCE Datasettvelger, UJ-4 steg 3)
Fix: Raden «Datasett byttes»: Skeleton i rapport, liste og WAPE-linje, ingen slør, Select er aktiv.

**[State coverage]** — «{n} produkter» i lasteboksen krever et arkitekturvalg (§ EXPERIENCE State Patterns → Kjøring pågår)
FR-7 gir én forespørsel, så n er ukjent før svaret.
Fix: Frontend teller unike `produkt_id` før opplasting, ellers generell tekst. Si det eksplisitt.

**[State coverage]** — Ingen tidsavbrudd for kjøringen (§ EXPERIENCE State Patterns → Kjøring pågår)
En forespørsel som henger, låser hele siden (`inert`), i praksis en felle (jf. 2.1.2). *Funnet av begge: rubrikk §4 (low), tilgjengelighet M6 (medium). Løftet til middels.*
Fix: Klientgrense på ~120 s → *Kjøring feilet* med norsk melding og fokusregelen over.

**[Inheritance discipline]** — Rødt brukes i en tilstand DESIGN ikke tillater (§ EXPERIENCE State Patterns → Ingen kontakt med backend)
Fix: Utvid regelen til «avvist, feilet eller utilgjengelig», eller bruk grå variant.

**[Inheritance discipline]** — Regelen for blått motsier seg selv (§ DESIGN Colors, Do's and Don'ts)
Fix: «Valgt, prognose og handling (primærknapp, lenkeknapper, fokus)».

**[Inheritance discipline]** — Fontvektene motsier hverandre (§ DESIGN Typography)
«Bare 400 og 600», men label er 500.
Fix: Label til 400 eller 600, eller skriv tre vekter.

**[Tilgjengelighetsreview]** — M2. Roving tabindex uspesifisert ved filter og Tab inn i listen (§ EXPERIENCE Interaction Primitives → Produktlisten)
Selection-follows-focus er OK, men Tab inn må aldri bytte produkt, og hvert piltrykk gir Skeleton.
Fix: Tab inn fokuserer valgt rad hvis synlig, ellers første treff uten valg. Debounce ~200 ms, `aria-busy`, `aria-label="Produkter, svakeste først"`.

**[Tilgjengelighetsreview]** — M3. Live-regioner må finnes i DOM før innholdet settes (§ EXPERIENCE Annonsering, Kjøring pågår)
Fix: Permanent statusregion utenfor det inerte treet. Lasteboksen som søsken av app-roten med `tabindex="-1"` og fokus.

**[Tilgjengelighetsreview]** — M4. Recharts-tooltipen oppfyller ikke 1.4.13 (§ EXPERIENCE Component Patterns → Graf)
Fix: Esc skjuler tooltipen, og den plasseres så den ikke dekker punktet.

**[Tilgjengelighetsreview]** — M5. Udefinert WAPE «–» leses ikke av skjermleser (§ EXPERIENCE Tall- og datoformat)
Fix: `aria-hidden` på «–» pluss visuelt skjult «udefinert».

**[Tilgjengelighetsreview]** — M7. Scrollbare regioner må nås med tastatur (2.1.1) (§ EXPERIENCE Fil avvist, Responsive & Platform)
Fix: `tabindex="0"`, `role="region"` og `aria-label` på hver scrollbeholder.

**[Tilgjengelighetsreview]** — M8. Produktradens tilgjengelige navn er uklart (1.3.1) (§ DESIGN Produktrad, EXPERIENCE Produktliste)
Fix: «P-109, WAPE 24,0 %, flagg: ETS taper», ikonene `aria-hidden`. Avklar hvilken WAPE raden viser.

**[Tilgjengelighetsreview]** — M9. Kravet til CSV-kolonner er bare usynlig instruks (3.3.2) (§ EXPERIENCE Accessibility Floor → Etiketter)
Fix: Synlig linje «CSV med kolonnene produkt_id, maaned, antall», og pek `aria-describedby` dit.

**[Mockup-rendering]** — Eksempelet på historikkfordeling stemmer ikke med «3 flagget (kort historikk)» (§ EXPERIENCE Component Patterns → Valideringsrapport, Key Flows UJ-1 steg 3)
«ingen 3 · sesongnaiv 15 · ets 182» gir 18 med kort historikk, fordi både *ingen* og *sesongnaiv* flagges etter FR-5.
Fix: For eksempel «ingen 1 · sesongnaiv 2 · ets 197», og skriv regelen k = ingen + sesongnaiv ved malen.

### Low (35)

**[Flow coverage]** — Autovalg i UJ-1 steg 4 er ikke merket som avvik fra PRD-en (§ EXPERIENCE Key Flows UJ-1)
Fix: Én setning i UJ-1 eller under Åpne punkter.

**[Flow coverage]** — UJ-1 og UJ-4 har ingen feillinje (§ EXPERIENCE Key Flows)
Fix: Én linje per flyt med henvisning til *Kjøring feilet* / *Ingen kontakt*.

**[Token completeness]** — `fontVariantNumeric` er ikke en nøkkel i spesifikasjonen (§ DESIGN `typography.table`)
Fix: Flytt `tabular-nums` til prosaen.

**[Token completeness]** — Layoutverdier står som tall i prosa (§ EXPERIENCE Responsive & Platform, State Patterns)
Fix: Gjør minst `sidebar-width-compact` og `report-max-height` til spacing-tokens.

**[Component coverage]** — Komponenter som brukes, er ikke listet i DESIGN (§ DESIGN Components)
Skeleton, spinner, hopplenke, «Lukk», «Tøm søk», «Vis alle advarsler». `Alert` er listet, men ikke brukt.
Fix: Utvid listen. Fjern `Alert`, eller si at rapporten bygger på den.

**[Component coverage]** — Tooltip og forklaring i grafen har ingen visuell spesifikasjon (§ DESIGN Components)
Fix: Én linje hver: flate, kant, typografi.

**[State coverage]** — WAPE-oversikten mangler tilstand for m = 0 (§ EXPERIENCE WAPE-oversikt)
Fix: «Total WAPE: ingen produkter har backtest for begge modellene».

**[State coverage]** — Ingen tilstand for feilet henting av ett produkt (§ EXPERIENCE State Patterns)
Fix: Dempet feillinje i grafområdet med «Prøv igjen».

**[State coverage]** — Backtest-utvidelsen er ikke beskrevet for bare baseline eller ingen backtest (§ EXPERIENCE Backtest-tabell)
Fix: Skjul knappen ved *Ingen backtest*, vis bare baseline-kolonnen ved baseline-backtest.

**[State coverage]** — Avbrutt filvelger og fil som ikke er CSV er ikke beskrevet (§ EXPERIENCE State Patterns)
Fix: Avbrudd gjør ingenting. En fil som ikke er CSV, gir vanlig avvisning.

**[State coverage]** — Piltastene gir et blink av Skeleton for hvert tastetrykk (§ EXPERIENCE Interaction Primitives → Produktlisten)
Henger sammen med tilgjengelighet M2.
Fix: `prefetchQuery` for naboer, eller Skeleton først etter ~150 ms.

**[Visual reference coverage]** — Linja «Composition reference» mangler i IA (§ EXPERIENCE Information Architecture)
Fix: Legg den inn når mockupene er promotert. Vurder mockup av lasteboksen og historikknivå *ingen*.

**[Bloat & overspecification]** — Tilstanden *Ingen produkt valgt* kan ikke oppstå (§ EXPERIENCE State Patterns)
Fix: Fjern raden, eller gjør den forbigående før autovalget.

**[Bloat & overspecification]** — Regler står to steder (§ DESIGN Colors/Components, Layout & Spacing / EXPERIENCE Responsive & Platform)
Fix: Detaljene ett sted, henvisning det andre.

**[Inheritance discipline]** — FR-21 sier «kolonne», spinen har modellene som rader (§ DESIGN Backtest-tabell)
Fix: Si at «kolonne» leses som «raden for ETS».

**[Inheritance discipline]** — «Ordrett som i PRD-en (§11.2)» stemmer ikke for alle linjene (§ EXPERIENCE Faste tekster)
Fix: Siter FR-12 ordrett, og merk FR-18 som mal.

**[Inheritance discipline]** — PRD-ens *Topplinje* inkluderer rapporten, spinen skiller dem (§ EXPERIENCE IA)
Fix: Én setning i IA.

**[Inheritance discipline]** — «Spenn Pessimistisk–Optimistisk» er ikke et ordlisteord (§ EXPERIENCE Graf)
Fix: Kort merknad i raden Graf.

**[Inheritance discipline]** — «i dag kl. 09.42» følger ikke datoformatet (§ EXPERIENCE UJ-1 steg 3)
Fix: Fast format, eller regel for relativ dato.

**[Inheritance discipline]** — Feil kildemerking i Voice and Tone (§ EXPERIENCE Voice and Tone)
Fix: «UJ-2-eksempel» i stedet for «FR-3, ordrett format».

**[Inheritance discipline]** — Oppsummeringsmalen mangler regler for n = 1 og k = 0 (§ EXPERIENCE Faste tekster)
Fix: Fastsett entall og om «· 0 flagget» vises.

**[Shape fit]** — DESIGN-frontmatteren har nøkler utenfor spesifikasjonen (§ DESIGN frontmatter)
Fix: Ingen handling nødvendig, eventuelt samle under `meta:`.

**[Tilgjengelighetsreview]** — L1. «Scenariotabell» som tab-stopp (§ EXPERIENCE Accessibility Floor → Tastatur)
Fix: Fjern, eller presiser scrollbeholderen. Ta med «Vis alle advarsler», «Lukk», «Tøm søk».

**[Tilgjengelighetsreview]** — L2. Horisontmarkøren og etiketten «Prognose →» (§ DESIGN Colors → Grafen)
2,24:1 mot båndet, og etikettfargen er ikke gitt.
Fix: Etiketten i `{colors.muted-foreground}`, vurder `#6B7480` for markøren, pilen `aria-hidden`.

**[Tilgjengelighetsreview]** — L3. Landemerker og overskriftsnivåer er ikke spesifisert (§ EXPERIENCE Accessibility Floor)
Fix: `<header>`, `<main>`, `<nav aria-label="Produkter">`, panelhoder som `<h2>`, hopplenkemål med `tabindex="-1"`.

**[Tilgjengelighetsreview]** — L4. Faste høyder mot tekstavstand (1.4.12) (§ DESIGN `topbar-height`, Produktrad)
Fix: `min-height` i stedet for `height`.

**[Tilgjengelighetsreview]** — L5. Språk og symboler (§ EXPERIENCE Voice and Tone)
Fix: «✓» og «→» `aria-hidden`, vurder skjult tekst for «≥».

**[Tilgjengelighetsreview]** — L6. Dobbel annonsering ved godkjent resultat (§ EXPERIENCE Annonsering)
Fix: Velg fokusflytting, dropp live-regionen for rapporten.

**[Tilgjengelighetsreview]** — L7. Festet bunnlinje kan skjule fokus (2.4.11, utenfor målet) (§ DESIGN Layout & Spacing)
Fix: `scroll-padding-bottom`, og `scrollIntoView({block:'nearest'})` for valgt rad.

**[Tilgjengelighetsreview]** — L8. Tabelldetaljer (1.3.1) (§ EXPERIENCE tabeller)
Fix: `<caption>`, radhoder med `scope="row"`, FR-12 via `aria-describedby`, debounce søketelleren, `prefers-reduced-motion` for spinneren.

**[Mockup-rendering]** — Raden med kort historikk og WAPE «–» vises ikke i mocken (§ EXPERIENCE Produktliste, FR-19)
Havner rundt plass 21, utenfor mockens 12 rader.
Fix: Vis den i en søkefiltrert variant, eller beskriv radtilstanden og plasseringen i spinen.

**[Mockup-rendering]** — Spinen sier ikke om grafen viser hele historikken eller et vindu (§ DESIGN Prognosegraf, EXPERIENCE Graf)
Fix: For eksempel «hele historikken pluss 6 prognosemåneder».

**[Mockup-rendering]** — Spinen sier ikke hvor båndet og den stiplede linja starter (§ DESIGN Colors → Grafen, EXPERIENCE UJ-1 steg 5)
Mocken valgte: fra siste faktiske punkt, med markøren ved første prognosemåned.
Fix: Skriv valget inn i spinen.

**[Mockup-rendering]** — «Produktnavnet i topplinjen (16 px)», men topplinjen har ikke produktnavn (§ DESIGN Typography)
Mocken satte P-109 i grafens panelhode.
Fix: Skriv at den største teksten er valgt `produkt_id` i grafens panelhode, eller legg navnet i topplinjen i IA.

**[Mockup-rendering]** — Mocken måtte finne opp panelhoder, advarselstekst og ikon foran advarsler (§ EXPERIENCE Faste tekster, Valideringsrapport)
Bekrefter rubrikkfunnene i kategori 3 og 1. Ikonet er nytt.
Fix: Fastsett dem i spinen, med mockens valg som utgangspunkt.

## Reviewer files

- `review-rubric.md`
- `review-tilgjengelighet.md`
- Mockup-rendering: `.working/key-dashbord.html`, `.working/key-avvist.html` (funnene er overført direkte og har ingen egen reviewfil)
