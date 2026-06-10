import Link from "next/link";

const appNavItems = [
  { href: "/console", label: "Console" },
  { href: "/marketplace", label: "Hire Agents" },
  { href: "/bounties", label: "Bounty Board" },
  { href: "/docs", label: "Docs" },
];

const landingNavItems = [
  { href: "#product", label: "Product" },
  { href: "/marketplace", label: "Marketplace" },
  { href: "/bounties", label: "Bounties" },
  { href: "/docs", label: "Docs" },
];

type AppHeaderProps = {
  subtitle?: string;
  variant?: "landing" | "app";
};

export function AppHeader({ subtitle = "Agent commerce network console", variant = "app" }: AppHeaderProps) {
  const navItems = variant === "landing" ? landingNavItems : appNavItems;

  return (
    <header className={variant === "landing" ? "cg-header cg-header--landing" : "cg-header"}>
      <Link className="brand-lockup" href="/">
        <div className="cg-brand-mark">C</div>
        <div>
          <div className="cg-brand-title">CoAgenta</div>
          <div className="cg-brand-subtitle">{subtitle}</div>
        </div>
      </Link>
      <nav className="cg-top-nav" aria-label="Primary navigation">
        {navItems.map((item) => (
          <Link key={item.href} href={item.href}>
            {item.label}
          </Link>
        ))}
      </nav>
      <div className="cg-header-actions">
        {variant === "landing" ? (
          <>
            <Link className="cg-link-button" href="https://github.com/Leeboom7/Agent-Commerce-Network">
              GitHub
            </Link>
            <Link className="cg-button cg-button--dark" href="/console">
              Launch Console
            </Link>
          </>
        ) : (
          <Link className="cg-button cg-button--dark" href="/transactions/demo">
            Run Demo
          </Link>
        )}
      </div>
    </header>
  );
}
