import { Calendar, Coins, Users } from "lucide-react"
import type { NetworkTask } from "@/lib/types"
import { getAgent } from "@/lib/mock-data"
import { formatNC } from "@/lib/utils"
import { Badge } from "./ui/badge"
import { TaskStatusBadge } from "./status-badges"
import { Button } from "./ui/button"

export function TaskCard({ task }: { task: NetworkTask }) {
  const buyer = getAgent(task.buyerId)

  return (
    <div className="flex flex-col rounded-xl border border-border bg-card p-5 transition-colors hover:border-info/40">
      <div className="flex items-start justify-between gap-3">
        <span className="text-sm text-muted-foreground">
          Posted by {buyer?.name ?? task.buyerId}
        </span>
        <TaskStatusBadge status={task.status} />
      </div>

      <h3 className="mt-3 text-base font-semibold leading-snug">{task.title}</h3>
      <p className="mt-2 text-sm leading-relaxed text-muted-foreground line-clamp-2">
        {task.description}
      </p>

      <div className="mt-4 flex flex-wrap gap-1.5">
        {task.requiredCapabilities.map((c) => (
          <Badge key={c} variant="info" className="font-mono text-[11px]">
            {c}
          </Badge>
        ))}
      </div>

      <div className="mt-5 flex flex-wrap items-center gap-x-4 gap-y-2 border-t border-border pt-4 text-sm">
        <span className="inline-flex items-center gap-1 font-mono font-semibold text-foreground">
          <Coins className="h-3.5 w-3.5 text-primary" />
          {formatNC(task.budget)} NC
        </span>
        <span className="inline-flex items-center gap-1 text-muted-foreground">
          <Calendar className="h-3.5 w-3.5" />
          {task.deadline}
        </span>
        <span className="inline-flex items-center gap-1 text-muted-foreground">
          <Users className="h-3.5 w-3.5" />
          {task.proposals} proposals
        </span>
        <Button size="sm" variant="outline" className="ml-auto" disabled={task.status === "closed"}>
          {task.status === "awarded" ? "View deal" : "Submit proposal"}
        </Button>
      </div>
    </div>
  )
}
