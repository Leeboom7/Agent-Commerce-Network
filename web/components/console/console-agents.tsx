import Link from "next/link"
import { AGENTS } from "@/lib/mock-data"
import { ConnectorHealthDot } from "@/components/status-badges"
import { ReputationScore } from "@/components/reputation-gauge"
import { Badge } from "@/components/ui/badge"

export function ConsoleAgents() {
  const owned = AGENTS.filter((a) => a.owned)
  // show owned first, then a couple connected externals for context
  const externals = AGENTS.filter((a) => !a.owned).slice(0, 2)
  const rows = [...owned, ...externals]

  return (
    <div className="rounded-xl border border-border bg-card">
      <div className="flex items-center justify-between border-b border-border px-5 py-4">
        <div>
          <h2 className="text-sm font-semibold">Your agents</h2>
          <p className="text-xs text-muted-foreground">
            Connector health and reputation
          </p>
        </div>
        <Link href="/discover" className="text-xs font-medium text-primary hover:underline">
          Browse network
        </Link>
      </div>

      <ul className="divide-y divide-border/60">
        {rows.map((agent) => (
          <li key={agent.id} className="flex items-center gap-4 px-5 py-3.5">
            <ConnectorHealthDot status={agent.status} />
            <div className="min-w-0 flex-1">
              <Link
                href={`/agents/${agent.id}`}
                className="text-sm font-medium hover:text-primary"
              >
                {agent.name}
              </Link>
              <p className="truncate text-xs text-muted-foreground">{agent.role}</p>
            </div>
            <Badge variant="outline" className="hidden sm:inline-flex">
              {agent.connector}
            </Badge>
            {agent.owned ? (
              <Badge variant="info">operated</Badge>
            ) : (
              <Badge variant="muted">external</Badge>
            )}
            <ReputationScore score={agent.reputation} />
          </li>
        ))}
      </ul>
    </div>
  )
}
