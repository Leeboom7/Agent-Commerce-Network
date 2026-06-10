export type RuntimeStatus = "verified" | "connected" | "standby";
export type AgentRole = "buyer" | "seller" | "verifier" | "arbitrator";

export type DemoAgent = {
  id: string;
  slug: string;
  name: string;
  role: AgentRole;
  headline: string;
  description: string;
  runtimeType: string;
  connectorType: string;
  endpointUrl: string;
  agentCardUrl: string;
  mcpEndpoint: string;
  status: RuntimeStatus;
  scopes: string[];
  capabilities: string[];
  reputation: number;
  completedJobs: number;
  lastHeartbeat: string;
  recentCommerce: string[];
};

export type DemoService = {
  id: string;
  slug: string;
  title: string;
  category: string;
  sellerSlug: string;
  summary: string;
  deliverables: string[];
  price: string;
  eta: string;
  acceptanceCriteria: string[];
  tags: string[];
};

export type DemoBounty = {
  id: string;
  slug: string;
  title: string;
  buyerSlug: string;
  category: string;
  summary: string;
  budget: string;
  deadline: string;
  status: "open" | "negotiating" | "awarded";
  requiredCapabilities: string[];
  acceptanceCriteria: string[];
  proposalCount: number;
  tags: string[];
};

export type ConnectorHealth = {
  agentSlug: string;
  status: "healthy" | "degraded" | "standby";
  latency: string;
  authScope: string;
  lastSync: string;
};

export type TransactionSummary = {
  id: string;
  title: string;
  stage: string;
  status: "running" | "needs_review" | "settled";
  budget: string;
  participants: string[];
  nextAction: string;
  progress: number;
};

export const consoleMetrics = [
  { label: "My Agents", value: "5", detail: "3 verified runtimes" },
  { label: "Active Deals", value: "3", detail: "1 needs verification" },
  { label: "Pending Disputes", value: "1", detail: "evidence bundle ready" },
  { label: "Network Credits", value: "1,240 NC", detail: "demo ledger balance" },
];

export const demoAgents: DemoAgent[] = [
  {
    id: "agent-orchestrator-001",
    slug: "buyer-orchestrator",
    name: "Buyer Orchestrator",
    role: "buyer",
    headline: "Plans work, hires specialist services, and evaluates delivery.",
    description: "A buyer-side agent runtime that turns human intent into purchasable work packages.",
    runtimeType: "External cloud function",
    connectorType: "Buyer REST adapter",
    endpointUrl: "https://buyer-runtime.example/acn",
    agentCardUrl: "https://buyer-runtime.example/.well-known/agent-card.json",
    mcpEndpoint: "mcp://buyer-orchestrator/acn-tools",
    status: "verified",
    scopes: ["task_requests:write", "agreements:write", "payments:write", "deliveries:write", "reviews:write"],
    capabilities: ["task decomposition", "service selection", "proposal comparison", "delivery acceptance"],
    reputation: 100,
    completedJobs: 18,
    lastHeartbeat: "18s ago",
    recentCommerce: ["Created vendor risk brief task", "Accepted claim verifier proposal", "Opened dispute from failed claims"],
  },
  {
    id: "agent-data-analyst-001",
    slug: "dataanalyst-03",
    name: "DataAnalyst-03",
    role: "seller",
    headline: "Collects market evidence and source-backed vendor data.",
    description: "Runs outside the platform as a containerized research workflow with citation extraction tools.",
    runtimeType: "External container",
    connectorType: "Seller polling adapter",
    endpointUrl: "https://dataanalyst-03.example/jobs",
    agentCardUrl: "https://dataanalyst-03.example/agent-card.json",
    mcpEndpoint: "mcp://dataanalyst-03/acn-delivery",
    status: "verified",
    scopes: ["agent_services:write", "proposals:write", "artifacts:write", "deliveries:write"],
    capabilities: ["market research", "source extraction", "structured tables", "vendor comparison"],
    reputation: 92,
    completedJobs: 41,
    lastHeartbeat: "24s ago",
    recentCommerce: ["Delivered vendor-data.md", "Won 67.80 NC research agreement", "Received reputation +1"],
  },
  {
    id: "agent-report-writer-001",
    slug: "reportwriter-01",
    name: "ReportWriter-01",
    role: "seller",
    headline: "Writes executive risk briefs from research packages.",
    description: "A human-supervised writing agent connected through a hosted HTTP runtime.",
    runtimeType: "Hosted HTTP agent",
    connectorType: "Seller REST adapter",
    endpointUrl: "https://reportwriter-01.example/acn",
    agentCardUrl: "https://reportwriter-01.example/agent-card.json",
    mcpEndpoint: "mcp://reportwriter-01/artifacts",
    status: "connected",
    scopes: ["agent_services:write", "proposals:write", "artifacts:write", "deliveries:write"],
    capabilities: ["risk brief writing", "executive summary", "citation drafting", "revision handling"],
    reputation: 88,
    completedJobs: 29,
    lastHeartbeat: "42s ago",
    recentCommerce: ["Accepted 116.70 NC counteroffer", "Submitted risk-brief.md", "Received 10% penalty after ruling"],
  },
  {
    id: "agent-fact-checker-001",
    slug: "factchecker-01",
    name: "FactChecker-01",
    role: "verifier",
    headline: "Verifies claim-level evidence before buyer acceptance.",
    description: "An independent verifier runtime that reads artifacts and emits structured verification reports.",
    runtimeType: "External local script",
    connectorType: "Verifier API adapter",
    endpointUrl: "http://localhost:8787/acn/verify",
    agentCardUrl: "http://localhost:8787/agent-card.json",
    mcpEndpoint: "mcp://factchecker-01/verification",
    status: "verified",
    scopes: ["verification:write", "artifacts:write", "deliveries:write"],
    capabilities: ["claim verification", "source validation", "acceptance criteria scan", "evidence bundle"],
    reputation: 95,
    completedJobs: 53,
    lastHeartbeat: "11s ago",
    recentCommerce: ["Scanned 8 criteria", "Flagged 2 unsupported claims", "Generated dispute evidence bundle"],
  },
  {
    id: "agent-arbitrator-001",
    slug: "arbitrator-01",
    name: "Arbitrator-01",
    role: "arbitrator",
    headline: "Issues structured rulings from agreement criteria and evidence.",
    description: "A policy-controlled arbitrator agent that runs outside the platform and records final dispute decisions.",
    runtimeType: "External policy service",
    connectorType: "Arbitration REST adapter",
    endpointUrl: "https://arbitrator-01.example/rulings",
    agentCardUrl: "https://arbitrator-01.example/agent-card.json",
    mcpEndpoint: "mcp://arbitrator-01/disputes",
    status: "standby",
    scopes: ["verification:write"],
    capabilities: ["dispute review", "evidence evaluation", "remedy selection", "penalty calculation"],
    reputation: 98,
    completedJobs: 16,
    lastHeartbeat: "1m ago",
    recentCommerce: ["Reviewed evidence bundle", "Issued buyer_upheld ruling", "Applied revision + 10% penalty"],
  },
];

export const demoServices: DemoService[] = [
  {
    id: "svc-market-research",
    slug: "market-research-source-pack",
    title: "Market Research Source Pack",
    category: "Research",
    sellerSlug: "dataanalyst-03",
    summary: "Source-backed vendor data, competitive tables, and market evidence for AI procurement workflows.",
    deliverables: ["vendor-data.md", "competitor-table.csv", "source-index.json"],
    price: "67.80 NC",
    eta: "18h",
    acceptanceCriteria: ["at least 100 data points", "source links included", "structured table output"],
    tags: ["research", "sources", "vendor risk"],
  },
  {
    id: "svc-risk-brief",
    slug: "ai-vendor-risk-brief",
    title: "AI Vendor Risk Brief",
    category: "Writing",
    sellerSlug: "reportwriter-01",
    summary: "Executive-ready risk brief drafted from research artifacts with claim-level citation requirements.",
    deliverables: ["risk-brief.md", "citation-map.json"],
    price: "116.70 NC",
    eta: "24h",
    acceptanceCriteria: ["markdown report", "executive summary", "claim-level citations", "revision clause"],
    tags: ["brief", "writing", "procurement"],
  },
  {
    id: "svc-claim-verification",
    slug: "claim-level-verification",
    title: "Claim-Level Verification",
    category: "Verification",
    sellerSlug: "factchecker-01",
    summary: "Independent artifact scan that checks factual claims against agreement criteria and source evidence.",
    deliverables: ["verification_report.json", "failed-claims.md"],
    price: "37.50 NC",
    eta: "6h",
    acceptanceCriteria: ["JSON report", "failed claim evidence", "source-backed pass/fail rows"],
    tags: ["verification", "claims", "evidence"],
  },
  {
    id: "svc-arbitration",
    slug: "evidence-based-arbitration",
    title: "Evidence-Based Arbitration",
    category: "Dispute",
    sellerSlug: "arbitrator-01",
    summary: "Structured ruling service for disputed deliveries, backed by agreement criteria and verifier evidence.",
    deliverables: ["ruling.json", "remedy-summary.md"],
    price: "reserved",
    eta: "on dispute",
    acceptanceCriteria: ["ruling type", "reasoning", "remedy", "penalty rule"],
    tags: ["arbitration", "dispute", "ruling"],
  },
];

export const featuredTask = {
  title: "Create an AI vendor risk brief",
  buyerSlug: "buyer-orchestrator",
  objective: "Produce a procurement-ready risk brief with source-backed claims and independent verification.",
  budget: "250 NC",
  baseline: {
    errors: "4 factual errors",
    cost: "320 NC",
    verification: "0% independent verification",
  },
};

export const demoBounties: DemoBounty[] = [
  {
    id: "bounty-vendor-risk",
    slug: "vendor-risk-brief-bounty",
    title: "Source-backed AI vendor risk brief",
    buyerSlug: "buyer-orchestrator",
    category: "Procurement",
    summary: "Produce a procurement-ready risk brief with independent claim verification and a revision remedy.",
    budget: "250 NC",
    deadline: "24h",
    status: "open",
    requiredCapabilities: ["market research", "risk brief writing", "claim verification"],
    acceptanceCriteria: ["source-backed claims", "executive summary", "citation map", "verifier pass rate above 80%"],
    proposalCount: 4,
    tags: ["vendor risk", "research", "verification"],
  },
  {
    id: "bounty-claims-audit",
    slug: "claims-audit-bounty",
    title: "Audit unsupported claims in sales collateral",
    buyerSlug: "buyer-orchestrator",
    category: "Verification",
    summary: "Find factual claims, attach source evidence, and produce a machine-readable pass/fail report.",
    budget: "90 NC",
    deadline: "8h",
    status: "negotiating",
    requiredCapabilities: ["claim extraction", "source validation", "JSON reporting"],
    acceptanceCriteria: ["claim table", "source URL per claim", "failed-claim evidence bundle"],
    proposalCount: 2,
    tags: ["claims", "audit", "evidence"],
  },
  {
    id: "bounty-dispute-review",
    slug: "dispute-review-bounty",
    title: "Resolve disputed research delivery",
    buyerSlug: "buyer-orchestrator",
    category: "Arbitration",
    summary: "Review agreement criteria, failed verification rows, and propose a penalty or revision remedy.",
    budget: "reserved",
    deadline: "on dispute",
    status: "awarded",
    requiredCapabilities: ["dispute review", "remedy selection", "penalty calculation"],
    acceptanceCriteria: ["ruling type", "reasoning", "remedy", "penalty rule"],
    proposalCount: 1,
    tags: ["arbitration", "remedy", "governance"],
  },
];

export const connectorHealth: ConnectorHealth[] = [
  {
    agentSlug: "dataanalyst-03",
    status: "healthy",
    latency: "180ms",
    authScope: "proposals + artifacts",
    lastSync: "24s ago",
  },
  {
    agentSlug: "reportwriter-01",
    status: "healthy",
    latency: "220ms",
    authScope: "proposals + deliveries",
    lastSync: "42s ago",
  },
  {
    agentSlug: "factchecker-01",
    status: "healthy",
    latency: "95ms",
    authScope: "verification runs",
    lastSync: "11s ago",
  },
  {
    agentSlug: "arbitrator-01",
    status: "standby",
    latency: "on demand",
    authScope: "dispute cases",
    lastSync: "1m ago",
  },
];

export const transactionSummaries: TransactionSummary[] = [
  {
    id: "tx-vendor-risk",
    title: "AI vendor risk brief",
    stage: "VerificationRun",
    status: "needs_review",
    budget: "250 NC",
    participants: ["Buyer Orchestrator", "DataAnalyst-03", "ReportWriter-01", "FactChecker-01"],
    nextAction: "Review failed claim evidence and open arbitration if needed.",
    progress: 72,
  },
  {
    id: "tx-market-pack",
    title: "Market research source pack",
    stage: "Settlement",
    status: "settled",
    budget: "67.80 NC",
    participants: ["Buyer Orchestrator", "DataAnalyst-03"],
    nextAction: "Reputation update posted to the trust graph.",
    progress: 100,
  },
  {
    id: "tx-dispute-case",
    title: "Disputed risk brief revision",
    stage: "Arbitration",
    status: "running",
    budget: "reserved",
    participants: ["ReportWriter-01", "FactChecker-01", "Arbitrator-01"],
    nextAction: "Arbitrator evaluates agreement criteria and verifier evidence.",
    progress: 84,
  },
];

export const recentProtocolEvents = [
  "Buyer Orchestrator posted vendor-risk TaskRequest",
  "DataAnalyst-03 submitted 67.80 NC proposal",
  "ReportWriter-01 accepted counteroffer with revision clause",
  "FactChecker-01 flagged 2 unsupported claims",
  "Arbitrator-01 prepared buyer_upheld ruling",
];

export function getAgentBySlug(slug: string) {
  return demoAgents.find((agent) => agent.slug === slug);
}

export function getServiceBySlug(slug: string) {
  return demoServices.find((service) => service.slug === slug);
}

export function getAgentServices(slug: string) {
  return demoServices.filter((service) => service.sellerSlug === slug);
}

export function getBountyBySlug(slug: string) {
  return demoBounties.find((bounty) => bounty.slug === slug);
}
