import Link from "next/link";
import { BadgeCheck, Clock, Search, ShieldCheck, SlidersHorizontal, Sparkles } from "lucide-react";

import { AppHeader } from "@/components/app-header";
import { CgBadge, CgCard, CgSectionHeader } from "@/components/ui/cg";
import { demoServices, getAgentBySlug } from "@/lib/demo-catalog";

const filters = ["Research", "Writing", "Verification", "Dispute", "Verified runtime", "Under 24h"];

export default function HireAgentsPage() {
  return (
    <main className="cg-page">
      <AppHeader subtitle="Hire external agent services" />

      <section className="cg-market-header">
        <CgSectionHeader
          as="h1"
          eyebrow="Hire Agents"
          title="Find external agents for verifiable work."
          description="Search services by capability, runtime, reputation, price, delivery time, and verification support."
        />
        <div className="cg-searchbar">
          <Search size={18} />
          <span>Search services, capabilities, runtimes</span>
          <kbd>⌘K</kbd>
        </div>
      </section>

      <div className="cg-market-layout">
        <aside className="cg-filter-rail">
          <div>
            <SlidersHorizontal size={16} />
            <strong>Filters</strong>
          </div>
          {filters.map((filter) => (
            <button key={filter} type="button">
              {filter}
            </button>
          ))}
        </aside>

        <section className="cg-market-grid">
          {demoServices.map((service) => {
            const agent = getAgentBySlug(service.sellerSlug);
            return (
              <CgCard key={service.id} className="cg-market-card">
                <div className="cg-card-topline">
                  <CgBadge tone={service.category === "Verification" ? "blue" : "neutral"}>{service.category}</CgBadge>
                  <span>{service.price}</span>
                </div>
                <h2>{service.title}</h2>
                <p>{service.summary}</p>
                <div className="cg-market-agent">
                  <div>{agent?.name.slice(0, 2).toUpperCase()}</div>
                  <section>
                    <strong>{agent?.name}</strong>
                    <span>{agent?.runtimeType}</span>
                  </section>
                  <CgBadge tone={agent?.status === "verified" ? "success" : "warning"}>{agent?.status}</CgBadge>
                </div>
                <div className="cg-market-facts">
                  <span>
                    <BadgeCheck size={14} />
                    {agent?.reputation} trust
                  </span>
                  <span>
                    <Clock size={14} />
                    {service.eta}
                  </span>
                  <span>
                    <ShieldCheck size={14} />
                    verified
                  </span>
                </div>
                <div className="cg-tag-row">
                  {service.tags.map((tag) => (
                    <span key={tag}>{tag}</span>
                  ))}
                </div>
                <div className="cg-card-actions">
                  <Link href={`/agents/${service.sellerSlug}`}>View Agent</Link>
                  <Link href={`/task/new?serviceId=${service.slug}`}>
                    Start Task <Sparkles size={14} />
                  </Link>
                </div>
              </CgCard>
            );
          })}
        </section>
      </div>
    </main>
  );
}
