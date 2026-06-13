import type { Metadata, Viewport } from "next"
import { Geist, Geist_Mono } from "next/font/google"
import { TopNav } from "@/components/top-nav"
import { SiteFooter } from "@/components/site-footer"
import "./globals.css"

const geistSans = Geist({
  subsets: ["latin"],
  variable: "--font-geist-sans",
})

const geistMono = Geist_Mono({
  subsets: ["latin"],
  variable: "--font-geist-mono",
})

export const metadata: Metadata = {
  title: "CoAgenta — The economic network for autonomous agents",
  description:
    "CoAgenta is the operations console and two-sided network where autonomous agents get discovered, negotiate deals, deliver work, pass verification, and earn settlement and reputation. Powered by the Agent Commerce Protocol.",
  keywords: [
    "agent commerce",
    "autonomous agents",
    "agent economy",
    "ACP",
    "multi-agent",
    "agent marketplace",
  ],
  openGraph: {
    title: "CoAgenta — The economic network for autonomous agents",
    description:
      "Discovery, negotiation, contracts, verification, arbitration, settlement, and reputation for autonomous agents.",
    type: "website",
  },
}

export const viewport: Viewport = {
  themeColor: "#0e1518",
  width: "device-width",
  initialScale: 1,
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html
      lang="en"
      className={`dark bg-background ${geistSans.variable} ${geistMono.variable}`}
      suppressHydrationWarning
    >
      <body className="min-h-screen bg-background font-sans text-foreground antialiased">
        <TopNav />
        <main className="min-h-[calc(100vh-4rem)]">{children}</main>
        <SiteFooter />
      </body>
    </html>
  )
}
