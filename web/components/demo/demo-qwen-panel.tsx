import type { DemoQwen } from "@/lib/types"
import { QwenStatusPill } from "@/components/status-badges"
import { Badge } from "@/components/ui/badge"
import { Brain } from "lucide-react"

export function DemoQwenPanel({ qwen }: { qwen: DemoQwen }) {
  return (
    <div className="rounded-xl border border-border bg-card p-5">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <span className="flex h-7 w-7 items-center justify-center rounded-lg bg-primary/10 text-primary">
            <Brain className="h-4 w-4" />
          </span>
          <h2 className="text-sm font-semibold">Qwen decision layer</h2>
        </div>
        <QwenStatusPill status={qwen.status} />
      </div>

      {qwen.status === "fallback" && (
        <p className="mt-3 rounded-lg border border-warning/30 bg-warning/10 px-3 py-2 text-xs text-warning-foreground">
          Running with deterministic fallback reasoning — no QWEN_API_KEY present. The loop still
          completes identically.
        </p>
      )}

      <div className="mt-4">
        <p className="text-xs font-medium uppercase tracking-wide text-muted-foreground">
          Planner
        </p>
        <p className="mt-1 text-sm leading-relaxed text-muted-foreground">
          {qwen.plannerOutput.summary}
        </p>
        <ul className="mt-2 space-y-1">
          {qwen.plannerOutput.workPackages.map((w) => (
            <li key={w} className="flex items-start gap-2 text-xs text-muted-foreground">
              <span className="mt-1.5 h-1 w-1 shrink-0 rounded-full bg-primary" />
              {w}
            </li>
          ))}
        </ul>
        <div className="mt-3 flex flex-wrap gap-1.5">
          {qwen.plannerOutput.selectedServices.map((s) => (
            <Badge key={s} variant="muted" className="font-mono text-[10px]">
              {s}
            </Badge>
          ))}
        </div>
      </div>

      <div className="mt-4 border-t border-border pt-4">
        <p className="text-xs font-medium uppercase tracking-wide text-muted-foreground">
          Negotiation rationale
        </p>
        <p className="mt-1 text-sm leading-relaxed text-muted-foreground">
          {qwen.negotiationRationale}
        </p>
      </div>

      <div className="mt-4 border-t border-border pt-4">
        <p className="text-xs font-medium uppercase tracking-wide text-muted-foreground">
          Arbitration rationale
        </p>
        <p className="mt-1 text-sm leading-relaxed text-muted-foreground">
          {qwen.arbitrationRationale}
        </p>
      </div>
    </div>
  )
}
