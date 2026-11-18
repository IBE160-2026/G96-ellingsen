import { expect, test } from "@playwright/test";

test("helsesjekken svarer ok gjennom proxyen", async ({ request }) => {
  const svar = await request.get("/api/health");
  expect(svar.status()).toBe(200);
  expect(await svar.json()).toEqual({ status: "ok" });
});

test("ukjent API-sti gir backendens norske 404 uendret", async ({ request }) => {
  const svar = await request.get("/api/finnes-ikke");
  expect(svar.status()).toBe(404);
  const kropp = await svar.json();
  expect(Object.keys(kropp)).toEqual(["detail"]);
  expect(typeof kropp.detail).toBe("string");
  expect(kropp.detail.length).toBeGreaterThan(0);

  const direkte = await request.get("http://127.0.0.1:8000/api/finnes-ikke");
  expect(direkte.status()).toBe(404);
  expect(await svar.text()).toBe(await direkte.text());
  expect(svar.headers()["content-type"]).toBe(direkte.headers()["content-type"]);
});
