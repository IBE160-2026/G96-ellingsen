import { readdirSync, statSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";
import { expect, test } from "@playwright/test";

// AD-14: e2e skal bruke en midlertidig databasefil, aldri backend/data/prognos.db.
test("e2e-backenden bruker midlertidig database, ikke utviklerens", () => {
  const mappe = join(tmpdir(), "prognos-e2e");
  const filer = readdirSync(mappe)
    .filter((navn) => navn.endsWith(".db"))
    .map((navn) => statSync(join(mappe, navn)));
  expect(filer.length).toBeGreaterThan(0);
  const nyeste = filer.reduce((a, b) => (b.birthtimeMs > a.birthtimeMs ? b : a));

  const utviklerDb = resolve(import.meta.dirname, "../../backend/data/prognos.db");
  let utviklerMtime: number | undefined;
  try {
    utviklerMtime = statSync(utviklerDb).mtimeMs;
  } catch {
    utviklerMtime = undefined;
  }
  if (utviklerMtime !== undefined) {
    expect(utviklerMtime).toBeLessThan(nyeste.birthtimeMs);
  }
});
