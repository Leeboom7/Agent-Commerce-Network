import type { DemoResult } from "@/lib/types"
import { Server, Plug, KeyRound } from "lucide-react"

export function DemoRuntime({
  runtime,
}: {
  runtime: DemoResult["runtimeBoundary"]
}) {
  return (
    <div className="rounded-xl border border-border bg-card p-5">
      <h2 className="text-sm font-semibold">External runtime boundary</h2>
      <p className="mt-1 text-xs text-muted-foreground">
        Agents run in their own environments — never platform hosted.
      </p>

      <ul className="mt-4 space-y-3">
        <Item icon={Server} label="Hosting" value={runtime.hosting} />
        <Item icon={Plug} label="Connector" value={runtime.connector} />
        <Item icon={KeyRound} label="Secrets" value={runtime.secrets} />
      </ul>
    </div>
  )
}

function Item({
  icon: Icon,
  label,
  value,
}: {
  icon: typeof Server
  label: string
  value: string
}) {
  return (
    <li className="flex gap-3">
      <span className="mt-0.5 flex h-7 w-7 shrink-0 items-center justify-center rounded-lg bg-secondary text-muted-foreground">
        <Icon className="h-3.5 w-3.5" />
      </span>
      <div>
        <p className="text-xs font-medium uppercase tracking-wide text-muted-foreground">
          {label}
        </p>
        <p className="mt-0.5 text-sm leading-relaxed text-foreground">{value}</p>
      </div>
    </li>
  )
}
