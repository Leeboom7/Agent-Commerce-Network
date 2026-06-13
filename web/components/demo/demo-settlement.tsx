import type { DemoResult } from "@/lib/types"
import { getAgent } from "@/lib/mock-data"
import { formatNC } from "@/lib/utils"
import { Wallet } from "lucide-react"

export function DemoSettlement({
  settlement,
}: {
  settlement: DemoResult["settlement"]
}) {
  return (
    <div className="rounded-xl border border-border bg-card p-5">
      <div className="flex items-center gap-2">
        <span className="flex h-7 w-7 items-center justify-center rounded-lg bg-primary/10 text-primary">
          <Wallet className="h-4 w-4" />
        </span>
        <h2 className="text-sm font-semibold">Settlement ledger</h2>
      </div>

      <ul className="mt-4 space-y-3">
        {settlement.payments.map((p) => {
          const agent = getAgent(p.agent)
          return (
            <li key={p.agent} className="flex items-center justify-between gap-2">
              <div className="min-w-0">
                <p className="truncate text-sm font-medium">{agent?.name ?? p.agent}</p>
                {p.penalty > 0 && (
                  <p className="font-mono text-xs text-destructive">
                    -{formatNC(p.penalty)} NC penalty
                  </p>
                )}
              </div>
              <span className="font-mono text-sm font-semibold">{formatNC(p.amount)} NC</span>
            </li>
          )
        })}
      </ul>

      <div className="mt-4 flex items-center justify-between border-t border-border pt-4">
        <span className="text-sm text-muted-foreground">Total settled</span>
        <span className="font-mono text-base font-semibold text-primary">
          {formatNC(settlement.total_cost)} NC
        </span>
      </div>
    </div>
  )
}
