import { readdirSync, readFileSync, statSync } from "node:fs";
import { join, resolve } from "node:path";
import { describe, expect, it } from "vitest";

import nextConfig from "../next.config";
import playwrightConfig from "../playwright.config";

const rot = resolve(import.meta.dirname, "..");
const pakke = JSON.parse(readFileSync(join(rot, "package.json"), "utf8"));

function filerUnder(mappe: string): string[] {
  let stier: string[];
  try {
    stier = readdirSync(mappe);
  } catch {
    return [];
  }
  return stier.flatMap((navn) => {
    const sti = join(mappe, navn);
    if (statSync(sti).isDirectory()) return filerUnder(sti);
    return [sti];
  });
}

describe("frontend-oppsett", () => {
  it("låser next til eksakt 16.4.6", () => {
    expect(pakke.dependencies.next).toBe("16.4.6");
  });

  it("låser alle andre pakker på minor med ~", () => {
    const pakker: Record<string, string> = {
      ...pakke.dependencies,
      ...pakke.devDependencies,
    };
    const ulaast = Object.entries(pakker).filter(
      ([navn, versjon]) => navn !== "next" && !versjon.startsWith("~"),
    );
    expect(ulaast).toEqual([]);
  });

  it("sender /api/* videre til backend på 127.0.0.1:8000", async () => {
    expect(nextConfig.rewrites).toBeTypeOf("function");
    const regler = await nextConfig.rewrites!();
    expect(regler).toEqual([
      {
        source: "/api/:path*",
        destination: "http://127.0.0.1:8000/api/:path*",
      },
    ]);
  });

  it("har proxyfrist og agentUpgrade av (AD-11)", () => {
    expect(nextConfig.experimental).toMatchObject({
      proxyTimeout: 130000,
      agentUpgrade: false,
    });
  });

  it("Playwright gjenbruker aldri en kjørende server og bruker temp-database (AD-14)", () => {
    const servere = [playwrightConfig.webServer].flat();
    expect(servere).toHaveLength(2);
    for (const server of servere) {
      expect(server?.reuseExistingServer).toBe(false);
    }
    const backend = servere.find((s) => s?.command.includes("prognos"));
    expect(backend?.command).toContain("prognos-e2e");
    expect(backend?.command).not.toMatch(/data[\\/]prognos\.db/);
  });

  it("hindrer next dev i å skrive AGENTS.md fra malen", () => {
    expect(nextConfig.agentRules).toBe(false);
  });

  const filer = ["app","components", "lib"].flatMap((mappe) =>
    filerUnder(join(rot, mappe)),
  );

  it("finner appfilene som skal sjekkes", () => {
    expect(filer.length).toBeGreaterThan(0);
  });

  it.each(["next/font/google", "process.env", "http://", "https://"])(
    "ingen appfil inneholder %s",
    (forbudt) => {
      const treff = filer.filter((fil) =>
        readFileSync(fil, "utf8").includes(forbudt),
      );
      expect(treff).toEqual([]);
    },
  );

  it.each([
    "next.config.ts",
    "playwright.config.ts",
    "vitest.config.ts",
    "postcss.config.mjs",
  ])("%s leser ikke process.env", (fil) => {
    expect(readFileSync(join(rot, fil), "utf8")).not.toContain("process.env");
  });
});
