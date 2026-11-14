# Revisjon av product brief

## 2026-11-14 kl. 17:11 — Mathias Ellingsen

### Oppgave
Revidere `PRODUCT_BRIEF.md` etter tilbakemelding om at omfanget var for stort: velge én primærbruker, bytte forretningsmål ut med testbare funksjonelle kriterier og avgrense v1 til en tydelig kjerneflyt, med resten flyttet til senere trinn og en visjon. Deretter committe, pushe og merge til `main`.

### Plan
- Tre runder med omskriving av briefen, én per tilbakemelding.
- Commit på grenen `revider-product-brief`, push, og deretter merge inn i `main`.

### Resultat
- `PRODUCT_BRIEF.md` er skrevet om:
  - Primærbruker er etterspørselsplanleggeren (persona «Kari»).
  - Nytt avsnitt 4 Omfang: v1 (CSV-import, ETS mot sesongnaiv baseline, tre scenarioer P10/P50/P90, backtest med WAPE, Streamlit-dashbord, syntetiske testdata), trinn 2 (produksjon vs. lager med sikkerhetslager = Σ(P90 − P50) over ledetiden, valgfri LLM-forklaring med mock-modus), senere trinn, visjon og det som er utenfor omfang uansett.
  - Suksesskriterier F1–F10 (v1) og B1–B3, L1 (trinn 2).
- Commit `6da487f` på `revider-product-brief`. `origin/main` hadde fått 4 nye commits fra Bård (tilbakemelding, sesjonslogg-skill, `technology.md`), og disse ble merget inn uten konflikt. Merge-commit `8aacd59` er pushet til `main`.
- Git-identitet er satt lokalt i repoet (`user.name`/`user.email`), siden den manglet.

### Åpne punkter
- Det syntetiske testdatasettet og generatoren finnes ikke ennå. Det trengs før F7–F9 kan testes.
- Valgte terskler må vurderes av gruppen: 24 måneders minimumshistorikk, 6 måneders horisont og 65–95 % intervalldekning (F8).
- `.docs/planning-artifacts/architecture/technology.md` beskriver FastAPI, Next.js og PostgreSQL. Den reviderte briefen bruker Streamlit uten database i v1, så dokumentene må samkjøres.
