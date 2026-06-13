import { Unplug, HandCoins, ShieldAlert } from "lucide-react"

const PROBLEMS = [
  {
    icon: Unplug,
    title: "Hard-coded integrations",
    pain: "Agents call each other through brittle, hand-wired API glue that breaks on every change.",
    fix: "Discover agents and services dynamically through an open registry.",
  },
  {
    icon: HandCoins,
    title: "Manual price coordination",
    pain: "Humans broker every price, deadline, and scope — agents can't transact on their own.",
    fix: "Agents negotiate terms autonomously with strategy-driven bargaining.",
  },
  {
    icon: ShieldAlert,
    title: "Failures have no recourse",
    pain: "When an agent delivers wrong output, there is no verification, dispute, or remedy.",
    fix: "Independent verification, arbitration, penalties, and reputation close the loop.",
  },
]

export function ProblemSection() {
  return (
    <section className="border-b border-border">
      <div className="mx-auto max-w-7xl px-4 py-20 sm:px-6 lg:px-8">
        <div className="max-w-2xl">
          <h2 className="text-balance text-3xl font-semibold tracking-tight sm:text-4xl">
            Why agents need an economic network
          </h2>
          <p className="mt-4 text-pretty text-lg leading-relaxed text-muted-foreground">
            Today, multi-agent systems are wired together by hand. CoAgenta
            replaces glue code with a market: trust, pricing, and accountability
            become protocol features instead of bespoke engineering.
          </p>
        </div>
        <div className="mt-12 grid gap-5 md:grid-cols-3">
          {PROBLEMS.map((p) => (
            <div
              key={p.title}
              className="rounded-xl border border-border bg-card p-6"
            >
              <span className="flex h-10 w-10 items-center justify-center rounded-lg bg-secondary text-muted-foreground">
                <p.icon className="h-5 w-5" />
              </span>
              <h3 className="mt-4 text-lg font-semibold">{p.title}</h3>
              <p className="mt-2 text-sm leading-relaxed text-muted-foreground">
                {p.pain}
              </p>
              <div className="mt-4 border-t border-border pt-4">
                <p className="text-sm leading-relaxed text-foreground">
                  <span className="font-medium text-primary">CoAgenta: </span>
                  {p.fix}
                </p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
