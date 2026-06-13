import Link from "next/link"
import { DEALS, getAgent } from "@/lib/mock-data"
import { DealStatusBadge } from "@/components/status-badges"
import { formatNC } from "@/lib/utils"
import { ArrowUpRight } from "lucide-react"

export function ConsoleDeals() {
  return (
    <div className="rounded-xl border border-border bg-card">
      <div className="flex items-center justify-between border-b border-border px-5 py-4">
        <div>
          <h2 className="text-sm font-semibold">Active & recent deals</h2>
          <p className="text-xs text-muted-foreground">
            Lifecycle status across the network
          </p>
        </div>
        <Link
          href="/bounties"
          className="text-xs font-medium text-primary hover:underline"
        >
          Post a task
        </Link>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-border text-left text-xs text-muted-foreground">
              <th className="px-5 py-2.5 font-medium">Deal</th>
              <th className="px-3 py-2.5 font-medium">Counterparty</th>
              <th className="px-3 py-2.5 font-medium">Status</th>
              <th className="px-3 py-2.5 text-right font-medium">Net</th>
              <th className="px-5 py-2.5" />
            </tr>
          </thead>
          <tbody>
            {DEALS.map((deal) => {
              const seller = getAgent(deal.sellerId)
              return (
                <tr
                  key={deal.id}
                  className="border-b border-border/60 last:border-0 transition-colors hover:bg-secondary/40"
                >
                  <td className="px-5 py-3">
                    <Link href={`/deals/${deal.id}`} className="font-medium hover:text-primary">
                      {deal.title}
                    </Link>
                    <p className="mt-0.5 font-mono text-xs text-muted-foreground">{deal.id}</p>
                  </td>
                  <td className="px-3 py-3 text-muted-foreground">{seller?.name}</td>
                  <td className="px-3 py-3">
                    <DealStatusBadge status={deal.status} />
                  </td>
                  <td className="px-3 py-3 text-right font-mono">
                    {formatNC(deal.netPayment)}
                    {deal.penalty > 0 && (
                      <span className="ml-1 text-xs text-destructive">
                        -{formatNC(deal.penalty)}
                      </span>
                    )}
                  </td>
                  <td className="px-5 py-3 text-right">
                    <Link
                      href={`/deals/${deal.id}`}
                      className="inline-flex text-muted-foreground hover:text-primary"
                      aria-label={`Open ${deal.title}`}
                    >
                      <ArrowUpRight className="h-4 w-4" />
                    </Link>
                  </td>
                </tr>
              )
            })}
          </tbody>
        </table>
      </div>
    </div>
  )
}
