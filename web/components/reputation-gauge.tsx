import { cn } from "@/lib/utils"

export function ReputationScore({ score }: { score: number }) {
  const color =
    score >= 90 ? "text-success" : score >= 75 ? "text-primary" : "text-warning"
  return (
    <span className="inline-flex items-baseline gap-1">
      <span className={cn("font-mono text-lg font-semibold leading-none", color)}>{score}</span>
      <span className="text-[10px] uppercase tracking-wide text-muted-foreground">rep</span>
    </span>
  )
}

export function ReputationGauge({
  score,
  size = 88,
  className,
}: {
  score: number
  size?: number
  className?: string
}) {
  const radius = (size - 10) / 2
  const circumference = 2 * Math.PI * radius
  const pct = Math.max(0, Math.min(100, score)) / 100
  const dash = circumference * pct

  const color =
    score >= 90 ? "var(--success)" : score >= 75 ? "var(--primary)" : "var(--warning)"

  return (
    <div
      className={cn("relative inline-flex items-center justify-center", className)}
      style={{ width: size, height: size }}
    >
      <svg width={size} height={size} className="-rotate-90">
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke="var(--border)"
          strokeWidth={5}
        />
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke={color}
          strokeWidth={5}
          strokeLinecap="round"
          strokeDasharray={`${dash} ${circumference}`}
        />
      </svg>
      <div className="absolute inset-0 flex flex-col items-center justify-center">
        <span className="font-mono text-lg font-semibold leading-none">{score}</span>
        <span className="mt-0.5 text-[10px] uppercase tracking-wide text-muted-foreground">
          rep
        </span>
      </div>
    </div>
  )
}
