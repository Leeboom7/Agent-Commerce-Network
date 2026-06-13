import { cn } from "@/lib/utils"
import type { HTMLAttributes } from "react"

type BadgeVariant =
  | "default"
  | "outline"
  | "primary"
  | "success"
  | "warning"
  | "danger"
  | "info"

const variants: Record<BadgeVariant, string> = {
  default: "bg-secondary text-secondary-foreground border-transparent",
  outline: "bg-transparent text-muted-foreground border-border",
  primary: "bg-primary/15 text-primary border-primary/25",
  success: "bg-success/15 text-success border-success/25",
  warning: "bg-warning/15 text-warning border-warning/25",
  danger: "bg-destructive/15 text-destructive border-destructive/25",
  info: "bg-info/15 text-info border-info/25",
}

interface BadgeProps extends HTMLAttributes<HTMLSpanElement> {
  variant?: BadgeVariant
}

export function Badge({ className, variant = "default", ...props }: BadgeProps) {
  return (
    <span
      className={cn(
        "inline-flex items-center gap-1.5 rounded-full border px-2.5 py-0.5 text-xs font-medium",
        variants[variant],
        className,
      )}
      {...props}
    />
  )
}
