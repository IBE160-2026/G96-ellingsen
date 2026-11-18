import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "PROGNOS",
  description: "Prognoseverktøy for etterspørselsplanleggeren.",
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html lang="nb" className="h-full antialiased">
      <body className="min-h-full flex flex-col">{children}</body>
    </html>
  );
}
