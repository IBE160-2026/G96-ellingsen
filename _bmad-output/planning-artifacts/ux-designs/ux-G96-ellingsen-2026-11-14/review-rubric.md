# Spine Pair Review — G96-ellingsen

Gjennomgått: `DESIGN.md` og `EXPERIENCE.md` (begge `status: draft`, 2026-11-14) mot kildene `prd.md` og `addendum.md` (prd-G96-ellingsen-2026-11-14). Referanser: eksemplene i `bmad-ux/assets` og `design-md-spec.md`. Disse valgene er tatt bevisst av brukeren og regnes ikke som funn: kun lys modus, desktop fra 1280 px, WCAG 2.1 AA, nøytral grå med én blå aksent, og søk i produktlisten som tillegg (ført som åpent PRD-punkt).

## Overall verdict

**Adequate. Kontrakten er brukbar etter at tre høye funn er rettet.** Paret er stramt og godt forankret i kildene. Alle fire brukerreisene finnes med navnene ordrett fra PRD-en. Hver har protagonist, nummererte steg og klimaks. Alle `{token}`-referansene resolver, alle farger har hex, og seksjonsrekkefølgen følger spesifikasjonen. De ordrette tekstene for FR-20 og FR-21 er riktige.

Tre punkter vil likevel tvinge en nedstrøms konsument (arkitektur eller story-dev) til å gjette eller bryte et krav:

1. Dommerlinjen i backtest-tabellen er binær («slår»/«taper»). Det motsier PRD-ordlista, der like WAPE-verdier verken er seier eller tap, og det finnes ingen tekst for udefinert WAPE.
2. Kantene på inndatafeltene (søkefeltet og datasettvelgeren) arver en kant med kontrast 1,38:1 og bryter WCAG 1.4.11, som er det valgte målet.
3. Det finnes ingen modell for vertikal scrolling eller noe høydebudsjett. Topplinjen, rapporten med opptil 5 advarsler eller 320 px feilliste, grafen på 360 px, tabellene og den festede WAPE-linja får ikke plass på 720 CSS-px. Det er vanlig høyde på en laptop med 150 % skalering.

Resten er middels og lave presiseringer: manglende feilmeldingsmaler, interne motsetninger i DESIGN.md (farge- og vektregler), komponentnavn som ikke er like i de to filene, og noen tilstander som mangler.

## 1. Flow coverage — adequate

Uttrekk fra kildene: UJ-1 til UJ-4 i PRD §2.3. Alle fire finnes i EXPERIENCE.md *Key Flows* med samme navn. Kari er protagonist, med kontekst i UJ-1. Alle har nummererte steg og en uthevet **Klimaks**. UJ-1 har kanttilfellet fra PRD-en, og UJ-2 er i seg selv feilstien for opplasting.

Gjennomgang av FR-ene som gjelder UI:

| Krav | Dekning |
|---|---|
| FR-1 | Dekket (filvelger, `.csv`, `aria-describedby` med kolonnene) |
| FR-2, FR-3 | Delvis, se funn |
| FR-4 | Delvis, se funn |
| FR-5, FR-6, FR-7 | Dekket |
| FR-10, FR-11, FR-12 | Dekket |
| FR-16 | Dekket indirekte (WAPE «–» og backtest-tekster) |
| FR-17 til FR-22 | Dekket |
| FR-25 | Dekket |
| FR-8, FR-9, FR-13 til FR-15, FR-23, FR-24 | Ingen egen UI, og det er riktig |

### Findings

- **[medium]** Feilmeldingene for avvist fil har bare to eksempler: duplikat og antall som ikke er heltall (EXPERIENCE *Voice and Tone* og *Key Flows* UJ-2). FR-3 og FR-2 gir minst fem andre feiltyper uten mal: manglende kolonne (skal nevne kolonnen ved navn), `maaned` i feil format, tom celle, fil uten datarader og skilletegn som ikke gjenkjennes. Story-dev må finne på ordlyden, og NFR-4 og Playwright-testene får ingenting å sjekke mot. *Fix:* Legg en tabell «Feilmeldinger (FR-2, FR-3)» under *Faste tekster*. Gi én mal per regel, for eksempel «Mangler påkrevd kolonne: `antall`», «Rad {r}: maaned må ha formatet ÅÅÅÅ-MM», «Rad {r}: tom celle i `{kolonne}`», «Fila har ingen datarader» og «Fant ikke kolonnene produkt_id, maaned og antall med komma eller semikolon som skilletegn».
- **[medium]** Advarselsteksten for utfylte måneder (FR-4) mangler mal. Det står bare «én per produkt med månedene listet» (EXPERIENCE *Component Patterns*, rad Valideringsrapport). *Fix:* Fastsett formen, for eksempel «P-031: 2 måneder fylt inn med 0 (2025-03, 2025-07)».
- **[low]** UJ-1 steg 4 avviker fra PRD-en. I PRD-en velger Kari det første produktet selv, mens EXPERIENCE velger det automatisk. Avviket er bevisst (`.memlog.md`, override), men EXPERIENCE merker det ikke som avvik fra kilden. *Fix:* Legg inn én setning i UJ-1, eller under *Åpne punkter*, om at autovalg erstatter PRD-steget. Da kan PRD-eieren oppdatere UJ-1.
- **[low]** UJ-1 og UJ-4 har ingen «Failure»-linje i flyten. Tilstandene *Kjøring feilet* og *Ingen kontakt med backend* finnes i *State Patterns*, men flytene viser ikke til dem. *Fix:* Legg inn én linje per flyt. For UJ-1: «Feil: kjøringen feiler → rød rapport, forrige datasett står (se *Kjøring feilet*).» For UJ-4: «Feil: datasettet kan ikke hentes → …».

## 2. Token completeness — adequate

Alle tokens i frontmatteren er definert. Alle 16 fargene har hex. Alle `{path}`-referansene i prosa og i `components` resolver i begge filene: `colors.*`, `typography.body/table/title/label/caption/panel-heading`, `spacing.min-viewport/sidebar-width/panel-padding/panel-gap/topbar-height`, `rounded.sm/md/full`, og `{colors.ring}` i EXPERIENCE. Ingen referanse peker på noe som ikke finnes.

Kontrast er regnet etter WCAG-luminans:

| Kombinasjon | Oppgitt | Regnet | Vurdering |
|---|---|---|---|
| muted-foreground / background | ≥ 6:1 | 6,17 | ✓ |
| primary / background | 6,4:1 | 6,37 | ✓ |
| chart-horizon / background | 3,2:1 | 3,18 | ✓ (grafisk objekt) |
| foreground / background, surface-subtle, primary-subtle | — | 15,80 / 14,73 / 13,75 | ✓ |
| primary-foreground / primary (knapp) | — | 6,37 | ✓ |
| muted-foreground / surface-subtle (undertekst i tabellhodet) | — | 5,75 | ✓ AA, men påstanden «minst 6:1» gjelder bare mot hvitt |
| primary / primary-subtle | — | 5,54 | ✓ |
| destructive / destructive-subtle | — | 5,75 | ✓ |
| chart-forecast / chart-band (P50-linja i båndet) | — | 4,48 | ✓ |
| chart-horizon / chart-band | — | 2,24 | ✗ der markøren krysser båndet |
| chart-band / background | — | 1,42 | ✗ grafisk objekt |
| border (og arvet `input`) / background | — | 1,38 | ✗ komponentgrense |

### Findings

- **[high]** Kantene på inndatafelt og Select bryter WCAG 1.4.11 (DESIGN frontmatter `colors`, kommentaren på linje 11–12, og *Components*: «`Input` (søkefeltet)», «`Select` (datasettvelgeren)»). `input` arves fra shadcn og er ikke overstyrt. shadcn-standarden og `border` (`#D9DCE0`) gir begge omtrent 1,3–1,4:1 mot hvitt. 1.4.11 krever 3:1 for den visuelle grensen som identifiserer en kontroll. Med WCAG 2.1 AA som uttalt mål får story-dev et brudd innebygd. *Fix:* Legg inn `input: '#8A919A'` (3,18:1) eller mørkere i frontmatteren, og la `border` beholde sin rolle for paneler. Si i *Components* at Input og Select bruker `{colors.input}`.
- **[medium]** P10–P90-båndet (`chart-band` `#C9DAF0`) har 1,42:1 mot hvitt (DESIGN *Colors*, «Grafen»). Båndet er informasjonsbærende (FR-20) og faller derfor inn under 1.4.11. *Fix:* Legg en tynn kantlinje på P10 og P90 i en farge med minst 3:1, for eksempel et nytt token `chart-band-edge`. Alternativt kan det skrives eksplisitt at scenariotabellen er tekstalternativet og at båndet regnes som supplerende. Det er svakere.
- **[medium]** Kontrasttallene for viktige kombinasjoner er ikke samlet (DESIGN *Colors*, bare tre tall i prosa). EXPERIENCE *Accessibility Floor* sier likevel «Kontrastverdiene står i DESIGN.md». Knapp, rød rapport, valgt rad, undertekst på grå flate og horisontmarkør mot båndet mangler. *Fix:* Legg en kontrasttabell i DESIGN *Colors* med tallene over, og presiser at 6:1 gjelder mot `background`.
- **[medium]** Fokusringen er ikke spesifisert godt nok (DESIGN frontmatter `ring: '#1F5FAD'`, EXPERIENCE *Accessibility Floor*). Ringen har samme farge som flaten på `button-primary` (1:1), og bredde og offset er ikke oppgitt. shadcn for Tailwind v4 bruker `ring-ring/50` uten offset, som gir en svak ring rundt den blå knappen. *Fix:* Fastsett 2 px ring med 2 px offset i `{colors.background}` og ingen opasitet, gjerne som komponent-token `focus-ring`.
- **[low]** `typography.table.fontVariantNumeric` er ikke en nøkkel i spesifikasjonen. `design-md-spec.md` tillater `fontFamily`, `fontSize`, `fontWeight`, `lineHeight` og `letterSpacing`. *Fix:* Flytt `tabular-nums` til et `note`-felt eller til prosaen, der det allerede står.
- **[low]** Flere layoutverdier står bare som tall i prosa og ikke som tokens: 260 px for produktlisten (EXPERIENCE *Responsive & Platform*), 320 px for feillisten (*State Patterns*), 50 vh, 80 % slør, strek 6/4, stripe på 3 px og 4 px. *Fix:* Gjør i det minste `sidebar-width-compact: 260px` og `report-max-height: 320px` til `spacing`-tokens.

## 3. Component coverage — adequate

| Komponent | DESIGN.Components | EXPERIENCE.Component Patterns |
|---|---|---|
| Topplinje | ✓ (`topbar`) | – (bare IA) |
| Last opp CSV / button-primary | ✓ | ✓ |
| Datasettvelger | arvet `Select` | ✓ |
| Valideringsrapport | ✓ (`report-approved/rejected`) | ✓ |
| Søk i produktlisten | arvet `Input` | ✓ |
| Produktliste / Produktrad | ✓ (heter «Produktrad») | ✓ (heter «Produktliste») |
| Flagg-merke | ✓ (`flag-badge`) | – |
| Graf / Prognosegraf | ✓ (heter «Prognosegraf») | ✓ (heter «Graf») |
| Scenariotabell | ✓ | ✓ |
| Backtest-tabell | ✓ | ✓ |
| WAPE-oversikt | ✓ | ✓ |
| Lasteboks | ✓ (prosa) | – (bare *State Patterns*) |
| Skeleton, hopplenke, «Lukk», «Tøm søk», «Vis alle advarsler» | – | nevnt i tilstander og tilgjengelighet |

### Findings

- **[medium]** Komponentnavnene er ikke like i de to filene (se tabellen). DESIGN bruker «Prognosegraf», mens EXPERIENCE og PRD bruker «Graf». DESIGN har «Produktrad», mens EXPERIENCE har «Produktliste». Topplinje, Flagg-merke og Lasteboks mangler rad i EXPERIENCE *Component Patterns*. *Fix:* Bruk PRD-navnet «Graf» i DESIGN, og eventuelt «Produktliste (rad)». Legg inn rader i EXPERIENCE for Flagg-merke (ikke interaktivt, ingen tooltip eller med tooltip?), Lasteboks (henvisning til *Kjøring pågår*) og Topplinje.
- **[medium]** Kolonnene i utvidelsen per opprinnelse er ikke definert (EXPERIENCE *Component Patterns*, Backtest-tabell: «faktisk verdi og P50 per opprinnelse»). DESIGN.md har ingen spesifikasjon. FR-21 og NFR-5 krever at WAPE kan regnes etter, og UJ-3 steg 3 forutsetter at baseline og ETS kan sammenlignes per måned. *Fix:* Fastsett kolonnene, for eksempel *Opprinnelse · Måned · Faktisk · P50 baseline · P50 ETS*, og eventuelt |feil| og en sumrad som gir WAPE. Si hva som vises når det bare finnes baseline-backtest.
- **[medium]** Teksten i panelhodene er ikke fastsatt (DESIGN `panel-header`, EXPERIENCE IA). Ingenting sier hvilken overskrift graf, scenariotabell og backtest-tabell har, eller hvor valgt `produkt_id` vises. NFR-4 sier at «Playwright-testen sjekker overskriftene». *Fix:* Legg overskriftene under *Faste tekster*, for eksempel «Prognose – {produkt_id}», «Scenarioer», «Backtest (siste 6 måneder)» og «Produkter».
- **[medium]** Grafen har to roller som er i konflikt med hverandre (EXPERIENCE *Interaction Primitives* og *Accessibility Floor*). Den har `role="img"`, men skal også være fokuserbar og bruke pil venstre og høyre mellom månedene. `img` er ikke interaktiv, og barna regnes som presentasjonelle, så skjermleseren leser ikke tooltip-innholdet. *Fix:* Velg én modell. Enten er grafen `role="img"` og ikke fokuserbar, og scenariotabellen er tekstalternativet. Eller den er `role="group"` med `aria-roledescription="graf"` og en `aria-live`-region for måneden som har fokus.
- **[low]** Komponenter som brukes, er ikke listet i DESIGN *Components*: Skeleton (*State Patterns*), spinner, hopplenke (som må vises ved fokus), «Lukk», «Tøm søk» og «Vis alle advarsler». `Alert` er listet, men brukes ingen steder. *Fix:* Utvid listen over shadcn-komponenter som brukes uendret, eller si hvilken variant de har. Fjern `Alert`, eller si at rapporten bygger på den.
- **[low]** Tooltip og forklaring (legend) i grafen er Recharts-komponenter, ikke shadcn `Tooltip`. Ingen av dem har visuell spesifikasjon. *Fix:* Gi én linje hver i DESIGN *Components*: flate, kant og typografi.

## 4. State coverage — thin

Gjennomgangen gikk del for del i IA-en. Dekket: første oppstart, kjøring pågår, godkjent, avvist med over 15 feil, kjøring feilet, ingen kontakt med backend, produktdetalj lastes, historikknivå *ingen*, *sesongnaiv* uten ETS-backtest, *ETS taper*, søk uten treff, og valgt produkt utenfor filteret.

### Findings

- **[high]** Dommerlinjen i backtest-tabellen har bare to verdier (EXPERIENCE *Component Patterns*, Backtest-tabell: «ETS slår baseline» eller «ETS taper mot baseline» der «strengt lavere WAPE gir slår»). Da blir like WAPE-verdier til «taper». Det motsier PRD §3 *ETS slår baseline* og §11.2, der like verdier verken er seier eller tap og ikke gir flagget. Det finnes heller ingen tekst for udefinert WAPE (Σ faktisk = 0, FR-14), der WAPE vises som «–». En konsument vil implementere `etsWape < baseWape ? slår : taper`, og det er feil. *Fix:* Gjør dommerlinjen til tre tilfeller pluss ett: «ETS slår baseline», «ETS taper mot baseline», «ETS og baseline har lik WAPE», og «Kan ikke sammenlignes (WAPE er udefinert når faktisk salg er 0)». Legg inn tilsvarende rader i *State Patterns*.
- **[high]** Det finnes ingen modell for vertikal scrolling og intet høydebudsjett (DESIGN *Layout & Spacing*, EXPERIENCE *Responsive & Platform*). Topplinjen (56 px), godkjent rapport (oppsummering, fordeling og opptil 5 advarsler pluss lenke, rundt 200 px), grafen (360 px), tabellene (overskrift, 6 rader, sum, merknad og dommerlinje, rundt 300 px) og WAPE-linja er til sammen nesten 950 px. På en laptop med 1920×1080 og 150 % skalering er visningen 1280×720 CSS-px. Det står ikke om siden scroller som helhet eller om bare produktlisten scroller, eller hva «fyller høyden mellom rapporten og WAPE-oversikten» betyr når rapporten er 320 px. Klimakset i UJ-1 (sumraden) kan havne under bretten. *Fix:* Fastsett en minimumshøyde, for eksempel 720 px. Velg modell: siden scroller, og listen er `sticky` med høyde `100vh − topplinje − WAPE`. Vurder å la godkjent rapport være sammenfoldbar til oppsummeringslinja (shadcn `Collapsible` er allerede i bruk).
- **[medium]** Det mangler en tilstand for lasting ved bytte av datasett (EXPERIENCE *Component Patterns*, Datasettvelger, og UJ-4 steg 3: «ingen lasteboks»). Rapporten, listen og WAPE-oversikten må hentes på nytt. Det står ikke hva som vises i mellomtiden, eller om forrige datasett blir stående. *Fix:* Legg inn raden «Datasett byttes»: Skeleton i rapport, liste og WAPE-linje, ingen slør, og Select er aktiv.
- **[medium]** «{n} produkter» i lasteboksen krever et arkitekturvalg som ikke er tatt (EXPERIENCE *State Patterns*, *Kjøring pågår*: «Før `n` er kjent …»). FR-7 sier én forespørsel, så frontend får ikke vite n fra backend før svaret kommer. UJ-1 steg 2 viser «200 produkter» med en gang. *Fix:* Bestem at frontend teller unike `produkt_id` ved å lese CSV-en på klientsiden før opplasting. Ellers kan dere bare bruke den generelle teksten. Si det eksplisitt, siden det påvirker arkitekturen.
- **[medium]** Det står ikke hva som skjer etter «Lukk» på en avvist rapport (EXPERIENCE *State Patterns*, *Fil avvist*). Rapporten er «alltid synlig for valgt datasett» (FR-18), så det er uklart om den godkjente rapporten for gjeldende datasett kommer tilbake. Det står heller ikke hvor fokus havner, og avvisningen flytter ikke fokus. *Fix:* «Lukk» bør vise rapporten for valgt datasett igjen og flytte fokus til rapportoverskriften. Sett fokus på avvisningsoverskriften også ved avvisning.
- **[low]** WAPE-oversikten mangler tilstand for m = 0, altså når ingen produkter har backtest for begge modellene, og total WAPE derfor er udefinert. *Fix:* Gi en tekst, for eksempel «Total WAPE: ingen produkter har backtest for begge modellene».
- **[low]** Det finnes ingen tilstand for når henting av ett produkt feiler. *Ingen kontakt med backend* ligger bare i rapporten. *Fix:* Vis en dempet feillinje i grafområdet med «Prøv igjen».
- **[low]** Det står ikke hva som skjer hvis kjøringen henger forbi NFR-7-grensen eller får tidsavbrudd i nettverket. Det finnes ingen avbrytknapp, så siden kan bli låst for alltid. *Fix:* Sett en klientgrense, for eksempel 120 s, og gå deretter til *Kjøring feilet*.
- **[low]** Backtest-utvidelsen er ikke beskrevet for produkter med bare baseline-backtest eller uten backtest. Det står ikke om knappen vises, eller om «(6)» stemmer. *Fix:* Skjul knappen ved *Ingen backtest*, og vis bare baseline-kolonnen ved baseline-backtest.
- **[low]** Det står ikke hva som skjer når filvelgeren avbrytes, eller når Kari velger en fil som ikke er CSV via «Alle filer». *Fix:* Ved avbrudd skjer ingenting. En fil som ikke er CSV, gir vanlig avvisning med feilmeldingen for skilletegn eller kolonner.
- **[low]** Piltastene velger produkt med en gang, og «Forrige produkt blir ikke stående», så hvert tastetrykk gir et blink av Skeleton. *Fix:* Hent nabo-produktene på forhånd (TanStack Query `prefetchQuery`), eller vis Skeleton først etter rundt 150 ms.

## 5. Visual reference coverage — venter på mockups

`mockups/` finnes ikke ennå, og det er avtalt. Ifølge `.memlog.md` er det planlagt mockups av dashbordet i godkjent tilstand med P-109 valgt og av avvist rapport (UJ-2). Det dekker UJ-1, UJ-2 og UJ-3 visuelt.

### Findings

- **[low]** EXPERIENCE *Information Architecture* mangler linja «→ Composition reference: mockups/… Spine wins on conflict.», som begge eksemplene har. *Fix:* Legg den inn når mockupene er klare. Vurder også en mockup av lasteboksen og av historikknivå *ingen*, siden de tilstandene har mest egen layout.

## 6. Bloat & overspecification — strong

Paret er stramt. Den egne seksjonen *Tall- og datoformat* fortjener plassen sin (NFR-5). Det er lite gjentakelse av PRD-en, og innledningen sier eksplisitt at kravene ikke gjentas.

### Findings

- **[low]** Tilstanden *Ingen produkt valgt* kan ikke oppstå (EXPERIENCE *State Patterns*: «bare mulig hvis datasettet har 0 produkter»). PRD §3 sier at et datasett har ett eller flere produkter, og FR-3 avviser en fil uten datarader. *Fix:* Fjern raden, eller gjør den om til forbigående tilstand før autovalget har skjedd.
- **[low]** Reglene for grafen står både i DESIGN *Colors* og i DESIGN *Components*. Reflow-regelen står i både DESIGN *Layout & Spacing* og EXPERIENCE *Responsive & Platform*, og 1024–1279-trinnet finnes bare i EXPERIENCE. Dette er en driftrisiko. *Fix:* Behold detaljene ett sted, og la det andre stedet bare henvise.

## 7. Inheritance discipline — adequate

Kildene resolver: `../../prds/prd-G96-ellingsen-2026-11-14/prd.md` og `addendum.md`, og lenken i innledningen til EXPERIENCE. Brukerreisenavnene er ordrette. Tekstene for FR-20 og begge FR-21 er ordrette. Scenarionavn, flaggnavn, *Sesongnaiv baseline*, *opprinnelse* og *Intervalldekning* følger ordlista. WAPE-oversikten følger *baseline først*. Søket er riktig merket som tillegg og åpent PRD-punkt. Addendum H6 er riktig ført som åpent punkt.

### Findings

- **[medium]** Rødfargen brukes også i en tilstand DESIGN.md ikke tillater. EXPERIENCE *State Patterns*, *Ingen kontakt med backend*, bruker «Rød variant». DESIGN *Colors* og *Do's and Don'ts* sier at rødt er «forbeholdt én situasjon: avvist fil eller feilet kjøring». *Fix:* Utvid regelen i DESIGN til «avvist, feilet eller utilgjengelig», eller gi tilstanden den grå varianten.
- **[medium]** Regelen for blått motsier seg selv (DESIGN *Colors* og *Do's and Don'ts*). Den sier «bruk blått bare for valgt og prognose», men samme seksjon bruker blått på primærknappen, fokusringen og lenkeknappene. *Fix:* Skriv regelen om til «valgt, prognose og handling (primærknapp, lenkeknapper, fokus)».
- **[medium]** Fontvektene motsier hverandre (DESIGN *Typography*). Teksten sier «Bare to vekter: 400 og 600», men `typography.label.fontWeight: '500'` og teksten «vekt 500» på neste linje. *Fix:* Sett label til 400 eller 600, eller skriv tre vekter.
- **[low]** FR-21 sier «ETS-kolonnen viser teksten …», men begge filene har modellene som rader («ETS-raden byttes ut», DESIGN *Components*, Backtest-tabell). Teksten er den samme, men orienteringen avviker fra kilden. *Fix:* Si i EXPERIENCE at modellene er rader, og at PRD-ens «kolonne» leses som «raden for ETS».
- **[low]** Tabellen *Faste tekster* sier «ordrett som i PRD-en (§11.2)», men §11.2 fastsetter bare FR-12, FR-20 og FR-21. FR-18-linja er bare «på formen». Selve FR-12-merknaden siteres ikke, så konsumenten må til PRD-en for å finne den. *Fix:* Siter FR-12-teksten ordrett. Merk FR-18-linja som mal.
- **[low]** PRD §3 definerer *Topplinje* slik at den inkluderer valideringsrapporten, mens EXPERIENCE IA og FR-18 («rett under topplinjen») skiller dem. Avviket kommer fra PRD-en, men spines bør velge og si det. *Fix:* Skriv én setning i IA: «Valideringsrapporten hører til topplinjen i PRD-ordlista, men står som eget felt rett under.»
- **[low]** Forklaringen i grafen bruker «Spenn Pessimistisk–Optimistisk (P10–P90)», som ikke er et ordlisteord. Ordlista har *Prediksjonsintervall*. Valget er bevisst og knyttet til PRD spm. 3 under *Åpne punkter*, men avviket er ikke merket der teksten står. *Fix:* Legg inn en kort merknad i raden Graf.
- **[low]** UJ-1 steg 3 viser «i dag kl. 09.42», men *Tall- og datoformat* fastsetter bare «13.11.2026 kl. 09.42». *Fix:* Bruk det faste formatet i flyten, eller legg til en regel for relativ dato.
- **[low]** I *Voice and Tone* er «Rad 418: antall må være et heltall ≥ 0» merket som «FR-3, ordrett format». Teksten kommer fra eksempelet i UJ-2, og FR-3 fastsetter ingen ordlyd. *Fix:* Endre kilden til «UJ-2-eksempel».
- **[low]** Oppsummeringsmalen «✓ {n} produkter godkjent · {k} flagget (kort historikk)» mangler regler for n = 1 og k = 0. *Fix:* Fastsett entall («1 produkt godkjent») og om «· 0 flagget …» skal vises eller utelates.

## 8. Shape fit — strong

DESIGN.md følger den kanoniske rekkefølgen: Brand & Style, Colors, Typography, Layout & Spacing, Elevation & Depth, Shapes, Components, Do's and Don'ts. EXPERIENCE.md har alle standardseksjonene: Foundation, Information Architecture, Voice and Tone, Component Patterns, State Patterns, Interaction Primitives, Accessibility Floor, Responsive & Platform, Inspiration & Anti-patterns og Key Flows. De to egne seksjonene, *Tall- og datoformat* og *Åpne punkter*, fortjener plassen sin. Frontmatteren har `name`, `status` og `sources` i begge filene.

### Findings

- **[low]** DESIGN-frontmatteren har nøkler utenfor spesifikasjonen: `status`, `created`, `updated` og `sources`. Det er ufarlig, men en strikt DESIGN.md-parser kan advare. *Fix:* Ingen handling nødvendig. Eventuelt kan nøklene samles under en `meta:`-nøkkel hvis verktøyet klager.

## Mechanical notes

- Alle `{…}`-referansene i begge filene er sjekket mot frontmatteren, og ingen peker på noe som ikke finnes. Tokenene som aldri refereres i prosa, er `spacing.chart-height` (360 px står som tall i ASCII-skissen) og `spacing.topbar-height`, som bare brukes i `components`.
- Kontrastene er regnet med relativ luminans etter WCAG 2.x (sRGB-linearisering, (L1 + 0,05) / (L2 + 0,05)). De tre tallene DESIGN.md oppgir, stemmer: 6,17, 6,37 og 3,18.
- Fargeforskjellen mellom historikk og prognose er bare 1,54:1 (`chart-history` mot `chart-forecast`). Det er greit fordi linjestilen skiller dem (heltrukket mot stiplet), slik begge filene sier.
- `.memlog.md` er konsistent med spines på alle beslutningspunkter: autovalg, én desimal i WAPE, rødt bare ved feil, reflow under 1024 px og søk som åpent punkt. Unntaket er at «rødt bare ved avvist/feilet» er brutt av tilstanden *Ingen kontakt med backend* (se kategori 7).
- Antall funn: critical 0 · high 3 · medium 15 · low 23.
