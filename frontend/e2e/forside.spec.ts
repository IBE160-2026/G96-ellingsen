import { expect, test } from "@playwright/test";

test("forsiden er norsk og viser ordmerket PROGNOS", async ({ page }) => {
  await page.goto("/");
  await expect(page.locator("html")).toHaveAttribute("lang", "nb");
  await expect(page).toHaveTitle("PROGNOS");
  await expect(page.getByRole("heading", { name: "PROGNOS" })).toBeVisible();
});
