import Link from "next/link";
import type { ReactNode } from "react";

type CgButtonProps = {
  href?: string;
  children: ReactNode;
  variant?: "primary" | "secondary" | "ghost";
  className?: string;
};

export function CgButton({ href, children, variant = "primary", className = "" }: CgButtonProps) {
  const classes = `cg-button ${variant === "primary" ? "cg-button--dark" : variant === "secondary" ? "cg-button--light" : "cg-button--ghost"} ${className}`;

  if (href) {
    return (
      <Link className={classes} href={href}>
        {children}
      </Link>
    );
  }

  return <span className={classes}>{children}</span>;
}

export function CgBadge({ children, tone = "neutral" }: { children: ReactNode; tone?: "neutral" | "success" | "warning" | "danger" | "blue" }) {
  return <span className={`cg-badge cg-badge--${tone}`}>{children}</span>;
}

export function CgCard({ children, className = "" }: { children: ReactNode; className?: string }) {
  return <article className={`cg-card ${className}`}>{children}</article>;
}

export function CgMetric({ label, value, detail }: { label: string; value: string; detail: string }) {
  return (
    <CgCard className="cg-metric-card">
      <span>{label}</span>
      <strong>{value}</strong>
      <small>{detail}</small>
    </CgCard>
  );
}

export function CgSectionHeader({
  eyebrow,
  title,
  description,
  as = "h2",
}: {
  eyebrow?: string;
  title: string;
  description?: string;
  as?: "h1" | "h2";
}) {
  const Heading = as;

  return (
    <div className="cg-section-header">
      {eyebrow ? <span>{eyebrow}</span> : null}
      <Heading>{title}</Heading>
      {description ? <p>{description}</p> : null}
    </div>
  );
}

export function CgActivityFeed({ items }: { items: string[] }) {
  return (
    <div className="cg-activity-feed">
      {items.map((item) => (
        <div key={item} className="cg-activity-row">
          <i />
          <span>{item}</span>
        </div>
      ))}
    </div>
  );
}
