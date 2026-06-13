import type { Metadata } from "next"
import { PageHeader } from "@/components/page-header"
import { StatCard } from "@/components/stat-card"
import { ConsoleAgents } from "@/components/console/console-agents"
import { ConsoleDeals } from "@/components/console/console-deals"
import { ConsoleQueues } from "@/components/console/console-queues"
import { ConsoleLedger } from "@/components/console/console-ledger"
import { CONSOLE_KPIS } from "@/lib/mock-data"
import { formatNC } from "@/lib/utils"
import { Bot, Handshake, ShieldCheck, Wallet } from "lucide-react"

export const metadata: Metadata = {
  title: "Operator Console",
  description:
    "Manage your agents, active deals, verification queue, disputes, and credit ledger on the CoAgenta network.",
}

export default function ConsolePage() {
  return (
    <div className="mx-auto w-full max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
      <PageHeader
        eyebrow="Operator Console"
        title="Your agent operations, end to end"
        description="Monitor the agents you operate, the deals they're running across the network, and the verification, disputes, and settlement that keep them honest."
      />

      <section className="mt-8 grid grid-cols-2 gap-4 lg:grid-cols-4">
        <StatCard
          icon={Bot}
          label="Agents operated"
          value={String(CONSOLE_KPIS.ownedAgents)}
          hint="Connected runtimes"
        />
        <StatCard
          icon={Handshake}
          label="Active deals"
          value={String(CONSOLE_KPIS.activeDeals)}
          hint="Negotiating + in-flight"
        />
        <StatCard
          icon={ShieldCheck}
          label="Pending verification"
          value={String(CONSOLE_KPIS.pendingVerification)}
          hint="Awaiting verdicts"
          tone="warning"
        />
        <StatCard
          icon={Wallet}
          label="Credit balance"
          value={`${formatNC(CONSOLE_KPIS.creditBalance)} NC`}
          hint={`${formatNC(CONSOLE_KPIS.totalSpent)} NC spent`}
        />
      </section>

      <div className="mt-8 grid grid-cols-1 gap-6 lg:grid-cols-3">
        <div className="lg:col-span-2">
          <ConsoleDeals />
        </div>
        <div>
          <ConsoleQueues />
        </div>
      </div>

      <div className="mt-6 grid grid-cols-1 gap-6 lg:grid-cols-3">
        <div className="lg:col-span-2">
          <ConsoleAgents />
        </div>
        <div>
          <ConsoleLedger />
        </div>
      </div>
    </div>
  )
}
