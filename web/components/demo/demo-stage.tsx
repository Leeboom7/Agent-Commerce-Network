"use client"

import { useCallback, useEffect, useRef, useState } from "react"
import { Play, RotateCcw, Loader2, Zap } from "lucide-react"
import type { DemoResult } from "@/lib/types"
import { PageHeader } from "@/components/page-header"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { QwenStatusPill } from "@/components/status-badges"
import { DemoEventStream } from "./demo-event-stream"
import { DemoQwenPanel } from "./demo-qwen-panel"
import { DemoVerification } from "./demo-verification"
import { DemoSettlement } from "./demo-settlement"
import { DemoBaseline } from "./demo-baseline"
import { DemoRuntime } from "./demo-runtime"

type RunState = "idle" | "running" | "done"

export function DemoStage() {
  const [state, setState] = useState<RunState>("idle")
  const [result, setResult] = useState<DemoResult | null>(null)
  const [visibleEvents, setVisibleEvents] = useState(0)
  const timers = useRef<ReturnType<typeof setTimeout>[]>([])

  const clearTimers = useCallback(() => {
    timers.current.forEach(clearTimeout)
    timers.current = []
  }, [])

  useEffect(() => clearTimers, [clearTimers])

  const playEvents = useCallback((count: number) => {
    clearTimers()
    setVisibleEvents(0)
    for (let i = 1; i <= count; i++) {
      const t = setTimeout(() => setVisibleEvents(i), i * 550)
      timers.current.push(t)
    }
  }, [clearTimers])

  const run = useCallback(async () => {
    setState("running")
    setResult(null)
    setVisibleEvents(0)
    try {
      const res = await fetch("/api/demo/run", { method: "POST" })
      const data = (await res.json()) as DemoResult
      setResult(data)
      setState("done")
      playEvents(data.events.length)
    } catch {
      setState("idle")
    }
  }, [playEvents])

  const reset = useCallback(() => {
    clearTimers()
    setState("idle")
    setResult(null)
    setVisibleEvents(0)
  }, [clearTimers])

  return (
    <div className="mx-auto w-full max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
      <PageHeader
        eyebrow="Live commerce demo"
        title="Watch the full economic loop run"
        description="This runs the canonical Python ACP scenario: five agents collaborate on a 2026 China AI coding-tools risk brief. It is not a happy path — verification fails, a dispute is raised, and arbitration applies a penalty before settlement."
        action={
          state === "done" ? (
            <Button variant="outline" onClick={reset}>
              <RotateCcw className="h-4 w-4" />
              Replay
            </Button>
          ) : (
            <Button onClick={run} disabled={state === "running"}>
              {state === "running" ? (
                <>
                  <Loader2 className="h-4 w-4 animate-spin" />
                  Running…
                </>
              ) : (
                <>
                  <Play className="h-4 w-4" />
                  Run live demo
                </>
              )}
            </Button>
          )
        }
      />

      {state === "idle" && (
        <div className="mt-10 flex flex-col items-center justify-center rounded-2xl border border-dashed border-border bg-card/40 py-20 text-center">
          <span className="flex h-12 w-12 items-center justify-center rounded-xl bg-primary/10 text-primary">
            <Zap className="h-6 w-6" />
          </span>
          <h2 className="mt-4 text-lg font-semibold">Ready to run the network</h2>
          <p className="mt-2 max-w-md text-pretty text-sm text-muted-foreground">
            Press run to execute the live Python runtime. If the runtime is unavailable, a packaged
            snapshot is used so the demo never breaks.
          </p>
          <Button className="mt-6" onClick={run}>
            <Play className="h-4 w-4" />
            Run live demo
          </Button>
        </div>
      )}

      {(state === "running" || state === "done") && (
        <div className="mt-8">
          {result && (
            <div className="mb-6 flex flex-wrap items-center gap-2">
              <QwenStatusPill status={result.qwen.status} />
              <Badge variant={result.source === "live" ? "success" : "warning"}>
                {result.source === "live" ? "Live Python runtime" : "Packaged snapshot"}
              </Badge>
              <Badge variant="muted">5 agents</Badge>
              <Badge variant="muted">{result.events.length} protocol events</Badge>
            </div>
          )}

          {state === "running" && !result && (
            <div className="flex items-center gap-2 rounded-xl border border-border bg-card px-5 py-4 text-sm text-muted-foreground">
              <Loader2 className="h-4 w-4 animate-spin text-primary" />
              Executing agents, negotiations, verification, and settlement…
            </div>
          )}

          {result && (
            <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
              <div className="lg:col-span-2 flex flex-col gap-6">
                <DemoEventStream events={result.events} visible={visibleEvents} />
                <DemoVerification result={result} />
                <DemoBaseline baseline={result.baseline} />
              </div>
              <div className="flex flex-col gap-6">
                <DemoQwenPanel qwen={result.qwen} />
                <DemoSettlement settlement={result.settlement} />
                <DemoRuntime runtime={result.runtimeBoundary} />
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}
