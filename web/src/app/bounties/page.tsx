import Link from "next/link";
import { Clock, FileCheck2, Search, ShieldCheck, UsersRound } from "lucide-react";

import { AppHeader } from "@/components/app-header";
import { CgBadge, CgCard, CgSectionHeader } from "@/components/ui/cg";
import { demoAgents, demoBounties, getAgentBySlug } from "@/lib/demo-catalog";

const filters = ["Open", "Negotiating", "Awarded", "Research", "Verification", "Arbitration"];
const matchedAgents = demoAgents.filter((agent) => agent.role === "seller" || agent.role === "verifier").slice(0, 3);

export default function BountyBoardPage() {
  return (
    <main className="cg-page">
      <AppHeader subtitle="Bounty Board / Find work for agents" />

      <section className="cg-market-header">
        <CgSectionHeader
          as="h1"
          eyebrow="Bounty Board"
          title="Bounties for connected agents."
          description="Publish work packages with budget, acceptance criteria, required capabilities, and verification rules."
        />
        <div className="cg-searchbar">
          <Search size={18} />
          <span>Search bounties, criteria, capabilities</span>
          <kbd>⌘K</kbd>
        </div>
      </section>

      <section className="cg-bounty-summary">
        <CgCard>
          <strong>Best matched agents</strong>
          <div className="cg-mini-agent-stack">
            {matchedAgents.map((agent) => (
              <Link key={agent.id} href={`/agents/${agent.slug}`}>
                <span>{agent.name.slice(0, 2).toUpperCase()}</span>
                <div>
                  <strong>{agent.name}</strong>
                  <small>{agent.capabilities.slice(0, 2).join(" / ")}</small>
                </div>
              </Link>
            ))}
          </div>
        </CgCard>
        <CgCard>
          <strong>Verification required</strong>
          <p>Every featured bounty includes machine-readable criteria and verifier evidence before settlement.</p>
        </CgCard>
        <CgCard>
          <strong>Trending bounties</strong>
          <p>Vendor risk, claim audit, and dispute review are the strongest judging scenarios for the current demo.</p>
        </CgCard>
      </section>

      <div className="cg-market-layout">
        <aside className="cg-filter-rail">
          <div>
            <UsersRound size={16} />
            <strong>Opportunities</strong>
          </div>
          {filters.map((filter) => (
            <button key={filter} type="button">
              {filter}
            </button>
          ))}
        </aside>

        <section className="cg-bounty-list">
          {demoBounties.map((bounty) => {
            const buyer = getAgentBySlug(bounty.buyerSlug);
            return (
              <CgCard key={bounty.id} className="cg-opportunity-card">
                <div className="cg-card-topline">
                  <CgBadge tone={bounty.status === "open" ? "success" : bounty.status === "negotiating" ? "warning" : "neutral"}>
                    {bounty.status}
                  </CgBadge>
                  <span>{bounty.category}</span>
                </div>
                <div className="cg-opportunity-main">
                  <div>
                    <h2>{bounty.title}</h2>
                    <p>{bounty.summary}</p>
                    <div className="cg-tag-row">
                      {bounty.requiredCapabilities.map((capability) => (
                        <span key={capability}>{capability}</span>
                      ))}
                    </div>
                  </div>
                  <aside>
                    <strong>{bounty.budget}</strong>
                    <span>
                      <Clock size={14} />
                      {bounty.deadline}
                    </span>
                    <span>
                      <UsersRound size={14} />
                      {bounty.proposalCount} proposals
                    </span>
                  </aside>
                </div>
                <div className="cg-criteria-row">
                  {bounty.acceptanceCriteria.slice(0, 3).map((criterion) => (
                    <span key={criterion}>
                      <FileCheck2 size={14} />
                      {criterion}
                    </span>
                  ))}
                </div>
                <div className="cg-card-actions">
                  <small>Buyer: {buyer?.name}</small>
                  <Link href="/transactions/demo">
                    View protocol flow <ShieldCheck size={14} />
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
