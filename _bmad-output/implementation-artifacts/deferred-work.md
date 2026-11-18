- source_spec: `_bmad-output/implementation-artifacts/spec-1-2-frontend-skjelett-med-proxy-til-backend.md`
  summary: `npm test` (vitest run) i `frontend/` feiler med «Cannot read properties of undefined (reading 'config')» når arbeidsmappa har liten stasjonsbokstav (`c:\...`, typisk i cmd og VS Code-terminalen).
  evidence: Reprodusert 2026-11-18. Fra `C:/IBE160/...` gir den 10/10 grønt, fra `c:\IBE160\...` i cmd feiler den før noen test samles. Feilen ligger i Vitest/Vite og ikke i koden. Mulige tiltak: beskrive det i README (Story 1.3), eller normalisere `root` i `vitest.config.ts`.
