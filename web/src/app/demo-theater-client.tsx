"use client";

import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import {
  Brain,
  AlertTriangle,
  ChevronLeft,
  ChevronRight,
  CircleDollarSign,
  ClipboardCheck,
  FileArchive,
  FileCheck2,
  FileText,
  Gavel,
  Handshake,
  Inbox,
  PackageCheck,
  Play,
  RotateCcw,
  Search,
  ShieldCheck,
  Square,
  UploadCloud,
} from "lucide-react";

type Tone = "neutral" | "success" | "warning" | "danger" | "qwen" | "contract" | "payment";
type LaneId = "buyer" | "research" | "writer" | "verifier" | "arbitrator" | "ledger";
type PacketMotion =
  | "task-split"
  | "offer"
  | "counter"
  | "accept"
  | "contract"
  | "execute"
  | "artifact"
  | "scan"
  | "case"
  | "ruling"
  | "payment";

type AgentLane = {
  id: LaneId;
  label: string;
  short: string;
  role: string;
  accent: string;
  reputation?: string;
};

type Milestone = {
  key: string;
  label: string;
  phase: string;
  title: string;
  claim: string;
  start: number;
  previewAt: number;
  icon: typeof Brain;
};

type ReplayPacket = {
  id: string;
  showAt: number;
  hideAt?: number;
  lane: LaneId;
  title: string;
  meta: string;
  tone: Tone;
  motion: PacketMotion;
};

type ConsoleEntry = {
  id: string;
  at: number;
  actor: string;
  command: string;
  detail: string;
  tone?: Tone;
};

type Metric = {
  label: string;
  value: string;
  hint: string;
  tone?: Tone;
};

type ReplaySnapshot = {
  milestoneIndex: number;
  milestone: Milestone;
  visiblePackets: ReplayPacket[];
  visibleConsole: ConsoleEntry[];
  metrics: Metric[];
  activeLanes: Set<LaneId>;
  progress: number;
};

type DemoTheaterClientProps = {
  initialSceneIndex: number;
  initialTick: number;
};

const TOTAL_DURATION = 76_000;
const AUTO_STEP_MS = 700;

const LANES: AgentLane[] = [
  {
    id: "buyer",
    label: "Buyer Agent",
    short: "BUYER",
    role: "Posts task, compares offers, accepts work",
    accent: "#FFE033",
    reputation: "100 rep",
  },
  {
    id: "research",
    label: "Research Seller",
    short: "DATA",
    role: "Sources, market facts, vendor data",
    accent: "#22C55E",
    reputation: "92 rep",
  },
  {
    id: "writer",
    label: "Brief Writer",
    short: "WRITE",
    role: "Drafts the AI vendor risk brief",
    accent: "#7C3AED",
    reputation: "88 rep",
  },
  {
    id: "verifier",
    label: "Verifier Agent",
    short: "VERIFY",
    role: "Checks claims against agreement criteria",
    accent: "#14B8A6",
    reputation: "95 rep",
  },
  {
    id: "arbitrator",
    label: "Arbitrator",
    short: "JUDGE",
    role: "Resolves failed delivery disputes",
    accent: "#FF5E5E",
    reputation: "98 rep",
  },
  {
    id: "ledger",
    label: "Settlement Ledger",
    short: "LEDGER",
    role: "Demo credits, penalties, reputation deltas",
    accent: "#111111",
  },
];

const MILESTONES: Milestone[] = [
  {
    key: "plan",
    label: "Plan",
    phase: "01 / Task Decomposition",
    title: "Qwen Reasoning Trace",
    claim: "Buyer Agent turns one request into paid specialist jobs.",
    start: 0,
    previewAt: 5_000,
    icon: Brain,
  },
  {
    key: "find",
    label: "Find",
    phase: "02 / Service Discovery",
    title: "AgentService Registry",
    claim: "The buyer discovers sellers, verifier, and dispute guardrail.",
    start: 9_500,
    previewAt: 12_500,
    icon: Search,
  },
  {
    key: "deal",
    label: "Deal",
    phase: "03 / Live Negotiation",
    title: "Offer -> Counter -> Accept",
    claim: "Agents negotiate concrete price and terms before work starts.",
    start: 19_000,
    previewAt: 29_500,
    icon: Handshake,
  },
  {
    key: "sign",
    label: "Sign",
    phase: "04 / Agreement Snapshot",
    title: "Machine-Verifiable Agreement",
    claim: "Accepted proposals become locked work contracts.",
    start: 31_000,
    previewAt: 33_500,
    icon: FileCheck2,
  },
  {
    key: "deliver",
    label: "Deliver",
    phase: "05 / Seller Execution",
    title: "Artifact Delivery",
    claim: "Sellers execute work and upload deliverables.",
    start: 39_000,
    previewAt: 46_000,
    icon: FileArchive,
  },
  {
    key: "check",
    label: "Check",
    phase: "06 / Independent Verification",
    title: "Claim Scan",
    claim: "Verifier opens the artifact and catches two unsupported claims.",
    start: 48_500,
    previewAt: 52_500,
    icon: ShieldCheck,
  },
  {
    key: "judge",
    label: "Judge",
    phase: "07 / Dispute Resolution",
    title: "Evidence -> Ruling",
    claim: "Failed claims become a dispute case and a structured remedy.",
    start: 58_000,
    previewAt: 62_000,
    icon: Gavel,
  },
  {
    key: "proof",
    label: "Proof",
    phase: "08 / Baseline Proof",
    title: "Multi-Agent Gain",
    claim: "Agent society beats the single-agent baseline.",
    start: 67_000,
    previewAt: 70_000,
    icon: CircleDollarSign,
  },
];

const REPLAY_PACKETS: ReplayPacket[] = [
  {
    id: "task-request",
    showAt: 0,
    hideAt: 16_000,
    lane: "buyer",
    title: "TaskRequest",
    meta: "Create an AI vendor risk brief",
    tone: "qwen",
    motion: "task-split",
  },
  {
    id: "work-research",
    showAt: 2_000,
    hideAt: 20_000,
    lane: "research",
    title: "Work Package",
    meta: "vendor data + sources",
    tone: "success",
    motion: "task-split",
  },
  {
    id: "work-writing",
    showAt: 3_000,
    hideAt: 20_000,
    lane: "writer",
    title: "Work Package",
    meta: "risk brief + citations",
    tone: "qwen",
    motion: "task-split",
  },
  {
    id: "work-verify",
    showAt: 4_000,
    hideAt: 20_000,
    lane: "verifier",
    title: "Work Package",
    meta: "claim-level verification",
    tone: "success",
    motion: "task-split",
  },
  {
    id: "work-arbitrate",
    showAt: 5_000,
    hideAt: 21_000,
    lane: "arbitrator",
    title: "Guardrail",
    meta: "ruling if delivery fails",
    tone: "danger",
    motion: "task-split",
  },
  {
    id: "service-data",
    showAt: 10_500,
    hideAt: 24_000,
    lane: "research",
    title: "AgentService match",
    meta: "92 rep / market research",
    tone: "success",
    motion: "offer",
  },
  {
    id: "service-writer",
    showAt: 11_500,
    hideAt: 24_000,
    lane: "writer",
    title: "AgentService match",
    meta: "88 rep / risk brief drafting",
    tone: "qwen",
    motion: "offer",
  },
  {
    id: "service-verifier",
    showAt: 12_500,
    hideAt: 24_000,
    lane: "verifier",
    title: "AgentService match",
    meta: "95 rep / independent checks",
    tone: "success",
    motion: "offer",
  },
  {
    id: "offer-data",
    showAt: 19_500,
    hideAt: 34_000,
    lane: "research",
    title: "Offer",
    meta: "67.80 NC / 18h",
    tone: "warning",
    motion: "offer",
  },
  {
    id: "offer-writer",
    showAt: 21_000,
    hideAt: 34_000,
    lane: "writer",
    title: "Offer",
    meta: "128.00 NC / report draft",
    tone: "warning",
    motion: "offer",
  },
  {
    id: "counter-writer",
    showAt: 24_000,
    hideAt: 35_000,
    lane: "buyer",
    title: "Counteroffer",
    meta: "116.70 NC + revision clause",
    tone: "qwen",
    motion: "counter",
  },
  {
    id: "accept-stack",
    showAt: 28_500,
    hideAt: 39_000,
    lane: "buyer",
    title: "Accepted",
    meta: "3 proposals locked",
    tone: "success",
    motion: "accept",
  },
  {
    id: "agreement-data",
    showAt: 31_500,
    hideAt: 44_000,
    lane: "research",
    title: "Agreement",
    meta: "sources + data criteria",
    tone: "contract",
    motion: "contract",
  },
  {
    id: "agreement-write",
    showAt: 32_500,
    hideAt: 44_000,
    lane: "writer",
    title: "Agreement",
    meta: "brief + claim checks",
    tone: "contract",
    motion: "contract",
  },
  {
    id: "agreement-verify",
    showAt: 33_500,
    hideAt: 46_000,
    lane: "verifier",
    title: "Agreement",
    meta: "8 acceptance checks",
    tone: "contract",
    motion: "contract",
  },
  {
    id: "research-executing",
    showAt: 39_500,
    hideAt: 51_000,
    lane: "research",
    title: "Executing",
    meta: "collecting vendor evidence",
    tone: "success",
    motion: "execute",
  },
  {
    id: "writer-executing",
    showAt: 40_500,
    hideAt: 51_500,
    lane: "writer",
    title: "Executing",
    meta: "drafting risk brief",
    tone: "qwen",
    motion: "execute",
  },
  {
    id: "artifact-data",
    showAt: 43_500,
    hideAt: 57_000,
    lane: "buyer",
    title: "Artifact received",
    meta: "vendor-data.md passed",
    tone: "success",
    motion: "artifact",
  },
  {
    id: "artifact-brief",
    showAt: 45_000,
    hideAt: 58_500,
    lane: "buyer",
    title: "Artifact received",
    meta: "risk-brief.md needs checking",
    tone: "warning",
    motion: "artifact",
  },
  {
    id: "claim-scan",
    showAt: 48_500,
    hideAt: 63_000,
    lane: "verifier",
    title: "Claim Scan",
    meta: "8 checks running",
    tone: "success",
    motion: "scan",
  },
  {
    id: "failed-claims",
    showAt: 52_500,
    hideAt: 66_000,
    lane: "verifier",
    title: "Failed Claims",
    meta: "2 unsupported claims",
    tone: "danger",
    motion: "scan",
  },
  {
    id: "dispute-case",
    showAt: 58_000,
    hideAt: 70_000,
    lane: "arbitrator",
    title: "Dispute Case",
    meta: "evidence bundle attached",
    tone: "danger",
    motion: "case",
  },
  {
    id: "ruling",
    showAt: 62_000,
    hideAt: 72_500,
    lane: "arbitrator",
    title: "Ruling",
    meta: "revision + 10% penalty",
    tone: "qwen",
    motion: "ruling",
  },
  {
    id: "payment-data",
    showAt: 65_000,
    hideAt: 76_000,
    lane: "ledger",
    title: "Pay DataAnalyst",
    meta: "+67.80 NC / rep +1",
    tone: "payment",
    motion: "payment",
  },
  {
    id: "payment-writer",
    showAt: 65_800,
    hideAt: 76_000,
    lane: "ledger",
    title: "Pay ReportWriter",
    meta: "+105.03 NC / rep -1",
    tone: "warning",
    motion: "payment",
  },
  {
    id: "payment-verifier",
    showAt: 66_600,
    hideAt: 76_000,
    lane: "ledger",
    title: "Pay FactChecker",
    meta: "+37.50 NC / rep +1",
    tone: "payment",
    motion: "payment",
  },
];

const CONSOLE_ENTRIES: ConsoleEntry[] = [
  {
    id: "c01",
    at: 0,
    actor: "BUYER",
    command: "POST /task-requests",
    detail: "Create an AI vendor risk brief for enterprise procurement.",
    tone: "qwen",
  },
  {
    id: "c02",
    at: 1_500,
    actor: "QWEN",
    command: "planner.decompose()",
    detail: "Split into research, writing, verification, and arbitration roles.",
    tone: "qwen",
  },
  {
    id: "c03",
    at: 3_200,
    actor: "BUYER",
    command: "create_work_package",
    detail: "Research package requires cited vendor evidence.",
    tone: "success",
  },
  {
    id: "c04",
    at: 4_500,
    actor: "BUYER",
    command: "create_work_package",
    detail: "Writing package requires claim-level citations.",
    tone: "qwen",
  },
  {
    id: "c05",
    at: 10_500,
    actor: "REGISTRY",
    command: "discover(AgentService)",
    detail: "Matched DataAnalyst-03, ReportWriter-01, FactChecker-01.",
    tone: "success",
  },
  {
    id: "c06",
    at: 14_000,
    actor: "BUYER",
    command: "rank_services",
    detail: "Trust filter keeps independent verifier separate from writer.",
    tone: "success",
  },
  {
    id: "c07",
    at: 19_500,
    actor: "DATA",
    command: "submit_proposal",
    detail: "Offer: 67.80 NC, 18h, 6 evidence tables.",
    tone: "warning",
  },
  {
    id: "c08",
    at: 21_000,
    actor: "WRITE",
    command: "submit_proposal",
    detail: "Offer: 128.00 NC, draft brief with citations.",
    tone: "warning",
  },
  {
    id: "c09",
    at: 24_000,
    actor: "BUYER",
    command: "counter_offer",
    detail: "Counter: 116.70 NC, revision required if verifier fails claims.",
    tone: "qwen",
  },
  {
    id: "c10",
    at: 28_500,
    actor: "WRITE",
    command: "accept_counter",
    detail: "Accepted: price locked, revision clause attached.",
    tone: "success",
  },
  {
    id: "c11",
    at: 31_500,
    actor: "PROTOCOL",
    command: "snapshot_agreement",
    detail: "Agreement stores parties, price, deliverables, checks, remedy terms.",
    tone: "contract",
  },
  {
    id: "c12",
    at: 39_500,
    actor: "DATA",
    command: "execute_delivery",
    detail: "Collecting market evidence and source links.",
    tone: "success",
  },
  {
    id: "c13",
    at: 41_000,
    actor: "WRITE",
    command: "execute_delivery",
    detail: "Composing risk brief from research package.",
    tone: "qwen",
  },
  {
    id: "c14",
    at: 43_500,
    actor: "DATA",
    command: "upload_artifact",
    detail: "vendor-data.md delivered and attached to agreement.",
    tone: "success",
  },
  {
    id: "c15",
    at: 45_000,
    actor: "WRITE",
    command: "upload_artifact",
    detail: "risk-brief.md delivered for verification.",
    tone: "warning",
  },
  {
    id: "c16",
    at: 48_500,
    actor: "VERIFY",
    command: "open_artifact",
    detail: "Scanning 8 acceptance criteria against sources.",
    tone: "success",
  },
  {
    id: "c17",
    at: 52_500,
    actor: "VERIFY",
    command: "flag_failed_claims",
    detail: "2 unsupported claims: market share and release date.",
    tone: "danger",
  },
  {
    id: "c18",
    at: 58_000,
    actor: "BUYER",
    command: "open_dispute",
    detail: "DisputeCase created with verifier evidence bundle.",
    tone: "danger",
  },
  {
    id: "c19",
    at: 61_000,
    actor: "QWEN",
    command: "arbitration_rationale",
    detail: "Agreement requires claim-level citation; failed claims breach criteria.",
    tone: "qwen",
  },
  {
    id: "c20",
    at: 62_000,
    actor: "JUDGE",
    command: "issue_ruling",
    detail: "buyer_upheld: revision required, writer receives 10% penalty.",
    tone: "qwen",
  },
  {
    id: "c21",
    at: 65_000,
    actor: "LEDGER",
    command: "settle_payments",
    detail: "210.33 NC released after penalty; reputation snapshots updated.",
    tone: "payment",
  },
  {
    id: "c22",
    at: 68_000,
    actor: "BASELINE",
    command: "compare_single_agent",
    detail: "Single agent: 4 errors, 320 NC, no independent verification.",
    tone: "danger",
  },
  {
    id: "c23",
    at: 70_000,
    actor: "PROOF",
    command: "measure_gain",
    detail: "Agent society: 50% fewer errors, 34% lower cost, 100% verified.",
    tone: "success",
  },
];

const BIDDING_ROWS = [
  { agent: "DataAnalyst-03", offer: "67.80 NC", counter: "-", final: "Accepted", tone: "success" as Tone, showAt: 19_500 },
  { agent: "ReportWriter-01", offer: "128.00 NC", counter: "116.70 NC", final: "Accepted", tone: "warning" as Tone, showAt: 21_000 },
  { agent: "FactChecker-01", offer: "37.50 NC", counter: "-", final: "Accepted", tone: "success" as Tone, showAt: 23_000 },
];

const CLAIM_ROWS = [
  { label: "Vendor coverage", result: "pass", detail: "source-backed table", showAt: 49_500 },
  { label: "Market share", result: "fail", detail: "45% claim unsupported", showAt: 51_500 },
  { label: "Release date", result: "fail", detail: "wrong April 2026 date", showAt: 52_500 },
  { label: "Risk controls", result: "pass", detail: "criteria satisfied", showAt: 54_000 },
];

function sceneHref(sceneIndex: number, tick?: number) {
  const boundedIndex = Math.max(0, Math.min(MILESTONES.length - 1, sceneIndex));
  const params = new URLSearchParams({ scene: String(boundedIndex + 1) });

  if (typeof tick === "number") {
    params.set("t", String(Math.max(0, Math.min(TOTAL_DURATION, tick))));
  }

  return `/?${params.toString()}`;
}

function getMilestoneIndex(tick: number) {
  let currentIndex = 0;

  for (let index = 0; index < MILESTONES.length; index += 1) {
    if (tick >= MILESTONES[index].start) {
      currentIndex = index;
    }
  }

  return currentIndex;
}

function getMilestoneEnd(index: number) {
  return MILESTONES[index + 1]?.start ?? TOTAL_DURATION;
}

function getMetrics(tick: number): Metric[] {
  if (tick >= 67_000) {
    return [
      { label: "Errors", value: "-50%", hint: "4 -> 2 factual errors", tone: "success" },
      { label: "Cost", value: "-34%", hint: "320 -> 210.33 NC", tone: "success" },
      { label: "Verified", value: "100%", hint: "independent claim checks", tone: "qwen" },
    ];
  }

  if (tick >= 58_000) {
    return [
      { label: "Dispute", value: "1", hint: "opened from failed claims", tone: "danger" },
      { label: "Ruling", value: "buyer", hint: "revision + penalty", tone: "qwen" },
      { label: "Penalty", value: "10%", hint: "writer agreement", tone: "warning" },
    ];
  }

  if (tick >= 48_500) {
    return [
      { label: "Claims", value: "8", hint: "acceptance checks", tone: "success" },
      { label: "Failures", value: "2", hint: "caught before acceptance", tone: "danger" },
      { label: "Verifier", value: "separate", hint: "not the writer", tone: "qwen" },
    ];
  }

  if (tick >= 39_000) {
    return [
      { label: "Artifacts", value: "2", hint: "data + brief", tone: "success" },
      { label: "Status", value: "upload", hint: "seller delivery process", tone: "warning" },
      { label: "Next", value: "verify", hint: "claim scan starts", tone: "qwen" },
    ];
  }

  if (tick >= 31_000) {
    return [
      { label: "Agreements", value: "3", hint: "locked snapshots", tone: "contract" },
      { label: "Criteria", value: "8", hint: "machine-checkable", tone: "qwen" },
      { label: "Escrow", value: "demo", hint: "credit ledger only", tone: "neutral" },
    ];
  }

  if (tick >= 19_000) {
    return [
      { label: "Offers", value: "3", hint: "seller proposals", tone: "warning" },
      { label: "Counter", value: "1", hint: "price + remedy clause", tone: "qwen" },
      { label: "Accepted", value: tick >= 28_500 ? "3" : "0", hint: "locked after negotiation", tone: "success" },
    ];
  }

  if (tick >= 9_500) {
    return [
      { label: "Services", value: "3", hint: "seller + verifier", tone: "success" },
      { label: "Avg rep", value: "91.7", hint: "selected agents", tone: "qwen" },
      { label: "Guardrail", value: "on", hint: "arbitrator reserved", tone: "danger" },
    ];
  }

  return [
    { label: "Task", value: "1", hint: "buyer request", tone: "qwen" },
    { label: "Jobs", value: tick >= 5_000 ? "4" : "splitting", hint: "specialist packages", tone: "success" },
    { label: "Baseline", value: "1 agent", hint: "comparison path", tone: "neutral" },
  ];
}

function useReplayEngine(tick: number): ReplaySnapshot {
  return useMemo(() => {
    const milestoneIndex = getMilestoneIndex(tick);
    const milestone = MILESTONES[milestoneIndex];
    const milestoneStart = milestone.start;
    const milestoneEnd = getMilestoneEnd(milestoneIndex);
    const progress = Math.max(0, Math.min(1, (tick - milestoneStart) / (milestoneEnd - milestoneStart)));
    const visiblePackets = REPLAY_PACKETS.filter((packet) => {
      return tick >= packet.showAt && tick < (packet.hideAt ?? TOTAL_DURATION + 1);
    });
    const visibleConsole = CONSOLE_ENTRIES.filter((entry) => tick >= entry.at).slice(-9);
    const activeLanes = new Set<LaneId>(visiblePackets.map((packet) => packet.lane));

    if (tick < 12_000) activeLanes.add("buyer");
    if (tick >= 48_500 && tick < 58_000) activeLanes.add("verifier");
    if (tick >= 58_000 && tick < 65_000) activeLanes.add("arbitrator");
    if (tick >= 65_000) activeLanes.add("ledger");

    return {
      milestoneIndex,
      milestone,
      visiblePackets,
      visibleConsole,
      metrics: getMetrics(tick),
      activeLanes,
      progress,
    };
  }, [tick]);
}

function formatTime(ms: number) {
  const totalSeconds = Math.floor(ms / 1000);
  const minutes = Math.floor(totalSeconds / 60);
  const seconds = totalSeconds % 60;

  return `${String(minutes).padStart(2, "0")}:${String(seconds).padStart(2, "0")}`;
}

function clampTick(value: number) {
  return Math.max(0, Math.min(TOTAL_DURATION, value));
}

function ExecutionConsole({ entries, tick }: { entries: ConsoleEntry[]; tick: number }) {
  return (
    <section className="execution-console" aria-label="Agent execution console">
      <div className="panel-heading">
        <span>Agent Execution Console</span>
        <strong>{formatTime(tick)}</strong>
      </div>
      <div className="console-task-card">
        <span>TaskRequest</span>
        <strong>Create an AI vendor risk brief</strong>
        <small>Buyer Agent hires specialist agents instead of solving alone.</small>
      </div>
      <div className="console-stream">
        {entries.map((entry) => (
          <div key={entry.id} className={`console-entry console-entry--${entry.tone ?? "neutral"}`}>
            <span>{formatTime(entry.at)}</span>
            <strong>{entry.actor}</strong>
            <code>{entry.command}</code>
            <p>{entry.detail}</p>
          </div>
        ))}
      </div>
    </section>
  );
}

function SwimlaneActor({
  lane,
  isActive,
  children,
}: {
  lane: AgentLane;
  isActive: boolean;
  children: React.ReactNode;
}) {
  return (
    <div className={`swimlane swimlane--${lane.id} ${isActive ? "swimlane--active" : ""}`}>
      <div className="swimlane__actor">
        <div className="swimlane__orb" style={{ background: isActive ? lane.accent : "#FFFFFF" }}>
          {lane.short}
        </div>
        <div>
          <strong>{lane.label}</strong>
          <span>{lane.role}</span>
          {lane.reputation ? <small>{lane.reputation}</small> : null}
        </div>
      </div>
      <div className="swimlane__work">{children}</div>
    </div>
  );
}

function MovingPacket({ packet }: { packet: ReplayPacket }) {
  return (
    <div className={`moving-packet moving-packet--${packet.tone} moving-packet--${packet.motion}`}>
      <span>{packet.title}</span>
      <strong>{packet.meta}</strong>
    </div>
  );
}

function BiddingTable({ tick }: { tick: number }) {
  if (tick < 19_000 || tick >= 36_500) return null;

  return (
    <div className="bidding-table" aria-label="Live bidding table">
      <div className="bidding-table__header">
        <span>Live Bids</span>
        <strong>offer &rarr; counter &rarr; accept</strong>
      </div>
      {BIDDING_ROWS.filter((row) => tick >= row.showAt).map((row) => (
        <div key={row.agent} className={`bidding-row bidding-row--${row.tone}`}>
          <span>{row.agent}</span>
          <strong className="price-tick">{row.offer}</strong>
          <em>{tick >= 24_000 ? row.counter : "waiting"}</em>
          <b className={tick >= 28_500 ? "accept-stamp" : ""}>{tick >= 28_500 ? row.final : "open"}</b>
        </div>
      ))}
    </div>
  );
}

function ArtifactBuilder({ tick }: { tick: number }) {
  if (tick < 39_000 || tick >= 48_500) return null;

  const researchProgress = Math.min(100, Math.max(18, Math.round(((tick - 39_500) / 4_000) * 100)));
  const writingProgress = Math.min(100, Math.max(12, Math.round(((tick - 40_500) / 5_000) * 100)));
  const stages = [
    { label: "Execute", icon: FileText },
    { label: "Package", icon: PackageCheck },
    { label: "Upload", icon: UploadCloud },
    { label: "Buyer inbox", icon: Inbox },
  ];

  return (
    <div className="artifact-builder" aria-label="Artifact delivery process">
      <div className="artifact-builder__header">
        <FileArchive size={16} />
        <strong>Artifact Delivery</strong>
        <span>seller execution &rarr; package &rarr; upload</span>
      </div>
      <div className="artifact-pipeline" aria-label="Delivery pipeline">
        {stages.map((stage) => {
          const StageIcon = stage.icon;
          return (
            <div key={stage.label} className="artifact-stage">
              <StageIcon size={15} />
              <span>{stage.label}</span>
            </div>
          );
        })}
        <div className="artifact-flight artifact-flight--data">
          <FileText size={14} />
          <span>vendor-data.md</span>
        </div>
        <div className="artifact-flight artifact-flight--brief">
          <FileText size={14} />
          <span>risk-brief.md</span>
        </div>
      </div>
      <div className="artifact-file-stack">
        <div className="artifact-job">
          <FileText size={14} />
          <span>vendor-data.md</span>
          <div className="artifact-progress">
            <i style={{ width: `${researchProgress}%` }} />
          </div>
          <strong>{researchProgress >= 100 ? "uploaded" : `${researchProgress}%`}</strong>
        </div>
        <div className="artifact-job artifact-job--warning">
          <FileText size={14} />
          <span>risk-brief.md</span>
          <div className="artifact-progress">
            <i style={{ width: `${writingProgress}%` }} />
          </div>
          <strong>{writingProgress >= 100 ? "uploaded" : `${writingProgress}%`}</strong>
        </div>
      </div>
    </div>
  );
}

function ClaimVerifier({ tick }: { tick: number }) {
  if (tick < 48_500 || tick >= 61_000) return null;

  return (
    <div className="claim-verifier" aria-label="Claim verification scan">
      <div className="claim-verifier__header">
        <ShieldCheck size={16} />
        <strong>Verification Report</strong>
        <span>open artifact &rarr; scan claims</span>
      </div>
      <div className="verification-workbench">
        <div className="artifact-document" aria-label="Opened artifact document">
          <div className="artifact-document__bar">
            <FileText size={14} />
            <strong>risk-brief.md</strong>
            <span>opened</span>
          </div>
          <p className="doc-line doc-line--pass">Vendor coverage includes source-backed risk table.</p>
          <p className={tick >= 51_500 ? "doc-line doc-line--fail" : "doc-line"}>Market share claim: 45% category lead.</p>
          <p className={tick >= 52_500 ? "doc-line doc-line--fail" : "doc-line"}>Release date: April 2026 enterprise GA.</p>
          <p className="doc-line doc-line--pass">Risk controls mapped to agreement criteria.</p>
          <div className="scan-beam" />
        </div>
        <div className="claim-list">
          {CLAIM_ROWS.filter((row) => tick >= row.showAt).map((row) => (
            <div key={row.label} className={`claim-row claim-row--${row.result}`}>
              <span>{row.label}</span>
              <strong>{row.result.toUpperCase()}</strong>
              <small>{row.detail}</small>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

function DisputeDocket({ tick }: { tick: number }) {
  if (tick < 58_000 || tick >= 67_000) return null;

  return (
    <div className="dispute-docket" aria-label="Dispute resolution docket">
      <div className="dispute-docket__case">
        <div>
          <span>DisputeCase</span>
          <strong>Buyer opens claim</strong>
          <small>failed claims + agreement criteria + artifact evidence</small>
        </div>
        <div className="evidence-bundle">
          <FileArchive size={16} />
          <span>evidence.bundle</span>
          <b>2 failed claims</b>
        </div>
      </div>
      <div className="evidence-arrow">EVIDENCE &rarr; ARBITRATOR</div>
      <div className="arbitrator-chamber">
        <Gavel size={18} />
        <span>Arbitrator</span>
        <strong>{tick >= 62_000 ? "Ruling issued" : "Reviewing evidence"}</strong>
        {tick >= 62_000 ? (
          <div className="ruling-card">
            <span>Ruling</span>
            <strong>buyer_upheld</strong>
            <small>revision required + 10% penalty</small>
          </div>
        ) : (
          <div className="ruling-pending">
            <AlertTriangle size={14} />
            <small>agreement criteria breach under review</small>
          </div>
        )}
      </div>
    </div>
  );
}

function LedgerSettlement({ tick }: { tick: number }) {
  if (tick < 65_000 || tick >= 69_000) return null;

  return (
    <div className="ledger-settlement" aria-label="Ledger settlement">
      <div className="ledger-settlement__row ledger-settlement__row--success">
        <span>DataAnalyst</span>
        <strong>+67.80 NC</strong>
        <small>rep +1</small>
      </div>
      <div className="ledger-settlement__row ledger-settlement__row--warning">
        <span>ReportWriter</span>
        <strong>+105.03 NC</strong>
        <small>rep -1 / penalty applied</small>
      </div>
      <div className="ledger-settlement__row ledger-settlement__row--success">
        <span>FactChecker</span>
        <strong>+37.50 NC</strong>
        <small>rep +1</small>
      </div>
    </div>
  );
}

function BaselineReplayStage() {
  const rows = [
    { metric: "Factual errors", single: "4", society: "2", gain: "50% fewer errors", tone: "success" as Tone },
    { metric: "Total cost", single: "320 NC", society: "210.33 NC", gain: "34% lower cost", tone: "success" as Tone },
    { metric: "Independent verification", single: "0%", society: "100%", gain: "100% verified", tone: "qwen" as Tone },
  ];

  return (
    <div className="baseline-replay-stage" aria-label="Single agent versus agent society proof">
      <div className="baseline-replay-stage__headline">
        <span>Single-agent baseline</span>
        <h2>Specialists + verification beat one generalist.</h2>
      </div>
      <div className="baseline-lanes">
        <div className="baseline-lane baseline-lane--single">
          <strong>Single agent</strong>
          <span>one prompt &rarr; one draft &rarr; no independent check</span>
          <b>4 errors / 320 NC / 0% verified</b>
        </div>
        <div className="baseline-lane baseline-lane--society">
          <strong>Agent society</strong>
          <span>hire specialists &rarr; verify &rarr; arbitrate &rarr; settle</span>
          <b>2 errors / 210.33 NC / 100% verified</b>
        </div>
      </div>
      <div className="baseline-proof-grid">
        {rows.map((row) => (
          <div key={row.metric} className={`baseline-proof-card baseline-proof-card--${row.tone}`}>
            <span>{row.metric}</span>
            <strong>{row.gain}</strong>
            <small>
              Single {row.single} &rarr; Society {row.society}
            </small>
          </div>
        ))}
      </div>
    </div>
  );
}

function ActorMap({ activeLanes }: { activeLanes: Set<LaneId> }) {
  return (
    <div className="actor-map" aria-label="Compact actor map">
      {LANES.slice(0, 5).map((lane, index) => (
        <div
          key={lane.id}
          className={`actor-map__node actor-map__node--${lane.id} ${
            activeLanes.has(lane.id) ? "actor-map__node--active" : ""
          }`}
          style={{ "--node-index": index } as React.CSSProperties}
        >
          {lane.short}
        </div>
      ))}
    </div>
  );
}

function CommerceProcessBoard({ snapshot, tick }: { snapshot: ReplaySnapshot; tick: number }) {
  if (snapshot.milestone.key === "proof") {
    return (
      <section className="commerce-board commerce-board--proof" aria-label="Commerce baseline proof">
        <BaselineReplayStage />
      </section>
    );
  }

  return (
    <section className="commerce-board" aria-label="Commerce process board">
      <div className="commerce-board__top">
        <div>
          <span>{snapshot.milestone.phase}</span>
          <h1>{snapshot.milestone.claim}</h1>
        </div>
        <ActorMap activeLanes={snapshot.activeLanes} />
      </div>

      <div className="swimlane-stack">
        {LANES.filter((lane) => lane.id !== "ledger" || tick >= 58_000).map((lane) => (
          <SwimlaneActor key={lane.id} lane={lane} isActive={snapshot.activeLanes.has(lane.id)}>
            {snapshot.visiblePackets
              .filter((packet) => packet.lane === lane.id)
              .map((packet) => (
                <MovingPacket key={packet.id} packet={packet} />
              ))}
          </SwimlaneActor>
        ))}
      </div>

      <BiddingTable tick={tick} />
      <ArtifactBuilder tick={tick} />
      <ClaimVerifier tick={tick} />
      <DisputeDocket tick={tick} />
      <LedgerSettlement tick={tick} />
    </section>
  );
}

function ProofBar({ metrics }: { metrics: Metric[] }) {
  return (
    <div className="proof-bar" aria-label="Current proof metrics">
      {metrics.map((metric) => (
        <div key={metric.label} className={`proof-card proof-card--${metric.tone ?? "neutral"}`}>
          <span>{metric.label}</span>
          <strong>{metric.value}</strong>
          <small>{metric.hint}</small>
        </div>
      ))}
    </div>
  );
}

function ReasoningPanel({ snapshot, tick }: { snapshot: ReplaySnapshot; tick: number }) {
  const lines =
    tick >= 58_000
      ? [
          "Agreement requires claim-level citations.",
          "Verifier evidence shows two unsupported claims.",
          "Remedy: buyer_upheld, revision required, 10% penalty.",
        ]
      : tick >= 48_500
        ? [
            "Open risk-brief.md artifact.",
            "Scan every acceptance criterion against source evidence.",
            "Escalate failed claims into dispute-ready evidence.",
          ]
        : tick >= 19_000
          ? [
              "Compare price, delivery time, reputation, and remedy clause.",
              "Counter the writer's high offer with penalty-backed terms.",
              "Accept only proposals that are verifiable after delivery.",
            ]
          : [
              "Decompose buyer request into commercially bounded work.",
              "Assign specialist roles before execution starts.",
              "Keep verification and arbitration independent from the writer.",
            ];

  return (
    <aside className="reasoning-panel" aria-label="Reasoning trace">
      <div className="panel-heading">
        <span>{snapshot.milestone.title}</span>
        <strong>{Math.round(snapshot.progress * 100)}%</strong>
      </div>
      <div className="reasoning-card">
        <Brain size={18} />
        <strong>Deterministic cached replay</strong>
        <p>Visible Qwen-style reasoning path for planning, negotiation, verification, arbitration, and settlement.</p>
      </div>
      <div className="reasoning-lines">
        {lines.map((line) => (
          <div key={line} className="reasoning-line">
            <ClipboardCheck size={14} />
            <span>{line}</span>
          </div>
        ))}
      </div>
      <div className="scene-takeaway">
        <span>Judge takeaway</span>
        <strong>{snapshot.milestone.claim}</strong>
      </div>
    </aside>
  );
}

function parseInitialTick(sceneIndex: number, initialTick: number) {
  if (Number.isFinite(initialTick) && initialTick >= 0) {
    return clampTick(initialTick);
  }

  return MILESTONES[Math.max(0, Math.min(MILESTONES.length - 1, sceneIndex))].previewAt;
}

export default function DemoTheaterClient({ initialSceneIndex, initialTick }: DemoTheaterClientProps) {
  const [tick, setTick] = useState(() => parseInitialTick(initialSceneIndex, initialTick));
  const [isAutoRunning, setIsAutoRunning] = useState(false);
  const timerRef = useRef<ReturnType<typeof setInterval> | null>(null);
  const snapshot = useReplayEngine(tick);
  const CurrentIcon = snapshot.milestone.icon;

  const updateUrl = useCallback((nextTick: number) => {
    const sceneIndex = getMilestoneIndex(nextTick);
    window.history.replaceState(null, "", sceneHref(sceneIndex, nextTick));
  }, []);

  const stopAuto = useCallback(() => {
    if (timerRef.current !== null) {
      clearInterval(timerRef.current);
      timerRef.current = null;
    }
    setIsAutoRunning(false);
  }, []);

  const jumpToScene = useCallback(
    (sceneIndex: number) => {
      stopAuto();
      const boundedIndex = Math.max(0, Math.min(MILESTONES.length - 1, sceneIndex));
      const nextTick = MILESTONES[boundedIndex].previewAt;
      setTick(nextTick);
      updateUrl(nextTick);
    },
    [stopAuto, updateUrl],
  );

  const resetDemo = useCallback(() => {
    jumpToScene(0);
  }, [jumpToScene]);

  const startAuto = useCallback(() => {
    if (timerRef.current !== null) return;
    setIsAutoRunning(true);
    timerRef.current = setInterval(() => {
      setTick((currentTick) => {
        const nextTick = clampTick(currentTick + AUTO_STEP_MS);

        if (nextTick >= TOTAL_DURATION) {
          if (timerRef.current !== null) {
            clearInterval(timerRef.current);
            timerRef.current = null;
          }
          setIsAutoRunning(false);
        }

        window.history.replaceState(null, "", sceneHref(getMilestoneIndex(nextTick), nextTick));
        return nextTick;
      });
    }, AUTO_STEP_MS);
  }, []);

  useEffect(() => stopAuto, [stopAuto]);

  return (
    <div className="demo-theater">
      <header className="theater-header">
        <div className="brand-lockup">
          <div className="brand-mark">CO</div>
          <div>
            <div className="brand-title">CoAgenta</div>
            <div className="brand-subtitle">Track 3: Agent Society | ACP-powered commerce replay</div>
          </div>
        </div>

        <div className="scene-header">
          <div className="scene-header__kicker">{snapshot.milestone.phase}</div>
          <div className="scene-header__title">
            <CurrentIcon size={18} />
            {snapshot.milestone.claim}
          </div>
        </div>

        <div className="control-strip">
          <a
            className="icon-button"
            href={sceneHref(snapshot.milestoneIndex - 1)}
            aria-label="Previous milestone"
            onClick={(event) => {
              event.preventDefault();
              jumpToScene(snapshot.milestoneIndex - 1);
            }}
          >
            <ChevronLeft size={16} />
            Prev
          </a>
          <a
            className="icon-button icon-button--primary"
            href={sceneHref(snapshot.milestoneIndex + 1)}
            aria-label="Next milestone"
            onClick={(event) => {
              event.preventDefault();
              jumpToScene(snapshot.milestoneIndex + 1);
            }}
          >
            <ChevronRight size={16} />
            Next
          </a>
          <button
            className="icon-button"
            type="button"
            aria-label={isAutoRunning ? "Stop demo replay" : "Run demo replay"}
            onClick={isAutoRunning ? stopAuto : startAuto}
          >
            {isAutoRunning ? <Square size={14} /> : <Play size={15} />}
            {isAutoRunning ? "Stop" : "Run Demo"}
          </button>
          <a
            className="icon-button icon-button--dark"
            href={sceneHref(0)}
            aria-label="Reset demo"
            onClick={(event) => {
              event.preventDefault();
              resetDemo();
            }}
          >
            <RotateCcw size={15} />
            Reset
          </a>
        </div>
      </header>

      <main className="theater-main">
        <aside className="timeline-panel" aria-label="Demo milestones">
          <div className="panel-heading">
            <span>Replay Timeline</span>
            <strong>{formatTime(tick)}</strong>
          </div>
          <div className="timeline-list">
            {MILESTONES.map((item, index) => {
              const StepIcon = item.icon;
              const isActive = index === snapshot.milestoneIndex;
              const isComplete = index < snapshot.milestoneIndex;
              return (
                <a
                  key={item.key}
                  href={sceneHref(index)}
                  className={`timeline-step ${isActive ? "timeline-step--active" : ""} ${
                    isComplete ? "timeline-step--complete" : ""
                  }`}
                  onClick={(event) => {
                    event.preventDefault();
                    jumpToScene(index);
                  }}
                >
                  <span className="timeline-step__index">{String(index + 1).padStart(2, "0")}</span>
                  <span className="timeline-step__icon">
                    <StepIcon size={16} />
                  </span>
                  <span className="timeline-step__body">
                    <strong>{item.label}</strong>
                    <small>{item.title}</small>
                  </span>
                </a>
              );
            })}
          </div>
        </aside>

        <ExecutionConsole entries={snapshot.visibleConsole} tick={tick} />

        <section
          className={`replay-stage ${snapshot.milestone.key === "proof" ? "replay-stage--proof" : ""}`}
          aria-label="Agent commerce replay stage"
        >
          <CommerceProcessBoard snapshot={snapshot} tick={tick} />
          {snapshot.milestone.key === "proof" ? null : <ProofBar metrics={snapshot.metrics} />}
        </section>

        <ReasoningPanel snapshot={snapshot} tick={tick} />
      </main>
    </div>
  );
}
