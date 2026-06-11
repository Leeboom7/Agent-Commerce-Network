import { Activity, BadgeCheck, CircleDollarSign, Radio, ShieldCheck } from "lucide-react";

import { connectorHealth, consoleMetrics, demoAgents, transactionSummaries } from "@/lib/demo-catalog";

export function ProductFrame() {
  return (
    <div className="cg-product-frame" aria-label="CoAgenta console preview">
      <div className="cg-product-frame__bar">
        <div aria-hidden="true">
          <span />
          <span />
          <span />
        </div>
        <strong>Network Console</strong>
        <small>live</small>
      </div>
      <div className="cg-product-frame__body">
        <section className="cg-product-summary">
          {consoleMetrics.slice(0, 3).map((metric) => (
            <div key={metric.label}>
              <span>{metric.label}</span>
              <strong>{metric.value}</strong>
            </div>
          ))}
        </section>
        <section className="cg-product-main">
          <div className="cg-product-panel cg-product-panel--large">
            <div className="cg-mini-heading">
              <Activity size={14} />
              <span>Active transactions</span>
            </div>
            {transactionSummaries.map((transaction) => (
              <div key={transaction.id} className="cg-preview-transaction">
                <div>
                  <strong>{transaction.title}</strong>
                  <span>{transaction.stage}</span>
                </div>
                <small>{transaction.budget}</small>
              </div>
            ))}
          </div>
          <div className="cg-product-panel">
            <div className="cg-mini-heading">
              <Radio size={14} />
              <span>Agent health</span>
            </div>
            {connectorHealth.slice(0, 3).map((connector) => {
              const agent = demoAgents.find((item) => item.slug === connector.agentSlug);
              return (
                <div key={connector.agentSlug} className="cg-preview-agent">
                  <BadgeCheck size={14} />
                  <div>
                    <strong>{agent?.name}</strong>
                    <span>{connector.lastSync}</span>
                  </div>
                </div>
              );
            })}
          </div>
        </section>
        <section className="cg-proof-strip">
          <div>
            <ShieldCheck size={15} />
            <span>verified artifact</span>
          </div>
          <div>
            <CircleDollarSign size={15} />
            <span>settled NC ledger</span>
          </div>
        </section>
      </div>
    </div>
  );
}
