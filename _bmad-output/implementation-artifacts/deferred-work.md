- source_spec: `_bmad-output/implementation-artifacts/spec-1-2-frontend-skjelett-med-proxy-til-backend.md`
  summary: `npm test` (vitest run) i `frontend/` feiler med «Cannot read properties of undefined (reading 'config')» når arbeidsmappa har liten stasjonsbokstav (`c:\...`, typisk i cmd og VS Code-terminalen).
  evidence: Reprodusert 2026-11-18. Fra `C:/IBE160/...` gir den 10/10 grønt, fra `c:\IBE160\...` i cmd feiler den før noen test samles. Feilen ligger i Vitest/Vite og ikke i koden. Mulige tiltak: beskrive det i README (Story 1.3), eller normalisere `root` i `vitest.config.ts`.
  resolved: 2026-11-18. Story 1.3 beskriver det i README (PowerShell anbefales, med rundganger for cmd og Git Bash). Brukeren valgte bort `scripts/test.mjs`.
- source_spec: `_bmad-output/implementation-artifacts/spec-1-3-readme-repohygiene-og-kontroll-av-oppstarten.md`
  summary: Den manuelle offline-kontrollen i F12 og NFR-1 er ikke gjort. Den skal starte backend og frontend etter README med nettverket koblet fra og sjekke `/api/health` gjennom frontend.
  evidence: Kontrollen med nett er gjort 2026-11-18 og var grønn. Offline-delen krever at brukeren kobler fra nettverket selv. Resultatet føres i sesjonsloggen med dato og maskin.
  resolved: 2026-11-18. Kontrollen uten nett er gjort på utviklerens PC og var grønn (helse gjennom proxyen, forsiden, 32 + 15 tester). Ført i `.logs/mathias-ellingsen/987-2026-11-18-13-43-05-story-1-3-readme-repohygiene.md`.
