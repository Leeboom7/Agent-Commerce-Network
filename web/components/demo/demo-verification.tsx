import type { DemoResult } from "@/lib/types"
import { cn } from "@/lib/utils"
import { CheckCircle2, XCircle, Gavel } from "lucide-react"

export function DemoVerification({ result }: { result: DemoResult }) {
  const reports = Object.entries(result.verification_reports)
  const arb = result.arbitration

  return (
    <div className="rounded-xl border border-border bg-card">
      <div className="border-b border-border px-5 py-4">
        <h2 className="text-sm font-semibold">Verification & arbitration</h2>
        <p className="text-xs text-muted-foreground">
          The honest part — claims are checked, and failures have consequences
        </p>
      </div>

      <ul className="divide-y divide-border/60">
        {reports.map(([key, report]) => {
          const passed = report.verdict === "accepted"
          return (
            <li key={key} className="flex items-center gap-3 px-5 py-3">
              {passed ? (
                <CheckCircle2 className="h-4 w-4 shrink-0 text-success" />
              ) : (
                <XCircle className="h-4 w-4 shrink-0 text-destructive" />
              )}
              <span className="flex-1 font-mono text-xs">{key}</span>
              <span
                className={cn(
                  "text-xs font-medium",
                  passed ? "text-success" : "text-destructive",
                )}
              >
                {report.verdict}
              </span>
              <span className="w-12 text-right font-mono text-xs text-muted-foreground">
                {Math.round(report.pass_rate * 100)}%
              </span>
            </li>
          )
        })}
      </ul>

      <div className="m-5 mt-4 rounded-lg border border-destructive/30 bg-destructive/5 p-4">
        <div className="flex items-center gap-2">
          <Gavel className="h-4 w-4 text-destructive" />
          <h3 className="text-sm font-semibold">Arbitration ruling</h3>
        </div>
        <dl className="mt-3 grid grid-cols-1 gap-x-6 gap-y-1.5 text-xs sm:grid-cols-2">
          <Row label="Case ID" value={arb.case_id} mono />
          <Row label="Ruling" value={String(arb.ruling_type)} mono />
          {Object.entries(arb.remedy).map(([k, v]) => (
            <Row key={k} label={k} value={String(v)} mono />
          ))}
        </dl>
      </div>
    </div>
  )
}

function Row({ label, value, mono }: { label: string; value: string; mono?: boolean }) {
  return (
    <div className="flex items-center justify-between gap-3">
      <dt className="text-muted-foreground">{label}</dt>
      <dd className={mono ? "font-mono text-foreground" : "text-foreground"}>{value}</dd>
    </div>
  )
}
