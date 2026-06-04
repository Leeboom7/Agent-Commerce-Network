/** Agent node on the network graph */
export interface AgentNodeData {
  id: string;
  name: string;
  serviceType: string;
  reputation: number; // 0-100
  totalTransactions: number;
  status: "online" | "busy" | "disputed" | "offline";
  capabilities: Record<string, string[]>;
}

/** Contract edge between agents */
export interface ContractEdgeData {
  id: string;
  sourceAgentId: string;
  targetAgentId: string;
  relationshipType: string;
  price: number;
  currency: string;
  status: "negotiating" | "active" | "delivered" | "accepted" | "disputed" | "resolved";
  acceptanceCriteria: string[];
}

/** An event in the demo timeline */
export interface DemoEvent {
  timestamp: string;
  type: "negotiation_round" | "contract_signed" | "delivery" | "verification"
    | "dispute" | "arbitration" | "settlement" | "reputation_update";
  actor: string;
  target?: string;
  message: string;
  data: Record<string, unknown>;
}

/** Full demo state */
export interface DemoState {
  phase: "idle" | "running" | "paused" | "complete";
  currentScene: number;
  totalScenes: number;
  agents: AgentNodeData[];
  contracts: ContractEdgeData[];
  events: DemoEvent[];
  ledgerBalance: number;
  totalCost: number;
}

/** Floating card metadata */
export interface FloatingCardSpec {
  id: string;
  type: "registry" | "feed" | "negotiation" | "contract" | "arbitration" | "ledger" | "reputation";
  title: string;
  position: { x: number; y: number };
  visible: boolean;
}
