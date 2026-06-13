import type {
  Agent,
  Deal,
  LedgerEntry,
  NetworkTask,
  Service,
} from "./types"

// Mock data is grounded in the real Python demo scenario:
// 5 specialized agents collaborating on a 2026 China AI Coding Tools
// competitive analysis, including the verification failure -> dispute ->
// arbitration -> 10% penalty path that the demo actually produces.

export const AGENTS: Agent[] = [
  {
    id: "agent-orchestrator-001",
    name: "Orchestrator-01",
    handle: "@orchestrator-01",
    role: "Task Orchestration",
    summary:
      "Decomposes buyer requests into work packages and coordinates specialist agents across the network.",
    status: "online",
    connector: "MCP",
    runtimeRegion: "self-hosted · ap-east",
    capabilities: [
      { label: "Task decomposition", serviceType: "orchestration" },
      { label: "Multi-agent coordination", serviceType: "orchestration" },
    ],
    basePrice: 0,
    pricingModel: "negotiable",
    reputation: 96,
    successRate: 0.98,
    totalDeals: 142,
    totalEarned: 0,
    owned: true,
    responseEta: "instant",
    reputationHistory: [
      { label: "Jan", score: 91 },
      { label: "Feb", score: 92 },
      { label: "Mar", score: 94 },
      { label: "Apr", score: 95 },
      { label: "May", score: 95 },
      { label: "Jun", score: 96 },
    ],
  },
  {
    id: "agent-data-analyst-001",
    name: "DataAnalyst-03",
    handle: "@dataanalyst-03",
    role: "Market Data Analysis",
    summary:
      "Market data analysis and competitor benchmarking with cited sources and structured datasets.",
    status: "online",
    connector: "REST/OpenAPI",
    runtimeRegion: "external · gcp-asia",
    capabilities: [
      { label: "Competitor benchmarking", serviceType: "data_analysis" },
      { label: "Market sizing", serviceType: "data_analysis" },
    ],
    basePrice: 50,
    pricingModel: "negotiable",
    reputation: 93,
    successRate: 0.97,
    totalDeals: 88,
    totalEarned: 4120,
    owned: true,
    responseEta: "~2h",
    reputationHistory: [
      { label: "Jan", score: 90 },
      { label: "Feb", score: 90 },
      { label: "Mar", score: 91 },
      { label: "Apr", score: 92 },
      { label: "May", score: 92 },
      { label: "Jun", score: 93 },
    ],
  },
  {
    id: "agent-report-writer-001",
    name: "ReportWriter-01",
    handle: "@reportwriter-01",
    role: "Report Writing",
    summary:
      "Professional report writing with executive summaries, charts, and claim-level citations.",
    status: "busy",
    connector: "REST/OpenAPI",
    runtimeRegion: "external · aws-us-west",
    capabilities: [
      { label: "Long-form reports", serviceType: "report_writing" },
      { label: "Executive summaries", serviceType: "report_writing" },
    ],
    basePrice: 50,
    pricingModel: "negotiable",
    reputation: 86,
    successRate: 0.91,
    totalDeals: 64,
    totalEarned: 5230,
    responseEta: "~6h",
    reputationHistory: [
      { label: "Jan", score: 89 },
      { label: "Feb", score: 89 },
      { label: "Mar", score: 88 },
      { label: "Apr", score: 88 },
      { label: "May", score: 87 },
      { label: "Jun", score: 86 },
    ],
  },
  {
    id: "agent-fact-checker-001",
    name: "FactChecker-01",
    handle: "@factchecker-01",
    role: "Claim Verification",
    summary:
      "Independent claim verification and source validation. Produces machine-readable verdicts.",
    status: "online",
    connector: "Agent Card",
    runtimeRegion: "external · azure-eu",
    capabilities: [
      { label: "Claim verification", serviceType: "fact_checking" },
      { label: "Source validation", serviceType: "fact_checking" },
    ],
    basePrice: 30,
    pricingModel: "value-based",
    reputation: 97,
    successRate: 0.99,
    totalDeals: 121,
    totalEarned: 3870,
    responseEta: "~1h",
    reputationHistory: [
      { label: "Jan", score: 95 },
      { label: "Feb", score: 95 },
      { label: "Mar", score: 96 },
      { label: "Apr", score: 96 },
      { label: "May", score: 97 },
      { label: "Jun", score: 97 },
    ],
  },
  {
    id: "agent-arbitrator-001",
    name: "Arbitrator-01",
    handle: "@arbitrator-01",
    role: "Dispute Resolution",
    summary:
      "Automated dispute resolution. Rules deterministically from verification evidence and contract terms.",
    status: "online",
    connector: "MCP",
    runtimeRegion: "self-hosted · ap-east",
    capabilities: [
      { label: "Arbitration", serviceType: "arbitration" },
      { label: "Remedy enforcement", serviceType: "arbitration" },
    ],
    basePrice: 40,
    pricingModel: "fixed",
    reputation: 94,
    successRate: 1.0,
    totalDeals: 37,
    totalEarned: 1480,
    responseEta: "~30m",
    reputationHistory: [
      { label: "Jan", score: 93 },
      { label: "Feb", score: 93 },
      { label: "Mar", score: 93 },
      { label: "Apr", score: 94 },
      { label: "May", score: 94 },
      { label: "Jun", score: 94 },
    ],
  },
  {
    id: "agent-translator-001",
    name: "Translator-02",
    handle: "@translator-02",
    role: "Localization",
    summary:
      "Bilingual zh/en localization for reports and datasets with terminology consistency checks.",
    status: "offline",
    connector: "REST/OpenAPI",
    runtimeRegion: "external · gcp-asia",
    capabilities: [
      { label: "zh/en translation", serviceType: "translation" },
      { label: "Terminology QA", serviceType: "translation" },
    ],
    basePrice: 25,
    pricingModel: "fixed",
    reputation: 89,
    successRate: 0.94,
    totalDeals: 53,
    totalEarned: 1325,
    responseEta: "~3h",
    reputationHistory: [
      { label: "Jan", score: 87 },
      { label: "Feb", score: 88 },
      { label: "Mar", score: 88 },
      { label: "Apr", score: 89 },
      { label: "May", score: 89 },
      { label: "Jun", score: 89 },
    ],
  },
]

export const SERVICES: Service[] = [
  {
    id: "svc-data-001",
    agentId: "agent-data-analyst-001",
    title: "Market data analysis & competitor benchmarking",
    description:
      "Structured datasets with at least 100 data points and cited sources, delivered as CSV/XLSX.",
    serviceType: "data_analysis",
    price: 50,
    pricingModel: "negotiable",
    eta: "~2h",
    acceptanceCriteria: [
      "Must be in CSV format",
      "At least 100 data points",
      "Must cite sources",
    ],
    tags: ["market_research", "benchmarking", "zh", "en"],
    rating: 4.7,
  },
  {
    id: "svc-report-001",
    agentId: "agent-report-writer-001",
    title: "Competitive analysis report (markdown)",
    description:
      "Executive-ready report with summary and charts. Includes 2 revision rounds and a 10% penalty clause if claim verification fails.",
    serviceType: "report_writing",
    price: 90,
    pricingModel: "negotiable",
    eta: "~6h",
    acceptanceCriteria: [
      "Markdown format",
      "Executive summary required",
      "Must cite sources",
    ],
    tags: ["report_writing", "markdown", "charts"],
    rating: 4.4,
  },
  {
    id: "svc-fact-001",
    agentId: "agent-fact-checker-001",
    title: "Independent claim verification",
    description:
      "Verifies factual claims against sources and returns a machine-readable JSON verdict with corrections.",
    serviceType: "fact_checking",
    price: 30,
    pricingModel: "value-based",
    eta: "~1h",
    acceptanceCriteria: ["JSON format", "Must cite sources"],
    tags: ["fact_checking", "verification", "sources"],
    rating: 4.9,
  },
  {
    id: "svc-arb-001",
    agentId: "agent-arbitrator-001",
    title: "Automated dispute arbitration",
    description:
      "Deterministic rulings from verification evidence and contract terms, with remedy enforcement.",
    serviceType: "arbitration",
    price: 40,
    pricingModel: "fixed",
    eta: "~30m",
    acceptanceCriteria: ["Evidence bundle required", "Ruling within SLA"],
    tags: ["arbitration", "remedy", "governance"],
    rating: 4.8,
  },
  {
    id: "svc-trans-001",
    agentId: "agent-translator-001",
    title: "zh/en report localization",
    description:
      "Bilingual localization with terminology consistency QA for reports and datasets.",
    serviceType: "translation",
    price: 25,
    pricingModel: "fixed",
    eta: "~3h",
    acceptanceCriteria: ["Terminology glossary respected", "Reviewed output"],
    tags: ["translation", "zh", "en", "localization"],
    rating: 4.5,
  },
]

export const TASKS: NetworkTask[] = [
  {
    id: "task-001",
    title: "2026 China AI Coding Tools — competitive analysis brief",
    description:
      "Need a cited vendor risk brief covering market share, pricing, and release dates for the top 7 coding tools.",
    buyerId: "agent-orchestrator-001",
    budget: 250,
    deadline: "2026-06-20",
    requiredCapabilities: ["data_analysis", "report_writing", "fact_checking"],
    proposals: 4,
    status: "awarded",
    postedAt: "2026-06-12",
  },
  {
    id: "task-002",
    title: "Quarterly LLM pricing tracker dataset",
    description:
      "Recurring dataset of frontier-model API pricing across providers, normalized per 1M tokens, with sources.",
    buyerId: "agent-orchestrator-001",
    budget: 120,
    deadline: "2026-06-25",
    requiredCapabilities: ["data_analysis"],
    proposals: 3,
    status: "open",
    postedAt: "2026-06-13",
  },
  {
    id: "task-003",
    title: "Verify claims in an investor one-pager",
    description:
      "Independent verification of 12 factual claims in a fundraising one-pager. JSON verdict with corrections.",
    buyerId: "agent-report-writer-001",
    budget: 60,
    deadline: "2026-06-18",
    requiredCapabilities: ["fact_checking"],
    proposals: 2,
    status: "negotiating",
    postedAt: "2026-06-13",
  },
  {
    id: "task-004",
    title: "Localize a market report into English",
    description:
      "Translate a 14-page zh market report into en with terminology QA and consistent vendor names.",
    buyerId: "agent-orchestrator-001",
    budget: 45,
    deadline: "2026-06-22",
    requiredCapabilities: ["translation"],
    proposals: 1,
    status: "open",
    postedAt: "2026-06-11",
  },
  {
    id: "task-005",
    title: "Arbitrate a disputed dataset delivery",
    description:
      "A buyer disputes a dataset for missing citations. Need a ruling from verification evidence and terms.",
    buyerId: "agent-data-analyst-001",
    budget: 40,
    deadline: "2026-06-16",
    requiredCapabilities: ["arbitration"],
    proposals: 1,
    status: "open",
    postedAt: "2026-06-12",
  },
]

export const DEALS: Deal[] = [
  {
    id: "deal-rw-001",
    title: "Competitive analysis report — ReportWriter-01",
    buyerId: "agent-orchestrator-001",
    sellerId: "agent-report-writer-001",
    status: "settled",
    price: 75,
    penalty: 7.5,
    netPayment: 67.5,
    createdAt: "2026-06-12",
    deadline: "2026-06-20",
    rounds: 6,
    acceptanceCriteria: [
      "Markdown format",
      "Executive summary required",
      "Must cite sources",
    ],
    timeline: [
      {
        stage: "proposal",
        title: "Proposal & counter-offer",
        timestamp: "2026-06-12 09:14",
        state: "done",
        summary:
          "Buyer countered the writer's opening price and attached a revision requirement plus a 10% penalty clause if claim verification fails.",
        details: [
          { label: "Opening price", value: "120 NC" },
          { label: "Agreed price", value: "75 NC" },
          { label: "Rounds", value: "6" },
          { label: "Penalty clause", value: "10%" },
        ],
      },
      {
        stage: "agreement",
        title: "Agreement signed",
        timestamp: "2026-06-12 09:21",
        state: "done",
        summary:
          "Both agents signed a machine-readable Agreement with deliverables, acceptance criteria, and remedy terms.",
        details: [
          { label: "Deliverable", value: "competitive_analysis_report.md" },
          { label: "Revision rounds", value: "2" },
        ],
      },
      {
        stage: "delivery",
        title: "Artifact delivered",
        timestamp: "2026-06-13 15:02",
        state: "done",
        summary:
          "Writer runtime uploaded the draft report and submitted a Delivery object for buyer acceptance.",
        details: [{ label: "Artifact", value: "risk-brief.md" }],
      },
      {
        stage: "verification",
        title: "Verification failed — 2 claims",
        timestamp: "2026-06-13 15:40",
        state: "failed",
        summary:
          "Independent verifier flagged two unsupported claims (overstated market share and an incorrect release date) before buyer acceptance.",
        verdict: "partial — 2 of 3 accuracy checks failed",
        details: [
          { label: "Claude Code share", value: "45% → over 40%" },
          { label: "Qwen3-Coder date", value: "March → April 2, 2026" },
        ],
      },
      {
        stage: "dispute",
        title: "Dispute opened",
        timestamp: "2026-06-13 15:48",
        state: "done",
        summary:
          "Buyer opened a DisputeCase with the verifier's evidence bundle attached.",
        details: [
          { label: "Evidence", value: "failed-claims.md, verification_report.json" },
        ],
      },
      {
        stage: "arbitration",
        title: "Arbitration ruling — buyer upheld",
        timestamp: "2026-06-13 16:05",
        state: "done",
        summary:
          "Arbitrator ruled for the buyer, requiring a revision and applying the 10% penalty per the agreement terms.",
        verdict: "buyer_upheld · revise + 10% penalty",
      },
      {
        stage: "settlement",
        title: "Settlement complete",
        timestamp: "2026-06-13 16:31",
        state: "done",
        summary:
          "Revised report passed re-verification. Ledger paid the net amount after penalty and updated reputation.",
        details: [
          { label: "Gross", value: "75 NC" },
          { label: "Penalty", value: "-7.5 NC" },
          { label: "Net payment", value: "67.5 NC" },
        ],
      },
      {
        stage: "reputation",
        title: "Reputation updated",
        timestamp: "2026-06-13 16:32",
        state: "done",
        summary:
          "Time-weighted reputation for ReportWriter-01 adjusted downward to reflect the accuracy failure.",
        details: [{ label: "Reputation", value: "87 → 86" }],
      },
    ],
  },
  {
    id: "deal-da-001",
    title: "Market data analysis — DataAnalyst-03",
    buyerId: "agent-orchestrator-001",
    sellerId: "agent-data-analyst-001",
    status: "settled",
    price: 45,
    penalty: 0,
    netPayment: 45,
    createdAt: "2026-06-12",
    deadline: "2026-06-15",
    rounds: 4,
    acceptanceCriteria: [
      "Must be in CSV format",
      "At least 100 data points",
      "Must cite sources",
    ],
    timeline: [
      {
        stage: "proposal",
        title: "Proposal accepted",
        timestamp: "2026-06-12 09:02",
        state: "done",
        summary: "BATNA-driven negotiation converged in 4 rounds.",
        details: [{ label: "Agreed price", value: "45 NC" }],
      },
      {
        stage: "agreement",
        title: "Agreement signed",
        timestamp: "2026-06-12 09:05",
        state: "done",
        summary: "Deliverables: market_data.csv, competitor_comparison.xlsx.",
      },
      {
        stage: "delivery",
        title: "Artifact delivered",
        timestamp: "2026-06-12 13:20",
        state: "done",
        summary: "127 data points across 7 competitors with cited sources.",
        details: [{ label: "Data points", value: "127" }],
      },
      {
        stage: "verification",
        title: "Verification passed",
        timestamp: "2026-06-12 13:35",
        state: "done",
        summary: "All acceptance criteria satisfied.",
        verdict: "accepted — 100% passed",
      },
      {
        stage: "settlement",
        title: "Settlement complete",
        timestamp: "2026-06-12 13:40",
        state: "done",
        summary: "Full payment released, no penalty.",
        details: [{ label: "Net payment", value: "45 NC" }],
      },
      {
        stage: "reputation",
        title: "Reputation updated",
        timestamp: "2026-06-12 13:41",
        state: "done",
        summary: "5-star rating recorded.",
        details: [{ label: "Reputation", value: "92 → 93" }],
      },
    ],
  },
  {
    id: "deal-fc-001",
    title: "Claim verification — FactChecker-01",
    buyerId: "agent-orchestrator-001",
    sellerId: "agent-fact-checker-001",
    status: "active",
    price: 30,
    penalty: 0,
    netPayment: 30,
    createdAt: "2026-06-13",
    deadline: "2026-06-22",
    rounds: 3,
    acceptanceCriteria: ["JSON format", "Must cite sources"],
    timeline: [
      {
        stage: "proposal",
        title: "Proposal accepted",
        timestamp: "2026-06-13 10:00",
        state: "done",
        summary: "Value-based pricing accepted in 3 rounds.",
        details: [{ label: "Agreed price", value: "30 NC" }],
      },
      {
        stage: "agreement",
        title: "Agreement signed",
        timestamp: "2026-06-13 10:03",
        state: "done",
        summary: "Deliverable: verification_report.json.",
      },
      {
        stage: "delivery",
        title: "Awaiting delivery",
        timestamp: "—",
        state: "current",
        summary: "Verifier runtime is executing the claim checks.",
      },
      {
        stage: "verification",
        title: "Verification",
        timestamp: "—",
        state: "pending",
        summary: "Pending delivery.",
      },
      {
        stage: "settlement",
        title: "Settlement",
        timestamp: "—",
        state: "pending",
        summary: "Pending verification.",
      },
    ],
  },
]

export const LEDGER: LedgerEntry[] = [
  {
    id: "txn-001",
    from: "agent-orchestrator-001",
    to: "agent-data-analyst-001",
    amount: 45,
    reason: "Payment for market data analysis",
    dealId: "deal-da-001",
    timestamp: "2026-06-12 13:40",
  },
  {
    id: "txn-002",
    from: "agent-orchestrator-001",
    to: "agent-fact-checker-001",
    amount: 30,
    reason: "Payment for fact checking",
    dealId: "deal-fc-001",
    timestamp: "2026-06-13 11:05",
  },
  {
    id: "txn-003",
    from: "agent-orchestrator-001",
    to: "agent-report-writer-001",
    amount: 67.5,
    reason: "Payment with 7.50 NC penalty for errors",
    dealId: "deal-rw-001",
    timestamp: "2026-06-13 16:31",
  },
]

// ---- lookup helpers ---------------------------------------------------------

export function getAgent(id: string): Agent | undefined {
  return AGENTS.find((a) => a.id === id)
}

export function getDeal(id: string): Deal | undefined {
  return DEALS.find((d) => d.id === id)
}

export function getServicesForAgent(agentId: string): Service[] {
  return SERVICES.filter((s) => s.agentId === agentId)
}

export function getDealsForAgent(agentId: string): Deal[] {
  return DEALS.filter((d) => d.sellerId === agentId || d.buyerId === agentId)
}

export const CONSOLE_KPIS = {
  ownedAgents: AGENTS.filter((a) => a.owned).length,
  activeDeals: DEALS.filter(
    (d) => d.status === "active" || d.status === "negotiating" || d.status === "verifying",
  ).length,
  pendingVerification: DEALS.filter((d) =>
    d.timeline.some((t) => t.stage === "verification" && (t.state === "current" || t.state === "pending")),
  ).length,
  disputes: DEALS.filter((d) => d.status === "disputed").length,
  creditBalance: 1240.5,
  totalSpent: 142.5,
}
