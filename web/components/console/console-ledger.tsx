import { LEDGER, getAgent } from "@/lib/mock-data"
import { formatNC } from "@/lib/utils"
import { ArrowRight } from "lucide-react"

export function ConsoleLedger() {
  return (
    <div className="rounded-xl border border-border bg-card">
      <div className="border-b border-border px-5 py-4">
        <h2 className="text-sm font-semibold">Credit ledger</h2>
        <p className="text-xs text-muted-foreground">Network Credits (NC) settlement log</p>
      </div>
      <ul className="divide-y divide-border/60">
        {LEDGER.map((txn) => {
          const from = getAgent(txn.from)
          const to = getAgent(txn.to)
          return (
            <li key={txn.id} className="px-5 py-3.5">
              <div className="flex items-center justify-between gap-2">
                <span className="inline-flex items-center gap-1.5 text-xs text-muted-foreground">
                  {from?.name}
                  <ArrowRight className="h-3 w-3" />
                  {to?.name}
                </span>
                <span className="font-mono text-sm font-semibold">
                  {formatNC(txn.amount)} NC
                </span>
              </div>
              <p className="mt-1 text-xs text-muted-foreground">{txn.reason}</p>
              <p className="mt-0.5 font-mono text-[11px] text-muted-foreground/70">
                {txn.timestamp}
              </p>
            </li>
          )
        })}
      </ul>
    </div>
  )
}
