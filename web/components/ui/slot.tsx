"use client"

import { cloneElement, isValidElement, type ReactNode } from "react"

// Minimal Slot: merges props onto a single child element.
// Lets <Button asChild><Link/></Button> render an anchor with button styles.
export function Slot({
  children,
  ...props
}: { children?: ReactNode } & Record<string, unknown>) {
  if (isValidElement(children)) {
    const childProps = children.props as Record<string, unknown>
    return cloneElement(children, {
      ...props,
      ...childProps,
      className: [props.className, childProps.className]
        .filter(Boolean)
        .join(" "),
    } as Record<string, unknown>)
  }
  return null
}
