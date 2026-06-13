import Link from "next/link"
import { Star, Clock, ArrowRight } from "lucide-react"
import type { Service } from "@/lib/types"
import { getAgent } from "@/lib/mock-data"
import { formatNC } from "@/lib/utils"
import { Badge } from "./ui/badge"
import { ConnectorHealthDot } from "./status-badges"

export function ServiceCard({ service }: { service: Service }) {
  const agent = getAgent(service.agentId)
  if (!agent) return null

  return (
    <div className="flex flex-col rounded-xl border border-border bg-card p-5 transition-colors hover:border-primary/40">
      <div className="flex items-start justify-between gap-3">
        <Link
          href={`/agents/${agent.id}`}
          className="flex items-center gap-2 text-sm text-muted-foreground hover:text-foreground"
        >
          <ConnectorHealthDot status={agent.status} />
          {agent.name}
        </Link>
        <Badge variant="outline">{agent.connector}</Badge>
      </div>

      <h3 className="mt-3 text-base font-semibold leading-snug">{service.title}</h3>
      <p className="mt-2 text-sm leading-relaxed text-muted-foreground line-clamp-2">
        {service.description}
      </p>

      <div className="mt-4 flex flex-wrap gap-1.5">
        {service.tags.slice(0, 3).map((t) => (
          <Badge key={t} variant="default" className="font-mono text-[11px]">
            {t}
          </Badge>
        ))}
      </div>

      <div className="mt-5 flex items-center gap-4 border-t border-border pt-4 text-sm">
        <span className="font-mono font-semibold text-foreground">
          {formatNC(service.price)} NC
        </span>
        <span className="inline-flex items-center gap-1 text-muted-foreground">
          <Clock className="h-3.5 w-3.5" />
          {service.eta}
        </span>
        <span className="inline-flex items-center gap-1 text-muted-foreground">
          <Star className="h-3.5 w-3.5 text-warning" />
          {service.rating}
        </span>
        <Link
          href={`/agents/${agent.id}`}
          className="ml-auto inline-flex items-center gap-1 text-sm font-medium text-primary hover:underline"
        >
          Hire
          <ArrowRight className="h-3.5 w-3.5" />
        </Link>
      </div>
    </div>
  )
}
