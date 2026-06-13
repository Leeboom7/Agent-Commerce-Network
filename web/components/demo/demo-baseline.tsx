import type { DemoResult } from "@/lib/types"
import { ArrowDown, ShieldCheck } from "lucide-react"

export function DemoBaseline({ baseline }: { baseline: DemoResult["baseline"] }) {
  const rows = [
    {
      label: "Factual errors",
      single: baseline.single_agent.factual_errors,
      multi: baseline.multi_agent.factual_errors,
      suffix: "",
    },
    {
      label: "Cost",
      single: baseline.single_agent.cost_nc,
      multi: baseline.multi_agent.cost_nc,
      suffix: " NC",
    },
    {
      label: "Verified claims",
      single: `${baseline.single_agent.verified_percent}%`,
      multi: `${baseline.multi_agent.verified_percent}%`,
      suffix: "",
    },
  ]

  return (
    <div className="rounded-xl border border-border bg-card">
      <div className="border-b border-border px-5 py-4">
        <h2 className="text-sm font-semibold">Single agent vs the network</h2>
        <p className="text-xs text-muted-foreground">Why coordination is worth it</p>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-border text-left text-xs text-muted-foreground">
              <th className="px-5 py-2.5 font-medium">Metric</th>
              <th className="px-3 py-2.5 text-right font-medium">Single agent</th>
              <th className="px-3 py-2.5 text-right font-medium">CoAgenta network</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((r) => (
              <tr key={r.label} className="border-b border-border/60 last:border-0">
                <td className="px-5 py-3 text-muted-foreground">{r.label}</td>
                <td className="px-3 py-3 text-right font-mono text-muted-foreground">
                  {r.single}
                  {r.suffix}
                </td>
                <td className="px-3 py-3 text-right font-mono font-semibold text-foreground">
                  {r.multi}
                  {r.suffix}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="grid grid-cols-3 gap-px border-t border-border bg-border">
        <Gain icon={ArrowDown} value={`-${baseline.gain.fewer_errors_percent}%`} label="errors" />
        <Gain icon={ArrowDown} value={`-${baseline.gain.lower_cost_percent}%`} label="cost" />
        <Gain
          icon={ShieldCheck}
          value={`${baseline.gain.verified_percent}%`}
          label="verified"
        />
      </div>
    </div>
  )
}

function Gain({
  icon: Icon,
  value,
  label,
}: {
  icon: typeof ArrowDown
  value: string
  label: string
}) {
  return (
    <div className="flex flex-col items-center justify-center gap-1 bg-card py-4">
      <span className="inline-flex items-center gap-1 font-mono text-lg font-semibold text-success">
        <Icon className="h-4 w-4" />
        {value}
      </span>
      <span className="text-xs text-muted-foreground">{label}</span>
    </div>
  )
}
