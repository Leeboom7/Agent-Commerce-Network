"use client"

import { useState } from "react"
import {
  Check,
  ChevronDown,
  Circle,
  FileText,
  Gavel,
  Handshake,
  PackageCheck,
  ShieldCheck,
  Star,
  Wallet,
  X,
} from "lucide-react"
import type { DealStage, DealTimelineNode } from "@/lib/types"
import { cn } from "@/lib/utils"

const stageIcon: Record<DealStage, typeof Check> = {
  proposal: FileText,
  agreement: Handshake,
  delivery: PackageCheck,
  verification: ShieldCheck,
  dispute: X,
  arbitration: Gavel,
  settlement: Wallet,
  reputation: Star,
}

export function DealTimeline({ nodes }: { nodes: DealTimelineNode[] }) {
  return (
    <ol className="relative">
      {nodes.map((node, i) => (
        <TimelineItem key={node.stage + i} node={node} isLast={i === nodes.length - 1} />
      ))}
    </ol>
  )
}

function TimelineItem({ node, isLast }: { node: DealTimelineNode; isLast: boolean }) {
  const [open, setOpen] = useState(node.state === "failed" || node.state === "current")
  const Icon = stageIcon[node.stage]
  const hasDetails = (node.details && node.details.length > 0) || node.verdict

  const dot =
    node.state === "failed"
      ? "border-destructive bg-destructive/15 text-destructive"
      : node.state === "current"
        ? "border-warning bg-warning/15 text-warning"
        : node.state === "pending"
          ? "border-border bg-secondary text-muted-foreground"
          : "border-success/50 bg-success/15 text-success"

  return (
    <li className="relative flex gap-4 pb-6 last:pb-0">
      {!isLast && (
        <span
          className="absolute left-[18px] top-9 h-[calc(100%-1rem)] w-px bg-border"
          aria-hidden
        />
      )}
      <span
        className={cn(
          "z-10 flex h-9 w-9 shrink-0 items-center justify-center rounded-full border",
          dot,
        )}
      >
        {node.state === "done" ? (
          <Check className="h-4 w-4" />
        ) : node.state === "failed" ? (
          <X className="h-4 w-4" />
        ) : node.state === "pending" ? (
          <Circle className="h-3 w-3" />
        ) : (
          <Icon className="h-4 w-4" />
        )}
      </span>

      <div className="min-w-0 flex-1">
        <button
          onClick={() => hasDetails && setOpen((v) => !v)}
          className={cn(
            "flex w-full items-start justify-between gap-3 text-left",
            hasDetails && "cursor-pointer",
          )}
          aria-expanded={open}
          disabled={!hasDetails}
        >
          <div>
            <div className="flex items-center gap-2">
              <Icon className="h-3.5 w-3.5 text-muted-foreground" />
              <h3
                className={cn(
                  "text-sm font-semibold",
                  node.state === "failed" && "text-destructive",
                )}
              >
                {node.title}
              </h3>
            </div>
            <p className="mt-0.5 font-mono text-xs text-muted-foreground">{node.timestamp}</p>
          </div>
          {hasDetails && (
            <ChevronDown
              className={cn(
                "mt-1 h-4 w-4 shrink-0 text-muted-foreground transition-transform",
                open && "rotate-180",
              )}
            />
          )}
        </button>

        <p className="mt-2 text-sm leading-relaxed text-muted-foreground">{node.summary}</p>

        {open && hasDetails && (
          <div className="mt-3 rounded-lg border border-border bg-background p-3">
            {node.verdict && (
              <p
                className={cn(
                  "mb-2 font-mono text-xs font-medium",
                  node.state === "failed" ? "text-destructive" : "text-foreground",
                )}
              >
                {node.verdict}
              </p>
            )}
            {node.details && (
              <dl className="grid grid-cols-1 gap-x-6 gap-y-1.5 sm:grid-cols-2">
                {node.details.map((d) => (
                  <div key={d.label} className="flex items-center justify-between gap-3 text-xs">
                    <dt className="text-muted-foreground">{d.label}</dt>
                    <dd className="font-mono text-foreground">{d.value}</dd>
                  </div>
                ))}
              </dl>
            )}
          </div>
        )}
      </div>
    </li>
  )
}
