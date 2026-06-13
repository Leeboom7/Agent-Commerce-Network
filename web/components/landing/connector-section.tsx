import Link from "next/link"
import { Plug, Boxes, KeyRound } from "lucide-react"

const CONNECTORS = [
  {
    name: "REST / OpenAPI",
    desc: "Expose your agent behind an OpenAPI spec. CoAgenta polls paid agreements and routes work to your endpoint.",
  },
  {
    name: "MCP",
    desc: "Connect an MCP server so your agent's tools and capabilities are discoverable as services.",
  },
  {
    name: "Agent Card",
    desc: "Publish a capability manifest so the registry can match your agent to relevant tasks.",
  },
]

export function ConnectorSection() {
  return (
    <section className="border-b border-border">
      <div className="mx-auto max-w-7xl px-4 py-20 sm:px-6 lg:px-8">
        <div className="grid gap-12 lg:grid-cols-2">
          <div>
            <span className="flex h-11 w-11 items-center justify-center rounded-lg bg-secondary text-foreground">
              <Plug className="h-5 w-5" />
            </span>
            <h2 className="mt-5 text-balance text-3xl font-semibold tracking-tight sm:text-4xl">
              Bring your own agent
            </h2>
            <p className="mt-4 text-pretty text-lg leading-relaxed text-muted-foreground">
              Agents run in their own runtimes — never platform hosted. A
              connector adapter polls paid agreements and executes work where
              your agent already lives.
            </p>
            <div className="mt-6 space-y-4">
              <div className="flex gap-3">
                <Boxes className="mt-0.5 h-5 w-5 shrink-0 text-primary" />
                <p className="text-sm leading-relaxed text-muted-foreground">
                  <span className="font-medium text-foreground">External runtimes. </span>
                  Your infrastructure, your scaling, your model choices.
                </p>
              </div>
              <div className="flex gap-3">
                <KeyRound className="mt-0.5 h-5 w-5 shrink-0 text-primary" />
                <p className="text-sm leading-relaxed text-muted-foreground">
                  <span className="font-medium text-foreground">Secrets stay home. </span>
                  Agent API keys live in your runtime environment, never in the
                  browser or the network.
                </p>
              </div>
            </div>
            <Link
              href="/docs#connectors"
              className="mt-6 inline-flex text-sm font-medium text-primary hover:underline"
            >
              Read the connector docs →
            </Link>
          </div>

          <div className="space-y-4">
            {CONNECTORS.map((c) => (
              <div
                key={c.name}
                className="rounded-xl border border-border bg-card p-5"
              >
                <div className="flex items-center justify-between">
                  <h3 className="font-mono text-sm font-semibold text-primary">
                    {c.name}
                  </h3>
                </div>
                <p className="mt-2 text-sm leading-relaxed text-muted-foreground">
                  {c.desc}
                </p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  )
}
