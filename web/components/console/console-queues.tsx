import Link from "next/link"
import { DEALS, getAgent } from "@/lib/mock-data"
import { Clock, ShieldAlert, ShieldCheck } from "lucide-react"

export function ConsoleQueues() {
  const pendingVerification = DEALS.filter((d) =>
    d.timeline.some(
      (t) => t.stage === "verification" && (t.state === "current" || t.state === "pending"),
    ),
  )
  const recentRulings = DEALS.filter((d) =>
    d.timeline.some((t) => t.stage === "arbitration" && t.state === "done"),
  )

  return (
    <div className="flex flex-col gap-6">
      <div className="rounded-xl border border-border bg-card">
        <div className="flex items-center gap-2 border-b border-border px-5 py-4">
          <ShieldCheck className="h-4 w-4 text-warning" />
          <h2 className="text-sm font-semibold">Verification queue</h2>
        </div>
        {pendingVerification.length === 0 ? (
          <p className="px-5 py-6 text-sm text-muted-foreground">
            Nothing awaiting verification.
          </p>
        ) : (
          <ul className="divide-y divide-border/60">
            {pendingVerification.map((d) => {
              const seller = getAgent(d.sellerId)
              return (
                <li key={d.id} className="px-5 py-3.5">
                  <Link href={`/deals/${d.id}`} className="text-sm font-medium hover:text-primary">
                    {d.title}
                  </Link>
                  <p className="mt-1 inline-flex items-center gap-1.5 text-xs text-muted-foreground">
                    <Clock className="h-3 w-3" />
                    {seller?.name} · delivery in progress
                  </p>
                </li>
              )
            })}
          </ul>
        )}
      </div>

      <div className="rounded-xl border border-border bg-card">
        <div className="flex items-center gap-2 border-b border-border px-5 py-4">
          <ShieldAlert className="h-4 w-4 text-destructive" />
          <h2 className="text-sm font-semibold">Recent rulings</h2>
        </div>
        <ul className="divide-y divide-border/60">
          {recentRulings.map((d) => {
            const node = d.timeline.find((t) => t.stage === "arbitration")
            return (
              <li key={d.id} className="px-5 py-3.5">
                <Link href={`/deals/${d.id}`} className="text-sm font-medium hover:text-primary">
                  {d.title}
                </Link>
                <p className="mt-1 font-mono text-xs text-destructive">{node?.verdict}</p>
              </li>
            )
          })}
        </ul>
      </div>
    </div>
  )
}
