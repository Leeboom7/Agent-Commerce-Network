import type { Metadata } from "next"
import { notFound } from "next/navigation"
import Link from "next/link"
import { DEALS, getAgent, getDeal } from "@/lib/mock-data"
import { formatNC } from "@/lib/utils"
import { DealStatusBadge } from "@/components/status-badges"
import { DealTimeline } from "@/components/deal-timeline"
import { ArrowLeft, ArrowRight, CheckCircle2 } from "lucide-react"

export function generateStaticParams() {
  return DEALS.map((d) => ({ id: d.id }))
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ id: string }>
}): Promise<Metadata> {
  const { id } = await params
  const deal = getDeal(id)
  if (!deal) return { title: "Deal not found" }
  return { title: deal.title, description: `Deal lifecycle for ${deal.title}` }
}

export default async function DealWorkspacePage({
  params,
}: {
  params: Promise<{ id: string }>
}) {
  const { id } = await params
  const deal = getDeal(id)
  if (!deal) notFound()

  const buyer = getAgent(deal.buyerId)
  const seller = getAgent(deal.sellerId)

  return (
    <div className="mx-auto w-full max-w-6xl px-4 py-8 sm:px-6 lg:px-8">
      <Link
        href="/console"
        className="inline-flex items-center gap-1.5 text-sm text-muted-foreground hover:text-foreground"
      >
        <ArrowLeft className="h-4 w-4" />
        Back to console
      </Link>

      <div className="mt-6 flex flex-wrap items-start justify-between gap-4">
        <div>
          <div className="flex items-center gap-3">
            <h1 className="text-xl font-semibold sm:text-2xl">{deal.title}</h1>
            <DealStatusBadge status={deal.status} />
          </div>
          <p className="mt-1 font-mono text-xs text-muted-foreground">{deal.id}</p>
        </div>
      </div>

      <div className="mt-6 grid grid-cols-1 gap-6 lg:grid-cols-3">
        {/* Timeline */}
        <div className="lg:col-span-2">
          <div className="rounded-xl border border-border bg-card p-6">
            <h2 className="mb-5 text-sm font-semibold">Deal lifecycle</h2>
            <DealTimeline nodes={deal.timeline} />
          </div>
        </div>

        {/* Sidebar */}
        <div className="flex flex-col gap-6">
          <div className="rounded-xl border border-border bg-card p-5">
            <h2 className="text-sm font-semibold">Counterparties</h2>
            <div className="mt-3 flex items-center justify-between gap-2 text-sm">
              <Party label="Buyer" name={buyer?.name} id={buyer?.id} />
              <ArrowRight className="h-4 w-4 shrink-0 text-muted-foreground" />
              <Party label="Seller" name={seller?.name} id={seller?.id} align="right" />
            </div>
          </div>

          <div className="rounded-xl border border-border bg-card p-5">
            <h2 className="text-sm font-semibold">Contract terms</h2>
            <dl className="mt-3 space-y-2 text-sm">
              <Row label="Agreed price" value={`${formatNC(deal.price)} NC`} />
              {deal.penalty > 0 && (
                <Row label="Penalty applied" value={`-${formatNC(deal.penalty)} NC`} danger />
              )}
              <Row label="Net payment" value={`${formatNC(deal.netPayment)} NC`} strong />
              <Row label="Negotiation rounds" value={String(deal.rounds)} />
              <Row label="Deadline" value={deal.deadline} />
            </dl>
          </div>

          <div className="rounded-xl border border-border bg-card p-5">
            <h2 className="text-sm font-semibold">Acceptance criteria</h2>
            <ul className="mt-3 space-y-2">
              {deal.acceptanceCriteria.map((c) => (
                <li key={c} className="flex items-start gap-2 text-sm text-muted-foreground">
                  <CheckCircle2 className="mt-0.5 h-3.5 w-3.5 shrink-0 text-success" />
                  {c}
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>
    </div>
  )
}

function Party({
  label,
  name,
  id,
  align = "left",
}: {
  label: string
  name?: string
  id?: string
  align?: "left" | "right"
}) {
  return (
    <div className={align === "right" ? "text-right" : ""}>
      <p className="text-xs text-muted-foreground">{label}</p>
      {id ? (
        <Link href={`/agents/${id}`} className="text-sm font-medium hover:text-primary">
          {name}
        </Link>
      ) : (
        <span className="text-sm font-medium">{name}</span>
      )}
    </div>
  )
}

function Row({
  label,
  value,
  strong,
  danger,
}: {
  label: string
  value: string
  strong?: boolean
  danger?: boolean
}) {
  return (
    <div className="flex items-center justify-between gap-3">
      <dt className="text-muted-foreground">{label}</dt>
      <dd
        className={
          danger
            ? "font-mono text-destructive"
            : strong
              ? "font-mono font-semibold text-foreground"
              : "font-mono text-foreground"
        }
      >
        {value}
      </dd>
    </div>
  )
}
