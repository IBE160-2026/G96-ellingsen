# Tilgjengelighetsreview — G96-ellingsen

Gjennomgått: `DESIGN.md` og `EXPERIENCE.md` (ux-G96-ellingsen-2026-11-14), mot WCAG 2.1 AA. Kontrastverdier er beregnet med WCAG-formelen for relativ luminans (sRGB), ikke anslått.

## Overall verdict

**Godkjent med endringer.** Spinen er over snittet: ikke-bare-farge er gjennomført (linjestil, ikon + tekst på flagg, tekstlig dommerlinje), tekstkontrastene holder AA overalt, feilrapporten (3.3.1/3.3.3) er forbilledlig, og `inert`, hopplenke, synlige etiketter og ekte tabeller er spesifisert. Men fem forhold vil gi AA-brudd hvis spinen implementeres som skrevet, særlig fordi «shadcn uendret» arver standarder som ikke holder (fokusring og inndatakanter), og fordi grafens tastaturmodell og tekstalternativ ikke henger sammen. Ingen funn er kritiske.

| Alvorlighet | Antall |
|---|---|
| Critical | 0 |
| High | 5 |
| Medium | 9 |
| Low | 8 |

## Kontrasttabell (beregnet)

Krav: tekst 4,5:1; ikke-tekst/UI-komponenter og grafiske objekter 3:1 (1.4.11).

| Forgrunn | Bakgrunn | Bruk | Kontrast | Krav | Resultat |
|---|---|---|---|---|---|
| `#1F2328` tekst | `#FFFFFF` | brødtekst | 15,80 | 4,5 | OK |
| `#1F2328` tekst | `#F6F7F8` surface-subtle | panel-/tabellhoder, WAPE-linje, flagg | 14,73 | 4,5 | OK |
| `#1F2328` tekst | `#E8F0FA` primary-subtle | valgt produktrad | 13,75 | 4,5 | OK |
| `#1F2328` tekst | `#FDECEA` destructive-subtle | avvist rapport | 13,81 | 4,5 | OK |
| `#5B626B` dempet | `#FFFFFF` | akseetiketter, merknader | 6,17 | 4,5 | OK («minst 6:1» stemmer) |
| `#5B626B` dempet | `#F6F7F8` | P10/P50/P90-undertekst i tabellhode | 5,75 | 4,5 | OK (men under 6:1 — påstanden i DESIGN gjelder bare hvitt) |
| `#5B626B` dempet | `#E8F0FA` | dempet tekst i valgt rad | 5,37 | 4,5 | OK |
| `#5B626B` dempet | `#FDECEA` | dempet tekst i avvist rapport | 5,39 | 4,5 | OK |
| `#5B626B` dempet | `#C9DAF0` bånd | tekst oppå båndet (bør unngås) | 4,34 | 4,5 | **Feiler** hvis det forekommer |
| `#1F5FAD` primary | `#FFFFFF` | lenkeknapp «Vis detaljer» | 6,37 | 4,5 | OK |
| `#1F5FAD` primary | `#F6F7F8` | lenkeknapp på grå flate | 5,94 | 4,5 | OK |
| `#1F5FAD` primary | `#E8F0FA` | stripe/fokusring i valgt rad | 5,54 | 3 | OK |
| `#FFFFFF` | `#1F5FAD` | primærknapp | 6,37 | 4,5 | OK |
| `#B42318` destructive | `#FFFFFF` | rød tekst/stripe | 6,57 | 4,5 | OK |
| `#B42318` destructive | `#FDECEA` | rød overskrift/stripe i avvist rapport | 5,75 | 4,5 | OK |
| `#D9DCE0` border | `#FFFFFF` | **kant på Input/Select**, paneler | 1,38 | 3 (for inndatafelt) | **Feiler** for inndatafelt; OK for paneler (dekor) |
| `#D9DCE0` border | `#F6F7F8` | flagg-kant, godkjent-stripe | 1,28 | — | Dekor; OK fordi tekst bærer meningen |
| `#ECEEF0` gridline | `#FFFFFF` | rutenett graf/tabell | 1,16 | — | Dekor; OK (verdier finnes i tabell/tooltip) |
| `#F6F7F8` | `#FFFFFF` | hover på rad | 1,07 | — | OK (hover er ikke informasjonsbærende) |
| `#E8F0FA` | `#FFFFFF` | valgt rad-flate | 1,15 | — | OK fordi stripen (6,37) + `aria-selected` bærer valget |
| `#C9DAF0` chart-band | `#FFFFFF` | P10–P90-bånd + legendefelt | 1,42 | 3 | **Feiler** |
| `#1F5FAD` chart-forecast | `#C9DAF0` | P50-linje oppå båndet | 4,48 | 3 | OK |
| `#3D4450` chart-history | `#FFFFFF` | historikklinje | 9,81 | 3 | OK |
| `#3D4450` chart-history | `#C9DAF0` | historikk mot bånd (ved skjøt) | 6,90 | 3 | OK |
| `#3D4450` history | `#1F5FAD` forecast | skille historikk/prognose | 1,54 | — | OK fordi linjestil skiller (1.4.1) |
| `#8A919A` chart-horizon | `#FFFFFF` | horisontmarkør | 3,18 | 3 | OK (DESIGN sier 3,2 — stemmer) |
| `#8A919A` chart-horizon | `#C9DAF0` | markøren der den går gjennom båndet | 2,24 | 3 | Feiler marginalt (se L2) |
| `#8A919A` som **tekst** | `#FFFFFF` | hvis «Prognose →» får markørfargen | 3,18 | 4,5 | **Feiler** (se L2) |
| `#1F5FAD` ring, 100 % | `#FFFFFF` | fokusring slik DESIGN beskriver | 6,37 | 3 | OK |
| shadcn `ring-ring/50` → `#8FAFD6` | `#FFFFFF` | fokusring slik shadcn v4 leverer | 2,27 | 3 | **Feiler** |
| `#8FAFD6` | `#1F5FAD` | samme ring rundt primærknappen | 2,81 | 3 | **Feiler** |
| `ring/50` på `#E8F0FA` → `#84A8D4` | `#E8F0FA` | fokus i valgt rad | 2,14 | 3 | **Feiler** |

Kandidater for fiks (beregnet): `#767C85` gir 4,21 mot hvitt / 3,92 mot surface-subtle (inndatakant); `#4A74B5` gir 4,71 mot hvitt (båndkanter); `#6B7480` gir 4,74 mot hvitt / 3,33 mot bånd (horisontmarkør).

## High

### H1. Fokusringen arver shadcn sin 50 %-ring og feiler 1.4.11 / svekker 2.4.7
- **Lokasjon:** DESIGN.md frontmatter `ring: '#1F5FAD'` + *Components* («brukes som shadcn leverer det»); EXPERIENCE.md *Accessibility Floor* → «Fokusringen er alltid synlig (`{colors.ring}`)».
- **Problem:** shadcn v4-komponentene (Button, Input, Select) bruker `focus-visible:ring-ring/50 ring-[3px]`. Med `#1F5FAD` blir effektiv ring `#8FAFD6`: 2,27:1 mot hvitt, 2,81:1 mot primærknappen og 2,14:1 i valgt rad. Spinen sier bare «ring-farge», ikke opasitet, og sier eksplisitt at komponentene brukes uendret.
- **Fiks:** Spesifiser fokusindikator som token-sett: «2 px heltrukken `#1F5FAD` i 100 % opasitet med 2 px hvit offset (`ring-offset-2 ring-offset-background`)». Overstyr `ring-ring/50` globalt. Offset gir også synlig ring rundt den blå primærknappen (hvitt gap + blå ring = 6,37:1 mot gapet).

### H2. Kant på inndatafelt (søk, datasettvelger) er 1,38:1 — 1.4.11
- **Lokasjon:** DESIGN.md frontmatter `border: '#D9DCE0'` og kommentaren «input … arves fra shadcn»; *Components* (`Select`, `Input` uendret).
- **Problem:** Søkefeltet og Select-triggeren identifiseres visuelt bare av kanten. `#D9DCE0` gir 1,38:1 mot hvitt; shadcn-standard `input` (≈`#E5E5E5`) er enda svakere (~1,26:1). Begge feiler kravet om 3:1 for komponentgrenser.
- **Fiks:** Legg inn eget token `input: '#767C85'` (4,21:1 mot hvitt, 3,92:1 mot surface-subtle) for Input, Select-trigger og eventuelle sekundærknapper med kun kant. Behold `#D9DCE0` for paneler og skillelinjer.

### H3. Grafen er både `role="img"` og fokuserbar med piltaster, og historikken mangler tekstalternativ
- **Lokasjon:** EXPERIENCE.md *Interaction Primitives* («Grafen er også et fokuserbart element … pil venstre og høyre»), *Accessibility Floor → Grafen* («`role="img"` … Tabellen er derfor tekstalternativet»), *Component Patterns → Graf* (tooltip «Faktisk»).
- **Problem:** (a) `role="img"` gjør alle barn presentasjonelle; tooltip-innholdet som piltastene flytter mellom eksponeres aldri for skjermleser, og en interaktiv kontroll med bilderolle bryter 4.1.2. I skjermleserens lesemodus fanges piltastene av leseren, så tastatur-modellen virker bare for seende tastaturbrukere. (b) Påstanden «Alle tallene finnes også i scenariotabellen» er feil: de historiske månedsverdiene («Faktisk», 12–48 måneder) finnes bare i grafen og tooltipen. Det er 1.1.1/1.3.1-brudd for historikken.
- **Fiks:** Velg én modell. Anbefalt: grafen er `role="img"` med `aria-label`, **ikke** fokuserbar, og en `Collapsible` «Vis historikk som tabell» (Måned · Faktisk) under grafen gir tekstalternativet. Behold piltastnavigasjon kun hvis grafen får `role="group"` + `aria-roledescription="graf"`, en instruksjon i `aria-describedby`, og en `aria-live="polite"`-region som leser «nov. 2026: Pessimistisk 820, Forventet 960, Optimistisk 1 110» ved hvert steg. Oppdater tab-rekkefølgen tilsvarende.

### H4. Fokus går tapt etter avvist fil, feilet kjøring og backend-feil (2.4.3)
- **Lokasjon:** EXPERIENCE.md *State Patterns* (bare «Godkjent etter kjøring» flytter fokus), *Accessibility Floor → Inert under kjøring*.
- **Problem:** Når `inert` settes på siden mens **Last opp CSV** har fokus (fokus kommer tilbake dit når filvelgeren lukkes), blir fokus kastet til `<body>`. Når `inert` fjernes, kommer det ikke tilbake av seg selv. For godkjent er dette løst (fokus til rapportoverskrift), men for *Fil avvist*, *Kjøring feilet* og *Ingen kontakt* er fokus udefinert; en tastaturbruker havner øverst og må tabbe seg ned til feillisten. «Lukk» på rapporten mangler også fokusmål.
- **Fiks:** Regel for alle utfall: når sløret fjernes, flytt fokus til rapportoverskriften (`tabindex="-1"`), også ved avvisning og feil. Etter «Lukk»: fokus til **Last opp CSV**. Hvis fokus flyttes, kan `role="alert"` byttes til vanlig region for å unngå dobbel opplesing (se L6).

### H5. Reflow er bare spesifisert for 200 %, ikke 320 CSS-px, og den festede WAPE-linjen spiser viewporten (1.4.10)
- **Lokasjon:** DESIGN.md *Layout & Spacing* («festet nederst», «< 1024 … for eksempel ved 200 % zoom»); EXPERIENCE.md *Responsive & Platform*.
- **Problem:** 1.4.10 krever bruk uten todimensjonal scrolling ved 320 CSS-px (400 % zoom på 1280 px). På en 1366×768-laptop gir 400 % en viewport på ca. 341×192 CSS-px. WAPE-linjen («Total WAPE: Sesongnaiv baseline 21,3 % · ETS 18,1 % · ETS slår baseline for 162 av 180 produkter») brekker da til 4–5 linjer og tar halve høyden permanent; produktlisten med «maks 50 vh» blir ~96 px. Lasteboksen og topplinjen (fast 56 px) er heller ikke spesifisert for smal bredde.
- **Fiks:** Spesifiser reflow ned til 320 CSS-px. Under 1024 px: WAPE-linjen er ikke lenger festet (ligger sist i flyten), topplinjen er ikke festet og bruker `min-height`, produktlisten får `max-height: max(50vh, 240px)` eller ingen egen scroll. Lasteboksen: `max-width: calc(100vw - 32px)`. Test i Playwright med viewport 320×256.

## Medium

### M1. P10–P90-båndet er 1,42:1 mot hvitt (1.4.11)
- **Lokasjon:** DESIGN.md frontmatter `chart-band: '#C9DAF0'`, *Colors → Grafen*.
- **Problem:** Båndet er et grafisk objekt som bærer informasjon (spennet), og det samme feltet brukes i legenden. Kantene av båndet er det som må sees for å lese P10/P90. Scenariotabellen dekker verdiene, så dette er ikke blokkerende, men grafen alene oppfyller ikke 1.4.11.
- **Fiks:** Tegn P10- og P90-kanten som 1 px heltrukne linjer i `#4A74B5` (4,71:1 mot hvitt), skilt fra den stiplede P50-linjen. Behold fyllet som det er. Legendefeltet får samme kant.

### M2. «Velg ved pil» er forsvarlig, men roving tabindex er uspesifisert ved filter og ved tab inn i listen
- **Lokasjon:** EXPERIENCE.md *Interaction Primitives → Produktlisten*, *Component Patterns → Søk / Produktliste*.
- **Vurdering:** Selection-follows-focus er et godkjent APG-mønster for listbox, og oppdatering av graf og tabeller på samme side er innholdsendring, ikke kontekstendring — 3.2.1/3.2.2 brytes ikke. Auto-valg av første rad er også greit.
- **Problem:** (a) Hvis valgt produkt er filtrert bort, finnes ingen `option` med `tabindex="0"` som er valgt; spinen sier ikke hvilken rad som får fokus ved Tab, og om fokus på den da *endrer* valget (det bør det ikke — Tab inn skal aldri bytte produkt). (b) Hvert piltrykk utløser en produktforespørsel og en Skeleton («Forrige produkt blir ikke stående»); holder Kari pil nede, blinker graf og tabeller, og skjermlesere kan lese tomme skeleton-tilstander.
- **Fiks:** Spesifiser: Tab inn fokuserer valgt rad hvis den er synlig, ellers første treff uten å velge det; valg skjer først ved pil/Enter. Debounce henting ~200 ms etter siste piltrykk og marker panelene `aria-busy="true"` mens de laster. Gi listboxen `aria-label="Produkter, svakeste først"`.

### M3. Live-regioner må finnes i DOM før innholdet settes, og lasteboksen bør få fokus
- **Lokasjon:** EXPERIENCE.md *Accessibility Floor → Annonsering*, *State Patterns → Kjøring pågår*.
- **Problem:** En `role="status"`-boks som monteres samtidig med teksten blir ofte ikke annonsert (NVDA/JAWS i Chromium). Mens alt annet er `inert`, har skjermleserbrukeren dessuten ingenting fokusert å lese.
- **Fiks:** Hold en tom `role="status"`-region permanent utenfor det inerte treet og skriv teksten inn i den. Plasser lasteboksen som søsken av app-roten (ikke inni elementet som får `inert`) og gi den `tabindex="-1"` + fokus når den vises.

### M4. Recharts-tooltipen oppfyller ikke 1.4.13 uten tilpasning
- **Lokasjon:** EXPERIENCE.md *Component Patterns → Graf* («Tooltip ved hover eller tastaturfokus»), *Interaction Primitives*.
- **Problem:** Recharts-tooltip kan ikke lukkes med Esc (dismissable), og ved tastaturfokus finnes ingen definert lukkemekanisme. Den dekker også deler av grafen.
- **Fiks:** Esc skjuler tooltipen til neste pekerbevegelse/pil-trykk; tooltipen plasseres slik at den ikke dekker punktet den beskriver. shadcn/Radix `Tooltip` andre steder er OK, men ingen informasjon skal finnes bare i en tooltip.

### M5. Udefinert WAPE «–» leses ikke av skjermleser
- **Lokasjon:** EXPERIENCE.md *Tall- og datoformat* («Udefinert WAPE vises som «–»»).
- **Problem:** NVDA og JAWS hopper som standard over tankestrek; cellen/raden leses som tom og kan forveksles med manglende data.
- **Fiks:** `<span aria-hidden="true">–</span><span class="sr-only">udefinert</span>` i tabeller, produktrader og WAPE-linjen.

### M6. Ingen tidsavbrudd for kjøringen — siden kan bli låst for alltid
- **Lokasjon:** EXPERIENCE.md *State Patterns → Kjøring pågår* («ingen avbrytknapp»).
- **Problem:** 2.2.1 gjelder ikke (dette er ventetid, ikke en tidsfrist brukeren må handle innen), men hvis forespørselen henger, er hele siden `inert` uten utvei — i praksis en felle for alle brukere (jf. 2.1.2).
- **Fiks:** Klient-timeout (f.eks. 120 s) som går til tilstanden *Kjøring feilet* med en norsk melding, og fokusregelen fra H4.

### M7. Scrollbare regioner må nås med tastatur (2.1.1)
- **Lokasjon:** EXPERIENCE.md *State Patterns → Fil avvist* («maks 320 px høy»), *Responsive & Platform* («Grafen og tabellene kan scrolle vannrett»), produktlisten som «scroller for seg selv».
- **Problem:** Feillisten (kan ha hundrevis av rader uten fokuserbare barn) og vannrett scrollende tabeller ved reflow kan ikke scrolles med tastatur uten fokuserbar beholder i eldre Chromium, og har uansett ikke noe navn når de får fokus.
- **Fiks:** `tabindex="0"`, `role="region"` og `aria-label` («Feil i fila», «Scenariotabell») på hver scrollbeholder; ta dem med i tab-rekkefølgen.

### M8. Produktradens tilgjengelige navn er uklart (1.3.1)
- **Lokasjon:** DESIGN.md *Components → Produktrad*; EXPERIENCE.md *Component Patterns → Produktliste*.
- **Problem:** `option` får navnet sitt fra innholdet: «P-109 24,0 % ETS taper». Det sies ikke hva prosenten er (WAPE for hvilken modell?), og Lucide-ikonene må ikke gi støy.
- **Fiks:** Spesifiser navnet, f.eks. «P-109, WAPE 24,0 %, flagg: ETS taper». Visuelt skjult «WAPE» foran tallet; ikonene `aria-hidden`. Avklar i spinen hvilken WAPE raden viser.

### M9. Kravet til CSV-kolonner er bare usynlig instruks (3.3.2)
- **Lokasjon:** EXPERIENCE.md *Accessibility Floor → Etiketter* (`aria-describedby` med `produkt_id`, `maaned`, `antall`).
- **Problem:** Seende brukere får ikke vite formatkravet før fila avvises. 3.3.2 krever instruksjoner når input krever bestemt format.
- **Fiks:** Vis en kort linje i `{typography.caption}` (f.eks. i godkjent-rapporten eller ved knappen): «CSV med kolonnene produkt_id, maaned, antall», og pek `aria-describedby` til den samme synlige teksten.

## Low

### L1. Tab-rekkefølgen tar med «Scenariotabell» som stopp
- **Lokasjon:** EXPERIENCE.md *Accessibility Floor → Tastatur*. Statiske tabeller skal ikke være tab-stopp med mindre de scroller (da gjelder M7). Fjern den, eller presiser at det er scrollbeholderen. Ta med «Vis alle advarsler», «Lukk» og «Tøm søk» i rekkefølgen.

### L2. Horisontmarkøren og etiketten «Prognose →»
- **Lokasjon:** DESIGN.md *Colors → Grafen*. Markøren er 2,24:1 der den krysser båndet, og etikettens tekstfarge er ikke spesifisert (i `#8A919A` blir den 3,18:1 og feiler 4,5:1). Fiks: etiketten i `{colors.muted-foreground}` (6,17:1); vurder `#6B7480` for markøren (4,74 mot hvitt, 3,33 mot bånd). Pilen `aria-hidden`.

### L3. Landemerker og overskriftsnivåer er ikke spesifisert (1.3.1, 2.4.1, 2.4.6)
- Spesifiser `<header>`, `<main>`, produktlisten som `<nav aria-label="Produkter">` eller region, og panelhoder som `<h2>`. Hopplenken trenger et mål med `tabindex="-1"`.

### L4. Faste høyder vs. tekstavstand (1.4.12)
- **Lokasjon:** DESIGN.md `topbar-height: 56px`, produktrad med to linjer. Bruk `min-height`, ikke `height`, på topplinje, rader, flagg og WAPE-linje, så 1,5 linjeavstand / 0,12 em bokstavavstand ikke klipper tekst.

### L5. Språk og symboler (3.1.1/3.1.2)
- `lang="nb"` er riktig. ETS, WAPE og P10/P50/P90 er fagtermer og er unntatt 3.1.2; ingen `lang="en"` trengs. Merk tegn som leses rart: «✓» (`aria-hidden` — teksten «godkjent» bærer meningen), «→», «≥» (vurder visuelt skjult «større enn eller lik» i feilmeldinger hvis brukertest viser forvirring), «·» som skille.

### L6. Dobbel annonsering ved godkjent resultat
- **Lokasjon:** EXPERIENCE.md *Annonsering* — både `aria-live="polite"` og fokusflytting til overskriften. Skjermleseren kan lese rapporten to ganger. Velg fokusflytting (H4) og dropp live-regionen for rapporten.

### L7. Merknad: festet bunnlinje kan skjule fokus (2.4.11, WCAG 2.2 — ikke i målet)
- Fokuserte elementer nederst i hovedområdet kan havne under WAPE-linjen. Sett `scroll-padding-bottom` lik linjens høyde. «Valgt rad holder seg synlig ved scrolling» bør presiseres som `scrollIntoView({block:'nearest'})`, ikke som festet rad (som også kan dekke fokus).

### L8. Tabelldetaljer (1.3.1)
- Gi hver tabell `<caption>` (kan være visuelt skjult), månedskolonne og «Sum» som `<th scope="row">`, og knytt FR-12-merknaden til tabellen med `aria-describedby`. Når ETS-raden erstattes av «ETS er ikke backtestet …», behold `<th scope="row">ETS</th>` og la teksten spenne kolonnene. Søketelleren bør debounces så den ikke annonseres for hvert tastetrykk. Spinneren bør respektere `prefers-reduced-motion` (2.2.2 er ikke brutt, siden lasteanimasjon uten annen interaksjon regnes som essensiell).

## Det som er godt (ingen endring nødvendig)

- **1.4.1 Bruk av farge:** historikk/prognose skilles på linjestil, flagg har ikon + tekst, valgt rad har stripe + `aria-selected`, dommerlinjen er tekst, rødt bærer aldri mening alene, og trafikklys er eksplisitt forkastet.
- **Tekstkontrast:** alle tekstkombinasjoner i spinen er over 5,3:1. Påstandene i DESIGN.md (6:1 dempet på hvitt, 6,4:1 blått, 3,2:1 horisont) stemmer.
- **3.3.1/3.3.3:** alle feil listes samlet, med radnummer, filens månedsformat og konkret retting («må være et heltall ≥ 0»).
- **3.3.2:** synlige etiketter «Søk produkt-ID» og «Datasett», ikke bare plassholder.
- **2.4.1:** hopplenke til produktlisten.
- **Modaler, toasts, hover-only og dra-og-slipp** er forbudt — fjerner hele klasser av tilgjengelighetsfeil.
- **`inert`** under kjøring er riktig verktøy (forutsatt plasseringen i M3).
- **Ingen animasjon i grafen**, systemfonter og ekte `<table>` med `scope`.
