# Product Brief — PROGNOS

**AI-støttet prognose- og etterspørselsmodul for MRP**

Gruppe G96 · IBE160 Programmering med KI · Høgskolen i Molde · Høst 2026

---

## Executive brief

PROGNOS er en AI-støttet modul for prognoser og etterspørselsstyring (demand management) som kobles inn i et MRP-system (Material Requirements Planning). Modulen samler historiske salgstall, sesong- og trendsignaler, kampanjeplaner, markedsdata, faktiske kundebestillinger og selgernes egne salgsprognoser i én modell, og gjør dette om til etterspørselsprognoser per produkt med tilhørende usikkerhet. I stedet for ett tall får planleggeren flere scenarioer — forventet, optimistisk og pessimistisk — og konkrete anbefalinger på de beslutningene som faktisk koster penger: skal vi produsere nå eller trekke fra lager, og skal vi produsere selv eller sette ut til en underleverandør?

Problemet PROGNOS løser, er at MRP-systemet i de fleste små og mellomstore produksjonsbedrifter bare er så godt som prognosen det får inn, og den prognosen lages ofte i regneark, basert på fjorårets tall og magefølelse. Resultatet er kjent: for mye kapital bundet i feil varer, samtidig som populære produkter blir utsolgt, kampanjer som sprenger kapasiteten, og hastebestillinger hos underleverandører til høy pris. Når prognosen er feil, forplanter feilen seg gjennom hele materialplanen — fra innkjøp av råvarer til bemanning på gulvet.

Tidspunktet er riktig nå fordi tre ting har skjedd samtidig. Maskinlæringsmodeller for tidsserier har blitt modne, åpne og billige nok til at også mindre bedrifter kan ta dem i bruk. Forsyningskjedene har de siste årene vist seg å være langt mer ustabile enn planleggingsverktøyene ble laget for, noe som gjør scenario-tenkning til en nødvendighet og ikke en luksus. Og språkmodeller gjør det nå mulig å forklare en prognose i klartekst — *hvorfor* modellen tror etterspørselen øker — slik at planleggere faktisk stoler på og bruker tallene. PROGNOS kombinerer dette til et verktøy som flytter etterspørselsplanlegging fra regneark og antakelser til datadrevne, forklarbare beslutninger.

---

## 1. Problem

Produksjonsbedrifter planlegger materialbehov ut fra forventet etterspørsel, men dagens prognosearbeid har flere svakheter:

- **Fragmenterte datakilder.** Salgshistorikk ligger i ERP, kampanjeplaner i markedsavdelingens regneark, kundebestillinger i ordresystemet og selgernes forventninger i e-post og møtereferater. Ingen ser helheten.
- **Manuelle og statiske prognoser.** Prognoser lages ofte som enkle glidende gjennomsnitt eller «fjoråret + X %», og oppdateres sjelden når virkeligheten endrer seg.
- **Sesong, trend og kampanjer blandes sammen.** Uten å skille disse effektene fra hverandre er det vanskelig å vite om et salgsløft var en varig trend eller en engangseffekt av en kampanje.
- **Ingen håndtering av usikkerhet.** MRP får ett tall per produkt og periode. Planleggeren vet ikke hvor sikker prognosen er, og kan derfor ikke dimensjonere sikkerhetslager eller kapasitet fornuftig.
- **Beslutninger tas uten beslutningsstøtte.** Valg mellom å produsere eller levere fra lager, og mellom intern produksjon og outsourcing, tas ad hoc og ofte for sent — typisk når kapasiteten allerede er sprengt.

**Konsekvenser:** Høy lagerbinding, utsolgte produkter, tapt salg, dyre hasteordrer, overtid og dårlig utnyttelse av egen kapasitet.

---

## 2. Målgruppe

**Primære brukere**

| Rolle | Behov |
|---|---|
| **Etterspørselsplanlegger / demand planner** | Lage, justere og godkjenne prognoser per produkt; forstå hva som driver endringer. |
| **Produksjons- og materialplanlegger** | Få pålitelige prognoser inn i MRP; vite når kapasiteten ikke strekker til. |
| **Innkjøps- og logistikkansvarlig** | Planlegge innkjøp av råvarer og komponenter; vurdere outsourcing i tide. |

**Sekundære brukere**

| Rolle | Behov |
|---|---|
| **Salg og key account** | Legge inn egne salgsprognoser og store forventede ordrer; se konsekvensen. |
| **Markedsavdeling** | Registrere kampanjer og se forventet effekt på etterspørsel. |
| **Ledelse / økonomi (S&OP)** | Scenarioer for budsjett, kapasitet og kapitalbinding. |

**Målvirksomhet:** Små og mellomstore produksjonsbedrifter (ca. 20–500 ansatte) med et vareutvalg fra noen titalls til noen tusen produkter, som har et MRP/ERP-system, men mangler et dedikert verktøy for etterspørselsplanlegging.

---

## 3. Mål

**Forretningsmål**

1. Redusere prognosefeil (målt i MAPE/WAPE) sammenlignet med dagens metode.
2. Redusere lagerbinding uten å redusere leveringsevnen.
3. Øke leveringsgraden (service level) og redusere antall utsolgt-situasjoner.
4. Redusere kostnader til hasteordrer, overtid og ikke-planlagt outsourcing.

**Produktmål**

1. Samle alle relevante etterspørselssignaler i én prognosemodell.
2. Levere prognoser per produkt med usikkerhetsintervall, ikke bare ett punktestimat.
3. Gjøre det enkelt å sammenligne scenarioer før beslutninger tas.
4. Gi konkrete, forklarbare anbefalinger på beslutningspunktene *produksjon vs. lager* og *intern produksjon vs. outsourcing*.
5. Være forklarbar: brukeren skal alltid kunne se *hvorfor* prognosen ser ut som den gjør.

**Læringsmål (prosjekt)**

- Demonstrere hvordan KI kan brukes både *i* produktet (prognosemodeller, forklaringer) og *i* utviklingsprosessen (koding, testing, kvalitetssikring).

---

## 4. Hovedfunksjoner

### 4.1 Datainntak

Modulen tar inn og harmoniserer følgende data:

| Datakilde | Innhold | Bruk i modellen |
|---|---|---|
| **Historiske salgstall** | Salg per produkt, kunde, region og periode | Grunnlag for tidsseriemodellen |
| **Sesong- og trendsignaler** | Sesongmønstre, helligdager, langsiktige trender, vær (valgfritt) | Forklaringsvariabler og dekomponering |
| **Kampanjer og markedsdata** | Planlagte kampanjer, prisendringer, markedsandeler, bransjeindekser | Justering av forventet løft/fall |
| **Kundebestillinger** | Bekreftede og åpne ordrer, ordrereserve | Kortsiktig prognose («demand sensing») |
| **Salgsprognoser** | Selgernes egne estimater per kunde/produkt | Supplerende signal, vektes mot modellen |

Inkluderer validering, datakvalitetsrapport (manglende verdier, avvik, outliers) og mulighet for opplasting via CSV/Excel eller API.

### 4.2 Prognosemotor

- Etterspørselsprognose **per produkt** (og aggregert per produktgruppe) for valgt horisont, f.eks. uke/måned, 1–18 måneder frem.
- Dekomponering i **nivå, trend, sesong og kampanjeeffekt**.
- **Usikkerhetsintervaller** (f.eks. P10/P50/P90).
- Automatisk modellvalg per produkt basert på historisk treffsikkerhet (backtesting).
- Håndtering av nye produkter og produkter med sporadisk salg.

### 4.3 Scenarioer

- Standardscenarioer: **forventet, optimistisk og pessimistisk**.
- Egendefinerte «hva hvis»-scenarioer: f.eks. «kampanjen flyttes to uker», «stor kunde dobler ordren», «markedet faller 10 %».
- Side-om-side-sammenligning av scenarioer med effekt på volum, kapasitet, lager og kostnad.

### 4.4 Beslutningsstøtte

**Produksjon vs. lager**
- Anbefaler om etterspørselen bør dekkes fra eksisterende lager eller ved ny produksjon, basert på lagernivå, sikkerhetslager, holdbarhet, oppsettkostnader og prognoseusikkerhet.
- Foreslår sikkerhetslager ut fra ønsket leveringsgrad og prognoseusikkerhet.

**Intern produksjon vs. outsourcing**
- Sammenligner prognostisert behov med tilgjengelig intern kapasitet per periode.
- Varsler om kapasitetsgap i god tid og beregner kostnad for alternativer: overtid, omprioritering eller outsourcing.
- Anbefaler et alternativ med begrunnelse (kostnad, ledetid, risiko).

### 4.5 Forklaring og samarbeid

- **Forklaring i klartekst** generert av språkmodell: «Prognosen for produkt X er 18 % høyere enn i fjor, hovedsakelig på grunn av planlagt kampanje i uke 12 og en positiv trend siste seks måneder.»
- Planleggeren kan **overstyre** prognosen med begrunnelse; overstyringer logges og treffsikkerheten til overstyringer måles.
- Godkjenningsflyt før prognosen sendes til MRP.

### 4.6 Integrasjon og output

- Eksport av godkjent prognose til MRP (API eller fil).
- Dashboard med prognoser, scenarioer, avvik og anbefalinger.
- Varsler ved store avvik mellom prognose og faktisk salg.

---

## 5. Hva som ikke er med (avgrensning)

Følgende er bevisst holdt utenfor denne versjonen:

- **Full MRP-funksjonalitet.** PROGNOS beregner ikke stykklister (BOM), netto materialbehov eller innkjøpsordrer — det gjør MRP-systemet. PROGNOS leverer etterspørselen som MRP planlegger ut fra.
- **Detaljert produksjonsplanlegging og maskinsekvensering** (finplanlegging/scheduling).
- **Automatiske beslutninger.** Systemet anbefaler — et menneske beslutter. Ingen ordre eller outsourcing-avtale utløses automatisk.
- **Prisoptimalisering og dynamisk prising.**
- **Leverandørstyring og forhandling** med underleverandører utover kostnads- og ledetidsdata som input.
- **Finansiell budsjettering og regnskap.**
- **Sanntids-integrasjon mot alle ERP-systemer.** Første versjon støtter filimport og et generisk API; ferdige konnektorer til spesifikke ERP-systemer kommer senere.
- **Innsamling av ekstern markedsdata** (skraping, kjøp av datasett). Markedsdata må leveres av brukeren.

---

## 6. Teknisk tilnærming

### Arkitektur (overordnet)

```
Datakilder          →  Dataplattform       →  Prognose og analyse  →  Presentasjon
------------------     -----------------      --------------------    ---------------
Salgshistorikk         Import/validering      Prognosemodeller        Dashboard
Sesong/trend           Harmonisering          Scenariomotor           Scenarioer
Kampanjer/marked       Feature-lager          Beslutningsmotor        Anbefalinger
Kundeordrer            Database               LLM-forklaringer        Eksport til MRP
Salgsprognoser
```

### Komponenter

| Lag | Foreslått teknologi | Kommentar |
|---|---|---|
| **Backend / API** | Python, FastAPI | Python gir tilgang til de beste bibliotekene for tidsserier og ML. |
| **Database** | PostgreSQL (SQLite i utvikling) | Tidsseriedata, prognoser, scenarioer, overstyringslogg. |
| **Prognosemodeller** | Statistiske baseline-modeller (ETS, ARIMA via `statsforecast`), gradient boosting (LightGBM) med kalender-, kampanje- og ordrefeatures, ev. Prophet for sesong/helligdager | Start enkelt, mål mot baseline, legg til kompleksitet bare når den gir bedre treff. |
| **Usikkerhet** | Kvantilregresjon / konforme prediksjonsintervaller | Gir P10/P50/P90 per produkt. |
| **Scenario- og beslutningsmotor** | Regelbasert + enkel optimering (f.eks. `PuLP`/`OR-Tools`) | Kostnadsmodell for lager, produksjon, overtid og outsourcing. |
| **Forklaringer** | Språkmodell (Claude via Anthropic API) | Genererer tekst fra strukturerte modellresultater (feature-bidrag, dekomponering) — ikke fra rådata. |
| **Frontend** | Webapplikasjon (f.eks. React eller Streamlit for prototype) | Dashboard, scenariosammenligning, godkjenning. |

### Prinsipper

- **Baseline først:** Alle modeller måles mot en enkel referanse (sesongnaiv / glidende gjennomsnitt). En modell tas bare i bruk hvis den slår baseline.
- **Backtesting:** Rullerende tidsvindu-validering på historiske data før noe settes i drift.
- **Forklarbarhet:** Feature-bidrag (f.eks. SHAP) lagres og brukes som grunnlag for LLM-forklaringer, slik at teksten er forankret i faktiske modellresultater.
- **Menneske i loopen:** Alle anbefalinger kan overstyres; overstyringer logges og evalueres.
- **Sporbarhet:** Hver prognose lagres med versjon av data, modell og parametere.
- **KI i utviklingen:** KI-assistenter brukes til koding, testgenerering og kodegjennomgang, og bruken dokumenteres som del av prosjektet.

---

## 7. Hvordan vi måler suksess

### Prognosekvalitet

| Måltall | Beskrivelse | Mål |
|---|---|---|
| **WAPE / MAPE** | Gjennomsnittlig prognosefeil, vektet etter volum | Minst 20 % lavere enn dagens metode / baseline |
| **Bias** | Systematisk over- eller underprognostisering | Innenfor ±5 % |
| **Forecast Value Added (FVA)** | Forbedring fra hvert steg (modell, overstyring) mot baseline | Positiv FVA for modellen; overstyringer skal ikke forverre treffet |
| **Intervalldekning** | Andel faktiske verdier innenfor P10–P90 | Ca. 80 % |

### Forretningseffekt

| Måltall | Mål |
|---|---|
| **Lagerbinding** (lagerverdi / omløpshastighet) | 10–15 % reduksjon |
| **Leveringsgrad** (fill rate / OTIF) | Opprettholdt eller økt, mål ≥ 95 % |
| **Utsolgt-hendelser** | 25 % reduksjon |
| **Kostnad til hasteordrer, overtid og ikke-planlagt outsourcing** | Merkbar reduksjon |
| **Varslingstid for kapasitetsgap** | Kapasitetsgap identifiseres minst 4–8 uker før de oppstår |

### Bruk og tillit

| Måltall | Mål |
|---|---|
| **Andel prognoser som godkjennes uten overstyring** | Økende over tid |
| **Tid brukt på prognosearbeid per syklus** | 50 % reduksjon |
| **Brukertilfredshet** (enkel spørreundersøkelse) | ≥ 4 av 5 |
| **Andel anbefalinger som følges** | Følges opp og brukes til å forbedre beslutningsmotoren |

### Prosjektsuksess (IBE160)

- Fungerende prototype som tar inn testdata, produserer prognoser per produkt, viser scenarioer og gir anbefalinger på begge beslutningspunktene.
- Dokumentert backtest som viser at modellen slår en enkel baseline.
- Dokumentert bruk av KI i utvikling, testing og kvalitetssikring.
