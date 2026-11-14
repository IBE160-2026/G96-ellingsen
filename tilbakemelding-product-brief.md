# Tilbakemelding på product brief

| | |
|---|---|
| **Gruppe** | G96 – G96-ellingsen |
| **Product brief** | `PRODUCT_BRIEF.md` (commit `3505b8d`) |
| **Tilbakemelding fra** | Faglærer i IBE160 (utarbeidet med KI-støtte) |
| **Dato** | 2026-10-06 |

## Samlet vurdering

- **Bør revideres før dere går videre.** Rett punktene markert «Endre» før dere lager PRD og arkitektur.

**Det som er bra:**

1. Problemet er godt beskrevet og faglig forankret: fragmenterte datakilder, prognoser som «fjoråret + X %», sammenblanding av sesong, trend og kampanjer, og at MRP bare får ett tall uten usikkerhet. Avgrensningen mot full MRP (ingen BOM, ingen nettobehov, ingen innkjøpsordrer) er tydelig.
2. Prinsippene i den tekniske tilnærmingen er gode: baseline først, backtesting, at LLM-forklaringer bygger på strukturerte modellresultater og ikke på rådata, og at et menneske alltid beslutter. Det viser at dere tenker på kontroll og etterprøvbarhet.

**De viktigste endringene:**

1. Omfanget er for stort for semesteret og for én person. Briefen beskriver et fullt produkt for etterspørselsplanlegging: fem datakilder, automatisk modellvalg med ETS, ARIMA, LightGBM og Prophet, kvantilregresjon og konforme intervaller, SHAP, hva-hvis-scenarioer, to beslutningsmotorer med optimering, LLM-forklaringer, overstyringslogg, godkjenningsflyt, varsler og eksport til MRP. Velg én kjerneflyt for v1.
2. Suksesskriteriene er nesten bare forretningsmål som ikke kan måles i emnet: lagerbinding, leveringsgrad, utsolgt-hendelser og brukertilfredshet krever en ekte bedrift over tid. Legg til funksjonelle kriterier som kan bli testtilfeller, for eksempel «en opplastet CSV med 24 måneders salg gir en prognose for 6 måneder med P10/P50/P90» og «backtesten viser lavere WAPE enn sesongnaiv baseline på testdatasettet».
3. Del målgruppen ned til én primærbruker. Briefen har tre primære og tre sekundære roller. Velg etterspørselsplanleggeren og bygg v1 rundt hennes arbeidsflyt.

## Vanskelighetsgrad og gjennomførbarhet

### Vurdert vanskelighetsgrad

- **Vanskelig**

**Sammenlignbart med:** 4) KI-støttet MRP II, modul 4.1 Prognoser og Demand Management med elementer av 4.2 S&OP (produksjon vs. lager, intern produksjon vs. outsourcing). Én modul alene kunne vært middels, men med avansert maskinlæring, optimering og LLM i tillegg blir det vanskelig.

**Begrunnelse:**

| Faktor | Nivå (lav / middels / høy) | Kommentar |
|---|---|---|
| Domenelogikk – hvor mange og hvor kompliserte regler og beregninger må stemme? | Høy | Prognosemodeller, dekomponering, usikkerhetsintervaller, backtesting, sikkerhetslager, kapasitetsgap og kostnadsoptimering må alle stemme. |
| Datamodell – antall entiteter og relasjoner mellom dem | Høy | Produkt, produktgruppe, kunde, region, salg per periode, kampanje, ordre, salgsprognose, kapasitet, scenario, prognoseversjon og overstyringslogg. |
| Brukere, roller og innlogging | Middels | Seks roller er nevnt, og godkjenningsflyt forutsetter roller. |
| KI-funksjonalitet i appen, f.eks. kall til språkmodell, prompts i koden og håndtering av usikre svar | Høy | Flere ML-modeller med automatisk modellvalg, SHAP og LLM-forklaringer via Anthropic API. |
| Integrasjoner og eksterne tjenester, f.eks. API-er, betaling og e-post | Middels | Språkmodell-API og eksport til MRP via API eller fil. |
| Sanntid, samtidighet eller flere brukere som påvirker hverandre | Lav | Ikke beskrevet som krav. |
| Filhåndtering, f.eks. opplasting, PDF-lesing og eksport | Middels | CSV/Excel-import med datakvalitetsrapport og eksport til MRP. |
| Sikkerhet og personvern | Lav | Forretningsdata, men ingen personopplysninger utover kundenavn i salgsdata. Bruk syntetiske data. |

**Hva vanskelighetsgraden betyr for dere:**

- _Vanskelig:_ Et vanskelig prosjekt gir større mulighet for toppkarakter, men også større risiko. Definer en minimal versjon som sikkert kan bli ferdig, og legg resten i tydelige trinn etterpå. For dere bør den minimale versjonen være prognose med scenarioer og backtest for én datakilde.

### Gjennomførbarhet med BMAD og Claude Code

Dere skal planlegge med BMAD (product brief → PRD → arkitektur → epics og stories) og implementere med Claude Code. Vurderingen under tar hensyn til at det må være tid til hele denne flyten, og til testing, retting og README til slutt.

| Spørsmål | Vurdering (OK / risiko / stor risiko) | Kommentar |
|---|---|---|
| **Tid og omfang** – kan v1 realistisk bli ferdig og stabil i løpet av semesteret, med tid til flere iterasjoner? | Stor risiko | Seks hovedfunksjoner med mange underpunkter er langt mer enn én person rekker gjennom BMAD med testing. |
| **BMAD-flyten** – er briefen konkret nok til at PRD, arkitektur og stories kan lages uten store hull, og blir det overkommelig mange stories? | Risiko | Briefen er detaljert, men uten skille mellom v1 og senere. Det vil gi svært mange stories. |
| **Egnet for Claude Code** – bruker løsningen en vanlig, godt dokumentert teknologistakk som Claude Code håndterer godt, eller krever den nisjeteknologi, spesialmaskinvare eller mye manuell konfigurasjon? | Risiko | Python, FastAPI og SQLite er godt egnet. Mange ML-biblioteker samtidig (statsforecast, LightGBM, Prophet, SHAP, PuLP/OR-Tools) gir tung installasjon og flere feilkilder. |
| **Kontroll på KI-ens arbeid** – kan gruppen selv avgjøre om koden gjør det riktige? Krever domenet kunnskap gruppen ikke har, f.eks. avanserte beregninger eller fagregler, så er det vanskelig å kvalitetssikre. | Stor risiko | Det er svært vanskelig å avgjøre om en LightGBM-modell med konforme intervaller og SHAP-forklaringer er riktig implementert. Enkle modeller som ETS og sesongnaiv kan kontrolleres for hånd. |
| **Testbarhet** – finnes det tydelige regler og forventede resultater som tester kan skrives mot? | Risiko | Backtest mot baseline er et godt testprinsipp. Uten fasitserier og funksjonelle kriterier er det likevel uklart hva testene skal sjekke. |
| **Kjørbar for sensor** – kan appen kjøres lokalt etter README, uten gruppens nøkler, betalte kontoer eller egen infrastruktur? | Risiko | LLM-forklaringer via Anthropic API krever nøkkel. PostgreSQL krever databaseserver. Bruk SQLite og mock-forklaringer som standard. |
| **Avhengigheter og kostnader** – krever løsningen betalte API-er, f.eks. språkmodeller, og finnes det en plan for kostnad, testmodus eller mock-data? | Risiko | Anthropic API koster penger, og det er ingen plan for kostnad eller testmodus. Forklaringer kan også lages med maler ut fra dekomponeringen. |

**Konklusjon om gjennomførbarhet:**

- **Lite realistisk uten vesentlige endringer.** Se forslagene under.

**Forslag til justering av omfang eller vanskelighetsgrad:**

1. Gjør v1 til: CSV-import av salgshistorikk med enkel validering, prognose per produkt med én statistisk modell (for eksempel ETS) mot sesongnaiv baseline, tre scenarioer (forventet, optimistisk, pessimistisk), backtest med WAPE, og et dashbord som viser historikk, prognose og intervaller. Bruk syntetiske data med kjent sesong og trend.
2. Legg til ett beslutningspunkt i trinn 2, for eksempel produksjon vs. lager med en enkel regel for sikkerhetslager, og eventuelt LLM-forklaring med mock-modus. Flytt LightGBM, Prophet, SHAP, optimering, outsourcing-analyse, godkjenningsflyt og MRP-eksport til senere versjoner.

## Hvorfor product brief er viktig for mappen

Product brief er utgangspunktet for PRD, arkitektur, stories og til slutt koden. Del 1 av mappen vurderes blant annet på om sensor kan følge en sporbar vei fra plan til ferdig app. Den vurderes også på om appen gjør det dere har beskrevet, om den er testet, om den er godt designet, og om den kan kjøres etter README. Et uklart, for stort eller for lite brief gjør alt dette vanskeligere senere. Det er mye enklere å rette nå enn sent i semesteret.

## 1. Gjennomgang av briefens deler

| Del av brief | Status | Kommentar |
|---|---|---|
| Executive Summary – er det klart hva appen er, og hvilket problem den løser? | OK | Klart hva PROGNOS er, og hvorfor prognosekvalitet er viktig for MRP. |
| The Problem – er problemet konkret, med reelle situasjoner og brukere? | OK | Fem konkrete svakheter og tydelige konsekvenser. |
| The Solution – beskriver løsningen brukeropplevelsen, ikke bare teknologi? | Endre | Hovedfunksjonene og den tekniske delen beskriver hva systemet gjør og hvilke biblioteker det bruker, men ikke hva planleggeren gjør steg for steg. Beskriv én kjerneflyt fra brukerens perspektiv, og flytt teknologivalgene til arkitekturdokumentet. |
| What Makes This Different – er vurderingen ærlig og realistisk? | Juster | Mangler som egen del. Si ærlig hvordan PROGNOS skiller seg fra eksisterende verktøy for etterspørselsplanlegging, og at en studentprototype demonstrerer et prinsipp. |
| Who This Serves – er primærbrukerne tydelige, og vet vi hva de trenger? | Juster | Seks roller er for mange for v1. Velg etterspørselsplanleggeren som primærbruker. |
| Success Criteria – kan kriteriene faktisk sjekkes eller testes? | Endre | Forretningsmålene kan ikke måles i emnet. Legg til funksjonelle og testbare kriterier, og behold «modellen slår baseline i backtest» som det viktigste kvalitetskriteriet. |
| Scope – er det klart hva som er med i første versjon, og hva som ikke er det? | Endre | Det er klart hva som ikke er med, men alt annet ser ut til å være med i v1. Del i v1, senere trinn og visjon. |
| Vision – henger visjonen sammen med resten uten å blåse opp omfanget? | Juster | Mangler som egen del. Når v1 er kuttet, kan mye av dagens funksjonsliste flyttes til en visjon. |

## 2. Utgangspunkt for del 1 av mappen

Punktene følger kriteriene i sensorveiledningen for del 1. Vektene i parentes viser hvor mye hvert kriterium teller i del 1.

| Kriterium i del 1 | Hva briefen bør legge til rette for | Status | Kommentar |
|---|---|---|---|
| **1. Prosess og KI-styring** (30 %) | Brief som er presis nok til at PRD og stories kan bygges direkte på den, slik at krav kan spores fra brief til kode. | Endre | Uten avgrensning blir det vanskelig å spore krav fra brief til kode. En kort v1 gir en tydelig vei. |
| **2. Funksjonalitet og omfang** (20 %) | Realistisk omfang for gruppen og semesteret: en tydelig kjerneflyt som kan bli ferdig og stabil, og nok innhold til å vise reell funksjonalitet. | Endre | Risiko for mange halvferdige funksjoner. Prognose med scenarioer og backtest gir nok reell funksjonalitet. |
| **3. Kvalitetssikring og testing** (15 %) | Suksesskriterier og funksjoner som er konkrete nok til å bli testtilfeller. | Juster | Backtest mot baseline er et godt utgangspunkt. Lag fasitserier og funksjonelle kriterier i tillegg. |
| **4. Design og brukeropplevelse** (10 %) | Tydelige brukere og brukssituasjoner som designet kan bygges rundt, gjerne med de viktigste skjermbildene eller flytene skissert. | Juster | Dashbordet er nevnt, men uten brukssituasjon. Skisser prognosevisningen med intervaller og scenariosammenligningen. |
| **5. Kodekvalitet og arkitektur** (10 %) | Teknologivalg som er begrunnet og ikke mer komplekse enn appen trenger. | Endre | Mange ML- og optimeringsbiblioteker er mer enn v1 trenger. Start med én modell og baseline. |
| **6. README og kjørbarhet** (10 %) | Løsning som andre kan kjøre lokalt uten betalte kontoer, og uten tilgang til gruppens egne tjenester og nøkler. | Juster | Bruk SQLite og mock-forklaringer, slik at sensor kan kjøre appen uten nøkkel og databaseserver. |
| **7. Ryddighet i repoet** (5 %) | En plan for hvor hemmeligheter, testdata og dokumentasjon skal ligge. | Juster | Planlegg `.env.example` for API-nøkkelen og en egen mappe for syntetiske testdata. |

## 3. Neste steg for gruppen

1. Skriv om Scope med en tydelig v1 (CSV-import, én modell mot baseline, tre scenarioer, backtest, dashbord), og flytt resten til senere trinn og en visjon.
2. Lag et syntetisk datasett med kjent sesong og trend, og legg til funksjonelle suksesskriterier som kan testes mot det.
3. Velg etterspørselsplanleggeren som primærbruker, beskriv hennes kjerneflyt i 4–5 steg, og gå deretter videre til PRD.

Oppdater product brief i repoet når dere har gjort endringene, slik at historikken viser hvordan planen utviklet seg. Det er en del av prosessen sensor ser etter.
