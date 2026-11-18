import { tmpdir } from "node:os";
import { join } from "node:path";
import { defineConfig, devices } from "@playwright/test";

// AD-14: e2e kjører mot ekte backend på en midlertidig databasefil, aldri mot
// backend/data/prognos.db. Stien regnes ut på nytt i hver worker, men bare
// hovedprosessen starter webServer. Backend lager selv mappen og fila.
const testDb = join(tmpdir(), "prognos-e2e", `${Date.now()}.db`);

export default defineConfig({
  testDir: "./e2e",
  fullyParallel: true,
  reporter: "list",
  use: {
    baseURL: "http://localhost:3000",
  },
  projects: [{ name: "chromium", use: { ...devices["Desktop Chrome"] } }],
  webServer: [
    {
      command: `uv run python -m prognos --db "${testDb}" --port 8000`,
      cwd: "../backend",
      url: "http://127.0.0.1:8000/api/health",
      reuseExistingServer: false,
      timeout: 120_000,
    },
    {
      command: "npm run dev -- --port 3000",
      url: "http://localhost:3000",
      reuseExistingServer: false,
      timeout: 120_000,
    },
  ],
});
