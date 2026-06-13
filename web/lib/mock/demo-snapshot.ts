import type { DemoResult } from "../types"

// Packaged snapshot derived from the canonical Python demo output shape
// (demo/web_api.py -> run_web_demo). Used as a fallback when the live
// Python bridge is unavailable so the demo never breaks on stage.
export const DEMO_SNAPSHOT: DemoResult = {
  contracts: {
    data_analyst: { terms: { price: 45 } },
    report_writer: { terms: { price: 75 } },
    fact_checker: { terms: { price: 30 } },
  },
  verification_reports: {
    data_analyst: { verdict: "accepted", pass_rate: 1 },
    report_writer_initial: { verdict: "partial", pass_rate: 0.33 },
    report_writer_revised: { verdict: "accepted", pass_rate: 1 },
    fact_checker: { verdict: "accepted", pass_rate: 1 },
  },
  arbitration: {
    case_id: "case-7f3a91",
    ruling_type: "buyer_upheld",
    remedy: { action: "revise_and_penalize", penalty_rate: 0.1 },
  },
  settlement: {
    total_cost: 142.5,
    payments: [
      { agent: "agent-data-analyst-001", amount: 45, penalty: 0 },
      { agent: "agent-report-writer-001", amount: 67.5, penalty: 7.5 },
      { agent: "agent-fact-checker-001", amount: 30, penalty: 0 },
    ],
  },
  reputation: {
    "agent-data-analyst-001": { score: 93, transactions: 88, success_rate: 0.97 },
    "agent-report-writer-001": { score: 86, transactions: 64, success_rate: 0.91 },
    "agent-fact-checker-001": { score: 97, transactions: 121, success_rate: 0.99 },
  },
  events: [
    {
      event: "task_request_created",
      details: "Buyer Agent creates TaskRequest: AI vendor risk brief",
      data: { budget: "250 NC", buyer: "agent-orchestrator-001" },
    },
    {
      event: "qwen_planner_complete",
      details:
        "Qwen planner decomposes task into research, writing, verification, arbitration",
      data: { status: "fallback" },
    },
    {
      event: "agent_services_matched",
      details:
        "Marketplace matches external DataAnalyst, ReportWriter, FactChecker, and Arbitrator runtimes",
      data: { runtime_boundary: "external connector runtimes, not platform hosted" },
    },
    {
      event: "proposal_offer_received",
      details:
        "Seller agents submit offers with price, ETA, deliverables, and remedy clauses",
      data: { data_analyst: 45, report_writer: 75, fact_checker: 30 },
    },
    {
      event: "proposal_countered",
      details:
        "Buyer counters writer terms with revision requirement and penalty if claim verification fails",
      data: { counterparty: "agent-report-writer-001", penalty_rate: 0.1 },
    },
    {
      event: "agreement_snapshots_created",
      details: "Accepted proposals become machine-readable Agreements",
      data: { agreement_count: 3 },
    },
    {
      event: "external_runtime_execution",
      details:
        "Seller connectors poll paid Agreements and execute in their own runtimes",
      data: { hosting: "external", connector: "REST/OpenAPI adapter loop" },
    },
    {
      event: "artifact_delivery_submitted",
      details: "Research and writer runtimes upload artifacts and submit Delivery objects",
      data: { artifacts: ["vendor-data.md", "risk-brief.md", "citation-map.json"] },
    },
    {
      event: "verification_failed_claims",
      details: "Verifier runtime flags two unsupported claims before buyer acceptance",
      data: { fact_checker_verdict: "accepted", failed_claims: 2 },
    },
    {
      event: "dispute_case_opened",
      details: "Buyer opens DisputeCase with verifier evidence bundle",
      data: { evidence: ["failed-claims.md", "verification_report.json"] },
    },
    {
      event: "arbitration_ruling",
      details: "Qwen arbitration rationale supports buyer-upheld ruling and remedy",
      data: { ruling_type: "buyer_upheld", remedy: { action: "revise_and_penalize" } },
    },
    {
      event: "settlement_complete",
      details: "Demo ledger pays external agents, applies penalty, and updates reputation",
      data: {
        total_cost: 142.5,
        baseline_gain: { fewer_errors_percent: 50, lower_cost_percent: 34, verified_percent: 100 },
      },
    },
  ],
  qwen: {
    status: "fallback",
    plannerOutput: {
      summary:
        "Split the buyer request into research, writing, independent verification, and arbitration roles.",
      workPackages: [
        "collect market evidence and source links",
        "draft the AI vendor risk brief with claim-level citations",
        "verify acceptance criteria against artifacts",
        "resolve failed claims with evidence-backed ruling",
      ],
      selectedServices: [
        "market_research",
        "risk_brief_writing",
        "claim_verification",
        "dispute_arbitration",
      ],
    },
    negotiationRationale:
      "The buyer accepts specialist agents only after comparing price, reputation, delivery time, and remedy terms. The writer counteroffer includes a revision and penalty clause because claim-level verification is required.",
    arbitrationRationale:
      "The agreement requires cited factual claims. Verification evidence shows two unsupported claims, so the ruling upholds the buyer, requires revision, and applies the 10% penalty.",
  },
  baseline: {
    single_agent: { factual_errors: 4, cost_nc: 320, verified_percent: 0 },
    multi_agent: { factual_errors: 2, cost_nc: 210.33, verified_percent: 100 },
    gain: { fewer_errors_percent: 50, lower_cost_percent: 34, verified_percent: 100 },
  },
  runtimeBoundary: {
    hosting: "external",
    connector: "REST/OpenAPI polling adapter",
    secrets:
      "Agent API keys stay in runtime environment variables, never in browser bundles.",
  },
  source: "snapshot",
}
