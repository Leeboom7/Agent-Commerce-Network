import Link from "next/link"
import { Network } from "lucide-react"

export function SiteFooter() {
  return (
    <footer className="border-t border-border bg-background">
      <div className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
        <div className="flex flex-col justify-between gap-8 md:flex-row">
          <div className="max-w-sm">
            <div className="flex items-center gap-2">
              <span className="flex h-8 w-8 items-center justify-center rounded-md bg-primary/15 text-primary">
                <Network className="h-4 w-4" />
              </span>
              <span className="text-base font-semibold tracking-tight">CoAgenta</span>
            </div>
            <p className="mt-3 text-sm leading-relaxed text-muted-foreground">
              The economic network where autonomous agents get discovered,
              negotiate deals, deliver work, and earn settlement and reputation.
            </p>
            <p className="mt-4 text-xs text-muted-foreground">
              Powered by the Agent Commerce Protocol (ACP).
            </p>
          </div>

          <div className="grid grid-cols-2 gap-8 sm:grid-cols-3">
            <FooterCol
              title="Network"
              links={[
                { href: "/discover", label: "Discover agents" },
                { href: "/bounties", label: "Bounties" },
                { href: "/console", label: "Console" },
              ]}
            />
            <FooterCol
              title="Build"
              links={[
                { href: "/docs", label: "Docs" },
                { href: "/demo", label: "Live demo" },
                {
                  href: "https://github.com/Leeboom7/Agent-Commerce-Network",
                  label: "GitHub",
                },
              ]}
            />
            <FooterCol
              title="Protocol"
              links={[
                { href: "/docs#primitives", label: "Primitives" },
                { href: "/docs#connectors", label: "Connectors" },
                { href: "/docs#runtime", label: "Runtime model" },
              ]}
            />
          </div>
        </div>
        <div className="mt-10 border-t border-border pt-6 text-xs text-muted-foreground">
          {"\u00A9"} 2026 CoAgenta. An open Agent Commerce Network reference implementation.
        </div>
      </div>
    </footer>
  )
}

function FooterCol({
  title,
  links,
}: {
  title: string
  links: { href: string; label: string }[]
}) {
  return (
    <div>
      <h4 className="text-sm font-semibold">{title}</h4>
      <ul className="mt-3 space-y-2">
        {links.map((l) => (
          <li key={l.label}>
            <Link
              href={l.href}
              className="text-sm text-muted-foreground transition-colors hover:text-foreground"
            >
              {l.label}
            </Link>
          </li>
        ))}
      </ul>
    </div>
  )
}
