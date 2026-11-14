---
name: PROGNOS
description: Nøkternt, Excel-nært dashbord for etterspørselsplanleggeren. shadcn/ui på Next.js 16 + Tailwind v4; denne fila spesifiserer bare deltaet fra shadcn-standardene.
status: final
created: 2026-11-14
updated: 2026-11-14
sources:
  - ../../prds/prd-G96-ellingsen-2026-11-14/prd.md
  - ../../prds/prd-G96-ellingsen-2026-11-14/addendum.md
colors:
  # Lys modus eneste modus i v1. Tokens som ikke står her arves fra shadcn
  # (popover, popover-foreground, card-foreground, secondary).
  background: '#FFFFFF'
  foreground: '#1F2328'
  surface-subtle: '#F6F7F8'
  muted-foreground: '#5B626B'
  border: '#D9DCE0'
  input: '#767C85'
  gridline: '#ECEEF0'
  primary: '#1F5FAD'
  primary-foreground: '#FFFFFF'
  primary-subtle: '#E8F0FA'
  ring: '#1F5FAD'
  destructive: '#B42318'
  destructive-subtle: '#FDECEA'
  chart-history: '#3D4450'
  chart-forecast: '#1F5FAD'
  chart-band: '#C9DAF0'
  chart-band-edge: '#4A74B5'
  chart-horizon: '#6B7480'
typography:
  # Kun systemfonter (NFR-1 offline: ingen next/font/google, ingen CDN).
  # Alle roller bruker samme stakk. Tall settes med tabular-nums (se Typography).
  title:
    fontFamily: 'system-ui, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif'
    fontSize: 16px
    fontWeight: '600'
    lineHeight: '1.4'
  panel-heading:
    fontFamily: 'system-ui, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif'
    fontSize: 14px
    fontWeight: '600'
    lineHeight: '1.4'
  body:
    fontFamily: 'system-ui, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif'
    fontSize: 14px
    fontWeight: '400'
    lineHeight: '1.5'
  table:
    fontFamily: 'system-ui, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif'
    fontSize: 13px
    fontWeight: '400'
    lineHeight: '1.4'
  label:
    fontFamily: 'system-ui, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif'
    fontSize: 12px
    fontWeight: '500'
    lineHeight: '1.4'
  caption:
    fontFamily: 'system-ui, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif'
    fontSize: 12px
    fontWeight: '400'
    lineHeight: '1.4'
rounded:
  # Skarpere enn shadcn: regneark, ikke app.
  sm: 2px
  md: 4px
  full: 9999px
spacing:
  # Tailwind 4-skala arves. Navngitte layoutmål:
  topbar-height: 56px
  sidebar-width: 300px
  sidebar-width-compact: 260px
  panel-padding: 16px
  panel-gap: 16px
  chart-height: 360px
  chart-height-compact: 300px
  report-max-height: 320px
  min-viewport: 1280px
components:
  topbar:
    background: '{colors.background}'
    border-bottom: '1px solid {colors.border}'
    min-height: '{spacing.topbar-height}'
  focus-ring:
    outline: '2px solid {colors.ring}'
    outline-offset: '2px'
    offset-color: '{colors.background}'
    opacity: '100 %'
  button-primary:
    background: '{colors.primary}'
    foreground: '{colors.primary-foreground}'
    radius: '{rounded.md}'
  button-link:
    background: 'transparent'
    foreground: '{colors.primary}'
    decoration: 'underline ved hover og fokus'
  input-field:
    background: '{colors.background}'
    border: '1px solid {colors.input}'
    radius: '{rounded.sm}'
  panel:
    background: '{colors.background}'
    border: '1px solid {colors.border}'
    radius: '{rounded.md}'
    padding: '{spacing.panel-padding}'
  panel-header:
    background: '{colors.surface-subtle}'
    typography: '{typography.panel-heading}'
  data-table:
    typography: '{typography.table}'
    header-background: '{colors.surface-subtle}'
    row-divider: '1px solid {colors.gridline}'
    numeric-align: right
  product-row-selected:
    background: '{colors.primary-subtle}'
    indicator: '3px solid {colors.primary}'
  flag-badge:
    background: '{colors.surface-subtle}'
    foreground: '{colors.foreground}'
    border: '1px solid {colors.border}'
    radius: '{rounded.sm}'
    typography: '{typography.label}'
  report-rejected:
    background: '{colors.destructive-subtle}'
    border-left: '4px solid {colors.destructive}'
  report-approved:
    background: '{colors.surface-subtle}'
    border-left: '4px solid {colors.border}'
  chart-tooltip:
    background: '{colors.background}'
    border: '1px solid {colors.border}'
    radius: '{rounded.md}'
    typography: '{typography.table}'
  wape-overview:
    background: '{colors.surface-subtle}'
    border-top: '1px solid {colors.border}'
    typography: '{typography.table}'
  loading-box:
    background: '{colors.background}'
    border: '1px solid {colors.border}'
    radius: '{rounded.md}'
    veil: 'rgba(255, 255, 255, 0.8)'
---

## Brand & Style

PROGNOS er et arbeidsverktøy for Kari, etterspørselsplanleggeren som i dag gjør jobben i Excel. Uttrykket skal kjennes igjen derfra. Det skal være nøkternt og tett, med rutenett og tall som står pent i kolonner. Det skal ikke se ut som et SaaS-produkt. Verktøyets troverdighet ligger i at tallene er etterprøvbare (NFR-5), og designet skal ikke pynte på dem. Ingen fargeflater roper «innsikt», og ingen store KPI-kort konkurrerer med tabellene.

PROGNOS arver shadcn/ui. Denne fila beskriver bare avvikene:
- én blå aksent
- skarpere radius
- et tettere typografinivå
- en fokusring og inndatakanter som holder WCAG 1.4.11
- komponentene som er spesifikke for produktet

Alt annet brukes som shadcn leverer det.

## Colors

Paletten har grå nyanser og én blå farge. Sjekk alltid om et nytt farge-token kan unngås.

- **Bakgrunn (`#FFFFFF`)** og **Overflate (`#F6F7F8`)**. Hvit er arbeidsflaten. Den lyse gråfargen brukes til panelhoder, tabellhoder, WAPE-oversikten og godkjent valideringsrapport.
- **Tekst (`#1F2328`)** og **Dempet tekst (`#5B626B`)**. Dempet tekst brukes til forklaringer som P10/P50/P90, merknader, akseetiketter og etiketten «Prognose →».
- **Kantlinje (`#D9DCE0`)** og **Rutenett (`#ECEEF0`)**. Dette er dekorative skillelinjer for paneler og tabellrader. De er for svake til å markere kontroller.
- **Inndatakant (`#767C85`)** brukes på kanten av søkefeltet, datasettvelgeren og eventuelle knapper som bare har kant. Den sørger for at kontrollene oppfyller WCAG 1.4.11. `{colors.border}` skal aldri brukes på en kontroll.
- **Blå aksent (`#1F5FAD`)** er den eneste kromatiske fargen. Den betyr **valgt, prognose eller handling**:
  - valgt produktrad, med `{colors.primary-subtle}` som bakgrunn og en blå stripe
  - prognoselinjen i grafen
  - primærknappen **Last opp CSV** og lenkeknappene (`button-link`)
  - fokusringen

  Blått brukes aldri på overskrifter, ikoner eller som pynt.
- **Rød (`#B42318`)** betyr at noe stopper Kari. Den brukes bare i den røde varianten av valideringsrapporten, ved **avvist fil, feilet kjøring eller utilgjengelig tjeneste**. Rødt brukes ikke på flagg (heller ikke *ETS taper*) eller på svake WAPE-tall. De er informasjon, ikke feil.
- **Grafen:**
  - historikken er en heltrukket linje i `{colors.chart-history}`
  - prognosen (Forventet, P50) er en stiplet linje i `{colors.chart-forecast}`
  - intervallbåndet (P10–P90) har fyll i `{colors.chart-band}`
  - P10- og P90-kantene er 1 px heltrukne linjer i `{colors.chart-band-edge}`, så båndet kan leses uten å stole på fyllet
  - horisontmarkøren er en loddrett linje i `{colors.chart-horizon}`

  Historikk og prognose skilles også på linjestilen, ikke bare på fargen.

**Kontrast** er regnet etter WCAG 2.x. Kravet er 4,5:1 for tekst og 3:1 for kontroller og grafiske objekter.

| Kombinasjon | Bruk | Kontrast |
|---|---|---|
| `foreground` / `background` · `surface-subtle` · `primary-subtle` · `destructive-subtle` | brødtekst, hoder, valgt rad, rød rapport | 15,8 · 14,7 · 13,8 · 13,8 |
| `muted-foreground` / `background` · `surface-subtle` · `primary-subtle` | forklaringer, P10/P50/P90-undertekst | 6,17 · 5,75 · 5,37 |
| `primary-foreground` / `primary` | primærknapp | 6,37 |
| `primary` / `background` · `surface-subtle` | lenkeknapper, fokusring | 6,37 · 5,94 |
| `destructive` / `destructive-subtle` | overskrift og stripe i rød rapport | 5,75 |
| `input` / `background` · `surface-subtle` | kant på inndatafelt | 4,21 · 3,92 |
| `chart-band-edge` / `background` | P10- og P90-kant | 4,71 |
| `chart-forecast` / `chart-band` | P50-linjen i båndet | 4,48 |
| `chart-horizon` / `background` · `chart-band` | horisontmarkør | 4,74 · 3,33 |
| `chart-history` / `background` | historikklinje | 9,81 |

Det skal ikke stå tekst oppå båndet, fordi dempet tekst bare får 4,34:1 der.

Dette skal ikke brukes: trafikklysfarger (grønn/gul/rød) på WAPE eller flagg, gradienter, mer enn én aksentfarge eller mørk modus (utenfor v1).

## Typography

Siden bruker bare systemfonter (`system-ui`, Segoe UI på Windows). Det følger av offlinekravet NFR-1 og passer den nøkterne tonen.

- **Grunnstørrelsen er 14 px** (`{typography.body}`). Tabellene bruker 13 px (`{typography.table}`) fordi tettheten er viktig når Kari går gjennom 200 produkter.
- **Alle tall settes med `font-variant-numeric: tabular-nums`** og står høyrejustert, slik at sifrene står under hverandre som i Excel. Dette gjelder tabeller, produktlisten, WAPE-oversikten og tooltipen. Tallformatet er spesifisert i EXPERIENCE.md, under *Tall- og datoformat*.
- **Tre vekter:**
  - 400 for brødtekst og tabeller
  - 500 for etiketter og flagg (`{typography.label}`)
  - 600 for overskrifter, sumrader og ordmerket

  Det finnes ingen display-størrelse. Den største teksten er ordmerket «PROGNOS» i topplinjen (`{typography.title}`, 16 px). Valgt `produkt_id` står i grafens panelhode med `{typography.panel-heading}`.
- Etiketter skrives ikke i versaler, og det brukes ikke sperring.

## Layout & Spacing

Spacing følger Tailwind-skalaen, med 4 px som grunnenhet. Siden er laget for skjermer fra 1280 px bredde (`{spacing.min-viewport}`) og 720 px høyde. Hele dashbordet ligger på én side (PRD §4.5), og **hele siden scroller**:

```
┌──────────────────────────────────────────────────────────────┐
│ Topplinje: PROGNOS · [Datasettvelger ▾]        [Last opp CSV] │  ≥ 56 px
├──────────────────────────────────────────────────────────────┤
│ Valideringsrapport (full bredde, sammenfoldet til én linje)  │
├──────────────┬───────────────────────────────────────────────┤
│ Produktliste │ Graf (360 px / 300 px)                        │
│ [Søk]        │ [Vis historikk som tabell]                    │
│ 300 px       ├───────────────────────┬───────────────────────┤
│ sticky,      │ Scenariotabell        │ Backtest-tabell       │
│ scroller     ├───────────────────────┴───────────────────────┤
│ selv         │ Detaljer per opprinnelse (når utvidet)        │
├──────────────┴───────────────────────────────────────────────┤
│ WAPE-oversikt (én linje, festet nederst)                     │
└──────────────────────────────────────────────────────────────┘
```

- **Produktlisten** har fast bredde (`{spacing.sidebar-width}`) og er `position: sticky` under topplinjen. Høyden er `100vh − topplinje − WAPE-oversikt`, og listen scroller for seg selv. Resten av siden scroller vanlig.
- **Hovedområdet** er fleksibelt. Scenariotabellen og backtest-tabellen deler bredden 50/50. Detaljene per opprinnelse åpner seg i full bredde under begge tabellene.
- **Grafen** har høyden `{spacing.chart-height}`. Når vinduet er lavere enn 800 px, får den `{spacing.chart-height-compact}`. Høydebudsjettet ved 720 px er omtrent 56 (topplinje) + 60 (rapport) + 350 (graf med hode, forklaring og knapp) + 290 (scenariotabell) + 36 (WAPE) ≈ 790 px, altså omtrent 70 px mer enn vinduet. Sumraden i scenariotabellen havner derfor like under nedre skjermkant, og en kort scroll er nok til å se den. På 1080 px høyde er hele dashbordet synlig uten scrolling.
- **Valideringsrapporten** er sammenfoldet til oppsummeringslinjen som standard (se EXPERIENCE.md). Feillisten i avvist rapport er høyst `{spacing.report-max-height}` og scroller for seg selv.
- Panelene har 16 px innvendig luft og 16 px mellomrom (`{spacing.panel-padding}`, `{spacing.panel-gap}`).
- **WAPE-oversikten** ligger festet nederst når bredden er 1024 px eller mer. Siden har da `scroll-padding-bottom` lik linjens høyde, slik at linjen aldri dekker elementet som har fokus.
- **Faste høyder** brukes ikke på elementer med tekst. Topplinje, rader, flagg og WAPE-linje bruker `min-height`, slik at økt tekstavstand (WCAG 1.4.12) ikke klipper tekst.
→ Visuell referanse: [mockups/key-dashbord.html](mockups/key-dashbord.html) (layout, tokens og komponenter i godkjent tilstand) og [mockups/key-avvist.html](mockups/key-avvist.html) (rød rapport og lasteboks). Ved konflikt gjelder denne fila foran mockupene.

- Under 1024 CSS-px legger panelene seg i én kolonne. Reglene for dette står i EXPERIENCE.md, *Responsive & Platform*.

## Elevation & Depth

Dashbordet bruker ingen skygger. Panelene avgrenses med en 1 px `{colors.border}`, og lagdeling vises med tone, der `{colors.surface-subtle}` ligger mot hvitt.

Det eneste laget over siden er lasteboksen (`loading-box`): et hvitt slør på 80 % og en sentrert boks med 1 px kant. Verken den eller tooltipen i grafen (`chart-tooltip`) har skygge.

## Shapes

Radiusen er skarpere enn i shadcn:

- `{rounded.sm}` (2 px) på flagg og inndatafelt
- `{rounded.md}` (4 px) på knapper, paneler, nedtrekkslisten, tooltipen og lasteboksen

Full avrunding (`{rounded.full}`) brukes bare på spinneren. Formene skal minne om et regneark, ikke om en app.

## Components

**shadcn-komponenter som brukes uendret** (bortsett fra de globale overstyringene under):

| Komponent | Brukes til |
|---|---|
| `Button` (variantene ghost og link) | «Lukk», «Tøm søk», «Vis advarsler», «Vis detaljer per opprinnelse», «Vis historikk som tabell» |
| `Select` | datasettvelgeren |
| `Input` | søkefeltet |
| `Table` | alle tabeller |
| `Collapsible` | advarslene i rapporten, detaljer per opprinnelse og historikktabellen |
| `Skeleton` | lastetilstander i liste, graf, tabeller og rapport |
| `Separator` | skillelinjer |

**Globale overstyringer:**

- **Fokusring** (`focus-ring`). Den er en 2 px heltrukken linje i `{colors.ring}` med full opasitet og 2 px offset i `{colors.background}`. shadcns `ring-ring/50` overstyres globalt fordi den bare gir 2,27:1 i kontrast. Med offset blir ringen også synlig rundt den blå primærknappen.
- **Inndatafelt** (`input-field`). `Input` og `Select`-triggeren bruker `{colors.input}` som kant, ikke shadcns standardkant.

**Komponenter som er spesifikke for produktet:**

- **Topplinje** (`topbar`). Til venstre står ordmerket «PROGNOS» i `{typography.title}` og datasettvelgeren med etiketten «Datasett». Til høyre står `button-primary` med **Last opp CSV**. Under knappen står kolonnekravet i `{typography.caption}` og `{colors.muted-foreground}`: «CSV med kolonnene produkt_id, maaned, antall».
- **Valideringsrapport.** Den har to varianter:
  - `report-approved`: grå flate med en grå kantstripe
  - `report-rejected`: lys rød flate med en rød kantstripe

  Godkjent rapport har en oppsummeringslinje med ✓ i tekstfarge, ikke grønt. Under står fordelingen per historikknivå og lenkeknappen for advarsler (atferd i EXPERIENCE.md). Feillisten i avvist rapport står i `{typography.table}`, med radnumre i tabular-nums. Ingen av variantene har ikon utover ✓, og teksten bærer meningen.
- **Produktliste (rad).** Linje 1 har `produkt_id` til venstre og WAPE høyrejustert. Linje 2 har flaggene, hvis produktet har noen. Valgt rad bruker `product-row-selected`. Hover gir `{colors.surface-subtle}`.
- **Flagg-merke** (`flag-badge`). Hvert flagg har et ikon og en tekst, og teksten står alltid med. Ikonene er fra Lucide, som følger med shadcn og ligger lokalt.
  - *kort historikk* bruker et klokkeikon
  - *ETS taper* bruker et pil-ned-ikon
- **Graf (Recharts).**
  - Felles månedsakse som viser **hele historikken** og de 6 prognosemånedene.
  - Y-aksen starter på 0, og rutenettlinjene er horisontale i `{colors.gridline}`.
  - Historikken er heltrukket, med strek 2 px.
  - Den stiplede P50-linjen (strek 2 px, stiplet med 6 px strek og 4 px mellomrom) og båndet starter i siste faktiske punkt, så kurven henger sammen.
  - Båndet har fyll og kantlinjer som beskrevet under *Colors*.
  - Horisontmarkøren er en heltrukken linje på 1 px ved første prognosemåned, med etiketten «Prognose →» i `{colors.muted-foreground}`.
  - Grafen har ingen animasjon.
  - Panelhodet viser «Prognose – {produkt_id}», med modell og horisont i `{typography.caption}` (se EXPERIENCE.md, *Faste tekster*).
- **Tooltip i grafen** (`chart-tooltip`). Recharts-tooltip med hvit flate, 1 px kant og `{typography.table}`. Den plasseres slik at den ikke dekker punktet den beskriver.
- **Forklaring i grafen** (legend). Den står under grafen i `{typography.caption}`. Hver oppføring har et lite linjeutsnitt med samme stil som serien: heltrukket, stiplet, eller bånd med kant.
- **Historikktabell.** Den ligger sammenfoldet under grafen og bruker `data-table` med kolonnene Måned og Faktisk.
- **Scenariotabell.** Kolonnene er *Måned · Pessimistisk · Forventet · Optimistisk*. Under hvert scenarionavn står P10, P50 og P90 i `{typography.caption}` og `{colors.muted-foreground}`. Tabellen har 6 månedsrader og en sumrad i vekt 600 med en kantlinje over. Merknaden fra FR-12 står under tabellen i `{typography.caption}`.
- **Backtest-tabell.** Kolonnene er *Sesongnaiv baseline* først og *ETS* etter (rekkefølgen følger prinsippet *baseline først*, og kolonnenavnet *ETS* følger PRD-ens «ETS-kolonnen»). Radene er WAPE og Intervalldekning. Under tabellen står dommerlinjen som tekst, uten farge. Lenkeknappen «Vis detaljer per opprinnelse (6)» åpner detaljtabellen i full bredde.
- **WAPE-oversikt** (`wape-overview`). Én linje i `{typography.table}`, festet nederst, med grå flate og en kantlinje over.
- **Lasteboks** (`loading-box`). Den har spinner og tekst. Med `prefers-reduced-motion` står spinneren stille (se EXPERIENCE.md, *Accessibility Floor*).
- **Hopplenke.** Den er skjult til den får fokus, og vises da øverst til venstre som `button-primary`.

## Do's and Don'ts

| Gjør | Ikke gjør |
|---|---|
| Høyrejuster alle tall, med `tabular-nums` | Sentrer tall eller bland proporsjonale sifre |
| Bruk blått bare for valgt, prognose og handling | Bruk blått på overskrifter, ikoner eller pynt |
| Vis flagg med ikon og tekst | Vis flagg bare som farget prikk eller farget rad |
| Bruk `{colors.input}` på kanten av kontroller | Bruk `{colors.border}` på inndatafelt |
| Bruk fokusring på 2 px med offset og full opasitet | Behold shadcns `ring-ring/50` |
| Avgrens med 1 px linjer og tone | Bruk skygger, gradienter eller kort som «svever» |
| Bruk rødt bare ved avvist fil, feilet kjøring eller utilgjengelig tjeneste | Farg svake WAPE-tall eller *ETS taper* røde |
| Bruk systemfont, lokalt | Hent fonter fra Google Fonts eller en CDN |
| Bruk `min-height` på elementer med tekst | Bruk fast `height` som klipper tekst ved økt tekstavstand |
| Bruk en tett, Excel-aktig tabellrytme | Bruk store KPI-kort med kjempetall |
