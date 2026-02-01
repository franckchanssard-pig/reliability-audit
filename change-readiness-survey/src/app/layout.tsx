import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Change Readiness Survey — Pigment",
  description:
    "Assess your organization's readiness for change with this quick 15-question survey.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased">{children}</body>
    </html>
  );
}
