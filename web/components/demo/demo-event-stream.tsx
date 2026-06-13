"use client"

import type { DemoEvent } from "@/lib/types"
import { cn } from "@/lib/utils"
import { Check, Loader2 } from "lucide-react"

const FAIL_EVENTS = new Set(["verification_failed_claims", "dispute_case_opened"])

export function DemoEventStream({
  events,
  visible,
}: {
  events: DemoEvent[]
  visible: number
}) {
  return (
    <div className="rounded-xl border border-border bg-card">
      <div className="flex items-center justify-between border-b border-border px-5 py-4">
        <div>
          <h2 className="text-sm font-semibold">Protocol event stream</h2>
          <p className="text-xs text-muted-foreground">Real ACP messages, in order</p>
        </div>
        <span className="font-mono text-xs text-muted-foreground">
          {Math.min(visible, events.length)}/{events.length}
        </span>
      </div>

      <ol className="divide-y divide-border/60">
        {events.map((evt, i) => {
          const shown = i < visible
          const isCurrent = i === visible - 1
          const isFail = FAIL_EVENTS.has(evt.event)
          return (
            <li
              key={evt.event + i}
              className={cn(
                "flex gap-3 px-5 py-3 transition-all duration-300",
                shown ? "opacity-100" : "pointer-events-none opacity-30",
              )}
            >
              <span
                className={cn(
                  "mt-0.5 flex h-5 w-5 shrink-0 items-center justify-center rounded-full text-[10px]",
                  !shown
                    ? "border border-border text-muted-foreground"
                    : isFail
                      ? "bg-destructive/15 text-destructive"
                      : "bg-success/15 text-success",
                )}
              >
                {shown ? <Check className="h-3 w-3" /> : i + 1}
              </span>
              <div className="min-w-0 flex-1">
                <div className="flex items-center gap-2">
                  <code
                    className={cn(
                      "font-mono text-xs",
                      isFail ? "text-destructive" : "text-foreground",
                    )}
                  >
                    {evt.event}
                  </code>
                  {isCurrent && (
                    <Loader2 className="h-3 w-3 animate-spin text-primary" aria-hidden />
                  )}
                </div>
                <p className="mt-0.5 text-sm text-muted-foreground">{evt.details}</p>
              </div>
            </li>
          )
        })}
      </ol>
    </div>
  )
}
