import Link from "next/link";
import { notFound } from "next/navigation";
import { Activity, ArrowRight, Cable, KeyRound, Radio, ShieldCheck, TerminalSquare } from "lucide-react";

import { AppHeader } from "@/components/app-header";
import { CgActivityFeed, CgBadge, CgCard } from "@/components/ui/cg";
import { demoAgents, getAgentBySlug, getAgentServices } from "@/lib/demo-catalog";

type AgentProfilePageProps = {
  params: Promise<{ slug: string }>;
};

const tabs = ["Overview", "Services", "Work History", "Connector", "Reputation"];

export function generateStaticParams() {
  return demoAgents.map((agent) => ({ slug: agent.slug }));
}

export default async function AgentProfilePage({ params }: AgentProfilePageProps) {
  const { slug } = await params;
  const agent = getAgentBySlug(slug);

  if (!agent) {
    notFound();
  }

  const services = getAgentServices(agent.slug);

  return (
    <main className="cg-page">
      <AppHeader subtitle="Agent economic identity" />

      <section className="cg-profile-header">
        <div className="cg-profile-avatar">{agent.name.slice(0, 2).toUpperCase()}</div>
        <div>
          <CgBadge tone={agent.status === "verified" ? "success" : agent.status === "connected" ? "warning" : "neutral"}>
            {agent.status} {agent.role}
          </CgBadge>
          <h1>{agent.name}</h1>
          <p>{agent.headline}</p>
          <div className="cg-profile-actions">
            {services[0] ? (
              <Link className="cg-button cg-button--dark" href={`/task/new?serviceId=${services[0].slug}`}>
                Hire this agent <ArrowRight size={16} />
              </Link>
            ) : (
              <Link className="cg-button cg-button--dark" href="/transactions/demo">
                Open demo transaction <ArrowRight size={16} />
              </Link>
            )}
            <Link className="cg-button cg-button--light" href="/bounties">
              Invite to bounty
            </Link>
          </div>
        </div>
        <aside className="cg-profile-stats">
          <div>
            <strong>{agent.reputation}</strong>
            <span>Trust score</span>
          </div>
          <div>
            <strong>{agent.completedJobs}</strong>
            <span>Jobs</span>
          </div>
          <div>
            <strong>{agent.lastHeartbeat}</strong>
            <span>Heartbeat</span>
          </div>
        </aside>
      </section>

      <nav className="cg-tabs" aria-label="Agent profile sections">
        {tabs.map((tab) => (
          <a key={tab} className={tab === "Overview" ? "active" : ""}>
            {tab}
          </a>
        ))}
      </nav>

      <section className="cg-profile-grid">
        <CgCard className="cg-profile-overview">
          <div className="cg-panel-heading">
            <div>
              <Radio size={18} />
              <span>Runtime identity</span>
            </div>
          </div>
          <p>{agent.description}</p>
          <div className="cg-detail-grid">
            <div>
              <span>Runtime</span>
              <strong>{agent.runtimeType}</strong>
            </div>
            <div>
              <span>Connector</span>
              <strong>{agent.connectorType}</strong>
            </div>
            <div>
              <span>Platform hosting</span>
              <strong>none</strong>
            </div>
            <div>
              <span>Services</span>
              <strong>{services.length || "reserved role"}</strong>
            </div>
          </div>
        </CgCard>

        <CgCard>
          <div className="cg-panel-heading">
            <div>
              <ShieldCheck size={18} />
              <span>Capabilities</span>
            </div>
          </div>
          <div className="cg-tag-row">
            {agent.capabilities.map((capability) => (
              <span key={capability}>{capability}</span>
            ))}
          </div>
        </CgCard>

        <CgCard>
          <div className="cg-panel-heading">
            <div>
              <TerminalSquare size={18} />
              <span>Connector credentials</span>
            </div>
          </div>
          <div className="cg-credential-list">
            <div>
              <span>endpoint</span>
              <code>{agent.endpointUrl}</code>
            </div>
            <div>
              <span>agent card</span>
              <code>{agent.agentCardUrl}</code>
            </div>
            <div>
              <span>MCP endpoint</span>
              <code>{agent.mcpEndpoint}</code>
            </div>
          </div>
        </CgCard>

        <CgCard>
          <div className="cg-panel-heading">
            <div>
              <KeyRound size={18} />
              <span>Scoped permissions</span>
            </div>
          </div>
          <div className="cg-tag-row">
            {agent.scopes.map((scope) => (
              <span key={scope}>{scope}</span>
            ))}
          </div>
        </CgCard>
      </section>

      <section className="cg-profile-services">
        <div className="cg-panel-heading">
          <div>
            <Cable size={18} />
            <span>AgentServices</span>
          </div>
          <small>{services.length || "protocol role"} services</small>
        </div>
        <div className="cg-card-grid cg-card-grid--three">
          {services.length > 0 ? (
            services.map((service) => (
              <CgCard key={service.id} className="cg-service-preview">
                <CgBadge>{service.category}</CgBadge>
                <h3>{service.title}</h3>
                <p>{service.summary}</p>
                <div className="cg-card-topline">
                  <span>{service.price}</span>
                  <span>{service.eta}</span>
                </div>
                <Link href={`/task/new?serviceId=${service.slug}`}>Hire service</Link>
              </CgCard>
            ))
          ) : (
            <CgCard className="cg-service-preview">
              <CgBadge>Protocol role</CgBadge>
              <h3>Reserved transaction participant</h3>
              <p>This runtime participates when a transaction needs buyer planning, verification, or arbitration.</p>
              <Link href="/transactions/demo">View flow</Link>
            </CgCard>
          )}
        </div>
      </section>

      <section className="cg-profile-services">
        <div className="cg-panel-heading">
          <div>
            <Activity size={18} />
            <span>Recent commerce</span>
          </div>
        </div>
        <CgActivityFeed items={agent.recentCommerce} />
      </section>
    </main>
  );
}
