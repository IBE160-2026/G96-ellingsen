## Sesjonslogg

Når en oppgave eller økt avsluttes, før sluttoppsummeringen, bruk `sesjonslogg`-skillen: dokumenter Oppgave + Plan + Resultat + åpne punkter i `.logs/<bruker>/`, og før åpne punkter i `.logs/<bruker>/issues.md`. Skillen committer loggfila lokalt; push gjør du selv. Gruppens egne regler for commit og språk gjelder foran dette.

## Regler for implementering (fra retroen for Epic 1)

Kilde: [epic-1-retro-2026-11-18.md](_bmad-output/implementation-artifacts/epic-1-retro-2026-11-18.md).

- **R1 – Ingen innstillinger uten bestilling.** Hver ny linje i konfig, avhengigheter eller flagg skal kunne vises til i speccen eller i verktøyets egen mal. Det gjelder også verktøy som endrer repoet på egen hånd (for eksempel `next dev`, som skrev `AGENTS.md`). Reviewen spør for hver slik linje: «Hvem ba om denne?»
- **R2 – En test teller først når den er sett feile.** Før en akseptkriterietest regnes som bevis, skal den ha vært rød: brekk betingelsen eller bytt inn feil data. En sjekk som ikke kan slå ut, som `git status` mot en gitignored fil, er ikke bevis. Fasittester skal sammenligne med uavhengige konstanter, ikke med kodens egen output.
- **R3 – Kommandoer verifiseres i PowerShell.** README anbefaler PowerShell. Nye kommandoer i en spec eller README kjøres der før storyen settes til `done`.
- **Subagenter i `bmad-build`.** `bmad-build` bruker alltid subagenter til å kompilere konteksten og til uavhengig kodegjennomgang, uten å spørre først.
