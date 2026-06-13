import { cn } from "@/lib/utils"
import { Slot } from "./slot"
import type { ButtonHTMLAttributes } from "react"

type Variant = "primary" | "secondary" | "ghost" | "outline"
type Size = "sm" | "md" | "lg" | "icon"

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: Variant
  size?: Size
  asChild?: boolean
}

const variantClasses: Record<Variant, string> = {
  primary:
    "bg-primary text-primary-foreground hover:bg-primary/90 shadow-sm shadow-primary/20",
  secondary:
    "bg-secondary text-secondary-foreground hover:bg-secondary/80 border border-border",
  outline:
    "border border-border bg-transparent text-foreground hover:bg-secondary/60",
  ghost: "bg-transparent text-foreground hover:bg-secondary/60",
}

const sizeClasses: Record<Size, string> = {
  sm: "h-8 px-3 text-sm rounded-md gap-1.5",
  md: "h-10 px-4 text-sm rounded-md gap-2",
  lg: "h-11 px-6 text-base rounded-lg gap-2",
  icon: "h-9 w-9 rounded-md",
}

export function Button({
  className,
  variant = "primary",
  size = "md",
  asChild = false,
  ...props
}: ButtonProps) {
  const Comp = asChild ? Slot : "button"
  return (
    <Comp
      className={cn(
        "inline-flex items-center justify-center font-medium whitespace-nowrap transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 focus-visible:ring-offset-background disabled:pointer-events-none disabled:opacity-50",
        variantClasses[variant],
        sizeClasses[size],
        className,
      )}
      {...props}
    />
  )
}
