// Core domain types for the CoAgenta operator console + two-sided network.
// These intentionally translate ACP protocol primitives into user-facing concepts.
// A "Deal" is the unifying lifecycle object that absorbs Proposal / Agreement /
// Artifact / Verification / Dispute / Settlement as timeline stages.

export type AgentStatus = "online" | "busy" | "offline"

export type ConnectorKind = "REST/OpenAPI" | "MCP" | "Agent Card"

export interface AgentCapability {
  label: string
  /** service_type used by the ACP registry */
  serviceType: string
}

export interface ReputationPoint {
  /** ISO date or short label */
  label: string
  score: number
}

export interface Agent {
  id: string
  name: string
  handle: string
  role: string
  summary: string
  status: AgentStatus
  connector: ConnectorKind
  /** external runtime — never platform hosted */
  runtimeRegion: string
  capabilities: AgentCapability[]
  /** base price in Network Credits */
  basePrice: number
  pricingModel: "negotiable" | "fixed" | "value-based"
  reputation: number
  successRate: number
  totalDeals: number
  totalEarned: number
  reputationHistory: ReputationPoint[]
  owned?: boolean
  responseEta: string
}

export interface Service {
  id: string
  agentId: string
  title: string
  description: string
  serviceType: string
  price: number
  pricingModel: "negotiable" | "fixed" | "value-based"
  eta: string
  acceptanceCriteria: string[]
  tags: string[]
  rating: number
}

export type TaskStatus = "open" | "negotiating" | "awarded" | "closed"

export interface NetworkTask {
  id: string
  title: string
  description: string
  buyerId: string
  budget: number
  deadline: string
  requiredCapabilities: string[]
  proposals: number
  status: TaskStatus
  postedAt: string
}

export type DealStage =
  | "proposal"
  | "agreement"
  | "delivery"
  | "verification"
  | "dispute"
  | "arbitration"
  | "settlement"
  | "reputation"

export type DealStatus =
  | "negotiating"
  | "active"
  | "delivered"
  | "verifying"
  | "disputed"
  | "settled"
  | "failed"

export interface DealTimelineNode {
  stage: DealStage
  title: string
  timestamp: string
  state: "done" | "current" | "failed" | "pending"
  summary: string
  /** optional structured details rendered when the node expands */
  details?: { label: string; value: string }[]
  /** verification verdict / arbitration ruling text */
  verdict?: string
}

export interface Deal {
  id: string
  title: string
  buyerId: string
  sellerId: string
  status: DealStatus
  price: number
  penalty: number
  netPayment: number
  createdAt: string
  deadline: string
  acceptanceCriteria: string[]
  rounds: number
  timeline: DealTimelineNode[]
}

export interface LedgerEntry {
  id: string
  from: string
  to: string
  amount: number
  reason: string
  dealId: string
  timestamp: string
}

// ---- Live demo (Python bridge) result shape ---------------------------------

export interface DemoQwen {
  status: "live" | "fallback"
  error?: string
  plannerOutput: {
    summary: string
    workPackages: string[]
    selectedServices: string[]
  }
  negotiationRationale: string
  arbitrationRationale: string
}

export interface DemoEvent {
  event: string
  details: string
  data: Record<string, unknown>
  timestamp?: string
}

export interface DemoResult {
  contracts: Record<string, unknown>
  verification_reports: Record<
    string,
    { verdict: string; pass_rate: number }
  >
  arbitration: {
    case_id: string
    ruling_type: string
    remedy: Record<string, unknown>
  }
  settlement: {
    total_cost: number
    payments: { agent: string; amount: number; penalty: number }[]
  }
  reputation: Record<
    string,
    { score: number; transactions: number; success_rate: number }
  >
  events: DemoEvent[]
  qwen: DemoQwen
  baseline: {
    single_agent: { factual_errors: number; cost_nc: number; verified_percent: number }
    multi_agent: { factual_errors: number; cost_nc: number; verified_percent: number }
    gain: { fewer_errors_percent: number; lower_cost_percent: number; verified_percent: number }
  }
  runtimeBoundary: {
    hosting: string
    connector: string
    secrets: string
  }
  /** injected by the API route to tell the UI whether this is live or a packaged snapshot */
  source?: "live" | "snapshot"
}
