import { Badge } from "./ui/badge"
import { cn } from "@/lib/utils"
import type { DealStatus, TaskStatus, AgentStatus } from "@/lib/types"

const dealMap: Record<DealStatus, { label: string; variant: Parameters<typeof Badge>[0]["variant"] }> = {
  negotiating: { label: "Negotiating", variant: "warning" },
  active: { label: "Active", variant: "info" },
  delivered: { label: "Delivered", variant: "info" },
  verifying: { label: "Verifying", variant: "warning" },
  disputed: { label: "Disputed", variant: "danger" },
  settled: { label: "Settled", variant: "success" },
  failed: { label: "Failed", variant: "danger" },
}

const taskMap: Record<TaskStatus, { label: string; variant: Parameters<typeof Badge>[0]["variant"] }> = {
  open: { label: "Open", variant: "success" },
  negotiating: { label: "Negotiating", variant: "warning" },
  awarded: { label: "Awarded", variant: "info" },
  closed: { label: "Closed", variant: "outline" },
}

export function DealStatusBadge({ status }: { status: DealStatus }) {
  const { label, variant } = dealMap[status]
  return <Badge variant={variant}>{label}</Badge>
}

export function TaskStatusBadge({ status }: { status: TaskStatus }) {
  const { label, variant } = taskMap[status]
  return <Badge variant={variant}>{label}</Badge>
}

const agentDot: Record<AgentStatus, string> = {
  online: "bg-success",
  busy: "bg-warning",
  offline: "bg-muted-foreground",
}

export function ConnectorHealthDot({
  status,
  className,
}: {
  status: AgentStatus
  className?: string
}) {
  return (
    <span className={cn("relative inline-flex h-2 w-2", className)}>
      {status === "online" && (
        <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-success/60" />
      )}
      <span className={cn("relative inline-flex h-2 w-2 rounded-full", agentDot[status])} />
    </span>
  )
}

export function QwenStatusPill({ status }: { status: "live" | "fallback" }) {
  return (
    <Badge variant={status === "live" ? "success" : "warning"}>
      <span
        className={cn(
          "h-1.5 w-1.5 rounded-full",
          status === "live" ? "bg-success" : "bg-warning",
        )}
      />
      Qwen {status === "live" ? "live" : "fallback"}
    </Badge>
  )
}
