import Link from "next/link"
import { ArrowUpRight, Coins } from "lucide-react"
import type { Agent } from "@/lib/types"
import { Badge } from "./ui/badge"
import { ConnectorHealthDot } from "./status-badges"
import { ReputationScore } from "./reputation-gauge"

export function AgentCard({ agent }: { agent: Agent }) {
  return (
    <Link
      href={`/agents/${agent.id}`}
      className="group flex flex-col rounded-xl border border-border bg-card p-5 transition-colors hover:border-primary/40"
    >
      <div className="flex items-start justify-between gap-3">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary/10 font-mono text-sm font-semibold text-primary">
            {agent.name.slice(0, 2).toUpperCase()}
          </div>
          <div>
            <h3 className="text-sm font-semibold leading-tight">{agent.name}</h3>
            <p className="text-xs text-muted-foreground">{agent.role}</p>
          </div>
        </div>
        <ArrowUpRight className="h-4 w-4 text-muted-foreground transition-colors group-hover:text-primary" />
      </div>

      <p className="mt-3 text-sm leading-relaxed text-muted-foreground line-clamp-2">
        {agent.summary}
      </p>

      <div className="mt-4 flex flex-wrap gap-1.5">
        {agent.capabilities.slice(0, 3).map((c) => (
          <Badge key={c.serviceType + c.label} variant="muted" className="font-mono text-[11px]">
            {c.label}
          </Badge>
        ))}
      </div>

      <div className="mt-5 flex items-center justify-between border-t border-border pt-4">
        <ReputationScore score={agent.reputation} />
        <div className="flex items-center gap-3 text-xs text-muted-foreground">
          <span className="inline-flex items-center gap-1 font-mono">
            <Coins className="h-3.5 w-3.5 text-primary" />
            {agent.totalDeals} deals
          </span>
          <ConnectorHealthDot status={agent.status} />
        </div>
      </div>
    </Link>
  )
}
