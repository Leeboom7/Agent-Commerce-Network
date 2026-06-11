"use client";

import { useMemo, useState } from "react";
import {
  Activity,
  AlertTriangle,
  BadgeCheck,
  Brain,
  Cable,
  CircleDollarSign,
  ClipboardCheck,
  FileArchive,
  FileCheck2,
  Gavel,
  Play,
  Radio,
  ShieldCheck,
} from "lucide-react";

import { AppHeader } from "@/components/app-header";
import { CgBadge, CgCard } from "@/components/ui/cg";
import { demoAgents, featuredTask } from "@/lib/demo-catalog";

type DemoResult = {
  contracts: Record<string, { contract_id?: string; status?: string; terms?: { price?: number; currency?: string } }>;
  verification_reports: Record<string, { verdict: string; pass_rate: number }>;
  arbitration: { case_id: string; ruling_type: string; remedy: { action?: string; penalty_to_seller?: number } };
  settlement: { total_cost: number; payments: Array<{ agent: string; amount: number; penalty: number }> };
  reputation: Record<string, { score: number; transactions: number; success_rate: number }>;
  events: Array<{ event: string; details: string; data?: Record<string, unknown> }>;
  qwen: {
    status: "live" | "fallback";
    plannerOutput: { summary?: string; workPackages?: string[]; selectedServices?: string[] } | string;
    negotiationRationale: string;
    arbitrationRationale: string;
    error?: string;
  };
  baseline: {
    gain: { fewer_errors_percent: number; lower_cost_percent: number; verified_percent: number };
  };
};

const objectTimeline = [
  { label: "TaskRequest", detail: "Buyer Agent creates vendor risk task", icon: ClipboardCheck },
  { label: "Qwen Planner", detail: "Decomposes specialist work", icon: Brain },
  { label: "AgentService", detail: "Matches external runtimes", icon: Cable },
  { label: "Proposal", detail: "Sellers negotiate remedy terms", icon: Activity },
  { label: "Agreement", detail: "Terms become machine-readable", icon: FileCheck2 },
  { label: "Artifact", detail: "Runtimes upload delivery bundles", icon: FileArchive },
  { label: "VerificationRun", detail: "Verifier flags unsupported claims", icon: ShieldCheck },
  { label: "DisputeCase", detail: "Evidence reaches arbitrator", icon: Gavel },
  { label: "Settlement", detail: "Credits and reputation update", icon: CircleDollarSign },
];

function renderPlanner(output: DemoResult["qwen"]["plannerOutput"]) {
  if (typeof output === "string") return output;
  return output.summary ?? "Qwen planner produced specialist work packages.";
}

export default function TransactionWorkbench() {
  const [result, setResult] = useState<DemoResult | null>(null);
  const [isRunning, setIsRunning] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const visibleEvents = useMemo(() => result?.events?.slice(-9) ?? [], [result]);
  const verification = result ? Object.values(result.verification_reports)[0] : null;

  async function runDemo() {
    setIsRunning(true);
    setError(null);
    setResult(null);

    try {
      const response = await fetch("/api/demo/run", { method: "POST" });
      const payload = await response.json();
      if (!response.ok) {
        throw new Error(payload?.message ?? "Demo run failed");
      }
      setResult(payload);
    } catch (runError) {
      setError(runError instanceof Error ? runError.message : "Unknown demo error");
    } finally {
      setIsRunning(false);
    }
  }

  return (
    <main className="cg-page">
      <AppHeader subtitle="Live transaction workbench" />

      <section className="cg-workbench-header">
        <div>
          <CgBadge tone={result ? "success" : "blue"}>{result ? "Run complete" : "Live protocol run"}</CgBadge>
          <h1>{featuredTask.title}</h1>
          <p>
            Run the Python commerce demo through the Next.js API route. The workbench keeps Qwen rationale,
            verification, arbitration, settlement, and baseline proof visible as operational evidence.
          </p>
        </div>
        <button className="cg-button cg-button--dark" type="button" disabled={isRunning} onClick={runDemo}>
          <Play size={16} />
          {isRunning ? "Running protocol..." : "Run Live Protocol"}
        </button>
      </section>

      {error ? (
        <section className="cg-error-panel">
          <AlertTriangle size={18} />
          <strong>Demo run failed</strong>
          <span>{error}</span>
        </section>
      ) : null}

      <section className="cg-workbench-grid">
        <aside className="cg-panel cg-workbench-timeline">
          <div className="cg-panel-heading">
            <div>
              <ClipboardCheck size={18} />
              <span>Transaction timeline</span>
            </div>
          </div>
          {objectTimeline.map((item, index) => {
            const ItemIcon = item.icon;
            const active = result || index < (isRunning ? 5 : 1);
            return (
              <article key={item.label} className={active ? "cg-timeline-step active" : "cg-timeline-step"}>
                <span>{String(index + 1).padStart(2, "0")}</span>
                <ItemIcon size={17} />
                <div>
                  <strong>{item.label}</strong>
                  <small>{item.detail}</small>
                </div>
              </article>
            );
          })}
        </aside>

        <section className="cg-workbench-center">
          <CgCard className="cg-current-object">
            <div className="cg-card-topline">
              <CgBadge tone={verification?.verdict === "failed" ? "danger" : result ? "success" : "neutral"}>
                {verification ? verification.verdict : "preview"}
              </CgBadge>
              <span>{result ? `${verification?.pass_rate ?? 0}% pass rate` : "waiting for run"}</span>
            </div>
            <h2>{result ? "Verification and dispute evidence" : "Commerce object preview"}</h2>
            <p>
              {result
                ? "The verifier output becomes evidence for arbitration and settlement. Failed claims are no longer hidden inside a chat transcript."
                : "Run the demo to produce contracts, verification reports, arbitration, settlement, reputation, and protocol events."}
            </p>
            <div className="cg-object-document">
              <div className="pass">Agreement: source-backed vendor risk brief</div>
              <div className="pass">Artifact: risk-brief.md + citation-map.json</div>
              <div className={result ? "fail" : ""}>Verification: unsupported claims trigger dispute review</div>
              <div className={result ? "pass" : ""}>Settlement: NC credits and reputation update</div>
            </div>
          </CgCard>

          <section className="cg-result-metrics">
            <CgCard>
              <span>Contracts</span>
              <strong>{result ? Object.keys(result.contracts).length : "-"}</strong>
              <small>agreement snapshots</small>
            </CgCard>
            <CgCard>
              <span>Total cost</span>
              <strong>{result ? `${result.settlement.total_cost.toFixed(2)} NC` : "-"}</strong>
              <small>demo credit ledger</small>
            </CgCard>
            <CgCard>
              <span>Ruling</span>
              <strong>{result?.arbitration.ruling_type ?? "-"}</strong>
              <small>{result?.arbitration.remedy.action ?? "pending"}</small>
            </CgCard>
            <CgCard>
              <span>Baseline gain</span>
              <strong>
                {result
                  ? `${result.baseline.gain.fewer_errors_percent}% / ${result.baseline.gain.lower_cost_percent}%`
                  : "-"}
              </strong>
              <small>fewer errors / lower cost</small>
            </CgCard>
          </section>

          {result ? (
            <CgCard className="cg-settlement-card">
              <div className="cg-panel-heading">
                <div>
                  <CircleDollarSign size={18} />
                  <span>Settlement ledger</span>
                </div>
                <CgBadge tone="success">credits cleared</CgBadge>
              </div>
              <div className="cg-settlement-rows">
                {result.settlement.payments.map((payment) => (
                  <div key={payment.agent} className="cg-settlement-row">
                    <span>{payment.agent}</span>
                    <small className={payment.penalty > 0 ? "penalty" : ""}>
                      {payment.penalty > 0 ? `-${payment.penalty.toFixed(2)} penalty` : "no penalty"}
                    </small>
                    <strong>{payment.amount.toFixed(2)} NC</strong>
                  </div>
                ))}
              </div>
            </CgCard>
          ) : null}

          {result ? (
            <CgCard className="cg-reputation-card">
              <div className="cg-panel-heading">
                <div>
                  <BadgeCheck size={18} />
                  <span>Reputation graph</span>
                </div>
              </div>
              <div className="cg-reputation-rows">
                {Object.entries(result.reputation).map(([agent, rep]) => (
                  <div key={agent} className="cg-reputation-row">
                    <span>{agent}</span>
                    <i>
                      <b style={{ width: `${Math.min(100, Math.round(rep.success_rate * 100))}%` }} />
                    </i>
                    <small>{rep.transactions} txns</small>
                    <strong>{rep.score.toFixed(1)}</strong>
                  </div>
                ))}
              </div>
            </CgCard>
          ) : null}
        </section>

        <aside className="cg-workbench-side">
          <CgCard className="cg-qwen-card">
            <div className="cg-panel-heading">
              <div>
                <Brain size={18} />
                <span>Qwen rationale</span>
              </div>
              <CgBadge tone={result?.qwen.status === "live" ? "success" : "neutral"}>
                {result ? result.qwen.status : "fallback"}
              </CgBadge>
            </div>
            <strong>{result ? renderPlanner(result.qwen.plannerOutput) : "Decompose task into specialist work packages."}</strong>
            <p>{result?.qwen.negotiationRationale ?? "Compare proposals by price, reputation, delivery, and remedy."}</p>
            <p>{result?.qwen.arbitrationRationale ?? "Read failed claims and agreement criteria before ruling."}</p>
          </CgCard>

          <CgCard>
            <div className="cg-panel-heading">
              <div>
                <Activity size={18} />
                <span>Protocol events</span>
              </div>
            </div>
            <div className="cg-event-console">
              {result ? (
                visibleEvents.length > 0 ? (
                  visibleEvents.map((event, index) => (
                    <div key={`${event.event}-${index}`}>
                      <span>{event.event}</span>
                      <strong>{event.details}</strong>
                    </div>
                  ))
                ) : (
                  <div>
                    <span>demo_complete</span>
                    <strong>Python protocol returned transaction proof.</strong>
                  </div>
                )
              ) : (
                <div>
                  <span>idle</span>
                  <strong>Click Run Live Protocol to execute the Python demo.</strong>
                </div>
              )}
            </div>
          </CgCard>

          <CgCard>
            <div className="cg-panel-heading">
              <div>
                <Radio size={18} />
                <span>External runtimes</span>
              </div>
            </div>
            <div className="cg-runtime-stack">
              {demoAgents
                .filter((agent) => agent.role !== "buyer")
                .map((agent) => (
                  <div key={agent.id}>
                    <BadgeCheck size={15} />
                    <span>{agent.name}</span>
                    <small>{agent.status}</small>
                  </div>
                ))}
            </div>
          </CgCard>
        </aside>
      </section>
    </main>
  );
}
