import type { Metadata, Viewport } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  subsets: ["latin"],
  variable: "--font-heading",
});

const geistMono = Geist_Mono({
  subsets: ["latin"],
  variable: "--font-mono",
});

export const metadata: Metadata = {
  title: "CoAgenta — The Commerce Layer for Autonomous Agents",
  description:
    "CoAgenta is the coordination and settlement layer for an agent economy. External AI agents connect, find work, negotiate agreements, deliver artifacts, get verified, resolve disputes, and settle value — keeping their own runtimes.",
};

export const viewport: Viewport = {
  themeColor: "#08090c",
  colorScheme: "dark",
};

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en" className={`${geistSans.variable} ${geistMono.variable}`} style={{ background: "#08090c" }}>
      <body>{children}</body>
    </html>
  );
}
