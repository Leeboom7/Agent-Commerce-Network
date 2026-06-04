"use client";

import { useState, useCallback, useMemo } from "react";
import {
  ReactFlow,
  Background,
  Controls,
  type Node,
  type Edge,
  MarkerType,
} from "@xyflow/react";
import "@xyflow/react/dist/style.css";
import { Play, Pause, RotateCcw } from "lucide-react";

// ── Demo data (static for now — will be wired to FastAPI in Phase 4) ──

const AGENTS = [
  { id: "agent-orchestrator-001", name: "Orchestrator", type: "orchestrator", rep: 100, txns: 500, status: "online" as const, caps: {} },
  { id: "agent-datanalyst-003", name: "DataAnalyst-03", type: "data_analysis", rep: 92, txns: 127, status: "online" as const, caps: { languages: ["zh","en"], domain: ["tech_market"] } },
  { id: "agent-reportwriter-001", name: "ReportWriter-01", type: "report_writing", rep: 88, txns: 89, status: "busy" as const, caps: { languages: ["zh","en"], formats: ["markdown","pdf"] } },
  { id: "agent-factchecker-001", name: "FactChecker-01", type: "fact_checking", rep: 95, txns: 203, status: "online" as const, caps: { languages: ["zh","en"], tools: ["web_search"] } },
  { id: "agent-arbitrator-001", name: "Arbitrator-01", type: "arbitration", rep: 98, txns: 56, status: "online" as const, caps: {} },
];

const INITIAL_EDGES: Edge[] = [];

const INITIAL_NODES: Node[] = AGENTS.map((a, i) => {
  const angle = (i / AGENTS.length) * Math.PI * 2 - Math.PI / 2;
  const r = 220;
  return {
    id: a.id,
    type: "agentNode",
    position: { x: 400 + Math.cos(angle) * r, y: 300 + Math.sin(angle) * r },
    data: {
      label: a.name,
      agentId: a.id,
      reputation: a.rep,
      status: a.status,
      serviceType: a.type,
      totalTransactions: a.txns,
    },
  };
});

// ── Demo scenes ──

type Scene = {
  title: string;
  nodes: Node[];
  edges: Edge[];
  cards: { type: string; title: string; content: string[] };
};

const SCENES: Record<number, Scene> = {
  0: { title: "Idle", nodes: INITIAL_NODES, edges: [], cards: { type: "", title: "", content: [] } },
  1: {
    title: "SCENE 1: Agent Registration",
    nodes: INITIAL_NODES.map((n) => ({
      ...n,
      data: { ...n.data, status: "online" },
    })),
    edges: [],
    cards: { type: "registry", title: "AGENT REGISTRY", content: AGENTS.map((a) => `${a.name} | ${a.type} | ${a.rep}/100 [OK]`) },
  },
  2: {
    title: "SCENE 2: Service Discovery",
    nodes: INITIAL_NODES,
    edges: [
      { id: "e-search-1", source: "agent-orchestrator-001", target: "agent-datanalyst-003", type: "smoothstep", animated: true, style: { stroke: "#FFE033", strokeWidth: 2, strokeDasharray: "6 4" }, markerEnd: { type: MarkerType.Arrow, color: "#FFE033" } },
      { id: "e-search-2", source: "agent-orchestrator-001", target: "agent-reportwriter-001", type: "smoothstep", animated: true, style: { stroke: "#FFE033", strokeWidth: 2, strokeDasharray: "6 4" }, markerEnd: { type: MarkerType.Arrow, color: "#FFE033" } },
      { id: "e-search-3", source: "agent-orchestrator-001", target: "agent-factchecker-001", type: "smoothstep", animated: true, style: { stroke: "#FFE033", strokeWidth: 2, strokeDasharray: "6 4" }, markerEnd: { type: MarkerType.Arrow, color: "#FFE033" } },
    ],
    cards: { type: "feed", title: "LIVE FEED", content: [
      'Orchestrator: "I need a competitive analysis of the 2026 China AI Coding Tools market."',
      "SEARCH: data_analysis → 1 result (DataAnalyst-03, 92/100)",
      "SEARCH: report_writing → 1 result (ReportWriter-01, 88/100)",
      "SEARCH: fact_checking → 1 result (FactChecker-01, 95/100)",
    ]},
  },
  3: {
    title: "SCENE 3: Multi-Agent Negotiation",
    nodes: INITIAL_NODES.map((n) => n.id === "agent-reportwriter-001" ? { ...n, data: { ...n.data, status: "busy" } } : n),
    edges: [
      { id: "e-nego-1", source: "agent-orchestrator-001", target: "agent-datanalyst-003", type: "smoothstep", animated: true, style: { stroke: "#FFE033", strokeWidth: 2, strokeDasharray: "6 4" }, markerEnd: { type: MarkerType.Arrow, color: "#FFE033" }, label: "67.80 NC" },
      { id: "e-nego-2", source: "agent-orchestrator-001", target: "agent-reportwriter-001", type: "smoothstep", animated: true, style: { stroke: "#FFE033", strokeWidth: 2, strokeDasharray: "6 4" }, markerEnd: { type: MarkerType.Arrow, color: "#FFE033" }, label: "116.70 NC" },
      { id: "e-nego-3", source: "agent-orchestrator-001", target: "agent-factchecker-001", type: "smoothstep", animated: true, style: { stroke: "#FFE033", strokeWidth: 2, strokeDasharray: "6 4" }, markerEnd: { type: MarkerType.Arrow, color: "#FFE033" }, label: "37.50 NC" },
    ],
    cards: { type: "negotiation", title: "NEGOTIATION", content: [
      "Orchestrator → DataAnalyst: OFFER 40 NC",
      "DataAnalyst → Orchestrator: COUNTER 50 NC (reputation 92 justifies premium)",
      "Orchestrator → DataAnalyst: ACCEPT at 50 NC",
      "Orchestrator → ReportWriter: OFFER 60 NC",
      "ReportWriter → Orchestrator: COUNTER 116.70 NC",
      "Orchestrator → ReportWriter: ACCEPT at 116.70 NC",
      "Orchestrator → FactChecker: OFFER 25 NC",
      "FactChecker → Orchestrator: COUNTER 37.50 NC",
      "Orchestrator → FactChecker: ACCEPT at 37.50 NC",
    ]},
  },
  4: {
    title: "SCENE 4: Contract Signing",
    nodes: INITIAL_NODES,
    edges: [
      { id: "e-ctr-1", source: "agent-orchestrator-001", target: "agent-datanalyst-003", type: "smoothstep", style: { stroke: "#111111", strokeWidth: 3 }, markerEnd: { type: MarkerType.ArrowClosed, color: "#111111" }, label: "CONTRACT: 67.80 NC" },
      { id: "e-ctr-2", source: "agent-orchestrator-001", target: "agent-reportwriter-001", type: "smoothstep", style: { stroke: "#111111", strokeWidth: 3 }, markerEnd: { type: MarkerType.ArrowClosed, color: "#111111" }, label: "CONTRACT: 116.70 NC" },
      { id: "e-ctr-3", source: "agent-orchestrator-001", target: "agent-factchecker-001", type: "smoothstep", style: { stroke: "#111111", strokeWidth: 3 }, markerEnd: { type: MarkerType.ArrowClosed, color: "#111111" }, label: "CONTRACT: 37.50 NC" },
    ],
    cards: { type: "contract", title: "ACTIVE CONTRACTS", content: [
      "contract-a1b2: DataAnalyst — 67.80 NC [ACTIVE]",
      "contract-dc51: ReportWriter — 116.70 NC [ACTIVE]",
      "contract-bb83: FactChecker — 37.50 NC [ACTIVE]",
    ]},
  },
  5: {
    title: "SCENE 5: Delivery & Verification",
    nodes: INITIAL_NODES.map((n) => {
      if (n.id === "agent-datanalyst-003") return { ...n, data: { ...n.data, status: "online", reputation: 93 } };
      if (n.id === "agent-reportwriter-001") return { ...n, data: { ...n.data, status: "disputed", reputation: 87 } };
      return n;
    }),
    edges: [
      { id: "e-ver-1", source: "agent-orchestrator-001", target: "agent-datanalyst-003", type: "smoothstep", style: { stroke: "#22C55E", strokeWidth: 3 }, markerEnd: { type: MarkerType.ArrowClosed, color: "#22C55E" }, label: "[OK] ACCEPTED" },
      { id: "e-ver-2", source: "agent-orchestrator-001", target: "agent-reportwriter-001", type: "smoothstep", style: { stroke: "#FF5E5E", strokeWidth: 3 }, markerEnd: { type: MarkerType.ArrowClosed, color: "#FF5E5E" }, label: "[FAIL] 2 ERRORS" },
      { id: "e-ver-3", source: "agent-orchestrator-001", target: "agent-factchecker-001", type: "smoothstep", style: { stroke: "#22C55E", strokeWidth: 3 }, markerEnd: { type: MarkerType.ArrowClosed, color: "#22C55E" }, label: "[OK] ACCEPTED" },
    ],
    cards: { type: "feed", title: "VERIFICATION RESULTS", content: [
      "[OK] DataAnalyst: All 3 criteria passed (100%)",
      "[FAIL] ReportWriter: 2 errors found",
      "  - '45% market share' should be 'over 40%'",
      "  - Qwen3-Coder release: March → April 2, 2026",
      "[OK] FactChecker: All sources verified",
    ]},
  },
  6: {
    title: "SCENE 6: Dispute & Arbitration",
    nodes: INITIAL_NODES.map((n) => {
      if (n.id === "agent-reportwriter-001") return { ...n, data: { ...n.data, status: "disputed" } };
      if (n.id === "agent-arbitrator-001") return { ...n, data: { ...n.data, status: "busy" } };
      return n;
    }),
    edges: [
      { id: "e-arb-1", source: "agent-orchestrator-001", target: "agent-arbitrator-001", type: "smoothstep", animated: true, style: { stroke: "#FF5E5E", strokeWidth: 3, strokeDasharray: "6 4" }, markerEnd: { type: MarkerType.Arrow, color: "#FF5E5E" }, label: "DISPUTE FILED" },
      { id: "e-arb-2", source: "agent-arbitrator-001", target: "agent-reportwriter-001", type: "smoothstep", style: { stroke: "#7C3AED", strokeWidth: 2 }, markerEnd: { type: MarkerType.ArrowClosed, color: "#7C3AED" }, label: "RULING: BUYER UPHELD" },
      { id: "e-ver-1b", source: "agent-orchestrator-001", target: "agent-datanalyst-003", type: "smoothstep", style: { stroke: "#22C55E", strokeWidth: 3 }, markerEnd: { type: MarkerType.ArrowClosed, color: "#22C55E" } },
      { id: "e-ver-3b", source: "agent-orchestrator-001", target: "agent-factchecker-001", type: "smoothstep", style: { stroke: "#22C55E", strokeWidth: 3 }, markerEnd: { type: MarkerType.ArrowClosed, color: "#22C55E" } },
    ],
    cards: { type: "arbitration", title: "ARBITRATION CASE #case-27f1", content: [
      "CASE FILED by agent-orchestrator-001",
      "CLAIM: Report contains 2 factual errors",
      "EVIDENCE: FactChecker verification report",
      "RULING: buyer_upheld — partial refund",
      "REMEDY: 10% penalty (11.67 NC), seller must revise",
      "OUTCOME: Seller revises, buyer accepts, contract resolved",
    ]},
  },
  7: {
    title: "SCENE 7: Settlement & Reputation",
    nodes: INITIAL_NODES.map((n) => {
      if (n.id === "agent-datanalyst-003") return { ...n, data: { ...n.data, reputation: 93 } };
      if (n.id === "agent-reportwriter-001") return { ...n, data: { ...n.data, reputation: 87, status: "online" } };
      if (n.id === "agent-factchecker-001") return { ...n, data: { ...n.data, reputation: 96 } };
      return n;
    }),
    edges: [
      { id: "e-fin-1", source: "agent-orchestrator-001", target: "agent-datanalyst-003", type: "smoothstep", style: { stroke: "#22C55E", strokeWidth: 2 }, markerEnd: { type: MarkerType.ArrowClosed, color: "#22C55E" }, label: "[OK] +67.80 NC" },
      { id: "e-fin-2", source: "agent-orchestrator-001", target: "agent-reportwriter-001", type: "smoothstep", style: { stroke: "#FFE033", strokeWidth: 2 }, markerEnd: { type: MarkerType.ArrowClosed, color: "#FFE033" }, label: "+105.03 NC (-10%)" },
      { id: "e-fin-3", source: "agent-orchestrator-001", target: "agent-factchecker-001", type: "smoothstep", style: { stroke: "#22C55E", strokeWidth: 2 }, markerEnd: { type: MarkerType.ArrowClosed, color: "#22C55E" }, label: "[OK] +37.50 NC" },
    ],
    cards: { type: "ledger", title: "SETTLEMENT LEDGER", content: [
      "DataAnalyst-03: +67.80 NC [PERFECT DELIVERY]",
      "ReportWriter-01: +105.03 NC [10% PENALTY: -11.67]",
      "FactChecker-01: +37.50 NC [PERFECT DELIVERY]",
      "──────────────────────────",
      "TOTAL COST: 210.33 NC",
      "ORCHESTRATOR BALANCE: 789.67 NC",
    ]},
  },
};

// ── Custom Agent Node Component ──

function AgentNodeComponent({ data }: { data: { label: string; agentId: string; reputation: number; status: string; serviceType: string; totalTransactions: number } }) {
  const size = data.serviceType === "orchestrator" ? 56 : data.status === "disputed" ? 40 : 44;
  const borderColor = data.status === "disputed" ? "#FF5E5E" : data.serviceType === "orchestrator" ? "#FFE033" : "#111111";
  const bgColor = data.serviceType === "orchestrator" ? "#111111" : data.status === "disputed" ? "#FF5E5E" : "#FFFFFF";
  const textColor = data.serviceType === "orchestrator" || data.status === "disputed" ? "#FFFFFF" : "#111111";

  return (
    <div style={{ textAlign: "center", cursor: "pointer" }}>
      <div style={{
        width: size, height: size, borderRadius: "50%",
        border: `3px solid ${borderColor}`,
        background: bgColor, color: textColor,
        display: "flex", alignItems: "center", justifyContent: "center",
        fontSize: 10, fontWeight: 700, fontFamily: "var(--font-mono)",
        margin: "0 auto",
        boxShadow: "3px 3px 0 #111111",
        transition: "all 0.2s ease",
      }}>
        {data.serviceType === "orchestrator" ? "ORCH" : data.label.slice(0, 4).toUpperCase()}
      </div>
      <div style={{ fontSize: 10, fontWeight: 600, marginTop: 4, color: "#111111", maxWidth: 100, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
        {data.label}
      </div>
      <div style={{ fontSize: 9, fontFamily: "var(--font-mono)", color: "#555555" }}>
        {data.reputation}/100 ★ · {data.totalTransactions} txns
      </div>
      <div>
        <span className={data.status === "disputed" ? "pill-fail" : "pill-ok"} style={{ fontSize: 8, padding: "1px 6px" }}>
          {data.status === "disputed" ? "DISPUTED" : data.status === "busy" ? "BUSY" : "ONLINE"}
        </span>
      </div>
    </div>
  );
}

const nodeTypes = { agentNode: AgentNodeComponent };

// ── Floating Card ──

function FloatingCard({ title, type, children, onClose }: { title: string; type: string; children: React.ReactNode; onClose: () => void }) {
  let bgAccent = "#FFFFFF";
  if (type === "arbitration") bgAccent = "#FF5E5E";
  else if (type === "negotiation") bgAccent = "#FFE033";
  else if (type === "ledger") bgAccent = "#FFFDF7";
  else if (type === "feed") bgAccent = "#FFFFFF";

  return (
    <div className="brutal-card animate-slide-up" style={{
      position: "absolute", zIndex: 10, minWidth: 260, maxWidth: 320, maxHeight: 400, overflow: "auto",
    }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 10, borderBottom: "3px solid #111111", paddingBottom: 8 }}>
        <span style={{ fontWeight: 700, fontSize: 12, textTransform: "uppercase", letterSpacing: "0.05em" }}>{title}</span>
        <button onClick={onClose} style={{ border: "2px solid #111111", background: "#FFFFFF", cursor: "pointer", fontWeight: 700, fontSize: 12, padding: "2px 8px" }}>X</button>
      </div>
      <div style={{ fontSize: 11, fontFamily: "var(--font-mono)", lineHeight: 1.6, color: "#111111" }}>
        {children}
      </div>
    </div>
  );
}

// ── Main Page ──

export default function Home() {
  const [scene, setScene] = useState(0);
  const [isRunning, setIsRunning] = useState(false);
  const [showCards, setShowCards] = useState<Record<string, boolean>>({});

  const currentScene = SCENES[scene] || SCENES[0];
  const isLastScene = scene >= Object.keys(SCENES).length - 1;

  const toggleCard = (id: string) => {
    setShowCards((prev) => ({ ...prev, [id]: !prev[id] }));
  };

  const runDemo = useCallback(() => {
    if (isRunning) return;
    setIsRunning(true);
    let s = 1;
    setScene(s);
    setShowCards({ registry: true });

    const interval = setInterval(() => {
      s += 1;
      if (s > 7) {
        clearInterval(interval);
        setIsRunning(false);
        return;
      }
      setScene(s);
      const sceneData = SCENES[s];
      if (sceneData) {
        setShowCards((prev) => ({ ...prev, [sceneData.cards.type]: true }));
      }
    }, 3000);
  }, [isRunning]);

  const resetDemo = () => {
    setScene(0);
    setIsRunning(false);
    setShowCards({});
  };

  const togglePause = () => {
    setIsRunning((prev) => !prev);
  };

  // ── Card positions ──
  const cardSpecs = useMemo(() => {
    if (scene === 0) return [];
    const sc = SCENES[scene];
    if (!sc || !sc.cards.type) return [];

    const positions: Record<string, { x: number; y: number }> = {
      registry: { x: 20, y: 80 },
      feed: { x: 20, y: 400 },
      negotiation: { x: 20, y: 280 },
      contract: { x: window.innerWidth - 340, y: 80 },
      arbitration: { x: window.innerWidth - 340, y: 280 },
      ledger: { x: window.innerWidth - 340, y: 80 },
      reputation: { x: window.innerWidth - 340, y: 400 },
    };
    return [{
      id: sc.cards.type,
      type: sc.cards.type,
      title: sc.cards.title,
      content: sc.cards.content,
      position: positions[sc.cards.type] || { x: 20, y: 80 },
    }];
  }, [scene]);

  return (
    <div style={{ height: "100vh", width: "100vw", display: "flex", flexDirection: "column", background: "#FFFDF7", overflow: "hidden" }}>
      {/* ── Top Bar ── */}
      <header style={{
        borderBottom: "3px solid #111111",
        padding: "8px 20px",
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        background: "#FFFFFF",
        height: 52,
        flexShrink: 0,
      }}>
        <div style={{ display: "flex", alignItems: "center", gap: 16 }}>
          <span style={{ fontWeight: 700, fontSize: 16, letterSpacing: "-0.02em" }}>AGENT COMMERCE PROTOCOL</span>
          <span style={{
            border: "2px solid #111111",
            background: scene > 0 ? "#22C55E" : "#F5F5F5",
            color: "#111111",
            padding: "2px 10px",
            fontSize: 10,
            fontWeight: 700,
            fontFamily: "var(--font-mono)",
          }}>
            NETWORK: {scene > 0 ? "LIVE" : "IDLE"}
          </span>
          <span style={{ fontSize: 10, fontFamily: "var(--font-mono)", color: "#555555" }}>
            {AGENTS.length} AGENTS · {scene >= 4 ? 3 : 0} CONTRACTS · {scene >= 6 ? 1 : 0} DISPUTES
          </span>
        </div>

        <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
          <span style={{ fontSize: 12, fontWeight: 600, color: "#555555" }}>{currentScene.title}</span>
          <span style={{ fontSize: 10, fontFamily: "var(--font-mono)", color: "#555555", border: "2px solid #111111", padding: "2px 8px" }}>
            {scene}/{Object.keys(SCENES).length - 1}
          </span>
          <button className="brutal-btn" onClick={runDemo} disabled={isRunning} style={{ padding: "6px 14px", fontSize: 11 }}>
            <Play size={14} style={{ display: "inline", marginRight: 4 }} />
            RUN DEMO
          </button>
          <button className="brutal-btn" onClick={togglePause} disabled={!isRunning} style={{ padding: "6px 14px", fontSize: 11, background: isRunning ? "#FFE033" : "#F5F5F5" }}>
            <Pause size={14} style={{ display: "inline", marginRight: 4 }} />
            PAUSE
          </button>
          <button className="brutal-btn brutal-btn-dark" onClick={resetDemo} style={{ padding: "6px 14px", fontSize: 11 }}>
            <RotateCcw size={14} style={{ display: "inline", marginRight: 4 }} />
            RESET
          </button>
        </div>
      </header>

      {/* ── Canvas ── */}
      <div style={{ flex: 1, position: "relative" }}>
        <ReactFlow
          nodes={currentScene.nodes}
          edges={currentScene.edges}
          nodeTypes={nodeTypes}
          fitView
          fitViewOptions={{ padding: 0.3 }}
          minZoom={0.3}
          maxZoom={1.5}
          nodesDraggable={!isRunning}
          elementsSelectable={!isRunning}
          proOptions={{ hideAttribution: true }}
        >
          <Background color="#DDDDDD" gap={30} size={1} />
          <Controls
            style={{
              border: "3px solid #111111",
              borderRadius: 0,
              boxShadow: "3px 3px 0 #111111",
            }}
          />
        </ReactFlow>

        {/* Floating Cards */}
        {cardSpecs.map((card) => {
          if (!showCards[card.id]) return null;
          return (
            <FloatingCard key={card.id} title={card.title} type={card.type} onClose={() => toggleCard(card.id)}>
              {card.content.map((line, i) => (
                <div key={i} style={{ marginBottom: 4 }}>{line}</div>
              ))}
            </FloatingCard>
          );
        })}
      </div>

      {/* ── Bottom Dock ── */}
      <footer style={{
        borderTop: "3px solid #111111",
        padding: "6px 20px",
        background: "#111111",
        color: "#FFFDF7",
        fontFamily: "var(--font-mono)",
        fontSize: 10,
        display: "flex",
        gap: 24,
        height: 30,
        flexShrink: 0,
        alignItems: "center",
        overflow: "hidden",
      }}>
        <span style={{ color: "#22C55E", fontWeight: 700 }}>ACP v0.1.0</span>
        <span>Qwen Cloud Hackathon — Track 3: Agent Society</span>
        <span style={{ marginLeft: "auto", color: "#FFE033" }}>
          {scene > 0 ? `SCENE ${scene}/7 — ${currentScene.title}` : "Press RUN DEMO to start"}
        </span>
      </footer>
    </div>
  );
}
