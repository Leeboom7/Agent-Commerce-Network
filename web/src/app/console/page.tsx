import Link from "next/link";
import {
  Activity,
  ArrowRight,
  CircleDollarSign,
  ClipboardCheck,
  FileWarning,
  Radio,
  ShieldCheck,
} from "lucide-react";

import { AppHeader } from "@/components/app-header";
import { CgActivityFeed, CgBadge, CgMetric } from "@/components/ui/cg";
import {
  connectorHealth,
  consoleMetrics,
  demoAgents,
  recentProtocolEvents,
  transactionSummaries,
} from "@/lib/demo-catalog";

function statusTone(status: string) {
  if (status === "healthy" || status === "verified" || status === "settled") return "success";
  if (status === "degraded" || status === "needs_review" || status === "negotiating") return "warning";
  if (status === "running") return "blue";
  return "neutral";
}

export default function ConsolePage() {
  return (
    <main className="cg-page">
      <AppHeader subtitle="Operator console / Powered by ACP" />

      <div className="cg-app-layout">
        <aside className="cg-sidebar">
          <div className="cg-sidebar__label">Workspace</div>
          <strong>Qwen Hackathon Lab</strong>
          <nav aria-label="Console sections">
            <a href="#alerts" className="active">
              Overview
            </a>
            <a href="#transactions">Transactions</a>
            <a href="#agents">My Agents</a>
            <a href="#verification">Verification</a>
            <a href="#ledger">Ledger</a>
          </nav>
        </aside>

        <section className="cg-console-main">
          <div className="cg-console-header">
            <div>
              <CgBadge tone="success">Network online</CgBadge>
              <h1>Agent commerce operations</h1>
            </div>
            <Link className="cg-button cg-button--dark" href="/transactions/demo">
              Run live demo
            </Link>
          </div>

          {/* Triage: alerts & needs-attention front and center */}
          <section className="cg-console-alerts" id="alerts">
            <Link className="cg-signal-card cg-signal-card--actionable" href="/transactions/demo">
              <FileWarning size={18} />
              <div>
                <strong>2 failed claims ready for arbitration</strong>
                <span>Evidence bundle from FactChecker-01 is attached. Review and rule.</span>
              </div>
              <ArrowRight size={16} />
            </Link>
          </section>

          {/* Key metrics */}
          <section className="cg-console-metrics">
            {consoleMetrics.map((metric) => (
              <CgMetric key={metric.label} {...metric} />
            ))}
          </section>

          {/* Main grid: transactions (wide) + agent health + activity */}
          <section className="cg-console-grid">
            <article className="cg-panel cg-panel--wide" id="transactions">
              <div className="cg-panel-heading">
                <div>
                  <ClipboardCheck size={18} />
                  <span>Active transactions</span>
                </div>
                <Link href="/transactions/demo">Open workbench</Link>
              </div>
              <div className="cg-table">
                <div className="cg-table-row cg-table-row--head">
                  <span>Work</span>
                  <span>Stage</span>
                  <span>Budget</span>
                  <span>Status</span>
                </div>
                {transactionSummaries.map((transaction) => (
                  <Link
                    key={transaction.id}
                    className="cg-table-row"
                    href="/transactions/demo"
                  >
                    <div className="cg-table-title">
                      <strong>{transaction.title}</strong>
                      <small>{transaction.nextAction}</small>
                    </div>
                    <span className="cg-stage-cell">
                      {transaction.stage}
                      <i style={{ width: `${transaction.progress}%` }} />
                    </span>
                    <span className="cg-number">{transaction.budget}</span>
                    <CgBadge tone={statusTone(transaction.status)}>{transaction.status}</CgBadge>
                  </Link>
                ))}
              </div>
            </article>

            <article className="cg-panel" id="agents">
              <div className="cg-panel-heading">
                <div>
                  <Radio size={18} />
                  <span>Agent health</span>
                </div>
              </div>
              <div className="cg-health-list">
                {connectorHealth.map((connector) => {
                  const agent = demoAgents.find((item) => item.slug === connector.agentSlug);
                  return (
                    <Link key={connector.agentSlug} href={`/agents/${connector.agentSlug}`} className="cg-health-row">
                      <div>
                        <strong>{agent?.name}</strong>
                        <span>{connector.authScope}</span>
                      </div>
                      <small>
                        {connector.latency} / {connector.lastSync}
                      </small>
                      <CgBadge tone={statusTone(connector.status)}>{connector.status}</CgBadge>
                    </Link>
                  );
                })}
              </div>
            </article>

            <article className="cg-panel" id="activity">
              <div className="cg-panel-heading">
                <div>
                  <Activity size={18} />
                  <span>Protocol activity</span>
                </div>
              </div>
              <CgActivityFeed items={recentProtocolEvents} />
            </article>

            <article className="cg-panel" id="verification">
              <div className="cg-panel-heading">
                <div>
                  <ShieldCheck size={18} />
                  <span>Verification queue</span>
                </div>
              </div>
              <div className="cg-signal-card">
                <FileWarning size={18} />
                <strong>2 failed claims ready for arbitration</strong>
                <span>Evidence bundle from FactChecker-01 is attached to the agreement.</span>
              </div>
            </article>

            <article className="cg-panel" id="ledger">
              <div className="cg-panel-heading">
                <div>
                  <CircleDollarSign size={18} />
                  <span>Ledger</span>
                </div>
              </div>
              <div className="cg-ledger-card">
                <strong>1,240 NC</strong>
                <span>Demo credit balance across connected agent accounts.</span>
              </div>
            </article>
          </section>
        </section>
      </div>
    </main>
  );
}
