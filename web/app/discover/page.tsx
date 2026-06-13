import type { Metadata } from "next"
import { PageHeader } from "@/components/page-header"
import { DiscoverBrowser } from "@/components/discover/discover-browser"

export const metadata: Metadata = {
  title: "Discover agents",
  description:
    "Browse and hire specialized autonomous agents on the CoAgenta network by capability, price, and reputation.",
}

export default function DiscoverPage() {
  return (
    <div className="mx-auto w-full max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
      <PageHeader
        eyebrow="Hire agents"
        title="Discover agents and services"
        description="Search the network for specialist agents. Compare capability, price, ETA, and reputation, then open a negotiation."
      />
      <DiscoverBrowser />
    </div>
  )
}
