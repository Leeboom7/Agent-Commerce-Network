import type { Metadata } from "next"
import { notFound } from "next/navigation"
import Link from "next/link"
import {
  AGENTS,
  getAgent,
  getServicesForAgent,
  getDealsForAgent,
} from "@/lib/mock-data"
import { formatNC } from "@/lib/utils"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { ReputationGauge } from "@/components/reputation-gauge"
import { ReputationChart } from "@/components/reputation-chart"
import { ConnectorHealthDot, DealStatusBadge } from "@/components/status-badges"
import { ServiceCard } from "@/components/service-card"
import {
  ArrowLeft,
  CheckCircle2,
  Coins,
  Cpu,
  Gauge,
  MapPin,
} from "lucide-react"

export function generateStaticParams() {
  return AGENTS.map((a) => ({ id: a.id }))
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ id: string }>
}): Promise<Metadata> {
  const { id } = await params
  const agent = getAgent(id)
  if (!agent) return { title: "Agent not found" }
  return {
    title: `${agent.name} — ${agent.role}`,
    description: agent.summary,
  }
}

export default async function AgentProfilePage({
  params,
}: {
  params: Promise<{ id: string }>
}) {
  const { id } = await params
  const agent = getAgent(id)
  if (!agent) notFound()

  const services = getServicesForAgent(agent.id)
  const deals = getDealsForAgent(agent.id)

  return (
    <div className="mx-auto w-full max-w-6xl px-4 py-8 sm:px-6 lg:px-8">
      <Link
        href="/discover"
        className="inline-flex items-center gap-1.5 text-sm text-muted-foreground hover:text-foreground"
      >
        <ArrowLeft className="h-4 w-4" />
        Back to network
      </Link>

      <div className="mt-6 grid grid-cols-1 gap-6 lg:grid-cols-3">
        {/* Identity */}
        <div className="lg:col-span-2">
          <div className="rounded-xl border border-border bg-card p-6">
            <div className="flex flex-wrap items-start justify-between gap-4">
              <div className="flex items-center gap-4">
                <div className="flex h-14 w-14 items-center justify-center rounded-xl bg-primary/10 font-mono text-lg font-semibold text-primary">
                  {agent.name.slice(0, 2).toUpperCase()}
                </div>
                <div>
                  <div className="flex items-center gap-2">
                    <h1 className="text-xl font-semibold">{agent.name}</h1>
                    <ConnectorHealthDot status={agent.status} />
                  </div>
                  <p className="font-mono text-xs text-muted-foreground">{agent.handle}</p>
                  <p className="mt-0.5 text-sm text-muted-foreground">{agent.role}</p>
                </div>
              </div>
              <Button>
                <Coins className="h-4 w-4" />
                Hire this agent
              </Button>
            </div>

            <p className="mt-4 text-pretty text-sm leading-relaxed text-muted-foreground">
              {agent.summary}
            </p>

            <div className="mt-5 grid grid-cols-2 gap-3 sm:grid-cols-4">
              <Stat icon={Cpu} label="Connector" value={agent.connector} />
              <Stat icon={MapPin} label="Runtime" value={agent.runtimeRegion} />
              <Stat
                icon={Gauge}
                label="Success rate"
                value={`${Math.round(agent.successRate * 100)}%`}
              />
              <Stat icon={Coins} label="Earned" value={`${formatNC(agent.totalEarned)} NC`} />
            </div>

            <div className="mt-5 flex flex-wrap gap-1.5">
              {agent.capabilities.map((c) => (
                <Badge key={c.serviceType + c.label} variant="muted" className="font-mono text-[11px]">
                  {c.label}
                </Badge>
              ))}
            </div>
          </div>

          {/* Reputation history */}
          <div className="mt-6 rounded-xl border border-border bg-card p-6">
            <h2 className="text-sm font-semibold">Reputation history</h2>
            <p className="text-xs text-muted-foreground">
              Time-weighted score derived from settled deals and verification outcomes
            </p>
            <div className="mt-4">
              <ReputationChart data={agent.reputationHistory} />
            </div>
          </div>
        </div>

        {/* Reputation gauge sidebar */}
        <div>
          <div className="flex flex-col items-center rounded-xl border border-border bg-card p-6">
            <ReputationGauge score={agent.reputation} size={120} />
            <p className="mt-3 text-sm font-medium">Network reputation</p>
            <p className="text-xs text-muted-foreground">
              {agent.totalDeals} deals · {agent.pricingModel} pricing
            </p>
            <div className="mt-4 w-full border-t border-border pt-4">
              <div className="flex items-center justify-between text-sm">
                <span className="text-muted-foreground">Base price</span>
                <span className="font-mono font-semibold">
                  {agent.basePrice === 0 ? "free" : `${formatNC(agent.basePrice)} NC`}
                </span>
              </div>
              <div className="mt-2 flex items-center justify-between text-sm">
                <span className="text-muted-foreground">Response ETA</span>
                <span className="font-mono">{agent.responseEta}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Services */}
      {services.length > 0 && (
        <section className="mt-10">
          <h2 className="text-lg font-semibold">Services offered</h2>
          <div className="mt-4 grid grid-cols-1 gap-4 md:grid-cols-2">
            {services.map((s) => (
              <ServiceCard key={s.id} service={s} />
            ))}
          </div>
        </section>
      )}

      {/* Deal history */}
      {deals.length > 0 && (
        <section className="mt-10">
          <h2 className="text-lg font-semibold">Deal history</h2>
          <div className="mt-4 overflow-hidden rounded-xl border border-border bg-card">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-border text-left text-xs text-muted-foreground">
                  <th className="px-5 py-2.5 font-medium">Deal</th>
                  <th className="px-3 py-2.5 font-medium">Status</th>
                  <th className="px-3 py-2.5 text-right font-medium">Net</th>
                </tr>
              </thead>
              <tbody>
                {deals.map((d) => (
                  <tr key={d.id} className="border-b border-border/60 last:border-0 hover:bg-secondary/40">
                    <td className="px-5 py-3">
                      <Link href={`/deals/${d.id}`} className="font-medium hover:text-primary">
                        {d.title}
                      </Link>
                    </td>
                    <td className="px-3 py-3">
                      <DealStatusBadge status={d.status} />
                    </td>
                    <td className="px-3 py-3 text-right font-mono">{formatNC(d.netPayment)} NC</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>
      )}
    </div>
  )
}

function Stat({
  icon: Icon,
  label,
  value,
}: {
  icon: typeof CheckCircle2
  label: string
  value: string
}) {
  return (
    <div className="rounded-lg border border-border bg-background p-3">
      <span className="inline-flex items-center gap-1.5 text-xs text-muted-foreground">
        <Icon className="h-3.5 w-3.5" />
        {label}
      </span>
      <p className="mt-1 truncate text-sm font-medium">{value}</p>
    </div>
  )
}
