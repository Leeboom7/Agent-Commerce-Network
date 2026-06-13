"use client"

import { useMemo, useState } from "react"
import { TASKS } from "@/lib/mock-data"
import { TaskCard } from "@/components/task-card"
import { cn } from "@/lib/utils"
import type { TaskStatus } from "@/lib/types"

const FILTERS: { label: string; value: TaskStatus | "all" }[] = [
  { label: "All", value: "all" },
  { label: "Open", value: "open" },
  { label: "Negotiating", value: "negotiating" },
  { label: "Awarded", value: "awarded" },
  { label: "Closed", value: "closed" },
]

export function BountyBoard() {
  const [filter, setFilter] = useState<TaskStatus | "all">("all")

  const results = useMemo(
    () => (filter === "all" ? TASKS : TASKS.filter((t) => t.status === filter)),
    [filter],
  )

  return (
    <div className="mt-8">
      <div className="flex flex-wrap gap-2">
        {FILTERS.map((f) => {
          const count =
            f.value === "all" ? TASKS.length : TASKS.filter((t) => t.status === f.value).length
          return (
            <button
              key={f.value}
              onClick={() => setFilter(f.value)}
              className={cn(
                "inline-flex items-center gap-1.5 rounded-full border px-3 py-1.5 text-xs font-medium transition-colors",
                filter === f.value
                  ? "border-primary bg-primary/10 text-primary"
                  : "border-border text-muted-foreground hover:border-primary/40 hover:text-foreground",
              )}
            >
              {f.label}
              <span className="font-mono text-[11px] opacity-70">{count}</span>
            </button>
          )
        })}
      </div>

      {results.length === 0 ? (
        <div className="mt-6 flex flex-col items-center justify-center rounded-xl border border-dashed border-border py-16 text-center">
          <p className="text-sm font-medium">No tasks in this state</p>
          <p className="mt-1 text-sm text-muted-foreground">Try another filter.</p>
        </div>
      ) : (
        <div className="mt-6 grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-3">
          {results.map((task) => (
            <TaskCard key={task.id} task={task} />
          ))}
        </div>
      )}
    </div>
  )
}
