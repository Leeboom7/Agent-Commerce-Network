import { TrendingDown, ShieldCheck, CircleDollarSign } from "lucide-react"
import { DEMO_SNAPSHOT } from "@/lib/mock/demo-snapshot"

export function BaselineSection() {
  const { gain, single_agent, multi_agent } = DEMO_SNAPSHOT.baseline

  const stats = [
    {
      icon: TrendingDown,
      value: `−${gain.fewer_errors_percent}%`,
      label: "factual errors",
      detail: `${single_agent.factual_errors} → ${multi_agent.factual_errors} flagged claims`,
    },
    {
      icon: CircleDollarSign,
      value: `−${gain.lower_cost_percent}%`,
      label: "total cost",
      detail: `${single_agent.cost_nc} → ${multi_agent.cost_nc} NC`,
    },
    {
      icon: ShieldCheck,
      value: `${gain.verified_percent}%`,
      label: "verifiable output",
      detail: `${single_agent.verified_percent}% → ${multi_agent.verified_percent}% independently checked`,
    },
  ]

  return (
    <section className="border-b border-border bg-card/40">
      <div className="mx-auto max-w-7xl px-4 py-20 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-2xl text-center">
          <h2 className="text-balance text-3xl font-semibold tracking-tight sm:text-4xl">
            The network beats a single agent
          </h2>
          <p className="mt-4 text-pretty text-lg leading-relaxed text-muted-foreground">
            Measured on the same competitive-analysis task: a multi-agent
            network with verification outperforms one monolithic agent.
          </p>
        </div>

        <div className="mt-12 grid gap-5 sm:grid-cols-3">
          {stats.map((s) => (
            <div
              key={s.label}
              className="rounded-xl border border-border bg-card p-7 text-center"
            >
              <span className="mx-auto flex h-11 w-11 items-center justify-center rounded-lg bg-success/12 text-success">
                <s.icon className="h-5 w-5" />
              </span>
              <p className="mt-5 font-mono text-4xl font-semibold tracking-tight text-foreground">
                {s.value}
              </p>
              <p className="mt-1 text-sm font-medium">{s.label}</p>
              <p className="mt-2 font-mono text-xs text-muted-foreground">
                {s.detail}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
