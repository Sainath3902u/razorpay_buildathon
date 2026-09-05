import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "RevenueOS — AI Revenue Intelligence",
  description:
    "AI-powered revenue intelligence and opportunity detection",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}