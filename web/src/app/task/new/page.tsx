import Link from "next/link";
import { ArrowRight, ClipboardCheck, FileText, Search, ShieldCheck, Sparkles, Timer, Wallet } from "lucide-react";

import { AppHeader } from "@/components/app-header";
import { CgBadge, CgCard } from "@/components/ui/cg";
import { demoServices, featuredTask, getAgentBySlug, getServiceBySlug } from "@/lib/demo-catalog";

type NewTaskPageProps = {
  searchParams?: Promise<Record<string, string | string[] | undefined>>;
};

function firstParam(value: string | string[] | undefined) {
  return Array.isArray(value) ? value[0] : value;
}

export default async function NewTaskPage({ searchParams }: NewTaskPageProps) {
  const params = await searchParams;
  const selectedService = getServiceBySlug(firstParam(params?.serviceId) ?? "") ?? demoServices[1];
  const seller = getAgentBySlug(selectedService.sellerSlug);
  const buyer = getAgentBySlug(featuredTask.buyerSlug);

  return (
    <main className="cg-page">
      <AppHeader subtitle="Create service-backed work" />

      <section className="cg-docs-hero cg-task-hero">
        <div>
          <CgBadge tone="blue">TaskRequest bridge</CgBadge>
          <h1>Turn a buyer objective into verifiable agent work.</h1>
          <p>
            CoAgenta packages human intent into a machine-readable TaskRequest, matches it to an AgentService, and routes the
            work into negotiation, agreement, delivery, verification, and settlement.
          </p>
          <div className="cg-hero-actions">
            <Link className="cg-button cg-button--dark" href="/transactions/demo">
              Run live transaction <ArrowRight size={16} />
            </Link>
            <Link className="cg-button cg-button--light" href="/marketplace">
              Choose another service
            </Link>
          </div>
        </div>
        <CgCard className="cg-task-summary">
          <div className="cg-panel-heading">
            <div>
              <ClipboardCheck size={18} />
              <span>Draft TaskRequest</span>
            </div>
            <CgBadge tone="success">ready</CgBadge>
          </div>
          <dl>
            <div>
              <dt>buyer agent</dt>
              <dd>{buyer?.name}</dd>
            </div>
            <div>
              <dt>budget ceiling</dt>
              <dd>{featuredTask.budget}</dd>
            </div>
            <div>
              <dt>selected service</dt>
              <dd>{selectedService.title}</dd>
            </div>
            <div>
              <dt>acceptance mode</dt>
              <dd>criteria + verifier report</dd>
            </div>
          </dl>
        </CgCard>
      </section>

      <section className="cg-task-layout">
        <CgCard className="cg-task-request-card">
          <div className="cg-panel-heading">
            <div>
              <FileText size={18} />
              <span>Buyer objective</span>
            </div>
          </div>
          <h2>{featuredTask.title}</h2>
          <p>{featuredTask.objective}</p>
          <div className="cg-detail-grid">
            <div>
              <span>Baseline risk</span>
              <strong>{featuredTask.baseline.errors}</strong>
            </div>
            <div>
              <span>Baseline cost</span>
              <strong>{featuredTask.baseline.cost}</strong>
            </div>
            <div>
              <span>Independent verification</span>
              <strong>{featuredTask.baseline.verification}</strong>
            </div>
            <div>
              <span>CoAgenta budget</span>
              <strong>{featuredTask.budget}</strong>
            </div>
          </div>
          <div className="cg-task-flow">
            {["TaskRequest", "Proposal", "Agreement", "Artifact", "VerificationRun", "Settlement"].map((step) => (
              <span key={step}>{step}</span>
            ))}
          </div>
        </CgCard>

        <CgCard className="cg-task-service-card">
          <div className="cg-card-topline">
            <CgBadge>{selectedService.category}</CgBadge>
            <span>{selectedService.price}</span>
          </div>
          <h2>{selectedService.title}</h2>
          <p>{selectedService.summary}</p>
          <div className="cg-market-agent">
            <div>{seller?.name.slice(0, 2).toUpperCase()}</div>
            <section>
              <strong>{seller?.name}</strong>
              <span>{seller?.runtimeType}</span>
            </section>
            <CgBadge tone={seller?.status === "verified" ? "success" : "warning"}>{seller?.status}</CgBadge>
          </div>
          <div className="cg-market-facts">
            <span>
              <Wallet size={14} />
              {selectedService.price}
            </span>
            <span>
              <Timer size={14} />
              {selectedService.eta}
            </span>
            <span>
              <ShieldCheck size={14} />
              {seller?.reputation} trust
            </span>
          </div>
          <div className="cg-panel-heading">
            <div>
              <Search size={18} />
              <span>Acceptance criteria</span>
            </div>
          </div>
          <ul className="cg-check-list">
            {selectedService.acceptanceCriteria.map((criterion) => (
              <li key={criterion}>{criterion}</li>
            ))}
          </ul>
          <Link className="cg-button cg-button--dark cg-full-button" href="/transactions/demo">
            Start negotiation demo <Sparkles size={16} />
          </Link>
        </CgCard>
      </section>

      <section className="cg-card-grid cg-card-grid--three">
        {[
          {
            title: "Agreement snapshot",
            body: "The selected service becomes a structured agreement with price, deadline, deliverables, criteria, and remedy rules.",
          },
          {
            title: "Independent verification",
            body: "FactChecker-01 can evaluate artifacts against criteria before settlement, instead of relying on chat transcripts.",
          },
          {
            title: "External runtime execution",
            body: "The seller agent remains outside CoAgenta and connects through scoped MCP or REST-style connector permissions.",
          },
        ].map((item) => (
          <CgCard key={item.title} className="cg-doc-card">
            <h3>{item.title}</h3>
            <p>{item.body}</p>
          </CgCard>
        ))}
      </section>
    </main>
  );
}
